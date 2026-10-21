# Reviewer A2 — Design & Statistics

This is a reanalysis with an unusually disciplined pre-specification structure (frozen protocol, dual negative controls, a pre-specified positive control, and a five-set benchmark). That discipline is real and valuable, and most of the arithmetic in the manuscript checks out against the source JSONs (see § What I actually checked). My concerns below are about *interpretation and statistical soundness of the positive claims*, not about fabrication. The central issue is that the manuscript wraps several fragile or logically weak results in language that overstates how firmly they support the headline conclusion ("established ECM/mechanotransduction gene sets retain tissue specificity in pain").

---

## Item 1 — G4 specificity index is an artefact of a denominator ≈ 0; "retained specificity" for G4 is not a robust claim

【Problem】 The Layer-3 claim that G4 (actin/Rho/ROCK) "retains specificity" (SI_g = 240.5) is entirely an artefact of a blood (BLD) MRU that sits essentially exactly on the null (0.5); the ratio is pathologically unstable to any perturbation of that near-zero denominator, and the DRG shift itself is not significant.

【Evidence】 From `analysis/results/layer3/layer3_generality.json` (per_set_specificity block, lines 46–51), the full-precision values are:
- MRU(DRG,SNI) = 0.72239618 → |ΔDRG−0.5| = 0.222396
- MRU(BLD,SNI) = 0.49907517 → |ΔBLD−0.5| = **0.00092483** (the manuscript reports this rounded as 0.0009)
- SI_g = 0.222396 / 0.00092483 = **240.47** (matches the reported 240.5).

I recomputed SI_g under perturbations of the BLD MRU (DRG fixed at 0.722396):

| BLD MRU | |ΔBLD−0.5| | SI_g |
|---|---|---|
| 0.4995 / 0.5005 | 0.0005 | 444.8 |
| 0.4990 / 0.5010 | 0.0010 | 222.4 |
| 0.4980 / 0.5020 | 0.0020 | 111.2 |
| 0.4970 / 0.5030 | 0.0030 | 74.1 |
| 0.4960 / 0.5040 | 0.0040 | 55.6 |

A perturbation of merely ±0.002 in the blood MRU — well within the noise of an n = 3 per-contrast summary-statistic input — swings SI_g from 240 down to 55–111. At BLD MRU = 0.5000 the ratio diverges to infinity. The ratio is not a stable quantity.

Crucially, the *substantive* components are weak: from the same JSON table, G4 DRG×SNI has matched p = 0.2256, q_BH40 = 0.3533 (lines 417–429) — **not significant** — while G4 BLD×SNI has MRU = 0.4991 and matched p = 0.9976 (lines 501–513), i.e. blood shows *no shift at all*. So G4's "strong specificity" is the ratio of a (non-significant) DRG shift to a blood shift of essentially zero. The honest description is "blood shows no shift (MRU = 0.4991 ≈ 0.5); DRG shows a shift (MRU = 0.7224) that is not itself statistically distinguishable from 0.5 at this input." The magnitude "240.5" carries no information beyond "blood ≈ null."

【Why it matters】 The abstract (manuscript line 12) and Discussion (line 83) present the specificity range "0.44–240.5" and treat 4/5 sets as having "retained specificity," listing G4 among them. If one of those four rests on a denominator that is numerically zero, the "4/5" count is partly illusory. A reader who takes SI_g = 240.5 as a precise, informative index is misled. This directly undermines the manuscript's "most substantive result" (line 83).

【Specific fix】 Replace the ratio-based specificity for G4 (and analogous near-zero-denominator cases) with the absolute shifts, and demote G4 from "strong specificity retained" to "blood not shifted, DRG nominally shifted but non-significant." Concretely, in Table 3 and the abstract, change the G4 row/cited value to something like:

> "G4 (actin/Rho/ROCK): DRG×SNI MRU = 0.7224 (|Δ| = 0.222, matched p = 0.226, not significant); BLD×SNI MRU = 0.4991 (|Δ| = 0.001, p = 0.998). The specificity index SI_g = 240.5 is unstable (denominator ≈ 0) and should not be read as strong specificity; the informative statement is that blood shows no shift while DRG shows a non-significant shift."

