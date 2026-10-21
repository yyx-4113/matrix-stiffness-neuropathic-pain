#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage B POSITIVE CONTROL - pipeline sensitivity check (protocol v0.4 section 10).

Problem this solves
-------------------
Every layer of this project returns a null. A pipeline that only ever returns
nulls cannot distinguish "there is no signal" from "this apparatus cannot see a
signal". Until that is excluded, no null conclusion carries any weight.

Design
------
Run a gene set that the literature has independently and repeatedly shown to be
strongly UP-regulated in DRG neurons after peripheral nerve injury, through the
EXACT same scoring machinery as the stiffness signatures:
      counts -> CPM -> log2(CPM+1) -> CPM>1 in >=4/16 filter -> per-gene z
      across all 16 samples -> mean z over present members -> exact permutation
      on the saline arm (SNI vs sham).

The gene set is taken from published nerve-injury reports ONLY. It is never
chosen by looking at any expression result in this project, which would make the
sensitivity check circular.

Interpretation
--------------
  passes  -> the apparatus CAN detect a real effect of this kind; the stiffness
             nulls are then interpretable as bounded negative findings.
  fails   -> the apparatus is unvalidated; all null conclusions are void.

Outputs: analysis/results/layer2/layer2_positive_control.json
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

from layer1_projection import human_to_mouse            # noqa: E402
from layer2_sample_scores import build_counts, load_symbol_map  # noqa: E402


