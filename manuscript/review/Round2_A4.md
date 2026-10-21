# Round-2 Review — A4 (Venue / Editor) — BLIND

**Manuscript:** `manuscript/manuscript.md`
**Target:** GigaScience (Oxford Academic / GigaScience Press). IF ~5.0. Open-data mandate; publishes large-scale biology, datasets, software, methodological / reanalysis articles.
**Round-1 role:** A4 Venue — reporting honesty, format/word/figure/table compliance, data-availability, Vancouver references, claim-strength red lines.
**Independence:** Blind review — did NOT read other reviewers' Round-2 outputs. Read manuscript, own Round-1 (A4_venue.md), consolidated fix list (REVIEW_round1_2026-10-21.md), README.md, CITATION.cff, LICENSE, and globbed `analysis/results/layer2/fig/` + `layer3/fig/`.

---

## 1. Round-1 points — RESOLVED / UNRESOLVED / PENDING

| # | Round-1 item | Verdict | Evidence (Round-2) |
|---|---|---|---|
| T0-1 | Title asserted universal specificity failure, contradicting Layer-3 (1/5 fail) | **RESOLVED** | New title (`manuscript.md:1`): *"A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity"*. Matches the reframed conclusion and Table 3 (only G2 fails; 4/5 DRG > blood). No more "fails across five sets" over-claim. |
| T0-2 | Data-availability URL is a placeholder | **PENDING-PACKAGING (acceptable)** | `manuscript.md:99` still reads "(named repository URL + tag v1.0.0)". Per the project plan this is a *packaging step* (real GitHub repo under yyx-4113 + MANIFEST + git tag v1.0.0 to be created next). The surrounding wording is correct: source GSE IDs (GSE98547/111216/261676) are named; "every numeric claim in this manuscript is traceable to a file under `analysis/results/`" is accurate. Flag ONLY if wording wrong → it is not. **Acceptable pending the real URL fill.** |
| T1-5 / Finding 3 | Abstract over the ≤350-word cap (~358) | **RESOLVED** | Re-counted: **Abstract = 308 words** (≤350 ✓); **Body = 1,835 words** excl. tables/captions (≤4,000 ✓). See §2. |
| Finding 2 / T1-6 | Discussion opening lumped Layer-3 primary with HD_up nulls | **RESOLVED** | `manuscript.md:84–85` now reads: *"Stage A (§5.3 verdict), Layer 3b, and Layer 4 did not confirm the hypothesised tissue-specific engagement, and the Layer-3 primary was also not met — but its non-meeting means specificity was retained, not lost (only 1/5 sets lacked specificity)."* The Layer-3 result is now correctly separated and framed as specificity *retained*. |
| Finding 5 | Unreferenced orphan figure file | **PARTIAL (non-blocking)** | The orphan `analysis/results/layer2/fig/fig2_member_contributions.png` **still exists** on disk but is NOT referenced in the manuscript. Consolidated review Tier-3 called this a misread, but the file is genuinely present. All 6 main (Fig 1–6) + 1 supp (Fig S1) figures are referenced and exist → figure set is complete. The stray file is a repo-hygiene nit, not a manuscript-text defect. |
| Finding 7 | Protocol §8.1 stale BLD q = 0.0072 | **MANUSCRIPT CORRECT / PROTOCOL-HYGIENE** | Outside the manuscript text; the manuscript reports matched BLD q = 0.409 correctly (`:14, 59, 121`). Protocol text reconciliation is not a manuscript blocker. Noted for completeness. |
| Finding 1 (MAJOR) | → superseded by T0-1 | **RESOLVED** | see T0-1 |
| Finding 4 (MAJOR/blocker) | → = T0-2 | **PENDING-PACKAGING** | see T0-2 |
| Finding 8 | 10 Vancouver refs authentic | **RESOLVED / STILL COMPLIANT** | see §3 |

**Summary of Round-1 status:** Both MAJOR blockers addressed — T0-1 fully resolved in-text; T0-2 acceptable as pending packaging. Abstract and Discussion fixes confirmed. No carried-over manuscript-text blocker remains from Round 1.

