# 阶段 7 迁移矩阵：初步观察（2026-10-22，04:35 校对版）

数据：`results/stage7/main/transfer_matrix.csv`（签核后代码 + reviewed 标签；seed 42，bootstrap 1000 按 question_id）。
可用样本：LLaDA 195 / Dream 178（reviewed，`human:ledstevenovo:rule-signoff`；format_failure 不计入）；test 每方向 45–48 条。

> 说明：本笔记的全部数字由当前 CSV 直接核对生成。早期草稿中的数字来自一次已被覆盖的运行，已废弃；以本文件与 CSV 为准。稳健性结论由稳定性重采样（`reports/main_project_stability.*`，每格 300 次，全 16 格完成）给出，见 §5。

## 1. 域内（source = target）

| 特征集 | 模型 | LR（95% CI） | MLP（95% CI） |
|---|---|---|---|
| entropy_raw | LLaDA | 0.848 [0.72,0.95] | 0.703 [0.55,0.85] |
| entropy_raw | Dream | 0.803 [0.60,0.97] | 0.803 [0.62,0.95] |
| relative_normalized | LLaDA | 0.887 [0.77,0.97] | 0.750 [0.60,0.88] |
| relative_normalized | Dream | 0.800 [0.59,0.97] | 0.782 [0.61,0.93] |

## 2. 跨模型

| 特征集 | 方向 | LR（95% CI） | MLP（95% CI） |
|---|---|---|---|
| entropy_raw | LLaDA → Dream | 0.820 [0.63,0.97] | 0.756 [0.60,0.90] |
| entropy_raw | Dream → LLaDA | 0.830 [0.69,0.94] | 0.579 [0.41,0.75] |
| relative_normalized | LLaDA → Dream | 0.779 [0.59,0.93] | 0.732 [0.54,0.88] |
| relative_normalized | Dream → LLaDA | **0.494 [0.30,0.70]** | 0.502 [0.37,0.65] |

## 3. 需要解释的异常

1. **`relative_normalized + LR`：Dream → LLaDA = 0.494**（≈随机；同特征 LLaDA → Dream = 0.779，同方向 entropy_raw + LR = 0.830）。
   分层（CIs 见 CSV）：hotpotqa 层 n=20、positive=16、negative=**4**，AUROC **0.141** [0.00,0.33]；triviaqa 层 n=28，AUROC 0.583。
   即在该特征下，异常几乎完全由 hotpotqa 仅 4 个负例的小层驱动；`transfer_cost_auroc` = +0.393（目标域监督比迁移高 0.39）。
   待办：稳定性重采样给出该格重采样分布与 `P(AUROC<0.5)`；若频繁稳定低于随机，应检查标准化在跨模型评分时的方向性问题（源域 fit / 目标域 score），并写入协议差异。
2. **`entropy_raw + MLP`：Dream → LLaDA = 0.579**（同方向 LR = 0.830，差 0.25）：模型类别的差异在该方向上大于特征集的差异；`relative_normalized + MLP` = 0.502 同样接近随机。LR 与 MLP 在 Dream→LLaDA 上的一致性缺口值得复核（两特征、两类模型共 4 格中 3 格接近随机，只有 entropy_raw+LR 例外）。
3. 所有 test 层只有 18–48 条，CI 很宽（跨模型多数格 95% CI 覆盖 0.5），**单次矩阵不能作为检测器优劣结论**；方案只要求回答"是否出现稳定迁移缺口"。

## 4. 与主方案口径的一致性

- 只用 reviewed 标签，未用 test 调参；阈值来自源域 validation（`training_audit.json`）；每方向 bootstrap 按 question_id 分组。
- 迁移代价（`transfer_cost_auroc` = 目标域监督 - 迁移）：
  | 方向 | ent+LR | ent+MLP | rel+LR | rel+MLP |
  |---|---|---|---|---|
  | LLaDA → Dream | -0.017 | +0.047 | +0.022 | +0.050 |
  | Dream → LLaDA | +0.018 | +0.124 | **+0.393** | +0.248 |
- LLaDA → Dream 四个组合的迁移代价均 ≤ 0.05（基本无损失）；Dream → LLaDA 除 entropy_raw+LR 外都明显更低，与上面异常一致。

## 5. 稳定性重采样：结论（2026-10-22 05:53 完成）

产物：`reports/main_project_stability.json` / `.csv`。配置：簇级重采样（question cluster，冻结 split 内），每格 **300** 次重复，8 个组合 × 2 目标 = 16 格全部完成（`stopped_early=false`，无 partial）；每组合独立确定性 RNG；比原计划的 800 次低（本机实测 1.4–1.6 s/次重拟合，800 次要 5+ 小时），但完整表格优于一半表格的高重复数。

**结论 1（异常格的判决）**：`relative_normalized + LR` Dream → LLaDA 在重采样下 **mean 0.514 ± 0.136，P(>0.5)=0.55，5–95% 分位 0.301–0.757**。即：
- 它**不是"稳定低于随机"**，而是**与随机无异**——该特征×模型组合在跨模型时**没有可检测的迁移信号**（同方向 entropy_raw+LR 为 0.838，P(>0.7)=0.95）；
- §3 中 hotpotqa 层的 0.141 由该层仅 4 个负例驱动，属小样本噪声，不作为"负迁移"证据。

**结论 2（Dream → LLaDA 的稳定迁移缺口）**：四个组合中只有 `entropy_raw + LR` 稳定迁移（0.838，P(>0.5)=1.00，P(>0.7)=0.95）；另外三个——`entropy_raw+MLP` 0.555（P(>0.7)=0.18）、`relative_normalized+LR` 0.514（0.08）、`relative_normalized+MLP` 0.514（0.14）——**在重采样下都不可靠**。这与"模型类别的差异大于特征集差异"的初判一致，并给出了量化阈值。

**结论 3（对照）**：`LLaDA → Dream` 四个组合全部稳定（P(>0.5) 0.94–1.00，P(>0.7) 0.72–0.88）；全部域内格 8/8 稳定（P(>0.5) 0.98–1.00，其中 LLaDA rel+LR = 0.874 ± 0.056）。

**对决策门的意义（主方案 §8）**：稳定的"迁移缺口"确实存在，但形态是 **Dream 源域的方向性缺失**（同一特征、同一方向，仅 entropy_raw+LR 有效），而非任何组合的负迁移。若要扩池，优先补 Dream 源域（尤其 hotpotqa 层）并保持两特征×两模型的完整网格。

注意：以上分位是重采样离散度，不是总体置信区间；阈值未在稳定性循环中重新调优。
