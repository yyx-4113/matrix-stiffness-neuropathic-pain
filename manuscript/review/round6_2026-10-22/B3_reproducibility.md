# B3 — Reproducibility & Reporting Review (PLOS ONE, blind)

**Reviewer lens:** Would an independent reader (or a PLOS ONE reprod-checklist reviewer) be able to reproduce every number, and is the Methods/Reporting complete enough to replicate? Judged as a fresh submission, from the manuscript and the source I read myself. I did NOT open `manuscript/review/` sibling files, `memory/`, or `.workbuddy/` task/SOP material.

**Verdict: MAJOR (text-only revisions).** Reproduction is *feasible* — raw inputs are present, scripts are coherent, the MANIFEST checksums every cited result artifact, a consistency gate exists, and every spot-checked number (including the full three-stage Stage-A calibration) traces exactly to a deposited file. However, the Methods text is **not fully self-contained for replication**: the exact Hedges-g formula, the matched-null construction detail, and the MRU rank basis are only recoverable from code, not prose. These are exactly the items a PLOS ONE "methods detailed enough to replicate" check flags. No new analyses are required — only textual specification.

---

## 1. DATA AVAILABILITY (manuscript line 97)

**F1 — Data-availability claim is substantively met; raw inputs are present, not absent.**
【Problem】The claim "Analysis code, configuration, and all result artifacts are deposited … with a MANIFEST of checksums; every numeric claim … traceable to a file under `analysis/results/`" could be doubted because the MANIFEST keys raw inputs as `raw_inputs_not_packaged` (42 entries). A reader might infer the raw GEO CEL/matrix files must be re-downloaded, making reproduction dependent on an external server.
【Evidence】`analysis/MANIFEST.json` top keys include `raw_inputs_not_packaged` (42 entries); yet on disk `analysis/data/raw/` contains `GSE98547_RAW.tar`, `GSE98547_series_matrix.txt.gz`, `GSE111216_Parisien_Suppl_Table_01..08_*.xlsx`, `GSE261676_RAW.tar`, `GSE261676_series_matrix.txt.gz`, and the 16 per-sample `GSM*.counts.txt.gz` under `_gse261676/`; a dated `_download.sh` (verified 2026-10-21, `analysis/data/raw/_download.sh:1-19`) provides a fallback. The cited result files are all checksummed: `analysis/results/layer0/layer0_signature.json`, `layer1/layer1_diag.json`, `layer3/layer3_generality.json`, `layer2/layer2_results.json`, `layer3/layer3b_sample_generality.json`, `layer4/layer4_positive_characterisation.json` all appear in `MANIFEST.json:artifacts` with sha256.
【Why it matters】Reproduction must not silently depend on a live GEO fetch; if the server moves, the deposit must stand alone. As deposited, it does.
【Specific fix】Clarify line 97: "Raw GEO inputs (GSE98547, GSE111216 supplement tables, GSE261676 per-sample counts) are included in `analysis/data/raw/` and also retrievable via `analysis/data/raw/_download.sh` (URLs verified 2026-10-21); the `raw_inputs_not_packaged` MANIFEST key denotes that these large inputs are listed but not individually checksummed, not that they are absent."

**F2 — Three spot-checked numbers trace exactly to cited result files.**
【Problem】None — reported as verified. CTGF Δ=+1.6405, P=9.49×10⁻⁶ (`analysis/results/layer0/layer0_signature.json` → `positive_control_canonical_targets`, `delta_WT`/`p_WT`); MRU=0.71677, P=0.10229, q=0.40916 for HD_up×DRG×SNI matched null (`analysis/results/layer1/layer1_diag.json` → `stratified_vs_unstratified`, `MRU_stratified_space`/`p_expression_matched`/`q_expression_matched`); G1 SI_g=38.416 (`analysis/results/layer3/layer3_generality.json` → `per_set_specificity/G1_core_matrisome/SI`). Blood control also matches: BLD MRU=0.6964, P=0.1004, q=0.4092.
【Why it matters】Confirms the central "every number traceable" claim for the headline anchors.
【Specific fix】No change required.

---

## 2. METHODS COMPLETENESS

