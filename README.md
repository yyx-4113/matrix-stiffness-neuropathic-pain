# Matrix stiffness × neuropathic pain — prospectively specified reanalysis

Reproducibility package for: *A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity* (Yongxin Yang, ORCID 0009-0004-9698-6552).

The protocol and the frozen analysis panel were committed before any pain-side expression data were examined. Every change and its motivation are recorded in the protocol changelog (v0.1 → v0.7). This package is the v1.0.0 release: the analysis, figures, and manuscript are internally consistent and every numeric claim is traceable to a file under `analysis/results/` (see `analysis/MANIFEST.json`).

## Headline result, stated honestly

| Layer | Question | Result |
|---|---|---|
| Layer 0 (GSE98547) | Which genes does matrix stiffness itself drive, and which need YAP/TAZ? | 18 Hippo-dependent up / 41 down. Biologically anchored: CTGF Δ = +1.64 (P = 9.5 × 10⁻⁶); LATS confirmation HD 0.797 / HI 0.286. |
| Stage A (GSE111216) | Is that programme activated in DRG / SC / BRN / BLD in CFA or SNI? | **Uninformative, not merely negative.** Under the expression-matched null: DRG×SNI HD_up MRU = 0.717, P = 0.102, BH q = 0.409; the **blood negative control is equally non-significant** (MRU = 0.696, P = 0.100, q = 0.409 = DRG). Per §5.3, because the control matches the target, no tissue-specific attribution can be made. (The unstratified null gives a spurious blood signal, P = 0.0009 — a baseline-expression confound, explicitly *not* a finding.) |
| Stage B (GSE261676) | Same question, sample level, mouse DRG, 4 vs 4 | HD_up **bounded null** (difference = +0.146, P = 0.80, Hedges g = 0.219). HD_down shifts **upward** (difference = +0.397, P = 0.0286, g = 2.658, BH q = 0.086) — reported as hypothesis-generating only. |
| Sensitivity (§10) | Can this pipeline detect a real effect at all? | **YES.** Pre-specified nerve-injury gene set: difference = +1.285, P = 0.0286, **Hedges g = 3.85**, complete separation. |
| Layer 3 (GSE111216) | Do established ECM / mechano sets retain tissue specificity? | **Yes — 4/5 do.** G1 SI = 38.4, G3 1.44, G4 240.5, G5 9.06 retain DRG-over-blood specificity; only G2 (YAP/TAZ canonical) fails (SI = 0.44). The pre-specified rule (≥ 4/5 fail) was **not** met, so specificity failure is **not universal** — it is signature- and cell-type-specific. |
| Layer 3b / 4 (GSE261676) | Sample-level divergence / descriptive characterisation | Underpowered: 0/5 ECM sets significantly upregulated (Hedges g 0.31–1.13); of 15 345 genes, 8 significant-up, ECM-union 0. No usable descriptive landscape. |

**Why the sensitivity check matters.** A pipeline that returns only nulls cannot distinguish "no signal" from "cannot see signal". With the positive control at g = 3.85 and HD_up at g = 0.219 — a 17.6-fold gap on identical scoring — the HD_up null is *bounded and interpretable*, not an inconclusive method artifact.

**What the HD_down signal is and is not.** Directionally robust under leave-one-animal-out and a Q4 expression-matched null (P = 0.092), but it does not survive BH correction across the 4-module family (q = 0.086). Reported as a bounded, hypothesis-generating observation — not a confirmation.

## What this project actually contributes

The value is both methodological and substantive, and it does not depend on a universal positive finding:

