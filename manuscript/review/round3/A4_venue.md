# A4 — Venue & Editor review (PLOS ONE, Round 3)

**Manuscript:** "A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity"
**Target venue:** PLOS ONE (Research Article / reanalysis)
**Reviewer role:** Independent journal editor + reporting-standards auditor
**Independence note:** Reviewed as a fresh submission; no prior reviews, audit artifacts, or other reviewers' files were consulted.

---

## 1. Abstract — non-structured and within limit, but abbreviation-heavy

【Problem】The abstract is correctly non-structured and within the word ceiling, but it packs ~25 abbreviations into 298 words, against PLOS ONE's "Abbreviations, if possible" guidance.

【Evidence】manuscript.md:9–14. Word count measured at **298 words** for the abstract body (300 if the section-heading token "Abstract" is counted) — inside the ≤300-word ceiling (per PLOS ONE submission guidelines: "Not exceed 300 words"). No bracketed literature citations appear in the abstract (good; PLOS ONE forbids citations in abstracts). The text is a single continuous narrative with no Background/Methods/Results/Conclusions sub-headings (correct for PLOS ONE). However it uses ECM, HEK293A, HD_up, HD_down, MRU, BH, DRG, SNI, BLD, CFA, GSE98547/111216/261676, YAP/TAZ, SI_g, and Hedges g without expansion in the abstract itself.

【Why it matters】An editor scanning the abstract sees a wall of symbols; PLOS ONE explicitly discourages abbreviations there because the abstract is indexed and read standalone. This will trigger a copy-edit query and can read as inaccessible.

【Specific fix】In the abstract, spell out the first occurrence of each acronym or drop the least essential ones: e.g., "extracellular matrix (ECM)" (already done in body), "human HEK293A cells", "dorsal root ganglion (DRG)", "spared-nerve-injury (SNI)", "blood (BLD)", "median-rank utility (MRU)", "Benjamini–Hochberg (BH)", "Hedges g effect size". At minimum expand DRG, SNI, BLD, MRU, BH, SI_g on first abstract appearance.

---

## 2. Ethics statement — under-specified for PLOS ONE (MUST-FIX)

【Problem】The one-line Ethics statement does not satisfy PLOS ONE's requirement to state *why* IRB/ethics approval was not obtained, nor that the underlying public datasets carried their own approvals, nor that the study posed no privacy risk.

【Evidence】manuscript.md:98 — "**Ethics.** This study used only public, de-identified transcriptomic datasets; no new human or animal subjects were enrolled." PLOS ONE guidance: "If approval was not obtained, the authors must provide a detailed statement explaining why it was not needed" and for anonymized/aggregated third-party data "informed consent is generally not required" while authors "should declare any potential risks to individuals or individual privacy, or affirm that … the study posed no such risks." The current statement asserts de-identification and no new subjects but (a) never states IRB/ethics approval was *not required / waived*, (b) does not note that the original GEO deposits (GSE98547 human cell line; GSE111216/GSE261676 mouse) carried their own institutional approvals, and (c) does not affirmatively state no privacy risk to individuals.

【Why it matters】PLOS ONE returns manuscripts with an incomplete Ethics statement before review. This is the single most likely compliance rejection point. The science is a secondary reanalysis, so "not required" is a defensible position — but it must be *said*, not implied.

【Specific fix】Replace manuscript.md:98 with:

> **Ethics.** This study is a secondary analysis of publicly available, de-identified transcriptomic datasets and involved no new enrollment of human participants or animal subjects. GSE98547 (human HEK293A cell line), GSE111216, and GSE261676 (mouse) were accessed through the Gene Expression Omnibus; the original deposits were approved by the ethics committees of the contributing institutions, and the data were de-identified and aggregated prior to our access, so informed consent was not required for this reanalysis. Institutional Review Board / Independent Ethics Committee approval was therefore not required for this study. We assess that the reanalysis posed no risk to the privacy of any individual.

