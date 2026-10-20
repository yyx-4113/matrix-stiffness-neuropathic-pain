# Matrix stiffness × neuropathic pain — prospectively specified reanalysis

Reproducibility package for: *The stiffness–Hippo transcriptional programme is not activated in the injured dorsal root ganglion: a prospectively specified reanalysis with an expression-matched null* (Yongxin Yang, ORCID 0009-0004-9698-6552).

Protocol v0.3 and the frozen panel (`ms-proto-frozen-2026-10-21`) were committed before any pain-side expression data were examined. Stage B (GSE261676) was added by explicit protocol amendment v0.3 **before its expression data were read**, and Stage A is reported in full regardless of the Stage B outcome.

## Headline result, stated honestly

| Layer | Question | Result |
|---|---|---|
| Layer 0 (GSE98547) | Which genes does matrix stiffness itself drive, and which need YAP/TAZ? | 18 Hippo-dependent up / 41 down; positive control passed (CTGF Δ = +1.64, P = 9.5e-6) |
| Stage A (GSE111216) | Is that programme activated in DRG / spinal cord / brain / blood in CFA or SNI? | **No.** Primary endpoint P = 0.106, q = 0.446 after expression-matched null; **no** module survived BH (min q = 0.066) |
| Stage B (GSE261676) | Same question, sample level, mouse DRG, 4 vs 4 | HD_up **null** (P = 0.80). HD_down shifts **upward** (diff = +0.397, exact P = 0.0286 = the 1/35 floor, Welch P = 0.011), i.e. the transcriptome moves **against** the stiff-matrix direction |

The Stage B HD_down effect is directionally robust (leave-one-animal-out, four scoring operators, no single-gene dominance) but **does not survive** either BH correction across the 4-module family (q = 0.086) or the size- and expression-matched null (P = 0.095). It is reported as a bounded, hypothesis-generating observation — not as a positive confirmation.

## File map

```
PROTOCOL_基质刚度与神经病理性痛.md   # prospective protocol v0.3 + full changelog + Stage A report
analysis/
  config/ms_panel.json               # FROZEN panel, tag ms-proto-frozen-2026-10-21
  MANIFEST.json                      # SHA-256 of 25 artifacts + 42 raw inputs
  scripts/
    layer0_stiffness_signature.py     # signature export + Hippo stratification (GSE98547)
    layer1_projection.py              # rank projection onto 8 pain contrasts (GSE111216)
    layer1_diag.py                    # baseline-expression confound audit + stratified null
    layer2_sample_scores.py           # per-animal module scores (GSE261676)
    layer2_robustness.py              # LOO, alternative operators, matched null, Mann-Whitney
    fig_layer2.py                     # Figs 1-4
    gen_manifest.py                   # refresh MANIFEST.json (run last)
    gate_consistency.py               # 23 assertions; must print "ALL ASSERTIONS PASS"
  data/raw/_download.sh               # verified GEO/GENCODE URLs
  results/
    layer0/  layer1/  layer2/         # JSON + CSV + fig/
```

## Reproduce

```bash
bash analysis/data/raw/_download.sh                 # GEO + GENCODE inputs
python analysis/scripts/layer0_stiffness_signature.py
python analysis/scripts/layer1_projection.py
python analysis/scripts/layer1_diag.py
python analysis/scripts/layer2_sample_scores.py
python analysis/scripts/layer2_robustness.py
python analysis/scripts/fig_layer2.py
python analysis/scripts/gate_consistency.py         # must exit 0
python analysis/scripts/gen_manifest.py             # run last
```

Software: Python 3.13.14, NumPy 2.4.6, pandas 2.3.3, SciPy 1.18.1, Matplotlib 3.11.1, openpyxl 3.1.5.

## Caveats

1. **Signature source is HEK293A, not a sensory neuron.** The signature is a cross-cell-type "core mechanotransduction programme", not a neuron-specific one.
2. **GSE111216 deposits no sample-level matrix.** Stage A is therefore a rank projection on published per-contrast statistics; it cannot estimate within-sample correlation or per-animal variance.
3. **The baseline-expression confound is severe and had to be modelled.** 40–58% of loci have zero baseline expression; signature genes were selected under an FPKM > 1 filter, so their baseline distribution differs from background (KS D ≈ 0.49, P < 1e-5). The unstratified null produces spurious "significance" in every tissue including blood — this is documented in `layer1_diag.json` and must not be quoted as a finding.
4. **Stage B is 4 vs 4.** The minimum attainable two-sided exact P is 1/35 ≈ 0.029; the HD_down result sits exactly at that floor and cannot be distinguished from it.
5. **Drug arm is exploratory.** Desipramine does not shift the HD_down score within SNI (diff = +0.015, P = 0.83).
6. **Two protocol amendments (v0.1 → v0.2 → v0.3) are disclosed** in the protocol changelog, including the reasoning and the fact that the v0.2 fixes were motivated by Layer-0 internal evidence only.

## Data availability

GSE98547, GSE111216 and GSE261676 are public on GEO; GENCODE v24lift37 annotation from EBI. All derived statistics are deposited here and hashed in `analysis/MANIFEST.json`.
