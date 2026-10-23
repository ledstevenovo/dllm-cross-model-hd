# 迁移不对称：方向存在，但不是"失效"

日期：2026-10-23。数据：2000 题主表（`results/pool2000/main/transfer_matrix.csv`，dataset=all）。

## 迁移代价 = 目标域监督（域内 AUROC） − 迁移 AUROC

| 方向 | 特征集 | 检测器 | 迁移 AUROC | 域内（目标） | **代价** |
|---|---|---|---:|---:|---:|
| LLaDA→Dream | entropy_raw | LR | 0.854 | 0.853 | **−0.000** |
| LLaDA→Dream | entropy_raw | MLP | 0.839 | 0.807 | **−0.032** |
| LLaDA→Dream | relative_normalized | LR | 0.865 | 0.871 | **+0.006** |
| LLaDA→Dream | relative_normalized | MLP | 0.739 | 0.794 | +0.055 |
| Dream→LLaDA | entropy_raw | LR | 0.671 | 0.799 | +0.128 |
| Dream→LLaDA | entropy_raw | MLP | 0.680 | 0.765 | +0.086 |
| Dream→LLaDA | relative_normalized | LR | 0.752 | 0.813 | +0.061 |
| Dream→LLaDA | relative_normalized | MLP | 0.600 | 0.773 | **+0.173** |

## 结论

1. **`LLaDA→Dream` 基本无代价**：两格甚至为负（迁移比域内略高），四格均值 +0.007。
   这与 pilot200 的定性一致，且扩池后更干净。
2. **`Dream→LLaDA` 有真实代价**：四格均值 +0.112，最差 `rel+MLP` +0.173。
   但**没有一格失效**——所有迁移 AUROC 的 CI 下界都 > 0.55（见主表）。
3. **所以"方向性"是真的，"缺口/失效"是错的**。准确的表述是：

> 从 LLaDA 迁移到 Dream 几乎无损；从 Dream 迁移到 LLaDA 有 0.06–0.17 的代价，
> 但仍显著优于随机（0.60–0.75）。

这与 pilot200 的旧表述（"Dream 源域方向性**缺口**，三个组合停在随机"）的区别是：
**代价存在，但没有断裂**。旧表述把"有代价"误读成了"不可迁移"。

## 为什么方向不对称

两个模型的轨迹统计量分布不同，而"从谁的分布出发"决定代价：

- **LLaDA → Dream**：LLaDA 的熵分布更宽（8B vs 7B、不同的 mask schedule），
  源域拟合的标准化器遇到较窄的目标分布时仍有区分度；
- **Dream → LLaDA**：源域方差较小，标准化后目标域的尾部被压缩，区分度下降。

这是分布形状不对称的**自然结果**，不是"Dream 的轨迹没有信息"——
`rel+LR` 迁移仍有 0.752，`ent+LR` 0.671，都显著高于 0.5。

## 与 pilot200 的对照

| 项 | pilot200 | 2000 题 |
|---|---|---|
| `LLaDA→Dream` 四格代价 | −0.02 ~ +0.05 | −0.03 ~ +0.06 |
| `Dream→LLaDA` 四格代价 | +0.02 ~ **+0.39** | +0.06 ~ **+0.17** |
| `Dream→LLaDA` 最差格 | `rel+LR` 0.494（随机） | `rel+MLP` 0.600（显著） |

扩池后最差格的代价从 0.39 缩到 0.17，且不再有格落在随机水平。
**"缺口"的量级本身就依赖样本量**，这也印证了 learning curve 的结论。
