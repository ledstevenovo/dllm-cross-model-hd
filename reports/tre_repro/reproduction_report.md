# TRE R1 复现报告：LLaDA-8B-Instruct × TriviaQA（800 题）

日期：2026-10-22。上位文档：`docs/TRE_4080SUPER_32GB_复现方案.md`（v3.1）。差异清单：`reports/tre_repro/protocol_diff.md`。
定位：**明示差异的协议近似复现**（替代 judge、自选题单、自定生成预算）；不声称与原文数值完全对齐。

## 1. 结果摘要

- 主口径（预注册）：**原始 TRE（全部 128 个生成位置的熵加权和）**，方向"越高越危险"；单次生成、无训练、无量化。
- **TRE AUROC = 78.34%**（95% CI 74.92–81.72），AUPRC = 82.75%（CI 78.83–86.78）
- 稳健性变体 `tre_effective`（仅有效回答区域）：AUROC = 82.70%（CI 79.72–85.53）
- 样本：800/800 保留（无剔除、无 needs_review）；正类 507 / 负类 293（正类率 63.4%）
- bootstrap：1000 次按 `question_id` 分组重采样（seed 20261021），有效 1000/1000

## 2. 与论文表 1 比较

原表列名为"总扩散步数"（128 / 64），与本次自定预算 L128/S64/B128 无法一一对应，两列并列对照：

| 条目 | 原文（表 1） | 本次 | 差值（百分点） | 本次 95% CI | 保留样本 | 协议差异要点 |
|---|---:|---:|---:|---|---:|---|
| LLaDA-8B-Instruct / TriviaQA（128 列） | 82.2 | **78.34** | −3.9 | 74.92–81.72 | 800 | judge 换为 J2（moma deepseek-v4.1-flash）；题单自选（seed 20261021，rc.nocontext validation）；prompt③ 裸问题；EOS/EOT 口径自定；生成预算自定 |
| LLaDA-8B-Instruct / TriviaQA（64 列） | 86.5 | **78.34** | −8.2 | 74.92–81.72 | 800 | 同上，另：原文 64 列对应 gen_length/揭示策略未公开 |

结论写法（按方案 §8 要求）：本次 CI 包含 128 列原值、不包含 64 列原值；**不因单次偏差判定方法无效，也不因接近就宣布对齐**。差异可解释项：替代 judge 的判定口径与保留集合（本次二判翻转 0，未剔除任何样本）、题单与 split（原文 ID/seed 未公开）、prompt 与答案格式、EOS/EOT 之后位置是否计分（本次主口径全位置计入，尾部占比均值 60.4%）、生成预算与揭示策略（原文未公开）。

## 3. 生成与标注计数

- 生成：800/800 完成；终止 769×EOT + 31×EOS；空答 0、截断 0；有效长度 min/中位/p95/max = 1/12/29/126
- judge（J2，冻结提示词 v3）：首判 correct 293、incorrect 507；二判实际执行 507 次，**incorrect→correct 翻转 0**（两遍过滤未剔除任何样本）；needs_review 0
- 标注过程中被限流的 80 条已按协议整体重跑（旧尝试留档 `paper_judgments.jsonl.retry.jsonl`），其中 1 条再次限流后单独重跑成功
- 诊断（不替换主口径，方向未翻转）：有效长度单独作 score 的 AUROC 0.399、`tail_tre` 0.624、尾部占比 0.237 —— 主口明显强于所有诊断项

## 4. 独立复算断言（正式批次全量）

对 800 条轨迹从原始 NPZ 按论文式(3)重新求和（不调用实现），与 `scores.csv` 的 `tre` 逐条比较：
**800/800 完全一致，最大绝对差 0.0**。正类方向与 `scores.csv` 标签计数（507 incorrect / 293 correct）一致。

## 5. 差异与口径（详见 protocol_diff.md）

1. judge：J2 moma `deepseek-v4.1-flash`（原文 GPT-4o mini，提示词/snapshot 未公开）——标签集合因此可能不同；
2. 题单：自选（`rc.nocontext` validation；原文 800 题 ID 与抽样 seed 未公开）；
3. prompt：③裸问题 + 原生 chat template；
4. 生成预算：自定 L128/S64/B128（每步 2 token）；
5. EOS/EOT：首个停止 token 前为可见回答，主口径为全位置 TRE（尾部诊断并列报告）；
6. 采样规则：与冻结参考 `Lost-in-Diffusion/LLaDA/generate.py`（sha256 `aafeca55…`）逐项一致；揭示置信度在 FP16 上计算（R0 已量化，|Δp| ≤ 3.5e-4 的近并列互换）；
7. 硬件：RTX 4080 SUPER 31.5 GiB（原文 Quadro RTX 6000 24GB）。

## 6. 限制与下一步

- 本结果**不是**论文 R2/R3 的完整复现：仅 LLaDA × TriviaQA × 单预算；Dream FP16 因原生 entropy 采样 NaN 风险仍阻塞（只保留 BF16 变体选项，需单独立项）；
- 下一步（R2）：HotpotQA / CommonsenseQA（CSQA 选项格式需另冻结）、另一预算列；Dream 的等效判定方案；
- 所有口径均预注册，未用测试集调参；bootstrap 只反映抽样不确定度，不补偿协议差异。

## 7. 可复算性

| 产物 | 路径 / 哈希 |
|---|---|
| 题单 | `data/tre_repro/questions/triviaqa_eval800.jsonl`，sha256 `257396001137e0d5…` |
| 轨迹 | `data/trajectories/tre_repro/llada_triviaqa_fp16_L128_S64_B128_v3`，manifest sha256 `911eec140439…` |
| 标注 | `data/tre_repro/labels/<run>/paper_judgments.jsonl`，sha256 `c5b1f07b7f23ad5e…`；提示词 sha256 `2d125bea4f6a5d5a…` |
| 评分 | `results/tre_repro/<run>/{scores.csv,metrics.json}` |
| 代码 | commit `f21eeba1180eea6b…`（judge 客户端含限流重跑；评分入口为 v3.1 交付） |
| 复算命令 | `score_tre_repro.py --run … --questions … --judgments … --judge-prompt … --output … --bootstrap 1000` |

**一句话结论：TRE 的核心方法在本实例上跑通并给出 78.3% AUROC（CI 74.9–81.7）；与原文的差距在明示差异下可解释，但不能归因于方法本身。**
