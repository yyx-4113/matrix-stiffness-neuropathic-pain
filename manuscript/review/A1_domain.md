# A1 — Domain review: mechanobiology / pain neuroscience

**Role:** A1 Domain (biological & clinical validity)
**Manuscript:** `manuscript/manuscript.md` (treated as first submission)
**Read myself:** manuscript.md, PROTOCOL (§4, §5.3, §8.1, §10, §11.2 red lines, §12), layer0/layer1_diag/layer2_positive_control/layer3/layer3b/layer4 JSONs; recomputed CTGF Δ & P, HD_up/HD_down sizes, and all five Layer-3 SI values in python.

---

## 核心判断（先看这里）

本文最关键的生物学主张是「把 HEK293A（肾上皮）受控刚度诱导出的 Hippo 依赖性签名，投射到小鼠痛觉 DRG/脊髓，结果不转移」——并进一步**重定位**为「这是签名/细胞类型特异性的失败，而非投射方法的普遍失败；疼痛-ECM 文献未被证伪」。

我的结论：**重定位在方向上科学上站得住，但支撑它的关键证据（Layer-3 的 SI 比值）比我预期脆弱，且标题、措辞与结论之间存在一处硬性自相矛盾，必须修正。** 签名本身（Layer 0）生物学上是可信的。跨细胞类型投射的合理性只能算「部分成立」，文中未排除一个重要的竞争性解释。

---

## 【问题 1】标题与本文自己的结论自相矛盾（最严重，必须改）

【Problem】稿件标题断言「tissue specificity fails across five independent ECM and mechanotransduction gene sets」，但 Layer-3 的实际结果是 **4/5 保留了组织特异性**（仅 G2 失败），讨论与摘要也都正确重定位为「特异性被保留」——标题与正文结论相反。

【Evidence】标题：`manuscript.md:1`。Layer-3 实测：`layer3_generality.json` 的 `n_sets_failing_specificity = 1`，`primary_endpoint_pass = false`；per_set_specificity 中 G1/G3/G4/G5 的 `specificity_failed = false`，SI 分别为 38.4 / 1.44 / 240.5 / 9.06。这与标题"fails across five"直接冲突。标题沿用了协议 §11.1 的预 Layer-3 工作标题，重定位后未同步更新。

【Why it matters】这是编辑/审稿人会第一时间抓到的硬伤。一个与数据相反的结论性标题会立即让评审质疑全文的诚实度与一致性，即便正文正确也会被判为"作者没把控住稿件"。GigaScience 的编辑初筛很可能据此退稿。

【Specific fix】将标题改为与重定位一致，例如：
"*A stiffness-controlled Hippo signature does not transfer to neuropathic-pain transcriptomes: tissue specificity is retained by established ECM/mechanotransduction gene sets but lost by YAP/TAZ stiffness-response programs*"。同时把协议 §11.1 的工作标题同步修订（Round-1 评审若只审协议而不审稿件会漏掉此处不一致）。

---

## 【问题 2】特异性指数（SI）是比值统计量，对近零分母极度敏感，"4/5 保留特异性"的强度被夸大

【Problem】重定位结论"4/5 保留组织特异性"几乎完全依赖 SI = |MRU(DRG)−0.5| / |MRU(BLD)−0.5|；其中 G4 的 SI=240.5 与 G1 的 38.4 主要由**血液 MRU 接近 0.5（无偏移）**造成，而非 DRG 有强偏移，比值被极端放大。

【Evidence】`layer3_generality.json` per_set_specificity：G4 `MRU_target=0.7224`、`MRU_negative_blood=0.4991` → 分母 |0.4991−0.5|=0.0009，SI=240.5；G1 `MRU_blood=0.5106`（|shift|=0.0106），SI=38.4。重算（python）确认一致。相对地，DRG 的绝对偏移其实很小：G4=|0.222|、G1=|0.406|、G5=|0.386|，均在 [0,1] 量纲上的中等偏移。SI>1 仅说明"血液偏移 ≤ DRG 偏移"，并不等于"DRG 有强组织特异性激活"。

