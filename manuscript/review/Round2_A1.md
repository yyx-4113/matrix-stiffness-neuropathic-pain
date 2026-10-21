# Round-2 Review — A1 (Domain Expert: mechanobiology / pain neuroscience)

**Blind design:** I did not read any other reviewer's Round-2 output. I read the post-R1 manuscript, my own R1 review (`A1_domain.md`), the consolidated fix list (`REVIEW_round1_2026-10-21.md`), and the two source JSONs (`layer0_signature.json`, `layer3_generality.json`). All key numbers were recomputed/verified against the JSONs and match the manuscript exactly (CTGF Δ=+1.64/P=9.5e-6; HD_up=18/HD_down=41; LATS HD=79.7%/HI=28.6%; Layer-3 SI 38.4/0.44/1.44/240.5/9.06; n_fail=1).

---

## 1. Round-1 points — RESOLVED / UNRESOLVED

| # | Round-1 concern | Status | Evidence in revised manuscript |
|---|---|---|---|
| 1 | Title contradicted own Layer-3 result ("fails across five sets" vs 4/5 retain) | **RESOLVED** | New title (manuscript.md:1): *"A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity."* Matches data (1/5 fail). |
| 2 | SI ratio fragile (G4=240.5, G1=38.4 from near-zero blood shift) | **RESOLVED** | Table 3 (lines 132–140) now prints `\|ΔDRG−0.5\|` and `\|ΔBLD−0.5\|` columns and carries the footnote: *"SI is unstable when \|ΔBLD−0.5\| ≈ 0 … read the absolute shifts directly."* SI is no longer presented as specificity strength. |
| 3 | "Conserved mechanical core" overstated (only 4/18 canonical) | **RESOLVED** | Layer 0 (line 54) now states the set's "core" is *mechanistic rather than a uniform set of canonical targets*, and explicitly lists only CTGF/CYR61/ANKRD1/AMOTL2 as the 4 canonical CTGF-class effectors among 18. |
| 4 | Input-mismatch competing explanation omitted | **RESOLVED** | Limitations (line 95): *"The mechanical input also differs … culture-substrate fibronectin stiffness vs nerve compression / perineural fibrosis in vivo — so cell-type and mechanical-input mismatches are confounded and cannot be separated here."* |
| 5 | "ECM literature not disproven" defense undercut by old title | **RESOLVED** | Conclusions (line 16) and Core conclusion #3 (line 92) both state literature "ECM enrichment in pain" findings are *not invalidated / not disproven*, only *circumscribed to the source cell type*. Consistent with new title. |
| 6 | Post-hoc "structural ECM vs YAP/TAZ separation" lacks DRG/YAP–TAZ citations (T2-4) | **UNRESOLVED (minor)** | References still #1–#10; no new citation added for the post-hoc ECM-structure vs YAP/TAZ-stiffness-response separation in DRG/pain, and no explicit "we found no direct contrast literature" statement. |
| 7 | LATS confirmation method opaque (T1-7) | **RESOLVED (partial)** | Methods Layer 0 (line 34) now defines directional confirmation: *"the sign of the WT stiffness response agreed between the WT estimate and the YAP/TAZ-dKO (or LATS-dKO) estimate … blunted, not reversed."* Accurate to the requested definition. Residual: the explicit magnitude threshold (e.g. \|Δ_LATS\| ≤ 0.5\|Δ_WT\|) is still implicit, not printed. |

**Round-1 KEY CONCERNS (as listed in the task) — all verified:**
- Title matches results ✓
- Discussion/Conclusions frame Layer-3 as "specificity RETAINED; failure signature- and cell-type-specific, NOT universal" (lines 16, 72, 85, 92) ✓
- LATS confirmation definition accurate (line 34) ✓
- Positive-control 12-gene markers (g=3.85, P=0.0286) run through identical pipeline, framed as "validates pipeline sensitivity" only — no over-claim ✓
- HD_down presented as hypothesis-generating only (lines 64, 124, 95) ✓

---

## 2. NEW domain issues (with manuscript quotes)

