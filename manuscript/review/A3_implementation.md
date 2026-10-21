# A3 — Implementation Audit: numeric traceability Layer 0 → Layer 4

**Reviewer role:** A3 Implementation (independent recomputation auditor)
**Manuscript:** `manuscript/manuscript.md`
**Protocol:** `PROTOCOL_基质刚度与神经病理性痛.md` (v0.4)
**Result artifacts audited:** `analysis/results/**`
**Status:** First submission, treated as unreviewed. Every number below was recomputed independently from the raw JSON artifacts and compared against the manuscript text. No prior review material was consulted.

---

## 1. Headline verdict

The manuscript's numeric claims are **fully traceable and internally consistent** with the result artifacts. I found **no fabricated, stale, or mismatched numbers** anywhere in Layers 0–4. The protocol's earlier, corrected-away Hedges-g values (HD_down = 3.057, positive-control = 4.431, HD_up = 0.252) are **not** used; the manuscript uses the post-R13 corrected values. The one structural weakness is **presentation/traceability hygiene**, not arithmetic: (a) two headline results (HD_up, positive control) are re-reported across Stage B and Layer 3b with identical numbers, and (b) two result files the manuscript depends on (`layer1_results.json`, `layer2_results.json`) sit outside the brief's mandatory source-data list, so a reader following the brief alone cannot verify two cited numbers.

This is an important distinction for the panel: a numeric audit can return "clean" while a reproducibility audit still has actionable items. The three Findings below are of the second kind — they improve verifiability and reader clarity but do not require any number in the manuscript to change. I have separated them explicitly from any claim of error so the editorial decision can be made on that basis.

---

*Scope note: I did not consult any other reviewer's output, any REVIEW_/RESPONSE_/REVISION_ file, or the submission manifest, per the brief's independence discipline. All judgements derive from the manuscript text and the JSON artifacts I read and recomputed myself. Where I cite a protocol section, it is from the frozen protocol I read directly.*

## Findings at a glance

| # | Issue | Severity | Numeric discrepancy? | Recommended action |
|---|---|---|---|---|
| 1 | HD_up & positive control re-reported in Stage B and Layer 3b (identical numbers) | Minor (presentation) | No | Cross-reference or label as repeated |
| 2 | Two cited numbers depend on files outside the brief's source list (`layer1_results.json`, `layer2_results.json`) | Minor (traceability) | No (values correct) | Add to MANIFEST / traceability register |
| 3 | Layer 3b 7-row table defined by protocol but never printed | Minor (visibility) | No (data correct in JSON) | Print the table |

**Bottom line for the panel:** The implementation layer is arithmetically sound. Every numeric claim I was asked to verify traces to a JSON artifact and matches it. There are no fabricated, stale, or mismatched figures. The recommendations are about *presentation hygiene and traceability documentation*, not about correcting wrong numbers. A reader can trust the arithmetic; the panel's biology reviewers should focus their scrutiny on the *interpretation* of the Layer-3 reframing rather than on whether the numbers support the text (they do).

---

## 2. Per-layer verification narrative

This section walks the audit end-to-end so the discrepancy table below can be read against a documented trail. I treated the JSON artifacts as the ground truth and the manuscript as the claim under test; where the two disagreed I treated it as a defect, and where the manuscript cited a number absent from the brief's seven-file list I searched the wider `analysis/results/` tree for its provenance.

**Layer 0 (signature derivation).** The Hippo-dependent partition yields HD_up = 18 and HD_down = 41, which the manuscript quotes verbatim. The LATS confirmation fractions (HD 0.7966 → 79.7%; HI 0.2857 → 28.6%) are reported as percentages and round correctly. The CTGF canonical-target positive control (Δ = 1.6405, P = 9.494 × 10⁻⁶) is the biological anchor; CYR61/ANKRD1/AMOTL2 (0.99/1.43/1.38) are also present and correctly transcribed. No issue.

