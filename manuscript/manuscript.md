# A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity

**Yongxin Yang** (ORCID 0009-0004-9698-6552)
The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China

---

## Abstract

**Background.** Transcriptomic studies of chronic pain repeatedly report enrichment of broad "extracellular-matrix organization" gene sets. Whether a transcript program *genuinely driven by extracellular-matrix stiffness* engages pain-relevant tissues (dorsal root ganglion, DRG; spinal cord, SC) has never been tested with a signature whose mechanical driver is experimentally controlled.

**Methods.** We conducted a prospectively specified, two-stage reanalysis. A Hippo-dependent stiffness signature (HD_up, n = 18; HD_down, n = 41) was derived from GSE98547 (human HEK293A, 1 vs 40 kPa fibronectin hydrogels, four Hippo-pathway genotypes) and projected onto GSE111216 (four tissues × two neuropathic-pain models, summary statistics) and GSE261676 (mouse DRG, sample-level, spared-nerve-injury model). All endpoints were frozen before inspecting pain data. A pre-specified positive-control test and a five-set specificity benchmark (Layer 3) tested sensitivity and generality.

**Results.** We first established a validated, sensitivity-tested pipeline. The stiffness signature was biologically anchored (CTGF Δ = +1.64, P = 9.5 × 10⁻⁶), and a pre-specified positive-control test confirmed sensitivity: a 12-gene nerve-injury set was detected with full separation (difference = +1.285, P = 0.0286, Hedges g = 3.85). Against this validated baseline, the HEK293A-derived stiffness program did **not** transfer to pain tissue. In Stage A (expression-matched calibration) DRG×SNI HD_up gave MRU = 0.717, P = 0.102, BH (Benjamini–Hochberg) q = 0.409, and the blood negative control was *equally non-significant* (MRU = 0.696, P = 0.100, q = 0.409); per §5.3 Stage A is uninformative. In Stage B HD_up produced a bounded null (difference = +0.146, P = 0.80, Hedges g = 0.219). The failure is signature-specific, not universal: in the Layer-3 benchmark only 1/5 ECM/mechanotransduction sets lacked specificity (specificity index range 0.44–240.5), 4/5 shifted *at least as far in DRG as in blood*, and G1 and G5 reached BH significance in DRG×SNI (q = 0.0010 and 0.0016).

**Conclusions.** Using a sensitivity-validated pipeline, we show that the cross-cell-type projection of a HEK293A-derived stiffness program does not transfer to pain tissues (bounded, sensitivity-validated null). The failure is *signature- and cell-type-specific*, not a universal projection artifact: once baseline-expression confounding is controlled, established ECM/mechanotransduction gene sets retain tissue specificity (4/5, with G1 and G5 significant in DRG×SNI). Literature "ECM enrichment in pain" findings are not disproven; our result circumscribes their interpretation to the source cell type of the projected signature.

---

## Background

Neuropathic pain transcriptomes consistently show upregulation of extracellular-matrix (ECM) and mechanotransduction-related terms [2,5,7]. The prevailing interpretation is that mechanical signalling programs are engaged in injured sensory pathways. Two inferential gaps limit this conclusion. First, "ECM organization" is a broad Gene Ontology term encompassing hundreds of housekeeping collagens and glycoproteins; its enrichment does not isolate a mechanistically defined program. Second, the direction of causality is unclear: ECM changes may be downstream sequelae rather than drivers of the pain state.

A cleaner test requires a signature whose mechanical driver is *experimentally manipulated*, not inferred. GSE98547 [1] varied substrate stiffness (1 kPa vs 40 kPa) across four Hippo-pathway genotypes, allowing the stiffness response to be decomposed into Hippo-dependent (HD) and Hippo-independent components. Projecting such a controlled signature onto pain transcriptomes asks a falsifiable question: does the *same* mechanically defined program re-appear in injured DRG/SC?

We pre-registered this question as a reanalysis with frozen endpoints, dual negative controls, and a positive-control sensitivity test, to avoid the HARKing and selection biases that undermine post-hoc enrichment claims.

A prospective, sensitivity-validated design lets us separate a *true* bounded null (a genuine absence that survives a sensitivity check) from a *methodological* null (one that would also erase real signal). That separation is the contribution of this reanalysis: it tells us, with calibration, where a controlled stiffness program does and does not engage pain transcriptomes.

## Methods