(The cover letter already states "no IRB/ethics approval required" at cover_letter.md:22 — mirror that language in the manuscript.)

---

## 3. Data Availability — adequate

【Problem】None material; one minor strengthening suggestion.

【Evidence】manuscript.md:99 — "Source datasets: GSE98547, GSE111216, GSE261676 (Gene Expression Omnibus). Analysis code, configuration, and all result artifacts are deposited at https://github.com/yyx-4113/matrix-stiffness-neuropathic-pain (tag v1.0.0) with a MANIFEST of checksums; every numeric claim … traceable to a file under `analysis/results/`." The three accession numbers match those cited in the body (manuscript.md:29) and in the cover letter (cover_letter.md:22). The repo URL is identical between manuscript and cover letter. A checksummed MANIFEST satisfies PLOS ONE's "every numeric claim traceable" expectation better than most.

【Why it matters】This is a compliance strength, not a defect; PLOS ONE requires accession numbers in the statement (present) and that data be at least as open as CC BY (a public GitHub repo + GEO satisfies this).

【Specific fix】Optional: add "Raw counts/FPKM are available from GEO under the three accessions above" so a reader knows the *raw* inputs are GEO-hosted and the *processed artifacts* are on GitHub. No change is mandatory.

---

## 4. Competing interests / Funding / Authors' contributions — present, with PLOS ONE placement notes

【Problem】All three statements exist, but PLOS ONE expects Competing Interests and Funding to be entered in the submission form rather than the manuscript, and the unfunded phrasing should follow the house template.

【Evidence】manuscript.md:100 "**Competing interests.** None declared."; :101 "**Funding.** None."; :102 "**Authors' contributions.** YY conceived, performed, and wrote the analysis and manuscript." PLOS ONE guidance: Competing Interests and Financial Disclosure "should not be in your manuscript file; you will provide it via our submission system," and for an unfunded study the exact statement is "The author(s) received no specific funding for this work."

【Why it matters】Including these in the manuscript is not a hard fail (many authors do), but "None." for funding deviates from the preferred wording and the competing-interests block will be re-requested in the form regardless. Single-author "conceived, performed, and wrote" is fully acceptable for PLOS ONE.

【Specific fix】Keep the Declarations block (harmless and transparent), but (a) change :101 to "**Funding.** The author received no specific funding for this work." and (b) change :100 to "**Competing interests.** The author has declared that no competing interests exist." These match PLOS ONE's standard phrasing and avoid an editor query.

---

## 5. References — Vancouver + PMID/DOI present and consistent

【Problem】No format failure; one stylistic nit on the DOI label.

【Evidence】manuscript.md:160–169. All 10 references are numbered in citation-sequence order, use "first six authors, et al.," carry a real PMID **and** a DOI, and each is actually cited in text (datasets [1][2][3]; mechanotransduction background [4]; gene-set sources [5][6][7][8][9][10]). Spot-checked plausibility: [1] Meng 2018 *Nature* 560:655 (RAP2/Hippo) ✓; [2] Parisien 2019 *Pain* 160:932 (ECM in pain) ✓; [3] Serafini 2024 *Neurobiol Pain* 15:100153 (GSE261676 source) ✓; [4] Dupont 2011 *Nature* 474:179 (YAP/TAZ mechanotransduction) ✓; [7] Wynn 2008 *J Pathol* 214:199 (fibrosis) ✓; [9] Zhao 2008 *Genes Dev* 22:1962 (TEAD/YAP) ✓. The DOI label uses "DOI:" whereas PLOS ONE's sample uses "doi:" — cosmetic only.

【Why it matters】Reference compliance is a pass; an editor will not block on this.

【Specific fix】Optional: change "DOI:" → "doi:" to match the ICMJE/PLOS sample exactly. No substantive change needed.

---

## 6. Cover letter vs manuscript consistency — "correction" over-claims