【Why it matters】"特异性保留"在方向上是对的（血液确实没动，DRG 动了），但把 SI=240.5 当作"强特异性"的证据会误导读者高估结论强度。若评审用稳健性眼光看，G4 的 SI 实际上是一个对血液近零偏移高度不稳定的比值，结论的根基比数字看起来要软。这与协议 §11.2 红线"不得报告超出证据的效应"相冲突——SI 量级不应被当作效应量呈现。

【Specific fix】在 Table 3 同时列出 `|MRU(DRG)−0.5|` 与 `|MRU(BLD)−0.5|` 两个绝对值（已部分可得），并明确声明"SI 为比值统计量，当对照组织偏移接近 0 时数值不稳定，故 SI 仅用于判定 SI<1（失败），不可读作特异性强度"。更稳健的做法是改用"DRG 与血液是否各自通过匹配零分布（P_BH<0.05）且 DRG 偏移更大"来定义特异性，而非单看比值。

---

## 【问题 3】"保守的机械核心（conserved mechanical core）"措辞高估了 HD_up 的机制同质性

【Problem】摘要与讨论把 HD_up（n=18）整体称为"受控体外程序"乃至"保守的机械核心"，但 18 个成员中只有 4 个是经典 YAP/TAZ 靶基因（CTGF、CYR61、ANKRD1、AMOTL2），其余 14 个（KRT8、KRT18、VIPR1、MTFMT、PPP2R2B、UBE2QL1、ADAP1、AJUBA、CNN2、EMILIN2、GPRC5A、AP1M2、HIST1H4D、SMAD7）是异质混合，并非都已确立为机械转导核心。

【Evidence】`layer0_signature.json` 的 `sets.hippo_dependent_up`（18 个）与 `canonical_yap_taz_targets_sensitivity_S4`（8 个候选中 6 个通过过滤：CTGF/CYR61/ANKRD1/AMOTL2/THBS1/CRIM1，其中 THBS1、CRIM1 在 WT 中未达 stiffness_up）。Layer 0 文字锚点只列了 4 个经典靶（manuscript.md:54）。协议 §2.1 已说明 HEK293A 提供的是"保守的跨细胞类型力学响应核心"而非"神经元力学传感"——但稿件正文把"核心"一词用在了 18 基因全集上。

【Why it matters】"保守机械核心"暗示整组基因在多种细胞类型中以相同方式被力学输入驱动。实际上只有 CTGF/CYR61/ANKRD1/AMOTL2 这一小簇是公认且被本文数据证实（CTGF Δ=+1.64, P=9.5e-6）的 YAP/TAZ 输出；其余成员的跨细胞类型保守性并无证据。这是一处机制过度宣称，触及 §11.2 红线精神。

【Specific fix】将"conserved mechanical core"限定为"a Hippo/YAP–TAZ-dependent stiffness-response program whose canonical markers (CTGF, CYR61, ANKRD1, AMOTL2) are established, mechano-responsive transcripts"，并明确 18 基因集中只有这 4 个属于经典核心；或补充一个仅用这 4 个基因的敏感性分析（协议 §4.5 S4 已预指定）以增强"核心"主张。

---

## 【问题 4】跨细胞类型投射的生物学合理性只部分成立，且文中未阐明"力学输入不匹配"这一竞争性解释

【Problem】HEK293A（肾上皮，2D 纤连蛋白水凝胶 1 vs 40 kPa）→ 小鼠痛觉 DRG/脊髓的投射，其"保守性"假设只得到 YAP/TAZ 通路层面支持，但两组实验的**力学输入本质不同**，而稿件把失败几乎完全归因于"细胞类型不同"。

【Evidence】签名来源为 GSE98547（manuscript.md:31），刺激是基底（纤连蛋白）刚度。痛觉 DRG 在 SNI 模型下的力学环境是神经压迫、神经周围纤维化、胶质瘢痕等，并非"基底刚度"。讨论（manuscript.md:87）写道"HEK293A epithelium ≠ sensory neuron/glia"，这只是一个解释方向；另一个同等重要的方向——"DRG 中根本不存在与基底刚度对应的力学输入因而不会运行该程序"——被略过。

