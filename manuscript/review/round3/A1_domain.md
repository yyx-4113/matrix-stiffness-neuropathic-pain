# A1 — Domain review (pain / extracellular-matrix / mechanotransduction biology)

**Manuscript:** "A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity"
**Reviewer role:** Independent domain expert (pain / ECM / mechanotransduction biologist)
**Verdict in brief:** The central biological hypothesis (a human epithelial substrate-stiffness program should re-appear in injured mouse sensory tissue) is, as the authors concede, biologically weak a priori, and the honest "cell-type- and mechanical-input-specific" framing is defensible. However, three of the five Layer-3 gene sets are mislabeled, overlapping, or mis-cited, and the "sensitivity-validated" claim is scoped too broadly. None of these are fatal, but the generality benchmark and the provenance of the gene sets must be corrected before the "4/5 retained specificity" conclusion can stand as written.

---

## Item 1 — G3 is not an "adhesome," and its anchor citation (Coste 2010) is misattributed

**【Problem】** Layer-3 set G3 is labelled "mechanosensing adhesome [6]" and cited solely to Coste 2010, but Coste 2010 is the *Piezo1/2 ion-channel* paper, and G3 in fact mixes eight mechanosensitive ion-channel genes with focal-adhesion proteins.

**【Evidence】** The frozen gene-set definitions list G3 members as `PIEZO1, PIEZO2, TRPV4, TRPA1, TRPC1, TRPC6, KCNK2, KCNK4, VCL, TLN1, TLN2, ITGA1, ITGA5, ITGB1, ITGB3, PXN, ZYX, SRC, PTK2, CAV1, ACTN1, FERMT2` (config `ms_panel.json`, G3 block) — 8 of 22 are ion channels, not adhesome components. The source line credits Coste 2010 (Piezo), Ranade 2014, and Zaidel-Bar 2007, yet the manuscript Table 3 (manuscript.md:136) cites only "Coste 2010 [6]" and calls the set an "adhesome." The Discussion never mentions Piezo or TRP at all.

**【Why it matters】** This is the single most pain-relevant mechanosensing module the authors possess — Piezo and TRP channels are the canonical *in-vivo* mechanical-pain transducers — and it is buried under a vague "adhesome" label with a misleading single citation. It also breaches the brief's traceability requirement: the deposited source list and the manuscript table disagree.

**【Specific fix】** Rename the set to "mechanosensitive channels + focal-adhesion module" and cite all three sources in Table 3, or split it into a Piezo/TRP channel set and a focal-adhesome set. Add a Discussion paragraph stating what G3's specificity index (SI = 1.44, retains) implies for ion-channel mechanotransduction in injured DRG.

---

## Item 2 — G1 and G5 are heavily overlapping, so "five independent sets" is overstated

**【Problem】** The generality benchmark rests on five "independent" sets, but the two that "retain specificity" (G1 and G5) share 10 members, so the "4/5" count double-counts a largely shared module.

**【Evidence】** Recomputing pairwise overlaps from the frozen member lists: G1 (core matrisome, 64 genes) ∩ G5 (ECM remodelling/fibrosis, 23 genes) = `{COL1A1, FN1, LOX, LOXL1, LOXL2, SERPINE1, SPP1, TIMP1, TIMP2, TIMP3}` — 10 of 23 G5 members (43%). The manuscript Table 3 (manuscript.md:134,138) then reports G1 SI = 38.4 and G5 SI = 9.06 both as separate confirmations of retained specificity.

**【Why it matters】** The benchmark's whole premise is that *independent* modules behave the same way. If G1 and G5 are treated as two independent wins, the "4/5 retained" headline overstates the independent lines of evidence. It does not overturn the conclusion (G3 and G4 are genuinely distinct and also retain), but the independence framing is inflated.

**【Specific fix】** Report all pairwise overlaps in a supplement, and either de-duplicate or describe G1/G5 as one "matrisome/fibrosis" module for the independence claim, re-wording "4/5" accordingly (e.g., "3 of 4 independent modules, plus a second matrisome-derived set").

---

## Item 3 — Table 3 citations understate the frozen protocol's actual gene-set sources

**【Problem】** Table 3 lists one reference per set, but the frozen protocol credits multiple primary sources for G2, G3, and G4; for G2 the citation is also substantively wrong.

