# 扩散式语言模型的答案正确性检测：跨模型迁移、稳定性与复现（工作稿 v0.1）

> 状态：**工作稿**（2026-10-22）。所有数字来自本仓库可复算产物（见 §7 清单），无占位数据；
> 稳定性为双种子 300×2 次/格（合并 600），人工抽查与标签证据已完成（§4）。英文投稿版可在此稿基础上翻译并调整篇幅/引用。

## 摘要

我们用**仅推理期可获得**的轨迹统计量（掩码扩散过程的熵、揭示进度与时间结构，全部 CPU 可算），预测两个扩散式语言模型
（LLaDA-8B-Instruct、Dream-v0-Instruct-7B）在开放问答上的答案正确性，并检验该"正确性检测器"能否**跨模型迁移**。
在 pilot200（每模型 120/30/50 划分，BF16，gen_length=64、steps=64、block=64、温度 0）上：

- **域内**检测稳定可用：AUROC 0.70–0.89（LR/MLP × 两个特征集），全部 8 格在 300 次簇级重采样下 `P(AUROC>0.5)=0.98–1.00`；
- **跨模型迁移出现方向性缺口**：`LLaDA→Dream` 四组合全部稳定迁移（AUROC 0.75–0.82，重采样 `P(>0.5)≥0.94`）；
  而 `Dream→LLaDA` 仅 `entropy_raw+LR` 稳定迁移（0.838，`P(>0.7)=0.95`），其余三个组合停在随机水平
  （0.51–0.58，`P(>0.7)≤0.18`）——且**不是负迁移**；
- **缺口有机制解释**：`relative_normalized` 的失败来自**特征尺度/分位漂移**——仅用未标注的目标模型轨迹做逐特征单调对齐，
  `rel+LR Dream→LLaDA` 即从 0.494 恢复到 **0.850 [0.72,0.96]**（hotpotqa / triviaqa 两层分别 0.83 / 0.88，故非小样本效应）；
  `ent+MLP` 的失败与对齐无关（另有机制，开放问题）；
- 该结论在 **5 个随机种子**、**300×2 次簇级重采样**、**10000 次簇级置换检验**（p=1e-4）下一致。
- 标签质量有独立证据：第二 judge（LongCat-2.5-Preview，冻结提示词）与 reviewed 标签 **373/373 全覆盖一致率 0.957，Cohen's κ=0.896**。
- 另附两项复现：TRE 轨迹级指标在 800 题上 AUROC 0.783（CI 0.749–0.817，置换 p=1e-4）；DynHD 方法级复现 22/22 验收断言通过。

## 1. 研究问题

1. 扩散式 LM 的推理轨迹是否携带**与正确性相关的可观测量**？（域内检测）
2. 该信号是否**跨模型族迁移**，即在哪些"特征×检测器"组合上迁移成立、哪些失效？（迁移矩阵 + 稳定性）
3. 迁移失效是**方向性缺口**还是噪声？（稳定性/多种子/置换，以及缺口的分层结构）
4. 既有方法（TRE 轨迹指标、DynHD 检测器）能否在本仓库设定下复现？

## 2. 数据与协议

| 项 | 设定 |
|---|---|
| 题集 | pilot200：hotpotqa + triviaqa，按簇（question cluster）全局划分 **120 train / 30 validation / 50 test**（每模型） |
| 模型 | LLaDA-8B-Instruct（rev `08b83a6…`）、Dream-v0-Instruct-7B（rev `05334cb…`） |
| 采集 | BF16，`gen_length=64`、`requested_steps=64`、`block_size=64`、`temperature=0`，单题原子落盘 + 指纹 |
| 标签 | 规则签核 reviewed（`human:ledstevenovo:rule-signoff`）；format_failure 不计入指标。可用样本 LLaDA 195 / Dream 178（test 每方向 45–48） |
| 特征 | `entropy_raw`（6 维）与 `relative_normalized`（10 维：6 个归一化熵 + uncertainty + 揭示进度/比例） |
| 检测器 | LR 与 MLP（小网格）；**阈值/归一化/超参只在源域 train/validation 拟合**，test 绝不参与 |
| 统计 | bootstrap 1000（按 question_id 分组）；跨数据集分层报告；多种子 5 个；簇级重采样稳定性 300 次/格（第二种子并行复核）；簇级置换 10000 次 |
| 标签质量 | 第二 judge 全覆盖 373 题（冻结提示词 v3，LongCat-2.5-Preview，温度 0）：一致率 0.957、κ=0.896 |

## 3. 结果

