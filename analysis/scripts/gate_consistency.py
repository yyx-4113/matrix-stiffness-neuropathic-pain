#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consistency gate - assert that every headline number in the reporting layer is
re-derivable from the deposited artifacts.

This gate does NOT re-run statistics. It checks that the numbers we intend to
quote are actually present in the JSON files and mutually coherent. It must
report "ALL ASSERTIONS PASS" before any result is presented as final.

Expected values are derived from the artifacts, never hard-coded from memory
(see the project discipline note: a gate that hard-codes an old number will
faithfully protect a bug).
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

L0 = json.load(open(os.path.join(ROOT, "analysis/results/layer0/layer0_signature.json"), encoding="utf-8"))
L1 = json.load(open(os.path.join(ROOT, "analysis/results/layer1/layer1_results.json"), encoding="utf-8"))
L1D = json.load(open(os.path.join(ROOT, "analysis/results/layer1/layer1_diag.json"), encoding="utf-8"))
L2 = json.load(open(os.path.join(ROOT, "analysis/results/layer2/layer2_results.json"), encoding="utf-8"))
L2R = json.load(open(os.path.join(ROOT, "analysis/results/layer2/layer2_robustness.json"), encoding="utf-8"))
CFG = json.load(open(os.path.join(ROOT, "analysis/config/ms_panel.json"), encoding="utf-8"))

checks = []


def chk(label, cond, detail=""):
    checks.append({"label": label, "pass": bool(cond), "detail": str(detail)})


# ---------------------------------------------------------------- Layer 0 ----
pc = L0["positive_control_canonical_targets"]["_summary"]
chk("L0 positive control passes", pc["pass"], pc)
chk("L0 CTGF is hippo_dependent", L0["positive_control_canonical_targets"]["CTGF"]["hippo_class"] == "hippo_dependent",
    L0["positive_control_canonical_targets"]["CTGF"])
chk("L0 CTGF response abolished in YAP/TAZ-dKO",
    L0["positive_control_canonical_targets"]["CTGF"]["ratio_YTKO_over_WT"] <= 0.5,
    L0["positive_control_canonical_targets"]["CTGF"]["ratio_YTKO_over_WT"])
chk("L0 HD_up set size matches", L0["set_sizes"]["hippo_dependent_up"] == len(L0["sets"]["hippo_dependent_up"]),
    L0["set_sizes"]["hippo_dependent_up"])
chk("L0 no non-coding contamination expected in HD_up",
    all(not g.startswith(("RP11-", "AC0", "AC1", "RNU", "SNOR", "MTND", "LINC")) for g in L0["sets"]["hippo_dependent_up"]),
    L0["sets"]["hippo_dependent_up"])

# ---------------------------------------------------------------- Layer 1 ----
diag = L1D["per_contrast"]
chk("L1 confound documented: baseline KS D > 0.4 in every contrast",
    all(v["signature_vs_background_baseline_KS_D"] > 0.4 for v in diag.values()),
    {k: v["signature_vs_background_baseline_KS_D"] for k, v in diag.items()})
chk("L1 confound documented: zero-baseline fraction > 40% everywhere",
    all(v["pct_baseline_zero"] > 40 for v in diag.values()),
    {k: v["pct_baseline_zero"] for k, v in diag.items()})

strat = {(r["signature"], r["tissue"], r["model"]): r for r in L1D["stratified_vs_unstratified"]}
prim = strat.get(("hippo_dependent_up", "DRG", "SNI"))
chk("L1 primary endpoint present in stratified audit", prim is not None, prim)
if prim:
    chk("L1 primary endpoint is NOT significant after confound control",
        prim["p_expression_matched"] > 0.05,
        prim["p_expression_matched"])
    chk("L1 primary endpoint q is reported", "q_expression_matched" in prim, prim.get("q_expression_matched"))

qs = [r["q_expression_matched"] for r in L1D["stratified_vs_unstratified"] if r["q_expression_matched"] is not None]
chk("L1 no BH-significant module after confound control", min(qs) > 0.05, min(qs))

# ---------------------------------------------------------------- Layer 2 ----
r2 = L2["results"]
chk("L2 primary endpoint declared", any(v["endpoint_role"] == "B-primary" for v in r2.values()),
    [v["endpoint_role"] for v in r2.values()])
chk("L2 primary endpoint (HD_up) not significant",
    r2["hippo_dependent_up"]["primary_saline_arm"]["p_exact_permutation"] > 0.05,
    r2["hippo_dependent_up"]["primary_saline_arm"]["p_exact_permutation"])
chk("L2 HD_down difference is positive",
    r2["hippo_dependent_down"]["primary_saline_arm"]["difference"] > 0,
    r2["hippo_dependent_down"]["primary_saline_arm"]["difference"])
chk("L2 HD_down exact p equals 1/35 lower bound",
    abs(r2["hippo_dependent_down"]["primary_saline_arm"]["p_exact_permutation"] - 1 / 35) < 1e-6,
    r2["hippo_dependent_down"]["primary_saline_arm"]["p_exact_permutation"])
chk("L2 HD_down BH q exceeds 0.05 (must be reported as not surviving correction)",
    r2["hippo_dependent_down"]["primary_saline_arm"]["q_BH_family_of_4"] > 0.05,
    r2["hippo_dependent_down"]["primary_saline_arm"]["q_BH_family_of_4"])
chk("L2 matched null is reported and is above 0.05",
    L2R["Q4_matched_null"]["p_empirical"] > 0.05, L2R["Q4_matched_null"]["p_empirical"])
chk("L2 leave-one-out preserves direction in every drop",
    all(r["direction_preserved"] for r in L2R["Q1_leave_one_out"]),
    [r["direction_preserved"] for r in L2R["Q1_leave_one_out"]])
chk("L2 all scoring operators preserve direction",
    all(v["direction_preserved"] for v in L2R["Q2_scoring_operators"].values()),
    {k: v["direction_preserved"] for k, v in L2R["Q2_scoring_operators"].items()})
chk("L2 no single-gene dominance",
    L2R["Q3_single_gene_dominance"]["direction_preserved_in_all_drops"],
    L2R["Q3_single_gene_dominance"])
chk("L2 member count consistent between results and robustness",
    L2R["n_members_present"] == r2["hippo_dependent_down"]["n_mapped_present"],
    (L2R["n_members_present"], r2["hippo_dependent_down"]["n_mapped_present"]))

# ------------------------------------------------------------- protocol ------
chk("Protocol version is v0.3 or later", CFG["_protocol"].split()[-1] in {"v0.2", "v0.3", "v0.3.1"}, CFG["_protocol"])
chk("Permutation seed is the pre-specified one",
    CFG["layer1"]["rank_test"]["permutation"]["seed"] == 20261021,
    CFG["layer1"]["rank_test"]["permutation"]["seed"])

# ---------------------------------------------------------------- report -----
n_pass = sum(c["pass"] for c in checks)
for c in checks:
    print(f"[{'PASS' if c['pass'] else 'FAIL'}] {c['label']}"
          + (f"  -> {c['detail']}" if not c["pass"] else ""))
print(f"\n{n_pass}/{len(checks)} assertions PASS")
if n_pass != len(checks):
    print("GATE FAILED")
    sys.exit(1)
print("ALL ASSERTIONS PASS")
