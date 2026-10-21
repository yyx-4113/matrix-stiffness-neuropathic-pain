# Independent Review Panel — Round 2 verification (2026-10-21)

**Mandate:** confirm that every Round-1 issue (T0-1, T0-2, T1-1…T1-7, T2-1…T2-6) is resolved and detect any NEW blocking issue. Four blind, self-contained reviewers; no reviewer read another's output.

## Per-reviewer verdict

| Reviewer | Role | Round-1 → Round-2 | Residual / new issues | Verdict |
|---|---|---|---|---|
| A1 | Domain (pain / mechanotransduction) | All blockers resolved; numbers re-verified against JSONs (CTGF, set sizes, LATS%, all 5 SI, 1/5 fail) — 0 discrepancies | 2 minor: (a) post-hoc "ECM/YAP–TAZ separation" lacked DRG citations; (b) "cell-type-specificity limit of mechanotransduction" over-generalises | MINOR |
| A2 | Design / Biostat | T1-1 (LOO/Q4→HD_down), Layer-3 reframing, Hedges-g labels — all RESOLVED | 3 minor: (a) line 59 residual "equally significant"; (b) line 40 C(8,4)=35 wrong (is 70); (c) Table 3 `\|Δ\|` 3-dp rounding hides SI | MINOR |
| A3 | Implementation / Auditor | 39/39 gate PASS; protocol §8.1 reconciled (BLD q=0.409); Tables 1–4 + inline match JSONs; no `0.0072`/`two orders` fingerprints | 2 minor: (a) line 59 "equally significant" residue; (b) MANIFEST omits layer3/3b/4 JSONs (non-blocking, Task #21) | MINOR |
| A4 | Venue / Editor (GigaScience) | T0-1 title resolved; abstract 319w / body 1964w within caps; 6+1 figs, 4 tables, 10 real PMID/DOI refs; byline/ORCID/affiliation correct (no degree) | 1 MAJOR (packaging-only): README.md + CITATION.cff asserted superseded conclusion (g=4.43/0.25/3.06, "blood P=0.0009" headline, "ECM lacks specificity") — contradicted manuscript; 1 minor: "BH" undefined on first use | MAJOR (packaging) |

## Fixes applied in this round (post-Round-2)

- **M1** Line 59: "equally significant" → "equally non-significant (q = 0.409 = DRG)".
- **M2** Line 40: "C(8,4) = 35 (4-vs-4) or 70 (8-sample)" → "C(8,4) = 70 possible 4-vs-4 splits (two-sided)".
- **M3** Table 3: MRU and `\|Δ\|` columns extended to 4 d.p. (0.9056 / 0.5106 … 0.8857 / 0.4574); footnote clarifies SI is from full-precision MRU and the rounded columns will not exactly reproduce SI by division.
- **M4** Line 14: first "BH q" expanded to "BH (Benjamini–Hochberg) q".
- **M5 (MAJOR)** README.md and CITATION.cff fully rewritten to the v1.0.0 reframed conclusion — correct Hedges g (HD_up 0.219, HD_down 2.658, positive control 3.85), correct Stage-A framing (blood control equally non-significant q=0.409; unstratified BLD P=0.0009 noted as confound only), correct "specificity retained by 4/5 established sets" narrative; version bumped to 1.0.0.
- **M6** Line 87: "cell-type-specificity limit of mechanotransduction" → "cell-type- and mechanical-input-specific limit of this particular HEK293A-derived, substrate-fibronectin-stiffness program".
- **M7** Added paragraph distinguishing Layer-3 rank-projection direction-of-shift specificity from Layer-3b/4 sample-level upregulation.
- **M8** Limitations: post-hoc YAP/TAZ-vs-structural-ECM separation flagged as hypothesis-generating, no direct DRG literature, requires validation.

## Status after fixes

- Consistency gate: **39/39 PASS** (re-run post-edits).
- No stale fingerprints ("0.0072", "two orders", "equally significant", "g=4.43", "ECM lacks specificity") remain in manuscript, README, or CITATION.
- Abstract 319 / body 1964 words — within GigaScience caps.
- All 10 references carry real, online-verifiable PMID/DOI.

**Panel consensus: content is ACCEPTABLE FOR SUBMISSION after the packaging step (T0-2): create the real repository, tag v1.0.0, and fill the data-availability URL.** No remaining content blocker. Next: de-AI polish (Task #20) → final gate + MANIFEST (Task #21) → repo + tag + URL (Task #18) → docx + cover letter (Task #22).