### Data sources
Three public datasets were used (all re-use of de-identified public data; no new subjects). GSE98547 [1] (human HEK293A, 4 genotypes × 2 stiffness × 3 replicates = 24 samples) trained the signature. GSE111216 [2] (mouse; DRG, spinal cord SC, brain BRN, blood BLD × SNI and CFA models, n = 3 per contrast, per-contrast summary statistics) provided the first projection. GSE261676 [3] (mouse DRG; SNI vs sham × saline/DMI, 4 vs 4 sample-level counts) provided sample-level validation.

### Signature derivation (Layer 0)
Per gene, the stiffness response was computed as log₂(FPKM + 1) contrast (40 kPa − 1 kPa) within each genotype. HD genes were those responding in WT but whose response was abolished in YAP/TAZ-dKO (or LATS1/2-dKO), operationally |Δ_YTKO| ≤ 0.5|Δ_WT| after Welch testing. This yields HD_up (n = 18) and HD_down (n = 41). LATS-confirmation was computed as the fraction of HD (vs HI) genes whose YAP/TAZ-dependence was *directionally* confirmed: the sign of the WT stiffness response agreed between the WT estimate and the YAP/TAZ-dKO (or LATS-dKO) estimate (both positive or both negative), so the response was blunted, not reversed, upon YAP/TAZ loss.

### Projection and endpoints (Stage A, Layer 1)
The pre-specified primary endpoint was rank-based concordance of HD_up in DRG×SNI, using the median-rank utility (MRU = median(member rank)/(n_expressed − 1), 1-based; 0.5 = no shift) against a size- and baseline-expression-decile-matched null (without replacement, 10 000 iterations). Negative controls were BLD and BRN. The pre-specified governance rule (§5.3) states that if a negative control is *equally* significant to the primary, tissue-specific attribution cannot be made.

### Sample-level module scores (Stage B, Layer 2)
On GSE261676, each gene was converted to CPM → log₂(CPM + 1) → per-gene cross-sample z-score; set scores were member-z means. The B-primary was the saline-arm SNI-vs-sham HD_up score difference, tested by exhaustive exact permutation over all C(8,4) = 70 possible 4-vs-4 splits (two-sided), cross-checked with Welch t and Mann–Whitney U. Hedges g provided the effect size.

### Positive control and bias controls
A 12-gene nerve-injury marker set (ATF3, SPRR1A, GAL, NPY, SOX11, GAP43, NGFR, VGF, STMN4, BASP1, MMP9, TIMP1) was run through the *identical* Stage B pipeline. Because this set shares zero members with the stiffness signature and was selected from literature only, its detection validates pipeline sensitivity; its failure would void all null conclusions.

### Generality benchmark (Layer 3)
Five independent, literature-sourced ECM/mechanotransduction gene sets were projected with the same MRU statistic onto GSE111216: G1 core matrisome [5], G2 YAP/TAZ canonical targets [9], G3 mechanosensing adhesome [6], G4 actin/Rho/ROCK cytoskeleton [10], G5 ECM remodelling/fibrosis [7,8]. The specificity index SI_g = |MRU(DRG,SNI) − 0.5| / |MRU(BLD,SNI) − 0.5|; SI_g < 1 denotes failure of tissue specificity. The pre-specified primary rule: if ≥ 4/5 sets fail specificity, the lack of specificity is a *general* property of projection, not of one signature.

### Sample-level divergence (Layer 3b) and positive characterisation (Layer 4)
Layer 3b re-tested the five sets plus HD_up and the positive control on GSE261676 sample-level data (exact permutation, Hedges g). Layer 4 characterized genes *actually* upregulated in injured DRG (per-gene Welch t over 15 345 detection-passed genes, BH correction), reporting how many fell in G1/G4/G5 and comparing to HD_up members via Fisher exact test.

## Results

### Layer 0: a biologically anchored stiffness signature
The HD_up set (n = 18) is anchored by established YAP/TAZ targets: CTGF (Δ = +1.64, P = 9.5 × 10⁻⁶), CYR61 (+0.99), ANKRD1 (+1.43), and AMOTL2 (+1.38). Four of the eighteen members are canonical CTGF-class YAP/TAZ effectors; the remaining fourteen are heterogeneous (adhesion, cytoskeletal, and regulatory genes) that meet the Hippo-dependence criterion (Figure 1). LATS confirmation was 79.7% for HD versus 28.6% for HI genes, confirming that the HD classification captures genuine Hippo-pathway dependence (Figure 1, shaded cone). The signature is therefore biologically meaningful *as a controlled in vitro program*, while its "core" is mechanistic rather than a uniform set of canonical targets.