**Stage A (expression-matched calibration, §5.3).** The matched-null endpoint for DRG×SNI HD_up is MRU 0.71677, P 0.10229, q 0.40916; the BLD×SNI negative control is MRU 0.6964, P 0.10039, q 0.40916. The two q-values are identical to four decimal places, which is precisely the condition that triggers the protocol's §5.3 "uninformative" governance rule. The manuscript's claim that the blood control is "statistically indistinguishable" is therefore arithmetically exact, not rhetorical. The unstratified diagnostic (DRG 0.597, BLD 0.0009) is a separate, explicitly non-pre-specified contrast and is correct where it lives (see Finding 2).

**Stage B (sample-level 4-vs-4, Layer 2).** HD_up: difference 0.14645, exact P 0.8, Hedges g 0.2187, coverage 0.6111 (11/18). HD_down: 0.39671, 0.028571, 2.6584, with q 0.085713 from the family-of-4 BH. Positive control: 1.28536, 0.028571, 3.8535. The g-gap 3.8535/0.2187 = 17.62 ≈ 17.6 as stated. Q4 matched null P = 0.092091 ≈ 0.092. All consistent.

**Layer 3 (generality benchmark).** Five SI values recomputed to 38.42, 0.440, 1.438, 240.47, 9.055 — faithfully rounded to 38.4/0.44/1.44/240.5/9.06. Exactly 1/5 fail (G2). Of 40 tests, 8 survive BH (q<0.05); on full recomputation those 8 are in DRG/SC/BRN with zero in blood, matching the manuscript's "8/40 … all in DRG/SC/BRN with none in blood." The 4/5 "DRG ≥ blood" pattern is directly visible in the SI values (four ≥ 1).

**Layer 3b (sample-level divergence).** All seven rows reproduce exactly. The five ECM sets have P-values 0.229/0.657/0.286/0.171/0.314 — none below 0.05, so "0/5 sig up" is correct. The stated Hedges-g range 0.31–1.13 matches G2 (0.310) through G4 (1.131). HD_up and the positive control rows are numerically identical to their Stage B counterparts (same GSE261676 saline-arm computation), which is the basis for Finding 1.

**Layer 4 (positive characterisation).** 15 345 genes tested, 8 sig-up (q<0.05), 3 sig-down. ECM-union (G1/G4/G5) contributes 0 sig-up genes with Fisher OR = 0, P = 1.0. HD_up members contribute 0 sig-up. All match the JSON.

---

## 3. Discrepancy table (claim → manuscript → JSON → match?)

### Layer 0 — signature derivation
| Claim | Manuscript | JSON artifact | Match |
|---|---|---|---|
| HD_up n | 18 | `layer0_signature.json` set_sizes.hippo_dependent_up = 18 | ✅ |
| HD_down n | 41 | set_sizes.hippo_dependent_down = 41 | ✅ |
| LATS confirmation HD | 79.7% | lats_confirmation_fraction.hippo_dependent = 0.7966 | ✅ |
| LATS confirmation HI | 28.6% | lats_confirmation_fraction.hippo_independent = 0.2857 | ✅ |
| CTGF Δ | +1.64 | positive_control_canonical_targets.CTGF.delta_WT = 1.6405 | ✅ |
| CTGF P | 9.5 × 10⁻⁶ | CTGF.p_WT = 9.494 × 10⁻⁶ | ✅ |
| CYR61 / ANKRD1 / AMOTL2 Δ | +0.99 / +1.43 / +1.38 | 0.9926 / 1.4263 / 1.3845 | ✅ |

### Stage A — expression-matched calibration (§5.3)
| Claim | Manuscript | JSON artifact | Match |
|---|---|---|---|
| DRG×SNI HD_up MRU / P / q | 0.717 / 0.102 / 0.409 | `layer1_diag.json` DRG SNI hippo_dependent_up: MRU 0.71677, p_expr_matched 0.10229, q 0.40916 | ✅ |
| BLD×SNI HD_up MRU / P / q | 0.696 / 0.100 / 0.409 | BLD SNI: MRU 0.6964, p 0.10039, q 0.40916 | ✅ |
| §5.3 "blood equally significant" | q_BLD = q_DRG | both 0.40916 | ✅ (framing valid) |
| Unstratified diagnostic DRG P | 0.597 | `layer1_results.json` DRG SNI HD_up p_permutation = 0.59674 | ✅ (see Issue 2) |
| Unstratified diagnostic BLD P | 0.0009 | `layer1_results.json` BLD SNI HD_up p_permutation = 0.0009 | ✅ (see Issue 2) |
| Baseline-zero fractions DRG/BLD/SC/BRN | 42.8 / 58.5 / 41.0 / 40.5 % | `layer1_diag.json` per_contrast pct_baseline_zero: 42.77 / 58.478 / 40.948 / 40.46 | ✅ |
| KS D ≈ 0.49 throughout | ~0.49 | per_contrast KS_D range 0.488–0.505 | ✅ |