**F3 — The exact Hedges-g formula is not stated in the text (only "Hedges g provided the effect size").**
【Problem】A reader cannot recompute the reported effect sizes (Stage B HD_up g=0.219; positive control g=3.85; Layer-3b Table 4) from the prose alone. The manuscript (line 34) says only "Hedges g provided the effect size." The actual estimator — a bias-corrected standardized mean difference — lives only in code.
【Evidence】`manuscript/manuscript.md:34` ("Hedges g provided the effect size"); implementation at `analysis/scripts/layer2_positive_control.py:75-93`: `g = (mean(a)−mean(b))/s_pooled × (1 − 3/(4*(n1+n2)−9))`, where `s_pooled = sqrt(((n1−1)·var(a,ddof=1)+(n2−1)·var(b,ddof=1))/(n1+n2−2))`, with the small-sample correction factor `J = 1 − 3/(4·8−9) = 0.8696` at n1=n2=4. The script's own comment notes an earlier version returned *uncorrected* Cohen's d while calling it Hedges g.
【Why it matters】PLOS ONE requires the statistic be specified such that it is replicable. An independent analyst reading the paper (without the repo) would not know the small-sample correction is applied, and would reproduce Cohen's d, not Hedges g — a ~15% magnitude discrepancy.
【Specific fix】Add to line 34 (Stage B) and to the Layer-3b/4 method lines: "Effect size was bias-corrected Hedges g = (mean₁−mean₂)/s_pooled × (1 − 3/(4(n₁+n₂)−9)), where s_pooled is the pooled standard deviation (ddof=1). At n₁=n₂=4 the correction factor is 0.8696."

**F4 — MRU is described as "1-based" but the code uses 0-based ranks.**
【Problem】The MRU definition in the text says "1-based," which is not what the implementation does; the value is numerically identical (centered at 0.5) but the basis is mislabeled, which can confuse a re-implementer.
【Evidence】`manuscript/manuscript.md:31`: "MRU = median(member rank)/(n_expressed − 1), 1-based; 0.5 = no shift". Code: `analysis/scripts/layer1_projection.py:192` assigns `rank_arr[order] = np.arange(len(df))` (0…n−1, i.e., 0-based); `analysis/scripts/layer1_diag.py:176` computes `rk = ranks_of(dfe, rank_var)/(ne-1)` with `ranks_of` likewise 0-based (`:48-52`). The denominator `n_expressed − 1` with 0-based ranks yields range ≈0…1 and a 0.5 null, so results are correct, but the "1-based" wording is inaccurate.
【Why it matters】A re-implementer trusting "1-based" would divide by `n` instead of `n−1` (or center differently) and get a shifted MRU; the formula is only right because both numerator and the stated centering happen to coincide.
【Specific fix】Replace "1-based" with "computed on 0-based ranks (0…n_expressed−1), so MRU ∈ [0,1] and 0.5 = no shift."