### 3.1 域内检测（AUROC[95% CI]，dataset=all）

| 特征集 | 模型 | LR | MLP |
|---|---|---|---|
| entropy_raw | LLaDA | 0.848 [0.72,0.95] | 0.703 [0.55,0.85] |
| entropy_raw | Dream | 0.803 [0.60,0.97] | 0.803 [0.62,0.95] |
| relative_normalized | LLaDA | **0.887** [0.77,0.97] | 0.750 [0.60,0.88] |
| relative_normalized | Dream | 0.800 [0.59,0.97] | 0.782 [0.61,0.93] |

### 3.2 跨模型迁移矩阵与稳定性缺口

| 方向 | ent+LR | ent+MLP | rel+LR | rel+MLP |
|---|---|---|---|---|
| LLaDA → Dream | 0.820 ✅ | 0.756 ✅ | 0.779 ✅ | 0.732 ✅ |
| Dream → LLaDA | **0.838** ✅ | 0.579 ⚠️ | 0.494 ⚠️ | 0.502 ⚠️ |

- ✅ = 簇级重采样 300 次下 `P(>0.5)≥0.94` 且 `P(>0.7)≥0.72`；⚠️ = 停在随机（`P(>0.7)≤0.18`）。
- 迁移代价（目标域监督 − 迁移）：LLaDA→Dream 四格 ≤ +0.05（几乎无损）；Dream→LLaDA 除 ent+LR(+0.018) 外为
  +0.124 / **+0.393** / +0.248 —— 目标域监督显著更高，与缺口方向一致。
- **双种子重采样汇总（seed 20261021 + 20261023，每格 600 次）**：

| 跨模型格 | 均值 ± σ（600） | P(>0.5) s1/s2 | P(>0.7) s1/s2 |
|---|---|---|---|
| Dream→LLaDA ent+LR | **0.839 ± 0.077** | 1.00/1.00 | 0.95/0.96 |
| Dream→LLaDA ent+MLP | 0.557 ± 0.151 | 0.63/0.65 | 0.18/0.19 |
| Dream→LLaDA rel+LR | **0.507 ± 0.143** | 0.55/0.46 | 0.08/0.09 |
| Dream→LLaDA rel+MLP | 0.520 ± 0.153 | 0.50/0.53 | 0.14/0.13 |
| LLaDA→Dream ent+LR | 0.803 ± 0.087 | 1.00/1.00 | 0.88/0.86 |
| LLaDA→Dream ent+MLP | 0.773 ± 0.088 | 1.00/1.00 | 0.79/0.79 |
| LLaDA→Dream rel+LR | 0.785 ± 0.094 | 0.98/1.00 | 0.81/0.85 |
| LLaDA→Dream rel+MLP | 0.758 ± 0.125 | 0.94/0.96 | 0.72/0.78 |

  两个种子间最大 |Δ均值| = 0.014（均值 0.006）→ 结论与种子无关。
- **异常格的分层**：`rel+LR Dream→LLaDA`；600 次重采样 mean **0.507 ± 0.143**、`P(≤0.5)≈0.50`、单种子 5–95% 分位 0.30–0.76
  ⇒ 判决为"**无可检测迁移信号**"而非"负迁移"。分层：hotpotqa 层 n=20（**仅 4 个负例**）AUROC 0.141、triviaqa 层 n=28 AUROC 0.583
  —— 异常几乎完全由该小层驱动，属小样本噪声（该层也是上游数据缺陷的所在，见 §6）。

### 3.3 稳健性

- **多种子**（5 seeds）：跨模型 LR 格种子间 σ=0.000（逐样本确定性训练），MLP 格 σ≤0.047；缺口方向不随种子变化。
- **置换检验**（TRE，10000 次簇级）：tre / tre_effective / tre_length_normalized 均 p=1.0e-4（null mean≈0.500，p95≈0.535）。
- **重采样稳定性**：双种子各 300 次、每格合并 600 次（`reports/stability_two_seeds.json`），种子间最大 |Δ均值| 0.014；
  域内 8/8、LLaDA→Dream 4/4 稳定，Dream→LLaDA 仅 ent+LR 稳定（§3.2）。

### 3.4 特征重要性（LR，置换 20 次，dataset=all）

- `revealing_entropy` 在 LLaDA 源格上至关重要（置换剔除后 AUROC 下降 +0.44/+0.46；LOO 同向）；
- `relative_normalized` 下最重要者为 `reveal_progress_entropy_vocab_normalized`（LLaDA 域内 +0.046）与 `revealing_entropy_vocab_normalized`；
- Dream→LLaDA 的 `rel` 格无显著重要特征（最大置换降幅 +0.079 且方差大）——与"无信号"判决一致。