And in the abstract, replace "specificity index 0.44–240.5" with the absolute-shift framing so the unstable 240.5 is not presented as a precise datum.

---

## Item 2 — Layer-3 BH q-values are correctly computed, but the "8/40 significant → specificity retained" inference conflates two different questions, and the 5 sets are not independent

【Problem】 The BH correction over the 40-test family is arithmetically correct and G1 (q = 0.0010) and G5 (q = 0.0016) do reach significance — but the manuscript uses these BH results to support a *specificity* claim that the SI_g ratio (not the BH q) actually carries, and it ignores that only 2 of the 4 "retained" sets have a significant DRG shift while the 5 sets are correlated.

【Evidence】 I reconstructed the 40-test family (5 sets × 4 tissues × 2 models) from the JSON table and re-ran Benjamini–Hochberg. Results match the file exactly:
- G1 DRG×SNI: p = 9.999e-05 → q = 0.0009999 ≈ **0.0010** (matches manuscript).
- G5 DRG×SNI: p = 0.00019998 → q = 0.00159984 ≈ **0.0016** (matches manuscript).
- 8/40 survive at q < 0.05 (matches the reported 8).

The 8 survivors are: G1 DRG-CFA, G1 DRG-SNI, G1 SC-CFA, **G1 BRN-SNI**, G4 SC-SNI, **G4 BRN-CFA**, G5 DRG-SNI, G5 SC-CFA. Two problems with how this is deployed:

1. **Conflated questions.** The BH q-values answer "does this contrast's MRU differ from 0.5?" They do NOT answer "does DRG shift more than blood?" (the SI_g question). G1 BRN-SNI (q = 0.0073) and G4 BRN-CFA (q = 0.020) being significant says nothing about DRG-over-blood specificity. Yet the manuscript (line 71, line 83) presents "8/40 BH-significant, all in DRG/SC/BRN, none in blood" as if it substantiates tissue specificity. It substantiates "these modules are shifted somewhere," not "specifically in DRG vs blood."

2. **Only 2 of the 4 "retained" sets actually have a significant DRG shift.** From the JSON table: G1 DRG×SNI q = 0.0010 (significant), G5 DRG×SNI q = 0.0016 (significant), but G3 DRG×SNI q = 0.0652 (not significant; SI = 1.44, marginal) and G4 DRG×SNI q = 0.3533 (not significant, Item 1). So the positive Layer-3 conclusion is really carried by **G1 and G5 only**; G3 and G4 are carried by the ratio against a non-significant blood null.

3. **The 5 sets are not independent.** G1 (core matrisome) and G5 (ECM remodelling/fibrosis) share members (FN1, COL1A1, SPP1, ACTA2, CTGF, TIMP1, …); G2 and G4 share TAGLN; G5 and G4 share ACTA2. BH assumes independent (or positively regression-dependent) tests. Correlated tests make the effective family smaller than 40, so the reported q-values are **anti-conservative** — the true FDR is higher than nominal.

【Why it matters】 The headline "4/5 retain specificity" and the emphasis on G1/G5 "reaching BH significance" together overstate the robustness of the Layer-3 positive result. A reviewer/reader could reasonably conclude there is strong, multiplicity-controlled evidence of DRG-specific ECM engagement; in fact only two sets show a significant DRG shift, one of the "retained" four is a denominator artefact, and the BH family is correlated.

【Specific fix】 (a) Separate the two claims explicitly: state that G1 and G5 show a BH-significant DRG×SNI shift (real), while G3 and G4 "retain specificity" only in the ratio sense against a non-significant blood null and are not themselves BH-significant in DRG×SNI. (b) Add a statement that the 5 gene sets are overlapping, non-independent modules, so the 40-test BH q-values are a lower bound on the true FDR and should be interpreted as suggestive, not confirmatory. (c) Either de-correlate the family (e.g., test non-overlapping gene subsets) or report a sensitivity analysis with a dependent-adjustment (e.g., Benjamini–Yekutieli) and state the resulting q-values.

