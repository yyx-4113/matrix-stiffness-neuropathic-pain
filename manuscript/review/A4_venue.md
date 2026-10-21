# A4 Venue — Reporting-honesty & format audit (first submission)

**Target venue:** GigaScience · **Article type claimed:** Research Article (computational reanalysis / methodological audit)
**Reviewer role:** A4 Venue — reporting honesty, internal consistency of the reframed conclusion, format/word/figure/table compliance, data-availability, Vancouver references, claim-strength red lines (protocol §11.2).
**Independence note:** I read only the manuscript, the frozen protocol, and the `analysis/results/**` artifact files. I treated the manuscript as a first submission and verified every headline number I cite against the source artifacts. Where the protocol text disagrees with its own frozen artifacts, I flag which side the data support.

---

## Part 1 — Internal consistency of the reframed conclusion (leftover over-claims)

### Finding 1 — MAJOR — The title still asserts *universal* specificity failure, contradicting the Layer-3 result and the manuscript's own reframed conclusion

**【Problem】** The manuscript title preserves the pre-registered, pre-data framing of "universal failure" verbatim, even though the actual Layer-3 data refuted that framing and the Discussion/Conclusions explicitly re-framed to "signature- and cell-type-specific failure."

**【Evidence】**
- Title, `manuscript.md:1`: *"Mechano-signatures do not transfer to pain transcriptomes: tissue specificity fails across five independent ECM and mechanotransduction gene sets."*
- Layer-3 result (the refuting data), `analysis/results/layer3/layer3_generality.json → per_set_specificity`: only **G2** (SI = 0.44) fails; **G1 = 38.4, G3 = 1.44, G4 = 240.5, G5 = 9.06** retain specificity. `n_sets_failing_specificity = 1 / 5`. `primary_endpoint_pass = false`.
- Manuscript's own Table 3 (`manuscript.md:130–138`) and Results (`manuscript.md:73`) agree: "Only 1/5 sets lacked specificity."
- Manuscript's own reframed conclusion, Discussion (`manuscript.md:85–92`): "established ECM/mechanotransduction gene sets retain tissue specificity in pain (4/5 DRG > blood)" and "the failure is signature- and cell-type-specific, not a universal property of projection statistics."
- The title is identical to the protocol's pre-registered work title, `PROTOCOL … md §11.1` (the "universal failure" core claim #2/#3 that the Layer-3 data disproved; see §12.6 / v0.7 reorientation).

**【Why it matters】** The title is the single most-read sentence. As written it (a) claims "tissue specificity fails across five independent … gene sets" — the direct opposite of Table 3 (only 1/5 failed); and (b) claims "Mechano-signatures do not transfer to pain transcriptomes" — an over-generalisation of the HD_up-specific null to "mechano-signatures" generally, when the data show established ECM/mechano sets *do* retain specificity/transfer (4/5 DRG > blood). This is precisely the "leftover over-claim" the panel was asked to hunt: the body honestly reframed, but the title did not. A reviewer or editor will read the title against Table 3 and flag the contradiction; at best it signals the authors did not reconcile the title after reorientation, at worst it looks like the universal-failure claim was quietly retained in the most prominent position.

**【Specific fix】** Replace the title so it matches the reframed conclusion, e.g.:

> *"A HEK293A-derived stiffness signature does not transfer to mouse pain transcriptomes, but established ECM/mechanotransduction gene sets retain tissue specificity"*

or, to stay close to the current wording while being honest:

> *"Cross-cell-type projection of a HEK293A stiffness program fails in pain tissues, while literature ECM/mechano signatures retain specificity"*

Either way the title must no longer say "tissue specificity fails across five independent … gene sets."

---

### Finding 2 — MINOR — Discussion narrative lumps the Layer-3 primary endpoint with the HD_up nulls as if all "did not confirm engagement"

**【Problem】** The first sentence of "What the data show" lists "Layer 3 primary" among endpoints that "did not confirm the hypothesised tissue-specific engagement of the projected stiffness program," which is imprecise: Layer-3's primary was a test of *universal specificity failure* across five independent sets, and its *failure to meet* that rule means established sets *retained* specificity — the opposite of "not engaging."

**【Evidence】** `manuscript.md:84–85`: "Three pre-specified primary endpoints (Stage A §5.3 verdict, Layer 3 primary, Layer 3b primary) and the Layer 4 primary did not confirm the hypothesised tissue-specific engagement of the projected stiffness program." The immediately following sentence (`manuscript.md:85`) correctly states Layer 3 "delivered the most substantive result … established ECM/mechanotransduction gene sets retain tissue specificity," so the two sentences are internally inconsistent in framing.

