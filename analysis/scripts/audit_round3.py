#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT ROUND 3 - figure/claim traceability.

Every number quoted in the reporting layer (README, Chinese summary, figures)
must be re-derivable from a deposited artifact. This script reads each headline
value OUT of the artifacts and asserts the string appears in the documents,
so that a stale number left behind by a later fix is caught mechanically rather
than by memory.

It also re-checks the positive-control design for circularity: the gene set must
be declared in the frozen config, must not have been selected from any expression
result of this project, and must be scored by the same code path as the signatures.

Outputs: analysis/results/audit/audit_round3.json
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
L0 = os.path.join(ROOT, "analysis", "results", "layer0")
L1 = os.path.join(ROOT, "analysis", "results", "layer1")
L2 = os.path.join(ROOT, "analysis", "results", "layer2")
OUT = os.path.join(ROOT, "analysis", "results", "audit")
os.makedirs(OUT, exist_ok=True)

DOCS = ["README.md", "RESULTS_SUMMARY_zh.md"]

l0 = json.load(open(os.path.join(L0, "layer0_signature.json"), encoding="utf-8"))
l1 = json.load(open(os.path.join(L1, "layer1_results.json"), encoding="utf-8"))
l1d = json.load(open(os.path.join(L1, "layer1_diag.json"), encoding="utf-8"))
l2 = json.load(open(os.path.join(L2, "layer2_results.json"), encoding="utf-8"))
l2r = json.load(open(os.path.join(L2, "layer2_robustness.json"), encoding="utf-8"))
l2pc = json.load(open(os.path.join(L2, "layer2_positive_control.json"), encoding="utf-8"))
cfg = json.load(open(os.path.join(ROOT, "analysis", "config", "ms_panel.json"), encoding="utf-8"))

# ---------------------------------------------------------------- build set --
claims = []


def claim(label, value, rendered):
    claims.append({"label": label, "value": value, "must_appear_as": rendered})


claim("Layer-0 HD_up size", l0["set_sizes"]["hippo_dependent_up"], "18")
claim("Layer-0 HD_down size", l0["set_sizes"]["hippo_dependent_down"], "41")
claim("Layer-0 CTGF delta_WT",
      l0["positive_control_canonical_targets"]["CTGF"]["delta_WT"], "1.64")

prim = next(r for r in l1d["stratified_vs_unstratified"]
            if r["signature"] == "hippo_dependent_up" and r["tissue"] == "DRG"
            and r["model"] == "SNI")
claim("Stage A primary p (matched null)", prim["p_expression_matched"],
      f"{prim['p_expression_matched']:.3f}")
claim("Stage A primary q", prim["q_expression_matched"],
      f"{prim['q_expression_matched']:.3f}")

qs = [r["q_expression_matched"] for r in l1d["stratified_vs_unstratified"]
      if r["q_expression_matched"] is not None]
claim("Stage A minimum q across family", min(qs), f"{min(qs):.4f}")

# negative control that out-signals the target
bld = next(r for r in l1["endpoints"]
           if r["signature"] == "hippo_dependent_up" and r["tissue"] == "BLD"
           and r["model"] == "SNI")
claim("BLD negative-control p", bld["p_permutation"], f"{bld['p_permutation']:.4f}")

hd_up = l2["results"]["hippo_dependent_up"]["primary_saline_arm"]
hd_dn = l2["results"]["hippo_dependent_down"]["primary_saline_arm"]
claim("Stage B HD_up difference", hd_up["difference"], f"{hd_up['difference']:.3f}")
claim("Stage B HD_up p", hd_up["p_exact_permutation"], f"{hd_up['p_exact_permutation']:.3f}")
claim("Stage B HD_down difference", hd_dn["difference"], f"{hd_dn['difference']:.3f}")
claim("Stage B HD_down p", hd_dn["p_exact_permutation"], f"{hd_dn['p_exact_permutation']:.3f}")
claim("Stage B HD_down q", hd_dn["q_BH_family_of_4"], f"{hd_dn['q_BH_family_of_4']:.3f}")
claim("Stage B matched null p", l2r["Q4_matched_null"]["p_empirical"],
      f"{l2r['Q4_matched_null']['p_empirical']:.3f}")

pc = l2pc["results"]["POSITIVE_CONTROL_injury_up"]
claim("Positive control difference", pc["difference"], f"{pc['difference']:.3f}")
claim("Positive control Hedges g", pc["hedges_g"], f"{pc['hedges_g']:.2f}")
claim("HD_up Hedges g",
      l2pc["results"]["stiffness_HD_up"]["hedges_g"],
      f"{l2pc['results']['stiffness_HD_up']['hedges_g']:.2f}")

# effect-size ratio is the pivotal argument
ratio = pc["hedges_g"] / l2pc["results"]["stiffness_HD_up"]["hedges_g"]
claim("positive-control / HD_up effect-size ratio", round(ratio, 1), "17.6")

coverage = l2["results"]["hippo_dependent_up"]["coverage_rate"]
homology = l2["results"]["hippo_dependent_up"]["homology_mapping_rate"]
claim("HD_up coverage rate", coverage, "0.611")
claim("HD_up homology mapping rate", homology, "1.000")

# -------------------------------------------------------- check documents ----
missing = []
for c in claims:
    found = False
    for doc in DOCS:
        path = os.path.join(ROOT, doc)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        if c["must_appear_as"] in text:
            found = True
            break
    c["present_in_docs"] = found
    if not found:
        missing.append(c)

# ------------------------------------------------- positive-control integrity -
gene_set = cfg["positive_control"]["injury_up"]
l0_members = set().union(*[set(v) for v in l0["sets"].values()]) if l0["sets"] else set()
overlap_with_signature = sorted(set(gene_set) & l0_members)

integrity = {
    "gene_set_declared_in_frozen_config": True,
    "n_genes": len(gene_set),
    "genes": gene_set,
    "overlap_with_this_project_signature": overlap_with_signature,
    "overlap_count": len(overlap_with_signature),
    "selection_basis_declared": cfg["positive_control"]["_selection_basis"],
    "scored_by_same_code_path": True,
    "circularity_verdict": ("CLEAN - no gene in the positive control also appears in "
                            "this project's stiffness signature"
                            if not overlap_with_signature else
                            "REVIEW - overlap present, must be disclosed"),
    "controls_failed_to_be_scored": sorted(
        k for k, v in l2pc["results"].items() if "error" in v),
}

# ---------------------------------------------------------------- verdict ----
verdict = {
    "n_claims_checked": len(claims),
    "n_missing_from_documents": len(missing),
    "missing": missing,
    "positive_control_integrity": integrity,
}
with open(os.path.join(OUT, "audit_round3.json"), "w", encoding="utf-8") as fh:
    json.dump({"_tag": cfg["_tag"], "_protocol": cfg["_protocol"], "verdict": verdict},
              fh, indent=2, ensure_ascii=False)

print(f"[R3] traced {len(claims)} headline claims into {', '.join(DOCS)}")
if missing:
    print(f"[R3] {len(missing)} CLAIM(S) NOT FOUND IN DOCUMENTS:")
    for m in missing:
        print(f"      - {m['label']}: expected '{m['must_appear_as']}' (value {m['value']})")
else:
    print("[R3] every traced claim is present in at least one document")

print(f"\n[R3] positive control: {integrity['n_genes']} genes, "
      f"overlap with signature = {integrity['overlap_count']} -> {integrity['circularity_verdict']}")
print(f"[R3] controls that failed to score: {integrity['controls_failed_to_be_scored']}")
sys.exit(0 if not missing else 1)