1. **A stiffness-controlled experiment yields a biologically anchored, mechanistically stratified signature** (Layer 0; positive control passed).
2. **Projecting that signature onto pain transcriptomes yields a bounded, sensitivity-validated null** — but this null is *signature- and cell-type-specific*, not evidence that projection statistics inherently fail. HEK293A epithelium is not a sensory neuron/glia, and the mechanical input (culture-substrate fibronectin stiffness) differs from in-vivo nerve compression / perineural fibrosis.
3. **Once baseline-expression confounding is controlled, established ECM / mechanotransduction gene sets retain tissue specificity in pain transcriptomes** (4/5 DRG > blood). This *refutes* the hypothesis that projection statistics are universally uninformative for pain-ECM biology and means the literature's "ECM enrichment in pain" findings are **not** invalidated by our result — our null merely circumscribes them to the source cell type of the projected signature.
4. **Methodological safeguards**: an expression-matched null, a coverage audit, and a positive-control sensitivity test are required to avoid the false-positive and false-negative traps this project documents.

## File map

```
PROTOCOL_基质刚度与神经病理性痛.md   # protocol v0.7 + full changelog
analysis/
  config/ms_panel.json               # frozen analysis panel
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
    fig_layer3.py                     # Fig 6 + Fig S1
    gen_manifest.py                   # refresh MANIFEST.json (run last)
    gate_consistency.py               # 39 assertions incl. 4 independent recomputations
  data/raw/_download.sh               # verified GEO/GENCODE URLs
  results/
    layer0/  layer1/  layer2/  layer3/  layer3b/  layer4/  audit/  # JSON + CSV + fig/
manuscript/
  manuscript.md                       # GigaScience Research Article (Vancouver, de-AI polished)
  review/                             # independent 4-panel review (Round 1 + Round 2)
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
python analysis/scripts/fig_layer3.py
python analysis/scripts/gate_consistency.py         # must exit 0 (39/39)
python analysis/scripts/audit_round1.py             # independent defect audit
python analysis/scripts/audit_round1b.py            # mapping vs coverage
python analysis/scripts/audit_round3.py            # claim-to-artifact traceability
python analysis/scripts/gen_manifest.py             # run last
```

Software: Python 3.13.14, NumPy 2.4.6, pandas 2.3.3, SciPy 1.18.1, Matplotlib 3.11.1, openpyxl 3.1.5.

## Caveats

1. **Signature source is HEK293A, not a sensory neuron.** The signature is a cross-cell-type "core mechanotransduction programme"; the DRG coverage shortfall (11/18 = 0.61) is a direct measurement of how imperfect that transfer is.
2. **GSE111216 deposits no sample-level matrix.** Stage A is a rank projection on published per-contrast statistics; it cannot estimate within-sample correlation or per-animal variance.
3. **The baseline-expression confound is severe.** It is documented in `layer1_diag.json` and is the reason Stage A is reported as uninformative rather than negative. The unstratified null must never be quoted as a finding.
4. **Stage B is 4 vs 4.** The minimum attainable two-sided exact P is 2/70 ≈ 0.029; the positive-control and HD_down signals sit exactly at that floor.
5. **Layer 3 does not show a universal failure.** Only the HEK293A-derived HD_up signature fails to transfer; 4/5 established ECM/mechano sets retain DRG-over-blood specificity. The pre-specified "universal failure" primary rule (≥ 4/5 fail) was not met.
6. **`mapping_rate` and `coverage_rate` are different quantities** (protocol §4.3). Homology mapping of HD_up is 18/18 = 1.000 and clears the 0.7 governance floor; the 0.611 figure is coverage, a power limitation, and must not be quoted as a mapping failure.
7. **Layer 3b and Layer 4 are underpowered** (4 vs 4; 8/15 345 detectable) and their non-findings are reported as such, not as evidence of absence.
8. **HD_down and the post-hoc ECM / YAP–TAZ separation are hypothesis-generating only** and require independent validation.

## Data availability

GSE98547, GSE111216 and GSE261676 are public on GEO; GENCODE v24lift37 annotation from EBI. All derived statistics are deposited at https://github.com/yyx-4113/matrix-stiffness-neuropathic-pain (tag `v1.0.0`) and hashed in `analysis/MANIFEST.json`; every numeric claim in the manuscript is traceable to a file under `analysis/results/`.
