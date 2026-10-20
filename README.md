# Matrix stiffness × neuropathic pain — prospectively specified reanalysis

Reproducibility package for: *Mechanobiology signatures do not transfer across cell types or expression strata: a prospectively specified cross-model reanalysis of stiffness-controlled programmes projected onto neuropathic-pain transcriptomes* (Yongxin Yang, ORCID 0009-0004-9698-6552).

Protocol v0.4 and the frozen panel (`ms-proto-frozen-2026-10-21`) were committed before any pain-side expression data were examined. Stage B (GSE261676) was added by explicit amendment v0.3 **before its expression data were read**, and Stage A is reported in full regardless of the Stage B outcome. v0.4 is an audit-driven correction; every change and its motivation are in the protocol changelog.

## Headline result, stated honestly

| Layer | Question | Result |
|---|---|---|
| Layer 0 (GSE98547) | Which genes does matrix stiffness itself drive, and which need YAP/TAZ? | 18 Hippo-dependent up / 41 down. **Positive control passed**: CTGF Δ = +1.64 (P = 9.5e-6), CYR61 +0.99, ANKRD1 +1.43, AMOTL2 +1.38 |
| Stage A (GSE111216) | Is that programme activated in DRG / spinal cord / brain / blood in CFA or SNI? | **The test is uninformative, not merely negative.** Primary endpoint under the expression-matched null P = 0.102, q = 0.409; **the blood negative control is far more significant (P = 0.0009, q = 0.007)**. Per protocol §5.3 the conclusion cannot stand when a negative control matches or exceeds the target |
| Stage B (GSE261676) | Same question, sample level, mouse DRG, 4 vs 4 | HD_up **null with a negligible effect size** (g = +0.25, P = 0.80). HD_down shifts **upward** (diff = +0.397, exact P = 0.0286 = the 1/35 floor, g = +3.06) — transcriptome moves **against** the stiff-matrix direction |
| **Sensitivity (§10)** | **Can this pipeline detect a real effect at all?** | **YES.** Pre-specified nerve-injury gene set: diff = +1.285, P = 0.0286, **g = +4.43**, complete separation |

**Why the sensitivity check changes the interpretation.** A pipeline that returns only nulls cannot distinguish "no signal" from "cannot see signal". With the positive control at g = 4.43 and HD_up at g = 0.25 — a 17.6-fold gap, both measured on the identical scoring machinery — the HD_up null becomes a *bounded, interpretable* negative finding rather than an inconclusive one.

**What the HD_down signal is and is not.** Directionally robust (leave-one-animal-out, four scoring operators, no single-gene dominance) but **does not survive** BH correction across the 4-module family (q = 0.086) or the size- and expression-matched null (P = 0.092), and is **not reversed by desipramine** (P = 0.83). Reported as a bounded, hypothesis-generating observation — not a confirmation.

## What this project actually contributes

The value is methodological, and it does not depend on any positive finding:

1. **A stiffness-controlled experiment yields a biologically anchored, mechanistically stratified signature** (Layer 0 passes its positive control).
2. **Projecting that signature onto pain transcriptomes produces systematic false positives.** 40–58% of loci have zero baseline expression; signature genes were selected under an FPKM > 1 filter, so their baseline stratum differs from background (KS D ≈ 0.49, P < 1e-5). An unmatched null returns "significant" enrichment in **every** tissue, including blood.
3. **Cross-cell-type transfer collapses coverage.** 7 of 18 HD_up members (`Ankrd1, Ap1m2, Gprc5a, Hist1h4d, Krt18, Krt8, Vipr1`) are simply not expressed in DRG — the epithelial mechanoresponse is not the neuronal one.
4. Therefore the frequently reported "ECM organisation enrichment" in pain transcriptomics lacks demonstrated tissue specificity, and projection-style analyses need an expression-matched null, a coverage audit, and a positive control.

## File map

