#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage B robustness (protocol v0.3.1, post hoc additions).

Everything here was requested by the primary result, not chosen freely:
Q1  leave-one-animal-out stability of the HD_down separation
Q2  alternative scoring operators (median-z, mean raw log2CPM z, rank-based)
Q3  single-gene dominance check (drop the single most influential member)
Q4  full size- and expression-decile-matched null at 10,000 iterations
Q5  non-parametric alternative to the exact test (Mann-Whitney U)

Outputs: analysis/results/layer2/layer2_robustness.json
"""

import itertools
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats as sps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CFG = os.path.join(ROOT, "analysis", "config", "ms_panel.json")
L0 = os.path.join(ROOT, "analysis", "results", "layer0")
OUT = os.path.join(ROOT, "analysis", "results", "layer2")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)
from layer1_projection import human_to_mouse  # noqa: E402
from layer2_sample_scores import build_counts, load_symbol_map  # noqa: E402


def build_data():
    cmat, meta = build_counts()
    lib = cmat.sum(axis=0)
    cpm = cmat / lib * 1e6
    keep = (cpm > 1).sum(axis=1) >= 4
    lg = np.log2(cpm[keep] + 1)
    smap = load_symbol_map()
    lg.index = [smap.get(g, None) for g in lg.index]
    lg = lg[lg.index.notnull()]
    lg = lg[~lg.index.duplicated(keep="first")]
    return lg, meta


def zframe(lg):
    return lg.sub(lg.mean(axis=1), axis=0).div(lg.std(axis=1, ddof=1), axis=0)


def exact_p(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if len(a) < 2 or len(b) < 2 or not np.isfinite(a).all() or not np.isfinite(b).all():
        return None, None, None
    obs = float(np.mean(a) - np.mean(b))
    pooled = np.concatenate([a, b])
    n, k = len(pooled), len(a)
    diffs = []
    for combo in itertools.combinations(range(n), k):
        idx = np.zeros(n, bool)
        idx[list(combo)] = True
        diffs.append(np.mean(pooled[idx]) - np.mean(pooled[~idx]))
    diffs = np.array(diffs)
    return obs, float((np.abs(diffs) >= abs(obs) - 1e-12).mean()), len(diffs)


def main():
    cfg = json.load(open(CFG, encoding="utf-8"))
    sig = json.load(open(os.path.join(L0, "layer0_signature.json"), encoding="utf-8"))
    seed = cfg["layer1"]["rank_test"]["permutation"]["seed"]
    rng = np.random.default_rng(seed)

    lg, meta = build_data()
    z = zframe(lg)

    members_raw = sig["sets"]["hippo_dependent_down"]
    members = [human_to_mouse(g) for g in members_raw]
    present = [m for m in members if m in z.index]

    sal_sni = [s for s in z.columns if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "SNI"]
    sal_sham = [s for s in z.columns if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "sham"]

    report = {"n_members_present": len(present), "members": sorted(present)}

    # ---- Q1 leave-one-animal-out ------------------------------------------
    print("[ROB] Q1 leave-one-animal-out (saline arm)")
    score = z.loc[present].mean(axis=0)
    loo = []
    for drop in sal_sni + sal_sham:
        a = [s for s in sal_sni if s != drop]
        b = [s for s in sal_sham if s != drop]
        obs, p, ns = exact_p(score[a].to_numpy(), score[b].to_numpy())
        loo.append({"dropped": drop, "difference": round(obs, 5),
                    "p_exact": round(p, 6), "n_splits": int(ns),
                    "direction_preserved": bool(obs > 0)})
    report["Q1_leave_one_out"] = loo
    for r in loo:
        print(f"      -{r['dropped']:14s} diff={r['difference']:+.4f}  p={r['p_exact']:.4f}")

    # ---- Q2 alternative scoring operators ---------------------------------
    print("[ROB] Q2 alternative scoring operators")
    alt = {}
    variants = {
        "mean_z": score,
        "median_z": z.loc[present].median(axis=0),
        "rank_based": z.loc[present].rank(axis=1, pct=True).mean(axis=0),
        "trimean_z": (z.loc[present].quantile(0.25, axis=0) * 0.25
                      + z.loc[present].median(axis=0) * 0.5
                      + z.loc[present].quantile(0.75, axis=0) * 0.25),
    }
    for name, sc in variants.items():
        obs, p, ns = exact_p(sc[sal_sni].to_numpy(), sc[sal_sham].to_numpy())
        t, pt = sps.ttest_ind(sc[sal_sni], sc[sal_sham], equal_var=False)
        alt[name] = {"difference": round(obs, 5), "p_exact": round(p, 6),
                     "welch_p": round(float(pt), 6),
                     "direction_preserved": bool(obs > 0)}
        print(f"      {name:12s} diff={obs:+.4f}  p_exact={p:.4f}  welch_p={pt:.4f}")
    report["Q2_scoring_operators"] = alt

    # ---- Q3 single-gene dominance -----------------------------------------
    print("[ROB] Q3 drop individually most influential member")
    contrib = {}
    base = score[sal_sni].mean() - score[sal_sham].mean()
    for g in present:
        rest = [x for x in present if x != g]
        sc = z.loc[rest].mean(axis=0)
        contrib[g] = float(sc[sal_sni].mean() - sc[sal_sham].mean())
    worst = min(contrib, key=contrib.get)
    best = max(contrib, key=contrib.get)
    obs_w, p_w, _ = exact_p(z.loc[[x for x in present if x != worst]].mean(axis=0)[sal_sni].to_numpy(),
                            z.loc[[x for x in present if x != worst]].mean(axis=0)[sal_sham].to_numpy())
    report["Q3_single_gene_dominance"] = {
        "baseline_difference": round(float(base), 5),
        "weakest_member": worst,
        "difference_without_weakest": round(contrib[worst], 5),
        "p_exact_without_weakest": round(p_w, 6),
        "strongest_member": best,
        "difference_without_strongest": round(contrib[best], 5),
        "range_of_leave_one_out_differences": [round(min(contrib.values()), 5), round(max(contrib.values()), 5)],
        "direction_preserved_in_all_drops": bool(all(v > 0 for v in contrib.values())),
    }
    print(f"      baseline diff={base:+.4f};  dropping any single gene keeps diff in "
          f"[{min(contrib.values()):+.4f}, {max(contrib.values()):+.4f}] -> all same sign: "
          f"{all(v > 0 for v in contrib.values())}")

    # ---- Q4 fuller matched null -------------------------------------------
    print("[ROB] Q4 size- and expression-decile-matched null (10,000 draws)")
    mean_expr = z.mean(axis=1)
    edges = np.array_split(np.argsort(mean_expr.to_numpy(), kind="mergesort"), 10)
    pool_by_bin = [mean_expr.index[e] for e in edges]
    member_bins = []
    for g in present:
        for b, pool in enumerate(pool_by_bin):
            if g in pool:
                member_bins.append(b)
                break
    actual = abs(score[sal_sni].mean() - score[sal_sham].mean())
    n_ge = 0
    n_iter = 10000
    for _ in range(n_iter):
        draws = [pool_by_bin[b][rng.integers(0, len(pool_by_bin[b]))] for b in member_bins]
        sc = z.loc[draws].mean(axis=0)
        if abs(sc[sal_sni].mean() - sc[sal_sham].mean()) >= actual:
            n_ge += 1
    report["Q4_matched_null"] = {
        "n_iterations": n_iter, "n_as_extreme": int(n_ge),
        "p_empirical": round((n_ge + 1) / (n_iter + 1), 6),
    }
    print(f"      matched-null p = {(n_ge + 1) / (n_iter + 1):.5f} ({n_ge} / {n_iter})")

    # ---- Q5 non-parametric -------------------------------------------------
    print("[ROB] Q5 non-parametric alternatives")
    u, pu = sps.mannwhitneyu(score[sal_sni], score[sal_sham], alternative="two-sided")
    report["Q5_nonparametric"] = {
        "mann_whitney_U": float(u), "p_mann_whitney": float(pu),
        "note": "4 vs 4 gives a minimum attainable two-sided p of 0.029 for any rank test",
    }
    print(f"      Mann-Whitney U={u}, p={pu:.4f}")

    with open(os.path.join(OUT, "layer2_robustness.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print("[ROB] wrote layer2_robustness.json")


if __name__ == "__main__":
    main()
