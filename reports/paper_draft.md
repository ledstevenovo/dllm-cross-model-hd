# 扩散式语言模型的答案正确性检测：跨模型迁移、稳定性与复现（工作稿 v0.3）

> 状态：**工作稿**（2026-10-23，v0.3）。所有数字来自本仓库可复算产物（见 §7 清单），无占位数据。
> **v0.3 相对 v0.2 的核心变化**：扩池到 2000 题/模型后，v0.2 的"Dream 源域方向性缺口"**未通过预注册判据**，
> 被判定为 pilot200（test 每方向 48 条）的抽样假象。v0.2 全文留档于 `reports/paper_draft_v0.2_pilot200.md`。
> 判决与证据见 `reports/pool2000_verdict.md`、`reports/pool2000_learning_curve.md`、
> `reports/pool2000_supplementary_checks.md`。

## 摘要

我们用**仅推理期可获得**的轨迹统计量（掩码扩散过程的熵、揭示进度与时间结构，全部 CPU 可算），预测两个扩散式语言模型
（LLaDA-8B-Instruct、Dream-v0-Instruct-7B）在开放问答上的答案正确性，并检验该"正确性检测器"能否**跨模型迁移**。
最终结论建立在 **2000 题/模型**（BF16，gen_length=64、steps=64、block=64、温度 0，两模型同设备采集）上：

- **域内**检测稳定可用：AUROC 0.77–0.87（LR/MLP × 两个特征集），8/8 格在 10000 次簇级置换检验下 p ≤ 1e-4；
- **跨模型迁移普遍成立但中度衰减**：16 格**全部** AUROC > 0.5（0.60–0.87），
  跨模型格（0.60–0.87）低于域内格（0.77–0.87），最弱为 `Dream→LLaDA rel+MLP` 0.600；
  **没有任何一格表现为失效或负迁移**，也没有方向性断裂；
- **v0.2 声称的"方向性缺口"是 48 题测试集的抽样假象**：同一检测器、同一特征，在 450–491 条测试样本上
  `rel+LR Dream→LLaDA` 为 **0.752 [0.70,0.80]**（pilot200 上曾为 0.494），`ent+LR` 为 **0.671 [0.62,0.72]**
  （曾为 0.830）。在 pilot200 的测试规模下做 2000 次重抽，真实值 0.75 的分布中 0.494 落在**第 0.1 百分位**——
  旧结论是抽到了极端尾部，不是机制；
- 因此 v0.2 中"尺度对齐修复异常格"的机制叙事**同时失效**：不做任何对齐该格已是 0.752，对齐后 0.764（几乎无变化）；
  且分位对齐在多个格上**反而变差**；
- **唯一经得起扩池检验的具体发现**：单特征 `late_entropy`（`late_only`）在 `Dream→LLaDA` 上 0.766，
  高于 6 维 `entropy_raw` 的 0.671 与 10 维 `relative_normalized` 的 0.752——加更多特征不一定更好；
- 该结论在 **5 个随机种子**、**簇级重采样（两种子）**、**10000 次簇级置换检验**（16/16 格 p ≤ 4e-4）下一致。
- 标签质量有独立证据：第二 judge 与 reviewed 标签全覆盖一致率 0.957（κ=0.896）；
  R2 的替代 judge（同模型、不同供应商）与 R1 judge 的一致性 0.990（κ=0.979）。
- 另附复现：TRE 轨迹级指标在 800 题上 AUROC 0.783（CI 0.749–0.817，置换 p=1e-4）；
  TRE R2（HotpotQA × LLaDA，800 题）另行报告；DynHD 方法级复现 22/22 验收断言通过。

> **方法学要点（本稿最重要的教训）**：v0.2 的结论同时通过了 bootstrap CI、双种子簇级重采样、簇级置换检验、
> 5 个随机种子，以及一个"机制解释"（尺度对齐）。这五项全部无法发现问题的真正来源——**测试集本身只有 48 条**。
> CI 宽是警告而不是结论；在固定样本上重采样测的是样本内变异，不是抽样误差；置换检验只说明"这 48 条不像有信号"。
> 唯一有效的检验是**换一批样本重测**。

