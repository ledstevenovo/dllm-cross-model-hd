# Dream×HotpotQA 的 judge 切换：从 deepseek 到 LongCat

日期：2026-10-23 16:10。

## 发生了什么

Dream×HotpotQA 采集完成后（15:22），判分开始时 deepseek 端点**变慢**：

| 指标 | 切换前（TriviaQA 判分时） | 切换时 |
|---|---:|---:|
| 单次调用（8 token） | 2.6 s | **6.9 s** |
| 平均延迟 | 3.6 s | **12.3 s** |
| p95 延迟 | — | **36.1 s** |
| 错误率 | 0 | 0 |

不是限流（无 429），是**供应商侧普遍变慢**。按 12.3 s/次、1.6 次/样本算，
剩余 648 条需 **2.5 小时**，会拖到 18:15。

## 为什么不"接着用 deepseek 判完"

项目规则是**一个标签文件一个 judge**。若前 202 条用 deepseek、后 598 条用 LongCat，
就是拼接，会让同一份标签里混着两个供应商的口径。

## 两个合规方案

| 方案 | 做法 | 完成时间 | 代价 |
|---|---|---|---|
| A | 等 deepseek 判完剩余 648 条 | ~18:15 | 慢 1 小时 |
| **B（采用）** | **整份 800 条改用 LongCat 重判** | **~17:00** | 丢弃 deepseek 的 202 条 |

选 B：更快，且**整份文件只有一个 judge**，规则满足。deepseek 的 202 条归档为
`/root/autodl-tmp/dream_hotpot_logs/deepseek_partial_202.jsonl`（从未进入任何已发布数字）。

## 切换前的一致性验证（先验证再换）

在**本数据集**上抽 57 条（30 条 incorrect + 40 条 correct，按 deepseek 判定分层）双判：

| 指标 | 值 |
|---|---:|
| 解决率 | 57/57 |
| 一致率 | **0.965** |
| Cohen's κ | **0.916** |
| 分歧 | 2 条（各方向 1 条） |

对照：跨供应商在 TriviaQA 上是 0.990 / κ 0.979；本项目人工 vs judge 是 0.960 / κ 0.884。
所以 0.965 / 0.916 属于"两个供应商之间的一致性高于它们与人工的一致性"这一正常范围。

**注意**：Dream 在 HotpotQA 上给的是短实体名（中位 5 token），与 LLaDA 的长复述不同，
所以这里的一致性**不能**从 TriviaQA 的结果直接外推——必须重新测，本页就是那次测量。

## 对最终数字的影响

R2（LLaDA/HotpotQA）用 deepseek + 三方仲裁。Dream/HotpotQA 用 LongCat。
**两者不是同一个 judge**，因此：

- 各自的 AUROC 可以与自己数据集内的随机基线比较；
- **跨模型的直接比较（LLaDA vs Dream 在 HotpotQA 上）必须带着这个差异读**；
- 若两者差距接近临界值，应以"judge 差异"作为一项不确定性来源列出，而不是当成效应。

## 可复算

```bash
set -a; . /root/autodl-tmp/.env.longcat; set +a
.venv/bin/python scripts/dh_crosscheck.py --sample /tmp/opencode/dh_crosscheck.json \
  --out reports/tre_repro/dh_judge_crosscheck.json --workers 3
```
