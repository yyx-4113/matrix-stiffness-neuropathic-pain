# A2 — Prose-fidelity / drift review (independent, blind-panel)

**Manuscript:** `manuscript/manuscript.md` (de-AI polished version)
**Reviewer role:** Domain scientist + Prose-fidelity reviewer
**Remit:** Confirm the de-AI polish (em-dash removal, phrase flattening, abstract trim to 289 words) introduced **no expression drift** in meaning, hedging strength, or the honesty discipline. I judged the text as a fresh submission and cross-checked every rephrased quantitative claim against `analysis/results/`.

> Independence note: I did not open `manuscript/review/`, any `RESPONSE_*.md`/`REVIEW_*.md`, `round5_2026-10-22/` outputs from other reviewers, memory/, or any `.workbuddy/` task-status files. All judgements come from text I read myself.

---

## 【Problem】
Discussion 第 83 行把 G3 与“稳定的、BH 显著的信号”打包在同一个名词短语里，与全文其它位置的诚实表述直接冲突。

## 【Evidence】
manuscript.md:83 — `the stable, BH-significant signal is the DRG-over-blood shift of G1 and G5 (q = 0.0010 and 0.0016 in DRG×SNI) plus a mechanosensory signal in G3`

对比：
- manuscript.md:71（Results）— `The stable, BH-significant signal is the DRG-over-blood shift of G1 and G5 (both q = 0.0010 and 0.0016 in DRG×SNI); G3 retains specificity by SI (1.44) but does not reach BH significance and was not upregulated at the sample level (Layer 3b)`
- manuscript.md:85（Discussion）— `the genuine, independent wins are G1, G3, and G5, of which G1 and G5 reach BH significance`

数据层面：layer3_generality.json 中 `G3_mechanosensing_adhesome` 的 `SI = 1.4379`（保留特异性），但其 BH q 在 DRG×SNI 为 `q_matched_BH40 = 0.0652`（见 Table 3 / layer3b Table 4 中 G3 在 sample 级 `q = 0.440`），从未达到 BH 显著。

## 【Why it matters】
句法上 `the stable, BH-significant signal is [G1/G5] plus [a mechanosensory signal in G3]` 把前置定语 “BH-significant” 同时施加到两个信号上，读者会自然读作 “G3 也是 BH 显著的 DRG-over-blood 信号”。但这与 line 71/85 的明确措辞（“G3 does not reach BH significance”、“of which G1 and G5 reach BH significance”）矛盾。本研究的核心诚实纪律正是 **G3 仅为假设生成、非确证发现**：line 87 明确 “We flag this only as a hypothesis”，Limitations line 97 也把 G3 的 DRG-over-blood shift 列为 “a hypothesis, not a finding”。该句虽处在 “needs qualifying” 段落，但局部表述越界，存在把 G3 轻微过度陈述为已确证信号的风险。
（说明：这更像润色前已存在的措辞，本轮回的 flattening 编辑未触及此处，故我将其作为**一致性/诚实纪律问题**提请作者注意，而非严格意义上的“润色漂移”；但它确实违反了 G3 的诚实纪律，必须修。）

## 【Specific fix】
将
> `the stable, BH-significant signal is the DRG-over-blood shift of G1 and G5 (q = 0.0010 and 0.0016 in DRG×SNI) plus a mechanosensory signal in G3`

改为
> `the stable, BH-significant signal is the DRG-over-blood shift of G1 and G5 (q = 0.0010 and 0.0016 in DRG×SNI), and a mechanosensory signal in G3 (SI = 1.44) that retains specificity but does not reach BH significance`

这样与 line 71/85 的措辞完全对齐，且保留该段 “needs qualifying” 的再保证语气。

---

## § Stands up（我怀疑漂移、但核验后完好）

1. **Em-dash 去除后句子语法完整、含义未变。** 全文 `—` 已为零（已 grep 确认）。重点核查位：Abstract line 14（`This is a sensitivity-validated null, not a methodological one. The failure is specific to this signature and cell type, not to projection generally.` 与 `Our result does not disprove …; it limits that claim …` 语义连贯）、Discussion line 83/89、Figure Legends line 181–193。均无断裂句、无矛盾句。

2. **“passed with full separation”（line 83）并非夸大。** 我核对了 layer2_positive_control.json 的 per_animal 数据：saline 臂 SNI 四值（0.600/0.286/0.367/0.781）全正、sham 四值（−1.237/−0.518/−0.838/−0.513）全负，即两组 z 分数完全不重叠 → 恰好对应精确置换最极端拆分，P = 2/70 = 0.0286，这正是 line 62 / line 189 所述的 “exact-permutation lower bound”。因此 “full separation” 与 “detected at the lower bound” 完全一致，**不构成 overstatement**。对 check #4 的疑虑已排除。

3. **“limits that claim … without disproving it” 完整保留原意。** Abstract line 14（`Our result does not disprove the literature's "ECM enrichment in pain" claim; it limits that claim to the projected signature's source cell type.`）与 Discussion line 89（`Our null therefore limits the literature's "ECM enrichment in pain" claim to the source cell type of the projected signature, without disproving it.`）都准确传达了原 “circumscribes … to the source cell type / 不 disprove” 的界限限定含义，未弱化也未强化。

4. **“needs tempering / needs qualifying” 保留原 hedging 强度。** Results line 71（`The "retained specificity" reading needs tempering.`）与 Discussion line 83（`The Layer-3 benchmark's positive reading needs qualifying.`）对应原 “must be tempered / must be qualified”，克制力度未变。