## 1. 研究问题

1. 扩散式 LM 的推理轨迹是否携带**与正确性相关的可观测量**？（域内检测）
2. 该信号是否**跨模型族迁移**？（迁移矩阵；在哪些"特征×检测器"组合上成立、强度如何）
3. 迁移的强度差异是**结构性缺口**还是**估计噪声**？（预注册判据 + 扩池 + 学习曲线）
4. 既有方法（TRE 轨迹指标、DynHD 检测器）能否在本仓库设定下复现？

## 2. 数据与协议

| 项 | 设定 |
|---|---|
| 题集 | **pool2000：每模型 2000 题**（hotpotqa + triviaqa），按簇全局划分 **1200 train / 300 validation / 500 test**；pilot200 的 200 题为其中的子集且保持原 split。题单冻结见 `reports/expansion_pack_v2.md` |
| 模型 | LLaDA-8B-Instruct（rev `08b83a6…`）、Dream-v0-Instruct-7B（rev `05334cb…`） |
| 采集 | BF16，`gen_length=64`、`requested_steps=64`、`block_size=64`、`temperature=0`，单题原子落盘 + 指纹，`--verify-observer` 全通过；**两模型在同一台 4080 SUPER (sm_89) 上采集**（跨设备规则见 `reports/device_migration_5090.md` §4） |
| 标签 | 规则签核 reviewed（`human:ledstevenovo:rule-signoff`）；format_failure 不计入指标。可用 test 样本：LLaDA 491 / Dream 449 |
| 特征 | `entropy_raw`（6 维）与 `relative_normalized`（10 维：6 个归一化熵 + uncertainty + 揭示进度/比例）；消融覆盖全部 10 个特征集 |
| 检测器 | LR 与 MLP（小网格）；**阈值/归一化/超参只在源域 train/validation 拟合**，test 绝不参与 |
| 统计 | bootstrap 1000（按 question_id 分组）；跨数据集分层报告；多种子 5 个；簇级重采样稳定性 300 次/格 ×2 种子；簇级置换 10000 次 |
| 预注册判据 | 冻结于任何 2000 题结果出现之前（`docs/NOGPU_WORKPLAN.md` §2d）：`rel+LR Dream→LLaDA` CI 上界 <0.6 且 `ent+LR` CI 下界 >0.7 |
| 标签质量 | 第二 judge 全覆盖 373 题（冻结提示词 v3，LongCat-2.5-Preview，温度 0）：一致率 0.957、κ=0.896 |

## 3. 结果

全部数字来自 2000 题/模型（`results/pool2000/main/`，bootstrap 1000 按 question_id 分组）。

### 3.1 域内检测

| 特征集 | 模型 | LR（95% CI） | MLP（95% CI） |
|---|---|---|---|
| entropy_raw | LLaDA | 0.799 [0.76,0.84] | 0.765 [0.72,0.81] |
| entropy_raw | Dream | 0.853 [0.81,0.89] | 0.807 [0.76,0.85] |
| relative_normalized | LLaDA | 0.813 [0.77,0.85] | 0.773 [0.73,0.82] |
| relative_normalized | Dream | **0.871** [0.84,0.91] | 0.794 [0.75,0.84] |

域内 8/8 格稳定可用，区间宽度仅 0.05–0.08（pilot200 时为 0.19–0.38）。

### 3.2 跨模型迁移矩阵

| 方向 | ent+LR | ent+MLP | rel+LR | rel+MLP |
|---|---|---|---|---|
| LLaDA → Dream | 0.854 [0.82,0.89] | 0.839 [0.80,0.88] | 0.865 [0.83,0.90] | 0.739 [0.69,0.78] |
| Dream → LLaDA | 0.671 [0.62,0.72] | 0.680 [0.63,0.73] | **0.752** [0.70,0.80] | 0.600 [0.55,0.65] |

