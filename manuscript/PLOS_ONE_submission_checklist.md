# PLOS ONE — 投稿前核查清单 (matrix-stiffness-neuropathic-pain, tag v1.0.0)

> 目标刊：PLOS ONE (Public Library of Science) · ISSN 1932-6203 · SCIE · JCR Q2 (Multidisciplinary Sciences) · 2025 JIF 2.8 · APC US$2,477
> 投稿入口（实测）：https://www.editorialmanager.com/pone/ （登录页自述 "PLOS One"）
> 切换原因：原 primary GigaScience 于 2025 年发生编委会危机（>60% 编委辞职，含创始主编）且 IF 从 11.8 暴跌至 3.9（−67%）。PLOS ONE 稳定、SCIE、soundness-only 且明确欢迎阴性/零结果/再分析，与本稿最契合。

## P0 — 投稿前必须完成

1. **摘要格式与字数** —— PLOS ONE 要求**非结构化**摘要且 ≤300 词。原稿为结构化（Background/Methods/Results/Conclusions）且 319 词。
   ✅ 已改为非结构化并压至 **298 词**（manuscript.md）；所有关键数字与引用保留（CTGF +1.64 / 9.5×10⁻⁶；阳性对照 +1.285 / 0.0286 / g=3.85；MRU 0.717/0.102/0.409；有界零 g=0.219；特异性指数 0.44–240.5；G1/G5 q=0.0010/0.0016）。
2. **Cover letter** —— 已改投 PLOS ONE / Public Library of Science，强调 soundness-only 契合、欢迎阴性/零结果/再分析，署名 Yongxin Yang, B.M.。
   ✅ manuscript/cover_letter.md + cover_letter.docx 已重生成。
3. **期刊政策声明**（须在 manuscript.md 中显式出现，投稿表单亦须勾选）：
   - 伦理/IRB：本研究仅使用去标识化公共数据（GSE98547/111216/261676），未纳入新的人体/动物受试者，无需 IRB/伦理审批。→ 确认 manuscript.md 已有此声明。
   - 利益冲突：The author declares no competing interests.
   - 基金：The author received no specific funding for this work.
   - 作者贡献（CRediT）：单作者，全部角色（Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Software, Validation, Visualization, Writing – original draft, Writing – review & editing: Yongxin Yang）。
4. **数据与代码可用性** —— PLOS ONE 要求 Data Availability Statement。当前：GitHub 仓库 + tag v1.0.0 + 带校验和 MANIFEST，且文中列明 GEO 登录号。
   ✅ 确认 manuscript.md 数据可用性段落写明仓库 URL、tag、MANIFEST，以及三个 GSE 编号。

## P1 — 应处理 / 核对

5. **报告指南（Reporting guidelines）** —— PLOS ONE 可能要求 EQUATOR 清单。本稿为公共数据再分析，无适用的主要临床/动物指南；前瞻性协议（PROTOCOL_*.md，冻结）即预注册，建议在 Methods 或 cover letter 中点明。
6. **图件文件** —— PLOS ONE 要求独立高分辨率图件（TIFF/PDF/EPS，≥300 dpi，宽 ≥1000 px）。当前图仅以 PNG 内嵌 docx。投稿前须从 `analysis/results/*/fig/` 提取 6 主图 + 1 辅图为合规格式至 `manuscript/figures/`。
7. **参考文献** —— PLOS ONE 用 Vancouver（编号）✅ 已采用；须确保所有 10 条均有 DOI/PMID 且格式正确（PLOS ONE 偏好 DOI）。
8. **标题与署名** —— 标题与 manuscript.md 一致；署名 "Yongxin Yang, B.M."（无 MD/PhD）、单位、ORCID 正确 ✅。
9. **摘要字数复核** —— 最终定稿后再次确认 ≤300（regen 后重数）。

## P2 — 投稿时操作

10. 上传：cover letter、manuscript（docx + md）、图件、补充文件、MANIFEST、notes。
11. 填写 PLOS ONE 网页投稿清单（伦理、利益冲突、基金、数据/代码可用性、作者贡献）。
12. APC：US$2,477（投稿时以官网为准）。

## 决策背景（留痕）

- 自 GigaScience（primary 至 2026-10-21）切换，因 2025 编委会危机（>60% 辞职，含创始主编）与 IF 暴跌 11.8→3.9（−67%）。
- PLOS ONE 选定理由：SCIE、Q2、稳定无危机、soundness-only、明确欢迎阴性/零结果/再分析 —— 最契合本"诚实优先"方法学稿。
- 配置 `ms_panel.json` 中原 "PLOS ONE excluded" 是基于**另一篇 MR 稿**的内部拒稿，不适用于本方法学再分析稿（已在 `_note_plosone` 注明）。