**【Evidence】** Frozen sources (config `ms_panel.json`): G2 = Dupont 2011 + Cordenonsi 2011 + Zhao 2008; G3 = Coste 2010 + Ranade 2014 + Zaidel-Bar 2007; G4 = Ohashi 2017 + Riento & Ridley 2003. Manuscript Table 3 (manuscript.md:135–138) lists G2 → "Zhao 2008 [9]" only, G3 → "Coste 2010 [6]" only, G4 → "Guan 2023 [10]" only. For G2 this matters biologically: the canonical YAP/TAZ targets CTGF and CYR61 come from Dupont 2011 / Cordenonsi 2011, whereas Zhao 2008 is about *TEAD* mediation — a different claim.

**【Why it matters】** Reader cannot reconstruct the true basis of the benchmark sets, and the substantive attribution for G2 points to the least direct of the three sources. This is a provenance/traceability defect.

**【Specific fix】** Align Table 3 source columns with the frozen `source` strings in `ms_panel.json` (cite all listed primary references for each set).

---

## Item 4 — AMOTL2 is an interactor, not a "canonical CTGF-class YAP/TAZ effector"

**【Problem】** The manuscript counts AMOTL2 among "four canonical CTGF-class YAP/TAZ effectors" in HD_up, but AMOTL2 (angiomotin-like 2) is a YAP/TAZ-binding/regulatory protein that sequesters YAP/TAZ cytoplasmically, not a transcriptional target/effector like CTGF, CYR61, or ANKRD1.

**【Evidence】** Manuscript.md:52 — "Four of the eighteen members are canonical CTGF-class YAP/TAZ effectors; the remaining fourteen… CTGF, CYR61, ANKRD1, and AMOTL2." The deposited signature (layer0) confirms these four are HD_up members, and CTGF/CYR61/ANKRD1 are genuine YAP/TAZ–TEAD targets, whereas AMOTL2 is an established YAP/TAZ interactor (and is itself listed in G2 as a YAP/TAZ "target," compounding the imprecision).

**【Why it matters】** Inflates the fraction of HD_up that is "mechanistically canonical" and slightly overstates the "core is mechanistic" claim in the Layer-0 paragraph.

**【Specific fix】** Re-word to "three canonical YAP/TAZ–TEAD effector targets (CTGF, CYR61, ANKRD1), plus AMOTL2, a YAP/TAZ-binding regulator," or move AMOTL2 out of the "effector" count.

---

## Item 5 — "Hippo-dependent" terminology conflicts with the cited Dupont 2011

**【Problem】** The signature is called "Hippo-dependent" because its response requires YAP/TAZ, but the very paper the manuscript cites for YAP/TAZ mechanotransduction (Dupont 2011, ref [4]) states explicitly that YAP/TAZ mechanical regulation is *independent of the Hippo/LATS cascade*.

**【Evidence】** Manuscript.md:31–32 (signature derivation, "Hippo-dependent"); Dupont 2011 abstract — "This regulation requires Rho GTPase activity and tension of the actomyosin cytoskeleton, but is independent of the Hippo/LATS cascade." GSE98547 (Meng 2018, ref [1]) does implicate the upstream Hippo/LATS arm, so the terminology is defensible operationally, but as written it can contradict the cited ref [4].

**【Why it matters】** A domain reader who knows Dupont 2011 may read "Hippo-dependent stiffness response" as LATS-dependent and be confused; the distinction (YAP/TAZ effector vs. LATS upstream) is central to mechanotransduction biology.

**【Specific fix】** Clarify: "Hippo-pathway-dependent (i.e., YAP/TAZ–TEAD-dependent), noting that the mechanical YAP/TAZ response is LATS-independent per Dupont 2011; we operationally define HD as YAP/TAZ-dKO–abolished."

---

## Item 6 — The MRU/summary-statistic arm (Stage A primary + most of Layer 3) was never sensitivity-validated

**【Problem】** The only positive control (12 nerve-injury markers) was run through the *sample-level* Stage B pipeline (GSE261676), not through the MRU/summary-statistic machinery on GSE111216. The "sensitivity-validated pipeline" and "bounded, sensitivity-validated null" claims therefore do not cover the MRU method that produced the Stage A null and the entire Layer-3 benchmark.

