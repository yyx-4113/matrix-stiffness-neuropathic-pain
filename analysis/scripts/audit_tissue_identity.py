#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit R10 - resolve the GSE261676 tissue-label conflict by expression evidence.

CONFLICT
--------
The GEO series matrix for GSE261676 reports, for all 16 samples:

    !Sample_source_name_ch1     "spinal cord"
    !Sample_characteristics_ch1 "tissue: spinal cord"
    !Sample_characteristics_ch1 "cell type: dorsal root ganglia"

while the associated paper (Serafini RA, et al. Neurobiol Pain 2024;15:100153,
PMID 38549875) states that RNA-seq was performed on dorsal root ganglia.

A tissue label is metadata and can be wrong; it should not be taken on trust
when the deposited data can adjudicate.

DISCRIMINATING LOGIC
--------------------
The two tissues differ structurally in a way no normalisation can mask:

  * Spinal cord contains white matter, i.e. oligodendrocyte myelin ->
    MBP / PLP1 / MOG transcripts are abundant.
  * DRG contains pseudo-unipolar sensory somata and satellite glia, and NO
    oligodendrocytes and NO CNS myelin -> Mbp/Plp1/Mog are near background.

  * DRG is dominated by peripheral sensory neuron somata ->
    high Prph (peripherin), Ntrk1 (TrkA), Scn10a (Nav1.8), Calca/Tac1.
  * Spinal cord grey matter carries intrinsic CNS neurons and glia ->
    relatively higher Gfap/Aqp4 and lower Prph/Scn10a.

We therefore report, per sample, the CPM of a compact marker panel and two
contrast scores:

    myelin_score   = mean log2CPM of (Mbp, Plp1, Mog, Cnp, Mag)
    sensory_score = mean log2CPM of (Prph, Ntrk1, Scn10a, Calca, Tac1, Piezo2)

RULE (pre-specified here, before looking):
    if myelin_score is at/near background while sensory_score is high
        -> the tissue is DRG   (paper is right; GEO source_name is wrong)
    if myelin_score is high
        -> the tissue is spinal cord (GEO is right; the analysis must be relabelled)
    if both are high or both low -> inconclusive, report as such.
