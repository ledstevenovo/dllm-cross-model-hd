# TRE R2（HotpotQA）设计与风险预判

日期：2026-10-23。题单：`data/tre_repro/questions/hotpotqa_eval800.jsonl`（冻结于 `data/tre_repro/questions_manifest_r2.json`）。

## 与 R1 的协议差异（必须逐条列出）

| 项 | R1（TriviaQA） | R2（HotpotQA） |
|---|---|---|
| prompt 版本 | `v3-bare-question`（裸问题） | `v4-hotpotqa-context`（上下文接地） |
| prompt 长度 | 均值 34 token，最大 68 | 均值 1475 token，最大 3715（LLaDA） |
| 单题耗时 | 2.8 s | **20.1 s**（smoke20 实测） |
| 800 题采集 | ~40 min | **~4.5 h** |
| judge 端点 | moma（zhenze-huhehaote） | vankit（sub.vankit.top） |
| judge 跨供应商一致性 | — | 0.990 / κ 0.979（`reports/tre_repro/judge_crosscheck.json`） |

上下文是 HotpotQA 的必需项（无上下文不可答），因此 prompt 版本必然不同。这不是"改动 R1 的 prompt"，而是新增一个版本；R1 的题单与记录仍逐字节不变。

## 预期正类率显著低于 R1

smoke20 的 20 题**全部判为 correct**。这是有上下文时的正常表现：HotpotQA 的答案直接出现在 distractor 段落里，8B 模型基本能摘出来。R1（TriviaQA，无上下文）的正类率是 63.4%。

这带来一个统计后果，提前算清：

| incorrect 率 | 正例 | 负例 | AUROC 标准误（真值 0.78） | 95% CI 宽度 |
|---:|---:|---:|---:|---:|
| 10% | 80 | 720 | 0.031 | ~0.12 |
| 15% | 120 | 680 | 0.026 | ~0.10 |
| 20% | 160 | 640 | 0.023 | ~0.09 |
| 30% | 240 | 560 | 0.019 | ~0.08 |
| 63%（R1） | 504 | 296 | 0.016 | ~0.06 |

即**即使正类率只有 10%，R2 的 CI 宽度仍约 0.12**，足以与论文表 1 的原文值（85.6 / 88.1）做区间比较。但若正类率低于 5%（正例 <40），CI 会宽到 0.17+，那时只能报告点估计与"方向"。

## 判读规则（先写死）

1. **主口径**：`tre`（全部生成位置的熵加权和），方向"越高越危险"，与 R1 一致；
2. **与原文比较**：原文 HotpotQA 列是 85.6（128 步）/ 88.1（64 步）。本次只跑 L128/S64/B128 一列，
   因此只与 128 列比较，**不并列两列**（R1 已确立这一写法）；
3. **若正类率 <5%**：只报告 AUROC 点估计与 CI，明确标注"正类过少，CI 过宽，不作强弱判断"；
4. **不因数值接近就宣布对齐**，也不因偏差就判方法无效——差异项已在上表逐条列出。

## 已知风险

1. **耗时**：4.5 h 采集 + ~30 min judge，若 07:30 才开始 judge，09:00 前可能未完成。judge 不占 GPU，
   可跨过期限继续跑；
2. **上下文导致的格式问题**：模型可能复述上下文（smoke20 里已见 `"Tom Hiddleston. \n\nRelevant context: ..."`）。
   这会拉低 correct 率但也可能引入判分噪声——R2 的 format_failure 率需要与 R1 对比后再定；
3. **judge 限流**：并发 4 + 5 次重试，收尾用 `--retry-needs-review`；
4. **与 pool2000 的 115 题重叠**：同一 HotpotQA test 池，协议不同，已写入 R2 manifest。
