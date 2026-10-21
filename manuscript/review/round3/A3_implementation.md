# Reviewer A3 — Implementation & Provenance audit

**Manuscript:** "A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity"
**Role:** Implementation / Provenance (trace every headline number to a deposited source file and recompute what is recomputable).
**Discipline:** Independent first-read. I did not consult prior review rounds, the old panel brief, the author's self-audit, README, memory, or the other three reviewers' files. Every numeric claim I challenge was re-derived from the deposited JSONs I was permitted to read.

---

## Executive summary

I traced the eight mandatory headline numbers plus every figure in Tables 2, 3, and 4 back to the frozen result JSONs. **Every headline number is supported by the deposited artifacts** — I found no fabricated, unsupported, or internally inconsistent value. The signature sizes, the CTGF contrast, both Stage A MRUs, both Stage B effects, the positive-control effect, all five Layer-3 specificity indices, the Layer-3 BH-q values, and the Layer-4 8/15345 count all reproduce to the printed precision from the JSONs. This is a strong provenance result.

The issues I raise below are therefore **transparency / reproducibility-hygiene** problems, not numerical errors: one double-rounding trap in Table 3 (G4) that a reader will hit if they re-derive SI from the printed columns; two divergent definitions of "unstratified P" in Stage A that live in different files; a deposit gap (CTGF Δ is confirmed only against the deposited contrast, not against raw FPKM); and an abstract that clears the 300-word ceiling by exactly two words. None invalidate a conclusion, but each should be tightened before acceptance.

---

## Provenance ledger (every headline number, recomputed/retrieved vs the manuscript)

