# Independent Review Panel — Shared Brief (Round 1)

## Manuscript under review
`D:/2026.10/基质刚度/manuscript/manuscript.md`
Target venue: **GigaScience** (IF ~5.0, scope: reproducible/computational biology, data reuse).
Article type claimed: Research Article (computational reanalysis / methodological audit).

## What the study is
A prospectively specified reanalysis that (a) derives a Hippo-dependent "stiffness signature" from a stiffness-controlled experiment GSE98547 (human HEK293A, 1 vs 40 kPa hydrogels, 4 Hippo-pathway genotypes → HD_up n=18, HD_down n=41), then (b) projects it onto neuropathic-pain transcriptomes GSE111216 (4 tissues × 2 pain models, summary stats) and GSE261676 (mouse DRG sample-level, SNI model). Endpoints were frozen before inspecting pain data.

## Core tension to scrutinize
The protocol's frozen core claims (§11.1) asserted that tissue specificity "fails universally" across ECM/mechano gene sets and that blood shifts as much or more than DRG. The ACTUAL Layer-3 data show only 1/5 sets (G2 YAP/TAZ) lack specificity (SI=0.44) while 4/5 retain it (G1 SI=38.4, G3 SI=1.44, G4 SI=240.5, G5 SI=9.06). The manuscript RE-FRAMED the conclusion to "signature/cell-type-specific failure" rather than universal method failure. The panel must judge whether this reframing is scientifically defensible and honestly reported, and whether any residual over-claim remains.

## Independence discipline (mandatory)
Forbidden to read: `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, any task-status or project-overview file, `SUBMISSION_MANIFEST.md`, any deposit SOP, `author_verification_statement.md`, and **other reviewers' outputs in this directory**.
Do NOT assume the manuscript is mature or has passed prior review. Treat as a first submission.
Every judgement must come from text or source data you read yourself. Any number you can verify, you MUST verify.

## Source data (read these; do not trust the manuscript)
- `D:/2026.10/基质刚度/manuscript/manuscript.md` (the text)
- `D:/2026.10/基质刚度/PROTOCOL_基质刚度与神经病理性痛.md` (frozen protocol, esp. §4, §5.3, §10, §11, §12)
- `D:/2026.10/基质刚度/analysis/results/layer0/layer0_signature.json`
- `D:/2026.10/基质刚度/analysis/results/layer1/layer1_diag.json`
- `D:/2026.10/基质刚度/analysis/results/layer2/layer2_positive_control.json`
- `D:/2026.10/基质刚度/analysis/results/layer2/layer2_robustness.json`
- `D:/2026.10/基质刚度/analysis/results/layer3/layer3_generality.json`
- `D:/2026.10/基质刚度/analysis/results/layer3/layer3b_sample_generality.json`
- `D:/2026.10/基质刚度/analysis/results/layer4/layer4_positive_characterisation.json`

## Mandatory checks (per expert)
- Recompute: CTGF Δ and P; Stage A matched MRU/P/q for DRG×SNI and BLD×SNI HD_up; Stage B HD_up & positive-control difference/P/Hedges g; Layer-3 SI for all 5 sets; Layer 3b table; Layer 4 n-sig-up. Compare to manuscript.
- Verify the §5.3 "uninformative not negative" framing is correct given BLD q = DRG q = 0.409.
- Verify HD_down is only hypothesis-generating; verify no claim exceeds protocol §11.2 red lines.
- Verify all 10 references are real (PMID/DOI) — this is a hard rule for this author.

## Output contract (every item needs all 4)
- 【Problem】one sentence
- 【Evidence】pinned to file:line or table/section + exact numbers you recomputed
- 【Why it matters】concrete effect on conclusions/credibility/acceptance
- 【Specific fix】paste-ready sentence, or explicit spec for a new analysis

## Also required
§ Stands up (≥3, with evidence) — things you suspected but found correct.
§ Questions for the authors.
§ What I actually checked — files read, values recomputed vs manuscript, discrepancies stated.