### Stage B — sample-level 4-vs-4 (Layer 2)
| Claim | Manuscript | JSON artifact | Match |
|---|---|---|---|
| HD_up diff / P / g | +0.146 / 0.80 / 0.219 | `layer2_positive_control.json` stiffness_HD_up: 0.14645 / 0.8 / 0.2187 | ✅ |
| HD_up coverage | 0.611 (11/18) | coverage_rate 0.6111, n_present_after_filter 11 | ✅ |
| HD_down diff / P / g / q | +0.397 / 0.0286 / 2.658 / 0.086 | diff 0.39671, p 0.028571, g 2.6584 (`layer2_positive_control`); **q 0.085713** (`layer2_results.json`) | ✅ |
| Positive control diff / P / g | +1.285 / 0.0286 / 3.85 | 1.28536 / 0.028571 / 3.8535 | ✅ |
| Positive control Mann–Whitney P | 0.0286 | mann_whitney_p 0.028571 | ✅ |
| 17.6-fold g-gap | 17.6× | 3.8535 / 0.2187 = 17.62 | ✅ |
| Q4 expression-matched null P | 0.092 | `layer2_robustness.json` Q4 p_empirical 0.092091 | ✅ |

### Layer 3 — generality benchmark
| Claim | Manuscript | JSON artifact | Match |
|---|---|---|---|
| SI G1 / G2 / G3 / G4 / G5 | 38.4 / 0.44 / 1.44 / 240.5 / 9.06 | per_set_specificity: 38.42 / 0.4402 / 1.4379 / 240.47 / 9.0547 | ✅ |
| Fail count | 1/5 | n_sets_failing_specificity = 1, n_sets_tested = 5 | ✅ |
| BH survivors | 8 / 40 | n_tests 40, n_surviving_BH_0.05 8 | ✅ |
| 8/40 all DRG/SC/BRN, blood 0 | as stated | recomputed: 8 q<0.05, tissues {DRG, SC, BRN}, BLD among them = 0 | ✅ |

### Layer 3b — sample-level divergence (7-row table)
| Set | Manuscript (prose summary) | JSON `layer3b_sample_generality.json` | Match |
|---|---|---|---|
| G1 n/diff/P/g | (not printed) | 62 / 0.513 / 0.229 / 0.839 | ✅ data present |
| G2 n/diff/P/g | (not printed) | 12 / 0.174 / 0.657 / 0.310 | ✅ data present |
| G3 n/diff/P/g | (not printed) | 22 / −0.277 / 0.286 / −0.823 | ✅ data present |
| G4 n/diff/P/g | (not printed) | 20 / 0.393 / 0.171 / 1.131 | ✅ data present |
| G5 n/diff/P/g | (not printed) | 21 / 0.371 / 0.314 / 0.766 | ✅ data present |
| HD_up n/diff/P/g | 11 / 0.146 / 0.80 / 0.219 | 11 / 0.146449 / 0.8 / 0.2187 | ✅ |
| Positive control | 12 / 1.285 / 0.0286 / 3.85 | 12 / 1.28536 / 0.028571 / 3.853 | ✅ |
| Stated g-range 0.31–1.13 | 0.31–1.13 | min 0.310 (G2), max 1.131 (G4) | ✅ |
| 0/5 ECM sig up | 0/5 | all 5 ECM P > 0.05 (0.229/0.657/0.286/0.171/0.314) | ✅ |

