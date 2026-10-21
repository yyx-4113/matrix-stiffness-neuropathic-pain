# Reviewer B1 — Significance / Novelty (independent blind assessment, PLOS ONE lens)

**Manuscript:** "A controlled stiffness signature does not transfer to neuropathic-pain transcriptomes, while established ECM/mechanotransduction gene sets show tissue-specific shifts"
**Commit:** 4785c52 · **Role:** Senior academic editor (Significance/Novelty) · **Standard applied:** PLOS ONE soundness, not novelty/impact.

---

## Overall verdict: **MAJOR REVISION**

The study is methodologically sound and, importantly, *honest about its nulls* — Stage A double-null, Stage B bounded null, Layer 3b/4 FAIL, and the Layer-3 universal-failure rule *not met* are all labelled plainly, and the G1/G5 overlap and G4 denominator artefact are disclosed. Those are exactly the properties that make a mixed/null result publishable at PLOS ONE. The manuscript is **not** rejectable: there is no methodological failure, no ethical issue, and a genuine, useful contribution exists (a *sensitivity-validated* null plus the observation that established ECM/fibrosis modules retain DRG-over-blood rank specificity).

It is **not** acceptable as-is because the *headline framing* — the title, Abstract line 10, and Core conclusion #3 — over-states the positive finding in a way that is demonstrably unsupported by the body's own statistics and that borders on HARKing. The positive contribution rests on **one independent** BH-significant observation (matrisome/fibrosis, which is G1 *and* G5 counting the same 10-gene overlap) plus a non-significant G3 (SI-only). Presenting this as "established ECM/mechanotransduction gene sets show tissue-specific shifts" and as a co-equal core conclusion is the decisive defect. This is fixable by reframing, so MAJOR REVISION, not rejection.

---

## Findings (each with Problem / Evidence / Why it matters / Specific fix)

### F1 — Title's second clause is not supported at the manuscript's own rigor standard

【Problem】 The title asserts that "established ECM/mechanotransduction gene sets show tissue-specific shifts." Of the five benchmark sets, only G1 and G5 reach BH significance (DRG×SNI q = 0.0010, 0.0016); G2 *failed* specificity (SI = 0.44); G3 is non-BH and non-sample-level; G4's large SI is a denominator artefact. G1 and G5 also overlap by 10 genes (one matrisome/fibrosis module counted twice). So the robust, independent positive is effectively **one** module, not "gene sets" broadly.

【Evidence】 `manuscript.md:1` — "…while established ECM/mechanotransduction gene sets show tissue-specific shifts." Body: `manuscript.md:67` ("Only 1/5 sets lacked specificity … G1 and G5 share 10 members … G4's large SI is a denominator artefact"); `manuscript.md:123` Table 2 ("Layer 3 primary (≥ 4/5 sets fail specificity) … rule not met … primary FAIL"); `analysis/results/layer3/layer3_generality.json` confirms G1 DRG×SNI q=0.0010, G5 q=0.0016, G3 DRG×SNI q=0.0652 (not BH), G4 BLD-SNI |Δ|=0.000925.

【Why it matters】 A PLOS ONE editor/reviewer scrutinises the title against the results. A title that implies broad support across "gene sets" when the body shows one overlapping module + a failure + an artefact is an over-claim that would trigger a "scope of claim vs evidence" objection. It does not, by itself, justify rejection, but it is a mandatory revision point.

【Specific fix】 Either (a) reframe the title to attribute the shift to the specific module, e.g. "…while a matrisome/fibrosis gene set (but not YAP/TAZ canonical targets) retains DRG-over-blood rank specificity," or (b) split into two sentences that explicitly scope the positive to G1/G5 and name G2's failure. Do not use the plural "gene sets" as the subject of a general claim.

### F2 — Abstract line 10 lumps G3 with BH-significant G1/G5, creating an HARKing-adjacent framing

【Problem】 The Abstract presents "matrisome/fibrosis (G1, G5) and mechanosensory (G3) modules" as a single recovered DRG-over-blood shift, equating G3 with G1/G5. But G3 reaches *only* SI specificity (SI = 1.44); it does **not** reach BH significance (DRG×SNI q = 0.0652) and was *not* upregulated at the sample level (Layer 3b G3 diff = −0.277, P = 0.286). The body itself labels G3's mechanosensory reading as a hypothesis only (line 83).

【Evidence】 `manuscript.md:10` — "Once baseline-expression confounding is controlled, established ECM/mechanotransduction sets show a DRG-over-blood shift for matrisome/fibrosis (G1, G5) and mechanosensory (G3) modules." Contrast with `manuscript.md:83` ("We flag this only as a hypothesis … was not upregulated at the sample level (Layer 3b, G3 diff = −0.277, P = 0.286)"). Table 4 (`manuscript.md:146`) confirms G3 P = 0.286, q = 0.440.

【Why it matters】 This is precisely the sentence a reviewer reads as "you dressed up a null as a positive result." The study is null-dominated (4 of the 5 pre-specified primary endpoints FAIL or are double-null), and the only robust BH-significant positive is G1/G5. Inflating G3 into the headline without its non-significance qualifier is the kind of post-hoc weighting PLOS ONE reviewers are trained to catch. It damages credibility even though the Discussion is careful.