- **16/16 格 AUROC > 0.5**，且 16/16 格在 10000 次簇级置换检验下 **p ≤ 4e-4**（零分布 p95 ≈ 0.548）；
- **没有失效格，也没有方向性断裂**。跨模型格（0.60–0.87）整体低于域内格（0.77–0.87），呈**中度衰减**；
- 迁移代价（目标域监督 − 迁移）：`LLaDA→Dream` −0.02～+0.06；`Dream→LLaDA` +0.06～+0.21，最弱格为目标域监督明显更优，但仍显著高于随机；
- 跨数据集轴（同一 backbone 内 hotpotqa ↔ triviaqa，32 格）0.663–0.886，**无低于 0.5 的格**。

### 3.3 预注册判据：未复现，且推翻旧结论

判据冻结于任何 2000 题结果出现之前：

| 检查项 | 观测 | 阈值 | 结果 |
|---|---:|---:|---|
| `rel+LR Dream→LLaDA` CI 上界 < 0.6 | **0.798** | 0.6 | ❌ |
| `ent+LR Dream→LLaDA` CI 下界 > 0.7 | **0.620** | 0.7 | ❌ |

两条不仅未通过，方向还相反：旧"异常格"从 0.494 升至 **0.752**，旧"唯一稳定迁移格"从 0.830 降至 **0.671**。

**这不是 bug，有三条独立核对**：

1. 把 2000 题表**限制回 pilot200 的 200 题**，16 格逐位复现旧数字（0.494 / 0.830 / 0.803 / 0.579 …）；
2. 绕开本项目流水线，手写 `StandardScaler+LogisticRegression` 独立复算：0.7519（流水线 0.7519）；
3. 数据结构核对：2000 题 / 4000 行，1200-300-500，配对 test 集，无重复 sample_id、无跨 split 簇、标签全 reviewed。

**学习曲线给出机制**（`reports/pool2000_learning_curve.md`）：检测器只拟合一次、仅改评分子集，
`rel+LR` 从 n=96 起稳定在 0.71–0.77（全量 0.752），说明真实值一直是 ~0.75。在 n=48 下重抽 2000 次，
均值 0.750（sd 0.075），**pilot200 观测到的 0.494 落在第 0.1 百分位**；同样的程序把 `ent+LR` 的 0.830
放在以 0.669 为中心的分布的第 98.4 百分位。pilot200 从一个 48 点测试集里同时抽到一个极端低值和一个极端高值，
二者的反差成了 v0.2 的主线。

### 3.4 稳健性

- **多种子**（5 seeds）：LR 格种子间 σ=0.000（逐样本确定性训练），MLP 格 σ≤0.047；
- **簇级重采样**：两种子各 300 次/格；域内 8/8、`LLaDA→Dream` 4/4、`Dream→LLaDA` 4/4 全部 `P(>0.5)=1.00`；
- **置换检验**：16/16 格 p ≤ 4e-4（下界 1e-4），零分布 p95 = 0.548；
- **稳定性结论的性质**：以上三项在 v0.2 时也全部做过且全部"通过"，但都没能发现问题——它们测的是
  固定样本内的变异与随机标签，**不测抽样误差**。本稿因此把"换一批样本重测"列为必要检验（§3.3）。

### 3.5 特征集消融：单特征 `late_entropy` 最优

`Dream→LLaDA`，10 个特征集（LR / MLP）：

| 特征集 | 维度 | LR | MLP |
|---|---:|---:|---:|
| `early_only` | 1 | 0.702 | 0.660 |
| `middle_only` | 1 | 0.718 | 0.706 |
| **`late_only`** | **1** | **0.766** | **0.765** |
| `entropy_raw` | 6 | 0.671 | 0.680 |
| `entropy_confidence` | 7 | 0.682 | 0.655 |
| `absolute_time` | 9 | 0.700 | 0.594 |
| `relative_time` | 10 | 0.752 | 0.651 |
| `relative_normalized` | 10 | 0.752 | 0.600 |
| `with_stability` | 11 | 0.753 | 0.630 |

