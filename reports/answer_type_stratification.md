# 按题型分层：`comparison` 是检测最弱的题型（但样本不足以下定论）

日期：2026-10-24 05:50。主项目 2000 题（reviewed 标签）+ TRE 两格。

## 主项目：迁移矩阵按题型拆分

`relative_normalized + LR`，test 集：

| 方向 | 题型 | n | 正类率 | AUROC | 95% CI |
|---|---|---:|---:|---:|---|
| Dream→LLaDA | WikipediaEntity | 238 | 62.2% | **0.771** | — |
| Dream→LLaDA | bridge | 206 | 87.4% | 0.708 | — |
| Dream→LLaDA | **comparison** | **32** | 53.1% | **0.388** | **[0.186, 0.590]** |
| Dream→LLaDA | 全部 | 491 | 72.5% | 0.752 | — |
| LLaDA→Dream | WikipediaEntity | 225 | 56.0% | **0.895** | — |
| LLaDA→Dream | bridge | 182 | 90.7% | 0.793 | — |
| LLaDA→Dream | **comparison** | **28** | 46.4% | **0.538** | **[0.306, 0.764]** |
| LLaDA→Dream | 全部 | 449 | 69.3% | 0.865 | — |

（`FreeForm` n=7–8、`Numerical` n=7 样本太少，不单列。）

## 一致的排序：WikipediaEntity > bridge > comparison

**三个独立数据源都给出同一顺序**：

| 数据源 | WikipediaEntity | bridge | comparison |
|---|---:|---:|---:|
| 主项目 Dream→LLaDA | 0.771 | 0.708 | 0.388 |
| 主项目 LLaDA→Dream | 0.895 | 0.793 | 0.538 |
| TRE LLaDA / HotpotQA（裸） | — | 0.841 | 0.691 |
| TRE Dream / HotpotQA（裸） | — | 0.801 | 0.668 |

**方向完全一致**：单跳事实题（WikipediaEntity）最好，多跳 bridge 次之，二选一 comparison 最差。

## 但不能定量

`comparison` 在主项目里只有 28–32 条，CI 宽度 **0.40 / 0.46**——比观测差距本身还大。

| 说法 | 状态 |
|---|---|
| "三个数据源方向一致"（4 组独立比较） | ✅ 有说服力 |
| "comparison 上 AUROC 约为 0.4–0.5" | ❌ 不可定量，CI 太宽 |
| "Dream→LLaDA 的 comparison 低于随机" | ❌ **不能说**（CI 含 0.5） |

## 为什么 comparison 更难

1. **二选一可以猜**：正类率降到 46–53%，接近平衡，AUROC 在平衡数据上更难做高；
2. **答案短且同质**（通常就是一个实体名），TRE 的熵信号区分度低；
3. **bridge 题的正类率 87–91%**，模型多半答不出，TRE 只需区分"明显不会"与"少数会"，容易。

## 对报告的建议

主项目的分层报告**应加入题型维度**（目前只有 hotpotqa / triviaqa）。
但必须在同一张表里标注 `comparison` 的 n=28–32，避免读者把 0.388 当成稳定估计。

## 若要确定，需要什么

- `comparison` 题在 pool2000 里只有 222 / 2000（11%），test 层每方向 28–32 条；
- 要把它压到 CI ≈0.15，需要约 **250 条 test**，即总池要 1000+ 条 comparison 题；
- HotpotQA 原始池的 comparison 占比就是 13%（213 / 1654），扩池也难大幅提高。
- **结论**：这一维度在现有数据规模下只能定性报告。

## 产物

- 主项目分层：本文（未落 JSON，因为样本量不支持作为正式产物）
- TRE 分层：`reports/tre_repro/answer_type_strata.md`
- 题型的定义来源：`data/raw_qa/subsets/pool2000_v1.jsonl` 的 `answer_type` 字段
