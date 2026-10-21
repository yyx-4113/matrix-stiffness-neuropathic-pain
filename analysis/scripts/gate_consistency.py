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

import gzip
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def version_tuple(text):
    """'v0.3.1' -> (0, 3, 1); non-numeric suffixes are ignored."""
    t = str(text).strip().lstrip("vV")
    parts = []
    for chunk in t.split("."):
        num = ""
        for ch in chunk:
            if ch.isdigit():
                num += ch
            else:
                break
        parts.append(int(num) if num else 0)
    return tuple(parts)

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
# Derived, not hard-coded: with 4 vs 4 the enumeration visits each distinct
# split twice (a set and its complement), so the smallest attainable two-sided
# exact p is 2 / n_enumerated. Hard-coding 1/35 here would silently protect a
# stale number the day the design changes.
_n_enum = r2["hippo_dependent_down"]["primary_saline_arm"]["n_permutations_enumerated"]
_min_attainable_p = 2.0 / _n_enum
chk("L2 HD_down exact p equals the enumeration lower bound",
    abs(r2["hippo_dependent_down"]["primary_saline_arm"]["p_exact_permutation"]
        - _min_attainable_p) < 1e-6,
    f"p={r2['hippo_dependent_down']['primary_saline_arm']['p_exact_permutation']} "
    f"lower_bound={_min_attainable_p:.6f} (n_enumerated={_n_enum})")
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
    L2R["n_members_present"] == r2["hippo_dependent_down"]["n_present_after_filter"],
    (L2R["n_members_present"], r2["hippo_dependent_down"]["n_present_after_filter"]))

# ------------------------------------------------------------- protocol ------
MIN_PROTO_VERSION = "v0.4"
pv = CFG["_protocol"].split()[-1]
chk(f"Protocol version is {MIN_PROTO_VERSION} or later",
    version_tuple(pv) >= version_tuple(MIN_PROTO_VERSION),
    f"declared={pv} required>={MIN_PROTO_VERSION}")
chk("Permutation seed is the pre-specified one",
    CFG["layer1"]["rank_test"]["permutation"]["seed"] == 20261021,
    CFG["layer1"]["rank_test"]["permutation"]["seed"])
chk("Protocol declares separate mapping-rate and coverage-rate governance",
    "min_acceptable_mapping_rate" in CFG["layer1"]["species_mapping"]
    and "min_acceptable_coverage_rate" in CFG["layer1"]["species_mapping"],
    list(CFG["layer1"]["species_mapping"]))

# ------------------------------------------------- independent recomputation -
# The discipline note is explicit: verifying that artifacts agree with each other
# only proves self-consistency. These checks re-derive headline numbers straight
# from the deposited raw inputs, so a bug in the pipeline cannot pass the gate.
print("[gate] independent recomputation from raw inputs ...")

scores = pd.read_csv(os.path.join(ROOT, "analysis/results/layer2/layer2_sample_scores.csv"))
hd = scores[scores.signature == "hippo_dependent_down"]
# column labels are '<agent>_<group><rep>', e.g. 'saline_SNI1'
hd = hd.assign(
    agent=hd["sample"].str.split("_").str[0],
    group=hd["sample"].str.split("_").str[1].str.replace(r"\d+$", "", regex=True),
)
sni = hd[(hd.agent == "saline") & (hd.group == "SNI")]["score"]
sham = hd[(hd.agent == "saline") & (hd.group == "sham")]["score"]
recomputed_diff = float(sni.mean() - sham.mean())
reported_diff = r2["hippo_dependent_down"]["primary_saline_arm"]["difference"]
chk("RECOMPUTE Stage B HD_down saline-arm difference from deposited scores",
    abs(recomputed_diff - reported_diff) < 1e-4,
    f"recomputed={recomputed_diff:+.6f} reported={reported_diff:+.6f}")
chk("RECOMPUTE all 4 SNI animals exceed all 4 sham animals",
    float(sni.min()) > float(sham.max()),
    f"min SNI={sni.min():+.4f} > max sham={sham.max():+.4f}")

