# Editor's Consolidated Review — Round 3 (journal-editor-organised independent panel)

**Manuscript:** "A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity"
**Target venue:** PLOS ONE (Research Article / reanalysis)
**Editor:** journal-editor role (this file). Panel: A1 Domain, A2 Design/Stats, A3 Implementation/Provenance, A4 Venue/Editor.
**Date:** 2026-10-21

---

## 1. Independence statement

Four reviewers were briefed from a shared `_PANEL_BRIEF.md` that (a) forbids reading any prior `REVIEW_*.md`, the old brief, the author's `audit_round*.json`, README/memory, or each other's outputs, and (b) requires every numeric claim to be recomputed from source. Each wrote independently to `manuscript/review/round3/A{1-4}_*.md`. No reviewer had access to another's file.

**Evidence it worked:** the four reviewers converged on several defects from different angles (A1 domain + A2 stats both flag G1/G5 overlap and G4 denominator instability; A2 stats + A3 provenance both flag the G4 table-presentation trap; A4 venue + A2 both flag the "4/5 retained" front-matter over-claim) while also surfacing complementary, non-overlapping findings (A1's G3 mislabel and Piezo/TRP gap; A3's unstratified-P collision and CTGF deposit gap; A4's Ethics/figure-legend compliance). The cluster on already-known issues was *absent* — this is a genuine independent pass.

As editor I independently reproduced the single most severe cluster with my own script reading only raw sources (no reviewer intermediate): G4 denominator instability (SI 45→2958 for a ±0.004 blood-MRU perturbation), G1∩G5 = 10/23 (43%), and G3's ion-channel composition (8/22). All three are **confirmed**.

---

## 2. Verdict table

| Reviewer | Role | Recommendation | One-line basis |
|---|---|---|---|
| A1 | Domain (pain/ECM/mechano) | Major revision | G3 mislabel + G1/G5 overlap + "sensitivity-validated" scope too broad; none fatal |
| A2 | Design/Stats | Major revision | G4 denominator artefact; BH conflates "shift≠0.5" with "DRG>blood"; §5.3 misapplied; "17.6× bounded null" invalid |
| A3 | Implementation/Provenance | Minor revision | Every headline number traces cleanly; only hygiene (G4 rounding, unstratified-P collision, CTGF deposit gap, abstract margin) |
| A4 | Venue/Editor | Minor revision | All issues are PLOS ONE reporting/format compliance; science sound and on-remit |

**Distribution:** 0 reject / 0 desk-reject / 2 major / 2 minor. The two "Major" verdicts are driven by *interpretive overstatement of the Layer-3 positive claim* and the *§5.3 misapplication* — both are wording/analysis-framing fixes, not new experiments. The two "Minor" verdicts are compliance/hygiene. **Net: the manuscript is scientifically sound and a strong PLOS ONE fit; it needs one substantive reframing pass plus a compliance pass, not reanalysis.**

---

## 3. Cross-verification table (manuscript claim vs independently recomputed)

Every headline number was recomputed by ≥1 reviewer (and the worst cluster by the editor). All arithmetically faithful.

| # | Manuscript location | Manuscript claim | Independently recomputed | Checked by | Verdict |
|---|---|---|---|---|---|
| 1 | Abs / L0 / Disc | CTGF Δ=+1.64, P=9.5×10⁻⁶ | 1.6405 / 9.494e-6 | A1,A3 | ✓ match |
| 2 | L0 | HD_up n=18, HD_down n=41 | counted 18 / 41 | A1,A3 | ✓ match |
| 3 | L0 | LATS conf 79.7% HD / 28.6% HI | 0.7966 / 0.2857 | A1,A3 | ✓ match |
| 4 | Stage A / Tbl2 | DRG×SNI MRU=0.717, P=0.102, q=0.409 | 0.71677 / 0.10229 / 0.40916 | A2,A3 | ✓ match |
| 5 | Stage A / Tbl2 | BLD×SNI MRU=0.696, P=0.100, q=0.409 | 0.6964 / 0.10039 / 0.40916 | A2,A3 | ✓ match |
| 6 | Stage B / Tbl2 | HD_up +0.146, P=0.80, g=0.219 | 0.14645 / 0.8 / 0.2187 | A2,A3 | ✓ match |
| 7 | Stage B / Tbl2 | Positive ctrl +1.285, P=0.0286, g=3.85 | 1.28536 / 0.028571 / 3.8535 | A2,A3 | ✓ match |
| 8 | L3 / Tbl3 | G1/G2/G3/G4/G5 SI = 38.4/0.44/1.44/240.5/9.06 | 38.416/0.4402/1.438/240.47/9.055 | A1,A2,A3 | ✓ match (G4 unstable) |
| 9 | L3 / Tbl3 | G1 q=0.0010, G5 q=0.0016 | 0.0009999 / 0.0015998 | A2,A3 | ✓ match |
| 10 | L3 | 8/40 BH-significant, all DRG/SC/BRN, blood 0 | 8 survivors, none blood | A2,A3 | ✓ match |
| 11 | L3 / Tbl3 | G4 BLD MRU=0.4991 (|Δ|=0.0009) | 0.499075 (|Δ|=0.000925) | **Editor** | ✓ full-precision; printed 4-d.p. gives 247.1≠240.5 (table artefact) |
| 12 | L4 / Tbl2 | 8/15345 up, 3 down, ECM-union sig-up=0, OR=0, P=1.0 | identical | A3 | ✓ match |
| 13 | Abs | 298 words, non-structured | 298, no headings | A3,A4 | ✓ match |
| 14 | L3 config | "five independent sets" | G1∩G5 = 10/23 (43%) | **Editor / A1** | ✗ overstated independence |
| 15 | L3 config | G3 = "mechanosensing adhesome" | 8/22 are ion-channel genes | **Editor / A1** | ✗ mislabel |

The **only** numeric discrepancy is the G4 printed-denominator trap (Table 3 footnote already discloses it). No headline number is fabricated or internally inconsistent.

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating
**None.** The core negative conclusion (HEK293A stiffness signature does not transfer to pain tissue; honest bounded null) is robust and not challenged.

### Tier 1 — analyses / claims to change (substantive)
- **T1-1 (Layer-3 overclaim).** The headline "4/5 retain specificity" and "most substantive result" rest on G4 (denominator artefact) and on G1/G5 (43% overlapping). Demote to: *suggestive, driven chiefly by G1 and G5 (BH-significant DRG shift); G3 marginal; G4 a denominator artefact; sets overlapping so the 40-test BH q is anti-conservative.* Add a Limitations paragraph stating Layer-3 inputs are n=3 summary stats → hypothesis-generating, not confirmatory. *(A1-2, A2-1, A2-2, A2-5)*
- **T1-2 (§5.3 misapplication).** Stage A is a *double null* (both DRG and BLD q=0.409, non-significant); the §5.3 trigger ("negative control equally *significant*") is not met. Change "uninformative by §5.3" → plain negative/underpowered result (DRG≈BLD, no tissue-specific engagement). *(A2-4)*
- **T1-3 ("17.6× bounded null" recast).** The Hedges-g gap validates the pipeline against *gross* failure but does not bound the size of a true HD_up effect (exact-perm lower bound P≈0.029 ⇒ only very large effects detectable). Reword to "sensitivity-validated, not tightly bounded." *(A2-3)*
- **T1-4 (G3 mislabel + Piezo/TRP gap).** Rename G3 to "mechanosensitive channels + focal-adhesion module," cite all three frozen sources, and add a Discussion paragraph engaging Piezo/TRP mechanotransduction-in-pain literature. *(A1-1, A1-7)*
- **T1-5 (G1/G5 independence).** Report all pairwise overlaps (or describe G1/G5 as one matrisome/fibrosis module); reword "4/5 independent" accordingly. *(A1-2)*
- **T1-6 (Table 3 citations).** Cite all frozen sources per set (G2→Dupont 2011+Cordenonsi 2011+Zhao 2008; G3→Coste 2010+Ranade 2014+Zaidel-Bar 2007; G4→Ohashi 2017+Riento&Ridley 2003). The G2 canonical CTGF/CYR61 attribution belongs to Dupont/Cordenonsi, not Zhao. *(A1-3)*
- **T1-7 (AMOTL2).** Reword "four canonical CTGF-class YAP/TAZ effectors" → "three canonical YAP/TAZ–TEAD targets (CTGF, CYR61, ANKRD1) plus AMOTL2, a YAP/TAZ-binding regulator." *(A1-4)*
- **T1-8 ("Hippo-dependent" caveat).** Clarify YAP/TAZ–TEAD dependence is LATS-independent per Dupont 2011; define HD operationally as YAP/TAZ-dKO–abolished. *(A1-5)*
- **T1-9 (positive-control scope).** The 12-gene injury control was run only through the *sample-level* Stage B pipeline, not the MRU/summary-statistic machinery that produced Stage A and all of Layer 3. Scope the "sensitivity-validated pipeline" claim to the sample-level arm, OR add an MRU-level positive control. *(A1-6, A1-8)* — **Editor decision: scope the claim** (no new analysis required; cleaner for a minor-revision path).

### Tier 2 — wording / provenance hygiene
- **T2-1 (Ethics MUST-FIX for PLOS ONE).** Expand to state IRB approval not required (secondary analysis of public de-identified data), source GEO deposits held their own approvals, no privacy risk. *(A4-2)*
- **T2-2 (cover letter "correction" → "refinement that circumscribes").** Align with manuscript's "circumscribes…without disproving." *(A4-6)*
- **T2-3 (title/abstract G4 caveat).** Add denominator-instability caveat to the front-matter positive clause; expand DRG/SNI/BLD/MRU/BH/SI_g on first appearance. Trim ~15 words for 300-word headroom. *(A4-1, A4-7; A3-4)*
- **T2-4 (Table 3 G4 denominator).** State full-precision denominator 0.000925 in the footnote; SI computed from full precision. *(A3-1)*
- **T2-5 (Stage A unstratified-P semantics).** One sentence clarifying the three coexisting P values (full-background 0.597/0.0009 vs diag matched-space unstratified 0.055/0.085 vs expression-matched primary 0.102). *(A3-2)*
- **T2-6 (CTGF deposit gap).** State in Data Availability that Δ is the regenerated WT contrast and that the per-replicate FPKM source is deposited so it can be reproduced; if raw FPKM is not yet deposited, deposit it. *(A3-3)*
- **T2-7 (Figure Legends section + "S1 Fig").** Add a dedicated Figure Legends section; rename "Figure S1" → "S1 Fig." *(A4-8)*
- **T2-8 (references "DOI:" → "doi:").** Cosmetic. *(A4-5)*
- **T2-9 (Funding/Competing standard phrasing).** "The author received no specific funding for this work." / "The author has declared that no competing interests exist." *(A4-4)*
- **T2-10 (Layer 3b PC BH q=0.200 note).** One line that 0.200 is the 7-set BH adjustment and does not contradict the Stage B sensitivity pass. *(A3-Q5)*

### Tier 3 — format
Absorbed into T2-7 / T2-8 / T2-9 / T2-3.

---

## 5. Consensus / complementarity / disagreement

**Consensus:** (i) the pre-specification discipline is genuine and praiseworthy and must be preserved; (ii) the core negative result is sound; (iii) the Layer-3 *positive* claim is overstated and must be demoted; (iv) no fabricated numbers — provenance is clean. **Complementarity:** A1 supplied the biological mislabels/attributions; A2 the statistical interpretation errors; A3 the provenance/hygiene traps; A4 the venue compliance. Each reviewer's blind spot was covered by another (e.g., A3 found no fabrication and could have concluded "accept," but A2's interpretive findings raise it to major; A4 found only compliance issues, but A1/A2 supply the scientific substance).