---

## Item 3 — The "17.6-fold Hedges-g gap" is not a valid bounded-null / sensitivity calibration

【Problem】 Comparing the positive-control Hedges g (3.85) to the HD_up g (0.219) and calling the 17.6-fold gap evidence that HD_up's null is "bounded (real absence) rather than a sensitivity failure" is not a sound internal sensitivity calibration; Hedges g is scale-dependent and the comparison only rules out gross pipeline collapse, not the presence of a moderate, undetectable effect.

【Evidence】 From `analysis/results/layer2/layer2_positive_control.json`: positive control difference = 1.28536, p_exact = 0.028571, **hedges_g = 3.8535** (lines 54–59); HD_up difference = 0.14645, p_exact = 0.8, **hedges_g = 0.2187** (lines 110–115). Ratio 3.8535 / 0.2187 = **17.62** (matches the reported 17.6). Both sets did run through identical scoring/permutation code — that part is correctly done and is a genuine positive control.

However:
- **g is scale-dependent and set-composition-dependent.** The two g's come from different gene sets (12 vs 11 members) with different internal coherence and different within-set pooled SD. g is not a calibrated sensitivity metric; a 17.6-fold ratio is not interpretable as "the null is bounded at 1/17.6 of the detectable effect."
- **A positive control vs a null is not a sensitivity *bound*.** It demonstrates the pipeline can detect a *large, known* signal. It does NOT establish the smallest effect the pipeline could detect, nor does it bound the size of a true HD_up effect that may be present but below the detection floor. A true moderate HD_up effect (g ≈ 0.3–0.6, entirely plausible for a cross-tissue/cross-species projection) would be completely invisible at the n = 4-vs-4 exact-permutation design, whose lower bound is P ≈ 0.029 (i.e. only very large effects can be rejected).
- **The two contrasts are different biology.** The positive control is nerve-injury markers expected to be strongly up in injured DRG; HD_up is a HEK293A stiffness program not expected in DRG. A large gap between them is exactly what any functioning pipeline would show regardless of sensitivity — it mainly confirms the positive control works, which the authors already concede ("its failure would void all null conclusions").

【Why it matters】 The "bounded null" framing is one of the two pillars of the manuscript's claim that the HD_up failure is *informative* rather than a method artefact (manuscript lines 62, 83, 91). If the 17.6-fold gap does not actually bound the null, then the strongest supported statement is only "the pipeline is not totally broken" — which leaves open that the HD_up non-result could still be a Type II error due to n = 4-vs-4 power, not a real absence.

【Specific fix】 Recast the argument. Replace:
> "The 17.6-fold Hedges-g gap between positive control and HD_up, on identical code, shows the HD_up null is bounded (a real absence of detectable signal at this design) rather than a sensitivity failure."

with:
> "Running the positive control through identical code detected a strong, known SNI signal (g = 3.85, P = 0.029), confirming the pipeline is not broken. HD_up was not detected (g = 0.22, P = 0.80). This validates the pipeline against gross sensitivity failure but does not bound the size of a true HD_up effect: at n = 4-vs-4 the exact-permutation lower bound is P ≈ 0.029, so only very large effects are detectable; a moderate true effect would also yield a null. The HD_up null is therefore a *sensitivity-validated* null, not a tightly bounded one."

---

## Item 4 — §5.3 negative-control governance is misapplied to a double-null; calling Stage A "uninformative" is an overstatement

【Problem】 The protocol's §5.3 rule is triggered when the negative control is *equally significant* to the primary (which would block tissue-specific attribution). Here **both** DRG and blood are *non-significant* (q = 0.409 each), so the trigger is not met; the manuscript nonetheless applies the rule and labels Stage A "uninformative," which overstates the situation.

