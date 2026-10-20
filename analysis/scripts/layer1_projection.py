#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layer 1 - Project the frozen stiffness signature onto the pain datasets.

This script is the FIRST consumption of GSE111216 expression content (milestone
M3). Every rule comes from analysis/config/ms_panel.json, frozen as protocol
v0.2 BEFORE the Layer-1 tables were read.

Outputs (analysis/results/layer1/):
  layer1_results.json       all endpoint statistics incl. permutation P and BH q
  layer1_endpoint_table.csv one row per (tissue x model x signature)
  layer1_gene_level.csv     per-member statistics in every contrast
  layer1_diagnostics.json   table integrity + mapping rates
"""

import json
import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd

# ---------------------------------------------------------------- paths ----
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CFG_PATH = os.path.join(ROOT, "analysis", "config", "ms_panel.json")
RAW_DIR = os.path.join(ROOT, "analysis", "data", "raw")
L0_DIR = os.path.join(ROOT, "analysis", "results", "layer0")
OUT_DIR = os.path.join(ROOT, "analysis", "results", "layer1")
os.makedirs(OUT_DIR, exist_ok=True)

TABLES = {
    ("BRN", "CFA"): "GSE111216_Parisien_Suppl_Table_01_gene_BRN_CTRvsCFA.xlsx",
    ("BRN", "SNI"): "GSE111216_Parisien_Suppl_Table_02_gene_BRN_CTRvsSNI.xlsx",
    ("SC", "CFA"): "GSE111216_Parisien_Suppl_Table_03_gene_SC_CTRvsCFA.xlsx",
    ("SC", "SNI"): "GSE111216_Parisien_Suppl_Table_04_gene_SC_CTRvsSNI.xlsx",
    ("DRG", "CFA"): "GSE111216_Parisien_Suppl_Table_05_gene_DRG_CTRvsCFA.xlsx",
    ("DRG", "SNI"): "GSE111216_Parisien_Suppl_Table_06_gene_DRG_CTRvsSNI.xlsx",
    ("BLD", "CFA"): "GSE111216_Parisien_Suppl_Table_07_gene_BLD_CTRvsCFA.xlsx",
    ("BLD", "SNI"): "GSE111216_Parisien_Suppl_Table_08_gene_BLD_CTRvsSNI.xlsx",
}


def human_to_mouse(sym):
    """Symbol mapping rule from the frozen config.

    Standard capitalisation convention: all-uppercase human symbols map to the
    mouse form by capitalising the first letter and lower-casing the rest.
    Symbols already in mixed case are left unchanged.
    """
    if sym.isupper():
        return sym[0] + sym[1:].lower()
    return sym


def _perm_median_rank(rank_vals, n_perm, m, rng, block=2000, max_retry=25):
    """Median rank of WITHOUT-replacement size-m random gene sets.

    Because m << n here (m ~ 7-41 against n ~ 1.5e4 background genes), an
    exact without-replacement draw is well approximated by rejection sampling:
    draw m indices and redraw only the rare rows that contain a duplicate
    (collision probability ~3.6% at m=33). This keeps the cost at O(n_perm * m)
    instead of O(n_perm * n), which is what made a full-permutation pass over
    all signature x contrast pairs intractable.
    """
    n = len(rank_vals)
    out = np.empty(n_perm, dtype=float)
    start = 0
    while start < n_perm:
        stop = min(start + block, n_perm)
        k = stop - start
        idx = rng.integers(0, n, size=(k, m))
        for _ in range(max_retry):
            nuniq = np.array([np.unique(row).size for row in idx])
            dup = nuniq < m
            if not dup.any():
                break
            idx[dup] = rng.integers(0, n, size=(int(dup.sum()), m))
        out[start:stop] = np.median(rank_vals[idx], axis=1)
        start = stop
    return out


def load_table(path):
    """Read one deposited per-contrast xlsx into a DataFrame indexed by gene."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)
    header = [str(c).strip() if c is not None else "" for c in next(rows)]
    data = []
    for r in rows:
        if r is None or all(v is None for v in r):
            continue
        data.append(r)
    df = pd.DataFrame(data, columns=header)
    wb.close()
    df = df.rename(columns={"gene": "symbol"})
    for c in ["value_CTR", "p_value", "log2_fc", "log2_fcZ", "pi_value"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def bh(pvals):
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    order = np.argsort(p)
    q = p[order] * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0, 1)
    out = np.empty(n)
    out[order] = q
    return out