**【Evidence】** Manuscript.md:41 — the positive control is run through the "identical Stage B pipeline"; the Layer-3 script computes MRU on GSE111216 summary statistics and contains no positive-control projection; Table 2 shows the positive control only at Stage B / Layer 4 (manuscript.md:123,152). The 8/40 BH-significant MRU hits (all non-blood) provide *indirect* evidence the MRU method works, but a same-level positive control is the cleaner demonstration.

**【Why it matters】** The headline "the HEK293A-derived stiffness program does not transfer" (Stage A) and the Layer-3 "specificity retained" conclusion both rest on MRU sensitivity that is never directly shown. This weakens, though does not invalidate, the bounded-null argument for the MRU arm.

**【Specific fix】** Either project the 12-gene nerve-injury set (and/or a known DRG-up set) through the MRU machinery on GSE111216 as an explicit positive control, or scope the "sensitivity-validated" claim explicitly to the sample-level arm only.

---

## Item 7 — Must-cite gap: Piezo/TRP ion-channel mechanotransduction in pain is absent from the Discussion

**【Problem】** The most direct in-vivo mechanotransduction-in-pain machinery — Piezo1/2 and TRP channels — is present in the authors' own G3 set but never discussed; the Discussion frames mechanotransduction only via YAP/stiffness/ECM.

**【Evidence】** G3 members include `PIEZO1, PIEZO2, TRPV4, TRPA1, TRPC1, TRPC6, KCNK2, KCNK4` (config `ms_panel.json`); the Discussion (manuscript.md:82–95) contains no mention of Piezo or TRP, and Coste 2010 is cited only as an "adhesome."

**【Why it matters】** A reader could reinterpret the authors' own G3 result (SI = 1.44, retains specificity; DRG shifts further than blood) as evidence that *ion-channel* mechanotransduction genes engage injured DRG — a conclusion the manuscript under-discusses. Engaging this literature would sharpen the central question ("what kind of mechanotransduction engages pain tissue?") and is the obvious missing citation set (e.g., the Piezo2-in-sensory-neuron and TRPA1/TRPV4 mechanical-pain literature).

**【Specific fix】** Add a Discussion paragraph citing Piezo/TRP mechanosensory literature and interpreting G3's SI in that light; this also resolves the mislabel in Item 1.

---

## Item 8 (lower priority) — The positive control validates a *DRG-injury* signal, not specifically a *mechano/stiffness* signal

**【Problem】** The 12-gene positive control (ATF3, SPRR1A, GAP43, NGFR, BASP1, etc.) is a classic axonal-injury/regeneration program; detecting it proves the pipeline sees a neuronal injury shift, not that it would necessarily see a stiffness-driven shift.

**【Evidence】** Manuscript.md:41 lists the markers; these are textbook regenerative-response genes, not mechanotransduction genes. The bounded-null argument (17.6-fold Hedges-g gap) implicitly assumes the positive control's detection implies the HD_up null is "real," but the two sets test different biology.

**【Why it matters】** Minor, but the "sensitivity-validated" wording could be read as validating mechano-specific detection, which it does not.

**【Specific fix】** State explicitly that the positive control validates detection of a genuine DRG transcriptional shift, and that mechano-specific sensitivity remains inferred from the Layer-3 benchmark, not from this control.

---

## § Stands up (things I checked and found correct)

