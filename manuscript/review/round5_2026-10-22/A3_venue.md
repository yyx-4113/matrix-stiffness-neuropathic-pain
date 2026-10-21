# A3 — Venue / Reporting-standard audit (PLOS ONE, Round 5, 2026-10-22)

**Role:** Independent venue/standard auditor on the blind panel. I judged only the manuscript (`manuscript/manuscript.md`), the cover-letter generator (`manuscript/build_docx.py`), and the consistency gate (`analysis/scripts/gate_consistency.py`). I did **not** read any prior review/response files, memory, or other panel output. All findings are from the current text.

---

## FINDINGS (each with Problem / Evidence / Why it matters / Specific fix)

### F1 — Abstract is NOT a single paragraph, and likely exceeds 300 words *(Checklist item 1)*

【Problem】 PLOS ONE requires the Abstract to be a single, unstructured paragraph of ≤300 words. The current Abstract is split into **three** paragraphs, and a direct token count exceeds the 300-word ceiling.

【Evidence】
- `manuscript.md:8` `## Abstract`, then three distinct paragraph blocks at `manuscript.md:10`, `:12`, `:14`, separated by blank lines `:11` and `:13`.
- Token count (whitespace-delimited): Para 1 ≈ 82, Para 2 ≈ 132, Para 3 ≈ 89 → **≈303 tokens total**. This is above 300. (Note: a few tokens are pure symbols/numbers — `Δ`, `×`, `§5.3`, `10⁻⁶` — which some counters exclude; the journal's own counter may land a few words lower, but the brief's stated "289 words" is not reproduced by a direct count, so the true margin is unconfirmed.)

【Why it matters】 A multi-paragraph / over-limit Abstract is a hard desk-reject or mandatory-revision trigger at PLOS ONE. It also signals to reviewers that the post-polish formatting pass was incomplete.

【Specific fix】 Merge `manuscript.md:10`, `:12`, `:14` into one paragraph under `## Abstract`. Paste-ready spec:
> "Under `## Abstract`, replace the three blocks (lines 10, 12, 14) with a single paragraph. Re-count with the submission system's counter; if still >300, cut the redundant second-sentence restatement of the positive control (the sensitivity result is already stated once) and/or trim the Layer-3 qualifying clause, which is fully developed in the Discussion."

---

### F2 — Figure path prefixes differ between body and legends (low severity) *(Checklist item 2, near-miss)*

【Problem】 Body figure links use a `../` prefix; legends cite the same filename without it. Not a hard violation (filenames match exactly), but inconsistent for a self-contained deposit.

【Evidence】
- Body: `manuscript.md:54,59,64,66,68,73,78` → `![...](../analysis/results/...png)`.
- Legends: `manuscript.md:181,183,185,187,189,191,193` → `Source: \`analysis/results/...png\`` (no `../`).

【Why it matters】 Both resolve to the same file, so figure rendering in the generated `.docx` is unaffected (the builder resolves paths from the manuscript root). But if the markdown is ever deposited or rendered standalone, the `../` vs bare path mismatch is a cosmetic inconsistency a meticulous editor may flag.

【Specific fix】 Make the two forms identical. Recommended: drop `../` from the body links so both read `analysis/results/...`, OR add `../` to the legend `Source:` lines. Either is fine; pick one and apply to all 7.

---

## § STANDS UP (compliance confirmed, with evidence)

1. **Figure Legends section complete and consistent.** `manuscript.md:179` `## Figure Legends` present; Figure 1–6 and S1 Fig each carry a legend ending in a `Source:` filename (`manuscript.md:181,183,185,187,189,191,193`), and every filename matches a body `![]()` reference (`manuscript.md:54,59,64,66,68,73,78`). All 7 of 7 present and consistent.

2. **Data Availability statement compliant.** `manuscript.md:101` names the real repository `https://github.com/yyx-4113/matrix-stiffness-neuropathic-pain`, the tag `v1.0.0`, and the traceability clause "every numeric claim in this manuscript is traceable to a file under `analysis/results/`." Meets the hard constraint.

3. **Ethics / no-IRB rationale present.** `manuscript.md:100` explicitly states the work uses only pre-existing, de-identified public GEO data and therefore "does not require institutional review board (IRB) approval," with the secondary-analysis justification. Adequate.

4. **References are Vancouver with lowercase `doi:` and PMID.** Spot-checked three: Ref 1 (Meng *Nature* 2018, PMID 30135582, doi 10.1038/s41586-018-0444-0), Ref 5 (Naba *Matrix Biol* 2016, PMID 26163349, doi 10.1016/j.matbio.2015.06.003), Ref 7 (Wynn *J Pathol* 2008, PMID 18161745, doi 10.1002/path.2277) — all real, correctly formatted, `doi:` lowercase, PMID present. Format is consistent across all 14 entries.

5. **Funding / Competing Interests use PLOS-standard phrasing.** `manuscript.md:102` "The author has declared that no competing interests exist." and `manuscript.md:103` "The author received no specific funding for this work." Both match PLOS boilerplate.

