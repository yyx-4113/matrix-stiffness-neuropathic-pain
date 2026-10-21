# Round-2 A3 — Implementation / Auditor verification

**Reviewer:** A3 Implementation (blind; did not read other Round-2 outputs)
**Manuscript:** `manuscript/manuscript.md`
**Protocol:** `PROTOCOL_基质刚度与神经病理性痛.md` (now v0.5/v0.7 in changelog)
**Gate:** `analysis/scripts/gate_consistency.py`
**Verdict scope:** numeric traceability Layer 0 → Layer 4, consistency gate, protocol reconciliation.

---

## 1. Consistency gate result

**39 / 39 assertions PASS. Exit code 0, "ALL ASSERTIONS PASS".** No assertion failed.

Derivation discipline (per user's audit requirement — confirmed by reading the script, not assumed):
- Every `chk(...)` pulls its comparison value from a deposited JSON (`layer0/1/1diag/2/2robustness`, `layer3_generality`, `audit_tissue_identity`) or from raw inputs (FPKM gz, `layer2_sample_scores.csv`, GSE111216 `.xlsx`), **not** from a memory constant.
- The L3 verdict is **derived**: `n_fail_l3 = sum(specificity_failed)` and `primary_endpoint_pass == (n_fail >= 4)` — both checked against the JSON's own stored `n_sets_failing_specificity` / `primary_endpoint_pass`, so a hard-coded verdict could not pass.
- Several RECOMPUTE checks re-derive headline numbers straight from raw files (HD_down saline diff from scores, CTGF log2 displacement from raw FPKM, HD_up homology-map rate from the GSE111216 xlsx, G2 DRG-SNI MRU from the deposited table). The only literals are methodological constants (α=0.05, KS>0.4, zero-baseline>40%, map-rate floor 0.7, seed 20261021), not stale result numbers. This is consistent with the script's own discipline note (a gate that hard-codes an old number protects a bug).

---

## 2. Round-1 points — RESOLVED / UNRESOLVED

| # | Round-1 item | Status | Evidence |
|---|---|---|---|
| T2-5 | Protocol §8.1 stale BLD q (0.0072) | **RESOLVED** | Protocol lines 258 & 295 now read **BLD q = 0.409** (= DRG q, matching `layer1_diag.json` matched value 0.40916). The 0.0072 fingerprint is gone from both protocol and manuscript. |
| T2-1 | Print Layer-3b 7-row table | **RESOLVED** | Manuscript **Table 4** now prints all 7 rows (G1–G5, HD_up, positive control) with n/diff/P/g/q. Values match `layer3b_sample_generality.json` exactly (verified below). |
| T2-2 | Cross-reference HD_up & positive control between Stage B and Layer 3b | **RESOLVED** | Table 4 footnote states the two rows "reproduce the Stage B results (identical GSE261676 computation) … not independent tests." |
| T2-3 | "equally significant" → "equally non-significant" | **MOSTLY RESOLVED (minor residue)** | Result is correctly phrased "equally non-significant" on lines 14, 85, 121. However "equally significant" still appears on **line 37** (describing the §5.3 rule) and **line 59** (reasoning clause: "because the negative control is equally significant …"). Both q = 0.409 are non-significant, so factual content is fine; only wording in the line-59 clause should be harmonized to "equally non-significant." Not a numeric/traceability defect. |
| T2-4 | Citations for post-hoc ECM/YAP–TAZ separation | **OUT OF SCOPE** | Biology/interpretation item (A1 remit). Not verified by A3. |
| T2-6 | Add `layer1_results.json` & `layer2_results.json` to MANIFEST | **RESOLVED** | `analysis/MANIFEST.json` (generated, n_artifacts=45) includes `analysis/results/layer1/layer1_results.json` and `analysis/results/layer2/layer2_results.json` — the two files carrying the unstratified 0.597/0.0009 and HD_down q = 0.086. |

A3's own Round-1 Findings 1→T2-2, 2→T2-6, 3→T2-1 are all resolved by the above.

---

## 3. Spot-check of manuscript Tables 1–4 and inline numbers vs JSON

- **Layer 0:** CTGF Δ=+1.64 / P=9.5e-6 → `layer0_signature.json` delta_WT 1.6405 / p_WT 9.494e-6 ✅. HD_up=18, HD_down=41; LATS HD 79.7% / HI 28.6% ✅ (Round-1 audit, confirmed).
- **Stage A (Table 2, line 14/59):** DRG×SNI MRU 0.717 / P 0.102 / q 0.409; BLD×SNI 0.696 / 0.100 / 0.409 → `layer1_diag.json` matched values 0.7168/0.1023/0.4092 and 0.6964/0.1004/0.4092 ✅. Unstratified diagnostic DRG 0.597 / BLD 0.0009 → `layer1_results.json` 0.59674 / 0.0009 ✅ (now in MANIFEST).
- **Stage B / Layer 2 (Table 2, line 64):** HD_up diff 0.146 / P 0.80 / g 0.219; HD_down 0.397 / 0.0286 / g 2.658 / q 0.086; positive control 1.285 / 0.0286 / g 3.85 → `layer2_positive_control.json` + `layer2_results.json` (q 0.085713) ✅. 17.6-fold g-gap = 3.8535/0.2187 ✅.
- **Layer 3 (Table 3):** all 5 rows recomputed from `layer3_generality.json` per_set_specificity:
  - G1 0.906/0.511/0.406/0.011/38.4 ✅ (json 0.9056/0.5106/0.4056/0.0106/38.42)
  - G2 0.618/0.768/0.118/0.268/0.44 ✅ (0.6180/0.7681/0.1180/0.2681/0.4402)
  - G3 0.804/0.711/0.304/0.211/1.44 ✅ (0.8040/0.7114/0.30398/0.2114/1.438)
  - G4 0.722/0.499/0.222/0.0009/240.5 ✅ (0.7224/0.4991/**0.000925**/240.47 → 0.0009 is |0.499075−0.5|, legitimate)
  - G5 0.886/0.457/0.386/0.043/9.06 ✅ (0.8857/0.4574/0.3857/0.0426/9.055)
  - New `|ΔDRG−0.5|` / `|ΔBLD−0.5|` columns and the stabilizing footnote (SI unstable when |ΔBLD−0.5|≈0, G1 denom 0.011, G4 denom 0.0009) are present and correct (T1-2 fix applied).
  - 8/40 BH-significant, all DRG/SC/BRN, blood 0 → json n_surviving_BH_0.05=8 + recomputation ✅.
- **Layer 3b (Table 4, 7 rows):** G1 62/0.513/0.229/0.839/0.440; G2 12/0.174/0.657/0.310/0.767; G3 22/−0.277/0.286/−0.823/0.440; G4 20/0.393/0.171/1.131/0.440; G5 21/0.371/0.314/0.766/0.440; HD_up 11/0.146/0.800/0.219/0.800; pos ctrl 12/1.285/0.0286/3.853/0.200 → `layer3b_sample_generality.json` ✅. 0/5 ECM sig-up and g-range 0.31–1.13 match ✅.
- **Layer 4 (line 78):** 15 345 tested, 8 sig-up, 3 sig-down, ECM-union sig-up 0 (OR 0, P 1.0), HD_up sig-up 0 → `layer4_positive_characterisation.json` ✅ (Round-1 audit confirmed).

**Stale-fingerprint hunt (manuscript):**
- `0.0072` — **not present** anywhere ✅.
- `0.0009` — appears on **line 59** (unstratified BLD, traceable to `layer1_results.json`) and on **lines 137 & 140** (G4 `|ΔBLD−0.5|`, traceable to `layer3_generality.json` 0.000925). All three are legitimate and JSON-backed; **no stale fingerprint**.
- `two orders` — **not present** ✅.
- `equally significant` — present on lines 37 & 59 (see T2-3 residue above); result statements correctly use "equally non-significant".

---

## 4. NEW traceability gap(s)

1. **MANIFEST completeness (NEW, non-blocking).** `analysis/MANIFEST.json` **has been generated** (n_artifacts = 45; Task #21 partly done). However it **omits** the Layer-3, Layer-3b, and Layer-4 result artifacts:
   - `analysis/results/layer3/layer3_generality.json` — MISSING from MANIFEST
   - `analysis/results/layer3/layer3b_sample_generality.json` — MISSING from MANIFEST
   - `analysis/results/layer4/layer4_positive_characterisation.json` — MISSING from MANIFEST
   The manuscript's Data-availability statement claims "every numeric claim … is traceable to a file under `analysis/results/`." The underlying numbers **are** all present in those JSONs (verified above), so content traceability holds; only the checksum inventory (MANIFEST) is incomplete. Per the brief, MANIFEST completion is Task #21 and is **not a blocker for content acceptance** — but `gen_manifest.py` should be re-run (or the three files added) before final packaging so the MANIFEST actually covers every cited artifact.
2. **Wording residue (NEW, minor).** Line 59 reasoning clause still reads "equally significant"; harmonize to "equally non-significant" for consistency with T2-3. No numeric impact.

No new numeric mismatch between manuscript and JSON was found.

---

## 5. VERDICT

**MINOR.**

Rationale:
- The consistency gate is **39/39 PASS** and derives its checks from JSON/raw inputs (no hard-coded stale values) — the arithmetic layer is sound.
- All Round-1 A3 content points are resolved: protocol §8.1 (and line 295) BLD q is reconciled to 0.409; the Layer-3b 7-row table and the `|ΔDRG−0.5|`/`|ΔBLD−0.5|` columns + stabilizing footnote are in place; the Stage-B/Layer-3b cross-reference is present; no stale `0.0072`/`two orders` fingerprints remain; `layer1_results.json`/`layer2_results.json` are now in the MANIFEST.
- Every headline number in Tables 1–4 and the inline text traces to a result JSON and matches it.
- Remaining items are non-content: (a) a minor wording residue ("equally significant" on line 59) and (b) an incomplete MANIFEST (missing layer3/layer3b/layer4 result JSONs) — both explicitly non-blocking for content acceptance and easily closed at final packaging.

Content (numbers, consistency, protocol reconciliation) is **acceptable**; minor housekeeping remains.
