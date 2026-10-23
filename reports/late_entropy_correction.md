# 修正：`late_entropy` 并不优于多维组合（撤回前一份报告）

日期：2026-10-23。前一份 `reports/late_entropy_finding.md` 的标题与结论**撤回**，保留本文作为更正记录。

## 原报告的说法

> 单特征 `late_entropy` 在 `Dream→LLaDA` 上 0.766，高于所有多维组合（`entropy_raw` 0.671、
> `relative_normalized` 0.752）。可部署结论：跨模型用揭示末期熵，不要堆特征。

## 为什么这是过度概括

我把"某一格最高"写成了"跨模型通用最优"。查四个方向的完整对照后：

| 方向 | `late_only` | `relative_normalized` | 胜者 | 差距 | CI 重叠？ |
|---|---:|---:|---|---:|---|
| Dream 域内 | 0.823 | **0.871** | 多维 | 0.048 | 基本不重叠 |
| LLaDA 域内 | 0.766 | **0.813** | 多维 | 0.047 | 部分重叠 |
| **Dream→LLaDA** | **0.766** | 0.752 | 单特征 | **0.014** | **几乎完全重叠** |
| LLaDA→Dream | 0.823 | **0.865** | 多维 | 0.043 | 部分重叠 |

`Dream→LLaDA` 上：`late_only` CI [0.72, 0.81]，`relative_normalized` CI [0.71, 0.80]。
这两个区间**几乎重合**，点估计差 0.014 完全在噪声范围内。

而在其余三个方向，多维组合**都**领先 0.04–0.05，且 CI 重叠更少。

## 更正后的结论

1. **`late_only` 与多维组合在 `Dream→LLaDA` 上不可区分**（差 0.014，CI 重叠）；
   它确实**高于 `entropy_raw`**（0.671，差 0.095，CI 不重叠）——这一点仍成立；
2. **在其余三个方向，多维组合一致更好**（0.04–0.05）；
3. 因此不能说"跨模型用末期熵、不要堆特征"。准确说法是：
   **`entropy_raw` 的六维组合在 `Dream→LLaDA` 上明显偏弱，换成更靠后的统计量能补上**——
   但补上之后，它与多维组合持平，并没有超越。

## 与 pilot200 的关系

pilot200 上 `late_only` 是 0.869，`entropy_raw` 0.830，看起来"单特征最强"。
扩池后 `late_only` 0.766、`entropy_raw` 0.671，差距反而**扩大**（0.095）。
所以"`late_only` 优于 `entropy_raw`"这条是稳的；不成立的是"优于所有组合"——
那个结论建立在 pilot200 上 `relative_normalized` 恰好崩到 0.494 的噪声值之上。

## 教训（与本项目主线一致）

这是同一种错误的小型复现：**把一格的点估计极值当成规律**。
pilot200 时 `relative_normalized` 是 0.494（第 0.1 百分位的噪声值），于是 `late_only` 的 0.869
显得鹤立鸡群；扩池后 `relative_normalized` 回到 0.752，`late_only` 的领先就缩到 0.014。

判断"特征 A 比 B 好"必须看**四个方向的一致性**，而不是单格最大值。

## 处理

- `reports/late_entropy_finding.md` 顶部加撤回声明，正文保留（作为错误记录）；
- `reports/pool2000_delivery.md` 中"唯一存活发现"一节改写；
- `reports/paper_draft.md` §3.5 与 §5.3 的相应表述收紧为"`late_only` 不劣于多维组合，
  且优于 `entropy_raw`"。