### Layer 4 — positive characterisation
| Claim | Manuscript | JSON artifact | Match |
|---|---|---|---|
| n_genes_tested | 15 345 | `layer4_positive_characterisation.json` n_genes_tested = 15345 | ✅ |
| n_sig_up (q<0.05) | 8 | n_sig_up_q05 = 8 | ✅ |
| n_sig_down (q<0.05) | 3 | n_sig_dn_q05 = 3 | ✅ |
| ECM-union sig-up | 0 (Fisher OR = 0, P = 1.0) | ecm_union.n_sig_up_q05 0, fisher_OR 0.0, fisher_P 1.0 | ✅ |
| HD_up members sig-up | 0 | hd_up_members.n_sig_up_q05 0 | ✅ |

### Stale-value guard (protocol §10.6 R13)
| Old (rejected) value | Manuscript uses | Correct? |
|---|---|---|
| HD_down g = 3.057 | 2.658 | ✅ avoids stale |
| Positive control g = 4.431 | 3.85 / 3.853 | ✅ avoids stale |
| HD_up g = 0.252 | 0.219 | ✅ avoids stale |

### Double-counting / redundancy check
| Overlap | Finding | Numeric discrepancy? |
|---|---|---|
| HD_up in Stage B (`layer2_positive_control`) vs Layer 3b (`layer3b_sample_generality`) | identical numbers (diff 0.14645 vs 0.146449; g 0.2187 vs 0.2187; P 0.8 both) | ❌ none — same computation |
| Positive control in Stage B vs Layer 3b | identical numbers (diff 1.28536 both; g 3.8535 vs 3.8535; P 0.028571 both) | ❌ none — same computation |

### Markdown integrity
All three printed tables (manuscript lines 111, 119, 132) are column-consistent (6/6, 5/5, 7/7 columns; no ragged rows). **No broken markdown table syntax found.**

---

## 4. Findings (4-part format)

### Finding 1 — Redundant re-reporting of HD_up and positive control across Stage B and Layer 3b
【Problem】The exact same two computations (HD_up 4-vs-4 and the positive-control 4-vs-4) appear in two separate "layers" of the manuscript with identical numbers, which can read as two independent confirmations rather than one result reported twice.

【Evidence】`layer2_positive_control.json` → `results.stiffness_HD_up` {difference 0.14645, p_exact_permutation 0.8, hedges_g 0.2187} is numerically identical to `layer3b_sample_generality.json` → table row HD_up {diff_saline_arm 0.146449, p_exact_saline_arm 0.8, hedges_g 0.2187}. The positive control is identical between the two files as well (1.28536 / 0.028571 / 3.8535). Manuscript reports these in both the Stage B section (lines 63–64) and the Layer 3b section (line 78). The numbers are the same GSE261676 saline-arm 4-vs-4 computation.

【Why it matters】Protocol §13.4 explicitly requires the three pre-specified conclusions (Stage B HD_up bounded-null, positive-control PASS, Layer-3 primary FAIL) and the post-hoc Layer-3b divergence observation to be "reported in tiers, not merged." Presenting HD_up and the positive control as rows inside the Layer-3b 7-set table alongside five novel ECM sets makes the table look like 7 independent tests, potentially diluting the distinction between a pre-specified sensitivity result and the Layer-3b divergence test. It is not a numeric error, but it is a presentation hazard that could confuse a careful reader about what is "new" in Layer 3b.

【Specific fix】In the Layer 3b presentation, either (a) drop the HD_up and positive-control rows from the 7-set table and cross-reference them to Stage B ("values identical to Stage B, same GSE261676 saline-arm computation"), or (b) add an explicit column/note labelling those two rows "repeated from Stage B (identical computation)" so the reader does not count them as 7 independent novel tests. State plainly that the Layer-3b novelty is the five ECM/mechano sets.

### Finding 2 — Traceability map incomplete: two cited numbers depend on files outside the brief's mandatory source list
【Problem】Two numbers the manuscript cites cannot be found in the seven result files the review brief listed as mandatory reading; they live in `layer1_results.json` and `layer2_results.json`, which were not in that list.

【Evidence】Stage A prose (manuscript line 59) cites an unstratified diagnostic "DRG P = 0.597 and BLD P = 0.0009." These values are absent from `layer1_diag.json` (which instead carries the matched values 0.102/0.100) and are found only in `analysis/results/layer1/layer1_results.json` (DRG SNI HD_up p_permutation 0.59674; BLD SNI HD_up p_permutation 0.0009). Separately, the HD_down row's q = 0.086 is found only in `analysis/results/layer2/layer2_results.json` (hippo_dependent_down q_BH_family_of_4 = 0.085713); the rest of that row's statistics come from `layer2_positive_control.json`. Both extra files exist and contain the correct values, so this is a documentation gap, not a fabrication.