【Evidence】 Manuscript states the §5.3 rule (line 35): "if a negative control is *equally* significant to the primary, tissue-specific attribution cannot be made." Stage A results (lines 56–57, Table 2 line 121): DRG×SNI HD_up MRU = 0.717, P = 0.102, BH q = 0.409; BLD control MRU = 0.696, P = 0.100, q = 0.409. I verified these against `analysis/results/layer1/layer1_diag.json`: DRG×SNI matched MRU = 0.71677, p_expression_matched = 0.10229, q = 0.40916 (lines 234–237); BLD×SNI matched MRU = 0.6964, p = 0.10039, q = 0.40916 (lines 190–193). Both are far from significance; the q-values are equal only because BH scaled both within the same family.

The logical error:
- The rule exists for the case where BLD is *significant* — that signals the projection statistic is confounded by a non-tissue-specific factor, making a DRG-positive result uninterpretable as tissue-specific. That trigger is **not present** here (BLD q = 0.409).
- A *double null* does not imply "uninformative." It implies "no detectable tissue-specific engagement at this design's power." That is a coherent (if weak) negative finding: DRG MRU = 0.717 and BLD MRU = 0.696 are close, i.e. the signature does **not** preferentially engage DRG over blood — which is entirely consistent with the paper's overall conclusion that the transfer fails. The data are *informative* in the direction they point; they are merely not statistically significant.
- "Uninformative" also discards the genuine signal that DRG ≈ BLD (both near 0.7, both non-significant), which is the opposite of "no information." The correct descriptor is "negative / inconclusive / underpowered," not "uninformative."

【Why it matters】 The manuscript elevates this misapplication into a formal verdict ("Stage A is uninformative, not merely negative," line 57; reiterated line 83, 91). It manufactures a governance-driven reason for a result that is simply a non-significant primary endpoint. This both overstates the rigor ("the protocol forced this verdict") and mislabels a coherent negative finding as content-free.

【Specific fix】 Change the Stage A verdict from "uninformative by §5.3" to a plain negative/underpowered result. Suggested:

> "Under the pre-specified expression-matched calibration, DRG×SNI HD_up gave MRU = 0.717, P = 0.102, BH q = 0.409 (not significant); the blood control was similarly non-significant (MRU = 0.696, P = 0.100, q = 0.409). The §5.3 rule (triggered when a negative control is *significant*) does not apply because neither contrast is significant. The primary endpoint is therefore a negative, underpowered result (n = 3 per contrast), not a governance-driven 'uninformative' one; DRG and blood shift comparably, consistent with no tissue-specific engagement."

---

## Item 5 — Small-n / multiple-comparison structure is not adequate to support the positive Layer-3 claim with confidence

【Problem】 Across all layers the effective sample sizes are tiny (n = 3 per contrast summary stats in Stage A / Layer 3; n = 4-vs-4 exact permutation in Stage B), yet the manuscript draws a confident *positive* Layer-3 conclusion ("4/5 retain specificity"). This is under-powered for a positive claim, and the multiple-comparison structure has unaddressed dependencies.

【Evidence】
- **Stage A / Layer 3 inputs are n = 3 per contrast summary statistics** (manuscript line 29, Table 1 line 114; protocol `ms_panel.json` layer1.n_per_group = 3). The MRU statistic is computed from per-contrast mean log2-FC of 3 samples, so its precision is intrinsically low; the 10 000-iteration matched null yields a p-value but the *input* uncertainty is large.
- **Stage B lower bound P ≈ 0.029** (manuscript line 95; exact permutation over C(8,4) = 70 splits). Only very large effects are detectable. The positive control (g = 3.85) passes; any moderate true HD_up effect would be missed — so the Stage B "bounded null" is bounded only at the large-effect extreme (Item 3).
- **Layer 3 positive conclusion rests on SI_g ratios, not on significance** (Item 1–2). Of the 4 "retained" sets, only G1 and G5 have a BH-significant DRG shift; G3 (SI = 1.44, DRG q = 0.065) is marginal and G4 is the denominator artefact. The pre-specified bar was "≥ 4/5 fail specificity → method-level failure"; that bar was *not* met (only 1/5 failed), so the authors infer specificity is *retained*. With only 5 sets and an uncorrected ratio test, plus one artefactual ratio, this inference is fragile.
- **"0/40 significant in blood" may be a power artefact, not specificity evidence.** Blood has far fewer mapped-present genes (n_mouse_present 61/42/20/22 across the 4 sets in the JSON table) than DRG/SC/BRN (~64/64/23), so BLD tests are intrinsically less powered. "None significant in blood" is therefore expected by design and low power, not strong evidence that DRG > blood specifically.
- **Correlated BH family** (Item 2): the 5 sets overlap, so the 40-test BH q-values understate the true FDR.