# recompute the Layer-0 flagship number (CTGF stiff-vs-soft in WT) from FPKM
raw_dir = os.path.join(ROOT, "analysis", "data", "raw", "_gse98547")
wt = {}
for fn in sorted(os.listdir(raw_dir)):
    m = re.match(r"^GSM\d+_WT_(1|40)kPa_Rep([123])\.txt\.gz$", fn)
    if not m:
        continue
    stiff, rep = m.group(1), m.group(2)
    df = pd.read_csv(os.path.join(raw_dir, fn), sep="\t",
                     usecols=["gene_short_name", "FPKM"], compression="gzip")
    v = df.loc[df["gene_short_name"].str.strip() == "CTGF", "FPKM"].sum()
    wt[f"{stiff}_{rep}"] = float(v)
# NOTE the order matters and matches Layer-0: log2(FPKM+1) is applied per
# sample FIRST, then averaged within each stiffness arm, then differenced.
# Averaging raw FPKM first and transforming afterwards is NOT equivalent.
soft_mean = float(np.mean([np.log2(wt[f"1_{r}"] + 1) for r in "123"]))
stiff_mean = float(np.mean([np.log2(wt[f"40_{r}"] + 1) for r in "123"]))
d_recomp = stiff_mean - soft_mean
pc_ctgf = L0["positive_control_canonical_targets"]["CTGF"]
chk("RECOMPUTE Layer-0 CTGF log2 stiffness displacement from raw FPKM",
    abs(d_recomp - pc_ctgf["delta_WT"]) < 1e-3,
    f"recomputed={d_recomp:+.6f} reported={pc_ctgf['delta_WT']:+.6f}")

# mapping rate must be recomputed, not trusted from the pipeline
sig = L0
import openpyxl as _ox
_wb = _ox.load_workbook(
    os.path.join(ROOT, "analysis", "data", "raw",
                 "GSE111216_Parisien_Suppl_Table_06_gene_DRG_CTRvsSNI.xlsx"),
    read_only=True, data_only=True)
_ws = _wb[_wb.sheetnames[0]]
_it = _ws.iter_rows(values_only=True)
_h = [str(c).strip() if c is not None else "" for c in next(_it)]
_gi = _h.index("gene")
_mouse = set()
for _r in _it:
    if _r is None or _r[_gi] is None:
        continue
    _mouse.add(str(_r[_gi]).strip())
_wb.close()
_h2m = lambda s: s[0] + s[1:].lower() if s.isupper() else s
recomputed_map = sum(1 for g in sig["sets"]["hippo_dependent_up"]
                     if _h2m(g) in _mouse) / len(sig["sets"]["hippo_dependent_up"])
chk("RECOMPUTE homology mapping rate of HD_up (must clear the 0.7 floor)",
    recomputed_map >= CFG["layer1"]["species_mapping"]["min_acceptable_mapping_rate"],
    f"recomputed={recomputed_map:.4f}")