def main():
    with open(CFG_PATH, encoding="utf-8") as fh:
        cfg = json.load(fh)
    with open(os.path.join(L0_DIR, "layer0_signature.json"), encoding="utf-8") as fh:
        sig = json.load(fh)

    l1 = cfg["layer1"]
    rt = l1["rank_test"]
    n_perm = rt["permutation"]["n_iterations"]
    seed = rt["permutation"]["seed"]
    ranking_var = rt["primary_ranking_variable"]

    families = ["hippo_dependent", "hippo_independent"]
    directions = ["up", "down"]
    sets = sig["sets"]

    print("[L1] loading GSE111216 contrast tables ...")
    tables = {}
    diag_tables = {}
    for (tissue, model), fn in TABLES.items():
        path = os.path.join(RAW_DIR, fn)
        df = load_table(path)
        n_raw = len(df)
        # drop rows without a usable ranking statistic
        df = df.dropna(subset=[ranking_var, "symbol"])
        n_dup = int(df["symbol"].duplicated().sum())
        df = df.drop_duplicates(subset="symbol", keep="first").set_index("symbol")
        tables[(tissue, model)] = df
        diag_tables[f"{tissue}_{model}"] = {
            "file": fn,
            "rows": int(n_raw),
            "rows_with_ranking_statistic": int(len(df)),
            "duplicate_symbols_dropped": n_dup,
            "author_deg_p05": int((df["p_value"] < 0.05).sum()),
            "author_deg_p01": int((df["p_value"] < 0.01).sum()),
            "median_log2fc": round(float(df[ranking_var].median()), 6),
        }
        print(f"      {tissue}_{model}: {len(df)} genes, "
              f"DEG(p<0.05) = {diag_tables[f'{tissue}_{model}']['author_deg_p05']}")

    print("[L1] mapping human signature -> mouse symbols ...")
    mapping_report = {}
    mapped_sets = {}
    for key, members in sets.items():
        mapped = {}
        for g in members:
            ms = human_to_mouse(g)
            mapped[g] = ms
        mapping_report[key] = {
            "n_human": len(members),
            "n_matched_in_DRG_SNI_example": int(
                sum(m in tables[("DRG", "SNI")].index for m in mapped.values())
            ),
            "unmatched": [m for m in mapped.values() if m not in tables[("DRG", "SNI")].index],
        }
        mapped_sets[key] = mapped

    n_to_rank = len(tables[("DRG", "SNI")])

    # ------------------- rank projections ---------------------------------
    print(f"[L1] rank-based projection, {n_perm} permutations, seed {seed} ...")
    rng = np.random.default_rng(seed)
    endpoints = []
    gene_rows = []

    for key, members in sets.items():
        fam, direction = key.rsplit("_", 1)
        for (tissue, model), df in sorted(tables.items()):
            # Rank ascending by the ranking variable -> high rank = up-regulated
            # in the pain model. Ties broken by stable position (mergesort).
            vals = df[ranking_var].to_numpy()
            order = np.argsort(vals, kind="mergesort")
            rank_arr = np.empty(len(df), dtype=float)
            rank_arr[order] = np.arange(len(df), dtype=float)
            ranks = pd.Series(rank_arr, index=df.index)
            mouse_in_table = [mapped_sets[key][g] for g in members]
            present = [m for m in mouse_in_table if m in df.index]
            if len(present) == 0:
                continue
            member_ranks = ranks.loc[present].to_numpy()

            n = len(df)
            m = len(present)
            # Wilcoxon rank-sum z (Mann-Whitney U standardised).
            # v0.4 R5 (audit finding A4): ranks here are 0-based (0 .. n-1), so the
            # null expectation of the rank sum is m*(n-1)/2, NOT m*(n+1)/2. The
            # previous 1-based mean biased every z downward by m/sd. The variance
            # is translation-invariant and unchanged.
            U = member_ranks.sum()
            mu = m * (n - 1) / 2.0
            sd = np.sqrt(m * (n - m) * (n + 1) / 12.0)
            z = (U - mu) / sd
            # normalised median-rank difference (MRU): 0.5 = no shift
            mru = float(np.median(member_ranks) / (n - 1))
            # permutation null: size-matched random gene sets, WITHOUT
            # replacement (v0.4 R6 / audit finding A5). Sampling with replacement
            # duplicates genes, shrinking the effective module size and widening the
            # null; measured duplicate rate was 3.35% of draws.
            rank_vals = ranks.to_numpy()
            perm_mru = _perm_median_rank(rank_vals, n_perm, m, rng) / (n - 1)
            obs_shift = mru - 0.5
            perm_shift = perm_mru - 0.5
            n_extreme = int((np.abs(perm_shift) >= abs(obs_shift)).sum())
            p_perm = (n_extreme + 1) / (n_perm + 1)

            # Fisher overlap with the authors' DEG calls
            deg05 = set(df.index[df["p_value"] < 0.05])
            deg01 = set(df.index[df["p_value"] < 0.01])
            res = {}
            for thr, deg in [(0.05, deg05), (0.01, deg01)]:
                a = len(set(present) & deg)
                b = len(set(present)) - a
                c = len(deg) - a
                d = n - a - b - c
                try:
                    from scipy.stats import fisher_exact
                    orr, pf = fisher_exact([[a, b], [c, d]])
                except Exception:
                    orr, pf = float("nan"), float("nan")
                res[f"p{thr}"] = {"a": a, "b": b, "c": c, "d": d, "odds_ratio": None if np.isnan(orr) else round(float(orr), 4), "p_fisher": None if np.isnan(pf) else float(pf)}

            level = "exploratory"
            for lvl, items in l1["endpoint_level"].items():
                for it in items:
                    if isinstance(it, dict) and it["tissue"] == tissue and it["model"] == model and f"{it['signature']}" == f"HD_{direction}":
                        level = lvl

            endpoints.append({
                "signature": key,
                "family": fam,
                "direction": direction,
                "tissue": tissue,
                "model": model,
                "endpoint_level": level if fam == "hippo_dependent" else "exploratory",
                "n_signature_human": len(members),
                "n_mapped_and_present": len(present),
                "mapping_rate": round(len(present) / max(len(members), 1), 4),
                "n_background_genes": n,
                "mean_rank_of_members": round(float(member_ranks.mean()), 2),
                "background_mean_rank": round(float((n - 1) / 2), 2),
                "median_rank_of_members": float(np.median(member_ranks)),
                "MRU": round(mru, 6),
                "wilcoxon_z": round(float(z), 4),
                "p_permutation": round(float(p_perm), 6),
                "n_permutations": n_perm,
                "seed": seed,
                "fisher_overlap": res,
                "members_present": sorted(present),
            })

            for g in members:
                ms = mapped_sets[key][g]
                if ms not in df.index:
                    gene_rows.append({"signature": key, "human": g, "mouse": ms,
                                      "tissue": tissue, "model": model,
                                      "in_table": False})
                    continue
                row = df.loc[ms]
                gene_rows.append({
                    "signature": key, "human": g, "mouse": ms,
                    "tissue": tissue, "model": model, "in_table": True,
                    "log2_fc": None if pd.isna(row[ranking_var]) else round(float(row[ranking_var]), 6),
                    "log2_fcZ": None if pd.isna(row["log2_fcZ"]) else round(float(row["log2_fcZ"]), 6),
                    "p_value": None if pd.isna(row["p_value"]) else float(row["p_value"]),
                    "value_CTR": None if pd.isna(row["value_CTR"]) else round(float(row["value_CTR"]), 4),
                    "value_model": None if pd.isna(row[f"value_{model}"]) else round(float(row[f"value_{model}"]), 4),
                    "floor_limited": bool(row["value_CTR"] <= 1 and row[f"value_{model}"] <= 1),
                    "rank": int(ranks.loc[ms]),
                })

    ep = pd.DataFrame(endpoints)

    # BH within each family x direction family (16 base tests each)
    for fam in families:
        for direction in directions:
            mask = (ep.family == fam) & (ep.direction == direction)
            if mask.sum() == 0:
                continue
            ep.loc[mask, "q_BH"] = bh(ep.loc[mask, "p_permutation"].to_numpy())
    ep["q_BH"] = ep["q_BH"].round(6)

    ep = ep.sort_values(["endpoint_level", "family", "direction", "tissue", "model"])
    ep.to_csv(os.path.join(OUT_DIR, "layer1_endpoint_table.csv"), index=False)
    pd.DataFrame(gene_rows).to_csv(os.path.join(OUT_DIR, "layer1_gene_level.csv"), index=False)

    min_rate = l1["species_mapping"]["min_acceptable_mapping_rate"]
    primary_rows = ep[ep.endpoint_level == "primary"].to_dict("records")
    downgraded = [r for r in primary_rows if r["mapping_rate"] < min_rate]

    with open(os.path.join(OUT_DIR, "layer1_results.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "_tag": cfg["_tag"],
            "_protocol": cfg["_protocol"],
            "source": "GSE111216",
            "ranking_variable": ranking_var,
            "permutation": {"n": n_perm, "seed": seed},
            "endpoints": ep.to_dict("records"),
            "primary_endpoint": primary_rows,
            "primary_downgraded_due_to_mapping": downgraded,
        }, fh, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT_DIR, "layer1_diagnostics.json"), "w", encoding="utf-8") as fh:
        json.dump({"tables": diag_tables, "mapping": mapping_report}, fh, indent=2, ensure_ascii=False)

    # ------------------- console report -----------------------------------
    print("\n[L1] endpoint summary (HD family)")
    cols = ["signature", "tissue", "model", "endpoint_level", "n_mapped_and_present",
            "MRU", "wilcoxon_z", "p_permutation", "q_BH"]
    sub = ep[ep.family.isin(["hippo_dependent", "hippo_independent"])][cols]
    print(sub.to_string(index=False))


if __name__ == "__main__":
    main()
