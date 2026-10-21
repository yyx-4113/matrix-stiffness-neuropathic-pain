# Implementation / Provenance Audit — Round 5 (independent)

**Manuscript:** `manuscript/manuscript.md` (de-AI polished version)
**Auditor role:** Independent implementation/provenance reviewer on a blind panel
**Independence note:** I treated the manuscript as a fresh submission and verified every headline number against the ground-truth JSON outputs and generating scripts in `analysis/results/` and `analysis/scripts/`, plus the frozen protocol `PROTOCOL_基质刚度与神经病理性痛.md`. I did not consult any prior review/response files.

---

## Headline verdict

**No expression drift was introduced by the polish.** Every number listed in the round brief is (a) still present in the manuscript and (b) matches the value I recomputed from the source JSONs to the stated precision. No digit was altered or dropped. The only item that fails the round brief's own numeric targets is the abstract length (303 words vs the ≤300 ceiling in the brief; still within the protocol's ≤350 ceiling). See § "Critical drift check" and § "What I actually checked."

---

## Findings

### F1 — Layer-0 signature sizes and biological anchor are internally consistent
【Problem】 The polish must preserve HD_up n=18 / HD_down n=41 and the CTGF/CYR61/ANKRD1/AMOTL2 anchor values.
【Evidence】 `layer0_signature.json`: `set_sizes.hippo_dependent_up = 18`, `hippo_dependent_down = 41`. `positive_control_canonical_targets`: CTGF `delta_WT = 1.6405`, `p_WT = 9.494e-6`; CYR61 `0.9926`; ANKRD1 `1.4263`; AMOTL2 `1.3845`. Manuscript line 10/52 reports HD_up 18, HD_down 41, CTGF Δ=+1.64 (P=9.5×10⁻⁶), CYR61 +0.99, ANKRD1 +1.43, AMOTL2 +1.38 — all match to 2–3 s.f. LATS confirmation `lats_confirmation_fraction.hippo_dependent = 0.7966`, `.hippo_independent = 0.2857` → manuscript line 32 "79.7% … 28.6%" ✓.
【Why it matters】 These are the load-bearing biological claims; any rounding slip would undermine the "biologically anchored" framing used throughout.
【Specific fix】 None required.

### F2 — Stage A matched-null values and the three-P contrast set are exact
【Problem】 Stage A DRG×SNI HD_up MRU=0.717, P=0.102, q=0.409 and BLD MRU=0.696, P=0.100, q=0.409 must match the matched-null JSON, and the three P-value families must be correctly attributed.
【Evidence】 `layer1_diag.json` `stratified_vs_unstratified`: HD_up×DRG×SNI `MRU_stratified_space = 0.71677`, `p_unstratified = 0.055394`, `p_expression_matched = 0.10229`, `q_expression_matched = 0.40916`; HD_up×BLD×SNI `MRU = 0.6964`, `p_unstratified = 0.085491`, `p_expression_matched = 0.10039`, `q = 0.40916`. `layer1_results.json` (full-background, unstratified): HD_up×DRG×SNI `p_permutation = 0.59674`; HD_up×BLD×SNI `p_permutation = 0.0009`. Manuscript line 56–57 reports MRU 0.717/0.696, P 0.102/0.100, q 0.409; full-background unstratified DRG 0.597/BLD 0.0009; diagnostic unstratified DRG 0.055/BLD 0.085; expression-matched DRG 0.102/BLD 0.100 — all match.
【Why it matters】 This is the most statistic-heavy contrast in the paper and the §5.3 governance hinge; misattribution of the three P families (full-background vs diagnostic-unstratified vs expression-matched) would constitute a serious error.
【Specific fix】 None required. The three-calibration discipline is preserved verbatim.

