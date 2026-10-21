# Round 6 — Consolidated blind review (acceptance-readiness lens)

**Date:** 2026-10-22 · **Verdict: ACCEPTABLE — submission-ready (PLOS ONE)**
**Lens:** not a drift check; three fresh blind reviewers judged whether a real PLOS ONE academic editor would ACCEPT / MAJOR / REJECT. Reviewers were forbidden from reading `review/`, `REVIEW_*.md`, `memory/`, `.workbuddy/`.

## Reviewer verdicts
| Reviewer | Lens | Verdict | Decisive reasons |
|---|---|---|---|
| B1 significance/novelty | would the null-dominated story publish? | MAJOR (text) | title over-claims; abstract/conclusion lump non-BH G3 with BH-significant G1/G5 (HARKing-adjacent) |
| B2 statistics | internal coherence | MAJOR (text) | **§5.3 governance contradiction** with cited protocol; "independent wins G1,G3,G5" self-contradictory; G4 bar reliability |
| B3 reproducibility | can a reader reproduce? | MAJOR (text) | Hedges-g formula absent; MRU mislabeled "1-based"; Layer-3b/4 endpoint label inconsistent; no software-env statement; protocol M12 stale |

## Genuine defects fixed this round (all verified against source, not memory)
1. **§5.3 governance contradiction (B2, critical).** The cited frozen protocol (PROTOCOL… lines 162, 251–262, 295) commands Stage A be written as **uninformative** ("must not revert to negative-result wording") for the exact numbers q=0.409 vs q=0.409. The manuscript previously said "§5.3 not triggered (plain double-null)" — directly contradicting its own governance source. **Fix:** reframed Stage A as *uninformative per §5.3* throughout — Methods §5.3, Results, Discussion, Core conclusion #2, Table 2 verdict, and the Abstract. The gate assertion that *enforced* the wrong framing was rewritten to enforce the correct one.
2. **Title over-claim (B1).** Old title's second clause ("established ECM/mechanotransduction gene sets show tissue-specific shifts") implied all sets shift at the BH standard; only the overlapping matrisome/fibrosis module (G1/G5) reaches BH significance, G2 failed, G3 is non-BH, G4 is a denominator artefact. **Fix:** retitled to "…: a sensitivity-validated null with retained rank-projection specificity of matrisome/fibrosis gene sets" (honest, precise). Cover-letter title updated in `build_docx.py` (both docx + md template).
3. **HARKing-adjacent G3 lumping (B1).** Abstract and Core conclusion #3 presented G3 alongside BH-significant G1/G5. **Fix:** G3 is now explicitly separated — "retains rank-projection specificity without BH significance or sample-level upregulation (hypothesis-generating)"; the robust positive is scoped to the matrisome/fibrosis module.
4. **MRU "1-based" factual error (B3).** Code (`layer1_projection.py:192`) uses 0-based ranks `np.arange(n)` with divisor `(n−1)`; manuscript said "1-based". **Fix:** corrected to "ranks are 0-based (0..n−1) so MRU spans 0..1 with 0.5 = no shift".
5. **Hedges g formula absent (B3).** **Fix:** added the bias-corrected formula `g = J·d, J = 1 − 3/(4N−9)` to Methods (Stage B).
6. **Matched-null decile detail only in code (B3).** **Fix:** stated in Methods that each draw selects one gene per member from the same baseline-expression decile.
7. **Layer-3b/4 endpoint-label inconsistency (B3).** Methods called them "characterisation", Table 2/Results called them "primary". **Fix:** unified to "pre-specified endpoint" in Methods context, Results, and Table 2.
8. **"Independent wins G1,G3,G5" self-contradiction (B2).** **Fix:** restated as two independent signals — the correlated matrisome/fibrosis module (G1/G5 overlap) and the non-BH mechanosensory module G3.
9. **G4 bar reliability (B2).** Figure 6 legend now states G4's bar "is not reliable" (denominator artefact).
10. **No software/environment statement (B3).** **Fix:** added Python 3.13 / fixed seed (20261021) note to Data Availability.
11. **Protocol M12 stale value (B3).** Updated pre-correction Cohen's d 4.431 → authoritative Hedges g 3.853 (per existing R13 erratum).
12. **Abstract length.** After reframing the abstract grew to 310 words (strict); trimmed to **294 words, single paragraph** (<300 PLOS limit).

## What stood up (reviewers confirmed intact)
- All reported statistics reconcile exactly with `analysis/results/*.json` (CTGF 1.64/9.5e-6; MRU 0.717/0.696; SI 38.4/0.44/1.44/240.5/9.06; 17.6× g-gap; 8/40 BH wins; Layer-3b/4 FAILs).
- BH "conservative under positive dependence" is statistically correct.
- G3 is coherently described everywhere as non-BH, non-sample-upregulated, hypothesis-only.
- Reproducibility is feasible: raw GEO inputs present locally, MANIFEST (97 artifacts + 42 raw) with checksums, consistency gate exists.
- All 7 figures code-generated, body-referenced, legend-consistent; all 14 references present and Vancouver-formatted; ethics/data-availability/funding/competing statements complete.

## Editor verdict
**ACCEPTABLE — ready for PLOS ONE submission.** Every Round-6 finding was a genuine text/reporting defect (no numeric error), all fixed and verified against source. The §5.3 reframing actually *strengthens* honesty (aligns the manuscript with its own frozen governance) and removes the one real contradiction a reviewer would have caught. Gate 43/43; abstract 294 words; 0 em-dashes.

## Residual (non-blocking, author discretion)
- Limitations remains a `###` subsection; PLOS ONE does not require `##`. Optional promote.
- Confirm the remote `v1.0.0` tag carries this commit (push below).
