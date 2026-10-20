#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage B - sample-level stiffness-programme scoring in GSE261676 (mouse DRG).

Rationale (protocol v0.3): Stage A (GSE111216) deposits only per-contrast summary
statistics, so it cannot support sample-level inference. Stage B uses a cohort
that deposits per-sample counts, allowing a per-animal module score and an exact
permutation test.

Nothing here re-derives the signature: Layer-0 (GSE98547) already did that and
is frozen. This script only projects it, per animal.

Outputs (analysis/results/layer2/):
  layer2_results.json     primary / secondary / exploratory endpoints
  layer2_sample_scores.csv per-animal module scores and covariates
  layer2_gene_level.csv    per-member per-animal statistics
"""

import gzip
import itertools
import json
import os
import re
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
OUT = os.path.join(ROOT, "analysis", "results", "layer2")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)
from layer1_projection import human_to_mouse  # noqa: E402

CNTS = os.path.join(RAW, "_gse261676")
FNAME_RE = re.compile(r"^(GSM\d+)_(DMI|saline)-(sham|SNI)(\d)_S\d+\.counts\.txt\.gz$", re.IGNORECASE)
ANNOT_XLSX = "GSE111216_Parisien_Suppl_Table_06_gene_DRG_CTRvsSNI.xlsx"


def load_symbol_map():
    """ENSMUSG -> mouse symbol, taken from Stage A's table (same species)."""
    wb = openpyxl.load_workbook(os.path.join(RAW, ANNOT_XLSX), read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)
    header = [str(c).strip() if c is not None else "" for c in next(rows)]
    gi, gs = header.index("gene_id"), header.index("gene")
    m = {}
    for r in rows:
        if r is None or r[gi] is None or r[gs] is None:
            continue
        gid = str(r[gi]).split(".")[0]
        m.setdefault(gid, str(r[gs]).strip())
    wb.close()
    return m


def build_counts():
    files = sorted(f for f in os.listdir(CNTS) if FNAME_RE.match(f))
    meta, series = {}, {}
    for fn in files:
        m = FNAME_RE.match(fn)
        gsm, agent_raw, group, rep = m.group(1), m.group(2), m.group(3), m.group(4)
        agent = "DMI" if agent_raw.lower() == "dmi" else "saline"
        grp = "SNI" if group.lower() == "sni" else "sham"
        label = f"{agent}_{grp}{rep}"
        counts = {}
        with gzip.open(os.path.join(CNTS, fn), "rt") as fh:
            for line in fh:
                if not line.strip():
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 2:
                    continue
                counts[parts[0].split(".")[0]] = float(parts[1])
        series[label] = pd.Series(counts)
        meta[label] = {"gsm": gsm, "agent": agent, "group": grp, "rep": int(rep)}
    return pd.DataFrame(series), pd.DataFrame(meta).T


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    q = p[o] * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[o] = q
    return np.clip(out, 0, 1)