### 3.5 尺度对齐诊断：异常格的机制

对跨模型格做三种特征处理对照（`scripts/alignment_diagnostic.py`；后两种仅用**未标注**的目标域 train 轨迹，属诊断，不进入主表）：

| 格 | source-scale（冻结流水线） | target-scale（目标域 z-score） | **quantile-map（逐特征分位对齐）** |
|---|---|---|---|
| Dream→LLaDA rel+LR | 0.494 | 0.705 | **0.850 [0.72,0.96]** |
| Dream→LLaDA rel+MLP | 0.502 | 0.344 | **0.744 [0.61,0.87]** |
| Dream→LLaDA ent+LR | 0.830 | 0.879 | 0.852 [0.73,0.97] |
| Dream→LLaDA ent+MLP | 0.579 | 0.588 | 0.439 [0.31,0.59] |
| LLaDA→Dream rel+LR | 0.779 | 0.767 | 0.743 [0.54,0.90] |
| LLaDA→Dream rel+MLP | 0.732 | 0.673 | 0.675 [0.48,0.83] |
| LLaDA→Dream ent+LR | 0.820 | 0.810 | 0.719 [0.52,0.89] |
| LLaDA→Dream ent+MLP | 0.756 | 0.820 | 0.698 [0.52,0.86] |

- **异常格的信号其实存在**：`rel+LR Dream→LLaDA` 在分位对齐后 0.494 → **0.850**，且**两层都恢复**（hotpotqa n=20：0.141 → 0.828；triviaqa n=28：0.583 → 0.875）——不是小样本效应；
- `rel+MLP` 同方向也恢复（0.502 → 0.744），但 target-scale 反而更差（0.344）→ 失配主要是**分布形状/分位**而非单纯位置尺度；
- **`ent+MLP` 的失败与对齐无关**（0.579 → 0.439），属另一机制，留作开放问题；
- LLaDA→Dream（本就可迁移）不因对齐获益，说明该诊断不是"万能增益"。

### 3.6 TRE R1 复现（800 题：507 incorrect / 293 correct）

| 指标 | AUROC [95% CI] |
|---|---|
| `tre_length_normalized` | 0.8370 [0.807,0.863] |
| `time_hard_last_30`（=average 变体） | 0.8341 [0.805,0.863] |
| `revealing_entropy` | 0.8314 [0.801,0.859] |
| `tre_effective` | 0.8270 [0.797,0.855] |
| `tre`（主口径） | 0.7834 [0.749,0.817] |

29 个分数族、按答案类型/终止方式分层与校准诊断见 `reports/tre_repro/offline_analysis.json`；协议差异见 `protocol_diff.md`。

### 3.7 DynHD 方法级复现

- CPU 验收断言 **22/22** 通过；LLaDA test AUROC 0.8824（3 seeds）、Dream 0.8093；
- 共同测试集（n=44）：LLaDA 0.8757 / Dream 0.8180；
- 已记录 5 条偏差与 3 条限制（`reports/dynhd_reproduction_summary.md`）。

## 4. 标签质量证据（独立第二 judge + 人工抽查）

| 对比 | 覆盖 | 一致率 | Cohen's κ |
|---|---|---|---|
| 第二 judge vs 规则 · 主项目（主表所用） | 373/373 全覆盖 | 0.957 | 0.896 |
| 第二 judge vs 规则 · 主项目 | 100 抽样 | 0.960 | 0.908 |
| 第二 judge vs 规则 · DynHD | 100 抽样 | 0.970 | 0.933 |
| **人工复核 vs 规则**（分歧富集的 50 条） | 50 | **0.900** | 0.733 |
| **人工复核 vs judge**（同上） | 50 | **0.960** | 0.884 |

- 7 条规则×judge 分歧的裁决：**5 条站在 judge、2 条站在规则**；judge 的两次失利均由**上游参考答案缺陷**（§6）造成；
- 按分层抽样外推（200 行中全部分歧 7 条 + 一致层 43 条复核）：规则标签误差 ≈**2.5%** [1.1%, 5.7%]、judge ≈**1.0%** [0.3%, 3.6%]（以人工为参照）；富集样本的比率本身不能当总体错误率；
- judge 与规则的 incorrect 边际高度吻合（LLaDA 全覆盖 0.7282 = 0.7282）；
- 结论：**主表所用 reviewed 标签的可靠性已有独立、全覆盖的一致性证据**，分歧全部经人工逐条裁决。