- **单特征 `late_entropy`（0.766）明显优于 6 维 `entropy_raw`（0.671，差 0.095，CI 不重叠）**，
  但与 10 维 `relative_normalized`（0.752）只差 0.014、CI 几乎完全重叠；
  且在 `LLaDA→Dream`（0.823 vs 0.865）与两个域内方向（0.823/0.766 vs 0.871/0.813）多维组合都更好。
  因此正确表述是「末期熵补上了 `entropy_raw` 的短板，但没有超越最优组合」；
- v0.2 曾报告"加入进度/长度特征会崩盘"（0.83 → 0.47），扩池后**整体反转**：含进度/长度特征的集合全部上升
  （+0.21～+0.29），纯熵类全部下降（−0.05～−0.16）。旧消融结论作废，见 `reports/pool2000_featureset_ablation.md`；
- 机制假设：进度类特征在 48 题上方差估计不稳，450 题后分布估计稳定，标准化便能吸收跨模型差异。

### 3.6 尺度对齐诊断：前提消失

| 格 | 原尺度 | 目标域标准化 | 分位对齐 |
|---|---:|---:|---:|
| `rel+LR Dream→LLaDA` | **0.752** | 0.751 | 0.764 |
| `rel+MLP Dream→LLaDA` | 0.600 | 0.601 | 0.726 |
| `ent+LR Dream→LLaDA` | 0.671 | 0.667 | 0.763 |
| `ent+MLP Dream→LLaDA` | 0.680 | 0.537 | 0.753 |
| `rel+MLP LLaDA→Dream` | 0.739 | 0.813 | **0.600** |
| `ent+MLP LLaDA→Dream` | 0.839 | 0.828 | **0.710** |

v0.2 的机制叙事建立在"对齐把 0.494 修复到 0.850"上。扩池后该格本就 0.752，对齐只到 0.764——
**没有问题需要修复**。且分位对齐在多个格上**反而变差**（`rel+MLP LLaDA→Dream` 0.739 → 0.600），
因为它用目标域 train 的分位重排目标域 test，样本充足后引入的扭曲超过其修正的漂移。
「尺度对齐是异常格的机制」这一结论撤回。

### 3.7 TRE 复现：三个格子（TriviaQA 双预算 + HotpotQA）

R1 主口径 TRIVIAQA × LLaDA（800 题，507 incorrect / 293 correct）：

| 指标 | AUROC [95% CI] |
|---|---|
| `tre_length_normalized` | 0.8370 [0.807,0.863] |
| `time_hard_last_30`（=average 变体） | 0.8341 [0.805,0.863] |
| `revealing_entropy` | 0.8314 [0.801,0.859] |
| `tre_effective` | 0.8270 [0.797,0.855] |
| `tre`（主口径） | 0.7834 [0.749,0.817] |

**双预算对照（同一 800 题、同一 judge）**：

| 预算 | 配置 | AUROC [95% CI] | AUPRC | 正类率 | 置换 p |
|---|---|---|---:|---:|---:|
| L128 | `L128/S64/B128` | **0.7834 [0.749,0.817]** | 0.8275 | 63.4% | 1e-4 |
| L64 | `L64/S64/B64` | **0.7016 [0.663,0.740]** | 0.7386 | 60.4% | 1e-4 |

预算减半使 AUROC 下降 **8.2 pp**。原文表 1 的 64 列（86.5）反而高于 128 列（82.2）；
我们两次运行都是**单块 64 步**，唯一差别是每步揭示 2 个还是 1 个 token，
即 TRE 求和的**位置数**不同。原文未公开 `gen_length`/`steps` 对应关系，"64"很可能指扩散步数
而非生成长度——**两种"64"不是同一个量**，不与原文 86.5 直接对照。详见 `reports/tre_repro/budget_columns.md`。

**Dream × TriviaQA（800 题，同题单同 seed）**：

