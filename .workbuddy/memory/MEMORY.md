# 项目约定 — 基质刚度 × 神经病理性痛

## 硬约束
- **前瞻性指定**：`analysis/config/ms_panel.json` 冻结标签 `ms-proto-frozen-2026-10-21`；任何改动须在协议 changelog 加条目 + 版本递增，且必须发生在**对应数据被审视之前**。
- **协议修订史必须公开**：v0.1（初版）→ v0.2（R1 Hippo 分层符号规则修正、R2 biotype 过滤、R3 BH NaN 处理）→ v0.3（新增 Stage B 队列）。三次修订的动机、时间、以及"信息仅来自 Layer-0 内部"的声明都在协议中留痕。
- **Stage A 不得被 Stage B 取代**：不论 Stage B 结果如何，Stage A 的阴性结果必须同时报告。已在协议中写成"不可删除"条款。
- **不得因结果不利于假设而弱化措辞**：HD_down 信号未过 BH 与匹配零分布，必须写成"有界假设生成"，不能写"趋势显著"。

## 分析口径
- 签名 source：GSE98547（人 HEK293A）；投射目标：小鼠 → 符号映射用 capitalize 规则，mapping rate < 0.7 则主终点降级。
- 表达过滤：FPKM > 1 于 ≥6/24 样本（L0）；CPM > 1 于 ≥4/16 样本（Stage B）。
- biotype：GENCODE v24lift37（与 cufflinks 输入 Gencode r24/hg19 一致），仅 `protein_coding`。
- 排列种子：**20261021**（固定）。
- 零分布必须做**基线表达分位匹配**；未匹配的零分布只能作为对照，不能作为推断依据。

## 已知陷阱（本项目实测）
- Welch t 在两组恒定时返回 NaN，BH 需先 `nan→1.0`。
- 秩必须按排序变量的实际顺序赋，不能按 DataFrame 行序。
- 分组标签大小写必须全链条统一（`sni` vs `SNI` 曾导致空臂 → p=0 假阳性）。
- `exact_perm_diff` 已加断言：空臂 / 非有限值直接抛错，不许静默返回。

## 复现顺序
layer0 → layer1_projection → layer1_diag → layer2_sample_scores → layer2_robustness → fig_layer2 → gate_consistency（须 23/23）→ gen_manifest（最后）。
