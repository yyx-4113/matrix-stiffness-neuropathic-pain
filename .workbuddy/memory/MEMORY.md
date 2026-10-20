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

## 已知陷阱（本项目实测，全部触发过）
- Welch t 在两组恒定时返回 NaN，BH 需先 `nan→1.0`。
- 秩必须按排序变量的实际顺序赋，不能按 DataFrame 行序。
- 分组标签大小写必须全链条统一（`sni` vs `SNI` 曾导致空臂 → p=0 假阳性）。
- `exact_perm_diff` 已加断言：空臂 / 非有限值直接抛错，不许静默返回。
- **biotype 过滤必须在 symbol 聚合之前**（locus 层），否则非编码 locus 的 FPKM 会被灌进编码基因；实测 37 个混合 biotype symbol、10 个被 any() 保留，保留者中位 40.6% 信号来自非编码 locus。
- **置换零分布必须无放回抽样**；`rng.integers(0,n,size=(n_iter,m))` 是有放回，实测 3.35% 抽样含重复基因，会缩小有效模块、加宽零分布。
- **Wilcoxon 秩和 z 的期望必须与秩基准一致**：0-based 秩（0…n−1）配 `mu=m*(n-1)/2`，不能用 1-based 的 `m*(n+1)/2`。

## 术语纪律（v0.4 R7，务必区分）
- `homology_mapping_rate`：签名成员经同源转换后能在**小鼠注释全集**中找到的比例（不受表达过滤影响）→ 缺失＝**映射失败** → <0.7 **触发主终点降级**。
- `coverage_rate`：签名成员在**目标表达矩阵经检测过滤后**仍保留的比例 → 缺失＝**功效/细胞类型限制** → <0.5 在 Limitations 声明，**不解释效应量**。
- 二者**不得合并报告**，也不得互相替代作治理判定。曾因合并导致 HD_up 被错误降级（实际同源映射 18/18＝1.000，0.611 是 coverage）。

## 三类对照的分工（缺一不可）
| 类型 | 目的 | 期望 |
|---|---|---|
| 阴性对照（BLD/BRN） | 组织特异性 | 不显著 |
| 匹配零分布（Q4） | 统计量校准 | 不显著 |
| **阳性对照（损伤特征基因集）** | **管线灵敏度** | **显著** |
前两者回答"显著是否可信"，第三者回答"**不显著是否可信**"。
阳性对照实测：diff=+1.285, P=0.0286, g=+4.431（完全分离）→ PASS。

## 复现顺序
layer0 → layer1_projection → layer1_diag → layer2_sample_scores → layer2_positive_control → layer2_robustness → fig_layer2 → gate_consistency → gen_manifest（最后）。