**NEW-1 (moderate, wording). "Cell-type-specificity limit of *mechanotransduction*" over-generalizes.**
- Quote (Discussion, line 87): *"this is most parsimoniously a **cell-type-specificity limit of mechanotransduction** (HEK293A epithelium ≠ sensory neuron/glia) rather than evidence that pain-ECM findings are artifacts."*
- The Hippo/YAP–TAZ pathway is itself *not* cell-type-specific (Dupont 2011, ref #4, is cited as the general mechanism). What fails to transfer is this particular *epithelial, fibronectin-substrate-stiffness* program. The Limitations paragraph (line 95) correctly frames it as a confounded cell-type **and** mechanical-input mismatch, but the Core-conclusion narrative (lines 87, 92) names "mechanotransduction" as cell-type-specific, which is biologically misleading. Recommend rephrasing to *"a limit of this epithelial Hippo/stiffness program's cross-cell-type transfer"* and dropping the word *mechanotransduction* as the thing that is cell-type-specific.

**NEW-2 (minor, honesty nuance). "Established ECM sets retain tissue specificity" vs Layer-3b/Layer-4.**
- The Layer-3 "specificity retained" claim (G1/G5 DRG MRU 0.906/0.886, q=0.001) is at the **summary-statistic, direction-of-shift** level (GSE111216). But Layer-3b (line 78) and Layer-4 (line 78) show that at the **sample level (GSE261676)**, 0/5 ECM sets are significantly *upregulated* in injured DRG and the ECM-union contributes 0 significant-up genes. These are genuinely different endpoints (direction-of-rank-shift vs injury-upregulation) and the manuscript keeps them separate, so the circumscription argument remains internally honest. However, a reader could conflate "retain specificity" with "activate in pain DRG." Suggest one clarifying sentence in Discussion that the Layer-3 specificity is a *relative direction* signal, not evidence of injury-induced ECM upregulation at sample level — to pre-empt misreading.

**NEW-3 (very minor). "Refuting the hypothesis that projection statistics inherently fail" (line 85).**
- Logically supported (≥4/5 failing was the pre-specified universal-failure test; only 1/5 failed), and hedged as "refuting the hypothesis" rather than "proving projection works." Acceptable, but note G3's SI=1.44 is only marginally >1, so "4/5 retained" rests partly on a thin margin for G3. Already mitigated by the Table-3 absolute-shift columns. No action required beyond current hedging.

---

## 3. Targeted questions answered

**(a) Is "HEK293A epithelium ≠ sensory neuron/glia is a cell-type-specificity limit" defensible?**
Defensible *as a parsimonious hypothesis*, and the manuscript now honestly pairs it with the mechanical-input-mismatch caveat in Limitations (line 95). It is **not** defensible to call it a limit of *mechanotransduction* per se (NEW-1). The source-cell-type circumscription of the null is the sound part; the "mechanotransduction is cell-type-specific" phrasing is the weak part.

**(b) Is "ECM enrichment in pain literature not disproven, only circumscribed to source cell type" honest?**
**Yes — honest and well-supported.** The null is specific to the HEK293A-derived HD_up *controlled stiffness* signature; Layer-3 independently shows generic ECM/mechano sets (G1/G4/G5) retain DRG-over-blood specificity, which is directionally consistent with Parisien 2019. The logic chain "controlled signature fails to transfer ⇒ only that program's interpretation is circumscribed, not the broad literature" holds. The only refinement needed is the NEW-2 clarification so readers don't equate "specificity retained" with "upregulated post-injury."

---

## 4. VERDICT

**MINOR REVISION**

All Round-1 blockers (title contradiction) and major domain concerns are resolved or adequately mitigated; numbers fully verified against source JSONs. Remaining items are minor: (i) add DRG/YAP–TAZ or pain-ECM-stiffening citations (or an explicit "no direct contrast literature found" statement) for the post-hoc separation claim (T2-4, UNRESOLVED); (ii) soften "cell-type-specificity limit of *mechanotransduction*" to a program/context-specific framing (NEW-1); (iii) optionally add one sentence distinguishing Layer-3 direction-specificity from Layer-3b/Layer-4 injury-upregulation (NEW-2). No biological misconduct, no data discrepancy, no remaining contradiction between abstract/results/discussion.