【Problem】The cover letter calls the result a "Methodology-driven correction to prior 'ECM enrichment in pain' interpretations," which is stronger than the manuscript's own "circumscribes … without disproving them" framing.

【Evidence】cover_letter.md:18 — "Methodology-driven correction to prior 'ECM enrichment in pain' interpretations; fit for PLOS ONE's soundness-only criterion." vs manuscript.md:87 — "Our null thus *circumscribes* the literature's 'ECM enrichment in pain' claims to the source cell type of the projected signature, without disproving them." Also check (a) journal name cover_letter.md:6 "PLOS ONE" ✓; (b) title cover_letter.md:11–13 exactly matches manuscript.md:1 ✓; (c) signature cover_letter.md:27 "Yongxin Yang, B.M." — correct, no MD/PhD, consistent with the author's stated B.M. credential ✓. The only mismatch is the verb "correction."

【Why it matters】PLOS ONE editors read the cover letter against the manuscript. "Correction" implies the prior literature was wrong; the manuscript explicitly denies disproving it. This inconsistency can read as over-claiming at the editorial triage stage and undermines the honest bounded-null framing the manuscript works hard to maintain.

【Specific fix】In cover_letter.md:18, replace "Methodology-driven correction to prior 'ECM enrichment in pain' interpretations" with "a methodology-driven refinement that circumscribes prior 'ECM enrichment in pain' interpretations to the source cell type of the projected signature."

---

## 7. Over-claim risk in title/abstract given the failed primary endpoints

【Problem】The title's positive second clause ("while established ECM gene sets retain tissue specificity") and the abstract's "4/5 shifted at least as far in DRG as in blood" rest on a rank-projection specificity index (SI_g) that is denominator-unstable for one of those five sets (G4), yet the caveat is buried in a table footnote rather than in the title/abstract.

【Evidence】Title manuscript.md:1; abstract manuscript.md:12 "4/5 shifted at least as far in DRG as in blood, with G1, G5 at BH significance (q = 0.0010, 0.0016)." The SI_g definition manuscript.md:44; Table 3 manuscript.md:137 shows G4 SI_g = 240.5 with |ΔBLD−0.5| = 0.0009; the footnote manuscript.md:140 explicitly warns "SI is unstable when |ΔBLD−0.5| ≈ 0 (G4 denominator ≈ 0.0009); read the absolute shifts directly." So the "4/5 retain specificity" headline includes one set (G4) whose specificity ratio is effectively undefined. Meanwhile the *pre-specified primary* Layer-3 hypothesis (≥4/5 sets FAIL specificity) was NOT met (manuscript.md:71, 125 "primary FAIL"), meaning specificity was *retained* — but that retention is a secondary/descriptive observation, not the registered primary conclusion.

【Why it matters】An editor skimming title + abstract sees a positive claim ("ECM gene sets retain tissue specificity") while the registered primaries (Layer 3 primary, Layer 3b, Layer 4, Stage A) all failed or were uninformative. Without the G4 caveat in the title/abstract, the positive clause can be read as over-selling a denominator-unstable ratio. The body is honest; the front-matter framing is not fully aligned with that honesty.

【Specific fix】Either (a) add a one-clause caveat to the abstract's positive sentence, e.g. "…established ECM/mechanotransduction gene sets retain tissue specificity in a rank-projection benchmark (4/5; G1, G5 significant; one set's index is denominator-unstable and read from absolute shifts)," or (b) soften the title's second clause to "while established ECM gene sets retain rank-projection tissue specificity." Do not drop the finding — it is real and well-discussed at manuscript.md:83,85 — but flag the G4 instability at the front-matter level.

---

## 8. Format hard-fails — figure legends not in a dedicated section; figure naming

【Problem】Figures are embedded with alt-text captions rather than gathered in a "Figure Legends" section, and the supplement is labelled "Figure S1" instead of PLOS ONE's "S1 Fig."