| # | Manuscript claim | Source file : location | Recomputed / retrieved value | Verdict |
|---|---|---|---|---|
| 1 | CTGF Δ = +1.64, P = 9.5×10⁻⁶ | `layer0_signature.json` `positive_control_canonical_targets.CTGF` (lines 136–145) | delta_WT = 1.6405 → **+1.64**; p_WT = 9.4940×10⁻⁶ → **9.5×10⁻⁶** | ✅ |
| 2 | HD_up n = 18 | `layer0_signature.json` `sets.hippo_dependent_up` (lines 38–57) | counted **18** members | ✅ |
| 3 | HD_down n = 41 | `layer0_signature.json` `sets.hippo_dependent_down` (lines 58–100) | counted **41** members | ✅ |
| 4 | LATS confirmation 79.7% HD vs 28.6% HI | `layer0_signature.json` `lats_confirmation_fraction` (lines 33–36) | 0.79661 → **79.7%**; 0.28571 → **28.6%** | ✅ |
| 5 | Stage A DRG×SNI HD_up MRU=0.717, P=0.102, q=0.409 | `layer1_diag.json` `stratified_vs_unstratified` DRG/SNI/HD_up (lines 228–238) | MRU 0.71677, p_expr_matched 0.10229, q 0.40916 | ✅ |
| 6 | Stage A BLD×SNI HD_up MRU=0.696, P=0.100, q=0.409 | `layer1_diag.json` BLD/SNI/HD_up (lines 184–194) | MRU 0.6964, p_expr_matched 0.10039, q 0.40916 | ✅ |
| 7 | Unstratified DRG P=0.597, BLD P=0.0009 | `layer1_results.json` DRG/SNI/HD_up primary (line 2391) & BLD/SNI/HD_up neg-control (line 2214) | p_perm 0.59674, 0.0009 | ✅ |
| 8 | Stage B HD_up +0.146, P=0.80, g=0.219 | `layer2_results.json` `primary_saline_arm` (lines 39,42); g in `layer2_positive_control.json` `stiffness_HD_up.hedges_g` (line 115) | diff 0.14645, p_exact 0.8, g 0.2187 | ✅ |
| 9 | Positive control +1.285, P=0.0286, g=3.85 | `layer2_positive_control.json` `POSITIVE_CONTROL_injury_up` (lines 54–59) | diff 1.28536, p 0.028571, g 3.8535 | ✅ |
| 10 | Layer 3 G1 SI=38.4, G2 0.44, G3 1.44, G4 240.5, G5 9.06 | `layer3_generality.json` `per_set_specificity` (lines 28–57) | 38.4159 / 0.44024 / 1.4379 / 240.472 / 9.0547 | ✅ |
| 11 | Table 3 MRU cells (G1–G5, DRG & BLD) | `layer3_generality.json` `per_set_specificity.MRU_target/_negative_blood` | 0.9056/0.5106, 0.6180/0.7681, 0.8040/0.7114, 0.7224/0.4991, 0.8857/0.4574 | ✅ |
| 12 | G1 q=0.0010, G5 q=0.0016 | `layer3_generality.json` `table` DRG/SNI rows (lines 78, 92, 540, 554) | q 0.0009999, 0.0015998 | ✅ |
| 13 | Layer 3: 8/40 BH-significant, all DRG/SC/BRN, blood 0 | `layer3_generality.json` `n_surviving_BH_0.05`=8, `n_tests`=40 (lines 62–63) | confirmed by hand-count of q<0.05 rows in `table` | ✅ |
| 14 | Layer 4: 8/15345 up, 3 down, ECM-union sig-up=0, OR=0, P=1.0 | `layer4_positive_characterisation.json` (lines 10–21) | n_genes_tested 15345, n_sig_up_q05 8, n_sig_dn_q05 3, ecm_union n_sig_up_q05 0, fisher_OR 0.0, fisher_P 1.0 | ✅ |
| 15 | Table 4 (all 7 rows) | `layer3b_sample_generality.json` `table` (lines 24–113) | G1 0.513/0.229/0.839/0.440; G2 0.174/0.657/0.310/0.767; G3 −0.277/0.286/−0.823/0.440; G4 0.393/0.171/1.131/0.440; G5 0.371/0.314/0.766/0.440; HD_up 0.146/0.800/0.219/0.800; PC 1.285/0.0286/3.853/0.200 | ✅ |
| 16 | HD_up coverage 0.611, 11/18 expressed | `layer2_results.json` `n_present_after_filter`=11, `coverage_rate`=0.6111 (lines 12–13) | 11/18 = 0.611 | ✅ |
| 17 | HD_down +0.397, P=0.0286, g=2.658, q=0.086 | `layer2_results.json` HD_down `primary_saline_arm` (lines 118,121,125); g `layer2_positive_control.json` line 194 | diff 0.39671, p 0.028571, g 2.6584, q 0.085713 | ✅ |
| 18 | Abstract ≤300 words, non-structured | `manuscript.md` lines 10–14 | **298** whitespace-delimited words; no Background/Methods/Results/Conclusions labels | ✅ (margin thin) |

---

## 【Problem 1】 Table 3's printed 4-d.p. |Δ| columns cannot reproduce the printed SI for G4 (double-rounding trap), and a reader who re-derives SI from the table gets 247.1, not 240.5.

**【Evidence】** `manuscript.md` Table 3 (lines 137, 140): G4 lists |ΔDRG−0.5| = 0.2224 and |ΔBLD−0.5| = 0.0009, with SI_g = 240.5. The full-precision values in `layer3_generality.json` `per_set_specificity.G4_actin_rho_rock` (lines 46–50) are |ΔDRG−0.5| = 0.22239618 and |ΔBLD−0.5| = 0.00092483, giving SI = 0.22239618 / 0.00092483 = **240.47** → 240.5 (correct). But 0.2224 / 0.0009 (the rounded table columns) = **247.1**, a 2.7% overstatement. The authors add a footnote (line 140) acknowledging "the |Δ| columns are rounded to 4 d.p. and will not exactly reproduce SI by division," which is honest, but the table as printed still invites the wrong recomputation and does not state the actual denominator.

