# Round-2 Review — A2 (Study Design / Biostatistics)

**Reviewer:** A2 Design (blind; did not read other reviewers' R2 outputs)
**Manuscript:** `manuscript.md` (current working version)
**Source of truth:** `analysis/results/**/*.json` (read directly and recomputed)
**Independence statement:** All numbers below were re-derived by me from the raw JSONs; no other reviewer's text was consulted.

---

## 1. Round-1 points — status

### T1-1 — Robustness misattribution (LOO + Q4 → HD_down) — **RESOLVED**
- `layer2_robustness.json` confirmed: `n_members_present = 33`, members = Abca7…Thbs3, `Q3_baseline_difference = 0.39671`, `Q4_matched_null.p_empirical = 0.092091`, LOO diffs 0.32–0.45 — i.e. **HD_down**, exactly as Round-1 asserted.
- Manuscript `manuscript.md:64` now correctly attributes the robustness evidence to HD_down:
  > "HD_down reached a nominally significant but BH-non-significant (q = 0.086) reverse elevation (difference = +0.397, P = 0.0286, g = 2.658) … **its direction was preserved under leave-one-animal-out and a Q4 expression-matched null (P = 0.092)**, supporting that the elevation is not a single-animal artifact."
- The HD_up bounded-null claim (diff +0.146, P 0.80, g 0.219) no longer borrows the Q4/LOO artifact. **Traceability gap closed.**

### T1-2 / SI fragility — **RESOLVED (with a residual, see NEW-2)**
- Table 3 (`manuscript.md:130-140`) now carries `|ΔDRG−0.5|` and `|ΔBLD−0.5|` columns and a stabilizing footnote:
  > "*SI_g … is unstable when |ΔBLD−0.5| ≈ 0 (G1 denominator 0.011; G4 denominator 0.0009); read the absolute shifts directly.*"
- SI values recomputed from `layer3_generality.json`: G1 38.416, G2 0.440, G3 1.438, G4 240.472, G5 9.055 → manuscript 38.4/0.44/1.44/240.5/9.06 ✓. G4 flagged as denominator-driven, not over-interpreted ✓.

### T1-5 — "equally significant" → "equally non-significant" — **PARTIALLY RESOLVED (residual, see NEW-3)**
- Abstract (`manuscript.md:14`), Table 2 (`manuscript.md:121`), and Discussion (`manuscript.md:85`) now correctly read **"equally non-significant"** (DRG q = BLD q = 0.409). ✓
- **Residual:** the Stage A Results paragraph (`manuscript.md:59`) still reads the old wording:
  > "Per §5.3, because the negative control is **equally significant**, no tissue-specific attribution can be made"
  This is the exact phrase Round-1 flagged as misleading (it can be misread as "the control lit up"); it was supposed to become "equally non-significant." Not yet fixed at this location.

### Stage A §5.3 verdict framing — **RESOLVED**
- `manuscript.md:58-59` frames the result as *uninformative, not merely "negative,"* and keeps the unstratified "blood two orders stronger" artifact (`DRG P = 0.597`, `BLD P = 0.0009`) explicitly separate ("*explicitly not the primary endpoint*"). Verified against `layer1_results.json` (`hippo_dependent_up` DRG×SNI primary `p_permutation = 0.59674`; BLD×SNI `p_permutation = 0.0009`). Correct separation of calibration regimes maintained.

### Layer-3 primary rule reframed as specificity retained — **RESOLVED**
- `manuscript.md:73`: "Only 1/5 sets lacked specificity, so the pre-specified primary rule (≥ 4/5 failing) was **not** met — we could *not* demonstrate that specificity failure is universal."
- Discussion `manuscript.md:85`: "the Layer-3 primary was also not met — but its non-meeting means specificity was *retained*, not lost." Honest, data-consistent reframing ✓.

### Hedges g labeling & values — **RESOLVED**
- All cited effect sizes match JSON and are labeled "Hedges g": pos ctrl g=3.853 (`layer2_positive_control.json` 3.8535) → ms 3.85 ✓; HD_up g=0.2187 → 0.219 ✓; HD_down g=2.6584 → 2.658 ✓; 17.6-fold gap = 3.853/0.219 = 17.59 ✓. No Cohen's-d mislabel found.

---

## 2. New statistical issues found

### NEW-1 — Combinatorial misstatement in the permutation description (`manuscript.md:40`)
> "The B-primary … tested by exhaustive exact permutation over all **C(8,4) = 35** (4-vs-4) or 70 (8-sample) splits, two-sided…"

**Error:** C(8,4) = **70**, not 35. The 4-vs-4 design enumerates 70 ordered assignments; the two-sided lower bound used for the positive control is P = 0.0286 = 2/70, which is only consistent with a denominator of 70. The companion artifact `layer3b_sample_generality.json` (design.test) correctly states *"exact permutation over all C(8,4)=70 splits, two-sided."* The manuscript's "C(8,4) = 35" is therefore an arithmetic/notation error and internally contradicts its own source JSON.
**Fix:** "exhaustive exact permutation over all C(8,4) = 70 splits (equivalently 35 unordered 4-vs-4 partitions), two-sided." The P-values themselves (2/70 = 0.0286 for the positive control; 56/70 = 0.80 for HD_up) are correct — only the stated count is wrong. Minor, but should be corrected.

### NEW-2 — SI absolute columns do not reproduce the printed SI after rounding (`manuscript.md:132-138`, residual of T1-2)
The new `|ΔDRG−0.5|` / `|ΔBLD−0.5|` columns are rounded to 3 decimals, and for near-zero denominators a reader who divides the *printed* columns gets a different SI than the printed SI:
- G1: printed 0.406 / 0.011 = **36.9**, but printed SI = 38.4 (true ratio 0.4056/0.0106 = 38.42).
- G4: printed 0.222 / 0.0009 = **247**, but printed SI = 240.5 (true 0.2224/0.000925).
- G5: 0.386 / 0.043 = 8.98 vs printed 9.06.
G2 and G3 reproduce fine (0.118/0.268=0.44; 0.304/0.211=1.44).
**Why it matters:** the whole point of adding these columns (T1-2) was to let readers verify SI directly; at 3-dp precision they fail to do so for exactly the unstable cases the footnote warns about. **Fix:** report the absolute shifts at ≥4 dp (or as the exact values 0.0106 / 0.000925 / 0.0426) so the ratio reconstructs.

### NEW-3 — Residual "equally significant" wording (`manuscript.md:59`) — see T1-5 above
The Stage A Results paragraph still says "equally significant" instead of "equally non-significant," inconsistent with the Abstract/Table 2/Discussion fix. Cosmetic but a direct Round-1 carry-over; change to "equally non-significant."

---

## 3. Other checks performed (no error found)
- **BH vs uncorrected:** Stage A q=0.409 (BH, from `layer1_diag.json`), Layer-3 8/40 BH-significant (`n_surviving_BH_0.05=8`, all DRG/SC/BRN, blood 0 — recomputed row-by-row ✓), Layer-3b `q_BH_family_of_7` correctly shows none <0.05 (only pos-ctrl 0.20), Layer-4 "8 sig-up (q<0.05)" correctly labeled BH, HD_down q=0.086 labeled BH-non-significant. No BH/uncorrected confusion.
- **Permutation two-sided logic at the lower bound:** pos ctrl 2/70=0.0286 ✓; HD_up 56/70=0.80 ✓; HD_down 2/70=0.0286 ✓ (all `n_permutations_enumerated=70` in JSONs).
- **Layer-3b 7-row table** vs `layer3b_sample_generality.json`: 7 rows, diff/P/g/q all match (G1 0.513/0.229/0.839 … pos ctrl 1.285/0.0286/3.853) ✓; verdict FAIL (`a=false,b=true,c=true`) ✓.
- **Layer 4:** 15345 tested, 8 up / 3 down, ECM-union sig-up = 0, Fisher OR=0, P=1.0 — matches `manuscript.md:78`.
- **Unstratified artifact kept separate** (L59) and correctly cited (DRG 0.597, BLD 0.0009).
- No number in the manuscript was found that cannot be traced to a JSON.

---

## 4. VERDICT — **MINOR**

All five substantive Round-1 A2 concerns are resolved (T1-1 fully; T1-2, T1-5 with minor residuals; Stage-A verdict, Layer-3 reframing, Hedges-g labeling fully). The single Round-1 "必修" item (robustness attribution) is closed. The three new findings (NEW-1…3) are **presentation/notation defects only** — the underlying statistics, P-values, effect sizes, and BH corrections are all correct and traceable; none affects the conclusions (bounded null + sensitivity-validated; specificity retained). Recommend acceptance after fixing NEW-1 (C(8,4)=70), NEW-2 (SI column precision), and NEW-3 (leftover "equally significant" wording at L59).
