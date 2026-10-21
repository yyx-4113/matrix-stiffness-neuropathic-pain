#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig 6  Layer-3 generality benchmark (specificity index, SI_g)
Fig S1 Layer-3b sample-level effect-size comparison (7 gene sets)

Both panels share the manuscript figure convention set in fig_layer2.py.
SI_g < 1  => the gene set shifts at least as far in blood as in DRG
            => tissue-specificity FAILS (red).
SI_g >= 1 => tissue-specific (blue).
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
L3 = os.path.join(ROOT, "analysis", "results", "layer3")
L3B = os.path.join(ROOT, "analysis", "results", "layer3")
FIG = os.path.join(L3, "fig")
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 10, "axes.titlesize": 10,
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight",
    "font.family": "DejaVu Sans",
})


def short(name):
    return {
        "G1_core_matrisome": "G1 core matrisome",
        "G2_yap_taz_canonical_targets": "G2 YAP/TAZ targets",
        "G3_mechanosensing_adhesome": "G3 mechanosensing",
        "G4_actin_rho_rock": "G4 actin/Rho-ROCK",
        "G5_ecm_remodelling_fibrosis": "G5 ECM remodelling",
    }[name]


def fig6():
    d = json.load(open(os.path.join(L3, "layer3_generality.json"), encoding="utf-8"))
    ps = d["per_set_specificity"]
    order = ["G1_core_matrisome", "G2_yap_taz_canonical_targets",
             "G3_mechanosensing_adhesome", "G4_actin_rho_rock",
             "G5_ecm_remodelling_fibrosis"]
    labels = [short(k) for k in order]
    si = [ps[k]["SI"] for k in order]
    fail = [ps[k]["specificity_failed"] for k in order]

    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ypos = np.arange(len(order))[::-1]
    colors = ["#C44E52" if f else "#4C72B0" for f in fail]
    ax.barh(ypos, si, color=colors, height=0.62)
    ax.set_xscale("log")
    ax.axvline(1.0, color="black", lw=1.0, ls="--", label="SI = 1 (no specificity)")
    ax.set_yticks(ypos)
    ax.set_yticklabels(labels, fontsize=8)
    for y, v, f in zip(ypos, si, fail):
        tag = "FAIL" if f else "PASS"
        ax.text(v * 1.18, y, f"{v:.1f} ({tag})",
                va="center", ha="left", fontsize=7.5, color="#303030")
    ax.set_xlim(0.25, 700)
    ax.set_xlabel("Specificity index  SI_g = |MRU(DRG,SNI) - 0.5| / |MRU(blood,SNI) - 0.5|")
    ax.set_title("Fig 6  Tissue specificity of five independent ECM / mechano gene sets\n"
                 "(red = shifts at least as far in blood as in DRG)")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    p = os.path.join(FIG, "fig6_generality.png")
    fig.savefig(p)
    plt.close(fig)
    return p


def figs1():
    d = json.load(open(os.path.join(L3B, "layer3b_sample_generality.json"), encoding="utf-8"))
    rows = d["table"]
    order = ["POSITIVE_CONTROL_injury", "HD_up", "G1_core_matrisome",
             "G2_yap_taz_canonical_targets", "G3_mechanosensing_adhesome",
             "G4_actin_rho_rock", "G5_ecm_remodelling_fibrosis"]
    lbl = {
        "POSITIVE_CONTROL_injury": "Positive control\n(nerve-injury genes)",
        "HD_up": "Stiffness HD_up",
        "G1_core_matrisome": "G1 core matrisome",
        "G2_yap_taz_canonical_targets": "G2 YAP/TAZ targets",
        "G3_mechanosensing_adhesome": "G3 mechanosensing",
        "G4_actin_rho_rock": "G4 actin/Rho-ROCK",
        "G5_ecm_remodelling_fibrosis": "G5 ECM remodelling",
    }
    rows = [r for r in rows if r["gene_set"] in order]
    rows.sort(key=lambda r: order.index(r["gene_set"]))
    g = [abs(r["hedges_g_saline_arm"]) for r in rows]
    p = [r["p_exact_saline_arm"] for r in rows]
    keys = [r["gene_set"] for r in rows]

    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    ypos = np.arange(len(keys))[::-1]
    colors = ["#2F7D5B" if k == "POSITIVE_CONTROL_injury" else "#8C8C8C" for k in keys]
    ax.barh(ypos, g, color=colors, height=0.62)
    ax.set_yticks(ypos)
    ax.set_yticklabels([lbl[k] for k in keys], fontsize=8)
    for y, gi, pi in zip(ypos, g, p):
        ax.text(gi + 0.08, y, f"g={gi:.2f}, p={pi:.3f}",
                va="center", fontsize=7.5, color="#303030")
    ax.set_xlim(0, max(g) * 1.5)
    ax.set_xlabel("|effect size| (Hedges g), saline-arm SNI vs sham (GSE261676, 4 vs 4)")
    ax.set_title("Fig S1  Layer-3b sample-level effect sizes (gene-set scores)")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    pth = os.path.join(FIG, "figS1_layer3b_effects.png")
    fig.savefig(pth)
    plt.close(fig)
    return pth


if __name__ == "__main__":
    print("wrote", fig6())
    print("wrote", figs1())
