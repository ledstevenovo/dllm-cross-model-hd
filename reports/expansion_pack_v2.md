# 扩池准备包 v2（规模 2000/模型，取代 v1 的 800）

状态：**题单已冻结**（2026-10-22，在出现任何新采集结果之前）。规模由用户于 2026-10-22 选择为 **2000/模型**。

> **与 v1 的关系（必须读）**：`reports/expansion_pack_v1.md` 曾冻结 800 规模。用户在两者之间选择了 2000，因此 v1 的题单被**作废**，文件已删除，不再构成预注册承诺。原因：两个题单用同一 seed 但按不同 `--total` 重新选择，**不是嵌套关系**（1800 道新题中仅 66 道与 v1 的 600 道重合），不能当作"v1 的超集"继续。任何引用 v1 的旧笔记以本文件为准。

## 1. 预注册规则（冻结，不得在看到新结果后修改）

1. **目标规模**：每模型 2000 条轨迹：train 1200 / validation 300 / test 500（60/15/25，与 pilot200 同比例）。
2. **pilot200 原样保留**：200 道旧题保持既有 split；只新增簇，**不重采、不重划分、不重编号**（新增 = 1800 题）。
3. **每簇一行代表**（sample_id 最小者），与 `build_pilot.py` 一致；分层 `hotpotqa:<answer_type>` + `triviaqa`，按存活池比例分配。
4. **排除**所有已被任何实验使用过的簇：pilot200（DynHD 复现同题）、small200、smoke20、TRE R1 `triviaqa_eval800`、TRE smoke20 → 共排除 **1192** 簇。
5. **确定性**：seed `20261022`，salt `pool2000-v1-<split>`，按 hash 排序取前 k；选择过程**不使用任何标签/分数/结果信息**。
6. **冻结即承诺**：本清单在任何新采集或新结果出现后不得修改。

## 2. 冻结产物

| 产物 | 路径 | sha256 |
|---|---|---|
| 全量列表（pilot + 新增） | `data/raw_qa/subsets/pool2000_v1.jsonl` | `1d39c0d2fcb83055677a02e4d803940c233c1158967633c86182506cae321c00` |
| **新增列表（采集输入）** | `data/raw_qa/subsets/pool2000_v1_new.jsonl` | `eb473032596f717ec79438deb939aa94059331a86ff6b02b9bcf0e6156a93f08` |
| manifest（规则 + 计数 + 全部 question_id） | `data/manifests/pool2000_v1.json` | — |

计数（combined = pilot + new）：

| split | hotpotqa:bridge | hotpotqa:comparison | triviaqa | 合计（new） |
|---|---|---|---|---|
| train | 427 | 60 | 713 | 1200（新 1080） |
| validation | 102 | 19 | 179 | 300（新 270） |
| test | 210 | 32 | 258 | 500（新 450） |

## 3. 完整性断言（已复算，全部通过）

- 两个 jsonl 的 sha256 与 manifest 逐字一致；
- `full = pilot + new`：2000 = 200 + 1800，且 question_id 集合严格相等；
- pilot200 的 split 全部保持；新增与 pilot 零重叠；无重复 question_id；
- 无跨 split 的簇（全局簇划分唯一）；新增簇与 1192 个排除簇零重叠；
- manifest 记录的 question_id 集合与两个文件完全一致。

复算：`.venv/bin/python scripts/build_expansion_subset.py --total 2000 --name pool2000_v1`

> 注意：`--name` 同时是选择用的 salt（`<name>-<split>`），因此**必须连同同名一起复算**，改名会得到另一套题（不是更小/更大的嵌套集）。已实测：同参数连跑两次 sha256 完全一致。

## 4. 题单预检（已做）

| 项 | 结果 |
|---|---|
| prompt 长度（词） | 均值 24.7、p95 36、最大 56（pilot 最大 59） |
| LLaDA token 长度（含 chat template） | 均值 49.0、p95 65、最大 **108** |
| Dream token 长度 | 均值 52.1、p95 68、最大 **106** |
| 上下文 / 生成预算 | 4096 / 64 → 无截断风险 |
| 与 pilot 重复的题干 | 0 |
| 空 gold answer | 0 |
| gold 出现在 prompt 中 | 0（粗检的 3 处命中为 `NIGER`⊂`Nigeria`、`no`⊂`known`、乐队名 `!!!` 等假阳性） |

