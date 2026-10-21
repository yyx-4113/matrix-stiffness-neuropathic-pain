# Round-4 independent re-review — consolidation & editor verdict

**Date:** 2026-10-21
**Manuscript:** `manuscript/manuscript.md` (tag v1.0.0, commit 19b8782)
**Gate status at review:** `gate_consistency.py` 43/43 PASS; abstract 291 words (≤300); MANIFEST regenerated.

## Panel & discipline
Four blind reviewers were dispatched in parallel, each explicitly forbidden from reading `manuscript/review/`, any `REVIEW_*.md`, or `memory/`. Roles: A = domain/scientific honesty, B = design/statistics, C = implementation/reproducibility & figure–legend accuracy, D = PLOS ONE venue compliance. The editor independently verified each "worst finding" against the source code (`layer0_stiffness_signature.py`, `fig_layer2.py`, `fig_layer3.py`) and the deposited JSONs before accepting any fix.

## Findings triage

| # | Reviewer | Issue | Editor verification | Disposition |
|---|----------|-------|--------------------|-------------|
| 1 | A | Methods said HD assigned on "YAP/TAZ-dKO (or LATS1/2-dKO)" but text claimed "LATS-independent" → contradiction | **Genuine.** `layer0_stiffness_signature.py:308` assigns HD using `ratio_yt` only; LATS is a separate confirmation metric (line 333). | FIXED — now states assignment uses YAP/TAZ-dKO only; LATS used solely for directional confirmation. |
| 2 | A | Results calls G3 "BH-significant" (line 71) but Discussion says only G1/G5 reach BH (line 85) | **Genuine contradiction.** | FIXED — line 71 now: G1 & G5 are BH-significant; G3 retains SI specificity but does not reach BH and was not up-regulated at sample level. |
| 3 | A, B | Abstract mis-states §5.3 trigger ("informative-negative-control rule is unmet"); rule triggers on *equally significant*, not *equally non-significant* | **Genuine.** | FIXED — abstract now: "§5.3 rule (triggered only by an equally significant control) did not apply … plain double-null". |
| 4 | A | Discussion presents G3 mechanosensory reading as "biologically salient" while Limitations calls it hypothesis-generating and Layer-3b shows G3 decreased (diff −0.277) | **Genuine over-assertion.** | FIXED — softened to "possible mechanosensory engagement … reported as hypothesis-generating only" with the Layer-3b numbers. |
| 5 | B | "40-test BH family is anti-conservative" is backwards — overlapping/positively dependent tests make BH *conservative* | **Genuine (statistically incorrect).** | FIXED — recast as non-independence + BH remains valid (conservative under positive dependence); the real flaw is the "4/5" double-counting. |
| 6 | B | G1's own denominator (|ΔBLD−0.5|=0.0106) also near-zero, so SI≈38 inflated; no SI uncertainty reported | **Genuine (partial).** | FIXED — Table 3 footnote now notes G1 denominator is also small; robust fact is its large BH-significant DRG MRU (0.906). |
| 7 | B | Abstract "did not transfer" and "fully separated" overstate a borderline lower-bound detection / low-power design | **Genuine (partial).** | FIXED — abstract: "no detectable transfer … at the 4-vs-4 resolution"; Fig 5 legend: "detected at the exact-permutation lower bound". |
| 8 | C | S1 Fig legend says "seven gene sets (HD_up, G1–G5)" = 6 gene sets + positive control → 7 bars; miscount | **Genuine.** | FIXED — "positive control plus six gene sets … seven bars in total". |
| 9 | D | Abstract 302 words > PLOS ONE 300 cap | **Genuine (verified 291 plain / 280 regex post-trim).** | FIXED — trimmed to 291 words. |
| 10 | D | "Pre-registered §5.3" invoked but no citable registration | **Genuine.** | FIXED — Methods cites `PROTOCOL_基质刚度与神经病理性痛.md` (tag v1.0.0) at the §5.3 mention. |

## Non-blocking (carried, not blocking)
- **C:** stale `analysis/results/layer2/fig/fig2_member_contributions.png` (superseded by `fig3_member_contributions.png`, unreferenced) — leave or delete at author discretion; MANIFEST already excludes nothing harmful.
- **D:** Limitations is a `###` subsection of Discussion rather than a standalone heading — acceptable; PLOS ONE does not require a separate heading.

## Editor verdict
**ACCEPTABLE — ready for PLOS ONE submission.** All ten genuine findings were verified against source code/data and resolved; the consistency gate (43/43) and abstract word cap (291 ≤ 300) both pass; figure legends now match actual figure contents (verified for Figures 1–6 and S1, including the Figure-4 = HD_down matched-null correction carried from Round 3). The manuscript's central, defensible claims are: (i) the HEK293A stiffness program shows no *detectable* transfer to injured DRG at the achievable 4-vs-4 resolution (a sample-level sensitivity-validated null, not a method artifact); (ii) Stage A is a plain double-null (§5.3 not triggered); (iii) once baseline-expression confounding is controlled, established ECM/mechanotransduction sets retain a DRG-over-blood shift for G1, G5, and the mechanosensory G3, with the G1/G5 overlap and G4 denominator artefact explicitly disclosed. No residual over-claim or number inconsistency was found.

## Residual author actions before submission (outside this review)
- Confirm the real GitHub remote carries the tag v1.0.0 commit (local tag only was re-pointed; remote was unreachable at review time).
- Optional: delete the stale `fig2_member_contributions.png`.
- Optional: promote Limitations to a standalone `##` heading.