【Why it matters】Protocol §11.4 mandates that every manuscript number be locatable in a results artifact, and the Data availability statement claims "every numeric claim … is traceable to a file under `analysis/results/`." That claim is true in substance, but a reviewer or reader following the brief's seven-file list literally could not locate the unstratified 0.597/0.0009 or the HD_down q = 0.086. Traceability must be demonstrable from the documented set, not merely exist somewhere on disk.

【Specific fix】Add `layer1_results.json` and `layer2_results.json` to the Data availability MANIFEST / traceability register (or cite them explicitly where the unstratified diagnostic and HD_down q are introduced), so the full provenance of every printed number is self-evident from the manuscript's own reference list.

### Finding 3 — Layer 3b 7-row table is defined by protocol but never printed in the manuscript
【Problem】Protocol §13.2 defines the Layer-3b output as a 7-set table (set, n, diff, P, Hedges g, q), and the JSON artifact contains exactly those columns, but the manuscript prints only a prose summary of Layer 3b (g-range 0.31–1.13; positive-control and HD_up values restated). The five ECM sets' individual n/diff/P/g/q are invisible on the page.

【Evidence】`layer3b_sample_generality.json` → `table` holds 7 rows with the full statistics; manuscript line 78 reports only "0/5 ECM sets were significantly upregulated (Hedges g 0.31–1.13; positive control g = 3.85, P = 0.0286; HD_up g = 0.219, P = 0.80)." The per-set numbers (e.g., G4 diff 0.393, P 0.171, g 1.131; G3 diff −0.277, P 0.286, g −0.823) are traceable but not shown.

【Why it matters】A reader cannot independently verify the "0/5 sig up" claim or the g-range statement without opening the JSON. For a reproducibility-focused venue (GigaScience), the absence of the printed 7-row table weakens the audit trail for the Layer-3b primary endpoint, even though the underlying data are correct and present in the artifact.

【Specific fix】Print the 7-row Layer-3b table (columns: set, n present, diff, exact P, Hedges g, q_BH) as a manuscript table (or a clearly labelled supplementary table). This satisfies protocol §13.2 and closes the only visibility gap in the numeric chain.

---

## 5. §Stands up (things I suspected but found correct)

1. **The reframing is honest, not a silent flip.** I expected the "signature-specific failure" conclusion to be a post-hoc rationalisation smuggled in. It is not: the manuscript Discussion (line 73, 85) explicitly states "we could *not* demonstrate that specificity failure is universal" and "the pre-specified primary rule (≥ 4/5 failing) was **not** met." This matches the protocol §12.6 downgrade instruction and is reported as a FAIL, not relabelled as a win. Three pre-specified primaries (Stage A §5.3, Layer 3, Layer 3b, Layer 4) are all openly reported as not-confirmed.

2. **§5.3 "uninformative not negative" is arithmetically defensible.** I recomputed and confirmed BLD q (0.40916) equals DRG q (0.40916); the negative control is *exactly* as significant as the target, so the protocol's governance rule (cannot attribute tissue specificity) is correctly applied. The manuscript does not over-claim a "null" here — it correctly calls Stage A uninformative.

3. **The "universal specificity failure" hypothesis was genuinely falsified by the data, not massaged.** I verified all five SI values independently: G1 38.42, G2 0.440, G3 1.438, G4 240.47, G5 9.055. Four of five exceed 1 (DRG shift ≥ blood), confirming 1/5 failed, not 4/5. The manuscript's 38.4 / 0.44 / 1.44 / 240.5 / 9.06 are faithful rounded transcriptions. The 8/40 BH-surviving tests are, on recomputation, all in DRG/SC/BRN with zero in blood — exactly as claimed.

4. **HD_down is correctly quarantined as hypothesis-generating.** Its P = 0.0286 is nominally significant but q = 0.086 (BH family of 4), and the manuscript labels it "hypothesis-generating only" and "reverse elevation," consistent with protocol §11.2 (report HD_down as hypothesis-generating, never as a discovery). No red line is crossed.

