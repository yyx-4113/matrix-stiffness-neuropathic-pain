# B2 — Statistical-coherence review (blind, independent)

**Manuscript:** `manuscript/manuscript.md` (commit 4785c52)
**Lens:** internal statistical coherence — contradictions in what is called significant/null, and inconsistent application of the pre-specified governance rule (§5.3).
**Verdict:** **MAJOR (revise)** — one governance-coherence failure must be reconciled; the rest are clarity/terminology fixes.

---

## FINDING F1 — §5.3 is applied inconsistently with the frozen protocol for the *identical* Stage A numbers
*(corresponds to item 2: "DOUBLE NULL" governance)*

【Problem】
The manuscript reads the §5.3 trigger narrowly ("triggered only when a negative control is *equally significant* to the target"; both DRG and BLD are non-significant, therefore "the rule does not apply" → "plain double-null") and repeats this verdict verbatim in the Abstract (line 10), Results (line 53), Discussion (line 79), Core conclusion #2 (line 89), and Table 2 (line 119: "§5.3 not triggered (double null)"). But the very protocol the manuscript cites as authoritative (`PROTOCOL_矩阵刚度与神经病理性痛.md`, tag v1.0.0; cited at line 31) applies §5.3 to these *exact* numbers and reaches the opposite verdict.

【Evidence】
- Manuscript line 53: "The pre-specified governance rule (§5.3) is triggered only when a negative control is *equally significant* to the target; here both DRG and blood are non-significant, so the rule does not apply and Stage A is a plain double-null."
- Manuscript Table 2 line 119: verdict = "§5.3 not triggered (double null)".
- Protocol line 162 (literal §5.3 rule): "若阴性对照与主终点同等显著，则结论不得成立" — "if the negative control is equally [significant/extreme] to the primary, the conclusion cannot stand."
- Protocol lines 251, 260, 262, 295: the Stage A result where "阴性对照（血液）在匹配后与主终点（DRG）同样不显著（q = 0.409 对 0.409），两者统计上不可区分" is adjudicated **per §5.3** as **uninformative (无效检验)**, and explicitly: "亦不得回退为'阴性结果'或淡化为'趋势'" / "这一改判必须写入手稿，不得回退为'阴性结果'表述" — i.e., it MUST NOT be presented as a negative result.
- The q = 0.409 vs 0.409 values in the protocol match the manuscript's own reported q-values exactly (`layer1/layer1_diag.json`: HD_up DRG×SNI `q_expression_matched = 0.40916`; HD_up BLD×SNI `q_expression_matched = 0.40916`), so this is the same result, not a different calibration.

The protocol's reading of "equally significant" is "statistically indistinguishable (whether both significant or both not)"; the manuscript's reading is "both must be significant." Applied to the same data (both NS, q = 0.409 = 0.409), the two readings diverge: protocol ⇒ §5.3 *engaged* ⇒ uninformative; manuscript ⇒ §5.3 *not triggered* ⇒ double null.

【Why it matters】
This is precisely the "governance rule applied inconsistently" failure a statistical reviewer must catch. The headline "double null" framing risks being read as a *negative result* ("nothing happened in DRG"), which the frozen protocol explicitly forbids for this scenario. It inflates the strength of Core conclusion #2 ("yields no tissue-specific evidence of engagement … a sample-level sensitivity-validated null"): if Stage A is genuinely *uninformative* (per the protocol), the burden of "this is a real, sensitivity-validated absence" rests entirely on Stage B — and Stage A cannot be cited as corroborating evidence. The within-manuscript statements (line 79 vs Table 2 line 119) *are* mutually consistent, but both contradict the cited governance source.

【Specific fix】 (paste-ready)
Replace the "§5.3 not triggered (double null)" framing with the protocol's mandated verdict. Minimal reconciling edits:
- Table 2 line 119: change verdict to "§5.3 engaged → Stage A **uninformative** (control and target both NS and statistically indistinguishable, q = 0.409 vs 0.409); no inference permitted."
- Manuscript line 53: "…so §5.3 *is* engaged and Stage A is adjudicated **uninformative** (not a negative result): the matched-rank test cannot distinguish target from negative control."
- Manuscript line 79 / Core conclusion #2 (line 89): drop "double-null with §5.3 not triggered"; use "Stage A is uninformative per §5.3 (both DRG and blood non-significant and indistinguishable)"; keep the correctly-stated caveat "the result is also not informative about mechanism."
- Abstract line 10: "the §5.3 rule (control and target statistically indistinguishable) rendered Stage A **uninformative**, not a negative result."

