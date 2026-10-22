# 跨数据集轴（`--axis dataset`）：首次在真实数据上运行

日期：2026-10-22。产物：`reports/cross_dataset/transfer_matrix.csv`、`coverage.json`、`manifest.json`（bootstrap 1000，按 question_id 分组，seed 42）。

## 为什么之前没有

方案（`docs/VGPU_32GB_完整实验方案.md` §评估口径）要求"跨模型"与"跨数据集"分开报告，`scripts/offline.py` 也实现了 `--axis dataset`，但 `results/stage7/` 与论文稿一直只跑 `--axis model`。这是一次补跑，不改任何已冻结的主表。

## 结果（在每个 backbone 内部，源域与目标域是数据集）

`backbone` 固定，源/目标在 `hotpotqa` 与 `triviaqa` 之间迁移。对角线是域内。

| backbone | 特征集 | 检测器 | →hotpotqa（负例数） | →triviaqa（负例数） |
|---|---|---|---:|---:|
| Dream | entropy_raw | LR | 0.667 (3) | 0.829 (10) |
| Dream | entropy_raw | MLP | 0.822 (3) | 0.824 (10) |
| Dream | relative_normalized | LR | 0.667 (3) | 0.841 (10) |
| Dream | relative_normalized | MLP | 0.744 (3) | 0.838 (10) |
| LLaDA | entropy_raw | LR | 0.875 (4) | 0.885 (12) |
| LLaDA | entropy_raw | MLP | 0.812 (4) | **0.471 (12)** |
| LLaDA | relative_normalized | LR | 0.875 (4) | 0.896 (12) |
| LLaDA | relative_normalized | MLP | 0.891 (4) | **0.526 (12)** |

（表中每个格子对源域的两个方向取值几乎相同，故只列目标域；完整 32 行见 CSV。）

## 两个可报告的观察

1. **hotpotqa 的 test 层几乎没有负例**：Dream 18 条可用里只有 **3** 个负例，LLaDA 20 条里只有 **4** 个。任何以 hotpotqa 为目标的 AUROC（含迁移矩阵里 `Dream→LLaDA` 异常格所在的那一层）都建立在 3–4 个负例上，CI 宽度必然接近 [0,1]。这不是新结论，但它给"异常格由 hotpotqa 小层驱动"提供了第二份独立证据：**问题在目标层太小，不在特征本身**。
2. **MLP 对"目标域换了"这件事普遍脆弱，LR 不是**：LLaDA 内部跨数据集时，`ent+MLP` 与 `rel+MLP` 掉到 0.471 / 0.526（低于随机），而同一个 backbone、同一特征、同一个源域的 LR 是 0.885 / 0.896。这与主表里 `Dream→LLaDA` 的 MLP 格（0.579 / 0.502）形态一致。

第 2 点值得写进讨论：**"Dream 源域方向性缺口"里 MLP 的那一半，更像是 MLP 小样本 + 域偏移的普遍脆弱，而不是 Dream 特有的性质**；真正 Dream 特有的只剩 `rel+LR` 那一格，而它已被尺度对齐诊断解释（0.494 → 0.850，`reports/alignment_diagnostic.json`）。

## 限制（必须与结论一起写）

- 目标层 n=18–28，负例 3–12 个，**不足以**做检测器优劣比较；
- 跨数据集迁移在本设定里天然混杂了"数据集难度"（hotpotqa 需要多跳、triviaqa 是单跳事实）：源域与目标域的正类率差异很大（hotpotqa 层正类率 0.83–0.89，triviaqa 0.57–0.63）；
- 因此本轴只用于**解释**主表异常格的来源，不进入任何主结论。