# ------------------------------------------------------- Layer 3 (v0.5) ------
def _load_table(path):
    """Independent re-read of a deposited contrast table (gate must not trust
    the pipeline's in-memory objects). De-duplication on SYMBOL before it
    becomes the index is mandatory - see the R12 note in the protocol."""
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)
    header = [str(c).strip() if c is not None else "" for c in next(rows)]
    df = pd.DataFrame([r for r in rows
                       if r is not None and not all(v is None for v in r)],
                      columns=header).rename(columns={"gene": "symbol"})
    for c in ["value_CTR", "p_value", "log2_fc", "log2_fcZ", "pi_value"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["symbol"] = df["symbol"].astype(str).str.strip()
    df = df.drop_duplicates(subset="symbol", keep="first")
    return df.set_index("symbol")


def _ranks_of(df, var):
    order = np.argsort(df[var].to_numpy(), kind="mergesort")
    arr = np.empty(len(df))
    arr[order] = np.arange(len(df))
    return pd.Series(arr, index=df.index)


L3P = os.path.join(ROOT, "analysis", "results", "layer3", "layer3_generality.json")
L3 = json.load(open(L3P, encoding="utf-8"))

n_fail_l3 = sum(1 for v in L3["per_set_specificity"].values()
                if v["specificity_failed"] is True)
chk("L3 verdict is derived, not hard-coded: fail-count matches per-set flags",
    n_fail_l3 == L3["n_sets_failing_specificity"],
    (L3["n_sets_failing_specificity"], n_fail_l3))
chk("L3 verdict is derived: PASS iff fail-count >= 4",
    bool(L3["primary_endpoint_pass"]) == bool(n_fail_l3 >= 4),
    (L3["primary_endpoint_pass"], n_fail_l3))
chk("L3 tested all 5 pre-specified independent gene sets",
    L3["n_sets_tested"] == 5, L3["n_sets_tested"])
chk("L3 test family is 5 sets x 4 tissues x 2 models = 40",
    L3["n_tests"] == 40, L3["n_tests"])
l3t = pd.DataFrame(L3["table"])
chk("L3 every set has a finite specificity index",
    all(np.isfinite(v["SI"]) for v in L3["per_set_specificity"].values()),
    [g for g, v in L3["per_set_specificity"].items() if not np.isfinite(v["SI"])])
chk("L3 background is not degenerate (>1000 expressed genes in every contrast)",
    bool((l3t["n_expressed_background"] > 1000).all()),
    int(l3t["n_expressed_background"].min()))
chk("L3 every set retains >=3 members in every contrast",
    bool((l3t["n_mouse_present"] >= 3).all()),
    int(l3t["n_mouse_present"].min()))
chk("L3 BH q-values are within [0,1]",
    bool(((l3t["q_matched_BH40"] >= 0) & (l3t["q_matched_BH40"] <= 1)).all()),
    (float(l3t["q_matched_BH40"].min()), float(l3t["q_matched_BH40"].max())))

# RECOMPUTE Layer-3 G2 (YAP/TAZ canonical targets) MRU in the DRG-SNI contrast
# straight from the deposited xlsx, with no reliance on the pipeline's artefacts.
_g2 = [g for g in CFG["layer3"]["gene_sets"]["G2_yap_taz_canonical_targets"]["members"]]
_g2m = [(_h2m(g)) for g in _g2]
_d3 = _load_table(os.path.join(ROOT, "analysis", "data", "raw",
                              "GSE111216_Parisien_Suppl_Table_06_gene_DRG_CTRvsSNI.xlsx"))
_e3 = _d3[_d3["value_CTR"] > 0]
_e3 = _e3[np.isfinite(_e3["log2_fc"])]
_r3 = _ranks_of(_e3, "log2_fc")
_p3 = [g for g in _g2m if g in _e3.index]
_mru3 = float(np.median(_r3.loc[_p3].to_numpy()) / (len(_e3) - 1))
_row3 = l3t[(l3t.gene_set == "G2_yap_taz_canonical_targets")
            & (l3t.tissue == "DRG") & (l3t.model == "SNI")]["MRU"].iloc[0]
chk("RECOMPUTE Layer-3 G2 MRU (DRG-SNI) from deposited table",
    abs(_mru3 - _row3) < 1e-6,
    f"recomputed={_mru3:.6f} reported={_row3:.6f}")

# ------------------------------------------------------- audit R10 (v0.5) ----
TI_P = os.path.join(ROOT, "analysis", "results", "audit",
                    "audit_tissue_identity.json")
TI = json.load(open(TI_P, encoding="utf-8"))
gap = float(TI["sensory_minus_myelin"])
chk("R10 tissue-identity resolved by expression markers (sensory - myelin > 2 log2)",
    bool(np.isfinite(gap)) and gap > 2.0, f"gap={gap:+.3f}")
chk("R10 all 5 myelin markers detected in the matrix",
    all(TI["markers_present"][g] for g in ["Mbp", "Plp1", "Mog", "Cnp", "Mag"]),
    [g for g in ["Mbp", "Plp1", "Mog", "Cnp", "Mag"] if not TI["markers_present"][g]])

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