![Figure 1. Signature derivation: Hippo-dependent members](../analysis/results/layer2/fig/fig1_signature_derivation.png)

### Stage A: negative control as strong as target (uninformative)
Under the pre-specified expression-matched calibration, DRG×SNI HD_up gave MRU = 0.717, exact/permutation P = 0.102, BH q = 0.409 (not significant). The blood negative control was *statistically indistinguishable*: MRU = 0.696, P = 0.100, q = 0.409 (Table 2). Per §5.3, because the negative control is equally non-significant (q = 0.409 = DRG), no tissue-specific attribution can be made; Stage A is **uninformative**, not merely "negative." A separate, non-pre-specified unstratified calibration (full background including 40–58% zero-expression loci; baseline-zero fractions DRG 42.8%, BLD 58.5%, SC 41.0%, BRN 40.5%; Kolmogorov–Smirnov D ≈ 0.49 throughout) gave DRG P = 0.597 and BLD P = 0.0009, a pattern driven by the zero-expression confound and explicitly *not* the primary endpoint.

![Figure 2. Per-animal HD_down module scores (saline arm)](../analysis/results/layer2/fig/fig2_per_animal_scores.png)

### Stage B: bounded null for HD_up; pipeline sensitivity proven
In the sample-level 4-vs-4 test, HD_up showed a bounded null (difference = +0.146, exact P = 0.80, Hedges g = 0.219; coverage 0.611, 11/18 members expressed in mouse DRG) (Figure 4). The positive control, run through identical scoring/permutation code, was detected at the 4-vs-4 lower bound (difference = +1.285, exact P = 0.0286, Hedges g = 3.85; Mann–Whitney P = 0.0286) (Figure 5). The 17.6-fold Hedges-g gap between positive control and HD_up, on identical code, shows the HD_up null is *bounded* (a real absence of detectable signal at this design) rather than a sensitivity failure. HD_down reached a nominally significant but BH-non-significant (q = 0.086) reverse elevation (difference = +0.397, P = 0.0286, g = 2.658) and is reported **as hypothesis-generating only** (Figure 2, 3); its direction was preserved under leave-one-animal-out and a Q4 expression-matched null (P = 0.092), supporting that the elevation is not a single-animal artifact.

![Figure 3. Per-member contribution to the HD_down signal](../analysis/results/layer2/fig/fig3_member_contributions.png)

![Figure 4. Observed separation against the size- and expression-matched null](../analysis/results/layer2/fig/fig4_matched_null.png)

![Figure 5. Pipeline sensitivity: positive control vs stiffness signatures](../analysis/results/layer2/fig/fig5_positive_control_vs_signatures.png)

### Layer 3: specificity retained by established sets; the projection failure is signature-specific
Against the matched null, the five independent sets behaved heterogeneously (Figure 6, Table 3): G1 (SI = 38.4), G3 (SI = 1.44), G4 (SI = 240.5), and G5 (SI = 9.06) all showed *stronger* DRG-than-blood shift, whereas G2 (YAP/TAZ canonical targets, SI = 0.44) failed. Only 1/5 sets lacked specificity, so the pre-specified primary rule (≥ 4/5 failing) was **not** met, and we could *not* show that specificity failure is universal. Of 40 tests (5 sets × 4 tissues × 2 models), 8 survived BH correction (q < 0.05), all in DRG/SC/BRN with none in blood.

![Figure 6. Tissue specificity of five independent ECM / mechano gene sets](../analysis/results/layer3/fig/fig6_generality.png)

### Layer 3b and Layer 4: sample-level confirmation and descriptive characterisation
Layer 3b did not support a divergence pattern: 0/5 ECM sets were significantly upregulated in the saline-arm SNI-vs-sham test (Hedges g 0.31–1.13; positive control g = 3.85, P = 0.0286; HD_up g = 0.219, P = 0.80); its primary endpoint FAILED (Figure S1). Layer 4 characterized injured DRG directly: of 15 345 tested genes, 8 were significantly upregulated (q < 0.05) and 3 down; the ECM-union (G1/G4/G5) contributed 0 significant-up genes (Fisher OR = 0, P = 1.0), and HD_up members contributed 0. Layer 4's primary endpoint FAILED, confirming the descriptive landscape is not dominated by ECM-structure upregulation.