**【Why it matters】** PLOS ONE and most readers verify SI by dividing the two printed |Δ| columns. For G4 the printed denominator rounds to 0.0009, which is the *only* cell where 4-d.p. rounding moves the leading digit of the ratio materially (the denominator is ~1×10⁻³, so 4-d.p. truncates it by ~3%). A reviewer replicating from the table concludes "240.5 is wrong; it should be 247" and may flag a numerical error where none exists. The current footnote is easy to miss because it sits below the table.

**【Specific fix】** Keep SI_g computed from full precision (already correct), but (a) report G4's |ΔBLD−0.5| to ≥6 d.p. (0.000925) or add the full-precision denominator in the footnote next to the ratio, and (b) reword the footnote from "will not exactly reproduce" to: *"SI_g is computed from full-precision MRU; for G4 the denominator |MRU(BLD,SNI)−0.5| = 0.000925, so SI_g = 0.222396/0.000925 = 240.5. Do not recompute SI from the 4-d.p. |Δ| columns."*

---

## 【Problem 2】 "Unstratified P" in Stage A has two different meanings in two deposited files; the manuscript cites only one, so a reader checking `layer1_diag.json` sees conflicting numbers.

**【Evidence】** `manuscript.md` line 57 states the unstratified full-background calibration gave "DRG P = 0.597 and BLD P = 0.0009." These match `layer1_results.json` (DRG/SNI/HD_up primary `p_permutation` = 0.59674 at line 2391; BLD/SNI/HD_up negative_control `p_permutation` = 0.0009 at line 2214). However, `layer1_diag.json` also carries a field `p_unstratified` for the *same* signature/tissue/model in its `stratified_vs_unstratified` block — DRG/SNI/HD_up `p_unstratified` = 0.055394 (line 235) and BLD/SNI/HD_up `p_unstratified` = 0.085491 (line 191). That is a third, different P (matched-space but unstratified permutation). So three P values coexist for "DRG×SNI HD_up unstratified": 0.597 (manuscript, full background), 0.055 (diag unstratified), and 0.102 (diag expression-matched, the actual primary). The manuscript is internally consistent about which one it means, but nothing in the text tells the reader that the diag file's `p_unstratified` is *not* the number being cited.