## 5. 讨论

1. **迁移缺口是方向性的，不是全局的**：同一特征、同一检测器下，缺口只出现在 Dream 源域；LLaDA 源域几乎无损。
   这提示"检测器可迁移性"应作为**逐方向**结论报告，而非"跨模型迁移是否可行"的二元判断。§3.5 进一步表明，Dream 源域缺口里的两个组合
   可由**未标注目标轨迹的逐特征单调对齐**修复（0.494→0.850），即"不可迁移"与"预处理未对齐"是两回事。
2. **模型类别与特征集的交互**：Dream→LLaDA 中，熵特征的 LR 有效而 MLP 失效（0.838 vs 0.579），
   同时 `relative_normalized` 两类都失效——失效模式更像"该方向的可分性在特征空间中被压缩"而非"检测器容量不足"。
3. **标准化特征的跨模型风险（已证实）**：`relative_normalized` 依赖词表归一化熵与揭示比例；源域 fit 的标准化器遇到目标域的漂移分布时，
   跨模型评分失真——§3.5 的分位对齐诊断把 `rel+LR Dream→LLaDA` 从 0.494 恢复到 0.850，且两层皆然。**可部署含义**：仅凭目标模型的
   *未标注* 轨迹即可做逐特征单调对齐，把"缺口"变成"可通过对齐修复的预处理问题"；但主表仍报告冻结流水线（不做此对齐）的结果，避免把诊断步骤混入主结论。
4. **限制**：test 每方向仅 45–48 条（CI 宽）；hotpotqa 层小（n≈20，个别仅 4 个负例）；judge 提示词的严格度会影响分歧率；
   上游数据存在个别错误答案（§6）。**单次矩阵不作为检测器优劣结论**；本稿所有结论均以重采样分布为准。

## 6. 数据质量附录（可核查）

- `triviaqa__qw_4069`（"Who succeeded Prince Rainier of Monaco?"）：上游 TriviaQA `rc.nocontext/validation` 的
  `answer.value = "Prince Albert"` 及其 27 个别名全部指向 19 世纪 Prince Consort Albert（raw 行：`rc.nocontext_validation.parquet`
  row 3802/12995，`raw_id=qw_4069`）。模型答 "Prince Albert II"（正确）被 judge 依据该参考答案判为 incorrect。
  **结论：上游数据缺陷，已在证据页与抽查表标注；正式分析不受影响（规则标签判为 correct）。**
- 该题是 16 条 judge 分歧中唯一由参考答案引起的；其余分歧为人判读类（严格/宽松），已进入人工抽查流程。

## 7. 产物与复算

| 内容 | 文件 |
|---|---|
| 迁移矩阵（主/消融） | `results/stage7/{main,ablations}/`（manifest 含输入/代码哈希） |
| 多种子 / 重要性 / 稳定性 | `reports/main_project_{multiseed,importance,stability}.json(.csv)`（+`_seed2`） |
| TRE R1 | `reports/tre_repro/{offline_analysis,permutation_test,protocol_diff,reproduction_report}.*` |
| DynHD | `reports/dynhd_reproduction_summary.{md,json}` |
| 标签证据 | `reports/{main_label_consistency,main_label_consistency_full,dynhd_label_consistency,label_quality_evidence}.*` |
| 人工抽查 | `reports/label_spotcheck_sheet.{md,csv,_review50.csv}` |
| 复算入口 | `scripts/offline.py extract|evaluate`、`scripts/multiseed_transfer.py`、`scripts/feature_importance.py`、`scripts/stability_study.py`、`scripts/tre_repro/*`、`scripts/dynhd_repro/*` |
| 夜间一键 | `scripts/overnight_nogpu.sh`（12 步，断点续跑/降级/看门狗）+ `scripts/morning_digest.py` |

## 8. 后续工作

1. **扩池决策门（主方案 §8）**：条件已满足（标签可靠 + 稳定缺口），规模由统计精度与标签成本决定——
   建议每模型 800 题起（test≈200/方向，CI 宽度约减半），优先补 Dream 源域与 hotpotqa 层；
2. 人工抽查完成后，将"人工 vs 规则"一致率写入 §4；
3. TRE R2（题单/prompt 冻结 → 采集）与 DynHD 扩池；
4. 尺度对齐诊断实验：验证 `relative_normalized` 跨模型的分布漂移假设；
5. 英文投稿版整理（图表清单见 §3，全部可由 §7 脚本一键重算）。
