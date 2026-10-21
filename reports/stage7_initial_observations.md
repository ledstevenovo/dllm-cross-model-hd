# 阶段 7 迁移矩阵：初步观察（2026-10-22，04:35 校对版）

数据：`results/stage7/main/transfer_matrix.csv`（签核后代码 + reviewed 标签；seed 42，bootstrap 1000 按 question_id）。
可用样本：LLaDA 195 / Dream 178（reviewed，`human:ledstevenovo:rule-signoff`；format_failure 不计入）；test 每方向 45–48 条。

> 说明：本笔记的全部数字由当前 CSV 直接核对生成。早期草稿中的数字来自一次已被覆盖的运行，已废弃；以本文件与 CSV 为准。稳健性结论由稳定性重采样（`reports/main_project_stability.*`，800 次）给出，见 §5。

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

## 5. 稳定性重采样（第 8 步，运行中）

- 产物：`reports/main_project_stability.json` / `.csv`；簇级重采样，每格 800 次重复，逐组合检查点续跑；整步设 3.5 小时硬上限（`--max-seconds`），若提前停止会在 JSON 中标记 `stopped_early` / `partial` / `missing_combos`。
- 本节的结论在完成后补入（预期清晨 07:10–07:50）。