```
PROTOCOL_基质刚度与神经病理性痛.md   # protocol v0.4 + full changelog + §10 positive control
analysis/
  config/ms_panel.json               # FROZEN panel, tag ms-proto-frozen-2026-10-21
  MANIFEST.json                      # SHA-256 of artifacts + raw inputs
  scripts/
    layer0_stiffness_signature.py     # signature export + Hippo stratification (GSE98547)
    layer1_projection.py              # rank projection onto 8 pain contrasts (GSE111216)
    layer1_diag.py                    # baseline-expression confound audit + stratified null
    layer2_sample_scores.py           # per-animal module scores (GSE261676)
    layer2_positive_control.py        # §10 pipeline-sensitivity check
    layer2_robustness.py              # LOO, alternative operators, matched null, Mann-Whitney
    audit_round1.py                   # independent audit: mapping, biotype, rank basis, sampling
    audit_round1b.py                  # separates homology mapping from post-filter coverage
    fig_layer2.py                     # Figs 1-5
    gen_manifest.py                   # refresh MANIFEST.json (run last)
    gate_consistency.py               # 28 assertions incl. 4 independent recomputations
  data/raw/_download.sh               # verified GEO/GENCODE URLs
  results/
    layer0/  layer1/  layer2/  audit/ # JSON + CSV + fig/
```

## Reproduce

```bash
bash analysis/data/raw/_download.sh                 # GEO + GENCODE inputs
python analysis/scripts/layer0_stiffness_signature.py
python analysis/scripts/layer1_projection.py
python analysis/scripts/layer1_diag.py
python analysis/scripts/layer2_sample_scores.py
python analysis/scripts/layer2_positive_control.py
python analysis/scripts/layer2_robustness.py
python analysis/scripts/fig_layer2.py
python analysis/scripts/gate_consistency.py         # must exit 0
python analysis/scripts/audit_round1.py             # independent defect audit
python analysis/scripts/audit_round1b.py            # mapping vs coverage
python analysis/scripts/audit_round3.py             # claim-to-artifact traceability
python analysis/scripts/gen_manifest.py             # run last
```

Software: Python 3.13.14, NumPy 2.4.6, pandas 2.3.3, SciPy 1.18.1, Matplotlib 3.11.1, openpyxl 3.1.5.

## Caveats

1. **Signature source is HEK293A, not a sensory neuron.** The signature is a cross-cell-type "core mechanotransduction programme"; the DRG coverage shortfall (11/18 = 0.61) is a direct measurement of how imperfect that transfer is.
2. **GSE111216 deposits no sample-level matrix.** Stage A is a rank projection on published per-contrast statistics; it cannot estimate within-sample correlation or per-animal variance.
3. **The baseline-expression confound is severe.** It is documented in `layer1_diag.json` and is the reason Stage A is reported as uninformative rather than negative. The unstratified null must never be quoted as a finding.
4. **Stage B is 4 vs 4.** The minimum attainable two-sided exact P is 1/35 ≈ 0.029; every "significant" result sits exactly at that floor and cannot be distinguished from it.
5. **Drug arm is exploratory.** Desipramine does not shift the HD_down score within SNI (diff = +0.015, P = 0.83); it does move HI_down (P = 0.029), which is reported as exploratory only.
6. **`mapping_rate` and `coverage_rate` are different quantities** (protocol §4.3). Homology mapping of HD_up is 18/18 = 1.000 and clears the 0.7 governance floor; the 0.611 figure is coverage, a power limitation, and must not be quoted as a mapping failure.
7. **Four protocol versions are disclosed** (v0.1 → v0.2 → v0.3 → v0.4), with motivation and timing for each. The v0.4 changes were driven by an implementation audit, not by any result.

## Data availability

GSE98547, GSE111216 and GSE261676 are public on GEO; GENCODE v24lift37 annotation from EBI. All derived statistics are deposited here and hashed in `analysis/MANIFEST.json`.
