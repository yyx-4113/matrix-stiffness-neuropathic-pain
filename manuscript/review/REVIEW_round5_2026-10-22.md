# REVIEW_round5_2026-10-22 — Drift-confirmation blind review (post de-AI polish)

## 1. Independence statement
Three blind reviewers (A1 Implementation/Provenance, A2 Domain/Prose-fidelity, A3 Venue/Reporting)
were briefed with a frozen `manuscript/review/round5_2026-10-22/_PANEL_BRIEF.md` and an explicit
forbidden-file list (no `REVIEW_*.md`, `RESPONSE_*.md`, `memory/`, `.workbuddy/` status, no other
reviewers' outputs). Each read the polished `manuscript/manuscript.md` and the analysis products
(`analysis/results/*.json`, `analysis/scripts/*`, `PROTOCOL_*.md`) independently and wrote to a
separate file. **Evidence independence worked:** A1, A2, and A3 converged on the same two genuine
defects (abstract structure/length; Discussion L83 G3 phrasing) from different angles, and A1's
recomputation of "full separation" (Discussion L83) independently confirmed A2's correctness on that
point — i.e. the panel did not merely re-litigate prior rounds.

## 2. Verdict table
| Reviewer | Layer | Verdict | Key point |
|---|---|---|---|
| A1 | Implementation/Provenance | PASS (1 minor) | No numeric drift; all digits match JSON. Flag: abstract >300 by strict count. |
| A2 | Domain/Prose-fidelity | PASS (1 fix) | No meaning drift; em-dash/flattening preserved hedging. Fix: L83 G3 BH-significant ambiguity. |
| A3 | Venue/Reporting | PASS (1 hard, 1 low) | Abstract 3-paragraph + >300 words; cover letter fully consistent, no em-dashes. |

**Distribution:** 0 Tier-0 (conclusion-invalidating), 0 Tier-1 (new analysis), 1 Tier-2 (wording/L83),
1 Tier-3 (format/abstract). **No drift from the de-AI polish was found** — every statistic, citation,
and conclusion in the polished text matches the analysis outputs and the pre-polish intent.

## 3. Cross-verification table (numbers vs JSON; editor-verified)
| # | Location | Manuscript claims | Independently recomputed | Who | Verdict |
|---|---|---|---|---|---|
| 1 | Layer 0 | CTGF Δ=+1.64, P=9.5×10⁻⁶ | matches layer0 JSON | A1 | ✓ |
| 2 | Stage A | DRG MRU=0.717/P=0.102/q=0.409; BLD 0.696/0.100/0.409 | matches layer1 JSON | A1 | ✓ |
| 3 | Stage B | HD_up +0.146/P=0.80/g=0.219; PC +1.285/P=0.0286/g=3.85; 17.6× gap | 3.8535/0.2187=17.62 | A1 | ✓ |
| 4 | Layer 3 | G1–G5 SI 38.4/0.44/1.44/240.5/9.06; 8/40 BH | matches layer3 JSON | A1 | ✓ |
| 5 | Layer 3 | G1∩G5 = 10 (43% of 23); G4 blood MRU≈0.499075 | recomputed 64∩23=10 | A1 | ✓ |
| 6 | Layer 3 | G1 q=0.0010, G5 q=0.0016 (DRG×SNI) | matches layer3 JSON | A1 | ✓ |
| 7 | Table 4 | G3 sample q=0.440, diff=−0.277, P=0.286 | matches layer3b JSON | A1, A2 | ✓ (and confirms G3 NOT BH-sig) |
| 8 | Discussion L83 | "passed with full separation" | saline SNI all +, sham all −; P=2/70=0.0286 = exact lower bound | A1 | ✓ accurate, not overstated |
| 9 | Abstract | 289 words strict / 275 filtered, 1 paragraph | editor recount | editor | ✓ after fix |

## 4. Graded consolidated issue list
- **Tier 2 (wording) — FIXED.** Discussion L83 attached "BH-significant signal" to G3 alongside G1/G5,
  contradicting L71/L85 (G3 does not reach BH significance; q=0.440 at sample level, q_matched=0.0652
  in DRG×SNI). Fixed to: "…the DRG-over-blood shift of G1 and G5 (q = 0.0010 and 0.0016 in DRG×SNI),
  and a mechanosensory signal in G3 (SI = 1.44) that retains specificity but does not reach BH
  significance." This is **pre-existing** (the flattening polish did not touch it) but is a genuine
  honesty-consistency defect caught by fresh eyes; not polish drift.
- **Tier 3 (format) — FIXED.** Abstract was 3 paragraphs and 303 words by strict whitespace count
  (PLOS ONE: single paragraph, ≤300 words). Merged to one paragraph and trimmed (~14 words) → 289
  strict / 275 filtered. All key elements retained (signature, 3 datasets, CTGF anchor, positive
  control, Stage A double-null §5.3 not triggered, Stage B bounded null, 1/5 specificity failure +
  G1/G5 overlap + G4 denominator artefact, limits-not-disproves conclusion).
- **Tier 3 (low, not fixed).** Body figure links use `../analysis/results/...` while legends cite
  `analysis/results/...`; filenames match, so not a hard violation. Left as-is (correct relative path
  for the manuscript subdirectory).

## 5. Consensus / complementarity / disagreement
- **Consensus:** the de-AI polish introduced no expression drift; em-dash removal and phrase flattening
  preserved meaning, hedging, and the honesty discipline (HD_down & G3 hypothesis-generating only;
  null is sensitivity-validated, not a method artifact).
- **Complementarity:** A1 (numbers) + A2 (meaning) + A3 (compliance) covered the three layers; A3's
  abstract finding was corroborated by A1's independent count.
- **Disagreement:** none of substance. A2 flagged "full separation" as slightly informal (optional
  unify with Methods terminology); A1 independently verified it is literally accurate, so no change
  made (kept for fidelity to the exact-permutation result).

## 6. Priority must-fix list
- (Tier 2) Discussion L83 G3 phrasing — FIXED.
- (Tier 3) Abstract single-paragraph + ≤300 — FIXED.
- No DESK-REJECT flags. No "must add analysis" items.

## 7. What stands up (do NOT change)
- All 43 gate assertions remain PASS; every numeric claim traces to `analysis/results/`.
- Honesty discipline intact: HD_down and G3 hypothesis-generating only; Stage A plain double-null
  (§5.3 not triggered); Stage B sensitivity-validated bounded null; G4 denominator artefact disclosed;
  G1/G5 10-member overlap disclosed.
- Cover letter fully consistent with manuscript; author "Yongxin Yang, B.M.", ORCID, repo+tag v1.0.0;
  no em-dashes in either manuscript or cover letter.
- Figure Legends (Fig 1–6 + S1), Data Availability (real repo + tag + traceability), Ethics/no-IRB,
  Vancouver `doi:`, Funding/Competing all compliant.

## 8. Recommended handling path
**C) Wording + format only** — no new analysis, no restructuring. The manuscript is submission-ready
for PLOS ONE after the two minor fixes above. Verdict: **ACCEPTABLE — ready for submission** (the
drift-confirmation round's purpose is satisfied; the two fixes are pre-existing/format issues, not
polish defects).

## 9. Process lessons
- A green consistency gate verifies arithmetic/provenance only; it does NOT cover abstract structure,
  word count, reference format, or cover-letter↔manuscript agreement — those needed human/venue review.
- Em-dash removal is safe only when the resulting sentence is re-punctuated as a complete sentence
  (verified here: 0 broken sentences).
- "Full separation" vs "detected at the exact-permutation lower bound" are the same event expressed
  two ways; a future editor should keep both only if they are provably identical (they are: P=2/70).