【Why it matters】 The manuscript's core positive contribution — "established ECM/mechanotransduction gene sets retain tissue specificity in pain" — is presented as the "most substantive result" (line 83). Given the above, it is better characterized as *suggestive but under-powered*: two sets (G1, G5) show a real, significant DRG shift; the other two "retained" sets are weak; and the design cannot rule out that the apparent specificity is partly a blood-low-power artefact. Presenting it as a confirmed finding risks over-claiming.

【Specific fix】 Add a Limitations paragraph (or strengthen the existing one) that explicitly states: (i) Layer 3 inputs are n = 3 summary statistics, so the specificity conclusions are hypothesis-generating, not confirmatory; (ii) only G1 and G5 show BH-significant DRG shifts — the 4/5 "retained" count includes one marginal (G3) and one denominator-artefact (G4) set; (iii) the 5 sets are overlapping/non-independent, so BH q-values are a lower bound on FDR; (iv) "0/40 in blood" partly reflects blood's smaller mapped gene count and lower power. Recast the "most substantive result" sentence to "suggests retained specificity, driven chiefly by G1 and G5, and requiring sample-level replication."

---

## § Stands up (things I verified and found correct)

1. **BH arithmetic is correct.** I re-ran Benjamini–Hochberg over the 40-test family and reproduced G1 DRG×SNI q = 0.0009999 (≈ 0.0010), G5 DRG×SNI q = 0.00159984 (≈ 0.0016), and the 8/40 survival count exactly as reported (manuscript lines 71, 83; `layer3_generality.json` lines 63–64, table).
2. **Stage A matched numbers are accurately transcribed.** DRG×SNI matched MRU = 0.71677 / P = 0.10229 / q = 0.40916 and BLD×SNI MRU = 0.6964 / P = 0.10039 / q = 0.40916 (`layer1_diag.json` lines 234–237, 190–193) match the manuscript's 0.717 / 0.102 / 0.409 and 0.696 / 0.100 / 0.409.
3. **The positive control genuinely validates the pipeline.** Identical-code detection of the 12-gene injury set at g = 3.85, P = 0.0286 (`layer2_positive_control.json` lines 54–59) is a real, well-executed sensitivity check; the pipeline is demonstrably not broken.
4. **Pre-specification discipline is real and praiseworthy.** The frozen protocol (`ms_panel.json`) pre-defines the SI_g definition, the primary rule (≥ 4/5 fail), the §5.3 governance, and the positive-control selection basis (literature-only, no expression results from the project). This is stronger than most reanalyses and should be preserved.
5. **G1 and G5 DRG×SNI shifts are large and credible.** MRU = 0.9056 (p = 9.999e-05) and 0.8857 (p = 0.0002) are strong, reproducible signal; these two sets are the legitimate core of the Layer-3 positive finding.

---

## § Questions for the authors