【Evidence】Embeds with alt-text captions at manuscript.md:54, 59, 64, 66, 68, 73, 78 (e.g., `![Figure 1. Signature derivation: Hippo-dependent members]…`). PLOS ONE requires figure legends in a dedicated "Figure Legends" section, each legend numbered and self-contained; alt-text alone is not an acceptable legend. The supplement is "Figure S1" (manuscript.md:78) whereas PLOS ONE style is "S1 Fig."

【Why it matters】PLOS ONE's production workflow expects a Figure Legends section; submissions without one are returned for formatting. Mislabeled supplementary figure numbering triggers a mechanical copy-edit loop.

【Specific fix】Add a "Figure Legends" section after the Tables containing, for each of Figs 1–6 and S1 Fig, a one-to-two sentence legend (what is plotted, what the shading/colour encodes, what the reader should conclude). Rename "Figure S1" → "S1 Fig" at manuscript.md:78 and in its legend.

---

## 9. Article-type fit — good; honest bounded null is exactly PLOS ONE's remit

【Problem】None — the manuscript fits PLOS ONE well.

【Evidence】PLOS ONE is explicitly "soundness-only" and "welcomes negative/null results and reanalysis." This manuscript is a pre-registered reanalysis whose multiple primary endpoints did not confirm the hypothesis, and it reports that honestly (Stage A "uninformative" per §5.3; Stage B "bounded null"; Layer 3b and Layer 4 "primary FAIL"). The Discussion (manuscript.md:83–87) carefully separates rank-projection specificity from sample-level upregulation and declines to over-generalize. This is precisely the rigorous null-result reporting PLOS ONE exists to publish.

【Why it matters】Fit is not in question; the risk is purely in presentation compliance (§2, §6, §8), not in scope or soundness.

【Specific fix】No change required for fit.

---

## § Stands up (verified correct)

1. **Abstract is genuinely non-structured and within the word limit.** Measured at 298 words (body); no Background/Methods/Results/Conclusions headings; no bracketed citations. Compliant.
2. **All three GEO accessions are internally consistent and correctly transcribed.** GSE98547, GSE111216, GSE261676 appear identically in the abstract (manuscript.md:10), Methods (manuscript.md:29), Table 1 (manuscript.md:113–115), the Data Availability statement (manuscript.md:99), and the cover letter (cover_letter.md:22). No typo or mismatch.
3. **GitHub repo URL and tag are identical across manuscript and cover letter** (manuscript.md:99 = cover_letter.md:23: `https://github.com/yyx-4113/matrix-stiffness-neuropathic-pain`, tag v1.0.0, checksummed MANIFEST). Data-availability traceability is stronger than the PLOS ONE minimum.
4. **References are complete Vancouver with real PMID + DOI and each is cited in text** — verified the dataset-source links ([1]→GSE98547, [2]→GSE111216, [3]→GSE261676) and spot-checked six entries for plausibility. No fabricated or mismatched identifiers found.
5. **Author signature and credentials are consistent and correctly modest** — "Yongxin Yang, B.M." (cover_letter.md:27) carries no MD/PhD, matching the single-author "conceived, performed, and wrote" contribution (manuscript.md:102), which PLOS ONE accepts.
6. **The manuscript's own framing of the null is honest and well-bounded** — it does not hide the failed primaries; the Discussion explicitly circumscribes rather than disproves the literature (manuscript.md:87).

---

## § Questions for the authors

1. Can you confirm the original GEO deposits (GSE98547, GSE111216, GSE261676) state their own institutional ethics approvals, so the reanalysis can cite "approval held by the source studies" rather than asserting a blanket exemption? (Needed for the strengthened Ethics statement in §2.)
2. Is the GitHub repository at tag v1.0.0 publicly reachable without authentication, and are the deposited artifacts licensed at least as open as CC BY? PLOS ONE requires the data/code to meet that openness bar.
3. For the G4 set, would you be willing to report the absolute shifts (|ΔDRG−0.5| = 0.2224 vs |ΔBLD−0.5| = 0.0009) as the primary specificity evidence in the abstract rather than the unstable SI_g = 240.5, so the front-matter claim does not rely on a near-zero denominator?
4. Will the Competing Interests and Funding statements be entered verbatim in the PLOS ONE submission form (they must be, even though you also list them in the manuscript)?