【Why it matters】若失败的主因是"输入不匹配"而非"细胞类型机制不通"，那么"细胞类型特异性失败"的结论就偏窄：它实际上同时是"刺激-情境特异性失败"。这影响读者对"哪些后续实验能挽救该签名"的判断（应能验证：在 DRG 施加真正相关的力学输入，而非简单换细胞类型）。不澄清会让重定位结论的解释空间被错误收窄。

【Specific fix】在 Discussion 的局限性或核心结论处补一句："The null could reflect either that DRG neurons/glia do not engage this Hippo program, or—equally—that substrate (fibronectin) stiffness, the input that defined the signature in HEK293A, is not the relevant mechanical cue in the injured DRG; both interpretations are consistent with a cell-type/signature-specific failure rather than a universal method failure." 这既诚实又不影响重定位。

---

## 【问题 5】"疼痛-ECM 文献未被证伪"的辩护成立，但被标题/信息所削弱

【Problem】稿件主张 null 并未推翻 Parisien 2019 等的"疼痛中 ECM 富集"结论，只把其解释限定到"被投射签名的来源细胞类型"——这一捍卫在科学上是**可辩护的**，但稿件自身的标题（见问题 1）和摘要的"do not transfer"措辞在读者感知上恰恰在暗示广泛失败，与这一捍卫自相矛盾。

【Evidence】讨论（manuscript.md:87）"our null thus circumscribes the literature's 'ECM enrichment in pain' claims to the source cell type of the projected signature, without disproving them"；Layer 3 中 G1（核心基质组）与 G5（ECM 重塑/纤维化）在 DRG 的 MRU 高达 0.886/0.906 且 BH 显著（layer3_generality.json table，G1 DRG SNI q=0.0010、G5 DRG SNI q=0.0016），与 Parisien 2019 方向一致——这本身支持"未被证伪"。

【Why it matters】"未被证伪"的辩护是本文最有价值也最易被接受的观点，但若标题仍写着"tissue specificity fails across five sets"，评审会认为作者言行不一：一边说没推翻文献，一边用标题说文献所依赖的特异性失效。修正问题 1 的标题后，这一辩护才能干净落地。

【Specific fix】保留"circumscribes, not disproves"的论述（它本身正确且重要），但确保标题、摘要结论句与之一致（见问题 1 的替换标题）。可在 Discussion 明确列出"G1/G5 在 DRG 的强偏移正是 Parisien 2019 结论在本分析中的独立印证"。

---

## 【问题 6】重定位出的"结构性 ECM（G1/G5）成功、YAP/TAZ 响应（G2/HD_up）失败"是一个 post hoc 新主张，必须作为假设生成，且最好补引文献

【Problem】"ECM 结构重塑程序与 YAP/TAZ 刚度响应程序在疼痛转录组中分离"是 Layer-3 主终点 FAIL 后的事后诊断（协议 §9 v0.6 已自承为 post hoc），稿件已标为 hypothesis-generating，这很好；但该分离主张恰好坐落于"YAP/TAZ 在感觉神经元/DRG 中的机械转导"这一细分领域，稿件却未引用任何直接相关的 DRG/YAP–TAZ 文献来支撑或对照这一说法。

【Evidence】Discussion（manuscript.md:87）提出分离；引用的 YAP/TAZ 文献只有 Dupont 2011（#4，通用机制）与 Zhao 2008（#9，TEAD），均为细胞系/通用层面，无 DRG/感觉神经元层面的直接证据。G3 的引用 Coste 2010（#6，Piezo1/2 机械门控阳离子通道）作为"mechanosensing adhesome"的来源也属较松的对应（Piezo 是通道而非黏附体）。

【Why it matters】一个真正新颖的分离主张若无领域文献对照，评审会质疑其新颖性是否真的新、以及作者是否忽略了已有相反证据。补引该细分领域文献既是 §11.3"每条须经在线核实"的要求，也能把 post hoc 观察放到正确语境。

【Specific fix】新增 1–2 条关于 (a) YAP/TAZ 在感觉神经元/DRG 中机械转导或神经损伤后作用、(b) 神经病理性痛中 ECM 僵硬化/神经周围纤维化的文献（如存在），并在引用 G3 时确认 Coste 2010 是否确为该 adhesome 集的来源，否则替换为更贴切的来源。若作者检索后确认该细分领域无直接文献，应在文中明确写出"we found no direct study of YAP/TAZ mechanotransduction in DRG to contrast our分离 claim"，这同样满足诚实性。