1. For G4, what is the bootstrap/Monte-Carlo uncertainty on the BLD×SNI MRU = 0.4991 given n = 3 input? Could you report a 95% interval for SI_g, or simply present the absolute shifts (DRG |Δ| = 0.222, BLD |Δ| = 0.001) instead of the ratio?
2. The 5 benchmark sets overlap in membership (e.g., G1∩G5 share FN1, COL1A1, SPP1, ACTA2, CTGF, TIMP1). Did you assess the effective number of independent tests? Would a Benjamini–Yekutieli (dependency-robust) adjustment change which of the 8 tests survive?
3. In Stage B, with exact-permutation lower bound P ≈ 0.029 at n = 4-vs-4, what is the minimum Hedges g the design could detect at 80% power? Is the HD_up non-result consistent with a true moderate effect (g ≈ 0.3–0.6) that the design simply cannot see?
4. Why is §5.3 (triggered by a *significant* negative control) applied to the double-null Stage A? Was the "uninformative" label intended to mean "negative and underpowered," or is there a separate governance clause I should be citing?
5. The "0/40 significant in blood" — given blood's much smaller mapped-present gene counts (20–61 vs ~64 in DRG/SC), isn't the absence of blood significance at least partly a power effect rather than evidence of DRG-over-blood specificity?

---

## § What I actually checked

Files read:
- `manuscript/manuscript.md` (full) — primary claims at lines 12, 29, 35, 44, 56–57, 62, 71, 83, 91, 95, 121, 137, 140.
- `analysis/results/layer3/layer3_generality.json` (full) — per_set_specificity (G4 lines 46–51), table rows for G4 DRG/BLD SNI (lines 417–429, 501–513), G1/G5 DRG SNI (lines 80–93, 529–541), n_surviving_BH_0.05 (line 63), min_q (line 64).
- `analysis/results/layer1/layer1_diag.json` (Stage A matched values) — DRG×SNI (lines 234–237), BLD×SNI (lines 190–193).
- `analysis/results/layer2/layer2_positive_control.json` (full) — positive control (lines 54–59), HD_up (lines 110–115).
- `analysis/config/ms_panel.json` (frozen protocol) — Layer 3 primary rule, SI_g definition, positive-control selection basis, BH family definition.

Computations performed (values recomputed from the JSONs, not taken from the manuscript):
1. **G4 SI_g:** |ΔDRG−0.5| = 0.22239618, |ΔBLD−0.5| = 0.00092483, SI_g = 0.22239618 / 0.00092483 = **240.47** (manuscript 240.5 ✓). Instability table generated: BLD MRU ±0.002 → SI_g 55–111; ±0.001 → 222; →∞ at 0.5000.
2. **G4 component significance:** DRG×SNI matched p = 0.2256 (q = 0.3533, **not significant**); BLD×SNI MRU = 0.4991, p = 0.9976 (no shift). Confirms the ratio is a denominator artefact.
3. **Layer-3 BH:** re-ran BH over all 40 p_matched values. Reproduced G1 DRG×SNI q = 0.0009999, G5 DRG×SNI q = 0.00159984, and 8/40 survivors exactly. Listed the 8 survivors; noted 2 are in BRN, and that the q-values answer "shift ≠ 0.5" not "DRG > blood."
4. **17.6-fold gap:** 3.8535 / 0.2187 = **17.62** (manuscript 17.6 ✓); both from identical-code runs (verified).
5. **Stage A matched values:** DRG×SNI MRU = 0.71677 / P = 0.10229 / q = 0.40916; BLD×SNI MRU = 0.6964 / P = 0.10039 / q = 0.40916 — match manuscript 0.717/0.102/0.409 and 0.696/0.100/0.409. Both non-significant, so the §5.3 "equally significant" trigger is not met.

Discrepancies found vs the manuscript:
- **None in arithmetic** for the recomputed values (SI_g, BH q, Hedges-g ratio, Stage A matched stats) — these are faithfully transcribed.
- **Interpretive overstatements** (not arithmetic errors): (a) G4 SI_g = 240.5 presented as strong specificity when it is a denominator≈0 artefact; (b) "8/40 BH-significant" used to support DRG-vs-blood *specificity* when BH only shows shift-vs-0.5; (c) only 2 of 4 "retained" sets have a significant DRG shift; (d) "17.6-fold gap" framed as a bounded-null calibration when it only rules out gross pipeline failure; (e) §5.3 misapplied to a double-null, producing an "uninformative" label that overstates the situation; (f) the 5 sets are overlapping/non-independent, making the BH q-values anti-conservative, which is not acknowledged.