【Specific fix】 In the Abstract, separate the two tiers explicitly, e.g.: "…the matrisome/fibrosis module (G1/G5, overlapping by 10 genes) retains a BH-significant DRG-over-blood shift, whereas the mechanosensory module (G3) shows rank specificity only (not BH-significant; not upregulated at sample level) and is flagged as hypothesis-generating." Remove the implication that G3 is a confirmed positive.

### F3 — Core conclusion #3 over-weights the single positive and is internally inconsistent with the Discussion

【Problem】 Core conclusion #3 states "The failure is signature- and cell-type-specific: expression-stratified projection recovers a DRG-over-blood shift for established ECM/mechanotransduction modules (G1, G5, and the mechanosensory G3)." This (i) lists G3 alongside G1/G5 as if co-equal, and (ii) frames the entire "positive" contribution as if it is the answer to "so what did you find," when the robust support is one overlapping module plus a non-significant SI.

【Evidence】 `manuscript.md:90` — exact wording above. The Discussion at `manuscript.md:81` already concedes "the genuine, independent wins are G1, G3, and G5, of which G1 and G5 reach BH significance," and `manuscript.md:83` calls G3 hypothesis-only — so the conclusion is stricter than the Discussion's own qualification.

【Why it matters】 Core conclusions are what editors and readers remember. Presenting a null-dominated study's single qualified observation as a decisive "signature- and cell-type-specific failure recovered a shift for established modules" inverts the evidentiary weight. A reviewer will ask whether conclusion #3 is supported, and the honest answer is "partially, and only for G1/G5." This is a MAJOR-revision-level framing defect, not a methodological one.

【Specific fix】 Rewrite #3 to (a) name G2's failure explicitly so the "specificity" claim is balanced, (b) state that G1 and G5 are the *same overlapping* module, and (c) downgrade G3 to "hypothesis-generating, rank-specificity only." Suggested: "The projection failure is signature- and cell-type-specific, not universal: the matrisome/fibrosis module (G1/G5, sharing 10 members) retains a BH-significant DRG-over-blood rank shift, whereas the YAP/TAZ canonical set (G2) loses it and the mechanosensory module (G3) shows rank specificity only (hypothesis-generating)."

### F4 — The "positive" contribution is real but needs honest re-weighting so the paper reads as a sound null, not a positive finding