---

## FINDING F2 — Three P-value sets for one contrast: defensible but the (a)/(b) boundary is confused and invites a selective-reporting reading
*(corresponds to item 1: TRIPLE P-VALUE PRESENTATION)*

【Problem】
Three P-value sets are presented for the same HD_up × DRG×SNI contrast: (a) full-background unstratified DRG P = 0.597 / BLD P = 0.0009; (b) diagnostic unstratified "in the matched null space" DRG P = 0.055 / BLD P = 0.085; (c) expression-matched primary DRG P = 0.102 / BLD P = 0.100. The explanation that only (c) is pre-specified and governs is present (line 53: "Only the last is pre-specified and governs the verdict"), so this is *not* P-hacking. However, (a) and (b) are both labelled "unstratified" yet differ ~10×, and (b) is oddly called "in the matched null space" though it is itself unstratified. A reader cannot tell operationally what differs between (a) and (b), which is exactly the ambiguity that fuels a selective-reporting suspicion.

【Evidence】
- Manuscript line 53 numbers recomputed from JSON:
  - (a) `layer1/layer1_results.json` HD_up DRG×SNI `p_permutation = 0.59674` (→0.597), BLD×SNI `p_permutation = 0.0009` (→0.0009). ✓
  - (b) `layer1/layer1_diag.json` HD_up DRG×SNI `p_unstratified = 0.055394` (→0.055), BLD×SNI `p_unstratified = 0.085491` (→0.085). ✓
  - (c) `layer1/layer1_diag.json` HD_up DRG×SNI `p_expression_matched = 0.10229` (→0.102), BLD×SNI `p_expression_matched = 0.10039` (→0.100). ✓
- The (a)/(b) gap is real and explained *only* by background definition, not stated in prose: (a) ranks over the **full** gene list including 40–58% zero-expression loci (`layer1/layer1_diag.json` per_contrast `pct_baseline_zero`: DRG 42.77%, BLD 58.48%); (b)/(c) recompute ranks within the **expressed** background only. The protocol's own note (line 260) calls the (b) unstratified calibration "inflated by artefact to near-significant (BLD 0.086, DRG 0.055)" — i.e., it is the *opposite* of a clean null, which makes presenting (b) as a neighbouring "0.055" next to (c)'s "0.102" look like showing a near-significant number that is then explained away.

【Why it matters】
The abstract reports only (c) (good). But in the body, surfacing a near-significant 0.055 (b) for the target alongside the governing 0.102 (c) is the single most P-hacking-resembling figure in the paper. The cure is not to hide (a)/(b) (they are valuable diagnostics of the zero-expression confound) but to make their *status* unmistakable and their *construction* explicit, so no reviewer suspects the primary was chosen post hoc from three candidates.

【Specific fix】 (paste-ready)
- Add to Methods (Stage A endpoint, around line 31): "Two additional, **non-pre-specified** diagnostic calibrations are reported for transparency only and never govern the verdict: (i) a full-background calibration ranking over all loci including 40–58% zero-expression genes; (ii) an expressed-background unstratified calibration. Only the expression-decile-matched primary (iii) is frozen and governs."
- Re-label so the two "unstratified" numbers are not confused: (a) "full-background (zeros-included) unstratified" and (b) "expressed-background unstratified (diagnostic)." Drop the phrase "in the matched null space" for (b) — it is unstratified, not matched.
- In line 53, state explicitly that (b) DRG P = 0.055 is the *artefact-inflated* value the protocol flags, to preempt a "near-significant" misreading.

---

## FINDING F3 — "Stage B a bounded null" (conclusion #2) under-specifies that HD_down within Stage B is nominally significant
*(corresponds to item 3: HD_up bounded null vs HD_down significant)*

【Problem】
Stage B's pre-specified primary (HD_up) is correctly a bounded null (diff = +0.146, P = 0.80, g = 0.219), and HD_down is correctly separated as a secondary, "nominally significant, BH-non-significant, hypothesis-generating only" result (diff = +0.397, P = 0.0286, q = 0.086, g = 2.658). These two framings are internally coherent *in the body* (lines 57–58). However, Core conclusion #2 (line 89) says only "Stage B a bounded null" without the HD_up qualifier, which a reader could read as "nothing in Stage B was significant" — contradicting the HD_down report.