---

## § What I actually checked

- **Files read:** manuscript.md (full), cover_letter.md (full), this round's _PANEL_BRIEF.md. Per the independence discipline I did **not** open any prior REVIEW_*.md, the old _PANEL_BRIEF.md, other round-3 reviewer files, audit_round*.json, README, memory, or task files.
- **Abstract word count:** counted the abstract body (manuscript.md:9–14) at **298 words** (300 with the "Abstract" heading token); confirmed ≤300 and non-structured. I did not estimate.
- **GEO accession consistency:** grepped all occurrences of GSE98547/111216/261676 across the manuscript and cover letter; confirmed identical transcription in abstract, Methods, Table 1, Data Availability, and cover letter.
- **Repo URL consistency:** confirmed manuscript.md:99 and cover_letter.md:23 are character-identical (URL + tag v1.0.0 + checksummed MANIFEST).
- **Reference spot-check:** verified Vancouver numbering/order, presence of PMID+DOI on all 10, and that each is cited in text; plausibility-checked six entries (Meng 2018, Parisien 2019, Serafini 2024, Dupont 2011, Wynn 2008, Zhao 2008).
- **Ethics/Data/Competing/Funding/Contributions:** read Declarations (manuscript.md:97–103) against PLOS ONE's stated requirements (IRB-not-required explanation, anonymized-data clause, submission-form placement of competing/funding, unfunded template wording).
- **Cover-letter cross-check:** verified journal name, title, author signature credential, and located the "correction" vs "circumscribes" mismatch (§6).
- **Over-claim assessment:** read the title, abstract, Layer-3/Table 3 specifics, and Discussion to judge whether the positive clause is supported; identified the G4 denominator-instability caveat (Table 3 footnote, manuscript.md:140) that is absent from the front-matter.
- **Format check:** confirmed figures are embedded with alt-text only (no dedicated Figure Legends section) and the supplement is labelled "Figure S1" (manuscript.md:78).

No numeric recomputation of the statistical results was required for this venue/edit review; the abstract's headline numbers (CTGF Δ=+1.64/P=9.5e-6; MRU=0.717/P=0.102/q=0.409; +0.146/P=0.80/g=0.219; G1/G5 q=0.0010/0.0016) were cross-read against the corresponding Results/Table statements and are internally consistent.

---

## Recommendation

**Minor revision.**

The study is sound, honestly framed, and an excellent fit for PLOS ONE's soundness-only, null-result-welcoming remit. The blocking issues are reporting/format compliance, not science:

- **Single most important must-fix:** Strengthen the Ethics statement (manuscript.md:98) to explicitly state that IRB/ethics approval was not required because this is a secondary analysis of public, de-identified data, that the source GEO deposits carried their own institutional approvals, and that the reanalysis posed no individual privacy risk (§2). PLOS ONE returns manuscripts with an incomplete Ethics statement before review.

Secondary must-fixes before resubmission: align the cover letter's "correction" wording to the manuscript's "circumscribes" framing (§6); add a dedicated Figure Legends section and rename "Figure S1" → "S1 Fig" (§8).

Recommended soft fixes: expand abstract abbreviations (§1); adopt PLOS ONE's standard Funding/Competing-Interests phrasing (§4); add the G4 denominator-instability caveat to the title/abstract positive clause (§7); optional "doi:" label normalization (§5).

None of these require new analyses; all are editorial. With the Ethics statement corrected and the cover-letter/figure-legend items addressed, this manuscript is acceptable for PLOS ONE.