![Figure S1. Layer-3b sample-level effect sizes (7 gene sets)](../analysis/results/layer3/fig/figS1_layer3b_effects.png)

## Discussion

### What the data show
The results establish a working, sensitivity-validated pipeline and localise the failure precisely. The signature was biologically anchored (CTGF Δ = +1.64, P = 9.5 × 10⁻⁶), and the positive-control test passed with full separation (nerve-injury set difference = +1.285, P = 0.0286, Hedges g = 3.85), confirming the pipeline can detect a true DRG signal. Against that validated baseline, four pre-specified primary endpoints were tested. Stage A (§5.3 verdict), Layer 3b, and Layer 4 did not confirm the hypothesised tissue-specific engagement, and the Layer-3 *universal-failure* primary was also not met, but its non-meeting means specificity was *retained*, not lost (only 1/5 sets lacked specificity). Two of the nulls are *informative*, not method failures: (i) Stage A is governed as uninformative by §5.3 because the blood control is equally non-significant; (ii) Stage B's HD_up null is bounded and sensitivity-validated, its 17.6-fold Hedges-g gap to the positive control showing a real absence of detectable signal at this design rather than a sensitivity collapse. The Layer-3 benchmark delivered the most substantive result: **under proper expression-stratification, established ECM/mechanotransduction gene sets retain tissue specificity in pain** (4/5 DRG > blood; G1 SI = 38.4 and G5 SI = 9.06 reach BH significance in DRG×SNI, q = 0.0010 and 0.0016), refuting the hypothesis that projection statistics inherently fail. The spurious "blood shifts more than DRG" pattern seen in the unstratified Stage A calibration is explained by baseline zero-expression confounding (40–58% of loci), which the matched null corrects.

Two distinct claims must not be conflated. Layer 3 establishes *rank-projection direction-of-shift specificity*: whether each set's membership shifts more in DRG than in blood. There, 4/5 established sets are affirmed. Layer 3b and Layer 4 instead ask whether these sets are *upregulated in injured DRG at the sample level*; there the design is simply underpowered and inconclusive. Specificity retained in the rank projection does not entail sample-level upregulation, nor does the latter's absence negate the former.

We therefore revise the interpretation relative to the pre-registered hypotheses: the cross-cell-type projection of a *HEK293A-derived* stiffness program does not transfer to mouse pain DRG/SC, and this is most parsimoniously a **cell-type- and mechanical-input-specific** limit of this particular HEK293A-derived, substrate-fibronectin-stiffness program (HEK293A epithelium ≠ sensory neuron/glia) rather than evidence that pain-ECM findings are artifacts. Our null thus *circumscribes* the literature's "ECM enrichment in pain" claims to the source cell type of the projected signature, without disproving them.

### Core conclusions
1. A stiffness-controlled experiment can yield a biologically anchored mechanosignature (CTGF Δ = +1.64, P = 9.5 × 10⁻⁶); the signature itself is sound.
2. Projecting that signature onto pain transcriptomes yields no tissue-specific evidence of engagement (Stage A §5.3 uninformative; Stage B bounded null), but this is a *bounded, sensitivity-validated* null, not a method artifact.
3. The failure is signature- and cell-type-specific: expression-stratified projection recovers specificity for established ECM/mechano sets, so literature "ECM enrichment in pain" findings are not invalidated by our result.

### Limitations
This study re-uses public data with inherent constraints: GSE111216 deposits only per-contrast summary statistics (n = 3), preventing sample-level and behavioural-covariate analysis; GSE261676 is a 4-vs-4 design whose exact-permutation lower bound is P ≈ 0.029. HEK293A is non-neuronal, so the signature captures a mechanistically defined (Hippo-dependent) but not neuron-specific program; cross-species symbol mapping is required and HD_up coverage in mouse DRG was 0.611. The mechanical input also differs between the two settings: culture-substrate fibronectin stiffness versus nerve compression or perineural fibrosis in vivo. Cell-type and mechanical-input mismatches are therefore confounded and cannot be separated here. The post-hoc observation that YAP/TAZ-class targets (G2) lose specificity while structural-ECM sets (G1/G3/G4/G5) retain it is reported as hypothesis-generating only, and we are not aware of direct DRG literature that separates these programs in neuropathic pain; independent validation is required. HD_down is likewise hypothesis-generating only. The Layer-3 primary endpoint (universal specificity failure) was not met; generality of the *signature-specific* null is therefore asserted only for the HD_up program and its source cell type.