5. **Stale Hedges-g values were purged.** I specifically checked for the protocol §10.6 R13 rejected values (HD_down 3.057, positive control 4.431, HD_up 0.252). The manuscript uses 2.658, 3.85, and 0.219 respectively — the corrected post-R13 numbers. No stale figure survived into the text.

6. **The positive control is genuinely independent of the signature (no circularity).** The protocol required the 12-gene nerve-injury marker set to share zero members with the stiffness signature and to be selected from literature only. I confirmed the intersection is empty in the artifact, and the positive-control genes (ATF3, SPRR1A, GAL, NPY, SOX11, GAP43, NGFR, VGF, STMN4, BASP1, MMP9, TIMP1) do not overlap the HD_up/HD_down member lists. Its detection (g = 3.85, P = 0.0286) therefore legitimately validates pipeline sensitivity rather than re-confirming the stiffness program.

7. **Rounding is conservative, never upward-biased.** Across every compared value, the manuscript rounds away from significance where ambiguity exists (e.g., q 0.40916 → 0.409; P 0.10229 → 0.102; g 0.2187 → 0.219) and never rounds a non-significant value into a significant-looking one. The only "friendly" rounding is the g-gap 17.62 → 17.6, which is downward. This pattern is consistent with honest reporting rather than number-shaping.

8. **Layer 4's "FAIL" is reported without spin.** The manuscript states plainly that of 15 345 tested genes only 8 were sig-up and the ECM-union contributed 0, and that this primary endpoint FAILED. The Fisher OR = 0 / P = 1.0 for ECM enrichment is reported verbatim, including its null result, rather than being omitted. This satisfies the protocol's requirement that Layer 4 be reported as a descriptive, hypothesis-generating failure.

### Note on the core-tension reframing (implementation scope only)
The brief's central tension is whether re-framing "universal specificity failure" (protocol §11.1 claim #3) as "signature/cell-type-specific failure" is scientifically defensible. As the implementation auditor my remit is numeric traceability, not adjudicating the biological claim. I will note only two implementation-relevant facts: (i) the reframed conclusion is **not** accompanied by any new or re-computed number that departs from the artifacts — it is an interpretation of the same SI values (four of five ≥ 1) already present in `layer3_generality.json`; and (ii) the manuscript explicitly labels the reframing as a FAIL of the pre-specified primary rule and as post-hoc/hypothesis-generating where required by protocol §12.6 and §13.4, so the reframing is at minimum *honestly signposted*. Whether four-of-five retaining specificity justifies the strong "circumscribes the literature" conclusion is a scientific-judgement question for the panel's biology reviewers, not a numeric defect.

---

## 6. §Questions for the authors

1. **Layer 3b independence:** Given that HD_up and the positive control in Layer 3b are literally the same GSE261676 saline-arm 4-vs-4 numbers as Stage B, what is the added inferential value of including them as rows in the Layer-3b table beyond the cross-reference already made in Stage B? Would it be cleaner to present Layer 3b as the five *novel* ECM/mechano sets only?

2. **HD_down q provenance:** The HD_down row mixes its diff/P/g (from `layer2_positive_control.json`) with its q = 0.086 (from `layer2_results.json`). Is the BH family-of-4 the intended correction for HD_down, and should that family be named explicitly in the Methods so the q is self-documenting?

3. **Unstratified diagnostic status:** The unstratified 0.597/0.0009 (full-background) numbers are presented as "a separate, non-pre-specified unstratified calibration." Since they come from `layer1_results.json` and directly contrast with the matched 0.102/0.100, can you add a one-line pointer to that artifact so the diagnostic is verifiable from the manuscript's own citations?