---

## 【问题 7】LATS 确认（79.7% HD vs 28.6% HI）作为生物学锚点，方法学不透明

【Problem】Layer 0 用"LATS1/2-dKO 对 HD/HI 基因 YAP/TAZ 依赖性的方向确认比例"来论证 HD 分类捕获了真正的 Hippo 依赖，但稿件未说明"方向确认"的判定算法，读者无法独立判断 79.7% 这一数字的含义。

【Evidence】manuscript.md:54 "LATS confirmation was 79.7% for HD versus 28.6% for HI genes"；`layer0_signature.json` 仅给 `lats_confirmation_fraction = {hippo_dependent: 0.7966, hippo_independent: 0.2857}`。我重算确认这两个数（79.7% / 28.6%）与文件一致，但文件未给出计算所用的 LATS Δ 阈值与"方向确认"定义，故该锚点的可重复性我无法独立重建。

【Why it matters】这是签名生物学可信度的两大支柱之一（另一为 CTGF 锚点）。CTGF 锚点我已用原始输入独立重算（Δ=+1.64, P=9.5e-6，精确匹配），而 LATS 确认因方法不透明只能"接受文件值"。若评审追问，作者需能出示 LATS 计算脚本与阈值。

【Specific fix】在 Methods（Layer 0）补 1–2 句：LATS 确认定义为"在 LATS1/2-dKO 中，|Δ_LATS| ≤ 0.5·|Δ_WT| 且方向与 WT 一致（或 Δ_LATS≈0 视为抹平确认）的基因占比"，并注明所用阈值与 CTGF 锚点同源。

---

## § Stands up（我原以为会有问题、但核查后认为正确）

1. **CTGF 生物学锚点真实且强**：python 重算 `layer0_signature.json` 得 CTGF `delta_WT=1.6405`、`p_WT=9.49e-6`，与稿件 +1.64 / 9.5e-6 精确一致；CYR61/ANKRD1/AMOTL2 同向且显著。签名来源确实被刚度驱动，Layer 0 成立。

2. **§5.3 "uninformative not negative" 判定正确**：`layer1_diag.json` 中 HD_up×DRG×SNI 匹配后 P=0.102、q=0.409；HD_up×BLD×SNI 匹配后 P=0.100、q=0.409——**血液与靶组织 q 完全相等（均 0.409）**，触发 §5.3"阴性对照与主终点同等显著则不得做组织特异性归因"。判定成立，且我确认其基于的是预指定的匹配零分布（非未分层口径）。

3. **Stage B 有界 null 与灵敏度对照可信**：`layer2_positive_control.json` 阳性对照 diff=+1.285、P=0.0286、g=3.85；HD_up diff=+0.146、P=0.80、g=0.219——二者走同一管线，17.6 倍 g 差确实把 HD_up 的 null 定性为"有界"而非"灵敏度不足"。阳性对照与签名交集为 0（协议 §10.6 已固化检查），无循环论证。

4. **Layer 3 "8/40 BH 显著、全在 DRG/SC/BRN、血液 0" 成立**：从 `layer3_generality.json` table 逐行核对 q_BH40<0.05，确为 8 项（G1×4、G4×2、G5×2），且血液组织 0 项，与稿件完全一致。

5. **HD_down 与 Layer-3b/Layer-4 均按要求标为假设生成/FAIL**：HD_down 仅标 hypothesis-generating（manuscript.md:64）；Layer-3b verdict=FAIL（0/5 ECM 显著上调）、Layer-4 verdict=FAIL（8/15345 上调、ECM 并集 0），均未越出 §11.2 红线把 null 升级为发现。治理纪律被遵守。

6. **参考文献标识真实**：我经 DOI 解析核对了 #3（Serafini, Neurobiol Pain 2024;15:100153，标题与期刊一致）与 #10（Guan, Genes 2023;14(2):272，标题/期刊/DOI 一致）；#1 Meng 2018 与 #4 Dupont 2011 的归属已按协议 R11 正确分离（GSE98547→Meng，Dupont 仅作背景），无早期"把 GSE98547 错归 Dupont"的残留错误。其余 #2/#5/#6/#7/#8/#9 为标准可引用文献，标识一致。未发现伪造或错位 PMID/DOI。