**【Why it matters】** Low risk, but it muddies the central reorientation and could be read as another residual universal-failure phrasing. It is a clarity defect, not a red-line violation.

**【Specific fix】** Rephrase the opening sentence to separate the HD_up projection endpoints from the Layer-3 benchmark, e.g.: "Three pre-specified endpoints concerning the projected HD_up program (Stage A §5.3 verdict, Stage B bounded null, Layer 3b divergence) and the Layer 4 descriptive endpoint did not confirm tissue-specific engagement of that program; separately, the Layer-3 generality benchmark failed its *universal-failure* rule, which — because only 1/5 sets lacked specificity — demonstrates retention of specificity rather than its absence."

---

## Part 2 — Word limits (protocol §11.3)

### Finding 3 — MINOR — Structured abstract exceeds the ≤350-word cap

**【Problem】** The structured abstract runs to ≈358 words (standard tokenization, counting numbers/units), ~8 words over the protocol-mandated ≤350 cap.

**【Evidence】** Word count of the Abstract block (`manuscript.md:8–17`, image captions excluded): total ≈358; approximate per-subsection — Background ≈60, Methods ≈105, Results ≈118, Conclusions ≈71. The body (Background→Declarations, excluding Tables, References, and figure-caption image lines) is ≈1,818 words, comfortably within the ≤4,000 cap.

**【Why it matters】** GigaScience enforces the structured-abstract word limit; an over-length abstract is a routine desk-reject/return-for-compliance item and is trivially fixable. The body limit is not at risk.

**【Specific fix】** Trim ~10 words, preferentially from the Methods or Results sentence. Example cuts: in Methods, drop "A pre-specified positive-control test (nerve-injury marker genes) was added to prove pipeline sensitivity, and a five-set tissue-specificity benchmark (Layer 3) was added to test generality beyond a single signature" → "A pre-specified positive-control test and a five-set tissue-specificity benchmark (Layer 3) were added." In Results, the clause "specificity index range 0.44–240.5" can be dropped (the range is in Table 3). Re-run a word count after editing to confirm ≤350.

---

## Part 3 — Figure/table completeness and data availability

### Finding 4 — MAJOR (blocker) — Data-availability statement is a placeholder: no real repository URL

**【Problem】** The Data availability statement promises "the project repository (named repository URL + tag v1.0.0)" but never names a repository or supplies a URL. Protocol §11.3 explicitly requires a *real* repository URL + tag + MANIFEST.

**【Evidence】** `manuscript.md:99`: "Analysis code, configuration, and all result artifacts are deposited at the project repository (named repository URL + tag v1.0.0) with a MANIFEST of checksums." The literal text "(named repository URL + tag v1.0.0)" is a template placeholder, not a URL. Protocol §11.3 (`PROTOCOL … md §11.3`): Data availability = "实名仓库 + tag + MANIFEST" (named repository + tag + MANIFEST).

**【Why it matters】** GigaScience (and most reproducible-biology venues) mandate a real, citable data/code repository with a version tag and a manifest; a placeholder is a hard compliance failure and will block acceptance regardless of scientific merit. The MANIFEST and tag are referenced but cannot be located by a reader. This is the most consequential formatting defect in the submission.

**【Specific fix】** Insert the actual repository URL (e.g., a Zenodo/Figshare/GitHub-archived DOI) in place of "(named repository URL + tag v1.0.0)", confirm the `v1.0.0` tag exists at that URL, and state the MANIFEST filename (e.g., `MANIFEST.json` with SHA-256 checksums). Example: "… deposited at Zenodo [DOI: 10.xxxx/zenodo.XXXXXXX], tag v1.0.0, with a SHA-256 MANIFEST (`MANIFEST.json`)."

---

### Finding 5 — MINOR — An unreferenced figure file exists (`fig2_member_contributions.png`)

**【Problem】** The figure directory contains a PNG that is never referenced in the manuscript, while the manuscript's Figure 2 is a different file. This is file hygiene, not a manuscript-text defect, but it can cause confusion at submission.

**【Evidence】** Referenced figures resolve to: `fig1_signature_derivation.png` (Fig 1), `fig2_per_animal_scores.png` (Fig 2), `fig3_member_contributions.png` (Fig 3), `fig4_matched_null.png` (Fig 4), `fig5_positive_control_vs_signatures.png` (Fig 5), `fig6_generality.png` (Fig 6), `figS1_layer3b_effects.png` (Fig S1) — all present under `analysis/results/layer2/fig/` and `analysis/results/layer3/fig/`. A separate file `analysis/results/layer2/fig/fig2_member_contributions.png` exists but is **not** referenced by any `![…](…)` caption in the manuscript.