---

## 2. Word counts (md, recomputed)

- **Abstract:** 308 words (cap ≤350) → **PASS**.
- **Body** (Background → Declarations, excludes Tables, References, and `![...](...)` caption lines): 1,835 words (cap ≤4,000) → **PASS**.
- Structured abstract subsections within cap; no over-length risk.

---

## 3. References — Vancouver [1]…[10]

All 10 entries carry a real PMID **and** DOI; Vancouver format; each is actually used in text (datasets GSE98547→[1], GSE111216→[2], GSE261676→[3]; gene-set sources [5][6][7][8][9][10]; methods/mechanotransduction [4]). Spot-checked dataset source links:
- GSE98547 → [1] Meng 2018 *Nature* PMID 30135582 ✓
- GSE111216 → [2] Parisien 2019 *Pain* PMID 30763288 ✓
- GSE261676 → [3] Serafini 2024 *Neurobiol Pain* PMID 38549875 ✓

No "[?]", no placeholder, no orphan/decorative citation. Round-1 already independently verified #3/#9/#10 via PubMed. **COMPLIANT.**

---

## 4. Figure / table inventory

Referenced and physically present (paths verified):
- Fig 1 → `layer2/fig/fig1_signature_derivation.png` ✓
- Fig 2 → `layer2/fig/fig2_per_animal_scores.png` ✓
- Fig 3 → `layer2/fig/fig3_member_contributions.png` ✓
- Fig 4 → `layer2/fig/fig4_matched_null.png` ✓
- Fig 5 → `layer2/fig/fig5_positive_control_vs_signatures.png` ✓
- Fig 6 → `layer3/fig/fig6_generality.png` ✓
- Fig S1 → `layer3/fig/figS1_layer3b_effects.png` ✓

→ **6 main + 1 supplementary, all referenced and present.** Tables 1–4 all present and referenced. Stray unreferenced `fig2_member_contributions.png` noted (§1, non-blocking).

---

## 5. Editorial / packaging NEW-CHECK

**Byline / author metadata — PASS.**
- `manuscript.md:3`: "**Yongxin Yang** (ORCID 0009-0004-9698-6552)".
- `manuscript.md:4`: affiliation "The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China".
- No MD/PhD/Dr./Professor degree appended to the byline (user convention honored). ORCID and affiliation present and correct; also match CITATION.cff author block.
- Declarations (`manuscript.md:97–103`): Ethics, Data availability, Competing interests ("None declared."), Funding ("None."), Authors' contributions ("YY conceived, performed, and wrote the analysis and manuscript."), Acknowledgements. All present.

**Ethics statement — ADEQUATE (minor suggestion).**
- `manuscript.md:98`: *"This study used only public, de-identified transcriptomic datasets; no new human or animal subjects were enrolled."* Sufficient for re-use of public de-identified data. Suggest adding an explicit IRB/ethics-exemption note (e.g., "exempt from institutional review as it re-uses publicly deposited, de-identified data") to pre-empt editor questions. Non-blocking.

### NEW BLOCKER A — Repository scaffolding contradicts the manuscript's reframed conclusion (PACKAGING, MAJOR)
The data-availability package (README.md, CITATION.cff) is the artifact GigaScience readers are pointed to, yet it still carries a **superseded, contradictory** narrative and **stale/wrong numbers**:

- README.md:27 — *"Therefore the frequently reported 'ECM organisation enrichment' in pain transcriptomics **lacks demonstrated tissue specificity**…"*
  → Directly contradicts the manuscript title (`manuscript.md:1`), Results (`manuscript.md:73` "Only 1/5 sets lacked specificity"), and Discussion (`manuscript.md:85, 92` "established ECM/mechanotransduction gene sets **retain** tissue specificity", 4/5 DRG > blood). The manuscript's core reframed finding is the *opposite* of this README claim.
