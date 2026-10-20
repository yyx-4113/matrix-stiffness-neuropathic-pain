#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layer-1 diagnostics - audit whether the observed signature concordance survives
a null that is matched on baseline expression level.

Why this exists: the raw permutation null samples genes at random, ignoring that
log2_fc depends on baseline expression. If signature genes sit at a particular
expression stratum, a random-sample null will flag them as "concordant" purely
because of that coupling. This script quantifies the problem and provides the
expression-matched (decile-stratified) null used downstream.

Outputs: analysis/results/layer1/layer1_diag.json
"""

import json
import os
import sys

import numpy as np
import openpyxl
import pandas as pd
from scipy import stats as sps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CFG = os.path.join(ROOT, "analysis", "config", "ms_panel.json")
RAW = os.path.join(ROOT, "analysis", "data", "raw")
L0 = os.path.join(ROOT, "analysis", "results", "layer0")
OUT = os.path.join(ROOT, "analysis", "results", "layer1")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)

from layer1_projection import TABLES, load_table, human_to_mouse  # noqa: E402


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    q = p[o] * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[o] = q
    return np.clip(out, 0, 1)


def ranks_of(df, var):
    order = np.argsort(df[var].to_numpy(), kind="mergesort")
    arr = np.empty(len(df))
    arr[order] = np.arange(len(df))
    return pd.Series(arr, index=df.index)


def _without_replacement(n_perm, m, n, rng, block=2000, max_retry=25):
    """n_perm index rows, each holding m DISTINCT indices drawn from [0, n).

    m << n here, so rejection sampling is far cheaper than permuting the whole
    background: a collision occurs in only a few percent of rows.
    """
    idx = rng.integers(0, n, size=(n_perm, m))
    for _ in range(max_retry):
        dup = np.array([np.unique(r).size < m for r in idx])
        if not dup.any():
            break
        idx[dup] = rng.integers(0, n, size=(int(dup.sum()), m))
    return idx


def _stratified_draws(rk, member_bins, pool_by_bin, n_perm, rng, max_retry=25):
    """Draw a distinct gene per member, each from that member's expression decile.

    rk is a pandas Series indexed by gene symbol, so pool entries are SYMBOLS and
    must be looked up with .loc -- indexing the underlying numpy value array with
    symbol strings raises IndexError.
    """
    out = np.empty((n_perm, len(member_bins)), dtype=float)
    for _ in range(max_retry):
        rows_ok = np.ones(n_perm, dtype=bool)
        picks = []
        for b in member_bins:
            pool = pool_by_bin[b]
            pick = pool[rng.integers(0, len(pool), n_perm)]
            for prev in picks:
                rows_ok &= ~(pick == prev)      # collision in this permutation row
            picks.append(pick)
        for j, pick in enumerate(picks):
            out[:, j] = rk.loc[pick].to_numpy()
        if rows_ok.all():
            return out
    return out


def main():
    cfg = json.load(open(CFG, encoding="utf-8"))
    sig = json.load(open(os.path.join(L0, "layer0_signature.json"), encoding="utf-8"))
    rank_var = cfg["layer1"]["rank_test"]["primary_ranking_variable"]
    n_perm = cfg["layer1"]["rank_test"]["permutation"]["n_iterations"]
    seed = cfg["layer1"]["rank_test"]["permutation"]["seed"]

    # mouse / human matched dictionary is not needed here: Layer-0 already gave
    # us sets; a companion file maps human->mouse. Reproduce it cheaply.
    H2M = {g: (g[0] + g[1:].lower() if g.isupper() else g) for g in
           {x for v in sig["sets"].values() for x in v}}

    report = {"per_contrast": {}, "stratified_vs_unstratified": []}
    rng = np.random.default_rng(seed)

    print("[DIAG] expression-independent null audit\n")
    hdr = f"{'contrast':12s} {'n_expr':>7s} {'zero%':>7s} {'rho(fc,base)':>13s} {'base_KS_D':>10s} {'p_KS':>9s}"
    print(hdr)
    print("-" * len(hdr))

    for (tissue, model), fn in sorted(TABLES.items()):
        df = load_table(os.path.join(RAW, fn))
        df = df.dropna(subset=[rank_var, "symbol"])
        df = df.drop_duplicates(subset="symbol", keep="first").set_index("symbol")

        n = len(df)
        base = df["value_CTR"].to_numpy()
        fc = df[rank_var].to_numpy()
        zero_pct = float((base == 0).mean() * 100)

        # (a) coupling between fold change and baseline expression
        sub = base > 0
        rho, _ = sps.spearmanr(base[sub], fc[sub])

        # (b) are signature genes at a different expression stratum?
        ks_rows = []
        all_present = []
        for key, members in sig["sets"].items():
            present = [H2M[g] for g in members if H2M[g] in df.index]
            if not present:
                continue
            all_present += present
        all_present = sorted(set(all_present))
        if all_present:
            ks = sps.ks_2samp(df.loc[all_present, "value_CTR"].to_numpy(), base)
            ks_D, ks_p = float(ks.statistic), float(ks.pvalue)
        else:
            ks_D, ks_p = float("nan"), float("nan")

        report["per_contrast"][f"{tissue}_{model}"] = {
            "n_genes": int(n),
            "pct_baseline_zero": round(zero_pct, 3),
            "spearman_log2fc_vs_baseline": round(float(rho), 5),
            "n_signature_members_present": len(all_present),
            "signature_vs_background_baseline_KS_D": round(ks_D, 5),
            "signature_vs_background_baseline_KS_p": round(ks_p, 6),
            "baseline_median_signature": round(float(np.median(df.loc[all_present, 'value_CTR'])), 4) if all_present else None,
            "baseline_median_background": round(float(np.median(base)), 4),
        }
        print(f"{tissue+'_'+model:12s} {n:7d} {zero_pct:7.2f} {rho:13.4f} {ks_D:10.4f} {ks_p:9.5f}")

    # ---------------- (c) stratified vs unstratified null -------------------
    print("\n[DIAG] expression-matched (decile-stratified) permutation null\n")
    rows = []
    for (tissue, model), fn in sorted(TABLES.items()):
        df = load_table(os.path.join(RAW, fn))
        df = df.dropna(subset=[rank_var, "symbol"])
        df = df.drop_duplicates(subset="symbol", keep="first").set_index("symbol")
        n = len(df)
        # restrict to expressed genes: undetected loci carry no interpretable FC
        expressed = df["value_CTR"] > 0
        dfe = df[expressed].copy()
        ne = len(dfe)
        # decile bins on baseline expression among expressed genes
        base = dfe["value_CTR"].to_numpy()
        order = np.argsort(base, kind="mergesort")
        bin_of = np.empty(ne, dtype=int)
        decile_edges = np.array_split(np.arange(ne), 10)
        for b, idxs in enumerate(decile_edges):
            bin_of[idxs] = b
        dfe["bin"] = bin_of
        # recompute ranks within the expressed background
        rk = ranks_of(dfe, rank_var) / (ne - 1)

        for key in ["hippo_dependent_up", "hippo_dependent_down",
                    "hippo_independent_up", "hippo_independent_down"]:
            members = [H2M[g] for g in sig["sets"].get(key, []) if H2M[g] in dfe.index]
            if len(members) < 3:
                continue
            obs = float(np.median(rk.loc[members].to_numpy()))
            # stratified null: for each member draw a gene from the same decile
            member_bins = dfe.loc[members, "bin"].to_numpy()
            pool_by_bin = {b: dfe.index[dfe["bin"] == b].to_numpy() for b in range(10)}
            draws = _stratified_draws(rk, member_bins, pool_by_bin, n_perm, rng)
            perm = np.median(draws, axis=1)
            p_strat = (int((np.abs(perm - 0.5) >= abs(obs - 0.5)).sum()) + 1) / (n_perm + 1)
            # unstratified null for comparison, sampled WITHOUT replacement too
            # (v0.4 R6) so that the stratified/unstratified contrast reflects
            # expression matching alone and not a difference in sampling scheme.
            idx = _without_replacement(n_perm, len(members), ne, rng)
            perm2 = np.median(rk.to_numpy()[idx], axis=1)
            p_un = (int((np.abs(perm2 - 0.5) >= abs(obs - 0.5)).sum()) + 1) / (n_perm + 1)
            rows.append({
                "signature": key, "tissue": tissue, "model": model,
                "n_present": len(members), "n_background_expressed": ne,
                "MRU_stratified_space": round(obs, 5),
                "p_unstratified": round(p_un, 6),
                "p_expression_matched": round(p_strat, 6),
            })
    rows = pd.DataFrame(rows)
    rows["q_expression_matched"] = np.nan
    for k in rows["signature"].unique():
        m = rows["signature"] == k
        rows.loc[m, "q_expression_matched"] = bh(rows.loc[m, "p_expression_matched"].to_numpy())
    rows = rows.sort_values(["signature", "tissue", "model"])
    print(rows.to_string(index=False))

    report["stratified_vs_unstratified"] = rows.to_dict("records")
    with open(os.path.join(OUT, "layer1_diag.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print("\n[DIAG] wrote layer1_diag.json")


if __name__ == "__main__":
    main()