def exact_perm_diff(a, b):
    """Exact two-sided permutation p on the difference of means."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 2 or len(b) < 2:
        raise ValueError("need at least 2 per arm")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("non-finite scores")
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


def hedges_g(a, b):
    """Bias-corrected standardised mean difference (Hedges g).

    CORRECTED (audit R13): an earlier revision returned Cohen's d while naming
    it Hedges g. At n1 = n2 = 4 the small-sample correction factor is
        1 - 3 / (4 * (n1 + n2) - 9) = 1 - 3/23 = 0.8696,
    so the uncorrected d overstated every effect by roughly 15%. The defect did
    not change any sign or any P value, but it did inflate the headline
    magnitude comparison (positive control 4.431 vs HD_up 0.252), so it is fixed here
    and the corrected values are carried into every downstream artefact.
    """
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n1, n2 = len(a), len(b)
    s = np.sqrt(((n1 - 1) * np.var(a, ddof=1) + (n2 - 1) * np.var(b, ddof=1))
                / (n1 + n2 - 2))
    if s == 0 or not np.isfinite(s):
        return float("nan")
    return float((np.mean(a) - np.mean(b)) / s) * (1 - 3 / (4 * (n1 + n2) - 9))


def build_z():
    """Identical normalisation and filtering to layer2_sample_scores.main()."""
    cmat, meta = build_counts()
    lib = cmat.sum(axis=0)
    cpm = cmat / lib * 1e6
    keep = (cpm > 1).sum(axis=1) >= 4
    lg = np.log2(cpm[keep] + 1)
    smap = load_symbol_map()
    lg.index = [smap.get(g, None) for g in lg.index]
    lg = lg[lg.index.notnull()]
    lg = lg[~lg.index.duplicated(keep="first")]
    z = lg.sub(lg.mean(axis=1), axis=0).div(lg.std(axis=1, ddof=1), axis=0)
    return z, meta, cmat, smap


def main():
    cfg = json.load(open(CFG, encoding="utf-8"))
    sig = json.load(open(os.path.join(L0, "layer0_signature.json"), encoding="utf-8"))
    pc_cfg = cfg["positive_control"]

    z, meta, cmat, smap = build_z()

    # full annotation universe, before the CPM filter (for coverage separation)
    annot = set(smap.get(g) for g in cmat.index)
    annot.discard(None)

    sal_sni = [s for s in z.columns
               if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "SNI"]
    sal_sham = [s for s in z.columns
                if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "sham"]

    def score_set(genes_human, label):
        mapped = [human_to_mouse(g) for g in genes_human]
        present = [m for m in mapped if m in z.index]
        if len(present) < 3:
            return {"label": label, "error": f"only {len(present)} present"}
        sc = z.loc[present].mean(axis=0)
        a = sc[sal_sni].to_numpy()
        b = sc[sal_sham].to_numpy()
        obs, p, nsp = exact_perm_diff(a, b)
        t, pt = sps.ttest_ind(a, b, equal_var=False)
        u, pu = sps.mannwhitneyu(a, b, alternative="two-sided")
        return {
            "label": label,
            "n_human": len(genes_human),
            "n_homology_mapped": int(sum(1 for m in mapped if m in annot)),
            "homology_mapping_rate": round(sum(1 for m in mapped if m in annot) / len(genes_human), 4),
            "n_present_after_filter": len(present),
            "coverage_rate": round(len(present) / len(genes_human), 4),
            "members_present": sorted(present),
            "members_absent": sorted(m for m in mapped if m not in z.index),
            "mean_score_SNI": round(float(a.mean()), 5),
            "mean_score_sham": round(float(b.mean()), 5),
            "difference": round(obs, 5),
            "p_exact_permutation": round(p, 6),
            "n_permutations_enumerated": int(nsp),
            "welch_p": round(float(pt), 6),
            "mann_whitney_p": round(float(pu), 6),
            "hedges_g": round(float(hedges_g(a, b)), 4),
            "per_animal": {s: round(float(sc[s]), 5) for s in sc.index},
        }

    controls = {
        "POSITIVE_CONTROL_injury_up": pc_cfg["injury_up"],
        "stiffness_HD_up": sig["sets"]["hippo_dependent_up"],
        "stiffness_HD_down": sig["sets"]["hippo_dependent_down"],
        "stiffness_HI_down": sig["sets"]["hippo_independent_down"],
    }

    out = {}
    print("[PC] positive-control / signature sensitivity comparison")
    print(f"[PC] background: {z.shape[0]} genes x {z.shape[1]} samples\n")
    for label, genes in controls.items():
        res = score_set(genes, label)
        out[label] = res
        if "error" in res:
            print(f"  {label:30s} {res['error']}")
            continue
        print(f"  {label:30s} n={res['n_present_after_filter']:3d}  "
              f"diff={res['difference']:+.4f}  p_exact={res['p_exact_permutation']:.4f}  "
              f"g={res['hedges_g']:+.3f}")

    # ---------------------------------------------------------- verdict ----
    pc = out["POSITIVE_CONTROL_injury_up"]
    if "error" in pc:
        verdict, detail = "UNRESOLVED", pc["error"]
    else:
        passes = pc["p_exact_permutation"] <= 0.05 and pc["difference"] > 0
        verdict = "PASS" if passes else "FAIL"
        detail = (f"diff={pc['difference']:+.4f}, p_exact={pc['p_exact_permutation']:.4f}, "
                  f"g={pc['hedges_g']:+.3f}")
    print(f"\n[PC] sensitivity verdict: {verdict}  ({detail})")
    print("[PC] meaning: PASS -> the stiffness nulls are interpretable bounded "
          "negative findings; FAIL -> every null from this pipeline is void.")

    payload = {
        "_tag": cfg["_tag"],
        "_protocol": cfg["_protocol"],
        "source": "GSE261676",
        "specification": {
            "gene_set": pc_cfg["injury_up"],
            "selection_basis": pc_cfg["_selection_basis"],
            "expected_direction": pc_cfg["_direction"],
            "pass_criterion": pc_cfg["pass_criterion"],
            "on_failure": pc_cfg["on_failure"],
        },
        "results": out,
        "sensitivity_verdict": verdict,
        "sensitivity_detail": detail,
    }
    with open(os.path.join(OUT, "layer2_positive_control.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    print("[PC] wrote layer2_positive_control.json")


if __name__ == "__main__":
    main()
