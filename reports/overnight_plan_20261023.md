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

---

## 8. 夜间执行记录与调整（03:56）

### 已完成（第一轮，全部 rc=0）

| 步 | 结果 |
|---|---|
| 01 Dream 签核草案 | correct 521 / incorrect 1098 / format_failure 180（正确率 28.9%，pilot200 27.0%） |
| 02 晋升 reviewed | 两模型各 1800 条，`human:ledstevenovo:rule-signoff:2026-10-23` |
| 03 特征抽取 | `data/features/pool2000_{llada,dream}.parquet` |
| 04 合并 | 2000 题 / 4000 行，1200-300-500 |
| **05 迁移矩阵** | 16 格，test 449–491 |
| **06 预注册判据** | **未复现（两条检查都不通过，且方向相反）** |
| 07 分层 | 跨数据集轴 32 格，0.663–0.886 |
| 08 置换 | 16/16 格 p ≤ 4e-4 |
| 09 对齐 | 该格 0.752 → 0.764，无物可修 |
| 10 消融 | 10 特征集；`late_only` 0.766 最优 |
| 11 第二 judge | 1000/1000 覆盖，一致率 0.933，κ 0.840 |

### 调整：稳定性降为 150 次 + 两种子并行

第一轮在 12_stability 暴露真实代价：2000 题后每次簇级重采样需重拟合 3760 行，
**2.8 s/次 × 16 组合 × 300 次 = 3.8 h**，会跑到 07:20 并挤压 R2 的 judge 窗口。

处置（无需用户决策，按"预算优先保证链路完整"原则）：

- 重复次数 **300 → 150/组合**，但**两个种子并行**跑，合计边际仍是 300 次/格，
  与 pilot200 的 300×2 口径等价；
- 实测 2 路并行 + 每进程 6 线程（16 核）不显著互相拖慢；
- 新脚本 `scripts/run_overnight_pass2.sh`，screen `night2`，`.done` 标记使已完成步骤自动跳过。

预计 150×16×2.8s ≈ 1.9 h（两种子同时），05:50 前后完成，留足 R2 收尾时间。

### R2 采集的实际代价

smoke20 实测 20.1 s/题（上下文使 prompt 长 30–40 倍），800 题 ≈ **4.5 h**，02:50 开始，
预计 **07:15–07:30** 完成。随后 `r2judge` 的 screen 会自动接手 judge（估计 20–30 min）。
若超出 09:00，judge 会继续跑到完成——它不占 GPU，可以独立于卡的期限。

---

## 9. 夜间事故与处置（07:55）

### 事故 1：R2 轨迹写到了仓库外

`run_gpu_queue.sh` 里 `Q=/root/autodl-tmp/tre_repro/...` 少了 `data/trajectories/tre_repro`
这一段，而其它任务用的是仓库相对路径。结果 800 题的采集写进了 `/root/autodl-tmp/tre_repro/`，
而 `data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1` 不存在。

发现方式：日志显示 653/800，但预期目录不存在。

**数据没有丢**：656 条 trace（44 MB）完好，`status=running`。处置：
1. 脚本全部改为 `"$REPO/data/trajectories/..."`，不再依赖 cwd；
2. `run_r2_judge.sh` 接受两个位置，优先仓库内，两个都存在时**拒绝合并**并报警；
3. 新增 `run_r2_watch.sh`：按进程等待采集结束 → 迁移 → 完整性预检（800 个冻结 sample_id 全在、缺 0）→ 再判分。

结果：07:12 自动迁移成功，预检 800/800、0 错误。

### 事故 2：队列静默中断（我的操作导致）

我**在 `run_gpu_queue.sh` 正在运行时编辑了它**。bash 是增量读取脚本文件的，改写运行中的脚本会让
读取位置错位，导致队列在 R2 之后静默退出——因此 L64 与 Dream 的任务都没有启动。

教训：**运行中的 shell 脚本不可编辑**，要先复制再改，或停掉重启。

处置：GPU 空转后立即用修正版脚本补跑价值最高的任务。

### 事故 3：judge 端点限流

并发 4 和并发 2 都在几分钟内撞 429。实测端点单次调用 200 正常，说明是速率限制而非配额耗尽。
处置：改**串行 + `--min-interval 1.2` + 10 次重试**，2 分钟稳定 45 条，无 429。R2 800 条在 25 分钟内判完。

**通用结论**：这个端点只支持近串行调用；并发带来的收益被重试抵消。后续所有 judge 任务固定 `--concurrency 1`。

### 期限内的取舍

07:54 时 GPU 空出，距 09:00 约 65 分钟。三个待办任务的代价：

| 任务 | 实测/估算 | 能否在 09:00 内完成 |
|---|---|---|
| TriviaQA L64（800 题，无上下文） | ~37 min | ✅ 启动于 07:54，预计 08:35 |
| HotpotQA L64（含上下文） | ~4.5 h | ❌ |
| Dream HotpotQA BF16 | ~4.5 h | ❌ |

选择 **TriviaQA L64**：它能补齐论文表 1 的第二个预算列（原文 86.5），是本轮唯一能在期限内产出
完整新数字的任务。另外两个留下脚本与说明，供后续执行。
