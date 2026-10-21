# Panel Brief — Round 3 (journal-editor-organised independent review)

**Manuscript:** "A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity"
**Target venue:** PLOS ONE (Research Article / reanalysis). ISSN 1932-6203. Soundness-only; explicitly welcomes negative/null results and reanalysis.
**Author:** Yongxin Yang (single author, B.M.).
**Study in one sentence:** A prospectively pre-specified, two-stage *reanalysis* testing whether a mechanically controlled (substrate-stiffness) transcriptional signature, derived from human HEK293A (GSE98547, 1 vs 40 kPa fibronectin hydrogels, 4 Hippo-pathway genotypes), re-appears in injured pain tissues (mouse DRG / spinal cord) after nerve injury.

## Independence discipline (MANDATORY)

You are reviewing this as if it were a **first submission you have never seen**. Do NOT read any of the following (they contain prior review conclusions and will bias you):

- `manuscript/review/REVIEW_round1_2026-10-21.md`, `REVIEW_round2_2026-10-21.md`
- `manuscript/review/_PANEL_BRIEF.md` (the OLD brief), `manuscript/review/A1_domain.md`, `A2_design.md`, `A3_implementation.md`, `A4_venue.md`, `manuscript/review/Round2_*.md`
- `analysis/results/audit/audit_round*.json` (author's prior self-audit — predigested conclusions; forbidden)
- `README.md`, any `memory/*.md`, any `*.task` / task-status file, `author_verification_statement.md`, deposit SOP
- **Do NOT read the other three reviewers' files in `manuscript/review/round3/`** (A1/A2/A3/A4). Your judgement must be your own.

Do NOT assume the manuscript is mature or has passed prior review. Treat it as a fresh submission. Every judgement must come from text or source data you read yourself. Any numeric claim in the manuscript that you CAN verify, you MUST verify by recomputing.

## Source data you MAY read (and must, for any number you challenge)

- `manuscript/manuscript.md` — the manuscript under review.
- `analysis/results/layer0/layer0_signature.json`, `layer0_diagnostics.json` — signature members, CTGF Δ.
- `analysis/results/layer1/layer1_results.json`, `layer1_diag.json` — MRU / P / q for DRG×SNI and BLD×SNI (matched vs unstratified).
- `analysis/results/layer2/layer2_results.json`, `layer2_robustness.json`, `layer2_positive_control.json` — Stage B HD_up / HD_down / positive control.
- `analysis/results/layer3/layer3_generality.json`, `layer3b_sample_generality.json` — SI_g, MRU, BH q.
- `analysis/results/layer4/layer4_positive_characterisation.json`.
- `analysis/config/ms_panel.json` — frozen protocol, §5.3 governance, pre-specified endpoints, target_journals.
- `analysis/scripts/*.py` — the actual analysis code (read to verify the manuscript describes the implementation faithfully).
- Python (managed venv): `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe` (has numpy/pandas/scipy/docx/openpyxl).

Raw GEO inputs (GSE98547/111216/261676) are public; if you need FPKM/counts not present in the JSONs above, state that as a limitation rather than guessing.

## Output contract (MANDATORY — four parts per item)

- **【Problem】** one sentence.
- **【Evidence】** pinned to `file:line` of the manuscript, or `table/section + exact numbers`; numbers you cite MUST be ones you recomputed yourself (state the value and the source file you recomputed from).
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance.
- **【Specific fix】** a paste-ready English replacement sentence, or an explicit spec for a new analysis (variables, strata, output columns).
  "Consider strengthening the discussion" is BANNED.

Also required (separate § sections):
- **§ Stands up** (≥3, with evidence) — things you suspected but verified correct. A deliverable, not filler.
- **§ Questions for the authors** — what you need to know; do not guess answers.
- **§ What I actually checked** — files read, commands/computations run, values recomputed vs the manuscript's, with the discrepancy stated.

## Role-specific mandatory recomputations (do not skip — incomplete review otherwise)

- **A1 Domain:** verify ≥1 literature claim from the references (e.g., that Parisien 2019 [2] reports ECM-organization enrichment in neuropathic pain; that CTGF/CYR61/ANKRD1/AMOTL2 are established YAP/TAZ targets — checking against the cited Meng 2018 [1] or Dupont 2011 [4]); assess whether the HEK293A (epithelial, human) → mouse DRG (neuronal/glial) cross-species, cross-cell-type projection is biologically defensible as the authors frame it.
- **A2 Design/Stats:** (a) recompute SI_g for G4 from the full-precision MRU in `layer3_generality.json` and assess the denominator-instability claim (|ΔBLD−0.5|≈0.0009); (b) recompute the Layer-3 BH q for G1/G5 from the 40-test family and check the manuscript's q=0.0010/0.0016; (c) assess whether the "17.6-fold Hedges-g gap" comparison between positive control (g=3.85) and HD_up (g=0.219) is a valid bounded-null argument; (d) assess the §5.3 negative-control governance (blood equally non-significant → uninformative) for logical soundness.
- **A3 Implementation/Provenance:** (a) trace every headline number (CTGF Δ=+1.64/P=9.5e-6; HD_up n=18/HD_down n=41; Stage A MRU=0.717/P=0.102/q=0.409; Stage B +0.146/P=0.80/g=0.219; positive control +1.285/P=0.0286/g=3.85; G1 SI=38.4, G5 SI=9.06, G2 SI=0.44, G4 SI=240.5; Layer 4 8/15345) to a specific file and confirm; (b) recompute CTGF Δ from `layer0_signature.json` FPKM; (c) recompute the positive-control diff from `layer2_positive_control.json`; (d) check the abstract word count (must be ≤300, non-structured) and the Table 2/3/4 numbers against the JSONs; flag any double-rounding or mismatch.
- **A4 Venue/Editor:** (a) verify PLOS ONE reporting compliance — non-structured abstract ≤300 words, data-availability statement complete, ethics/IRB statement correct (note: no IRB because public de-identified data — is that defensible? PLOS ONE requires an Ethics statement; check it is present and adequate), competing-interests/funding statements, reference format (Vancouver, PMID/DOI present); (b) check cover-letter-vs-manuscript consistency (the cover letter is `manuscript/cover_letter.md`); (c) flag any PLOS ONE format hard-fail; (d) judge whether the article type (Research Article reanalysis with an honest bounded null) fits PLOS ONE and whether the framing over-claims given the many FAILED primary endpoints.

## Tool-talk forbidden
Do not mention what tools/scripts you used. Write review comments only, as if you are a human reviewer returning a marked-up report.