def exact_perm_diff(a, b, n_max=None):
    """Exact two-sided permutation test on difference of means (n<=12 per arm).

    Enumerates every distinct split of the pooled samples; returns (observed
    diff, empirical two-sided p, n_splits).

    GUARD: silently returning p = 0.0 on empty or NaN inputs would look like a
    maximally significant result. Refuse instead.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) == 0 or len(b) == 0:
        raise ValueError("exact_perm_diff received an empty arm (label mismatch?)")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("exact_perm_diff received non-finite scores")
    obs = float(np.mean(a) - np.mean(b))
    pooled = np.concatenate([a, b])
    n = len(pooled)
    k = len(a)
    diffs = []
    for combo in itertools.combinations(range(n), k):
        idx = np.zeros(n, bool)
        idx[list(combo)] = True
        diffs.append(np.mean(pooled[idx]) - np.mean(pooled[~idx]))
    diffs = np.array(diffs)
    p = float((np.abs(diffs) >= abs(obs) - 1e-12).mean())
    return obs, min(p, 1.0), len(diffs)


def main():
    cfg = json.load(open(CFG, encoding="utf-8"))
    sig = json.load(open(os.path.join(L0, "layer0_signature.json"), encoding="utf-8"))

    print("[L2] building counts matrix ...")
    cmat, meta = build_counts()
    print(f"[L2] {cmat.shape[0]} genes x {cmat.shape[1]} samples")
    print(f"[L2] design:\n{meta.groupby(['agent','group']).size().to_string()}")

    lib = cmat.sum(axis=0)
    print("[L2] library sizes (M):", (lib / 1e6).round(2).to_dict())

    cpm = cmat / lib * 1e6
    keep = (cpm > 1).sum(axis=1) >= 4
    print(f"[L2] expression filter keeps {int(keep.sum())} / {cmat.shape[0]} genes")
    lg = np.log2(cpm[keep] + 1)

    # ENSMUSG -> symbol
    smap = load_symbol_map()
    lg.index = [smap.get(g, None) for g in lg.index]
    lg = lg[lg.index.notnull()]
    lg = lg[~lg.index.duplicated(keep="first")]
    print(f"[L2] {len(lg)} genes with a mouse symbol")

    # z-score every gene across all 16 samples (pre-specified: no group stratification)
    z = lg.sub(lg.mean(axis=1), axis=0).div(lg.std(axis=1, ddof=1), axis=0)

    results = {}
    sample_rows = []
    gene_rows = []

    sets = sig["sets"]
    for key in ["hippo_dependent_up", "hippo_dependent_down",
                "hippo_independent_up", "hippo_independent_down"]:
        members = [human_to_mouse(g) for g in sets.get(key, [])]
        present = [m for m in members if m in z.index]
        if len(present) < 3:
            print(f"[L2] {key}: only {len(present)} members present - skipped")
            continue
        score = z.loc[present].mean(axis=0)

        for s in score.index:
            sample_rows.append({
                "sample": s, "agent": meta.loc[s, "agent"], "group": meta.loc[s, "group"],
                "gsm": meta.loc[s, "gsm"], "signature": key,
                "score": round(float(score[s]), 6),
            })
        for g in present:
            for s in score.index:
                gene_rows.append({
                    "signature": key, "gene": g, "sample": s,
                    "agent": meta.loc[s, "agent"], "group": meta.loc[s, "group"],
                    "log2cpm": round(float(lg.loc[g, s]), 6),
                    "z": round(float(z.loc[g, s]), 6),
                })

        # ---- B-primary endpoint: saline arm, SNI vs sham ------------------
        sal_sni = [s for s in score.index if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "SNI"]
        sal_sham = [s for s in score.index if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "sham"]
        obs, p_exact, n_splits = exact_perm_diff(score[sal_sni].to_numpy(), score[sal_sham].to_numpy())
        t, pt = sps.ttest_ind(score[sal_sni], score[sal_sham], equal_var=False)

        # ---- B-secondary: all samples, drug-adjusted ----------------------
        all_sni = [s for s in score.index if meta.loc[s, "group"] == "SNI"]
        all_sham = [s for s in score.index if meta.loc[s, "group"] == "sham"]
        # stratified permutation: shuffle labels only within agent
        rng = np.random.default_rng(cfg["layer1"]["rank_test"]["permutation"]["seed"])
        def agent_stratified_diff():
            d = 0.0
            for ag in ["saline", "DMI"]:
                s = [x for x in score.index if meta.loc[x, "agent"] == ag and meta.loc[x, "group"] == "SNI"]
                h = [x for x in score.index if meta.loc[x, "agent"] == ag and meta.loc[x, "group"] == "sham"]
                d += np.mean(score[s]) - np.mean(score[h])
            return d / 2
        obs_all = agent_stratified_diff()
        perm = []
        for _ in range(10000):
            perm.append(_perm_once(score, meta, rng))
        perm = np.array(perm)
        p_all = (int((np.abs(perm) >= abs(obs_all)).sum()) + 1) / (len(perm) + 1)

        # ---- B-exploratory: within SNI, DMI vs saline ---------------------
        sni_dmi = [s for s in score.index if meta.loc[s, "agent"] == "DMI" and meta.loc[s, "group"] == "SNI"]
        obs_drug, p_drug, _ = exact_perm_diff(score[sni_dmi].to_numpy(), score[sal_sni].to_numpy())

        # ---- B-negative control: size- and expression-matched random sets -
        ctrl_p = _size_matched_control(z, present, score.index, meta, rng)

        role = {
            "hippo_dependent_up": "B-primary",
            "hippo_dependent_down": "B-secondary-1",
            "hippo_independent_up": "exploratory",
            "hippo_independent_down": "exploratory",
        }[key]
        results[key] = {
            "endpoint_role": role,
            "n_human_members": len(sets.get(key, [])),
            "n_mapped_present": len(present),
            "members_present": sorted(present),
            "primary_saline_arm": {
                "mean_score_SNI": round(float(score[sal_sni].mean()), 5),
                "mean_score_sham": round(float(score[sal_sham].mean()), 5),
                "difference": round(obs, 5),
                "n_SNI": len(sal_sni), "n_sham": len(sal_sham),
                "p_exact_permutation": round(p_exact, 6),
                "n_permutations_enumerated": int(n_splits),
                "welch_t": round(float(t), 4),
                "welch_p": round(float(pt), 6),
            },
            "secondary_all_samples_drug_adjusted": {
                "difference": round(float(obs_all), 5),
                "p_permutation": round(float(p_all), 6),
            },
            "exploratory_drug_effect_within_SNI": {
                "mean_DMI": round(float(score[sni_dmi].mean()), 5),
                "mean_saline": round(float(score[sal_sni].mean()), 5),
                "difference": round(obs_drug, 5),
                "p_exact_permutation": round(p_drug, 6),
            },
            "negative_control_size_expression_matched": ctrl_p,
        }

    # BH across the four B-module tests within the sample-level family
    keys = list(results)
    qs = bh([results[k]["primary_saline_arm"]["p_exact_permutation"] for k in keys])
    for k, q in zip(keys, qs):
        results[k]["primary_saline_arm"]["q_BH_family_of_4"] = round(float(q), 6)

    pd.DataFrame(sample_rows).to_csv(os.path.join(OUT, "layer2_sample_scores.csv"), index=False)
    pd.DataFrame(gene_rows).to_csv(os.path.join(OUT, "layer2_gene_level.csv"), index=False)
    with open(os.path.join(OUT, "layer2_results.json"), "w", encoding="utf-8") as fh:
        json.dump({"_tag": cfg["_tag"], "_protocol": cfg["_protocol"],
                   "source": "GSE261676", "results": results}, fh, indent=2, ensure_ascii=False)

    print("\n[L2] Stage B results (saline arm, SNI vs sham)")
    for k, v in results.items():
        p = v["primary_saline_arm"]
        print(f"  {k:26s} n={v['n_mapped_present']:3d}  diff={p['difference']:+.4f}  "
              f"p_exact={p['p_exact_permutation']:.4f}  q={p['q_BH_family_of_4']:.4f}  "
              f"[welch p={p['welch_p']:.4f}]  role={v['endpoint_role']}")


def _perm_once(score, meta, rng):
    """One agent-stratified label permutation -> mean stratified difference."""
    d = 0.0
    for ag in ["saline", "DMI"]:
        idx = [s for s in score.index if meta.loc[s, "agent"] == ag]
        v = score[idx].to_numpy().copy()
        rng.shuffle(v)
        half = len(v) // 2
        d += np.mean(v[:half]) - np.mean(v[half:])
    return d / 2


def _size_matched_control(z, present, samples, meta, rng, n_iter=2000):
    """Negative control: random gene sets matched on size AND expression decile."""
    mean_expr = z.mean(axis=1)
    edges = np.array_split(np.argsort(mean_expr.to_numpy(), kind="mergesort"), 10)
    pool_by_bin = [mean_expr.index[e] for e in edges]
    member_bins = []
    for g in present:
        for b, pool in enumerate(pool_by_bin):
            if g in pool:
                member_bins.append(b)
                break
    obs_fun = lambda vals: None
    sal_sni = [s for s in samples if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "SNI"]
    sal_sham = [s for s in samples if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "sham"]
    actual = abs(np.mean(z.loc[present][sal_sni].mean(axis=0).to_numpy())
                 - np.mean(z.loc[present][sal_sham].mean(axis=0).to_numpy()))
    n_ge = 0
    for _ in range(n_iter):
        draws = []
        for b in member_bins:
            pool = pool_by_bin[b]
            draws.append(pool[rng.integers(0, len(pool))])
        sc = z.loc[draws].mean(axis=0)
        d = abs(np.mean(sc[sal_sni].to_numpy()) - np.mean(sc[sal_sham].to_numpy()))
        if d >= actual:
            n_ge += 1
    return {"n_iterations": n_iter,
            "p_empirical": round((n_ge + 1) / (n_iter + 1), 6),
            "note": "random size- and expression-decile-matched gene sets; a non-significant value confirms the scoring pipeline alone does not produce apparent effects"}


if __name__ == "__main__":
    main()
