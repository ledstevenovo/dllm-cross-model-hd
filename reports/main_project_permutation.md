# 主项目迁移矩阵的簇级置换检验（新增证据）

日期：2026-10-22。产物：`reports/main_project_permutation.json`。脚本：`scripts/main_permutation.py`（`--permutations 10000 --seed 42`）。

## 为什么补

TRE 复现那边一直有置换零分布（p=1e-4），但主项目 16 格只有 bootstrap CI。CI 回答"重采样下这个数会怎么动"，置换回答"随机标签能不能凑出这么大的数"——两个问题不同。此前主表缺后者。

## 方法

- 用 `results/stage7/main/predictions.csv` 里**已拟合好的检测器**，score 固定不动；
- 只置换**目标测试集的标签**，以 question 簇为单位整簇搬动（与本项目其他所有重采样的单位一致）；
- 每格 10000 次，经验 p 单侧 = `(#{null ≥ observed}+1)/(permutations+1)`，下界 1e-4；
- 不重拟合：重拟合会把"信号不存在"和"拟合不稳"混在一起。

16 格**全部**满足"每个簇内标签一致"，因此全部使用簇级置换，没有回退到行级。

## 结果

| 源 → 目标 | 特征 | 检测器 | AUROC | 零分布 p95 | p |
|---|---|---|---:|---:|---:|
| Dream → Dream | entropy_raw | LR | 0.803 | 0.656 | 0.0005 |
| Dream → Dream | entropy_raw | MLP | 0.803 | 0.656 | 0.0007 |
| Dream → Dream | relative_normalized | LR | 0.800 | 0.661 | 0.0004 |
| Dream → Dream | relative_normalized | MLP | 0.782 | 0.644 | 0.0009 |
| LLaDA → LLaDA | entropy_raw | LR | 0.848 | 0.648 | **1e-4** |
| LLaDA → LLaDA | entropy_raw | MLP | 0.703 | 0.643 | 0.011 |
| LLaDA → LLaDA | relative_normalized | LR | 0.887 | 0.648 | **1e-4** |
| LLaDA → LLaDA | relative_normalized | MLP | 0.750 | 0.643 | 0.0022 |
| LLaDA → Dream | entropy_raw | LR | 0.820 | 0.659 | 0.0002 |
| LLaDA → Dream | entropy_raw | MLP | 0.756 | 0.615 | 0.0006 |
| LLaDA → Dream | relative_normalized | LR | 0.779 | 0.656 | 0.002 |
| LLaDA → Dream | relative_normalized | MLP | 0.731 | 0.661 | 0.009 |
| Dream → LLaDA | entropy_raw | LR | 0.830 | 0.645 | **1e-4** |
| Dream → LLaDA | entropy_raw | MLP | 0.579 | 0.648 | 0.19 |
| Dream → LLaDA | relative_normalized | LR | **0.494** | 0.645 | **0.53** |
| Dream → LLaDA | relative_normalized | MLP | 0.502 | 0.619 | 0.47 |

## 结论

1. **12 个格在随机标签下无法复现**（p ≤ 0.011），包括全部域内格与全部 `LLaDA→Dream` 格。这是主结论"域内与单向迁移确实存在信号"的第一份显著性证据。
2. **异常格 `rel+LR Dream→LLaDA` 的 p = 0.53**：观测值 0.494 落在零分布正中。它不是"微弱但真实的负迁移"，而是**与随机标签不可区分**——与稳定性重采样（mean 0.514、P(>0.5)=0.55）和尺度对齐诊断（对齐后 0.850）三者互相印证。
3. **`ent+MLP Dream→LLaDA` 的 p = 0.19**，同样不显著。这把"缺口"从"四个组合中三个失效"精确成"两个组合与随机无异"，而其中一个（`rel+LR`）已被机制解释。
4. 零分布 p95 集中在 0.62–0.66：在 n=45–48、负例 13–16 的规模下，随机标签本身就能做到 0.65 左右。**这正是为什么必须报 p 而不只报 CI**——0.579 这类数字单看 CI 会显得"接近显著"。

## 限制

- p 值下界 1e-4（10000 次），报告时写 "p < 1e-4" 而非 "p = 0"；
- 置换保持检测器不变，因此检验的是"这个 score 与标签的关联"，不是"这个特征集的信息量"；后者由消融实验回答；
- n 很小（目标 test 45–48），显著性只说明"不是噪声"，不说明效应量大小。