| 指标 | AUROC [95% CI] | AUPRC |
|---|---|---|
| `tre`（主口径） | **0.7948 [0.763, 0.826]** | 0.8064 |
| `tre_effective` | 0.8703 [0.845, 0.894] | 0.8745 |

置换 p = 1e-4。原文 128 列 83.9 → 本次 79.48（**−4.4 pp**），与 LLaDA 的 −3.9 pp 高度一致。
协议差异必须同报：**BF16**（Dream + FP16 因 NaN 风险被硬拒）、judge 用 vankit 端点、
以及 **Dream 的回答极短**（有效长度中位 **3**、全部 EOS 终止、最大 37，LLaDA 中位 12）——
TRE 对全部生成位置求和，故两列原始分数不可直接比大小。

**四格汇总**：

| 模型 | 数据集 | 生成 | 本次 | 原文 | 差值 |
|---|---|---|---:|---:|---:|
| LLaDA | TriviaQA | 128 | 78.34 | 82.2 | **−3.9** |
| Dream | TriviaQA | 128 | 79.48 | 83.9 | **−4.4** |
| LLaDA | TriviaQA | 64 | 70.16 | 86.5 | −16.3 |
| LLaDA | HotpotQA | 128 | 68.18 | 85.6 | −17.4 |

全部 p = 1e-4。**协议匹配的两格（TriviaQA-128，两个模型）偏差仅 −3.9 / −4.4 pp**，
这是"偏差是系统性而非偶然"的证据；两格大偏差各有已查明的协议原因（见下与
`reports/tre_repro/four_cells.md`）。

**HotpotQA × LLaDA（800 题，R2）**：

| 指标 | AUROC [95% CI] | AUPRC |
|---|---|---|
| `tre`（主口径，原始 judge） | 0.6818 [0.627, 0.734] | 0.2198 |
| **`tre`（三方仲裁后，最终）** | **0.7059 [0.657, 0.758]** | — |
| `tre_effective` | 0.6683 [0.613, 0.726] | 0.2175 |

置换 p = 1e-4 → judge 口径下信号显著，但比原文 128 列（85.6）低 **17.4 pp**，远大于 TriviaQA 的 −3.9 pp。
**标签口径已用第三方仲裁解决**：规则签核在同一批 786 条上只给 0.542（两口径一致率 0.831），
因为 HotpotQA 的长回答使规则的两条前提失效（子串命中≠答对；精确匹配≠等价）。
用第三个 judge（LongCat-2.5-Preview，不同模型家族）裁决 142 条分歧：
**126/142（88.7%）支持 deepseek judge，仅 16 条支持规则**；采用仲裁标签后
**AUROC = 0.7059 [0.657, 0.758]**。所以 0.542 来自不适用的标注器，不是方法失效，
但 0.706 仍比原文低 **15.0 pp**。见 `reports/tre_repro/r2_adjudication_report.md`。
两个已实测的机制：(1) 正类率仅 **12.1%**（95/786）—— 有上下文时答案就在段落里，模型能抄；
(2) **46.6%** 的生成撞上 126 token 上限（模型复述段落而非简短作答），而 TRE 是对**全部**生成位置求和。
剔除截断样本后仍为 0.660，故截断是稀释而非主因。长答错误率 17.2% vs 短答 8.2%。
**未为接近 85.6 做任何事后调参**；改进路径（提高预算、改 prompt、换 fullwiki）列为未来工作。

29 个分数族、按答案类型/终止方式分层与校准诊断见 `reports/tre_repro/offline_analysis.json`；
R2 详见 `reports/tre_repro/r2_report.md`；协议差异见 `protocol_diff.md` 与 `r2_design_note.md`。

### 3.7b TRE 与训练检测器的同轨迹对比（本项目首次）

此前两条线从未在同一数据上比较过。TRE 的轨迹是 trace-v1 格式，可被主项目特征抽取器直接读取，
因此本次比较是精确的：同一批生成、同一批题目、同一批标签，只差打分规则。
训练检测器因题目全为 `split=test`，用 **question-cluster 5-fold 交叉验证**（防近重复泄漏）。

