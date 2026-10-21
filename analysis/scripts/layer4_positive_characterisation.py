#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layer 4 - positive characterisation of the ECM / mechano programme in injured DRG.

WHY
---
Stages A/B and Layers 3/3b all answer "is the stiffness-Hippo programme there?".
None of them says what IS there. A manuscript that only reports an absence is easy
to read as purely negative, and it leaves the reader without a constructive
alternative. Layer 4 supplies the positive half: which ECM / mechano genes actually
move together in injured DRG.

PRE-SPECIFIED (protocol 14.2-14.3)
----------------------------------
  * saline arm (4 SNI vs 4 sham) is primary; all-8 drug-adjusted is secondary
  * per-gene Welch t-test, effect size Hedges g WITH the small-sample correction
    (see audit R13 - an earlier revision silently reported Cohen's d as Hedges g)
  * BH over all detection-filtered genes; primary threshold q < 0.05,
    exploratory threshold q < 0.10 reported separately and never promoted
  * primary endpoint L4-positive-characterisation needs ALL THREE:
      (a) >= 10 significantly up-regulated genes inside G1 u G4 u G5
      (b) Fisher OR > 1 with P < 0.05 for that union among up-regulated genes
      (c) <= 2 of the HD_up members are significantly up-regulated

    (c) is the discriminating control: it prevents the characterisation from
    degenerating into "everything went up", and it ties Layer 4 back to the
    pre-specified null result of Stage B.

Outputs (analysis/results/layer4/):
  layer4_positive_characterisation.json
  layer4_gene_level.csv
"""

import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats as sps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

CFG_PATH = os.path.join(ROOT, "analysis", "config", "ms_panel.json")
OUT_DIR = os.path.join(ROOT, "analysis", "results", "layer4")
os.makedirs(OUT_DIR, exist_ok=True)


def human_to_mouse(sym):
    if sym.isupper():
        return sym[0] + sym[1:].lower()
    return sym


def bh(p):
    p = np.asarray(p, dtype=float)
    p = np.where(np.isfinite(p), p, 1.0)
    n = len(p)
    o = np.argsort(p)
    q = p[o] * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[o] = q
    return np.clip(out, 0, 1)


def hedges_g(a, b):
    """Bias-corrected standardised mean difference (Hedges g).

    Deliberately applies the small-sample correction factor
    1 - 3/(4*(n1+n2) - 9). See audit R13.
    """
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan")
    s = np.sqrt(((n1 - 1) * np.var(a, ddof=1) + (n2 - 1) * np.var(b, ddof=1))
                / (n1 + n2 - 2))
    if s == 0 or not np.isfinite(s):
        return float("nan")
    return float((np.mean(a) - np.mean(b)) / s) * (1 - 3 / (4 * (n1 + n2) - 9))


def main():
    cfg = json.load(open(CFG_PATH, encoding="utf-8"))
    seed = cfg["layer1"]["rank_test"]["permutation"]["seed"]
    l3 = cfg["layer3"]

    from layer2_sample_scores import build_counts, load_symbol_map

    cmat, meta = build_counts()
    lib = cmat.sum(axis=0)
    cpm = cmat / lib * 1e6
    keep = (cpm > 1).sum(axis=1) >= 4
    lg = np.log2(cpm[keep] + 1)

    smap = load_symbol_map()
    lg = lg.copy()
    lg.index = [smap.get(g, None) for g in lg.index]
    lg = lg[lg.index.notnull()]
    lg = lg[~lg.index.duplicated(keep="first")]
    print(f"[L4] {lg.shape[0]} genes x {lg.shape[1]} samples after detection filter")

    samples = list(lg.columns)
    sal_sni = sorted([s for s in samples
                      if meta.loc[s, "agent"] == "saline"
                      and meta.loc[s, "group"] == "SNI"])
    sal_sham = sorted([s for s in samples
                       if meta.loc[s, "agent"] == "saline"
                       and meta.loc[s, "group"] == "sham"])
    dmi_sni = sorted([s for s in samples
                      if meta.loc[s, "agent"] == "DMI"
                      and meta.loc[s, "group"] == "SNI"])
    dmi_sham = sorted([s for s in samples
                       if meta.loc[s, "agent"] == "DMI"
                      and meta.loc[s, "group"] == "sham"])
    assert len(sal_sni) == 4 and len(sal_sham) == 4
    assert len(dmi_sni) == 4 and len(dmi_sham) == 4

    a = lg[sal_sni].to_numpy()
    b = lg[sal_sham].to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        t, p = sps.ttest_ind(a, b, axis=1, equal_var=False)
    p = np.where(np.isfinite(p), p, 1.0)
    q = bh(p)
    lfc = a.mean(axis=1) - b.mean(axis=1)
    g = np.array([hedges_g(a[i], b[i]) for i in range(a.shape[0])])

    stats = pd.DataFrame(
        {"log2_fc": lfc, "welch_t": t, "p_value": p, "q_BH": q, "hedges_g": g},
        index=lg.index,
    )

    # ---- gene set overlap / enrichment -----------------------------------
    sig0 = stats.index[(stats["q_BH"] < 0.05) & (stats["log2_fc"] > 0)]
    sig1 = stats.index[(stats["q_BH"] < 0.10) & (stats["log2_fc"] > 0)]

    sets = {k: [human_to_mouse(x) for x in v["members"]]
            for k, v in l3["gene_sets"].items()}
    union_ecm = sorted({m for v in sets.values() for m in v})
    union_present = [m for m in union_ecm if m in stats.index]

    per_set = {}
    for k, mem in sets.items():
        pres = [m for m in mem if m in stats.index]
        sub = stats.loc[pres]
        sig_up = sub[(sub["q_BH"] < 0.05) & (sub["log2_fc"] > 0)]
        sig_dn = sub[(sub["q_BH"] < 0.05) & (sub["log2_fc"] < 0)]
        per_set[k] = {
            "n_members": len(mem),
            "n_present": len(pres),
            "n_sig_up_q05": int(len(sig_up)),
            "n_sig_dn_q05": int(len(sig_dn)),
            "median_log2_fc": float(sub["log2_fc"].median()),
            "median_hedges_g": float(sub["hedges_g"].median()),
            "sig_up_genes_q05": sorted(sig_up.index),
        }

    n_ecm_sig = sum(1 for m in union_present
                    if stats.loc[m, "q_BH"] < 0.05 and stats.loc[m, "log2_fc"] > 0)

    # Fisher: is the ECM union over-represented among significantly up genes?
    a11 = n_ecm_sig
    a12 = len(union_present) - a11
    a21 = len(sig0) - a11
    a22 = len(stats) - len(union_present) - a21
    orr, fp = sps.fisher_exact([[a11, a12], [a21, a22]], alternative="greater")

    # HD_up members under the same per-gene test
    sig0s = set(sig0)
    hd_up = [human_to_mouse(g) for g in
             json.load(open(os.path.join(ROOT, "analysis", "results",
                                         "layer0", "layer0_signature.json"),
                            encoding="utf-8"))["sets"]["hippo_dependent_up"]]
    hd_up_present = [m for m in hd_up if m in stats.index]
    hd_up_sig = [m for m in hd_up_present if m in sig0s]

    pc = [human_to_mouse(g) for g in cfg["positive_control"]["injury_up"]]
    pc_present = [m for m in pc if m in stats.index]
    pc_sig = [m for m in pc_present if m in sig0s]

    cond_a = bool(n_ecm_sig >= 10)
    cond_b = bool(orr > 1) and bool(fp < 0.05)
    cond_c = bool(len(hd_up_sig) <= 2)
    verdict = "PASS" if (cond_a and cond_b and cond_c) else "FAIL"

    print("=" * 78)
    print("LAYER 4 - positive characterisation of the ECM/mechano programme")
    print("=" * 78)
    print(f"  genes tested                : {len(stats)}")
    print(f"  ECM union members present   : {len(union_present)}/{len(union_ecm)}")
    print(f"  significantly up (q<0.05)   : {len(sig0)}")
    print(f"  ECM-union genes among them  : {n_ecm_sig}")
    print(f"  Fisher OR = {orr:.3f}, P = {fp:.3e}")
    print()
    for k, v in per_set.items():
        print(f"  {k:34s} present={v['n_present']:3d}  "
              f"sig_up={v['n_sig_up_q05']:3d}  "
              f"median_g={v['median_hedges_g']:+.3f}")
    print(f"\n  HD_up members: present={len(hd_up_present)}, "
          f"significantly up={len(hd_up_sig)} {hd_up_sig}")
    print(f"  positive control: present={len(pc_present)}, "
          f"significantly up={len(pc_sig)}")
    print(f"\n  (a) >=10 ECM-union genes up: {cond_a}")
    print(f"  (b) Fisher OR>1 & P<0.05   : {cond_b}")
    print(f"  (c) <=2 HD_up members up   : {cond_c}")
    print(f"\n  VERDICT (L4-positive-characterisation): {verdict}")

    out = {
        "protocol": cfg["_protocol"],
        "design": {
            "data": "GSE261676 sample-level counts, saline arm (4 SNI vs 4 sham)",
            "test": "per-gene Welch t-test, BH over all detection-filtered genes",
            "primary_threshold": "q < 0.05",
            "exploratory_threshold": "q < 0.10 (reported separately, never promoted)",
            "seed": seed,
        },
        "n_genes_tested": int(len(stats)),
        "n_sig_up_q05": int(len(sig0)),
        "n_sig_up_q10": int(len(sig1)),
        "n_sig_dn_q05": int(((stats['q_BH'] < 0.05) & (stats['log2_fc'] < 0)).sum()),
        "ecm_union": {
            "n_members": len(union_ecm),
            "n_present": len(union_present),
            "n_sig_up_q05": n_ecm_sig,
            "fisher_OR": float(orr),
            "fisher_P": float(fp),
            "sig_up_genes": sorted(set(union_present) & sig0s),
        },
        "per_set": per_set,
        "hd_up_members": {
            "n_present": len(hd_up_present),
            "n_sig_up_q05": len(hd_up_sig),
            "sig_up_genes": hd_up_sig,
        },
        "positive_control": {
            "n_present": len(pc_present),
            "n_sig_up_q05": len(pc_sig),
            "sig_up_genes": pc_sig,
        },
        "conditions": {"a_ecm_up_ge10": cond_a,
                       "b_fisher_enrichment": cond_b,
                       "c_HDup_up_le2": cond_c},
        "verdict": verdict,
    }
    with open(os.path.join(OUT_DIR, "layer4_positive_characterisation.json"),
              "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    stats.sort_values("log2_fc", ascending=False).to_csv(
        os.path.join(OUT_DIR, "layer4_gene_level.csv"))
    print(f"\nwrote {OUT_DIR}/layer4_positive_characterisation.json")
    print(f"wrote {OUT_DIR}/layer4_gene_level.csv")


if __name__ == "__main__":
    main()