- README.md:12 — *"the blood negative control is **far more significant (P = 0.0009, q = 0.007)**"*
  → Contradicts the manuscript's §5.3-correct verdict: in the expression-matched null the blood control is **equally NON-significant** (MRU = 0.696, P = 0.100, q = 0.409; `manuscript.md:14, 59, 121`). README quotes the *unstratified, confounded* calibration as if it were the headline — exactly the misreading the manuscript warns against (`manuscript.md:59, 77`).
- README.md:13–14, 16 — positive-control **g = +4.43** and HD_up **g = +0.25** (17.6-fold gap).
  → Manuscript reports positive-control **g = 3.85** and HD_up **g = 0.219** (`manuscript.md:64`; also Table 4 g = 3.853 / 0.219). The README numbers do not match the manuscript or the cited `layer2_positive_control.json`.
- CITATION.cff:6–9 — abstract: *"no module survives expression-matched nulls or BH correction"* (older framing, omits the Layer-3 specificity-retention result).
- CITATION.cff:15 — `version: 0.1.0`, while the manuscript's data-availability statement promises tag **v1.0.0** (`manuscript.md:99`). Version mismatch.

**Why it blocks:** GigaScience mandates a coherent open-data package; a repository whose headline result and statistics contradict the paper (and carry wrong effect sizes) misleads readers and fails the "every numeric claim traceable / consistent" expectation. **Fix:** rewrite README "Headline result" + "What this project actually contributes" and CITATION.cff abstract to match the reframed conclusion (signature does NOT transfer; established ECM/mechano sets RETAIN specificity; blood control equally non-significant in the matched null; g = 3.85 / 0.219), and align version to v1.0.0.

### NEW BLOCKER B — "BH" abbreviation undefined on first use (MINOR, editorial)
- First use: `manuscript.md:14` (Abstract) — *"P = 0.102, **BH q** = 0.409"*. "Benjamini–Hochberg" is **never** spelled out anywhere in the manuscript (grep: "Benjamini" absent).
- Also at `manuscript.md:59, 64, 78`. **Fix:** expand at first use, e.g., "Benjamini–Hochberg (BH) q". Low risk but a routine editorial return item.

### Minor note — CFA undefined
- `manuscript.md:31`: "SNI and **CFA** models" — CFA (complete Freund's adjuvant) not expanded. SNI is defined later (`:39`). Suggest expanding both on first use. Cosmetic.

---

## 6. Scope fit for GigaScience

**YES — strong fit.** The article is a prospectively specified, two-stage reanalysis with (i) frozen endpoints / pre-registered governance (§5.3), (ii) open analysis code + MANIFEST of checksums, (iii) full traceability of every numeric claim to `analysis/results/`, (iv) a positive-control sensitivity test, and (v) an explicit methodological contribution (expression-matched null + coverage audit + positive control as required for projection analyses). This maps directly onto GigaScience's mandate for open-data, reusable, methodological/reanalysis articles. The reframed conclusion (cell-type-specific transfer failure with *retained* specificity of established sets) is a defensible, non-overclaimed methodological finding suitable for the venue.

---

## 7. VERDICT

**MAJOR** — *packaging-only*. The manuscript **body is now acceptable** for GigaScience: T0-1 (title) resolved, abstract/body within limits, Discussion reframing fixed, 6+1 figures and 4 tables complete, 10 references authentic, byline/ORCID/affiliation/degree-convention correct, ethics/competing-interests/funding/contributions declarations present, and §11.2 claim-strength red lines respected.

Two blockers remain, both fixable and outside the manuscript prose:
1. **T0-2** — real repository URL + tag v1.0.0 + MANIFEST must be filled (pending packaging; acceptable as scheduled).
2. **NEW BLOCKER A** — README.md / CITATION.cff must be reconciled to the reframed conclusion and corrected for stale/wrong numbers (blood P=0.0009 vs 0.100; g 4.43/0.25 vs 3.85/0.219; "lacks tissue specificity" vs "retains specificity"; version 0.1.0 vs v1.0.0).

Plus one trivial editorial nit (**NEW BLOCKER B**: define "BH" on first use) and a non-blocking orphan figure file. Resolve T0-2 and NEW BLOCKER A (and ideally B) before acceptance.