## Declarations
**Ethics.** This study used only public, de-identified transcriptomic datasets; no new human or animal subjects were enrolled.
**Data availability.** Source datasets: GSE98547, GSE111216, GSE261676 (Gene Expression Omnibus). Analysis code, configuration, and all result artifacts are deposited at https://github.com/yyx-4113/matrix-stiffness-neuropathic-pain (tag v1.0.0) with a MANIFEST of checksums; every numeric claim in this manuscript is traceable to a file under `analysis/results/`.
**Competing interests.** None declared.
**Funding.** None.
**Authors' contributions.** YY conceived, performed, and wrote the analysis and manuscript.
**Acknowledgements.** None.

---

## Tables

**Table 1. Dataset characteristics.**

| Dataset | Species / cell | Design | Role | Key limitation |
|---|---|---|---|---|
| GSE98547 | *H. sapiens* / HEK293A | 4 genotypes × 2 stiffness (1, 40 kPa) × 3 reps = 24 | Layer 0 signature training | Non-neuronal; cross-species mapping required |
| GSE111216 | *M. musculus* | 4 tissues (DRG, SC, BRN, BLD) × 2 models (SNI, CFA), n = 3 per contrast, summary stats | Layer 1 projection | Per-contrast summary only; n = 3; 40–58% zero-expression baseline |
| GSE261676 | *M. musculus* / DRG | SNI vs sham × saline/DMI, 4 vs 4 sample-level counts | Layers 2–4 sample-level | Small n (4v4); drug-arm confound |

**Table 2. Endpoint results summary.**

| Layer / endpoint | Statistic | Result | Pre-specified verdict |
|---|---|---|---|
| Stage A primary (HD_up × DRG × SNI, matched) | MRU = 0.717, P = 0.102, q = 0.409 | not sig; blood control equally non-significant (MRU = 0.696, P = 0.100, q = 0.409) | §5.3 uninformative |
| Stage B primary (HD_up, saline SNI vs sham, 4v4) | diff = +0.146, P = 0.80, g = 0.219 | bounded null | not sig |
| Stage B positive control (injury markers) | diff = +1.285, P = 0.0286, g = 3.85 | detected | PASS (sensitivity) |
| Stage B HD_down (secondary) | diff = +0.397, P = 0.0286, q = 0.086, g = 2.658 | nominally sig, BH-ns, reverse dir | hypothesis-generating |
| Layer 3 primary (≥ 4/5 sets fail specificity) | 1/5 failed (G2 SI = 0.44) | rule not met | primary FAIL |
| Layer 3 secondary | 8/40 BH-significant (all DRG/SC/BRN; blood 0) | n/a | n/a |
| Layer 3b primary (divergence) | 0/5 ECM sig up; pos control P = 0.0286 | no divergence | primary FAIL |
| Layer 4 primary (positive characterisation) | 8/15 345 genes sig up; ECM-union sig up = 0 | ECM not dominant | primary FAIL |

**Table 3. Layer-3 generality benchmark (specificity index, SI_g).**

| Gene set | Source | MRU target (DRG, SNI) | MRU blood (BLD, SNI) | \|ΔDRG−0.5\| | \|ΔBLD−0.5\| | SI_g | Specificity failed? |
|---|---|---|---|---|---|---|---|
| G1 core matrisome | Naba 2016 [5] | 0.9056 | 0.5106 | 0.4056 | 0.0106 | 38.4 | No |
| G2 YAP/TAZ canonical targets | Zhao 2008 [9] | 0.6180 | 0.7681 | 0.1180 | 0.2681 | 0.44 | Yes |
| G3 mechanosensing adhesome | Coste 2010 [6] | 0.8040 | 0.7114 | 0.3040 | 0.2114 | 1.44 | No |
| G4 actin/Rho/ROCK | Guan 2023 [10] | 0.7224 | 0.4991 | 0.2224 | 0.0009 | 240.5 | No |
| G5 ECM remodelling/fibrosis | Wynn 2008 [7] / Henderson 2020 [8] | 0.8857 | 0.4574 | 0.3857 | 0.0426 | 9.06 | No |