**【Why it matters】** A provenance reviewer (or the editor's statistician) who opens `layer1_diag.json` to verify Stage A will find `p_unstratified` = 0.055 for DRG and 0.085 for BLD, conclude the manuscript's 0.597/0.0009 are unsupported, and raise a false-positive error — or, worse, suspect the 0.597/0.0009 were cherry-picked. The discrepancy is purely semantic (different null spaces), but the deposit does not make that legible.

**【Specific fix】** In Methods (Stage A, around `manuscript.md` line 35) add one sentence: *"The unstratified comparison cited in Results uses the full-background null in `layer1_results.json`; `layer1_diag.json` additionally reports a matched-space unstratified P (HD_up DRG×SNI = 0.055, BLD×SNI = 0.085), which is a different null and is not the value reported."* Optionally rename the diag field to `p_matchedspace_unstratified` to remove the collision.

---

## 【Problem 3】 CTGF Δ is confirmed only against the deposited WT contrast, not recomputed from raw FPKM; the raw FPKM needed to independently reproduce it is not in the deposited artifacts.

**【Evidence】** `manuscript.md` line 52 (and abstract line 10, discussion line 83, conclusions line 90) anchor the signature with "CTGF Δ = +1.64, P = 9.5 × 10⁻⁶." The deposited `layer0_signature.json` `positive_control_canonical_targets.CTGF` (lines 136–145) reports `delta_WT` = 1.6405 and `p_WT` = 9.4940×10⁻⁶, which I confirm round correctly to the printed values. But `delta_WT` is itself a *product* of an upstream step (log2(FPKM+1) contrast within WT, then Welch test); the raw per-replicate FPKM for WT_1kPa and WT_40kPa are not present in any JSON I was permitted to read, and `layer0_diagnostics.json` only records the detection rule (FPKM > 1.0 in ≥6/24) and row counts. I could therefore verify the *deposited* contrast, not regenerate it from primary data.

**【Why it matters】** The brief's mandate (a)(ii) is to "recompute CTGF Δ from `layer0_signature.json` FPKM." The file does not contain FPKM; it contains the already-computed `delta_WT`. This is a deposit-completeness gap, not a numerical error — but it means the single most-emphasized biological anchor (repeated four times in the manuscript) is one step removed from independent reproducibility. If the upstream script had a sign or log-transform bug, the JSON would inherit it silently.

**【Specific fix】** Either (a) deposit the 24×2 per-genotype mean log2(FPKM+1) vectors (or the WT 1kPa/40kPa replicates) for the eight canonical targets so Δ can be regenerated by `1.6405 − 0`, or (b) add to Declarations/Data availability a statement that raw FPKM for the anchor genes are deposited at ⟨location⟩ and that `delta_WT` in `layer0_signature.json` is the regenerated value. Explicitly: *"CTGF Δ = +1.64 = mean log2(FPKM+1)|40kPa − mean log2(FPKM+1)|1kPa over WT replicates (n=3 each); source values deposited in ⟨file⟩."*

---

## 【Problem 4】 The abstract clears the PLOS ONE 300-word ceiling by exactly two words (298), leaving no headroom for copy-editing.

**【Evidence】** `manuscript.md` lines 10–14, three narrative paragraphs, no Background/Methods/Results/Conclusions subheadings (so the non-structured requirement is met). Whitespace-delimited word count = **298** (hyphenated compounds such as "extracellular-matrix", "neuropathic-pain", "Hippo-dependent", "cell-type-specific" counted as single words, consistent with PLOS ONE's counter). It is compliant, but the margin is 2 words.

**【Why it matters】** Compliance is binary at submission, but any later editorial request to add a clarifying clause (e.g., the G4 denominator caveat, or a sentence on the unstratified semantics from Problems 1–2) would push the abstract over 300 and force a cut elsewhere. More importantly, PLOS ONE's manuscript checker will flag borderline counts and ask the author to certify; a 2-word margin invites a needless query and a last-minute scramble that could introduce new errors.

**【Specific fix】** No change required for acceptance, but I recommend trimming ~10–15 words now to create headroom, e.g., condense the third paragraph: *"Using a sensitivity-validated pipeline we show the HEK293A-derived stiffness program does not transfer to pain tissues (bounded, sensitivity-validated null). The failure is signature- and cell-type-specific, not a universal projection artifact: once baseline-expression confounding is controlled, established ECM/mechanotransduction gene sets retain tissue specificity (4/5; G1, G5 significant), circumscribing — not disproving — literature 'ECM enrichment in pain' to the source cell type."* This drops the abstract to ~283 words.

---

## § Stands up (verified correct — things I suspected but confirmed)

1. **Signature sizes are real, not rounded estimates.** I counted the actual member lists in `layer0_signature.json` (`sets.hippo_dependent_up` lines 38–57 = 18; `sets.hippo_dependent_down` lines 58–100 = 41) rather than trusting `set_sizes`. Both match the manuscript exactly, and the 18/41 split is consistent with `counts.hippo_class` (hippo_dependent = 59 total, of which 18 up + 41 down).

2. **Stage A matched MRU/q values are exactly the pre-specified primary, not a re-labelled unstratified number.** I confirmed `layer1_diag.json` DRG/SNI/HD_up `MRU_stratified_space` = 0.71677, `p_expression_matched` = 0.10229, `q_expression_matched` = 0.40916 (lines 228–238) — i.e., the manuscript's 0.717/0.102/0.409 are the *expression-matched* endpoint the protocol froze, distinct from the full-background 0.560/0.597 that the authors correctly demote to "not the primary endpoint" (line 57). The governance logic (blood q = 0.409 = target q = 0.409 ⇒ uninformative) is arithmetically sound on the deposited numbers.

3. **The positive-control effect is computed by the identical code path as HD_up, exactly as claimed.** `layer2_positive_control.json` runs `POSITIVE_CONTROL_injury_up` and `stiffness_HD_up` through the same scoring/permutation fields: both report `difference`, `p_exact_permutation`, `welch_p`, `mann_whitney_p`, `hedges_g` (lines 54–59, 108–115). The g-gap is 3.8535 / 0.2187 = **17.62×**, matching the manuscript's "17.6-fold Hedges-g gap" (line 62). The sensitivity argument (a real DRG signal is detected at g≈3.85 while HD_up is null at g≈0.22 on identical code) is supported by the artifacts.

4. **Layer 3 specificity verdict is correctly derived.** `layer3_generality.json` `n_sets_failing_specificity` = 1 (lines 59–60) and `per_set_specificity` shows only G2 `specificity_failed` = true (line 38); the other four have SI > 1. The "1/5 failed, ≥4/5 rule not met, specificity retained" conclusion (manuscript line 71, 83) is a faithful reading of the JSON. The "4/5 shifted more in DRG than blood" statement is also correct: |ΔDRG−0.5| > |ΔBLD−0.5| for G1, G3, G4, G5 (Table 3 lines 134–138).

5. **Layer 4's negative characterization is clean.** `layer4_positive_characterisation.json`: 8 up / 3 down of 15345 tested; ECM-union (G1/G4/G5, 133 members, 123 present) contributes 0 significant-up (fisher_OR 0.0, fisher_P 1.0, lines 14–21); HD_up members 0 significant-up (lines 69–73). The "ECM not dominant in the descriptive landscape" claim is directly supported.

---

## § Questions for the authors (I do not assume the answers)

1. **Raw FPKM for the anchor genes.** Can you deposit the per-replicate WT 1kPa/40kPa FPKM (or the mean log2(FPKM+1) vectors) for CTGF/CYR61/ANKRD1/AMOTL2 so the +1.64 contrast can be regenerated from primary data, not just read from `delta_WT`? (Problem 3.)

2. **Unstratified P semantics.** Was the `p_unstratified` field in `layer1_diag.json` (0.055 DRG / 0.085 BLD) ever intended to be shown to readers, or is it purely internal? If internal, would you rename it to avoid collision with the manuscript's cited 0.597/0.0009? (Problem 2.)

3. **G4 denominator presentation.** Do you agree the Table 3 footnote should state the actual full-precision denominator (0.000925) so the 240.5 is not mis-reproduced as 247 from the 4-d.p. columns? (Problem 1.)

4. **HD_down promotion.** You report HD_down as "hypothesis-generating only" with q = 0.086 (BH-non-significant) but P = 0.0286. The `layer2_results.json` `q_BH_family_of_4` = 0.085713 (line 125) is within a 4-test family. Is the BH family of 4 (HD_up, HD_down, HI_down, and one other) the intended correction, and is q = 0.086 the value you stand behind? I found it consistent, but please confirm the family definition.

5. **Layer 3b "positive control BH q = 0.200".** Table 4 lists the positive control at BH q = 0.200 across the family of 7, while its raw P = 0.0286. This is correct BH behaviour (only the positive control is significant, so its q ≈ P×(7/1) capped at family max), but it looks odd next to Stage B's "g = 3.85 PASS." Can you add a one-line note that the 0.200 is the 7-set BH adjustment and does not contradict the Stage B sensitivity pass?

---

## § What I actually checked

**Files read (permitted by the brief):**
- `manuscript/manuscript.md` (full) — abstract (lines 10–14), Layer 0 (52), Stage A (56–57), Stage B (61–62), Layer 3 (70–71, 83), Layer 4 (75–76), Tables 1–4 (109–154), Declarations (97–103).
- `analysis/results/layer0/layer0_signature.json` (full) — CTGF block (136–145), set sizes (23–32), member lists (38–100), LATS fractions (33–36).
- `analysis/results/layer0/layer0_diagnostics.json` (full) — detection rule and per-file row counts; confirmed the deposit describes the detection filter (FPKM > 1.0 in ≥6/24), so the signature is built on a defensible expressed set.
- `analysis/results/layer1/layer1_diag.json` (full) — `stratified_vs_unstratified` block (184–238) for the two HD_up primary/negative-control contrasts; also noted the divergent `p_unstratified` values (191, 235).
- `analysis/results/layer1/layer1_results.json` — located the full-background primary (DRG/SNI/HD_up, lines 2376–2410, p_permutation 0.59674 at 2391) and negative_control (BLD/SNI/HD_up, lines 2199–2256, p_permutation 0.0009 at 2214) that the manuscript cites as "unstratified."
- `analysis/results/layer2/layer2_results.json` (full) — HD_up `primary_saline_arm` (36–47), HD_down (115–126).
- `analysis/results/layer2/layer2_positive_control.json` (full) — positive control (30–78) and stiffness_HD_up (79–134) effect sizes and g.
- `analysis/results/layer3/layer3_generality.json` (full) — `per_set_specificity` (28–57), `n_surviving_BH_0.05`=8 / `n_tests`=40 (62–63), and the 40-row `table` (65–626) used to verify G1/G5 q and the 8/40 claim.
- `analysis/results/layer3/layer3b_sample_generality.json` (full) — the 7-row `table` (22–114) used to verify every cell of Table 4.
- `analysis/results/layer4/layer4_positive_characterisation.json` (full) — n_genes_tested, sig counts, ecm_union Fisher, hd_up/positive_control contributions (10–78).

**Computations I performed:**
- Counted the HD_up (18) and HD_down (41) member lists by hand from the JSON arrays.
- Recomputed every SI_g from full-precision MRU in `per_set_specificity`: 38.4159, 0.44024, 1.4379, 240.472, 9.0547 → match printed 38.4/0.44/1.44/240.5/9.06.
- Recomputed SI from the *printed* 4-d.p. |Δ| columns to expose the G4 double-rounding trap (0.2224/0.0009 = 247.1 ≠ 240.5).
- Hand-counted the 40-row Layer-3 `table` for q < 0.05: 8 survivors, all in DRG/SC/BRN, none in BLD — matches the manuscript's "8/40 … blood 0."
- Verified all seven Table 4 rows against `layer3b_sample_generality.json` `table` to 3–4 d.p. (diff, P, g, BH q all match).
- Counted the abstract at 298 whitespace-delimited words and confirmed the absence of structured subheadings.

**Values recomputed by me vs the manuscript's, with discrepancy stated:**
- CTGF Δ: recomputed 1.6405 ↔ manuscript +1.64 → **no discrepancy** (rounding only).
- Stage A DRG×SNI HD_up: 0.71677 / 0.10229 / 0.40916 ↔ 0.717 / 0.102 / 0.409 → **no discrepancy**.
- Stage B HD_up: 0.14645 / 0.8 / 0.2187 ↔ +0.146 / 0.80 / 0.219 → **no discrepancy**.
- Positive control: 1.28536 / 0.028571 / 3.8535 ↔ +1.285 / 0.0286 / 3.85 → **no discrepancy**.
- Layer 3 SI set: all five match to printed precision → **no discrepancy**.
- Layer 4: 8/15345, 3 down, ECM-union 0, OR 0, P 1.0 ↔ identical → **no discrepancy**.
- G4 from printed |Δ| columns: 247.1 ↔ printed 240.5 → **discrepancy of 6.6**, but it is a rounding artifact of the printed columns, not of the underlying SI (full-precision SI = 240.47). Flagged as Problem 1.
- Abstract word count: 298 ↔ manuscript asserts ≤300 → **no discrepancy** (2-word margin).

**Key finding:** No headline number in the manuscript is unsupported by the deposited JSONs. The only numerical "discrepancy" (G4) is a table-presentation artifact already footnoted by the authors; the remaining items are provenance/transparency improvements (Problems 1–4) that do not alter any conclusion.