---

## § Questions for the authors

1. HD_up 在 DRG 的 Layer-3 投影里 MRU(DRG,SNI)=0.618（上移），只是血液 0.768 更大；严格说 HD_up/G2 在 DRG **也有**上移信号，只是无特异性。正文"does not transfer"是否略强于数据？能否改成"transfers without tissue specificity"？
2. G4 的 SI=240.5 几乎全由血液 MRU=0.499 驱动（见问题 2）。若改用"DRG 与血液各自是否通过匹配零分布且 DRG 更强"来定义特异性，G4 是否还成立？请附稳健性。
3. 跨细胞类型投射的失败，作者倾向于"细胞类型机制不通"；是否考虑过"力学输入不匹配（基底纤连蛋白刚度 vs 神经压迫/纤维化）"这一竞争性解释（问题 4）？是否有计划在真正相关的力学输入下验证？
4. "结构性 ECM 与 YAP/TAZ 刚度响应在疼痛中分离"这一 post hoc 主张，作者是否检索过 DRG/YAP–TAZ 或疼痛-ECM 僵硬化文献？若检索无果，是否愿意在文中显式声明"未见直接对照文献"？
5. Layer 0 的 LATS 确认阈值与"方向确认"定义能否在 Methods 中给出（问题 7），以便评审复算？

---

## § What I actually checked

**读取文件**
- `manuscript/manuscript.md`（全篇）、`PROTOCOL_基质刚度与神经病理性痛.md`（重点 §4, §5.3, §8.1, §9, §10, §11.2, §12）。
- JSON：`layer0/layer0_signature.json`、`layer1/layer1_diag.json`、`layer2/layer2_positive_control.json`、`layer3/layer3_generality.json`、`layer3/layer3b_sample_generality.json`、`layer4/layer4_positive_characterisation.json`。

**python 独立重算（结果对比稿件）**
- CTGF：Δ=+1.6405、P=9.49e-6 → 稿件 +1.64 / 9.5e-6 ✓。
- HD_up / HD_down 集合大小：数组长度 18 / 41，与 `set_sizes`（18/41）及稿件一致 ✓。
- LATS 确认：HD 0.7966（79.7%）、HI 0.2857（28.6%），与稿件一致 ✓（方法学见问题 7，未能独立重建判定算法）。
- Layer-3 SI 五集：G1=38.416、G2=0.440、G3=1.438、G4=240.472、G5=9.055，与稿件 38.4/0.44/1.44/240.5/9.06 全部一致 ✓；`n_sets_failing=1`、`primary_pass=false` ✓。
- Stage A 匹配口径：DRG×SNI P=0.1023/q=0.4092，BLD×SNI P=0.1004/q=0.4092 → BLD q = DRG q = 0.409，证实 §5.3"同等显著→uninformative"成立 ✓。
- Layer-3b 表与 Layer-4：HD_up diff=+0.146/P=0.80/g=0.219、阳性对照 +1.285/P=0.0286/g=3.85、0/5 ECM 显著、Layer-4 8/15345 上调且 ECM 并集 0 —— 均与稿件 Table 2/正文一致 ✓。

**与稿件不符/需注意的 discrepancies**
- 唯一硬性不一致：标题（manuscript.md:1）声称"tissue specificity fails across five sets"，与本文数据（4/5 保留）相反 → 问题 1。
- SI 量级（尤其 G4=240.5、G1=38.4）由对照近零偏移放大，不宜读作特异性强度 → 问题 2。
- 其余数值与稿件完全吻合，未发现数据造假或数值错位。

**未触及/无法独立验证项**
- 原始 GSE98547 FPKM 表与 GSE261676 counts 未在本轮读取（仅读产物 JSON）；CTGF 锚点是从产物中的 `delta_WT/p_WT` 复核，非从原始 FPKM 重新跑 Welch —— 但 JSON 值内部自洽且与稿件一致。
- LATS 确认的逐基因计算脚本未提供，故 79.7%/28.6% 接受文件值（见问题 7）。