**【Why it matters】** Submitting unreferenced artwork risks the wrong panel being typeset, or review questions about undisclosed analyses. The claimed figure set (6 main + 1 supplementary) is otherwise complete and every claimed figure is both present and referenced — that part **stands up**.

**【Specific fix】** Either delete `fig2_member_contributions.png` (it appears superseded by `fig3_member_contributions.png` and `fig2_per_animal_scores.png`), or, if a per-member HD_down contribution figure is intended as an additional panel, reference it explicitly. Confirm the final submission contains exactly the 7 referenced figures.

---

## Part 4 — Claim-strength red lines (protocol §11.2) and Vancouver references

### Finding 6 — COMPLIANT (reported as a positive check) — §11.2 red lines are respected

**【Problem】** (None — this is a confirmation that the manuscript honors the pre-specified claim-strength discipline.)

**【Evidence】**
- **HD_down is hypothesis-generating only:** `manuscript.md:64` — "HD_down reached a nominally significant but BH-non-significant (q = 0.086) reverse elevation … and is reported as hypothesis-generating only"; reinforced in Limitations, `manuscript.md:95` ("HD_down … reported as hypothesis-generating only"). Matches protocol §11.2 ("report HD_down as hypothesis-generating; never as a discovery").
- **Stage A is "uninformative," not "negative":** `manuscript.md:58–59` — "Stage A is uninformative, not merely 'negative.'" Verified against data: `layer1_diag.json` BLD_SNI matched q = 0.40916 = DRG_SNI matched q = 0.40916, so the §5.3 equal-significance verdict is correctly applied. (See Finding 7 for a stale protocol entry that does *not* reflect this.)
- **No "ECM unimportant" claim:** The reframed conclusion explicitly preserves the literature — `manuscript.md:16, 87, 92`: "Literature 'ECM enrichment in pain' findings are … not disproven"; "our result circumscribes their interpretation … without disproving them." No sentence asserts "ECM is unimportant in pain" or "original conclusions are wrong," both forbidden by §11.2.
- **No "program not activated" over-claim:** the HD_up null is consistently described as "bounded, sensitivity-validated null" (`manuscript.md:16, 91`), never "the program is absent."

**【Why it matters】** These are the exact red lines the panel must police. The manuscript passes them; this is credit to the author's adherence to the frozen protocol and should be acknowledged in the decision.

**【Specific fix】** None required.

---

### Finding 7 — MINOR — Protocol §8.1 contains a stale BLD value (q = 0.0072) that contradicts the actual matched-null output and the manuscript

**【Problem】** The protocol's Stage-A verdict table still records the blood negative control as two orders of magnitude more significant than DRG (BLD q = 0.0072), whereas the frozen artifact and the manuscript both show the *matched* BLD q = 0.409 — equal to DRG. The protocol text, not the manuscript, is the stale side here.

**【Evidence】** Protocol §8.1 table (`PROTOCOL … md §8.1`): "阴性对照 HD_up × BLD × SNI | 0.0009 | 0.0072" vs "主终点 DRG × SNI | 0.102 | 0.409." But `layer1_diag.json → stratified_vs_unstratified`, row `hippo_dependent_up / BLD / SNI`: `p_expression_matched = 0.10039`, `q_expression_matched = 0.40916` — exactly matching the manuscript (`manuscript.md:14, 59, 121`: MRU = 0.696, P = 0.100, q = 0.409). The §8.1 "0.0009 / 0.0072" figures correspond to the *unstratified* BLD result (which the manuscript correctly reports separately as the non-primary, confounded calibration, `manuscript.md:59`).

**【Why it matters】** A reviewer who cross-reads the protocol will see §8.1 say "blood two orders of magnitude stronger" while the manuscript says "equally significant," and may suspect the manuscript misreports. The data vindicate the manuscript; the protocol's §8.1 row is simply stale (it predates the corrected matched null, or conflates matched vs unstratified). This is a protocol-hygiene issue, not a manuscript defect, but it should be reconciled before the protocol is cited as supporting evidence.

**【Specific fix】** In protocol §8.1, correct the BLD row to the *matched* values (MRU = 0.696, P = 0.100, q = 0.409) and footnote that the older 0.0009/0.0072 figures refer to the unstratified calibration, which the manuscript reports separately as the confounded, non-primary endpoint.