【Problem】 The study reports Stage A double-null, Stage B bounded null, Layer 3b FAIL, Layer 4 FAIL, Layer-3 universal-failure rule NOT met. The only confirmed positive is the rank-projection DRG-over-blood specificity of G1/G5 (one overlapping module). Yet the narrative arc (title → abstract → conclusion #3) leads with the positive. A reviewer may ask "so what did you find?" and the answer ("sensitivity-validated null + one retained module") is genuinely publishable, but only if the paper owns the null rather than hinting it found the opposite.

【Evidence】 Aggregate of `manuscript.md:53` (Stage A double-null), `manuscript.md:58` (Stage B bounded null), `manuscript.md:67` (Layer 3 universal-failure rule not met), `manuscript.md:72` (Layer 3b & 4 FAIL). The contribution claim (b) "sensitivity-validated (not methodological) bounded null" and (c) "signature-specific failure" are stated as contributions at lines 10, 90.

【Why it matters】 PLOS ONE explicitly publishes sound null/mixed results. The manuscript's *methodology* already earns that. The risk is that the over-weighted positive makes the paper look like it is pretending to a finding it does not have, which invites rejection-on-framing. Correcting the weight converts a borderline case into a clean accept-after-revision.

【Specific fix】 Add one explicit sentence in the Discussion "What the data show" (or a short "Interpretive summary") that states plainly: "The robust, replication-grade result of this study is a *sensitivity-validated* null for HD_up transfer plus the narrower observation that one overlapping matrisome/fibrosis module (G1/G5) retains rank specificity in DRG over blood; we do not claim a novel mechanosensory finding." This makes the contribution transparent and defensible.

### F5 (minor) — Frozen-protocol version mismatch could undercut the "pre-specified" claim

【Problem】 The manuscript cites a deposited frozen protocol "tag v1.0.0" governing frozen endpoints (`manuscript.md:31`), but the result artifacts were generated under protocol "v0.5" (`analysis/results/layer3/layer3_generality.json:2` and `layer3b_sample_generality.json:2`). A reviewer checking reproducibility may read this as the protocol was not actually frozen at v1.0.0 when the numbers were produced.

【Evidence】 `manuscript.md:31` — "deposited frozen protocol, PROTOCOL_基质刚度与神经病理性痛.md, tag v1.0.0." Artifacts: `analysis/results/layer3/layer3_generality.json:2` "protocol": "... v0.5".

【Why it matters】 The pre-specification/frozen-endpoint design is the paper's main defence against HARKing. Any ambiguity about which protocol version produced the reported numbers weakens that defence. This alone would not drive rejection, but it is a credibility gap worth closing in revision.

【Specific fix】 Either regenerate/redeem the artifacts under the v1.0.0 protocol tag, or change the manuscript text to reference the actual version used (e.g., "frozen protocol v0.5, deposited as v1.0.0") and explicitly attest that no endpoint was altered after seeing the pain data. A one-line clarification in Methods + Declarations suffices.

---

## § Stands up (things that ARE acceptably done)

1. **Rigorous, pre-specified design with honest null governance.** The frozen-endpoint, dual-negative-control, positive-control-sensitivity design is well described (`manuscript.md:18,20,31`) and the §5.3 "equally-significant control" rule is applied correctly — Stage A is honestly called a *double-null* because both DRG and blood are non-significant (`manuscript.md:53,119`). This is exactly the discipline PLOS ONE rewards for null results.

2. **Genuine sensitivity validation of the null.** Running the 12-gene nerve-injury positive control through identical code and detecting it (g = 3.85, P = 0.0286) while HD_up stays null (g = 0.219, P = 0.80) is a strong, defensible argument that the HD_up null is *sensitivity-validated*, not a method artefact (`manuscript.md:37,58,121`; `layer3b_sample_generality.json` confirms P=0.0286). This is the paper's most solid contribution.

3. **Transparent self-qualification of the positive.** The authors disclose the G1/G5 10-gene overlap (`manuscript.md:67,138`), the G4 denominator artefact (`manuscript.md:67,135,138`), and correctly label HD_down and G3 as hypothesis-generating (`manuscript.md:58,83,93`). The audit gate even *requires* the G1/G5 overlap disclosure (`analysis/scripts/gate_consistency.py:310`). This transparency is what keeps the paper in MAJOR-REVISION rather than REJECT territory.

4. **Biologically anchored signature (Layer 0).** CTGF Δ = +1.64, P = 9.5×10⁻⁶, plus LATS directional confirmation (79.7% vs 28.6%), gives the signature real biological meaning as a controlled in-vitro program (`manuscript.md:48`). A reasonable, if modest, contribution.

5. **Reproducibility / data availability.** GitHub deposit with MANIFEST and checksum traceability, and a per-claim link to `analysis/results/` (`manuscript.md:97`). Strong for a computational reanalysis.

---

## § Questions for the authors

1. **Independent observations.** Given G1 and G5 share 10 members (one matrisome/fibrosis module counted twice) and G4 is a denominator artefact, how many *independent* BH-significant observations actually support the title's "established sets show tissue-specific shifts"? Is it effectively one?

2. **G3 placement.** G3 reaches only SI specificity (DRG×SNI q = 0.0652, not BH; Layer 3b diff = −0.277, P = 0.286). Why is it presented in the title-positive and Core conclusion #3 alongside G1/G5 rather than flagged hypothesis-only there, as the Discussion does at line 83?

3. **Protocol version.** The manuscript cites frozen protocol tag v1.0.0, but result artifacts were generated under v0.5. Can you confirm no endpoint was altered after seeing the pain data, and reconcile the version label?

4. **Title scope.** Would you accept reframing the title to scope the positive claim to the specific matrisome/fibrosis module and to name G2's failure, so the title matches the body's evidence?

5. **Contribution statement.** Could the Discussion open with a single explicit "interpretive summary" sentence that owns the null (sensitivity-validated null + one retained overlapping module) so the contribution is unambiguous to a soundness-focused editor?

---

## § What I actually checked

**Files read (independence preserved — no review/response/memory/.workbuddy files opened):**
- `manuscript/manuscript.md` — full read (190 lines).
- `analysis/results/layer3/layer3_generality.json` — confirmed G1 DRG×SNI q=0.0010, G5 q=0.0016, G3 DRG×SNI q=0.0652 (not BH), G4 BLD-SNI |Δ|=0.000925 (denominator artefact), primary_endpoint_pass=false, n_sets_failing_specificity=1.
- `analysis/results/layer3/layer3b_sample_generality.json` — confirmed G3 diff=−0.277, P=0.286, g=−0.823; verdict=FAIL; positive control P=0.0286, g=3.85; HD_up P=0.80.
- `analysis/scripts/gate_consistency.py` — confirmed the G1/G5 10-member overlap disclosure is a required gate (line 310).

**Verdict: MAJOR REVISION** — decisive reasons:
1. Title's second clause ("established ECM/mechanotransduction gene sets show tissue-specific shifts") is unsupported at the manuscript's own BH standard: only one overlapping module (G1/G5) is BH-significant; G2 failed; G3 is non-BH/non-sample-level; G4 is an artefact.
2. Abstract line 10 and Core conclusion #3 lump non-significant G3 with BH-significant G1/G5, an internal inconsistency with the Discussion (which calls G3 hypothesis-only) that reads as HARKing-adjacent and over-weights the single positive in a null-dominated study.
3. The genuine contribution (a *sensitivity-validated* null + retained specificity of one module) is real and publishable at PLOS ONE, but the paper must own the null and re-scope the positive; the methodology is sound enough that this is fixable in revision rather than grounds for rejection.