6. **Cover letter is fully consistent with the manuscript.** (a) Title match: `manuscript.md:1` vs `build_docx.py:172–174` / `:224–226`. (b) It says "sample-level, sensitivity-validated null, not a method artifact" (`build_docx.py:183` / `:234`), not "methodological null." (c) The "4/5" positive reading is qualified with the G1/G5 10-member overlap **and** the G4 denominator artefact, and the inflated count is acknowledged (`build_docx.py:186–188` / `:236–238`) — matching the manuscript's Table 3 footnote. (d) Author is "Yongxin Yang, B.M." (`build_docx.py:205` / `:248`) — not MD/PhD. (e) ORCID 0009-0004-9698-6552 present (`build_docx.py:207` / `:250`). (f) Repo + tag present (`build_docx.py:197–198` / `:244`). (g) **Em-dashes are absent from the cover letter** — grep for `—` in `build_docx.py` returned no matches, confirming the de-AI polish also cleaned the cover letter (both the Python docx body and the .md template use `—`-free phrasing, quotes, and `Δ`/`×`/`⁻⁶` characters instead).

7. **Manuscript itself is em-dash-free post-polish.** Grep for `—` in `manuscript.md` returned no matches; retained dashes are en-dashes (`–`) in ranges/compounds (e.g., "YAP/TAZ–TEAD", "Benjamini–Hochberg", "SNI − sham"), which are PLOS-acceptable and distinct from em-dashes. No expression drift detected in the quantitative claims (CTGF Δ=+1.64, P=9.5×10⁻⁶; positive control +1.285, P=0.0286, g=3.85; Stage A MRU=0.717/0.696, q=0.409; Stage B +0.146, P=0.80, g=0.219; G1/G5 q=0.0010/0.0016) — all internally consistent across Abstract, Results, Discussion, Tables, and cover letter.

---

## § QUESTIONS FOR THE AUTHORS

1. **Abstract word count:** Please confirm the exact word count with the journal's submission-system counter. My whitespace tokenization gives ≈303, above the 300 limit, and does not match the "289 words" figure in the round brief. If it is over, what will you cut? (The three-paragraph split must be fixed regardless.)
2. **Numeric traceability:** The Data Availability statement asserts every number traces to `analysis/results/`. I did not execute the pipeline. The gate (`gate_consistency.py`) independently recomputes only a *subset* (CTGF Δ, Stage-B HD_down diff, Layer-3 G2 MRU, mapping rate) from raw inputs; the full 40-test Layer-3 table, Table 2/4 verdicts, and the HD_down lower-bound claim rest on deposited artifacts I could not re-run. Can you confirm the complete set was regenerated and matches the manuscript?
3. **Figure path prefix:** Will the deposited `.docx` embed figures from the resolved (manuscript-root) path, and is the `../` vs bare `analysis/results/...` discrepancy in the markdown intentional or an artefact of the build script?

---

## § WHAT I ACTUALLY CHECKED

**Files read (in full):**
- `manuscript/manuscript.md` — all 194 lines.
- `manuscript/build_docx.py` — all 260 lines (extracted both the Python docx cover-letter body string, lines ~163–207, and the markdown cover-letter template, lines ~214–251).
- `analysis/scripts/gate_consistency.py` — all 329 lines.

**Items verified against the PLOS ONE checklist:**
1. Abstract paragraph structure (3 paragraphs, not 1) and approximate word count — **FAIL**.
2. Figure Legends section + all 7 legends vs 7 body `![]()` refs — **PASS**.
3. Data Availability URL + tag v1.0.0 + traceability clause — **PASS**.
4. Ethics / no-IRB rationale — **PASS**.
5. References Vancouver + lowercase `doi:` + PMID, 3 spot-checked — **PASS**.
6. Funding / Competing Interests standard phrasing — **PASS**.
7. Cover letter ↔ manuscript consistency: title, "sensitivity-validated null not method artifact", G1/G5+G4 qualification, author "B.M.", ORCID, repo+tag, and em-dash absence — **PASS**.
8. New format issues from polish: only the pre-existing/missed Abstract paragraph split and the path-prefix inconsistency; no broken tables, sentence fragments, or misplaced captions introduced. Em-dashes confirmed removed from both manuscript and cover letter.

**Discrepancies / limitations stated:**
- The brief's "289 words" is not reproduced by direct tokenization (≈303); true count depends on the journal's counter.
- The gate's manuscript-coherence guards (`gate_consistency.py:307–317`) assert only *string presence* (§5.3 double-null, G1/G5 overlap, "denominator artefact", "`## Figure Legends`"). They do **not** cover Abstract structure, word count, reference format, or cover-letter/manuscript agreement — so a green gate does not imply PLOS ONE compliance on those axes. I treated the gate as informational only, not as proof.
- I did **not** execute `gate_consistency.py` or the analysis pipeline, so I could not independently re-derive the numeric claims; I verified internal *consistency* of quoted numbers across the manuscript and cover letter, not independent reproducibility from raw data.
- En-dashes retained in compounds/ranges are PLOS-acceptable and were correctly left in place; only em-dashes were required to be absent, and they are.
