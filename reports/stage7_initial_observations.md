# 阶段 7 首次真实迁移矩阵：初步观察（2026-10-22 03:26）

数据：`results/stage7/main/transfer_matrix.csv`（pilot200 复核标签，LLaDA 195 / Dream 178 可用样本，test 约 45–48 条/方向）。
这是首次真实矩阵的**观察笔记**；稳健性结论由稳定性重采样（`reports/main_project_stability.*`，1500 次）给出，此处不做结论。

## 1. 域内（source = target）

| 特征集 | 模型 | LR | MLP |
|---|---|---|---|
| entropy_raw | LLaDA | 0.8312 | 0.7483 |
| entropy_raw | Dream | 0.7683 | 0.7747 |
| relative_normalized | LLaDA | 0.8737 | 0.7491 |
| relative_normalized | Dream | 0.7694 | 0.7697 |

## 2. 跨模型

| 特征集 | 方向 | LR | MLP |
|---|---|---|---|
| entropy_raw | LLaDA → Dream | 0.7833 | 0.7603 |
| entropy_raw | Dream → LLaDA | **0.8635** | 0.5472 |
| relative_normalized | LLaDA → Dream | 0.7520 | 0.7218 |
| relative_normalized | Dream → LLaDA | **0.4060** | 0.4711 |

## 3. 需要解释的异常

1. **`relative_normalized + LR`：Dream → LLaDA = 0.4060**（低于随机），而同特征下 LLaDA → Dream = 0.7520、同方向下 entropy_raw = 0.8635。
   分层看：该方向 hotpotqa 层 n=20、positive=16，AUROC 只有 0.1406；triviaqa 层 n=28 为 0.5833。即异常主要由 hotpotqa 的 20 条小样本驱动。
   - 待办：稳定性重采样会给出该格在重采样下的分布与 `p(AUROC<0.5)`；若频繁出现低于随机，应检查标准化在跨模型时的方向性问题（源域 fit、目标域 score），并写进协议差异。
2. **`entropy_raw + MLP`：Dream → LLaDA = 0.5472** 同样接近随机，而 LR 同方向 0.8635——模型类别（LR vs MLP）在跨模型时的差异大于特征集差异。
3. 所有 test 层只有 18–48 条，CI 很宽（多数跨模型格的 95% CI 覆盖 0.5），**单次矩阵不能作为检测器优劣结论**；方案本身也只要求"是否出现稳定迁移缺口"。

## 4. 与主方案口径的一致性

- 只用 reviewed 标签（`human:ledstevenovo:rule-signoff`），未使用 test 调参；阈值来自源域 validation（`training_audit.json`）。
- 目标域监督参照（target-trained reference）与迁移代价在 `transfer_matrix.csv` 的 `transfer_cost_auroc` 列：
  - LLaDA → Dream 迁移代价约 +0.015 ~ +0.048（目标监督更高）；
  - Dream → LLaDA 在 `relative_normalized+LR` 上为 **0.4677**（迁移比目标监督低 0.47），与上面的异常一致。
