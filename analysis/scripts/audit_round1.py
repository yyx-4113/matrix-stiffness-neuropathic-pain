#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT ROUND 1 - independent verification of suspected defects.

This script deliberately does NOT import the analysis pipeline's conclusions.
It re-derives every number from the raw inputs so that a defect in the pipeline
cannot hide behind a self-consistent artifact.

Checks
  A1  mapping rate per signature (does any endpoint breach the protocol's 0.7 floor?)
  A2  Layer-0 aggregate-then-filter ordering: are there symbols whose loci have
      MIXED biotypes? (if so, summing first contaminates the retained signal)
  A3  unnamed / placeholder cufflinks symbols ('-', '', 'XLOC_*')
  A4  Layer-1 Wilcoxon z rank-basis consistency (0-based ranks vs 1-based mean)
  A5  Layer-1 permutation sampling scheme (with vs without replacement)

Outputs: analysis/results/audit/audit_round1.json
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
CFG = os.path.join(ROOT, "analysis", "config", "ms_panel.json")
RAW = os.path.join(ROOT, "analysis", "data", "raw")
L0 = os.path.join(ROOT, "analysis", "results", "layer0")
L1 = os.path.join(ROOT, "analysis", "results", "layer1")
OUT = os.path.join(ROOT, "analysis", "results", "audit")
os.makedirs(OUT, exist_ok=True)

FNAME_RE = re.compile(r"^(GSM\d+)_(.+)_(1|40)kPa_Rep([123])\.txt\.gz$")
GTX_RE = re.compile(r'gene_id "([^"]+)"')
GTYPE_RE = re.compile(r'gene_type "([^"]+)"')

GENOTYPE_MAP = {"WT": "WT", "RAP2KO": "RAP2KO", "LATS1_2dKO": "LATSKO", "Y_TdKO": "YTKO"}


def human_to_mouse(sym):
    if sym.isupper():
        return sym[0] + sym[1:].lower()
    return sym


def load_biotype():
    cache = os.path.join(RAW, "_annotation", "gencode_v24lift37_geneid_to_biotype.tsv")
    if os.path.exists(cache):
        m = pd.read_csv(cache, sep="\t")
        return dict(zip(m["gene_id"], m["gene_type"]))
    gtf = os.path.join(RAW, "_annotation", "gencode.v24lift37.annotation.gtf.gz")
    out = {}
    with gzip.open(gtf, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.split("\t", 9)
            if len(f) < 9 or f[2] != "gene":
                continue
            gid = GTX_RE.search(f[8])
            gty = GTYPE_RE.search(f[8])
            if gid and gty:
                out[gid.group(1).split(".")[0]] = gty.group(1)
    return out


def main():
    cfg = json.load(open(CFG, encoding="utf-8"))
    sig = json.load(open(os.path.join(L0, "layer0_signature.json"), encoding="utf-8"))
    min_rate = cfg["layer1"]["species_mapping"]["min_acceptable_mapping_rate"]

    rep = {}
    raw_dir = os.path.join(RAW, "_gse98547")
    files = sorted(f for f in os.listdir(raw_dir) if FNAME_RE.match(f))

    # ---------------------------------------------- A2 / A3: raw-row audit --
    print("[AUD] A2/A3 raw-row audit (24 files) ...")
    btype = load_biotype()
    sym_biotypes = {}
    placeholder = 0
    n_rows = 0
    for fn in files:
        df = pd.read_csv(
            os.path.join(raw_dir, fn), sep="\t",
            usecols=["tracking_id", "gene_short_name", "FPKM"],
            compression="gzip",
            dtype={"tracking_id": str, "gene_short_name": str, "FPKM": float},
        )
        n_rows += len(df)
        df["sym"] = df["gene_short_name"].fillna("").str.strip()
        placeholder += int((df["sym"].isin(["", "-"])).sum())
        df["gid"] = df["tracking_id"].str.split(".").str[0]
        for sym, gid in zip(df["sym"], df["gid"]):
            sym_biotypes.setdefault(sym, set()).add(btype.get(gid))

    mixed = {s: sorted([b for b in bs if b]) for s, bs in sym_biotypes.items()
             if len([b for b in bs if b]) > 1}
    # how many MIXED symbols are kept by the any() rule, and how much of their
    # signal comes from non-protein-coding loci?
    mixed_kept = {s: bs for s, bs in mixed.items() if "protein_coding" in bs}
    # recompute the contamination magnitude for one representative file
    df0 = pd.read_csv(
        os.path.join(raw_dir, files[0]), sep="\t",
        usecols=["tracking_id", "gene_short_name", "FPKM"],
        compression="gzip", dtype={"tracking_id": str, "gene_short_name": str, "FPKM": float},
    )
    df0["sym"] = df0["gene_short_name"].fillna("").str.strip()
    df0["gid"] = df0["tracking_id"].str.split(".").str[0]
    df0["bt"] = df0["gid"].map(btype)
    contam_rows = df0[(df0["sym"].isin(mixed_kept)) & (df0["bt"] != "protein_coding")]
    tot_of_mixed = df0[df0["sym"].isin(mixed_kept)].groupby("sym")["FPKM"].sum()
    nc_of_mixed = contam_rows.groupby("sym")["FPKM"].sum()
    frac_nc = (nc_of_mixed / tot_of_mixed.replace(0, np.nan)).dropna()
    rep["A3_placeholder_symbols"] = {
        "total_rows_across_files": int(n_rows),
        "placeholder_rows": int(placeholder),
        "n_placeholder_symbols": len([s for s in sym_biotypes if s in ("", "-")]),
    }
    rep["A2_biotype_ordering"] = {
        "n_symbols": len(sym_biotypes),
        "n_symbols_with_multiple_loci": sum(1 for bs in sym_biotypes.values() if len(bs) > 1),
        "n_symbols_with_MIXED_biotypes": len(mixed),
        "n_mixed_symbols_retained_by_any_rule": len(mixed_kept),
        "example_mixed": dict(list(mixed.items())[:5]),
        "median_fraction_of_signal_from_noncoding_loci": (
            round(float(frac_nc.median()), 4) if len(frac_nc) else None
        ),
        "n_symbols_with_noncoding_fraction_gt_10pct": int((frac_nc > 0.10).sum()),
    }
    print(f"      mixed-biotype symbols: {len(mixed)}; retained by any(): {len(mixed_kept)}")

    # ------------------------------------------------------- A1: mapping ---
    print("[AUD] A1 mapping rate per signature ...")
    import openpyxl
    tbl_path = os.path.join(RAW, "GSE111216_Parisien_Suppl_Table_06_gene_DRG_CTRvsSNI.xlsx")
    wb = openpyxl.load_workbook(tbl_path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    it = ws.iter_rows(values_only=True)
    hdr = [str(c).strip() if c is not None else "" for c in next(it)]
    gi = hdr.index("gene")
    mouse_syms = set()
    for r in it:
        if r is None or r[gi] is None:
            continue
        mouse_syms.add(str(r[gi]).strip())
    wb.close()

    mp = {}
    for key, members in sig["sets"].items():
        if not members:
            continue
        mapped = [human_to_mouse(g) for g in members]
        present = [m for m in mapped if m in mouse_syms]
        rate = len(present) / len(members)
        mp[key] = {
            "n_human": len(members),
            "n_present": len(present),
            "mapping_rate": round(rate, 4),
            "breaches_protocol_floor": bool(rate < min_rate),
        }
    rep["A1_mapping_rates"] = {
        "protocol_min_acceptable_rate": min_rate,
        "per_signature": mp,
        "breaching_keys": [k for k, v in mp.items() if v["breaches_protocol_floor"]],
    }
    print(f"      breaching keys: {rep['A1_mapping_rates']['breaching_keys']}")

    # ------------------------------------------- A4: rank-basis arithmetic --
    print("[AUD] A4 Wilcoxon z rank basis ...")
    # the pipeline builds ranks with np.arange(len) -> 0-based (0 .. n-1)
    # but standardises with mu = m*(n+1)/2, the 1-based expectation.
    n_demo = 15000
    m_demo = 11
    sd = np.sqrt(m_demo * (n_demo - m_demo) * (n_demo + 1) / 12.0)
    bias = m_demo / sd
    rep["A4_rank_basis"] = {
        "rank_construction": "np.arange(len(df)) -> 0-based ranks in [0, n-1]",
        "expectation_used": "mu = m*(n+1)/2  (the 1-based formula)",
        "correct_expectation_for_0_based": "mu = m*(n-1)/2",
        "systematic_z_bias_units": round(float(bias), 6),
        "verdict": "logic defect; numerical impact negligible at n~15k but must be fixed",
    }
    print(f"      z bias = {bias:.6f}")

    # ------------------------------------------ A5: permutation sampling ---
    print("[AUD] A5 permutation sampling scheme ...")
    rng = np.random.default_rng(20261021)
    n_bg, m_bg, iters = 15000, 33, 20000
    idx = rng.integers(0, n_bg, size=(iters, m_bg))
    dup_frac = float(np.mean([len(np.unique(row)) < m_bg for row in idx]))
    rep["A5_sampling"] = {
        "scheme": "rng.integers(0, n, size=(n_iter, m)) -> WITH replacement",
        "protocol_wording": "random gene SUBSET of the same size |S|",
        "empirical_fraction_of_draws_containing_a_duplicate_gene": round(dup_frac, 4),
        "verdict": "should be without replacement; duplicate genes shrink the effective "
                   "module size and widen the null",
    }
    print(f"      draws with a duplicated gene: {dup_frac:.4f}")

    # ------------------------------------------------- A6: endpoint roles ---
    print("[AUD] A6 endpoint role vs protocol downgrade rule ...")
    l2 = json.load(open(os.path.join(ROOT, "analysis/results/layer2/layer2_results.json"),
                        encoding="utf-8"))["results"]
    roles = {}
    for k, v in l2.items():
        rate = v["homology_mapping_rate"]
        roles[k] = {
            "declared_role": v["endpoint_role"],
            "mapping_rate": round(rate, 4) if rate is not None else None,
            "must_downgrade_to_exploratory": bool(rate is not None and rate < min_rate),
        }
    rep["A6_endpoint_governance"] = {
        "protocol_rule": "mapping_rate < 0.7 -> primary endpoint downgraded to exploratory",
        "stage_B": roles,
        "violations": [k for k, v in roles.items()
                       if v["must_downgrade_to_exploratory"]
                       and "primary" in v["declared_role"]],
    }
    print(f"      governance violations: {rep['A6_endpoint_governance']['violations']}")

    with open(os.path.join(OUT, "audit_round1.json"), "w", encoding="utf-8") as fh:
        json.dump({"_tag": cfg["_tag"], "_protocol": cfg["_protocol"], "audit": rep},
                  fh, indent=2, ensure_ascii=False)
    print("\n[AUD] wrote audit_round1.json")

    print("\n" + "=" * 74)
    print("ROUND-1 AUDIT VERDICT")
    print("=" * 74)
    breaches = rep["A1_mapping_rates"]["breaching_keys"]
    viol = rep["A6_endpoint_governance"]["violations"]
    print(f"  A1 signature keys breaching the 0.7 mapping floor : {breaches}")
    print(f"  A2 mixed-biotype symbols retained by any() rule   : {len(mixed_kept)}")
    print(f"  A3 placeholder symbol rows                        : {placeholder}")
    print(f"  A4 rank-basis logic defect                        : PRESENT")
    print(f"  A5 with-replacement sampling (should be w/o)      : PRESENT")
    print(f"  A6 endpoint-governance violations                 : {viol}")


if __name__ == "__main__":
    main()