【Evidence】
- `layer2/layer2_results.json` HD_up `primary_saline_arm`: diff 0.14645, p 0.8, q_BH 0.8. ✓
- `layer2/layer2_results.json` HD_down `primary_saline_arm`: diff 0.39671, p 0.028571, q_BH 0.085713; `layer2/layer2_positive_control.json` HD_down hedges_g 2.6584. ✓ All match manuscript (line 58; Table 2 line 122; Table 4).
- Manuscript line 89: "Stage B a bounded null" — no HD_up qualifier.

【Why it matters】
Not a numeric contradiction, but a framing one. Conflating "the HD_up primary is a bounded null" with "Stage B is a null" lets conclusion #2 quietly omit that a *different* direction of the same signature is nominally significant. The body already distinguishes them; the conclusion should mirror that precision.

【Specific fix】 (paste-ready)
Line 89: change "Stage B a bounded null" to "Stage B: the HD_up primary is a bounded null (HD_down is nominally significant but BH-non-significant and reported as hypothesis-generating only)."

---

## FINDING F4 — "independent wins are G1, G3, and G5, with G1 and G5 correlated" is internally self-contradictory; conclusion #3 can be over-read as sample-level upregulation
*(corresponds to item 4: Layer 3 retained specificity vs Layer 3b/4 fails)*

【Problem】
Two sub-issues.
(1) Line 67 states "the independent specificity wins are G1, G3, and G5, with G1 and G5 correlated." If G1 and G5 are correlated (they share 10/23 members, 43%), they are not *both* independent wins; the genuinely independent wins are the G1/G5 matrisome–fibrosis cluster plus G3 — i.e., 2 independent signals, not 3.
(2) The multi-layer narrative (Layer 3 rank-projection specificity retained by G1/G3/G5; Layer 3b and Layer 4 both FAILED — no sample-level upregulation) is *coherent* because lines 81 and 83 carefully separate "rank-projection specificity" from "sample-level upregulation." But Core conclusion #3 (line 90) says "expression-stratified projection recovers a DRG-over-blood shift for established ECM/mechanotransduction modules (G1, G5, and the mechanosensory G3)" without the rank-projection qualifier, which can be read as "these modules are upregulated in injured DRG" — the very claim Layer 3b/4 say is absent/inconclusive.

【Evidence】
- `layer3/layer3_generality.json`: `n_sets_failing_specificity = 1` (only G2), `primary_endpoint_pass = false` → ≥4/5 rule not met. ✓ Matches manuscript line 67.
- G1∩G5 overlap = 10 members of G5's 23 (43.5%); manuscript line 67 "share 10 members (43% of G5's 23)." ✓
- `layer3b_sample_generality.json`: verdict "FAIL", 0/5 ECM sets significant at sample level; G3 `diff_saline_arm = -0.2768`, `p_exact_saline_arm = 0.2857` (manuscript line 83: G3 diff −0.277, P = 0.286). ✓
- `layer4/layer4_positive_characterisation.json`: `n_sig_up_q05 = 8`, `ecm_union.n_sig_up_q05 = 0`, `fisher_OR = 0`, `fisher_P = 1.0`, verdict "FAIL". ✓

【Why it matters】
The "retained specificity" and "sample-level absence" findings are not contradictory (they answer different questions), and the manuscript mostly says so. The risk is that conclusion #3 over-reads the rank-projection result as positive engagement, which would then appear to contradict Layer 3b/4. Tightening the wording removes the only internal tension in the Layer-3 story.