1. **Parisien 2019 [2] is described accurately.** The published abstract states extracellular-matrix (ECM) organization was "the most commonly regulated pathway across all tested tissues in the 2 animal assays" (DRG, spinal cord, brain, blood; nerve-injury and inflammation models), with GWAS overrepresentation in human back pain. The manuscript's Characterization of it as reporting "ECM-organization enrichment in neuropathic/inflammatory pain" (manuscript.md:18) is faithful.
2. **The signature anchor numbers are correct.** CTGF Δ = +1.64 (deposited 1.6405), P = 9.5 × 10⁻⁶ (deposited 9.494 × 10⁻⁶); CYR61 +0.99 (0.9926), ANKRD1 +1.43 (1.4263), AMOTL2 +1.38 (1.3845) all match the deposited Layer-0 file. CTGF, CYR61, and ANKRD1 are bona-fide YAP/TAZ–TEAD targets, so the "biologically anchored" claim holds (modulo Item 4 on AMOTL2).
3. **HD set sizes and LATS-confirmation fractions are correct.** HD_up n = 18, HD_down n = 41, and LATS confirmation 79.7% (HD) vs 28.6% (HI) match the deposited signature file exactly.
4. **Layer-3 specificity indices and BH q-values are correct.** Re-derived from the deposited Layer-3 JSON: G1 SI = 38.4 (q = 0.0010), G2 SI = 0.44 (fails), G3 SI = 1.44, G4 SI = 240.5, G5 SI = 9.06 (q = 0.0016); 8/40 tests survive BH (all DRG/SC/BRN, none in blood). Only G2 fails specificity — consistent with "4/5 retain."
5. **The G4 denominator-instability is real and honestly footnoted.** MRU(blood, SNI) for G4 = 0.49908, so |ΔBLD−0.5| = 0.00092 ≈ 0.0009; the resulting SI = 240.5 is unstable, and the manuscript's Table 3 footnote already tells the reader to read absolute shifts directly. This is handled correctly.
6. **The cross-species / cross-cell-type caveat is stated honestly.** The Limitations section (manuscript.md:95) explicitly concedes HEK293A is non-neuronal, requires symbol mapping (HD_up coverage 0.611 in mouse DRG), and that cell-type and mechanical-input mismatches are confounded and inseparable. The "cell-type- and mechanical-input-specific" interpretation is the biologically parsimonious reading of a negative result and is not overclaimed as disproving the pain-ECM literature.

---

## § Questions for the authors

1. Did you run any positive control through the MRU/summary-statistic machinery on GSE111216? If not, on what basis do you assert the MRU arm is "sensitivity-validated," and would you scope that claim to the sample-level arm only?
2. Will you rename/cite G3 properly (Item 1) and report the G1∩G5 overlap (Item 2)? If you de-duplicate, how does the "4/5" independence claim change?
3. For the "four canonical effectors" count, do you treat AMOTL2 as a YAP/TAZ transcriptional target or as an interactor (Item 4)?
4. Will you engage the Piezo/TRP ion-channel mechanotransduction-in-pain literature, given those genes are already in your G3 set (Item 7)?
5. Could the HD_up null alternatively reflect low mouse-DRG coverage (11/18) and the HD_up set's small size rather than a true absence of transfer? How sensitive is the Stage B result to the 7 absent members?

---

## § What I actually checked

- Read the manuscript in full and the panel brief's permitted-file list; read no forbidden or other-reviewers' files.
- Recomputed pairwise gene-set overlaps directly from the frozen gene-set member lists in the deposited protocol configuration; found G1∩G5 = 10 genes (43% of G5) and smaller 1-gene overlaps between G1–G2, G1–G3, G2–G4, G2–G5, G4–G5.
- Re-derived the Layer-3 specificity indices and BH q-values from the deposited Layer-3 result file and confirmed they match Table 3 and the Discussion; confirmed 8/40 BH-significant and that only G2 fails (4/5 retain).
- Verified the signature anchor statistics (CTGF Δ and P; CYR61/ANKRD1/AMOTL2 Δs), HD_up/HD_down sizes, and LATS-confirmation fractions against the deposited Layer-0 file.
- Verified the G4 blood denominator (0.49908 → |Δ| = 0.00092) matches the manuscript's "≈ 0.0009" and that the SI instability is footnoted.
- Retrieved and read the published abstract of Parisien 2019 (Pain 2019; PMID 30763288) and confirmed the ECM-organization finding; retrieved and read the published abstract of Dupont 2011 (Nature 2011; PMID 21654799) and confirmed YAP/TAZ as mechanical relays and the "independent of Hippo/LATS" statement.
- Confirmed the gene-set source strings in the frozen protocol differ from the single-reference citations in Table 3 for G2, G3, and G4.
- Confirmed the positive control is exercised only through the sample-level Stage B pipeline, with no positive-control projection through the MRU/summary-statistic Layer-1/3 machinery.

All numeric claims above were recomputed from the deposited files; no values were taken on trust from the manuscript text.