---

### Finding 8 — COMPLIANT — All 10 Vancouver references are real and correctly formatted

**【Problem】** (None — verification result.)

**【Evidence】** All 10 references carry valid PMID/DOI and are Vancouver-formatted. I verified three by independent lookup against PubMed:
- **#10** Guan G, et al. *Genes (Basel)* 2023;14(2):272 — PMID **36833199**, DOI 10.3390/genes14020272 → confirmed on PubMed/PMC (exact match).
- **#3** Serafini RA, et al. *Neurobiol Pain* 2024;15:100153 — PMID **38549875**, DOI 10.1016/j.ynpai.2024.100153 → confirmed on PubMed (exact match; this is the GSE261676 source paper).
- **#9** Zhao B, et al. *Genes Dev* 2008;22(14):1962–1971 — PMID **18579750**, DOI 10.1101/gad.1664408 → confirmed on PubMed/EuropePMC (exact match; page range 1962–1971 as listed).
The remaining seven (#1 Meng 2018, #2 Parisien 2019, #4 Dupont 2011, #5 Naba 2016, #6 Coste 2010, #7 Wynn 2008, #8 Henderson 2020) are well-known, identifier-bearing citations and are each actually *used* in the text (datasets and gene-set sources), so none are decorative or orphaned. No fabricated or mismatched identifiers detected.

**【Why it matters】** Reference authenticity is a hard rule for this author; the list passes. This removes a common rejection risk.

**【Specific fix】** None. (Optional: confirm the DOI hyperlinks resolve at proof stage.)

---

## § Stands up — things I suspected but found correct

1. **Stage A "uninformative, not negative" framing is correct.** I initially thought the protocol's §8.1 "BLD two orders of magnitude stronger" might mean the manuscript under-reported; the artifact (`layer1_diag.json`) shows matched BLD q = 0.409 = DRG q = 0.409, so §5.3 equal-significance → uninformative is correctly applied. (See Finding 7 for the stale protocol entry.)
2. **Layer-3 specificity indices are exactly as reported.** G1 38.4, G2 0.44, G3 1.44, G4 240.5, G5 9.06; only 1/5 fails; 4/5 DRG > blood (only G2 has blood > DRG). Table 3 matches `layer3_generality.json` to 2–3 s.f.
3. **The "8/40 BH-significant, all DRG/SC/BRN, none in blood" claim is exact.** Recomputed from the 40-row table: 8 entries with q < 0.05, all in DRG/SC/BRN, zero in blood.
4. **HD_down is confined to hypothesis-generating language** throughout (Results, Limitations); no discovery framing. §11.2 respected.
5. **No "ECM unimportant / original conclusions wrong" claim appears** anywhere; the literature's ECM-enrichment findings are explicitly preserved.
6. **Body word count (≈1,818) is well within the ≤4,000 cap.**
7. **All 6 main figures + 1 supplementary are present and referenced** (the only stray file is the unreferenced `fig2_member_contributions.png` in Finding 5). All 3 tables (1–3) are present and referenced.
8. **Stage B bounded-null vs positive-control contrast is consistent.** HD_up diff = +0.146, P = 0.80, g = 0.219; positive control diff = +1.285, P = 0.0286, g = 3.85; the 17.6× g-gap is arithmetically correct (3.85 / 0.219 ≈ 17.6) and both run on identical code (`layer2_positive_control.json`).
9. **Layer 0 biological anchor is correct.** CTGF Δ = +1.64, P = 9.5 × 10⁻⁶; LATS confirmation 79.7% (HD) vs 28.6% (HI) — matches `layer0_signature.json`.
10. **Layer 3b and Layer 4 FAIL verdicts are faithfully reported** as under-powered/descriptive, not as "divergence disproven" or "ECM dominant" — matching `layer3b_sample_generality.json` (0/5 ECM sig up; g 0.31–1.13) and `layer4_positive_characterisation.json` (8/15,345 sig up; ECM-union sig up = 0; Fisher OR = 0, P = 1.0).
11. **All 10 references are authentic Vancouver entries**; three independently verified (Finding 8).

---

## § Questions for the authors

1. **Repository URL:** What is the real data/code repository URL, version tag, and MANIFEST filename that should replace the placeholder at `manuscript.md:99`? (Blocking — GigaScience requires this.)
2. **Title reconciliation:** Why was the pre-registered §11.1 title (universal-failure framing) kept verbatim after the Layer-3 reorientation? Will you adopt a reframed title per Finding 1?
3. **Protocol §8.1:** Will you correct the stale BLD q = 0.0072 entry so the protocol and the frozen artifact/manuscript agree (Finding 7)?
4. **Orphan figure:** Is `fig2_member_contributions.png` an abandoned draft, or was an additional per-member panel intended? Should it be deleted or referenced (Finding 5)?
5. **Abstract length:** After tightening to ≤350 words, please confirm the final count; do you want the suggested cuts or different ones (Finding 3)?
6. **Layer-3 narrative:** Do you accept the reframing of the Discussion opening sentence so it no longer lists "Layer 3 primary" among the HD_up "did not confirm engagement" endpoints (Finding 2)?

---

## § What I actually checked

**Files read**
- `manuscript/manuscript.md` (full text, all claims below pinned to line numbers).
- `PROTOCOL_基质刚度与神经病理性痛.md` §4, §5.3, §8.1, §9 (v0.4/v0.5/v0.6/v0.7 changelog), §10, §11.1, §11.2, §11.3, §12.6.
- `analysis/results/layer0/layer0_signature.json` (CTGF Δ/P, LATS confirmation, set sizes).
- `analysis/results/layer1/layer1_diag.json` (matched vs unstratified MRU/P/q for HD_up × DRG/BLD × SNI — the Stage A numbers).
- `analysis/results/layer2/layer2_positive_control.json` (positive control, HD_up, HD_down differences/P/Hedges g).
- `analysis/results/layer2/layer2_robustness.json` (Q4 matched null P = 0.092; LOO direction preserved).
- `analysis/results/layer3/layer3_generality.json` (all five SI values, 1/5 fail, 8/40 BH-significant breakdown).
- `analysis/results/layer3/layer3b_sample_generality.json` (0/5 ECM sig up; g range; positive control g = 3.85, P = 0.0286).
- `analysis/results/layer4/layer4_positive_characterisation.json` (15,345 tested; 8 sig up; ECM-union sig up = 0; Fisher OR = 0, P = 1.0).
- Glob of `analysis/results/**/fig/*.png` (7 referenced figures present + 1 orphan).

**Values recomputed / verified against the manuscript**
- Stage A: MRU/ P/ q for DRG×SNI (0.717 / 0.102 / 0.409) and BLD×SNI (0.696 / 0.100 / 0.409) — match `layer1_diag.json` exactly.
- Stage B: HD_up (diff +0.146, P 0.80, g 0.219), positive control (diff +1.285, P 0.0286, g 3.85), HD_down (diff +0.397, P 0.0286, q 0.086, g 2.658) — all match `layer2_positive_control.json`; 17.6× g-gap arithmetic confirmed.
- Layer 3: SI G1 38.4, G2 0.44, G3 1.44, G4 240.5, G5 9.06; 1/5 fail; 8/40 BH-significant (all DRG/SC/BRN, none blood) — match `layer3_generality.json`.
- Layer 3b: 0/5 ECM sig up; g 0.31–1.13; positive control g 3.85, P 0.0286 — match artifact.
- Layer 4: 8/15,345 sig up; ECM-union sig up = 0; Fisher OR = 0, P = 1.0 — match artifact.
- Layer 0: CTGF Δ +1.64, P 9.5 × 10⁻⁶; LATS 79.7% vs 28.6% — match artifact.
- Word counts: abstract ≈358 (over 350 cap); body ≈1,818 (within 4,000).
- References: 3 of 10 independently verified via PubMed (PMID/DOI exact match); remaining 7 identifier-bearing and each used in text.

**Discrepancies / items to flag**
- Manuscript title (`manuscript.md:1`) contradicts Table 3 and the reframed Discussion/Conclusions → Finding 1 (MAJOR).
- Data-availability URL is a placeholder (`manuscript.md:99`) → Finding 4 (MAJOR/blocker).
- Abstract over the 350-word cap by ~8 words → Finding 3 (MINOR).
- Unreferenced figure file present → Finding 5 (MINOR).
- Protocol §8.1 BLD q = 0.0072 is stale vs the actual matched null (q = 0.409) and the manuscript; the manuscript is correct, the protocol text needs reconciliation → Finding 7 (MINOR).
- Discussion opening sentence mis-groups the Layer-3 primary with HD_up nulls → Finding 2 (MINOR).

**No fabricated references, no "ECM unimportant" claim, no HD_down-as-discovery framing, and no mislabeled Stage-A "negative" verdict were found.**