**Disagreement:** A3/A4 verdict "minor" vs A1/A2 "major." **Editor adjudication:** adopt the stricter (major) for the *scientific* framing (T1-1…T1-9 must be done), because A3/A4 scoped their "minor" to *their layer* (provenance clean / compliance only) and explicitly defer the scientific-claim assessment to others. The manuscript cannot be accepted with the Layer-3 overclaim and §5.3 misapplication standing. The "major" is a *reframing* major, not a *new-analysis* major — compatible with a single round of revision.

---

## 6. Priority must-fix list (with DESK-REJECT flags)

**DESK-REJECT flags:** **None.**

**Must-add-analysis vs must-reword split:**
- **Must reword (no new data):** T1-1, T1-2, T1-3, T1-4 (rename+cite+discuss), T1-5, T1-6, T1-7, T1-8, T1-9 (scope), T2-1…T2-10.
- **Must add artifact (cheap):** T2-6 (deposit/state raw FPKM source for CTGF anchor). T1-9 alternative (MRU-level positive control) is *optional* — scoping is accepted instead.

---

## 7. What stands up (do NOT change)

- Pre-specification / frozen protocol structure (preserve verbatim).
- CTGF Δ=+1.64/P=9.5e-6 and the L0 biological anchor; HD_up 18 / HD_down 41; LATS 79.7%/28.6%.
- Stage B positive control (g=3.85, P=0.029) as a genuine sensitivity check; HD_up bounded null (g=0.219, P=0.80).
- Layer-3 BH arithmetic (G1 q=0.0010, G5 q=0.0016, 8/40) — correct as computed; the *interpretation* (not the arithmetic) is what changes.
- Parisien 2019 description; cross-species/cell-type caveat (honest); the "circumscribes, does not disprove" framing.
- GEO accessions, repo URL+tag, checksummed MANIFEST (all internally consistent).