| Run | n | TRE（无训练） | `ent+LR` | `rel+LR` | `rel+MLP` | `late+LR` | 最好的检测器 |
|---|---:|---:|---:|---:|---:|---:|---:|
| LLaDA / TriviaQA | 800 | 0.783 | 0.813 | **0.848** | 0.809 | 0.779 | **0.848** |
| Dream / TriviaQA | 796 | 0.795 | 0.862 | **0.890** | 0.820 | 0.768 | **0.890** |
| LLaDA / HotpotQA | 786 | **0.706** | 0.677 | 0.680 | 0.625 | 0.468 | 0.680 |

**结论取决于数据集，两个方向都有信息**：

1. **两个 TriviaQA 上训练检测器明显更好**（+0.065 / +0.095，CI 不重叠）——
   10 个特征相对 1 个加权和，多出的信息是真的；
2. **HotpotQA 上反转，TRE 领先**（0.706 vs 0.680）——该数据集 47% 的生成在复述上下文，
   特征分布漂移，小样本训练的 10 维模型过拟合噪声；TRE 的单一加权和在漂移下更稳。
   这也重新解释了 R2 的低分：不是 TRE 变差，而是**训练检测器在这个数据集上更差**；
3. **`late_only` 三行全部落后**（HotpotQA 上 0.468，低于随机），再次否定"单特征最优"。

实践建议：**有标注且答案短 → 用训练检测器；无标注或分布漂移大 → 用 TRE**。

### 3.8 DynHD 方法级复现

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

1. **迁移普遍成立，只是有损**：16 格全部显著高于随机，没有失效格，也没有方向性断裂。跨模型格（0.60–0.87）整体低于
   域内格（0.77–0.87），这是"有损但可用"的迁移，而非"某些方向不可迁移"。检测器可迁移性因此应作为**连续的强度问题**
   报告，而不是"可行/不可行"的二元判断。
2. **最弱的组合是 MLP × 进度类特征**：`Dream→LLaDA rel+MLP` 0.600 为全表最低，但仍在 CI 下界 0.55 之上。
   同一方向的 LR 是 0.752——差距更像 MLP 在域偏移下的容量不匹配，而非特征本身不可用。
3. **末期熵补短板，但不超越最优组合**：`late_entropy` 一个量达到 0.766，明显高于 6 维 `entropy_raw`（0.671），
   但与 10 维 `relative_normalized`（0.752）持平（差 0.014，CI 重叠），且在另外三个方向都落后。
   可部署含义是**用靠后的轨迹统计量替换 `entropy_raw` 的早期/中期维度**，而不是"不要堆特征"。
   （本条曾写成"单特征胜过所有组合"，四方向核对后已收紧，见 `reports/late_entropy_correction.md`。）
4. **小样本能给多强的假信号（本稿最重要的方法学教训）**：v0.2 的"方向性缺口 + 尺度对齐机制"通过了 bootstrap CI、
   双种子簇级重采样（600 次/格）、簇级置换检验、5 个随机种子、以及一次独立的机制诊断。这些**全部**没能发现问题，
   因为问题不在估计的稳定性，而在测试集只有 48 条。48 题测试集在 2000 次重抽里能让真实值 0.75 的格子显示 0.494
   （第 0.1 百分位）。复现这类研究时，**换一批样本重测**应当与 CI 并列为必做项。
5. **限制**：test 每方向 449–491 条（区间宽度 0.05–0.10，仍不足以区分 0.02 量级差异）；hotpotqa 与 triviaqa 难度不同
   （正类率 0.57–0.89），跨数据集轴只用于解释、不作主结论；judge 提示词的严格度会影响分歧率；上游数据存在个别错误答案（§6）。
   本稿所有结论以簇级置换与 bootstrap 区间为准，不以单格点估计下判断。

## 6. 数据质量附录（可核查）

