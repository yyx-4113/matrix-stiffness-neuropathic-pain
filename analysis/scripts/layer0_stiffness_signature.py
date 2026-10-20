#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layer 0 - Export the stiffness-response signature from GSE98547.

Every parameter comes from the FROZEN config analysis/config/ms_panel.json.
The rules implemented here were specified in PROTOCOL v0.1 BEFORE any Layer-1
expression data were examined. Do not edit parameters here; edit the config.

Outputs (analysis/results/layer0/):
  layer0_signature.json     summary + per-class gene lists + statistics
  layer0_gene_level.csv     gene-level table across all four genotypes
  layer0_diagnostics.json   filtering / detection diagnostics
"""

import gzip
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy import stats

# ---------------------------------------------------------------- paths ----
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # project root
CFG_PATH = os.path.join(ROOT, "analysis", "config", "ms_panel.json")
RAW_DIR = os.path.join(ROOT, "analysis", "data", "raw", "_gse98547")
OUT_DIR = os.path.join(ROOT, "analysis", "results", "layer0")
os.makedirs(OUT_DIR, exist_ok=True)

# genotype in filename -> canonical key used in the config
GENOTYPE_MAP = {
    "WT": "WT",
    "RAP2KO": "RAP2KO",
    "LATS1_2dKO": "LATSKO",
    "Y_TdKO": "YTKO",
}

FNAME_RE = re.compile(r"^(GSM\d+)_(.+)_(1|40)kPa_Rep([123])\.txt\.gz$")

ANNOT_DIR = os.path.join(ROOT, "analysis", "data", "raw", "_annotation")
GTF_NAME = "gencode.v24lift37.annotation.gtf.gz"
GENE_MAP_CACHE = "gencode_v24lift37_geneid_to_biotype.tsv"

GTX_RE = re.compile(r'gene_id "([^"]+)"')
GTYPE_RE = re.compile(r'gene_type "([^"]+)"')


def load_gencode_biotype(cfg_keep):
    """Parse the GTF once -> {gene_id (no version): gene_type}. Cached to TSV.

    Implements protocol v0.2 R2: the biotype filter must be annotation-driven,
    not symbol-pattern heuristics.
    """
    cache_path = os.path.join(ANNOT_DIR, GENE_MAP_CACHE)
    if os.path.exists(cache_path):
        m = pd.read_csv(cache_path, sep="\t")
        return dict(zip(m["gene_id"], m["gene_type"]))

    gtf_path = os.path.join(ANNOT_DIR, GTF_NAME)
    if not os.path.exists(gtf_path):
        sys.exit(
            f"missing annotation {gtf_path}\n"
            f"download from: https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/"
            f"release_24/GRCh37_mapping/{GTF_NAME}"
        )
    out = {}
    n = 0
    with gzip.open(gtf_path, "rt") as fh:
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
                n += 1
    pd.DataFrame({"gene_id": list(out), "gene_type": list(out.values())}).to_csv(
        cache_path, sep="\t", index=False
    )
    print(f"[L0] parsed {n} gene records from GENCODE v24lift37 -> cached")
    return out


def bh_qvalues(p):
    """Benjamini-Hochberg q-values.

    v0.2 R3: NaN p-values (Welch t undefined when both groups are constant)
    are treated as 1.0 rather than propagated into the whole column.
    """
    p = np.asarray(p, dtype=float)
    p = np.where(np.isnan(p), 1.0, p)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0, 1)
    out = np.empty(n, dtype=float)
    out[order] = q
    return out


def build_matrix():
    """Read 24 per-sample cufflinks tables -> genes x samples FPKM matrix."""
    if not os.path.isdir(RAW_DIR):
        sys.exit(f"missing raw directory: {RAW_DIR}")
    files = sorted(f for f in os.listdir(RAW_DIR) if FNAME_RE.match(f))
    if len(files) != 24:
        sys.exit(f"expected 24 sample files, found {len(files)}")

    series = {}
    symbol_to_gids = {}
    dup_report = {}
    for fn in files:
        m = FNAME_RE.match(fn)
        genotype_raw, stiffness, rep = m.group(2), int(m.group(3)), m.group(4)
        genotype = GENOTYPE_MAP[genotype_raw]
        label = f"{genotype}_{stiffness}kPa_Rep{rep}"
        df = pd.read_csv(
            os.path.join(RAW_DIR, fn),
            sep="\t",
            usecols=["tracking_id", "gene_short_name", "FPKM"],
            compression="gzip",
            dtype={"tracking_id": str, "gene_short_name": str, "FPKM": float},
        )
        df["gene_short_name"] = df["gene_short_name"].str.strip()
        before = len(df)
        # same symbol annotated at >1 locus -> sum FPKM (conservative, keeps signal)
        s = df.groupby("gene_short_name")["FPKM"].sum()
        dup_report[label] = {"rows": int(before), "symbols": int(s.size)}
        series[label] = s
        # track which gene_ids back each symbol (needed for the biotype filter)
        df["gid"] = df["tracking_id"].str.split(".").str[0]
        for sym, gid in zip(df["gene_short_name"], df["gid"]):
            symbol_to_gids.setdefault(sym, set()).add(gid)

    mat = pd.DataFrame(series)
    mat = mat.sort_index()
    return mat, dup_report, files, symbol_to_gids


def _positive_control(tbl, targets):
    """v0.2: report the WT stiffness displacement of canonical YAP/TAZ targets.

    If these do not move upward on the stiff matrix, the signature has no
    biological anchor and the whole export must be treated as failed.
    """
    rows = {}
    for g in targets:
        if g not in tbl.index:
            rows[g] = {"present": False}
            continue
        r = tbl.loc[g]
        rows[g] = {
            "present": True,
            "delta_WT": round(float(r["delta_WT"]), 4),
            "p_WT": None if np.isnan(r["p_WT"]) else float(r["p_WT"]),
            "q_WT": None if np.isnan(r["q_WT"]) else float(r["q_WT"]),
            "delta_YTKO": round(float(r["delta_YTKO"]), 4),
            "ratio_YTKO_over_WT": None if np.isnan(r["ratio_YTKO_over_WT"]) else round(float(r["ratio_YTKO_over_WT"]), 4),
            "call": str(r["call"]),
            "hippo_class": str(r["hippo_class"]),
        }
    present = [g for g, v in rows.items() if v.get("present")]
    up_ok = [g for g in present if rows[g]["delta_WT"] > 0]
    rows["_summary"] = {
        "n_present": len(present),
        "n_present_and_upregulated": len(up_ok),
        "pass": len(present) > 0 and len(up_ok) / len(present) >= 0.75,
    }
    return rows


def main():
    with open(CFG_PATH, encoding="utf-8") as fh:
        cfg = json.load(fh)
    l0 = cfg["layer0"]

    print("[L0] building FPKM matrix ...")
    mat, dup_report, files, symbol_to_gids = build_matrix()
    n_genes_raw = mat.shape[0]
    print(f"[L0] {n_genes_raw} symbols x {mat.shape[1]} samples")

    # ---- biotype filter (v0.2 R2, annotation-driven) ---------------------
    bt = l0["biotype_filter"]
    gencode = load_gencode_biotype(bt["keep_gene_type"])
    keep_bt = bt["keep_gene_type"]

    def symbol_is_kept(sym):
        gids = symbol_to_gids.get(sym, ())
        return any(gencode.get(g) in keep_bt for g in gids)

    biotype_ok = pd.Series([symbol_is_kept(s) for s in mat.index], index=mat.index)
    n_before_biotype = int(mat.shape[0])

    # ---- detection filter (frozen rule) ----------------------------------
    d = l0["detection_filter"]
    detected = (mat > d["min_fpkm"]).sum(axis=1)
    keep = detected >= d["min_samples"]
    keep = keep & biotype_ok
    diagnostics = {
        "input_symbols": int(n_genes_raw),
        "biotype_filter_note": f"{bt['annotation']}; keep gene_type in {keep_bt}",
        "symbols_before_biotype": n_before_biotype,
        "symbols_passing_biotype": int(biotype_ok.sum()),
        "detection_rule": f"FPKM > {d['min_fpkm']} in >= {d['min_samples']}/{d['of_total']} samples",
        "genes_passing": int(keep.sum()),
        "genes_dropped": int((~keep).sum()),
        "per_file_rows_vs_symbols": dup_report,
        "files": files,
    }
    mat = mat.loc[keep]
    print(f"[L0] biotype filter keeps {int(biotype_ok.sum())} / {n_genes_raw} symbols")
    print(f"[L0] + detection filter keeps {keep.sum()} / {n_genes_raw} symbols")

    # ---- transform -------------------------------------------------------
    assert l0["transform"] == "log2(FPKM + 1)"
    lg = np.log2(mat + 1.0)

    samples = list(lg.columns)
    meta = pd.DataFrame(
        [
            {
                "sample": s,
                "genotype": s.split("_")[0],
                "stiffness_kPa": int(s.split("_")[1].replace("kPa", "")),
                "rep": int(s.split("_")[2].replace("Rep", "")),
            }
            for s in samples
        ]
    ).set_index("sample")

    # ---- per-genotype stiffness contrast (Welch) -------------------------
    sig = l0["signature_definition"]
    rows = {}
    for gt in l0["genotypes"].keys():
        soft = meta.index[(meta.genotype == gt) & (meta.stiffness_kPa == l0["factor_stiffness"]["soft_kPa"])]
        stiff = meta.index[(meta.genotype == gt) & (meta.stiffness_kPa == l0["factor_stiffness"]["stiff_kPa"])]
        assert len(soft) == len(stiff) == 3, f"unexpected n for {gt}"
        t, p = stats.ttest_ind(lg[stiff], lg[soft], axis=1, equal_var=False)
        delta = lg[stiff].mean(axis=1) - lg[soft].mean(axis=1)
        rows[gt] = pd.DataFrame(
            {
                f"delta_{gt}": delta,
                f"p_{gt}": p,
                f"mean_stiff_{gt}": lg[stiff].mean(axis=1),
                f"mean_soft_{gt}": lg[soft].mean(axis=1),
            }
        )
        print(f"[L0] {gt}: delta computed (mean |delta| = {np.abs(delta).mean():.4f})")

    tbl = pd.concat(rows.values(), axis=1)

    # BH q within the WT contrast (reported, not used for signature calling)
    tbl["q_WT"] = bh_qvalues(tbl["p_WT"].values)

    # ---- signature calling in WT ----------------------------------------
    up = (tbl["p_WT"] < sig["p_threshold"]) & (tbl["delta_WT"] >= sig["abs_log2fc_threshold"])
    dn = (tbl["p_WT"] < sig["p_threshold"]) & (tbl["delta_WT"] <= -sig["abs_log2fc_threshold"])
    tbl["call"] = np.where(up, "stiffness_up", np.where(dn, "stiffness_down", "ns"))
    print(f"[L0] WT signature: {int(up.sum())} up, {int(dn.sum())} down")

    # ---- Hippo stratification (frozen rules) ----------------------------
    h = l0["hippo_stratification"]
    d_wt = tbl["delta_WT"]
    d_yt = tbl["delta_YTKO"]
    d_lats = tbl["delta_LATSKO"]
    d_rap2 = tbl["delta_RAP2KO"]

    called = tbl["call"].isin(["stiffness_up", "stiffness_down"])

    same_sign_yt = np.sign(d_wt) == np.sign(d_yt)
    opp_sign_yt = ~same_sign_yt
    ratio_yt = d_yt.abs() / d_wt.abs().replace(0, np.nan)

    # v0.2 R1: dependence is declared on magnitude collapse alone.
    # A fully abolished response has no informative sign.
    hd_mask = called & (ratio_yt <= h["hippo_dependent"]["max_ratio_abs"])
    # v0.2 R1: response retained in magnitude but flipped in direction
    rev_mask = called & opp_sign_yt & (ratio_yt > h["hippo_dependent"]["max_ratio_abs"])
    hi_mask = (
        called & same_sign_yt & (ratio_yt >= h["hippo_independent"]["min_ratio_abs"])
    )

    tbl["hippo_class"] = np.select(
        [hd_mask, rev_mask, hi_mask],
        ["hippo_dependent", "reversed", "hippo_independent"],
        default=np.where(tbl["call"] != "ns", "ambiguous", "ns"),
    )
    tbl["hippo_class"] = pd.Series(tbl["hippo_class"], index=tbl.index)
    tbl["ratio_YTKO_over_WT"] = ratio_yt
    tbl["ratio_LATSKO_over_WT"] = d_lats.abs() / d_wt.abs().replace(0, np.nan)
    tbl["ratio_RAP2KO_over_WT"] = d_rap2.abs() / d_wt.abs().replace(0, np.nan)

    counts = tbl["hippo_class"].value_counts().to_dict()
    print(f"[L0] hippo classes: {counts}")

    # secondary confirmation: does LATS1/2-dKO also abolish the response?
    hd_genes = tbl.index[tbl["hippo_class"] == "hippo_dependent"]
    hi_genes = tbl.index[tbl["hippo_class"] == "hippo_independent"]
    amb_genes = tbl.index[tbl["hippo_class"] == "ambiguous"]

    def frac_lats_confirms(genes):
        sub = tbl.loc[genes]
        return float((sub["ratio_LATSKO_over_WT"] <= h["hippo_dependent"]["max_ratio_abs"]).mean())

    lats_confirm = {
        "hippo_dependent": frac_lats_confirms(hd_genes),
        "hippo_independent": frac_lats_confirms(hi_genes),
    }
    print(f"[L0] LATS1/2-dKO confirmation fraction: {lats_confirm}")

    # direction-sorted, validated sets actually used downstream
    sets_out = {}
    for cls in ["hippo_dependent", "hippo_independent", "reversed", "ambiguous"]:
        for direction, call_name in [("up", "stiffness_up"), ("down", "stiffness_down")]:
            members = sorted(tbl.index[(tbl["hippo_class"] == cls) & (tbl["call"] == call_name)])
            sets_out[f"{cls}_{direction}"] = members

    # ---- write outputs ---------------------------------------------------
    gene_csv = os.path.join(OUT_DIR, "layer0_gene_level.csv")
    tbl.round(6).to_csv(gene_csv)

    summary = {
        "_tag": cfg["_tag"],
        "_protocol": cfg["_protocol"],
        "source": "GSE98547",
        "transform": l0["transform"],
        "n_samples": int(lg.shape[1]),
        "signature_thresholds": {
            "p": sig["p_threshold"],
            "abs_log2fc": sig["abs_log2fc_threshold"],
            "bh_used_for_calling": sig["bh_corrected"],
        },
        "counts": {
            "stiffness_up": int(up.sum()),
            "stiffness_down": int(dn.sum()),
            "hippo_class": {k: int(v) for k, v in counts.items()},
        },
        "set_sizes": {k: len(v) for k, v in sets_out.items()},
        "lats_confirmation_fraction": lats_confirm,
        "sets": sets_out,
        "positive_control_canonical_targets": _positive_control(tbl, l0["canonical_yap_taz_targets"]),
        "canonical_yap_taz_targets_sensitivity_S4": l0["canonical_yap_taz_targets"],
        "canonical_targets_present_after_filter": [
            g for g in l0["canonical_yap_taz_targets"] if g in tbl.index
        ],
    }
    with open(os.path.join(OUT_DIR, "layer0_signature.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT_DIR, "layer0_diagnostics.json"), "w", encoding="utf-8") as fh:
        json.dump(diagnostics, fh, indent=2, ensure_ascii=False)

    print("[L0] wrote layer0_signature.json / layer0_gene_level.csv / layer0_diagnostics.json")
    for k, v in summary["set_sizes"].items():
        print(f"      {k}: {v}")


if __name__ == "__main__":
    main()
