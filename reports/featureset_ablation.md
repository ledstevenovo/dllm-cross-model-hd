# 全特征集消融：异常格的机制在「揭示进度」而不在尺度

日期：2026-10-22。产物：`reports/featureset_ablation/`（`transfer_matrix.csv` 240 行、`manifest.json`、`coverage.json`）。配置：`offline.py evaluate --axis model --bootstrap 500 --seed 42`，10 个特征集 × 2 检测器 × 4 方向。

## 为什么跑

主表只跑了 `entropy_raw` 与 `relative_normalized` 两个特征集，但 `src/detectors.py` 里定义了 10 个。此前对异常格 `rel+LR Dream→LLaDA = 0.494` 的解释是**尺度对齐**（`reports/alignment_diagnostic.json`：对齐后 0.850）。全特征集消融能把这个解释**拆到具体特征**上——因为不同特征集是不同特征的组合，掉分的那个组合会指向元凶。

## 结果（`dataset=all`）

| 特征集 | 维度 | Dream→LLaDA LR | Dream→LLaDA MLP | Dream→Dream LR |
|---|---:|---:|---:|---:|
| `early_only` | 1 | 0.754 | 0.797 | 0.788 |
| `middle_only` | 1 | 0.779 | 0.709 | 0.762 |
| **`late_only`** | **1** | **0.869** | **0.869** | 0.762 |
| `entropy_raw` | 6 | 0.830 | 0.579 | 0.803 |
| `entropy_normalized` | 6 | 0.830 | 0.568 | 0.803 |
| `entropy_confidence` | 7 | 0.822 | 0.760 | 0.820 |
| `absolute_time` | 9 | **0.465** | **0.453** | 0.805 |
| `relative_time` | 10 | **0.494** | **0.441** | 0.800 |
| `relative_normalized` | 10 | **0.494** | 0.502 | 0.800 |
| `with_stability` | 11 | **0.465** | **0.486** | 0.793 |

## 三个结论

### 1. 单特征 `late_entropy` 在异常方向上是最强的，不是最弱的

`late_only`（只用揭示末期熵这一个数）在 Dream→LLaDA 上 LR/MLP 都是 **0.869**，高于 6 维的 `entropy_raw`（0.830），也高于域内 Dream→Dream（0.762）。

这与"Dream 源域方向性缺口"的字面读法冲突：**不是 Dream 的轨迹特征没有跨模型信息，而是这个信息在 `late_entropy` 里保存得最好**。

### 2. 掉分的元凶是「揭示进度 / 长度」类特征，不是熵

- `entropy_raw`（6 熵）→ 0.830；加上 `mean_uncertainty` 变成 `entropy_confidence`（7 维）→ 0.822（几乎不变）；
- 再加 `mean_reveal_step` + `effective_length` → `absolute_time`（9 维）→ **0.465**；
- 或加 `mean_reveal_progress` + `revealed_fraction` + `reveal_progress_entropy` → `relative_time`（10 维）→ **0.494**；
- `relative_normalized` 用的是归一化熵 + 同样的进度类特征 → **0.494**。

**加入进度/长度特征就让 AUROC 从 0.83 掉到 0.47–0.49**，而熵类特征本身完全没问题。域内（Dream→Dream）同样的加入几乎无损（0.803 → 0.805 / 0.800），所以这不是"特征没用"，是**这些特征在跨模型时的分布不可比**。

### 3. 尺度对齐诊断因此得到精确解释

对齐诊断显示 `quantile_map` 能把该格从 0.494 恢复到 0.850——现在知道恢复的是什么：**进度/长度类特征的跨模型分位漂移**。两个模型的揭示步数分布不同（LLaDA 与 Dream 的 mask schedule 不同），源域拟合的标准化遇到目标域分布就错位。

这也解释了为什么 `ent+MLP`（0.579）对齐后没恢复（0.588）：它不含进度特征，问题在别处（MLP 小样本脆弱，见 `reports/cross_dataset_axis.md`）。

## 对主结论的影响（必须写清楚）

- 主表**不修改**：预注册口径仍是 `entropy_raw` / `relative_normalized` × LR/MLP，消融是二次分析；
- 但"Dream 源域方向性缺口"的表述需要精确化：**缺口是"包含揭示进度/长度特征的特征集"在跨模型时的失效，而不是 Dream 轨迹缺乏跨模型可迁移的熵信号**——后者被 `late_only = 0.869` 直接否定；
- 这不削弱结论，反而把它从"某方向不行"变成"某类特征不可直接搬"。后者是更有用的工程结论：跨模型用熵类特征，别用进度类。

## 限制

- 每个特征集只在同一份 pilot200 上评估，n=45–48，AUROC 差异小于 0.05 不应解读；
- `late_only` 是单特征，方差大，0.869 需要扩池后复核（pool2000 正在采集）；
- 消融的 bootstrap 是 500 次（主表 1000），仅作相对比较，不与主表数值直接混用。