- `triviaqa__qw_4069`（"Who succeeded Prince Rainier of Monaco?"）：上游 TriviaQA `rc.nocontext/validation` 的
  `answer.value = "Prince Albert"` 及其 27 个别名全部指向 19 世纪 Prince Consort Albert（raw 行：`rc.nocontext_validation.parquet`
  row 3802/12995，`raw_id=qw_4069`）。模型答 "Prince Albert II"（正确）被 judge 依据该参考答案判为 incorrect。
  **结论：上游数据缺陷，已在证据页与抽查表标注；正式分析不受影响（规则标签判为 correct）。**
- 该题是 16 条 judge 分歧中唯一由参考答案引起的；其余分歧为人判读类（严格/宽松），已进入人工抽查流程。

## 7. 产物与复算

| 内容 | 文件 |
|---|---|
| **迁移矩阵（主表，2000 题）** | `results/pool2000/main/`（manifest 含输入/代码哈希）、`reports/pool2000_verdict.{md,json}` |
| **预注册判据与学习曲线** | `reports/pool2000_verdict.json`、`reports/pool2000_learning_curve{,_entropy}.json` + `.md` |
| **补充检验（置换/对齐/跨数据集）** | `reports/pool2000_{permutation,alignment_diagnostic}.json`、`reports/pool2000_supplementary_checks.md`、`results/pool2000/{strata,featuresets}/` |
| 扩池题单（冻结） | `data/manifests/pool2000_v1.json`、`reports/expansion_pack_v2.md` |
| pilot200 旧版（留档，已被 §3.3 推翻） | `results/stage7/{main,ablations}/`、`reports/paper_draft_v0.2_pilot200.md`、`reports/featureset_ablation.md`、`reports/main_project_{multiseed,importance,stability}.*` |
| TRE R1 | `reports/tre_repro/{offline_analysis,permutation_test,protocol_diff,reproduction_report}.*` |
| TRE R2（HotpotQA） | `data/tre_repro/questions/hotpotqa_eval800.jsonl`、`data/tre_repro/questions_manifest_r2.json`、`results/tre_repro/llada_hotpotqa_*` |
| DynHD | `reports/dynhd_reproduction_summary.{md,json}` |
| 标签证据 | `reports/{main_label_consistency,main_label_consistency_full,dynhd_label_consistency,label_quality_evidence}.*`、`reports/tre_repro/judge_crosscheck.json` |
| 人工抽查 | `reports/label_spotcheck_sheet.{md,csv,_review50.csv}` |
| 设备与跨设备一致性 | `reports/device_migration_5090.md`、`reports/device_consistency_pilot200.json` |
| 复算入口 | `scripts/offline.py extract|evaluate`、`scripts/pool2000_verdict.py`、`scripts/pool2000_learning_curve.py`、`scripts/main_permutation.py`、`scripts/alignment_diagnostic.py`、`scripts/{multiseed_transfer,feature_importance,stability_study}.py`、`scripts/tre_repro/*` |
| 夜间一键 | `scripts/run_overnight_gpu.sh`（17 步，断点续跑）+ `scripts/morning_digest.py` |

## 8. 后续工作

1. ~~扩池决策门~~ **已完成（2000 题/模型），结论为"未复现旧缺口"**；主表改用 2000 题；
2. **TRE R2（HotpotQA × LLaDA 800 题）**：题单与 prompt 已冻结（v4 上下文版），轨迹采集中；标签用同模型不同供应商的 judge，跨 judge 一致性 0.990/κ 0.979 已量化；
3. **TRE 第二个预算列**（L64）与 Dream 的 BF16 变体：已在 GPU 队列中；
4. **DynHD 扩池**（可选）：pilot200 的 test 仅 47/45，CI 宽；
5. **英文投稿版整理**：§3 表格全部可由 §7 脚本一键重算；
6. **方法学附录**：把 pilot200→pool2000 的这次反转写成"小样本假信号"案例（§3.3、§5.4），包含 bootstrap 不保护、重采样不保护、
   置换不保护的具体数字——这是本稿对复现研究最有借鉴价值的部分。
