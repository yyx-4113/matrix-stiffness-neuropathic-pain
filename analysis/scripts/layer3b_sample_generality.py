#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layer 3b - sample-level generality / divergence test (protocol v0.6).

WHY
---
Layer 3 asked whether the projection artefact is general across independently
published ECM / mechano gene sets. The primary endpoint FAILED (1 of 5 sets
failed specificity), and diagnosing that failure suggested a more precise
pattern: structural ECM programmes DO shift specifically in injured neural
tissue, whereas YAP/TAZ-dependent stiffness-response signatures do not.

That diagnosis was post hoc. Layer 3b converts it into a pre-specified test by
running every gene set on a DIFFERENT data modality - sample-level counts with
exact permutation - where the post hoc pattern would have to reproduce if it
is real.

PRE-SPECIFIED DECISION RULE (frozen before execution, protocol 13.3)
--------------------------------------------------------------------
L3b-divergence PASS requires ALL THREE:
  (a) >= 3 of the 5 ECM/mechano sets have exact permutation P <= 0.05
      with a positive SNI-minus-sham difference in the saline arm;
  (b) the Layer-0 HD_up signature has P > 0.05 in that same test;
  (c) the positive control has P <= 0.05 and Hedges g > 1.

(c) exists so that (b) cannot be dismissed as insensitivity: if the positive
control also fails, the whole test is uninformative and L3b is recorded as
NOT PASS (uninformative), not as evidence of divergence.

Outputs (analysis/results/layer3/):
  layer3b_sample_generality.json   per-set exact-permutation results + verdict
  layer3b_sample_generality.csv    flat table