"""

import gzip
import json
import os
import re

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RAW_DIR = os.path.join(ROOT, "analysis", "data", "raw")
DATA_DIR = os.path.join(RAW_DIR, "_gse261676")
OUT_DIR = os.path.join(ROOT, "analysis", "results", "audit")
os.makedirs(OUT_DIR, exist_ok=True)

FNAME_RE = re.compile(r"^GSM\d+[_-](.+?)_S\d+\.counts\.txt\.gz$")

MYELIN = ["Mbp", "Plp1", "Mog", "Cnp", "Mag"]
SENSORY = ["Prph", "Ntrk1", "Scn10a", "Calca", "Tac1", "Piezo2"]
CNS_NEURON = ["Snap25", "Syt1", "Rbfox3", "Slc17a6"]
GLIA = ["Gfap", "Aqp4", "Slc1a2"]
SATELLITE = ["Fabp7", "Apoh"]


def build_counts():
    series, meta = {}, {}
    for fn in sorted(os.listdir(DATA_DIR)):
        m = FNAME_RE.match(fn)
        if not m:
            continue
        gsm = fn.split("_")[0]
        sample_full = m.group(1)
        low = sample_full.lower()
        agent = "DMI" if low.startswith("dmi") else "saline"
        grp = "SNI" if "sni" in low else "sham"
        label = f"{agent}_{grp}"
        df = pd.read_csv(os.path.join(DATA_DIR, fn), sep="\t", header=None,
                         names=["ens", "count"], compression="gzip",
                         dtype={"ens": str, "count": float})
        counts = {}
        for e, c in zip(df["ens"], df["count"]):
            if not isinstance(e, str):
                continue
            gid = e.split(".")[0]
            counts[gid] = counts.get(gid, 0.0) + (0.0 if pd.isna(c) else float(c))
        series[label + "_" + gsm] = pd.Series(counts)
        meta[label + "_" + gsm] = {"gsm": gsm, "agent": agent, "group": grp,
                                   "fname": fn}
    return pd.DataFrame(series), pd.DataFrame(meta).T


def load_symbol_map():
    """ENSMUSG -> mouse symbol.

    Built from the Stage A supplementary tables, which are Mus musculus and
    already carry a `gene_id` -> `gene` pair. We union all eight contrasts to
    maximise coverage of the background. Cached to disk because parsing eight
    xlsx files is slow and the mapping is fixed.
    """
    import openpyxl

    cache = os.path.join(OUT_DIR, "mus_symbol_map.json")
    # A previous run cached an EMPTY map (it looked for a mouse GTF that was
    # never downloaded); refuse to reuse a degenerate cache.
    if os.path.isfile(cache) and os.path.getsize(cache) > 100:
        loaded = json.load(open(cache, encoding="utf-8"))
        if len(loaded) > 1000:
            return loaded

    m = {}
    for fn in sorted(os.listdir(RAW_DIR)):
        if not (fn.startswith("GSE111216") and fn.endswith(".xlsx")):
            continue
        wb = openpyxl.load_workbook(os.path.join(RAW_DIR, fn),
                                    read_only=True, data_only=True)
        ws = wb[wb.sheetnames[0]]
        rows = ws.iter_rows(values_only=True)
        header = [str(c).strip() if c is not None else "" for c in next(rows)]
        if "gene_id" not in header or "gene" not in header:
            wb.close()
            continue
        gi, gs = header.index("gene_id"), header.index("gene")
        for r in rows:
            if r is None or r[gi] is None or r[gs] is None:
                continue
            m.setdefault(str(r[gi]).split(".")[0], str(r[gs]).strip())
        wb.close()

    if len(m) < 1000:
        sys.exit(f"symbol map degenerate: only {len(m)} entries")
    json.dump(m, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
    return m


def main():
    cmat, meta = build_counts()
    lib = cmat.sum(axis=0)
    cpm = cmat / lib * 1e6
    lg = np.log2(cpm + 1)

    smap = load_symbol_map()
    sym = [smap.get(g, None) for g in lg.index]
    lg = lg.copy()
    lg.index = sym
    lg = lg[lg.index.notnull()]
    lg = lg[~lg.index.duplicated(keep="first")]

    def panel(genes):
        present = [g for g in genes if g in lg.index]
        return lg.loc[present], present

    res = {"per_sample": {}, "panels": {}}
    for label in lg.columns:
        mm = meta.loc[label]
        my, py = panel(MYELIN)
        sn, ps = panel(SENSORY)
        cn, pc = panel(CNS_NEURON)
        gl, pg = panel(GLIA)
        st, pst = panel(SATELLITE)
        res["per_sample"][label] = {
            "gsm": mm["gsm"], "agent": mm["agent"], "group": mm["group"],
            "myelin_score": float(my[label].mean()),
            "sensory_score": float(sn[label].mean()),
            "cns_neuron_score": float(cn[label].mean()),
            "astroglia_score": float(gl[label].mean()),
            "satellite_score": float(st[label].mean()),
        }
    res["panels"] = {
        "myelin": py, "sensory": ps, "cns_neuron": pc,
        "astroglia": pg, "satellite": pst,
    }
    res["markers_present"] = {g: (g in lg.index) for g in MYELIN + SENSORY + CNS_NEURON + GLIA + SATELLITE}

    df = pd.DataFrame(res["per_sample"]).T
    print("=" * 78)
    print("AUDIT R10 - tissue identity of GSE261676 (spinal cord vs DRG)")
    print("=" * 78)
    print("\nMarker panel present in matrix:")
    print("  myelin (oligodendrocyte):", ", ".join(py) or "NONE")
    print("  sensory neuron (periph):", ", ".join(ps) or "NONE")
    print("  CNS neuron:", ", ".join(pc) or "NONE")
    print("  astroglia:", ", ".join(pg) or "NONE")
    print("  satellite glia:", ", ".join(pst) or "NONE")
    print("\nPer-sample scores (mean log2 CPM):")
    print(df[["myelin_score", "sensory_score", "cns_neuron_score",
              "astroglia_score", "satellite_score"]].round(3).to_string())

    gap = float(df["sensory_score"].mean() - df["myelin_score"].mean())
    print(f"\n  mean sensory - mean myelin = {gap:+.3f}")
    if gap > 2.0:
        verdict = ("DRG-like: sensory-neuron markers dominate while CNS myelin "
                   "markers are near background -> paper label supported, GEO "
                   "source_name appears to be a deposition error.")
    elif gap < -2.0:
        verdict = ("SPINAL-CORD-like: CNS myelin markers dominate -> GEO label "
                   "supported; Stage B must be relabelled.")
    else:
        verdict = "INCONCLUSIVE: markers do not separate the two tissues."
    res["verdict"] = verdict
    res["sensory_minus_myelin"] = gap
    print(f"  VERDICT: {verdict}")

    with open(os.path.join(OUT_DIR, "audit_tissue_identity.json"), "w",
              encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    print(f"\nwrote {OUT_DIR}/audit_tissue_identity.json")


if __name__ == "__main__":
    main()