---

## 8. Recommended handling path

**A) Restructure-and-resubmit as the same article type (PLOS ONE Research Article reanalysis) — recommended.** The required changes are a reframing of the Layer-3 positive claim + correction of the §5.3/17.6× framings + the G3/gene-set citation fixes, plus a PLOS ONE compliance pass. No new experiment. After these, the manuscript is acceptable.

**B) Downgrade article type — not indicated.** The study is a legitimate reanalysis; no need to demote.

**C) Wording-only — not viable** as the *sole* route, because the Layer-3 overclaim and §5.3 misapplication are claim-level, not cosmetic.

---

## 9. Process lessons (what gates could not catch)

- **Gates verify arithmetic, not design.** The G4 denominator instability, the G1/G5 overlap, and the §5.3 misapplication are all arithmetically faithful to the JSONs — a consistency gate passing at 100% says nothing about them. The panel caught all three. **New gate assertions to add:** (a) report G4's SI instability band (e.g., "SI_g for G4 is undefined to within an order of magnitude; report absolute shifts"); (b) assert the 5 sets' pairwise overlaps are reported; (c) assert the §5.3 trigger condition is actually met before the "uninformative" verdict is issued.
- **Self-contradiction left by prior rounds:** the title/abstract positive clause ("4/5 retain specificity") is not retracted in the front-matter even though the body (Table 3 footnote) discloses G4's instability. A fresh independent panel caught this instantly. Rule reinforced: when a prior round adds a caveat in one section, check whether the headline statement itself was retracted or merely qualified.
- **"Independent sets" claim vs overlapping gene sets:** add a frozen assertion that pairwise overlaps are computed and reported.

---

## 10. Editor's reframe note to the author

The strongest claim that does *not* hold as written is the Layer-3 headline "established ECM/mechanotransduction gene sets retain tissue specificity (4/5)" — it is not your fault: it follows faithfully from a pre-specified SI_g rule, but that rule produces a denominator-unstable ratio for G4 and double-counts the overlapping G1/G5 module. The second finding you *buried* — that G1 and G5 (matrisome/fibrosis) show a real, BH-significant DRG shift, and that G3's ion-channel mechanosensors engage injured DRG — is actually your contribution and is more interesting than the generic "4/5" count. Swapping the framing (lead with "two real, significant DRG-shifts + an ion-channel mechanosensing signal; the generic 4/5 count is inflated by overlap and a ratio artefact") converts the paper from a fragile aggregated claim into a stable, specific structural finding — and that is exactly the soundness-only story PLOS ONE publishes.
