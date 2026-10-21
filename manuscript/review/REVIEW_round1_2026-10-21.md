# REVIEW_round1 — Independent Review Panel Consolidation (2026-10-21)

## 1. Independence statement
Four experts (A1 Domain, A2 Design/Biostatistics, A3 Implementation/Auditor, A4 Venue/Editor) were briefed from a single shared brief (`_PANEL_BRIEF.md`) that forbade reading each other's outputs and any prior review/response files. Each recomputed key numbers from raw `analysis/results/**` JSONs with their own script. **Independence worked**: the most severe finding — the title contradicts the paper's own Layer-3 result (only 1/5 sets fail specificity, not "across five sets") — was hit independently by A1 and A4 from different angles (biology vs reporting-standards). A3 and A2 independently confirmed the numeric substrate is sound, so the defect is at the *design/interpretation* layer, not arithmetic — exactly what a gate cannot catch.

## 2. Verdict table
| Expert | Verdict | Basis |
|---|---|---|
| A1 Domain | Major revision | Title contradiction + over-claim "conserved core"; biology defensible after fixes |
| A2 Design | Major→Minor | No fatal flaw; robustness attribution must be fixed |
| A3 Implementation | Accept (minor) | All numbers trace; 3 presentation nits |
| A4 Venue | Major revision | Title + placeholder data-availability are blockers |

**Distribution**: 2 Major, 1 Major→Minor, 1 Accept(minor). No DESK-REJECT; the article is salvageable with targeted revision.

## 3. Cross-verification table (manuscript claim vs independently recomputed JSON)
| Location | Claim | JSON value | Checked by | Verdict |
|---|---|---|---|---|
| Layer 0 | HD_up=18, HD_down=41 | 18 / 41 | A3 | match |
| Layer 0 | CTGF Δ=+1.64, P=9.5e-6 | recomputed match | A1,A3 | match |
| Layer 0 | LATS HD 79.7% / HI 28.6% | 0.797 / 0.286 | A3 | match |
| Stage A | DRG×SNI MRU 0.717, P 0.102, q 0.409 | 0.7168/0.1023/0.4092 | A2,A3 | match |
| Stage A | BLD×SNI MRU 0.696, P 0.100, q 0.409 | 0.6964/0.1004/0.4092 | A2,A3 | match |
| Stage B | HD_up diff 0.146, P 0.80, g 0.219 | match | A3 | match |
| Stage B | HD_down diff 0.397, P 0.0286, g 2.658, q 0.086 | match | A3 | match |
| Stage B | Positive control diff 1.285, P 0.0286, g 3.85 | match | A3 | match |
| Layer 3 | SI 38.4/0.44/1.44/240.5/9.06; fail 1/5 | match | A1,A2,A3 | match |
| Layer 3 | 8/40 BH-sig, all DRG/SC/BRN, blood 0 | match | A2,A3 | match |
| Layer 3b | 7-row table | exact | A3 | match |
| Layer 4 | 15345 tested, 8 up, ECM-union 0 | match | A3 | match |

No numeric discrepancy found by any reviewer.

## 4. Graded issue list
**Tier 0 (conclusion-affecting / blocker)**
- **T0-1 Title contradiction** (A1, A4). Title asserts "tissue specificity fails across five independent ECM/mechano gene sets," but Layer-3 shows 1/5 fail; 4/5 *retain* specificity. Re-title to match the reframed conclusion.
- **T0-2 Data-availability placeholder** (A4). "(named repository URL + tag v1.0.0)" has no real URL; GigaScience blocks. Resolve in final packaging (create repo, tag, fill URL).

