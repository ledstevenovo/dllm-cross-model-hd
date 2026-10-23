# 发现一个恒常特征：`revealed_fraction` 对所有正常样本恒等于 1

日期：2026-10-24 06:20。影响主项目全部特征集。

## 现象

对 3760 条 reviewed 样本做特征审计：

| 特征 | 唯一值数 | 最常见的值占比 | 标准差 |
|---|---:|---:|---:|
| **`revealed_fraction`** | **1** | **100.0%** | **0.000000** |
| 其余 19 个特征 | ≥2 | ≤99.9% | >0 |

唯一的例外是 1 条 `effective_length = 0` 的拒答样本（0/1 = 0），
它的值是 0 而不是 1，这不改变结论。

## 根因：定义上是冗余的

`src/trace_schema.py:100`：

```python
'revealed_fraction': float(r.sum() / safe_length)
```

其中 `r = arrays['revealed'][:, :length]`，即**有效长度窗口内**的揭示标记。

而"有效长度"的定义就是**生成结束前的位置数**——在这个窗口内，每个位置最终必然被揭示。
所以 `r.sum() == length` 恒成立，比值恒为 1。

**这不是 bug，是一个在设计上无法变化的量**：它测量的是"有效窗口内被揭示的比例"，
而有效窗口本身就由"已揭示到哪里"决定，构成循环定义。

## 影响

### 1. 它浪费了 `relative_normalized` 的一个维度

`relative_normalized` 是 10 维：6 个归一化熵 + `mean_uncertainty` + `mean_reveal_progress`
+ **`revealed_fraction`** + `reveal_progress_entropy_vocab_normalized`。

其中 1 维是常数。**实际有效维度是 9。**

这也部分解释了为什么 10 维的 `relative_normalized` 与 6 维的 `entropy_raw` 差距不大：
其中一维是死的，另有几维高度相关（见下）。

### 2. 不影响任何已发布结论

- 常数列在标准化后为 0（`StandardScaler` 对 `std=0` 的处理是 safe 的，sklearn 会把它设为 0）；
- LR/MLP 对常数列的系数为 0，预测不受影响；
- 所以所有 AUROC 数字**有效**，只是"10 维"这个说法高估了实际信息量。

### 3. 特征相关性也值得记录

与 `effective_length` 的相关系数（`relative_normalized`）：

| 特征 | r |
|---|---:|
| `mean_reveal_progress` | **−0.664** |
| `late_entropy_vocab_normalized` | −0.474 |
| `mean_uncertainty` | −0.399 |
| `mean_entropy_vocab_normalized` | −0.381 |
| `revealing_entropy_vocab_normalized` | −0.357 |
| `reveal_progress_entropy_vocab_normalized` | +0.008 |

**6 个特征与长度的相关性绝对值 > 0.25**，所以"检测器含长度信息"这一说法成立
（虽然不像我之前说的"含长度代理"那样直接）。

## 建议

| 项 | 建议 |
|---|---|
| 论文表述 | 把 `relative_normalized` 从"10 维"改为"10 维（其中 `revealed_fraction` 恒为常数，实际有效 9 维）" |
| 代码 | 保留该特征（删除会改变已冻结的产出），但在文档里标注无效 |
| 未来实验 | 若要提高特征效率，应删除 `revealed_fraction` 并检查 `mean_reveal_progress` 与长度的共线性 |

## 为什么这个发现重要

主项目的特征集是**预先冻结**的（`reports/expansion_pack_v2.md`），所以不能为这个发现去改特征。
但报告"10 维"时应当诚实说明其中一维是常数——这是复现研究应当披露的实现细节，
和"生成预算""judge 供应商"一样属于影响可解释性的元信息。

## 未做

- 未重算去掉 `revealed_fraction` 后的 AUROC（预期几乎不变，因为常数列无贡献）；
- 未做 `mean_reveal_progress` 与 `effective_length` 的共线性诊断（VIF 等）。
