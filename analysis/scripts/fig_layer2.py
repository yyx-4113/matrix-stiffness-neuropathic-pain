#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figures for the stiffness x neuropathic-pain reanalysis.

Fig 1  per-animal HD_down scores (both treatment arms)
Fig 2  per-member contributions (leave-one-gene-out difference)
Fig 3  Layer-0 signature derivation (WT vs YAP/TAZ-dKO stiffness response)
Fig 4  observed separation against the size- and expression-matched null
"""

import itertools
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
L0 = os.path.join(ROOT, "analysis", "results", "layer0")
L1 = os.path.join(ROOT, "analysis", "results", "layer1")
L2 = os.path.join(ROOT, "analysis", "results", "layer2")
FIG = os.path.join(L2, "fig")
os.makedirs(FIG, exist_ok=True)
sys.path.insert(0, HERE)
from layer1_projection import human_to_mouse  # noqa: E402
from layer2_sample_scores import build_counts, load_symbol_map  # noqa: E402

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 10, "axes.titlesize": 10,
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight",
    "font.family": "DejaVu Sans",
})

ARM_COLORS = {"sham": "#4C72B0", "SNI": "#C44E52"}


def fig1():
    sc = pd.read_csv(os.path.join(L2, "layer2_sample_scores.csv"))
    hd = sc[sc.signature == "hippo_dependent_down"]
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    xmap = {"saline": 0, "DMI": 1}
    for agent, adf in hd.groupby("agent"):
        for i, grp in enumerate(["sham", "SNI"]):
            vals = adf[adf.group == grp]["score"].to_numpy()
            x = xmap[agent] * 2 + i
            xs = np.full(len(vals), x) + np.linspace(-0.06, 0.06, len(vals))
            ax.scatter(xs, vals, color=ARM_COLORS[grp], s=46, zorder=3,
                       edgecolor="white", linewidth=0.6,
                       label=f"{grp}" if agent == "saline" else None)
            ax.hlines(np.mean(vals), x - 0.22, x + 0.22, color=ARM_COLORS[grp], lw=1.8, zorder=4)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["sham\nsaline", "SNI\nsaline", "sham\nDMI", "SNI\nDMI"])
    ax.axhline(0, color="gray", lw=0.7, ls=":")
    ax.set_ylabel("HD_down module score (z)")
    ax.set_title("Fig 1  Stiffness-down Hippo-dependent module score, per animal")
    ax.legend(frameon=False, title="group", fontsize=8, title_fontsize=8, loc="upper left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    p = os.path.join(FIG, "fig1_per_animal_scores.png")
    fig.savefig(p)
    plt.close(fig)
    return p


def fig2():
    lg, meta = build_data_cached()
    z = lg.sub(lg.mean(axis=1), axis=0).div(lg.std(axis=1, ddof=1), axis=0)
    sig = json.load(open(os.path.join(L0, "layer0_signature.json"), encoding="utf-8"))
    members = [human_to_mouse(g) for g in sig["sets"]["hippo_dependent_down"]]
    present = [m for m in members if m in z.index]
    sal_sni = [s for s in z.columns if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "SNI"]
    sal_sham = [s for s in z.columns if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "sham"]
    per = pd.Series({g: float(z.loc[g, sal_sni].mean() - z.loc[g, sal_sham].mean()) for g in present})
    per = per.sort_values()

    fig, ax = plt.subplots(figsize=(5.2, 5.6))
    colors = ["#4C72B0" if v < 0 else "#C44E52" for v in per.values]
    ax.barh(np.arange(len(per)), per.values, color=colors, height=0.75)
    ax.set_yticks(np.arange(len(per)))
    ax.set_yticklabels(per.index, fontsize=7.5)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("mean z difference (SNI - sham), saline arm")
    ax.set_title("Fig 2  Per-member contribution to the HD_down signal")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    p = os.path.join(FIG, "fig2_member_contributions.png")
    fig.savefig(p)
    plt.close(fig)
    return p


def fig3():
    t = pd.read_csv(os.path.join(L0, "layer0_gene_level.csv"), index_col=0)
    sel = t[t.hippo_class == "hippo_dependent"]
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.scatter(sel["delta_WT"], sel["delta_YTKO"], s=18, color="#404040", alpha=0.7)
    lims = [-3.2, 3.2]
    ax.plot(lims, [0, 0], color="gray", lw=0.7)
    ax.plot([0, 0], lims, color="gray", lw=0.7)
    # shaded "dependent" cone: |delta_YT| <= 0.5 |delta_WT|
    xs = np.linspace(-3.2, 3.2, 100)
    ax.fill_between(xs, 0.5 * xs, -0.5 * xs, color="#C44E52", alpha=0.10, lw=0)
    for g in ["CTGF", "CYR61", "ANKRD1", "AMOTL2"]:
        if g in sel.index:
            ax.annotate(g, (sel.loc[g, "delta_WT"], sel.loc[g, "delta_YTKO"]),
                        fontsize=7.5, xytext=(3, 3), textcoords="offset points")
    ax.set_xlim(lims); ax.set_ylim(lims)
    ax.set_xlabel("stiffness response in WT, log2FC (40 kPa - 1 kPa)")
    ax.set_ylabel("same response in YAP/TAZ-dKO")
    ax.set_title("Fig 3  Signature derivation: Hippo-dependent members\n(shaded cone = |response| retains <= 50%)")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    p = os.path.join(FIG, "fig3_signature_derivation.png")
    fig.savefig(p)
    plt.close(fig)
    return p


def fig4():
    lg, meta = build_data_cached()
    z = lg.sub(lg.mean(axis=1), axis=0).div(lg.std(axis=1, ddof=1), axis=0)
    sig = json.load(open(os.path.join(L0, "layer0_signature.json"), encoding="utf-8"))
    members = [human_to_mouse(g) for g in sig["sets"]["hippo_dependent_down"]]
    present = [m for m in members if m in z.index]
    sal_sni = [s for s in z.columns if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "SNI"]
    sal_sham = [s for s in z.columns if meta.loc[s, "agent"] == "saline" and meta.loc[s, "group"] == "sham"]
    score = z.loc[present].mean(axis=0)
    obs = abs(score[sal_sni].mean() - score[sal_sham].mean())

    rng = np.random.default_rng(20261021)
    mean_expr = z.mean(axis=1)
    edges = np.array_split(np.argsort(mean_expr.to_numpy(), kind="mergesort"), 10)
    pool_by_bin = [mean_expr.index[e] for e in edges]
    member_bins = []
    for g in present:
        for b, pool in enumerate(pool_by_bin):
            if g in pool:
                member_bins.append(b)
                break
    null = []
    for _ in range(4000):
        draws = [pool_by_bin[b][rng.integers(0, len(pool_by_bin[b]))] for b in member_bins]
        sc = z.loc[draws].mean(axis=0)
        null.append(abs(sc[sal_sni].mean() - sc[sal_sham].mean()))
    null = np.array(null)

    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    ax.hist(null, bins=45, color="#B0B0B0", edgecolor="white", lw=0.4)
    ax.axvline(obs, color="#C44E52", lw=1.8, label=f"observed HD_down (|diff| = {obs:.3f})")
    pval = (int((null >= obs).sum()) + 1) / (len(null) + 1)
    ax.set_xlabel("|mean score difference, SNI - sham| (saline arm)")
    ax.set_ylabel("matched random gene sets")
    ax.set_title(f"Fig 4  Size- and expression-matched null\nempirical p = {pval:.3f}")
    ax.legend(frameon=False, fontsize=8)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    p = os.path.join(FIG, "fig4_matched_null.png")
    fig.savefig(p)
    plt.close(fig)
    return p


_CACHE = {}


def build_data_cached():
    if "data" not in _CACHE:
        cmat, meta = build_counts()
        lib = cmat.sum(axis=0)
        cpm = cmat / lib * 1e6
        keep = (cpm > 1).sum(axis=1) >= 4
        lg = np.log2(cpm[keep] + 1)
        smap = load_symbol_map()
        lg.index = [smap.get(g, None) for g in lg.index]
        lg = lg[lg.index.notnull()]
        lg = lg[~lg.index.duplicated(keep="first")]
        _CACHE["data"] = (lg, meta)
    return _CACHE["data"]


def fig5():
    """Effect-size comparison: positive control vs stiffness signatures.

    This is the pivotal figure. A pipeline that returns only nulls is
    uninterpretable on its own; placing a known-true positive control on the
    SAME axis shows the apparatus does detect real effects, so the stiffness
    nulls reflect absence of signal rather than absence of sensitivity.
    """
    pc = json.load(open(os.path.join(L2, "layer2_positive_control.json"), encoding="utf-8"))
    res = pc["results"]

    labels = {
        "POSITIVE_CONTROL_injury_up": "Positive control\n(nerve-injury genes)",
        "stiffness_HD_up": "Stiffness HD_up\n(B-primary)",
        "stiffness_HD_down": "Stiffness HD_down\n(B-secondary)",
        "stiffness_HI_down": "Stiffness HI_down\n(exploratory)",
    }
    keys = [k for k in labels if k in res and "error" not in res[k]]
    g = [abs(res[k]["hedges_g"]) for k in keys]
    p = [res[k]["p_exact_permutation"] for k in keys]
    n = [res[k]["n_present_after_filter"] for k in keys]

    colors = ["#2F7D5B" if k.startswith("POSITIVE") else "#8C8C8C" for k in keys]

    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    ypos = np.arange(len(keys))[::-1]
    bars = ax.barh(ypos, g, color=colors, height=0.62)
    ax.set_yticks(ypos)
    ax.set_yticklabels([labels[k] for k in keys], fontsize=8)
    for y, gi, pi, ni in zip(ypos, g, p, n):
        ax.text(gi + 0.08, y, f"g={gi:.2f}, p={pi:.3f}, n={ni}",
                va="center", fontsize=7.5, color="#303030")
    ax.set_xlim(0, max(g) * 1.45)
    ax.set_xlabel("|effect size| (Hedges g), saline arm SNI vs sham")
    ax.set_title("Fig 5  Pipeline sensitivity: positive control vs stiffness signatures")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    p = os.path.join(FIG, "fig5_positive_control_vs_signatures.png")
    fig.savefig(p)
    plt.close(fig)
    return p


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5):
        print("wrote", f())