## 5. 精度测算（test 集大小 → AUROC 95% 区间宽度）

沿用 v1 的簇级 bootstrap 方法（`reports/expansion_precision.json`，模型保持 pilot 拟合，只改变测试集规模）：

| 格 | 观测 AUROC | n=48（现状） | n=200（v1） | **n=450（本包）** | n=500 |
|---|---|---|---|---|---|
| 异常格 Dream→LLaDA rel+LR | 0.494 | 0.410 | 0.187 | **≈0.125** | ≈0.12 |
| 参考格 Dream→LLaDA ent+LR | 0.830 | 0.241 | 0.121 | **≈0.081** | ≈0.08 |
| LLaDA→Dream rel+LR | 0.779 | 0.339 | 0.164 | **≈0.110** | ≈0.11 |

**解读**：每方向 test 约 450–500 条，三个关键格的区间宽度压到 **0.08–0.13**，足以把"缺口是否稳定"与"检测器优劣"分开讨论。v1（800）只到 0.12–0.19。

## 6. 采集与标注执行清单（有卡时按序执行）

1. **设备**：必须在**同一台设备**上采完两个模型（见 `reports/device_migration_5090.md` §4）。先跑 `scripts/gpu_env_probe.py` 记录资格。
2. **成本**（5090 实测，pilot200 每模型 200 题 1.338/1.362 s 单题）：
   `T ≈ 1800×(1.34+1.36) s + 2×加载 + I/O ≈ 81 分钟 + 开销`，预计 **1.5–2 小时**（含 `--verify-observer` 的重复生成）。
3. **采集新增题**：
   ```bash
   .venv-llada/bin/python scripts/collect_llada.py --questions data/raw_qa/subsets/pool2000_v1_new.jsonl \
       --output data/trajectories/bf16_pool2000/llada --precision bf16 --verify-observer
   .venv-dream/bin/python  scripts/collect_dream.py  --questions data/raw_qa/subsets/pool2000_v1_new.jsonl \
       --output data/trajectories/bf16_pool2000/dream --precision bf16 --verify-observer
   ```
   中断后加 `--resume`；若进程被强杀留下 `.collection.lock`，**先核实锁内 PID 已不存在**再删除（代码故意不自动清理）。
4. **标签**：`offline.py label` → `scripts/draft_signoff_review.py --prefix pool2000`（规则已对 pilot200 400/400 回归，会自检）→ 人工签核 → `finalize_reviewed_labels.py`。
5. **标签质量**：第二 judge 全覆盖（`scripts/label_consistency_main.py`，LongCat API）+ 分层人工抽查。3600 条 judge 调用，按 R1 实测 0.5–2.1 s/次、4 路并发估算约 10–25 分钟。
6. **分析**：`offline.py extract` → `evaluate`（dataset axis 分层）→ `stability_study.py --repeats 300`（两种子）→ `multiseed_transfer.py` → 更新 `reports/paper_draft.md` §3 表格。
7. **预注册判据**（先写死再跑）：若 `rel+LR Dream→LLaDA` 的 95% CI 上界仍 <0.6，且 `ent+LR` 同方向 CI 下界 >0.7，则"Dream 源域方向性缺口"成立并可作为主结论；否则按"未复现"报告。

## 7. 状态

- [x] 规模选择（用户 2026-10-22：2000）
- [x] 题单冻结 + 全部完整性断言 + 预检
- [x] 复算可重现（同 `--name` 两次 sha256 一致）
- [ ] 有卡探针（5090 已完成，见 device_migration_5090.md）
- [ ] 采集 3600 条新增轨迹（需 GPU，1.5–2 h）
- [ ] 标签签核 + 第二 judge 全量一致性
- [ ] 分析与报告更新（§6.6–6.7）