"""

import itertools
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

CFG_PATH = os.path.join(ROOT, "analysis", "config", "ms_panel.json")
OUT_DIR = os.path.join(ROOT, "analysis", "results", "layer3")
os.makedirs(OUT_DIR, exist_ok=True)


def bh(p):
    p = np.asarray(p, dtype=float)
    n = len(p)
    o = np.argsort(p)
    q = p[o] * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[o] = q
    return np.clip(out, 0, 1)


def human_to_mouse(sym):
    if sym.isupper():
        return sym[0] + sym[1:].lower()
    return sym


def exact_perm_p(score, g1, g2):
    """Exact two-sided permutation P over all C(n, |g1|) splits.

    `g1` / `g2` are sample labels. Every split is enumerated, so P is exact
    rather than Monte-Carlo; the attainable minimum is 2/C(n,k) because each
    split and its complement give equal-magnitude opposite differences.
    """
    samples = list(g1) + list(g2)
    k = len(g1)
    obs = float(np.mean(score[g1]) - np.mean(score[g2]))
    diffs = []
    for combo in itertools.combinations(range(len(samples)), k):
        a = [samples[i] for i in combo]
        b = [s for s in samples if s not in a]
        diffs.append(float(np.mean(score[a]) - np.mean(score[b])))
    diffs = np.asarray(diffs)
    n_ge = int((np.abs(diffs) >= abs(obs) - 1e-12).sum())
    return obs, n_ge / len(diffs), len(diffs)


def hedges_g(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan")
    s = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1))
                / (n1 + n2 - 2))
    if s == 0 or not np.isfinite(s):
        return float("nan")
    d = (a.mean() - b.mean()) / s
    return d * (1 - 3 / (4 * (n1 + n2) - 9))


def main():
    cfg = json.load(open(CFG_PATH, encoding="utf-8"))
    l3 = cfg["layer3"]
    sig = json.load(open(os.path.join(ROOT, "analysis", "results",
                                      "layer0", "layer0_signature.json"),
                         encoding="utf-8"))

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

    # Hard failure instead of silent NaN: empty arms previously produced
    # p = 0 "super-significant" artefacts in an earlier revision.
    assert len(sal_sni) == 4 and len(sal_sham) == 4, \
        f"saline arm must be 4v4, got {len(sal_sni)}/{len(sal_sham)}"
    assert len(dmi_sni) == 4 and len(dmi_sham) == 4, \
        f"DMI arm must be 4v4, got {len(dmi_sni)}/{len(dmi_sham)}"

    sd = lg.std(axis=1, ddof=1)
    z = lg.sub(lg.mean(axis=1), axis=0).div(sd, axis=0)
    assert int(z.isna().sum().sum()) == 0, "NaN in z matrix"

    # ---- assemble the 7 gene sets ------------------------------------
    sets = {}
    for gname, gdef in l3["gene_sets"].items():
        sets[gname] = [human_to_mouse(g) for g in gdef["members"]]
    sets["HD_up"] = [human_to_mouse(g) for g in sig["sets"]["hippo_dependent_up"]]
    # The frozen positive-control panel is stored as HUMAN symbols; it needs the
    # same human->mouse mapping as every other set. Layer 2 applies the mapping,
    # Layer 3b must too, or the panel silently matches nothing.
    sets["POSITIVE_CONTROL_injury"] = [
        human_to_mouse(g) for g in cfg["positive_control"]["injury_up"]]

    rows = []
    for name, members in sets.items():
        present = [m for m in members if m in z.index]
        if len(present) < 3:
            print(f"[L3b] {name}: only {len(present)} members present - skipped")
            continue
        score = z.loc[present].mean(axis=0)

        obs, p_sal, n_split = exact_perm_p(score, sal_sni, sal_sham)
        g_sal = hedges_g(score[sal_sni].to_numpy(), score[sal_sham].to_numpy())

        # secondary: all 8 samples, drug-adjusted (mean of arm means)
        a = score[sal_sni + dmi_sni].mean()
        b = score[sal_sham + dmi_sham].mean()
        rows.append({
            "gene_set": name,
            "n_human_members": len(members),
            "n_mouse_present": len(present),
            "diff_saline_arm": obs,
            "p_exact_saline_arm": p_sal,
            "hedges_g_saline_arm": g_sal,
            "n_permutations_enumerated": n_split,
            "diff_all_samples_drug_adjusted": float(a - b),
            "mean_SNI": float(score[sal_sni].mean()),
            "mean_sham": float(score[sal_sham].mean()),
        })

    tbl = pd.DataFrame(rows)
    tbl["q_BH_family_of_7"] = bh(tbl["p_exact_saline_arm"].to_numpy())

    ecm = [r for r in rows if r["gene_set"].startswith("G")]
    hd = [r for r in rows if r["gene_set"] == "HD_up"][0]
    pos = [r for r in rows if r["gene_set"] == "POSITIVE_CONTROL_injury"][0]

    n_ecm_sig = sum(1 for r in ecm
                    if r["p_exact_saline_arm"] <= 0.05
                    and r["diff_saline_arm"] > 0)
    cond_a = bool(n_ecm_sig >= 3)
    cond_b = bool(hd["p_exact_saline_arm"] > 0.05)
    cond_c = bool(pos["p_exact_saline_arm"] <= 0.05
                  and pos["hedges_g_saline_arm"] > 1)
    verdict = "PASS" if (cond_a and cond_b and cond_c) else (
        "NOT PASS (uninformative: positive control failed)" if not cond_c
        else "FAIL")

    print("=" * 78)
    print("LAYER 3b - sample-level generality / divergence test")
    print("=" * 78)
    print(f"{'gene set':34s} {'n':>3s}  {'diff':>8s}  {'p_exact':>8s}  {'g':>7s}")
    for r in rows:
        print(f"  {r['gene_set']:32s} {r['n_mouse_present']:3d}  "
              f"{r['diff_saline_arm']:+8.4f}  "
              f"{r['p_exact_saline_arm']:8.4f}  "
              f"{r['hedges_g_saline_arm']:+7.3f}")
    print(f"\n  (a) ECM/mechano sets significant & up : {n_ecm_sig}/5 -> {cond_a}")
    print(f"  (b) HD_up NOT significant             : "
          f"p={hd['p_exact_saline_arm']:.4f} -> {cond_b}")
    print(f"  (c) positive control significant      : "
          f"p={pos['p_exact_saline_arm']:.4f}, g={pos['hedges_g_saline_arm']:.3f} -> {cond_c}")
    print(f"\n  VERDICT (L3b-divergence): {verdict}")

    out = {
        "protocol": cfg["_protocol"],
        "design": {
            "data": "GSE261676 sample-level counts, saline arm 4 SNI vs 4 sham (primary); "
                    "all 8 samples drug-adjusted (secondary)",
            "test": "exact permutation over all C(8,4)=70 splits, two-sided",
            "gene_sets": {k: len(v) for k, v in sets.items()},
        },
        "conditions": {"a_ecm_significant_up_ge3": cond_a,
                       "b_HDup_not_significant": cond_b,
                       "c_positive_control_pass": cond_c},
        "verdict": verdict,
        "table": tbl.to_dict(orient="records"),
    }
    with open(os.path.join(OUT_DIR, "layer3b_sample_generality.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    tbl.to_csv(os.path.join(OUT_DIR, "layer3b_sample_generality.csv"),
               index=False)
    print(f"\nwrote {OUT_DIR}/layer3b_sample_generality.json")
    print(f"wrote {OUT_DIR}/layer3b_sample_generality.csv")


if __name__ == "__main__":
    main()