**F5 — The matched-null construction is only fully specified in code, not prose.**
【Problem】The pre-specified null is described as "size- and baseline-expression-decile-matched, without replacement, 10 000 iterations" (line 31). The crucial detail — that *each member* is matched to *its own* baseline-expression decile (deciles among expressed genes), and that all drawn genes are distinct within a permutation — is only in the script.
【Evidence】`manuscript/manuscript.md:31` (concise prose); implementation `analysis/scripts/layer1_diag.py:70-91` (`_stratified_draws`: one distinct gene drawn per member from that member's decile pool) and `:184-187` (member bins from `dfe["bin"]`, 10 deciles on `value_CTR` among expressed genes). `n_permutations`=10000 confirmed in `layer1_results.json` (`permutation.n`=10000, `seed`=20261021).
【Why it matters】"Decile-matched" is ambiguous: per-member decile matching is far more stringent than a single global-expression-distribution match; an analyst replicating from text alone would build a different null.
【Specific fix】Expand line 31 (and the Stage-A Methods paragraph at line 53) to: "for each of the m signature members a control gene was drawn from *that member's own* baseline-expression decile (deciles computed among expressed genes, baseline = control-arm value_CTR), all m draws distinct (without replacement), 10 000 iterations, seed 20261021."

**F6 — Stage-B HD_up Hedges g is reported in the text but not persisted in the Stage-B result file.**
【Problem】The Stage-B Results (line 58) quote HD_up Hedges g = 0.219, but `layer2_results.json` (the Stage-B primary artifact) does not contain a `hedges_g` field; the value only exists in the Layer-3b artifact. The "every claim traceable to a file under analysis/results/" claim is technically true but the natural Stage-B artifact is incomplete for the effect size it quotes.
【Evidence】`manuscript/manuscript.md:58` ("Hedges g = 0.219") and `:120` (Table 2, Stage B primary g=0.219); `analysis/results/layer2/layer2_results.json` → `hippo_dependent_up.primary_saline_arm` keys are `mean_score_SNI, mean_score_sham, difference, n_SNI, n_sham, p_exact_permutation, n_permutations_enumerated, welch_t, welch_p, q_BH_family_of_4` — **no `hedges_g`**; the value 0.21874 is found only at `analysis/results/layer3/layer3b_sample_generality.json` → `table[HD_up].hedges_g_saline_arm`.
【Why it matters】A reader sent to the Layer-2 result file to verify the Stage-B effect size finds nothing; traceability relies on a different-layer file, weakening the audit trail.
【Specific fix】Either add `"hedges_g": round(float(hedges_g(score[sal_sni], score[sal_sham])),4)` to `layer2_sample_scores.py` `primary_saline_arm` and regenerate, or change line 58/Table 2 to cite the Layer-3b source explicitly ("HD_up g = 0.219, from the identical GSE261676 computation in Layer 3b / `layer3b_sample_generality.json`").

---

## 3. PRE-REGISTRATION HONESTY

**F7 — The §5.3 governance rule exists in the protocol and matches, but it is protocol §5 item 3, not a literal "§5.3" subsection.**
【Problem】The manuscript cites "§5.3 (deposited frozen protocol)" for the negative-control rule, but the protocol's §5 ("偏见控制") is a flat 5-bullet list; the rule is bullet 3, with no "§5.3" heading.
【Evidence】`manuscript/manuscript.md:31` ("The pre-specified governance rule (§5.3; deposited frozen protocol, PROTOCOL_基质刚度与神经病理性痛.md, tag v1.0.0)…"); `PROTOCOL_基质刚度与神经病理性痛.md:158` ("## 5. 偏见控制") and `:162` (bullet 3: "双阴性对照：BLD 与 BRN 预先指定为阴性对照；若阴性对照与主终点同等显著，则结论不得成立"). The rule substance matches the manuscript's description ("if a negative control is equally significant to the primary, tissue-specific attribution cannot be made").
【Why it matters】A reviewer cross-referencing the frozen protocol cannot find a "§5.3" and may think the citation is fabricated.
【Specific fix】Either re-cite as "Protocol §5(3)" / "Protocol §5, rule 3", or add a "### 5.3 阴性对照同等显著即结论不成立" heading in the protocol at line 162.

**F8 — The frozen protocol's milestone M12 records a stale positive-control Hedges g (+4.431) that disagrees with the manuscript/results (3.85) by ~15%.**
【Problem】The deposited "frozen" protocol still contains the *pre-correction* Cohen's d value for the positive control, while the manuscript and all result artifacts use the corrected Hedges g. Since the protocol is cited as the pre-registration, a reviewer comparing them sees an internal inconsistency.
【Evidence】`PROTOCOL_基质刚度与神经病理性痛.md:184` (M12: "PASS (diff=+1.285, g=+4.431)"); `analysis/results/layer2/layer2_positive_control.json` → `results/POSITIVE_CONTROL_injury_up/hedges_g = 3.8535`; `manuscript/manuscript.md:150` (Table 4 positive control g=3.853) and `:10` (abstract g=3.85). The ~4.431/0.8696 = 5.10 → actually 3.8535/0.8696 = 4.432, confirming 4.431 is the uncorrected d. The correction is documented in code at `layer2_positive_control.py:78-84` (audit R13).
【Why it matters】Pre-registration honesty is undermined if the cited frozen document carries a number the manuscript later "corrects" without an in-protocol note; it looks like the protocol was edited post-hoc to match.
【Specific fix】In the protocol, amend M12 to "g (Hedges, bias-corrected) = 3.85 (uncorrected Cohen's d was 4.43 prior to audit R13 correction)" or add a one-line erratum note at the changelog referencing audit R13, so the frozen record and the manuscript agree.

**F9 — Layer 3b / Layer 4 endpoint hierarchy is internally inconsistent ("primary" vs "characterisation").**
【Problem】The manuscript is not consistent about whether Layer 3b and Layer 4 are primary or secondary/characterisation endpoints. Table 2 and the Discussion call them "primary," while the Methods header and the overall narrative frame them as characterisation. They are genuinely pre-specified (added prospectively per protocol changelog before the relevant data were viewed), so they are NOT post-hoc — but the label should be made uniform and honest.
【Evidence】`manuscript/manuscript.md:125-126` (Table 2: "Layer 3b primary (divergence)", "Layer 4 primary (positive characterisation)") and `:79` ("four pre-specified primary endpoints were tested. Stage A, Layer 3b, and Layer 4 did not confirm…"); contrast `:42-43` (Methods header: "Sample-level divergence (Layer 3b) and positive characterisation (Layer 4)") with no "secondary" qualifier, and `:71` ("Layer 3b and Layer 4: sample-level confirmation and descriptive characterisation"). Protocol changelog shows Layer 3b added at v0.6 and Layer 4 at v0.7, both "before any … results were inspected" (`:302`, `:270`).
【Why it matters】The reviewer's specific concern — are these dressed as primary when they are really secondary/characterisation? — is partly justified by the Table-2/Discussion wording. The honest statement is: they are *additional pre-specified endpoints* (not the headline Stage-A/B primaries), and Layer 4 is explicitly descriptive.
【Specific fix】Add one sentence in the Methods (line 42-43) and align Table 2/Discussion: "Layer 3b and Layer 4 are additional *pre-specified* endpoints (Layer 3b a confirmatory divergence test, Layer 4 a descriptive characterisation); neither is the headline primary, and both were registered prospectively (protocol v0.6/v0.7) before the corresponding data were viewed."

---

## 4. FIGURE / CAPTION CONSISTENCY

**F10 — All six figures + S1 Fig are generated by the cited scripts, referenced in the body, and given legends with correct filenames. Figure 4 (HD_down matched null) body and legend agree.**
【Problem】None identified as an error. Verification: body `![...]` links at `manuscript/manuscript.md:50,55,60,62,64,69,74`; legends at `:177-189` cite the identical paths. Generation: `analysis/scripts/fig_layer2.py:119,65,92,163,224` write `fig1_signature_derivation.png, fig2_per_animal_scores.png, fig3_member_contributions.png, fig4_matched_null.png, fig5_positive_control_vs_signatures.png` into `analysis/results/layer2/fig/`; `analysis/scripts/fig_layer3.py:75,116` write `fig6_generality.png, figS1_layer3b_effects.png` into `analysis/results/layer3/fig/`. All seven PNGs exist on disk (45–49 KB each). Figure 4: body line 58 "places its observed value in the upper tail of a size- and expression-matched random-gene-set null" ↔ legend line 183 "Calibration check for the HD_down secondary endpoint: a size- and expression-decile-matched random-gene-set null … observed HD_down value lies in the upper tail" — consistent.
【Why it matters】Confirms the figures are code-derived (reproducible) and that body/legend descriptions match.
【Specific fix】No change required.

**F11 (minor) — Figure 1 (Layer-0 signature derivation) is stored under `layer2/fig/`, not `layer0/fig/`.**
【Problem】Cosmetic only: the Layer-0 derivation figure path is `analysis/results/layer2/fig/fig1_signature_derivation.png` even though its content is Layer 0. No mismatch between body and legend (both cite the same path), so it is not an error, but a reviewer may find the location confusing.
【Evidence】`manuscript/manuscript.md:50` and `:177` both cite `analysis/results/layer2/fig/fig1_signature_derivation.png`; script `analysis/scripts/fig_layer2.py:119`.
【Why it matters】Low; only a tidy-file-location note.
【Specific fix】Optional: move the figure to `analysis/results/layer0/fig/` (and update the two paths) or add a footnote in the legend explaining the file lives with the Layer-2 figure set for build convenience.

---

## 5. REFERENCES

**F12 — All 14 in-text citations [1]–[14] are present and references are correctly formatted (Vancouver, PMID + doi); two spot-checks confirm authenticity.**
【Problem】None identified. All markers `[1]`…`[14]` occur in the text (verified by search). Format is uniform Vancouver with PMID and doi. Spot-checked:
- Ref 1: Meng Z, Qiu Y, Lin KC, et al. *Nature*. 2018;560(7720):655–660. PMID 30135582, doi 10.1038/s41586-018-0444-0 — confirmed real and exact (WebSearch against PubMed/JAX).
- Ref 3 (GSE261676 source): Serafini RA, Ramakrishnan A, Shen L, Zachariou V. *Neurobiol Pain*. 2024;15:100153. PMID 38549875, doi 10.1016/j.ynpai.2024.100153 — confirmed real and exact.
【Why it matters】Confirms the data-source and method references are genuine and correctly cited.
【Specific fix】No change required. (Remaining references are standard, consistently formatted, and carry dois; a full 14/14 external verification was not performed but no anomaly was observed.)

---

## 6. MISSING REPORTING ELEMENTS A PLOS ONE REVIEWER WOULD DEMAND

**F13 — No software-environment / dependencies statement for full runnability.**
【Problem】PLOS ONE's reprod-checklist benefits from a stated environment (Python version, key package versions: numpy/pandas/scipy/openpyxl/matplotlib). None is given.
【Evidence】No `requirements.txt`/`environment.yml` and no version statement in `manuscript/manuscript.md` or `README.md` build notes; scripts import `numpy, pandas, scipy, openpyxl, matplotlib` without pinned versions.
【Why it matters】A reviewer re-running the pipeline cannot guarantee bitwise-identical results without the environment; seeds are fixed (20261021) which helps, but package-version drift (e.g., pandas ranking/decile behaviour) could alter outputs.
【Specific fix】Add to Data Availability (line 97) or a new "Code & environment" sentence: "Pipeline: Python 3.x with numpy ≥x, pandas ≥y, scipy ≥z, openpyxl, matplotlib; random seed 20261021 fixed in `ms_panel.json`; a `requirements.txt` is provided in the deposit."

**F14 — Pre-registration statement is adequate but could name the freeze commit/tag explicitly.**
【Problem】The manuscript states the protocol is "deposited frozen" and cites repo tag v1.0.0, but does not point to the protocol's own freeze marker (commit `10ec40c` / tag `v0.1.0` referenced inside the protocol at `PROTOCOL…md:172`), which would let a reviewer pin the exact pre-data-view version.
【Evidence】`manuscript/manuscript.md:18,31,97`; protocol `PROTOCOL_基质刚度与神经病理性痛.md:172` (M0: "commit 10ec40c / tag v0.1.0").
【Why it matters】Strengthens the pre-registration claim for the reprod-checklist ("was it pre-specified, and where?").
【Specific fix】Add to line 31/97: "…frozen at protocol commit 10ec40c (tag v0.1.0); the project repository snapshot is tag v1.0.0."

---

## § Stands up (verified reproducible / complete)

1. **Every headline number I traced reproduces exactly.** Beyond the three required spot-checks, the *entire* Stage-A three-calibration narrative reproduces: full-background unstratified DRG P=0.59674 / BLD P=0.0009; diagnostic unstratified DRG P=0.0554 / BLD P=0.0855; expression-matched primary DRG P=0.1023 / BLD P=0.1004 / q=0.4092 — all exactly as written at `manuscript/manuscript.md:52-53`, from `layer1_results.json` and `layer1_diag.json`.
2. **Raw inputs are genuinely deposited, not merely referenced.** `analysis/data/raw/` contains the GSE98547 RAW tar, GSE111216 eight supplement xlsx tables, GSE261676 per-sample counts and series matrix, plus a dated `_download.sh` — so reproduction does not require a live GEO fetch.
3. **The MANIFEST is real and checksum-backed.** `analysis/MANIFEST.json` holds 92 artifact entries with sha256 and lists the 42 raw inputs; all six cited result files are present with checksums.
4. **A reproducibility/consistency gate exists.** `analysis/scripts/gate_consistency.py` is designed to re-derive headline numbers from the deposited artifacts (not re-run statistics) and asserts mutual coherence; the commit history shows it passing (gate 43/43). This is a strong positive for a reprod reviewer.
5. **Layer 3 & 4 specificity/characterisation numbers trace.** G1 SI_g=38.416 (`:132`/result file); Table 3 footnote correctly warns G4's denominator is unstable (blood MRU≈0.5, |Δ|≈0.0009) and that G1/G5 overlap by 10 members — honest handling; Layer 4 `n_genes_tested=15345`, 8 up/3 down, ECM-union Fisher OR=0, P=1.0, HD_up 0 sig-up, verdict FAIL — all match `layer4_positive_characterisation.json`.
6. **Pre-specification is real, not post-hoc.** Layer 3b (protocol v0.6) and Layer 4 (v0.7) were registered before the corresponding data were inspected (protocol `:270,:302`), so they are legitimately pre-specified; the §5.3 negative-control rule matches the protocol's §5(3).
7. **All 6 + S1 figures are code-generated, body-referenced, and legend-consistent** (F10), and all 14 references/citations are present and correctly formatted (F12).

---

## § Questions for the authors

1. Will you add the explicit Hedges-g formula (with the small-sample correction factor) to the Methods, so the effect sizes are replicable from prose alone (F3)?
2. Will you correct the MRU "1-based" wording to "0-based" and expand the matched-null description to state *per-member* decile matching (F4, F5)?
3. Will you persist HD_up Hedges g in `layer2_results.json` (or cite the Layer-3b source) so the Stage-B effect size is traceable within its own result file (F6)?
4. Will you reconcile the protocol's M12 g=+4.431 with the corrected Hedges g=3.85, and re-label Layer 3b/4 endpoint hierarchy consistently as "additional pre-specified endpoints" (F8, F9)?
5. Will you add a software-environment/dependencies statement and name the protocol freeze commit (F13, F14)?
6. (For the panel) The positive-control P is reported as 0.0286 in the manuscript while `layer2_positive_control.json` stores `mann_whitney_p = 0.028571` and `welch_p = 0.001331`; the manuscript correctly governs on the exact-permutation P (0.0286). Please confirm in the text that the governing P is the exact permutation, with Welch/Mann–Whitney as cross-checks, so no reader mistakes the Welch P (0.0013) for the endpoint.

---

## § What I actually checked

**Files read (manuscript & source only):**
- `manuscript/manuscript.md` — full read (190 lines).
- Scripts: `layer0_stiffness_signature.py`, `layer1_projection.py`, `layer1_diag.py`, `layer2_sample_scores.py`, `layer2_positive_control.py` (partial, Hedges-g fn), `layer3_generality.py`, `layer3b_sample_generality.py` (partial), `layer4_positive_characterisation.py` (grep), `fig_layer2.py`, `fig_layer3.py`, `gate_consistency.py` (head), `gen_manifest.py` (not separately re-run).
- Results JSON (existence + content): `layer0_signature.json`, `layer1_results.json`, `layer1_diag.json`, `layer2_results.json`, `layer2_positive_control.json`, `layer2_robustness.json` (partial), `layer3_generality.json`, `layer3b_sample_generality.json`, `layer4_positive_characterisation.json`, `MANIFEST.json`.
- Protocol: `PROTOCOL_基质刚度与神经病理性痛.md` (§5 lines 158-198; M12 line 184; changelog v0.6/v0.7 lines 270,302).
- `manuscript/build_docx.py` — not required for this lens; figure/caption/number consistency was verified directly against source, which suffices.

**Existence verified:** all 7 figure PNGs on disk; git tag `v1.0.0` present; raw GEO inputs present; MANIFEST 92 artifacts + 42 raw inputs.

**Discrepancies stated:** (a) MRU "1-based" vs 0-based code; (b) Hedges-g formula absent from prose; (c) Stage-B HD_up g not in `layer2_results.json`; (d) protocol §5.3 is actually §5 item 3; (e) protocol M12 g=+4.431 vs results 3.85 (pre-correction Cohen's d); (f) Layer 3b/4 "primary" vs "characterisation" wording inconsistency; (g) no environment/dependency statement; (h) Figure 1 stored under `layer2/fig/`.

**Spot-checks that PASSED:** CTGF Δ=1.64/P=9.5e-6; MRU=0.717/P=0.102/q=0.409 (DRG) and 0.696/0.100/0.409 (BLD); G1 SI=38.4; positive control diff=1.285/P=0.0286/g=3.85; full Stage-A 3-calibration set; Layer 4 (15345 genes, 8 up/3 down, ECM-union OR=0/P=1.0); references 1 & 3 authentic.

**Verdict: MAJOR** — reproduction is feasible and the numbers are trustworthy and traceable, but the Methods text is not self-contained for replication (Hedges-g formula, matched-null per-member construction, and MRU rank basis are code-only). All fixes are textual; no new analyses needed. Once F3–F6, F8, F9, F13–F14 are addressed, this would clear to ACCEPT.