**Tier 1 (must fix before acceptance)**
- **T1-1 Robustness misattribution** (A2). LOO + Q4 (P=0.092) belong to HD_down (layer2_robustness.json, n=33), not HD_up. Re-attribute; do not imply HD_up has a separate robustness artifact.
- **T1-2 SI fragility** (A1, A2). SI_g explodes for near-zero blood shift (G4=240.5 denominator 0.0009; G1=38.4 denominator 0.011). Add |ΔDRG| and |ΔBLD| absolute columns to Table 3 + stabilizing footnote; do not read SI as specificity *strength*.
- **T1-3 "Conserved mechanical core" overstatement** (A1). Only 4/18 HD_up members are canonical YAP/TAZ targets (CTGF/CYR61/ANKRD1/AMOTL2); rest heterogeneous. Soften wording in Layer 0 and Discussion.
- **T1-4 Input-mismatch competing explanation omitted** (A1). Cross-cell-type failure could reflect mechanical *input* mismatch (culture-substrate fibronectin stiffness vs nerve compression/perineural fibrosis), not only cell type. Add to Discussion Limitations.
- **T1-5 Abstract over cap** (A4). ~358 words; trim to ≤350 (target ~330).
- **T1-6 Discussion opening mis-groups Layer-3** (A4). "did not confirm engagement" lumps Layer-3 (whose FAIL = specificity *retained*) with the HD_up nulls. Rephrase for clarity.
- **T1-7 LATS confirmation method opaque** (A1). Define the "directional confirmation" rule in Methods.

**Tier 2 (clarity / reporting)**
- **T2-1** Print the Layer-3b 7-row table (A3); currently only prose.
- **T2-2** Cross-reference HD_up & positive-control numbers between Stage B and Layer 3b to avoid implying 7 independent tests (A3).
- **T2-3** "equally significant" → "equally non-significant" for Stage A (A2).
- **T2-4** Add citations for the post-hoc ECM-structure vs YAP/TAZ separation (A1).
- **T2-5** Reconcile protocol §8.1 stale BLD q (A4) — manuscript correct, protocol text stale.
- **T2-6** Add `layer1_results.json` and `layer2_results.json` to MANIFEST so unstratified 0.597/0.0009 and HD_down q=0.086 are verifiable (A3).

**Tier 3 (resolved non-issues)**
- A4's "orphan fig2_member_contributions.png" is a misread: the file is `fig3_member_contributions.png` (Fig 3) and `fig2_per_animal_scores.png` (Fig 2); all 6+1 figures are referenced. No action.

## 5. Consensus / complementarity / disagreement
- **Consensus**: numeric substrate sound; §5.3 and §11.2 respected; reframed conclusion scientifically defensible in *direction*. The title is the single biggest defect.
- **Complementarity**: A1 (biology) + A4 (reporting) independently found the title defect; A2 (design) found the robustness attribution that A3 (implementation) had flagged as "redundancy"; A3 supplied the numeric proof base for everyone.
- **Disagreement**: none material. A2 rated Major→Minor (no fatal flaw); A1/A4 rated Major (title+URL blockers). Adopted stricter: title and URL are blockers.

## 6. Priority must-fix list (DESK-REJECT flags)
1. **[BLOCKER]** Re-title (T0-1).
2. **[BLOCKER]** Real repository URL + tag + MANIFEST (T0-2, Task #16).
3. Re-attribute robustness to HD_down (T1-1).
4. Add absolute-shift columns to Table 3 (T1-2).
5. Soften "conserved core" + add input-mismatch caveat (T1-3, T1-4).
6. Trim abstract (T1-5); fix Discussion opening (T1-6); define LATS rule (T1-7).

## 7. What stands up (do NOT change)
CTGF anchor; §5.3 "uninformative" framing; Stage B bounded-null vs positive-control sensitivity (the paper's strongest asset); Layer-3 primary FAIL honestly reported; all 10 references genuine; HD_down and Layer 3b/Layer 4 correctly labelled hypothesis-generating/FAIL; positive-control intersection=0 (no circularity).

## 8. Recommended handling
**A) Restructure-and-resubmit as the same article type (Research Article).** The strongest real contribution is the *prospective, positive-control-governed, anti-HARKing audit framework* plus the finding that expression-stratification *recovers* specificity that naive projection hides, and that cross-cell-type signature transfer fails due to cell-type/input specificity — not method uselessness. Swap the headline from "universal projection failure" (disproven) to "cell-type-specific transfer failure with preserved specificity of established sets." This converts a fragile signal into a stable methodological/报告学 finding.

## 9. Process lessons
- A 39/39 green gate certified arithmetic, not design. The title defect escaped the gate. New gate assertions needed: (i) a `title_consistent_with_layer3_verdict` check (title must not assert universal failure when fail-count<4); (ii) a `robustness_attribution` check that the manuscript's robustness JSON n_members matches the signature it is attributed to. These extend coverage to the design layer the panel caught.