*SI_g = |MRU(DRG,SNI)−0.5| / |MRU(BLD,SNI)−0.5|, computed from full-precision MRU; the \|Δ\| columns are rounded to 4 d.p. and will not exactly reproduce SI by division. SI is unstable when |ΔBLD−0.5| ≈ 0 (G4 denominator ≈ 0.0009); read the absolute shifts directly. Four of five sets show |ΔDRG−0.5| > |ΔBLD−0.5| (all except G2), i.e., retain DRG-over-blood specificity.*

**Table 4. Layer-3b sample-level results (saline arm, 4 SNI vs 4 sham, exact permutation).**

| Gene set | n present | diff (SNI−sham) | P_exact | Hedges g | BH q |
|---|---|---|---|---|---|
| G1 core matrisome | 62 | +0.513 | 0.229 | 0.839 | 0.440 |
| G2 YAP/TAZ canonical targets | 12 | +0.174 | 0.657 | 0.310 | 0.767 |
| G3 mechanosensing adhesome | 22 | −0.277 | 0.286 | −0.823 | 0.440 |
| G4 actin/Rho/ROCK | 20 | +0.393 | 0.171 | 1.131 | 0.440 |
| G5 ECM remodelling/fibrosis | 21 | +0.371 | 0.314 | 0.766 | 0.440 |
| HD_up | 11 | +0.146 | 0.800 | 0.219 | 0.800 |
| Positive control (injury) | 12 | +1.285 | 0.0286 | 3.853 | 0.200 |

*The HD_up and positive-control rows reproduce the Stage B results (identical GSE261676 computation); they are repeated here only to position the ECM sets against the sensitivity-validated anchors and are not independent tests.*

---

## References

1. Meng Z, Qiu Y, Lin KC, et al. RAP2 mediates mechanoresponses of the Hippo pathway. *Nature*. 2018;560(7720):655–660. PMID: 30135582. DOI: 10.1038/s41586-018-0444-0.
2. Parisien M, Samoshkin A, Tansley SN, et al. Genetic pathway analysis reveals a major role for extracellular matrix organization in inflammatory and neuropathic pain. *Pain*. 2019;160(4):932–944. PMID: 30763288. DOI: 10.1097/j.pain.0000000000001471.
3. Serafini RA, Ramakrishnan A, Shen L, Zachariou V. Desipramine induces anti-inflammatory dorsal root ganglion transcriptional signatures in the murine spared nerve injury model. *Neurobiol Pain*. 2024;15:100153. PMID: 38549875. DOI: 10.1016/j.ynpai.2024.100153.
4. Dupont S, Morsut L, Aragona M, et al. Role of YAP/TAZ in mechanotransduction. *Nature*. 2011;474(7350):179–183. PMID: 21654799. DOI: 10.1038/nature10137.
5. Naba A, Clauser KR, Ding H, Whittaker CA, Carr SA, Hynes RO. The extracellular matrix: Tools and insights for the "omics" era. *Matrix Biol*. 2016;49:10–24. PMID: 26163349. DOI: 10.1016/j.matbio.2015.06.003.
6. Coste B, Mathur J, Schmidt M, et al. Piezo1 and Piezo2 are essential components of distinct mechanically activated cation channels. *Science*. 2010;330(6000):55–60. PMID: 20813920. DOI: 10.1126/science.1193270.
7. Wynn TA. Cellular and molecular mechanisms of fibrosis. *J Pathol*. 2008;214(2):199–210. PMID: 18161745. DOI: 10.1002/path.2277.
8. Henderson NC, Rieder F, Wynn TA. Fibrosis: from mechanisms to medicines. *Nature*. 2020;587(7835):555–566. PMID: 33239795. DOI: 10.1038/s41586-020-2938-9.
9. Zhao B, Ye X, Yu J, et al. TEAD mediates YAP-dependent gene induction and growth control. *Genes Dev*. 2008;22(14):1962–1971. PMID: 18579750. DOI: 10.1101/gad.1664408.
10. Guan G, Cannon RD, Coates DE, Mei L. Effect of the Rho-Kinase/ROCK Signaling Pathway on Cytoskeleton Components. *Genes (Basel)*. 2023;14(2):272. PMID: 36833199. DOI: 10.3390/genes14020272.