5. **“the simplest explanation is a cell-type- and mechanical-input-specific limit”（line 89）等同于原 “most parsimoniously …”。** 奥卡姆/最简解释的语义完好，未改变结论强度。

6. **“hypothesis-generating only” → “a hypothesis, not a finding” 未改变诚实立场。** Limitations line 97 中 “is a hypothesis, not a finding” 与 “HD_down is likewise hypothesis-generating only”；G3 段 line 87 “We flag this only as a hypothesis … and was not upregulated at the sample level (Layer 3b, G3 diff = −0.277, P = 0.286)” —— 均为明确的假设框架，未弱化也未强化为确证。

7. **“We note the exact-permutation lower bound …” 被删后，其实质在 line 83 内文保留。** line 83 仍含 `the exact-permutation lower bound of P ≈ 0.029 means the null is bounded at this design, not tightly bounded in absolute magnitude`，与 Stage B line 62、Fig 5 legend line 189 一致，实质未丢失。

8. **全部定量主张与分析产物逐字吻合（已抽样核对）：** HD_up diff +0.146 / P 0.80 / g 0.219；positive control +1.285 / P 0.0286 / g 3.85；HD_down +0.397 / P 0.0286 / q 0.086 / g 2.658；G1–G5 SI = 38.4 / 0.44 / 1.44 / 240.5 / 9.06；G1 q 0.0010、G5 q 0.0016；Layer 3b 0/5 显著、PC q 0.200；Layer 4 = 8 显著上调、ECM-union 0（Fisher OR 0, P 1.0）、HD_up 0。任何再措辞下的数字均未漂移。

9. **Abstract 289 词删节未丢失任一关键要素。** 已逐项确认仍包含：YAP/TAZ–TEAD 依赖性签名（HD_up 18; HD_down 41）、GSE98547/111216/261676、CTGF 锚点（Δ = +1.64, P = 9.5×10⁻⁶）、阳性对照（12-gene set: +1.285, P 0.0286, g 3.85）、Stage A 双 null（§5.3 未触发）、Stage B bounded null、1/5 特异性失败（G1/G5 重叠 10 成员 + G4 分母伪迹）、以及 “limits, not disproves” 结论。无遗漏端点或引用。

---

## § Questions for the authors

1. Discussion line 83 的 G3 打包表述（见上条 Finding）是否确为作者本意？如非，请采纳上面的 paste-ready 修改，使其与 line 71/85 的 “G3 does not reach BH significance” 对齐。
2. （非阻断）Abstract 未显式标注 HD_down 为 “hypothesis-generating only”，而 Limitations / Stage B 均强调。考虑到 abstract 已有篇幅压力，可不补；但如需最严格一致，可在 Stage B 句后加半句提及 HD_down 为探索性。请作者定夺。
3. （非阻断）Discussion line 83 “passed with full separation” 虽经我核验为准确，但 “full separation” 是较口语化的措辞；若希望与 Methods/Results 的精确置换术语完全统一，可改为 “passed at the exact-permutation lower bound (complete 4-vs-4 separation)”。非必须。

---

## § What I actually checked

- **通读** `manuscript/manuscript.md` 全文（199 行），重点比对 prompt 指出的 em-dash 去除位（Abstract 14、Discussion 83/89、Figure Legends 181–193）及所有 flattening 改写点。
- **grep** 全文确认 `—` 已彻底移除（0 命中）。
- **抽样核对分析产物**（仅 `analysis/results/`，未触碰 review/）：
  - `layer2/layer2_results.json` + `layer2_positive_control.json` → HD_up / positive control / HD_down 的 diff、P、g、q、coverage 与 manuscript 一致；并据 per_animal 数据验证 “full separation” 即 P = 2/70。
  - `layer3/layer3_generality.json` → G1–G5 的 SI、MRU、BH q（含 G1/G5 DRG×SNI q ≈ 0.0010/0.0016）、n_sets_failing = 1；与 Table 3、manuscript line 12/71/83 一致；确认 G3 仅 SI 保留特异性、未达 BH 显著。
  - `layer3/layer3b_sample_generality.json` → 0/5 ECM 显著上调、PC P 0.0286 / q 0.200，与 Table 4 / line 76 一致。
  - `layer4/layer4_positive_characterisation.json` → 15 345 基因、8 显著上调 / 3 下调、ECM-union 0、HD_up 0，与 line 76/Table 2 一致。
- **内部一致性排查**：G3 的 BH 显著性在 line 71/83/85 之间；HD_up “sensitivity-validated null”（line 62/83/94）与 “not a method artifact”；HD_down / G3 “hypothesis-generating only” 在 Limitations/Stage B/G3 段；均一致，除上条 Finding 的 line 83 局部打包问题。
- **Abstract 完整性**：按 prompt 清单逐项确认 9 类要素均在，无端点/引用丢失。

**结论：** 本轮 de-AI 润色在 em-dash 去除、短语扁平化、摘要删节三方面基本未引入表达漂移；全部定量措辞与分析产物一致，核心诚实纪律（HD_down 与 G3 仅为假设生成、null 为敏感性验证而非方法伪迹）整体保留。唯一需修之处是 Discussion line 83 将 G3 与 “BH-significant signal” 不当打包，与上、下文冲突，建议按上列 paste-ready 句修正。