### F3 — Stage B HD_up, positive control, and HD_down all match
【Problem】 Stage B HD_up diff=+0.146, P=0.80, g=0.219, coverage 0.611, 11/18; positive control diff=+1.285, P=0.0286, g=3.85, MW P=0.0286; HD_down diff=+0.397, P=0.0286, g=2.658, q=0.086.
【Evidence】 `layer2_results.json` HD_up `difference = 0.14645`, `p_exact_permutation = 0.8`, `coverage_rate = 0.6111`, `n_present_after_filter = 11`/`n_human_members = 18`; `layer2_positive_control.json` HD_up `hedges_g = 0.2187`, positive control `difference = 1.28536`, `p_exact_permutation = 0.028571`, `hedges_g = 3.8535`, `mann_whitney_p = 0.028571`, HD_down `difference = 0.39671`, `p_exact_permutation = 0.028571`, `hedges_g = 2.6584`, `q_BH_family_of_4 = 0.085713`. Manuscript line 10/62/Table 2/Table 4 matches every figure. 17.6-fold gap = 3.8535 / 0.2187 = 17.62 ✓ (line 62, 189, 83).
【Why it matters】 The "sensitivity-validated null" conclusion rests entirely on these exact values and the gap.
【Specific fix】 None required.

### F4 — Layer 3 SI_g values, BH count, G1/G5 overlap, and denominator artefacts all verify
【Problem】 SI_g G1 38.4, G2 0.44, G3 1.44, G4 240.5, G5 9.06; 8/40 BH-significant; G1∩G5 = 10 members (43% of G5's 23); G4 blood MRU≈0.5 / |Δ|≈0.0009; G1 |ΔBLD−0.5|=0.0106; G1 q=0.0010, G5 q=0.0016 (DRG×SNI).
【Evidence】 `layer3_generality.json` `per_set_specificity` SI: 38.4159 / 0.4402 / 1.4379 / 240.4721 / 9.0547 → match to stated precision. `n_surviving_BH_0.05 = 8`, `n_tests = 40`. G1 DRG×SNI `q_matched_BH40 = 0.0009999` ≈ 0.0010; G5 DRG×SNI `0.0015998` ≈ 0.0016. G4 `MRU_negative_blood = 0.499075`, table `abs_shift` BLD×SNI `0.000925` ≈ 0.0009; G1 BLD×SNI `abs_shift = 0.010558` ≈ 0.0106. I independently recomputed the membership overlap from `analysis/config/ms_panel.json`: G1 = 64 members, G5 = 23 members, intersection = exactly 10 (`COL1A1, FN1, LOX, LOXL1, LOXL2, SERPINE1, SPP1, TIMP1, TIMP2, TIMP3`); 10/23 = 43.5% ≈ 43%. Manuscript abstract/results/discussion/Table 3/Table 3 footnote all match.
【Why it matters】 The overlap and denominator-artefact disclosures are the paper's central honesty checks; a dropped digit here would overstate the "4/5 pass" tally.
【Specific fix】 None required.

### F5 — Table 3 (MRU) and Table 4 (sample-level rows) reproduce the JSONs exactly
【Problem】 Every cell in Tables 3 and 4 must equal the source JSON.
【Evidence】 `layer3_generality.json` `per_set_specificity` MRU_target/MRU_negative_blood: G1 0.9056/0.5106, G2 0.6180/0.7681, G3 0.8040/0.7114, G4 0.7224/0.4991, G5 0.8857/0.4574 — match manuscript Table 3 (lines 136–140). `layer3b_sample_generality.json` table rows for G1–G5/HD_up/positive control (n, diff, p_exact, hedges_g, q_BH_family_of_7) match manuscript Table 4 (lines 148–154) to the digit, including HD_up `0.146/0.800/0.219/0.800` and positive control `1.285/0.0286/3.853/0.200`.
【Why it matters】 Tables are the most copy-error-prone section during a polish.
【Specific fix】 None required.

### F6 — Layer 3b and Layer 4 verdicts and counts verify
【Problem】 Layer 3b: 0/5 ECM sets significant; positive control g=3.85, P=0.0286; HD_up g=0.219, P=0.80. Layer 4: 15 345 genes tested, 8 sig up / 3 down, ECM-union 0 sig-up, Fisher OR=0, P=1.0.
【Evidence】 `layer3b_sample_generality.json` `conditions.a_ecm_significant_up_ge3 = false` (0/5), positive control `diff 1.28536, p 0.028571, g 3.8535`, HD_up `g 0.2187, p 0.8`. `layer4_positive_characterisation.json`: `n_genes_tested = 15345`, `n_sig_up_q05 = 8`, `n_sig_dn_q05 = 3`, `ecm_union.n_sig_up_q05 = 0`, `fisher_OR = 0.0`, `fisher_P = 1.0`. Manuscript line 76 matches. (Note: manuscript line 76 writes "15 345" with a thin space; `15345` is the numeric value — consistent.)
【Why it matters】 These are the "FAIL" primary endpoints that justify the conservative interpretation.
【Specific fix】 None required.

### F7 — Discussion line 83 "passed with full separation" is consistent with Stage B / Figure 5 "detected at the exact-permutation lower bound," NOT an overstatement
【Problem】 Determine whether the Discussion's "passed with full separation" conflicts with / overstates the Stage B and Figure 5 wording ("detected at the exact-permutation lower bound," P=0.0286, g=3.85).
【Evidence】 Recomputed from `layer2_positive_control.json` `per_animal` (saline arm): SNI scores = +0.78141, +0.60048, +0.28647, +0.36740 (all strictly positive); sham scores = −1.23742, −0.51799, −0.83764, −0.51264 (all strictly negative). The two groups do not overlap at all → literal *full separation* in the saline arm. The exact two-sided permutation lower bound for 4-vs-4 is 2 / C(8,4) = 2/70 = 0.028571, which equals the observed `p_exact_permutation = 0.028571` and `mann_whitney_p = 0.028571`. Thus "full separation" and "detected at the exact-permutation lower bound (P=0.0286, g=3.85)" are two descriptions of the *same* event.
【Why it matters】 A reader could read "full separation" as a stronger, unsourced claim; in fact it is the precise consequence of reaching the 2/70 bound and is already in the Stage B/Figure 5 text. No contradiction, no exaggeration.
【Specific fix】 None required. Optionally, to pre-empt a reviewer, add a one-line note in Discussion that "full separation" means all four saline-arm SNI scores exceeded all four sham scores (the configuration that yields the 2/70 bound). This is clarification only.

### F8 — Abstract word count is 303, above the round brief's ≤300 ceiling (still within protocol ≤350)
【Problem】 The round brief asks to confirm Abstract ≤300 words.
【Evidence】 Word count of the Abstract body (manuscript lines 10–14) = 303 words (verified by two independent counts). The frozen protocol §11.3 sets the Abstract ceiling at ≤350 words, so 303 is protocol-compliant. The round brief's context states the abstract was "trimmed to 289 words"; I measure 303, a 14-word difference from that stated target.
【Why it matters】 If 300 is a hard house limit for this round it fails; if the protocol's 350 governs, it passes. Either way the abstract is not bloated (it is near the lower end of the protocol range).
【Specific fix】 If a strict 300-word ceiling is required, delete ~4–5 words (e.g., trim "with an experimentally controlled mechanical driver," or "at the 4-vs-4 resolution" in the conclusions paragraph). If 350 governs, no change needed.

### F9 — §5.3 governance rule correctly characterized and correctly NOT triggered
【Problem】 The §5.3 rule ("equally significant control → cannot attribute") must be described accurately and its (non-)triggering must be right given both DRG and BLD are non-significant.
【Evidence】 Frozen protocol §5.3: "若阴性对照与主终点同等显著，则结论不得成立." Manuscript line 35/57: the rule triggers "only when a negative control is equally significant to the target"; since DRG q=0.409 and BLD q=0.409 are *both non-significant and statistically indistinguishable*, the rule does not apply and Stage A is a "plain double-null." This is the correct application — the rule is about an *equally significant* (i.e., significant) control, and here the control is equally *non*-significant, which is a different, correctly-handled situation.
【Why it matters】 Mis-stating §5.3 as "triggered" would have forced a different (and wrong) conclusion.
【Specific fix】 None required.

---

## Critical drift check (explicit)

I recomputed, from the raw JSONs, every value enumerated in the round brief and compared to the manuscript:

| Brief item | Recomputed from JSON | Manuscript | Match |
|---|---|---|---|
| HD_up 18 / HD_down 41 | 18 / 41 | 18 / 41 | ✓ |
| CTGF Δ+1.64, P 9.5e-6; CYR61 +0.99; ANKRD1 +1.43; AMOTL2 +1.38 | 1.6405/9.494e-6; 0.9926; 1.4263; 1.3845 | same | ✓ |
| LATS 79.7% / 28.6% | 0.7966 / 0.2857 | same | ✓ |
| Stage A DRG MRU 0.717, P 0.102, q 0.409; BLD 0.696, P 0.100, q 0.409 | 0.71677/0.10229/0.40916; 0.6964/0.10039/0.40916 | same | ✓ |
| 3 P-sets (0.597/0.0009; 0.055/0.085; 0.102/0.100) | 0.59674/0.0009; 0.055394/0.085491; 0.10229/0.10039 | same | ✓ |
| Stage B HD_up +0.146, P 0.80, g 0.219, cov 0.611, 11/18 | 0.14645/0.8/0.2187/0.6111/11-18 | same | ✓ |
| Positive control +1.285, P 0.0286, g 3.85; MW 0.0286 | 1.28536/0.028571/3.8535/0.028571 | same | ✓ |
| 17.6-fold gap | 3.8535/0.2187 = 17.62 | 17.6 | ✓ |
| HD_down +0.397, P 0.0286, g 2.658, q 0.086 | 0.39671/0.028571/2.6584/0.085713 | same | ✓ |
| SI_g G1 38.4, G2 0.44, G3 1.44, G4 240.5, G5 9.06 | 38.42/0.440/1.438/240.47/9.055 | same | ✓ |
| 8/40 BH-significant | 8 / 40 | same | ✓ |
| G1∩G5 = 10 (43% of 23) | 64∩23 = 10; 10/23 = 43.5% | same | ✓ |
| G4 artefact blood MRU≈0.5, |Δ|≈0.0009; G1 |ΔBLD−0.5|=0.0106 | 0.499075/0.000925; 0.010558 | same | ✓ |
| G1 q 0.0010, G5 q 0.0016 (DRG×SNI) | 0.0009999 / 0.0015998 | same | ✓ |
| Table 3 MRU (all 10 cells) | per_set_specificity | same | ✓ |
| Table 4 rows (G1–G5, HD_up, PC) | layer3b table | same | ✓ |
| Layer 3b 0/5; PC g 3.85 P 0.0286; HD_up g 0.219 P 0.80 | conditions + table | same | ✓ |
| Layer 4 15345 genes, 8 up/3 down, ECM-union 0, OR 0, P 1.0 | layer4 JSON | same | ✓ |
| Discussion "full separation" vs Stage B/Fig5 "lower bound" | both = 2/70 = 0.028571; non-overlapping saline-arm groups | consistent | ✓ |
| Abstract ≤300 words | 303 words | 303 (brief target 300) | ✗ (protocol ≤350 ok) |

**Conclusion:** No number was altered or dropped by the polish. The single deviation is the abstract length vs the round brief's 300-word target (F8).

---

## § Stands up (what survived the audit well)

1. **Source-traceable numerics.** Every headline statistic I spot-checked maps to a specific field in `analysis/results/**` and matches to the stated rounding. The "every number traceable to a result file" claim in the Data Availability statement is borne out by my recomputation.
2. **The three-calibration discipline for Stage A is intact.** The manuscript keeps the three P-value families strictly separated (full-background unstratified 0.597/0.0009; diagnostic unstratified 0.055/0.085; expression-matched primary 0.102/0.100) and correctly names the expression-matched set as the governing endpoint — exactly as the protocol §8.1 / §12.3 mandate. This is the easiest place for a polish to collapse three numbers into one, and it did not.
3. **Honesty disclosures preserved.** The G1/G5 10-member overlap (verified 10/23 = 43%), the G4 denominator artefact (blood MRU 0.499075, |Δ| 0.000925), and the "plain double-null" (not "negative result") characterization of Stage A are all retained and quantitatively correct. The positive-control "full separation" claim is consistent, not inflated (F7).
4. **Layer 3b / Layer 4 FAIL verdicts and Layer 0 anchor preserved verbatim**, with HD_down correctly held at "hypothesis-generating only" (q=0.086, not BH-significant) and the 17.6-fold gap intact.

---

## § Questions for the authors

1. **Abstract length:** The Abstract measures 303 words. Is a strict ≤300 ceiling imposed for this round, or does the protocol's ≤350 govern? If 300 is firm, please trim ~4–5 words (suggested cuts in F8).
2. **Granularity of "coverage":** Manuscript line 62 reports HD_up "11/18 expressed" and Limitations line 97 reports "coverage 0.611." These are the same quantity (11/18 = 0.611). Confirm you intend both phrasings and that neither is meant to imply all 18 map (homology mapping rate = 1.0, coverage = 0.611) — the protocol §4.3 distinction is correctly maintained elsewhere, but the two numbers in one paragraph could confuse a skimming reader.
3. **G1/G5 overlap provenance:** I verified the 10-member overlap from `analysis/config/ms_panel.json` (human HGNC member lists). Please confirm the overlap was computed on the *mapped mouse-present* members (the manuscript frames it as an overlap within the projected sets). If the overlap is on human symbols but the "4/5 pass" tally is on mouse-present members, the 43% figure is directionally right but the denominator (23) should be the mouse-present G5 count (21 per Table 4) rather than the human 23. Clarify which set the "23" refers to.
4. **Figure 5 / Discussion "full separation":** Would you accept the optional one-line clarification suggested in F7 to pre-empt a reviewer who reads "full separation" as stronger than "detected at the lower bound"?

---

## § What I actually checked

**Files read (source of truth):**
- `manuscript/manuscript.md` (full; line citations above refer to this file).
- `analysis/results/layer0/layer0_signature.json` — signature sizes, canonical-target deltas/P, LATS fractions.
- `analysis/results/layer1/layer1_results.json` — full-background unstratified P (HD_up DRG 0.59674, BLD 0.0009).
- `analysis/results/layer1/layer1_diag.json` — matched-null MRU/P/q and the three-calibration table; baseline-zero fractions.
- `analysis/results/layer2/layer2_results.json` — Stage B HD_up / HD_down primary saline-arm stats.
- `analysis/results/layer2/layer2_positive_control.json` — positive control + HD_up/HD_down g, MW P, per-animal saline-arm scores (used for F7 separation test).
- `analysis/results/layer3/layer3_generality.json` — SI_g, n-tests, n-BH-significant, per-set q, MRU, denominator artefacts.
- `analysis/results/layer3/layer3b_sample_generality.json` — Table 4 rows and FAIL conditions.
- `analysis/results/layer4/layer4_positive_characterisation.json` — 15345 genes, 8 up/3 down, ECM-union 0, Fisher OR/P.
- `analysis/config/ms_panel.json` — G1 (64) and G5 (23) member lists; recomputed intersection = 10.
- `PROTOCOL_基质刚度与神经病理性痛.md` — §5.3 governance, §8.1 Stage A verdict, §11.3 word limits, §12 Layer-3 design, v0.6/v0.7 changelog numbers.

**Values recomputed vs manuscript (discrepancies stated):** All brief-listed values recomputed and matched (table above). Discrepancies found: **none** in the numeric claims. The only mismatch is the abstract word count: brief/context implies ≤289–300 words; I measure **303** (still ≤ the protocol's 350). No digit was altered or dropped by the polish.

**Not independently re-derived (accepted from JSON as the frozen outputs):** The permutation P-values themselves were taken from the JSON fields rather than re-run from raw counts (the task was provenance/drift verification against the deposited artifacts, not a from-scratch re-execution). The internal consistency of those fields with the described methods (e.g., 2/70 = 0.028571 for 4-vs-4 exact two-sided; 9.999e-5 ≈ 1/10001 for 10000+1 permutation) was checked arithmetically and is sound.
