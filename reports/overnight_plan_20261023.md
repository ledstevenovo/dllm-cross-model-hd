# 整夜运行计划（2026-10-23 02:13 启动）

## 0. 起跑状态

| 项 | 状态 |
|---|---|
| pool2000 · LLaDA | ✅ 1800/1800，0 错误，已签核草案 + 已抽特征 |
| pool2000 · Dream | 1377/1800，预计 02:28 完成 |
| TRE R2 题单 | ✅ 已冻结（800 + 20，sha256 固定） |
| TRE judge | ✅ 新 key 验证通过：**100/100 解决，一致率 0.990，κ 0.979** |
| GPU | RTX 4080 SUPER（参考设备，与 pilot200 同源） |
| 剩余磁盘 | 68 GB |

## 1. 四个后台队列

| screen 名 | 脚本 | 职责 | 预计 |
|---|---|---|---|
| `pool2000` | `scripts/run_pool2000_collect.sh` | Dream 剩余采集 | ~02:28 结束 |
| `gpuqueue` | `scripts/run_gpu_queue.sh` | R2 smoke20 → R2 800 → TriviaQA L64 → HotpotQA L64 → Dream BF16 | 03:30–05:30 |
| `night` | `scripts/run_overnight_gpu.sh` | pool2000 全部分析（17 步） | 02:30–05:00 |
| `r2judge` | `scripts/run_r2_judge.sh` | R2 judge → 打分 → 置换 | R2 采完后 ~30 min |

`night` 与 `gpuqueue` 都等 pool2000 的 `driver done` 行，不靠估算时间。

## 2. 顺序设计：先出结论，后出稳健性

夜里可能跑不完，所以 `night` 队列按"能不能回答预注册问题"排序：

1. **Dream 签核草案** → 晋升 reviewed（`rule-signoff`，如实署名）
2. **特征抽取** → 合并 pilot200 + pool2000 = **2000 题**
3. **迁移矩阵**（预注册口径）→ **预注册判据**（唯一的"结论"步骤）
4. 分层 / 置换 / 对齐诊断 / 全特征集消融
5. 第二 judge 一致性（新 judge，只做一致性，不改标签）
6. 稳定性 ×2 种子 → 合并 → 多种子 → 重要性（最慢，放最后）

即使 08:00 被掐，第 3 步的结论已经在盘上。

## 3. 预注册判据（不得事后调整）

> `rel+LR Dream→LLaDA` 的 95% CI **上界 < 0.6** 且 `ent+LR` 同方向 CI **下界 > 0.7**
> → "Dream 源域方向性缺口"成立；否则按"未复现"报告。

`scripts/pool2000_verdict.py` 只算这两条，缺任何一格就**报错退出**而不是默认 false。
在 pilot200 上它正确地判为"未复现"——因为 CI 是 0.297–0.695，上界过不了 0.6。
这正是扩池要解决的问题：test 从 48 涨到 ~450，CI 宽度应从 ~0.40 压到 ~0.12。

## 4. 已完成的准备工作（本轮）

- **judge 换了供应商**：新 key 在 `sub.vankit.top`，模型名相同但服务栈不同。按项目规则
  "一个标签文件一个 judge"，先做了跨 judge 一致性：100 条 R1 已判样本重判，
  **一致率 0.990 / κ 0.979**，100/100 解决。所以新 key 可用于 R2，**但不改写 R1 标签**，
  两者在论文里作为协议差异记录。
- **端点限流实测**：并发 8 时 30/100 返回 429；并发 2 时 30/30 通过。队列因此固定
  并发 4 并带重试，而不是硬推 8。
- **合并逻辑已验证**：pilot200（200）+ pool2000（1800）= 2000 题，47 列完全对齐，
  无重复 sample_id，split 正好 1200/300/500。
- **LLaDA 已晋升**：1800 条 → `human:ledstevenovo:rule-signoff:2026-10-23`，
  correct 487 / incorrect 1281 / format_failure 32（正确率 27.1%，与 pilot200 的 26.4% 一致，
  无难度漂移）。

## 5. 早上怎么验收

```bash
# 1. 队列是否都结束
screen -ls
cat /root/autodl-tmp/night_logs/heartbeat.txt
cat /root/autodl-tmp/night_logs/driver.log | grep -E "START|OK|FAIL"

# 2. 唯一的结论
cat reports/pool2000_verdict.json

# 3. 关键产物是否齐
ls results/pool2000/main/transfer_matrix.csv
ls reports/pool2000_permutation.json
ls reports/pool2000_label_consistency.json
ls reports/tre_repro/r2_permutation_test.json

# 4. R2 的数字
cat results/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1/metrics.json
```

## 6. 预期时间线

| 时刻 | 事件 |
|---|---|
| 02:28 | Dream 采集完成 |
| 02:30 | `night` 开始签核 + 抽取（~5 min） |
| 02:35 | 迁移矩阵 + **判据出结果** |
| 02:45 | 分层 / 置换 / 对齐 / 消融 |
| 03:00 | 第二 judge 一致性（500×2 样本，并发 4，~15 min） |
| 03:15 | 稳定性种子 1（~35 min） |
| 03:50 | 稳定性种子 2（~35 min） |
| 04:30 | 多种子 + 重要性 + 晨检 |
| 03:30 | R2 800 采集开始（gpuqueue） |
| 04:30 | R2 judge（~15 min）→ 打分 → 置换 |

## 7. 已知风险

1. **Dream 采集可能比估算慢**：目前 2.02 s/题，稳定；若显存抖动会变慢，队列会等。
2. **judge 限流**：已按实测固定并发 4 + 5 次重试；若夜间被更严格限流，`--retry-needs-review`
   会在收尾再跑一遍。仍未解决的样本会进 `needs_review`，主表门禁会拦住而不是静默降级。
3. **R2 与 pool2000 有 115 题重叠**（同一 HotpotQA test 池），已写进 manifest；两项研究
   协议不同，不影响各自指标口径。
4. **扩池后 `late_only` 效应可能消失**：pilot200 上单特征 `late_entropy` 达 0.869，
   样本变大后可能回落。这是消融步骤要回答的，不是失败。