4. **Layer 3b table:** Will you add the printed 7-row Layer-3b table (or move Figure S1's underlying numbers into a supplementary table) so the "0/5 sig up" and g-range claims are on the page rather than only in JSON?

---

## 7. §What I actually checked

**Files read (primary):**
- `manuscript/manuscript.md` — full text, all tables.
- `PROTOCOL_基质刚度与神经病理性痛.md` — §4, §5.3, §8.1, §10.6 (R13), §11.1–11.2, §12, §13, §14.
- `analysis/results/layer0/layer0_signature.json`
- `analysis/results/layer1/layer1_diag.json`
- `analysis/results/layer1/layer1_results.json` (located during audit; not in brief list)
- `analysis/results/layer2/layer2_positive_control.json`
- `analysis/results/layer2/layer2_robustness.json`
- `analysis/results/layer2/layer2_results.json` (located during audit; not in brief list)
- `analysis/results/layer3/layer3_generality.json`
- `analysis/results/layer3/layer3b_sample_generality.json`
- `analysis/results/layer4/layer4_positive_characterisation.json`

**Values recomputed independently (vs manuscript):**
- Layer 0: HD_up=18, HD_down=41; LATS HD 0.7966→79.7%, HI 0.2857→28.6%; CTGF Δ 1.6405, P 9.494e-6.
- Stage A: DRG×SNI MRU 0.71677/P 0.10229/q 0.40916; BLD×SNI MRU 0.6964/P 0.10039/q 0.40916; §5.3 equality of q confirmed.
- Stage B: HD_up 0.14645/0.8/0.2187/coverage 0.6111; HD_down 0.39671/0.028571/2.6584 (q 0.085713 from layer2_results); positive control 1.28536/0.028571/3.8535; g-gap 17.62; Q4 0.092091.
- Layer 3: five SI values (38.42, 0.440, 1.438, 240.47, 9.055); fail 1/5; 8/40 BH survivors; verified all 8 in {DRG,SC,BRN}, zero in BLD.
- Layer 3b: all 7 rows reproduced; confirmed 0/5 ECM P>0.05; g-range 0.310–1.131 matches stated 0.31–1.13.
- Layer 4: 15345 tested, 8 sig-up, 3 sig-down, ECM-union sig-up 0 (OR 0, P 1.0), HD_up sig-up 0.

**Hunts performed:**
- **Double-counting:** HD_up and positive control appear in both Stage B and Layer 3b with identical numbers (same GSE261676 computation). No numeric discrepancy, but flagged as a presentation redundancy (Finding 1).
- **Broken markdown:** All three printed tables column-consistent; none broken.
- **Manuscript number absent from JSON:** None. Every printed number was located in a JSON artifact (two required files outside the brief's list — Finding 2).
- **JSON number that changed but manuscript didn't:** None found; manuscript matches all current artifact values.
- **Stale values:** Confirmed the manuscript does NOT use the protocol §10.6 R13 rejected values (3.057, 4.431, 0.252); it uses the corrected 2.658, 3.85, 0.219.

**Discrepancies stated:** No arithmetic or factual discrepancies. Three presentation/traceability issues (Findings 1–3) are recommended fixes, not errors. The implementation layer is sound; the remaining risk is reader-facing clarity, not numeric integrity.

### Verification checklist (all passed)
| Check | Result |
|---|---|
| Every Layer-0/1/2/3/3b/4 headline number located in a JSON | ✅ |
| Manuscript number not present in any artifact | none found |
| Artifact value changed but manuscript not updated | none found |
| Manuscript uses protocol §10.6 R13 rejected Hedges-g (3.057/4.431/0.252) | no — uses 2.658/3.85/0.219 |
| §5.3 "blood equally significant" arithmetically true | ✅ (q_BLD = q_DRG = 0.40916) |
| HD_down stays hypothesis-generating (never promoted to discovery) | ✅ |
| Layer-3 primary correctly reported as FAIL (1/5, not 4/5) | ✅ |
| Broken markdown table syntax | none (3 tables, all column-consistent) |
| Double-counting as a *numeric* discrepancy | none (HD_up & positive control identical across Stage B/Layer 3b, same computation) |
| Positive-control circularity | none (0 member overlap with signature) |

### Files that the manuscript depends on but the brief did not list
- `analysis/results/layer1/layer1_results.json` — source of unstratified Stage-A diagnostic (DRG P 0.597, BLD P 0.0009).
- `analysis/results/layer2/layer2_results.json` — source of HD_down q = 0.086 (q_BH_family_of_4 = 0.085713).

Both contain the correct values and exist under `analysis/results/`, so the Data-availability claim holds in substance; they should be added to the documented traceability set (Finding 2).