【Specific fix】 (paste-ready)
- Line 67: change "the independent specificity wins are G1, G3, and G5, with G1 and G5 correlated" → "the specificity wins beyond G2's failure are G1, G3, and G5; among these, G1 and G5 are mutually correlated (shared matrisome/fibrosis members), so the count of *independent* wins is two — the G1/G5 cluster and G3."
- Line 90 (conclusion #3): add qualifier — "expression-stratified projection recovers a **rank-projection** DRG-over-blood shift (relative specificity, not sample-level upregulation) for G1, G5, and the mechanosensory G3; this is consistent with Layer 3b/4 finding no sample-level upregulation of these modules."

---

## FINDING F5 — G3 is consistently described as specificity-retaining but NOT BH-significant and NOT sample-level upregulated (verified coherent)
*(corresponds to item 5: G3 ambiguity)*

【Problem / check】
Confirmed consistent. G3 "retains specificity by SI (1.44) but does not reach BH significance and was not upregulated at the sample level" is stated identically in Results (line 67), Discussion (lines 79, 83), and Limitations (line 93). No sentence attaches "BH-significant" to G3; the BH-significant group is explicitly scoped to "G1 and G5" (lines 67, 79).

【Evidence】
- `layer3/layer3_generality.json`: G3 DRG×SNI `MRU_target = 0.80398`, `MRU_negative_blood = 0.71140`, `SI = 1.4379` (→1.44); `q_matched_BH40` for G3 DRG×SNI = 0.06519 > 0.05 → not BH-significant. ✓
- `layer3b_sample_generality.json`: G3 `diff_saline_arm = -0.2768`, `p_exact_saline_arm = 0.2857` → not upregulated (even negative). ✓ Matches manuscript line 83 (G3 diff −0.277, P = 0.286).
- Grep of manuscript: "BH-significant" is attached only to G1 and G5 (lines 67, 79); G3 is always paired with "does not reach BH significance" / "retains specificity." No contradiction found.

【Why it matters / Specific fix】
No defect. (Included as a verified-coherent item; see § Stands up.)

---

## FINDING F6 — Claim that BH q-values are "conservative under positive dependence" is statistically correct
*(corresponds to item 6: BH under positive dependence)*

【Problem / check】
The manuscript states (lines 67, 138) that because G1 and G5 share members the 40 tests are positively dependent and "the BH q-values remain valid (conservative under positive dependence)." This is correct.

【Evidence】
- `layer3_generality.py` defines standard BH: `q = p[o] * n / (arange(n)+1)` then `minimum.accumulate` from the right, clipped to [0,1] (lines 81–90). Applied to the 40-test family (`tbl["q_matched_BH40"] = bh(tbl["p_matched"].to_numpy())`, line 262). ✓
- Statistical basis: Benjamini–Hochberg controls FDR under positive regression dependency on a subset (PRDS; Benjamini & Yekutieli, 2001). Under positive dependence the procedure is *conservative* (true FDR ≤ nominal), so the q-values are valid and, if anything, anti-liberal. Overlapping G1/G5 produce positively correlated test statistics, satisfying the positive-dependence condition. The claim is therefore sound.
- Value check: `layer3/layer3_generality.json` `n_surviving_BH_0.05 = 8` (manuscript line 67 "8/40 BH-significant"); `min_q_matched = 0.0009999` (G1 DRG q = 0.0010). ✓

【Why it matters / Specific fix】
No defect. (Verified-coherent; see § Stands up.)

---

## FINDING F7 — Table 3 / Figure 6 present G4's SI = 240.5 as a precise passing bar while the footnote says it is "undefined to within an order of magnitude"
*(corresponds to item 7: G4 bounded-null / denominator artefact)*

【Problem】
The arithmetic is correct (G4 SI = 0.2224 / 0.000925 = 240.5, `layer3/layer3_generality.json` `SI = 240.472`), and the denominator artefact is disclosed in the Table 3 footnote (line 138: "blood MRU = 0.499075, |ΔBLD−0.5| = 0.000925, so SI_g (≈240) is undefined to within an order of magnitude") and Limitations (line 93) and the Figure 6 legend (line 187). But Table 3 *lists* "240.5" as a precise value with verdict "No" (pass), and Figure 6 *draws* G4 as an ordinary solid passing bar on a log scale. A log-scale bar at ~240 looks like a robust pass; the visual therefore over-states G4 relative to the textual caveat.

【Evidence】
- `layer3/layer3_generality.json`: G4 `MRU_target = 0.72240`, `MRU_negative_blood = 0.499075`, `SI = 240.472`. Table 3 lists SI_g = 240.5, "Specificity failed? No." ✓
- Manuscript line 138 footnote: "SI_g (≈240) is undefined to within an order of magnitude and the absolute shifts must be read directly." ✓ consistent with the number, but the table/figure presentation is not.
- Figure 6 legend (line 187) discloses the artefact but the bar itself is not visually flagged.

【Why it matters】
This is a presentation-coherence gap, not a numeric error. A reader scanning Figure 6 sees four blue "pass" bars (G1, G3, G4, G5) and may count G4 as a fourth independent specificity win — which compound F4's over-count and undercuts the "apparent 4/5 pass is inflated" message the authors are at pains to convey.

【Specific fix】 (paste-ready)
- In Figure 6, annotate the G4 bar explicitly (e.g., hatch or an asterisk with caption "G4: denominator artefact — blood MRU ≈ 0.5, ratio undefined to ~1 order of magnitude; not counted as evidence").
- In Table 3, render G4's SI cell as "≈240 (undefined ±1 order)" rather than a bare "240.5," so the table does not assert false precision.

---

## § STANDS UP (verified internally coherent and correct)

1. **Stage A primary numbers reconcile exactly.** HD_up DRG×SNI MRU = 0.71677 → 0.717, P = 0.10229 → 0.102, q = 0.40916 → 0.409; BLD×SNI MRU = 0.6964 → 0.696, P = 0.10039 → 0.100, q = 0.40916 → 0.409 (`layer1/layer1_diag.json`; manuscript lines 10, 53, Table 2 line 119). The "equally non-significant, q = 0.409 each" statement is exactly right.
2. **Stage B sensitivity validation is real and the contrast is fair.** Positive control diff = +1.28536, P = 0.028571, g = 3.8535; HD_up diff = +0.14645, P = 0.8, g = 0.2187; the 17.6-fold g-gap (3.8535 / 0.2187 = 17.62) matches the manuscript's "17.6-fold" (`layer2/layer2_positive_control.json`, `layer2/layer2_results.json`; lines 10, 57–58). The bounded-null vs detected-control contrast is genuinely demonstrated.
3. **HD_down framing (nominal sig, BH-ns, hypothesis-generating) is numerically exact and correctly demoted.** diff = +0.39671, P = 0.028571, q_BH_family_of_4 = 0.085713, g = 2.6584 (`layer2/layer2_results.json`, `layer2/layer2_positive_control.json`; Table 2 line 122). The exact-permutation P = 0.028571 equals the enumeration lower bound 2/70, confirming it is the smallest attainable two-sided P at this 4-vs-4 design (`gate_consistency.py` L106–112; correct).
4. **Layer 3 primary verdict is arithmetically derived, not asserted.** `n_sets_failing_specificity = 1`, `primary_endpoint_pass = false` (only G2 fails, SI = 0.4402), so the ≥4/5 rule is correctly "not met" (`layer3/layer3_generality.json`; manuscript line 67, Table 2 line 123). All five SI values (G1 38.42, G2 0.44, G3 1.44, G4 240.47, G5 9.05) match Table 3 to the rounding shown.
5. **Layer 3b and Layer 4 FAIL verdicts are supported.** Layer 3b: 0/5 ECM sets significant (G1–G5 P = 0.229/0.657/0.286/0.171/0.314), positive control P = 0.028571 (q = 0.20), verdict FAIL (`layer3b_sample_generality.json`; manuscript lines 72, Table 4). Layer 4: 8/15 345 genes sig-up, ECM-union sig-up = 0, Fisher OR = 0, P = 1.0, verdict FAIL (`layer4/layer4_positive_characterisation.json`; line 72).
6. **BH-under-positive-dependence claim is correct** (F6 above).
7. **G3 treatment is coherent** (F5 above).
8. **CTGF biological anchor reconciles.** delta_WT = 1.6405 → +1.64, p_WT = 9.494 × 10⁻⁶ → 9.5 × 10⁻⁶ (`layer0/layer0_signature.json`; lines 10, 48, 79, 89). LATS confirmation 79.7% (HD) vs 28.6% (HI) (`layer0/layer0_signature.json` `lats_confirmation_fraction`; line 48).
9. **The "0/5 sets retain specificity" vs "signature-specific null" narrative is coherent**, provided the rank-projection/sample-level distinction (lines 81–83) is preserved — the manuscript does preserve it; only conclusion #3 needs the qualifier in F4.

---

## § QUESTIONS FOR THE AUTHORS

1. On F1: Do you intend Stage A to be reported as the protocol mandates — **uninformative per §5.3** — or as a "double null"? If the latter, what is your justification for departing from the frozen protocol's explicit "must not be a negative result" instruction for these exact numbers?
2. On F2: Could you add the Methods statement that (a) and (b) are *non-pre-specified* diagnostics, and clarify that (b)'s DRG P = 0.055 is the artefact-inflated value the protocol flags — to pre-empt any selective-reporting reading?
3. On F4/F7: Given G1 and G5 are correlated and G4 is a denominator artefact, how many *independent* Layer-3 specificity signals do you claim — two (G1/G5 cluster + G3) or three? Please make the count and the rank-projection-vs-sample-level distinction explicit in conclusion #3.
4. On F3: Will you qualify "Stage B a bounded null" (conclusion #2) so it is unambiguous that HD_down is nominally significant but BH-non-significant?
5. Minor: The abstract (line 10) says "we find no detectable transfer … at the 4-vs-4 resolution" and "This is a sensitivity-validated null" — given F1 (Stage A is uninformative per protocol, not a clean null), should the abstract's strength of claim be softened to "the sample-level (Stage B) test is a sensitivity-validated bounded null, while the rank-projection Stage A is uninformative per §5.3"?

---

## § WHAT I ACTUALLY CHECKED

**Files read (manuscript + source only; no review/response, memory, or sibling-reviewer files opened):**
- `manuscript/manuscript.md` (full).
- `PROTOCOL_矩阵刚度与神经病理性痛.md` (methodology/governance source cited by the manuscript at line 31) — read for the literal §5.3 rule (line 162) and its adjudication of the Stage A numbers (lines 251, 253, 260, 262, 295).
- JSON ground truth: `layer0/layer0_signature.json`; `layer1/layer1_results.json`, `layer1/layer1_diag.json`; `layer2/layer2_results.json`, `layer2/layer2_positive_control.json`; `layer3/layer3_generality.json`, `layer3/layer3b_sample_generality.json`; `layer4/layer4_positive_characterisation.json`.
- Scripts (to confirm method, not just numbers): `layer1_projection.py`, `layer1_diag.py`, `layer3_generality.py`, `gate_consistency.py` (BH function and the §5.3 "double null" guard at L307–309).

**Values recomputed / reconciled against the manuscript:**
- Stage A triple P-values (a/b/c) — all match to 3 decimals (F2 evidence).
- Stage A q = 0.409 each — matches `layer1_diag.json` `q_expression_matched` for HD_up DRG×SNI and BLD×SNI.
- Stage B HD_up (+0.146, P 0.80, g 0.219) and HD_down (+0.397, P 0.0286, q 0.086, g 2.658) — match.
- Positive control (+1.285, P 0.0286, g 3.85) — match; 17.6× gap confirmed (3.8535/0.2187 = 17.62).
- Layer 3 SI values G1 38.42, G2 0.44, G3 1.44, G4 240.47, G5 9.05 — match Table 3; G4 blood MRU 0.499075, |Δ| 0.000925 — match footnote.
- Layer 3: 1/5 fail, primary not met, 8/40 BH-sig — match.
- Layer 3b FAIL (0/5 sig up; G3 −0.277/0.286) and Layer 4 FAIL (8/15 345; ECM-union 0; OR 0, P 1.0) — match.
- CTGF anchor +1.64 / 9.5×10⁻⁶ — match.
- BH = standard Benjamini–Hochberg — confirmed in `layer3_generality.py`.

**Discrepancies / tensions found:**
- F1 (material): manuscript's "§5.3 not triggered / double null" contradicts the frozen protocol's mandated "uninformative" verdict for the identical q = 0.409 vs 0.409 result.
- F2 (minor): (a) and (b) both "unstratified," ~10× apart, under-explained; (b) DRG 0.055 is the protocol-flagged artefact value.
- F3 (minor): conclusion #2 "Stage B a bounded null" omits the HD_down nominal significance.
- F4 (minor): "independent wins G1,G3,G5 with G1,G5 correlated" is self-contradictory; conclusion #3 lacks the rank-projection qualifier.
- F7 (minor): G4 SI = 240.5 shown as precise passing bar/value despite "undefined to an order of magnitude" footnote.
- No numeric errors were found in any reported statistic.

**Verdict: MAJOR (revise).** All reported numbers are accurate and traceable to the JSON, and most of the multi-layer narrative is internally coherent. However, F1 is a genuine governance-coherence failure: the manuscript applies §5.3 in a way the cited frozen protocol rejects for these exact numbers (protocol ⇒ uninformative; manuscript ⇒ not triggered / double null), and the "double null" framing risks being read as the negative result the protocol explicitly forbids. F1 must be reconciled before acceptance. F2–F4 and F7 are clarity/terminology fixes that should accompany it. F5 and F6 are correct as written.
