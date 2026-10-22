# 扩池准备包 v1（主方案 §8 决策门达成后的执行预案）

状态：**题单已冻结（在任何新采集结果出现之前）**；尚未开始采集。规模默认 800/模型，见 §6 的规模选项。
决策门条件（标签可靠 + 稳定迁移缺口）已于 2026-10-22 夜间达成：稳定性研究 300×2 次重采样 + 标签质量证据（第二 judge 全覆盖 κ≈0.90、人工抽查 50 条）。

## 1. 预注册规则（冻结，不得在看到新结果后修改）

1. **目标规模**：题集 800（每模型 800 条轨迹）：train 480 / validation 120 / test 200，沿用 pilot200 的 60/15/25 比例。
2. **pilot200 原样保留**：200 道旧题保持既有 split；只新增簇，**不重采、不重划分、不重编号**（新增 = 600 题）。
3. **每簇一行代表**（sample_id 最小者），与 `build_pilot.py` 一致；分层 `hotpotqa:<answer_type>` + `triviaqa`，按存活池比例分配（`src.splitting.select_stratified`）。
4. **排除**所有已被任何实验使用过的簇：pilot200（DynHD 复现同题）、small200、smoke20（主项目）、TRE R1 `triviaqa_eval800`、TRE smoke20 → 共排除 **1192** 簇。
5. **确定性**：seed `20261022`，salt `pool800-v1-<split>`，按 hash 排序取前 k；选择过程**不使用任何标签/分数/结果信息**。
6. **冻结即承诺**：本清单在任何新采集或新结果出现后不得修改；如需变更规模，用同规则重新生成并单独记录（见 §6）。

## 2. 冻结产物

| 产物 | 路径 | sha256（前 16 位） |
|---|---|---|
| 全量列表（pilot + 新增） | `data/raw_qa/subsets/pool800_v1.jsonl` | `4e0680674855aa88` |
| **新增列表（采集输入）** | `data/raw_qa/subsets/pool800_v1_new.jsonl` | `df735229946387a9` |
| manifest（规则 + 计数 + 全部 question_id） | `data/manifests/pool800_v1.json` | `ba6aba47e6933bfc` |

计数（combined = pilot + new）：

| split | hotpotqa:bridge | hotpotqa:comparison | triviaqa | 合计（new） |
|---|---|---|---|---|
| train | 171 | 24 | 285 | 480（新 360） |
| validation | 41 | 7 | 72 | 120（新 90） |
| test | 81 | 13 | 106 | 200（新 150） |

**关键改进**：test 的 hotpotqa 层从 20 → **94**（bridge 81 + comparison 13）——正好修掉 pilot 里"hotpotqa 仅 20 条、个别层只有 4 个负例"这一最薄的层。

## 3. 完整性断言（脚本内失败即拒绝写出）

- 无跨 split 的簇（全局簇划分唯一）；无重复 question_id；新选与全部排除集合零重叠 —— 全部通过。
- 复算：`.venv/bin/python scripts/build_expansion_subset.py --total 800`（同参数应复现同一 sha256）。

## 4. 精度测算（test 集大小 → AUROC 95% 区间宽度）

方法：对 pilot 的目标域 test 项做簇级 bootstrap（1000 次/点），模型保持 pilot 拟合——刻画的是"测试集规模"带来的不确定性，正是扩池买到的部分。来源：`reports/expansion_precision.json`。

| 格 | 观测 AUROC | n=48 | n=100 | n=150 | **n=200** | n=300 |
|---|---|---|---|---|---|---|
| 异常格 Dream→LLaDA rel+LR | 0.494 | 0.410 | 0.265 | 0.230 | **0.187** | 0.158 |
| 参考格 Dream→LLaDA ent+LR | 0.830 | 0.241 | 0.174 | 0.142 | **0.121** | 0.095 |
| LLaDA→Dream rel+LR | 0.779 | 0.339 | 0.232 | 0.186 | **0.164** | 0.128 |

**解读**：800 规模下 test 每方向 ~200 条，三个关键格的区间宽度由 0.24–0.41 压到 **0.12–0.19（约减半）**，足以回答"缺口是否稳定"与"迁移/目标监督差"的方向问题。
**假设与保守性**：假设新题与 pilot 同分布；未计入"更大 train 重训"可能带来的变化（该变化通常进一步收窄区间，故此处偏保守）。

## 5. 采集与标注执行清单（有卡时按序执行）

1. **探针**（方案 §3/§4）：`nvidia-smi` + 在真实推理 venv 跑 BF16 资格脚本；再做两模型各 20 题 smoke，记录 `t_llada`、`t_dream` 单题时间、显存峰值、失败率。
2. **成本公式**（方案 §6，用实测代入，不预设价格）：`T = 600×(t_llada + t_dream) + 加载/I/O/重试`；共 **1200 条新增轨迹**（600 题 × 2 模型），已有有效样本复用。
3. **采集新增题**：
   ```bash
   .venv-llada/bin/python scripts/collect_llada.py --questions data/raw_qa/subsets/pool800_v1_new.jsonl \
       --output data/trajectories/bf16_pool800/llada --precision bf16 --verify-observer
   .venv-dream/bin/python scripts/collect_dream.py --questions data/raw_qa/subsets/pool800_v1_new.jsonl \
       --output data/trajectories/bf16_pool800/dream --precision bf16 --verify-observer
   ```
4. **标签**：`offline.py label` → 规则复核/签核 → 第二 judge 抽查（现成脚本：`scripts/label_consistency_main.py`，可按 pool800 全量跑）。
5. **分析**：`offline.py extract` → `evaluate`（含分层 dataset axis）→ `stability_study.py --repeats 300`（两 seed）→ `multiseed_transfer.py` → `morning_digest.py` 风格汇总；报告按 `reports/paper_draft.md` §3 表格复算。

## 6. 规模选项（同规则、同 seed，可按预算选择后再冻结）

| 规模 | 新增题 | test/方向（约） | 异常格区间宽度（投影） |
|---|---|---|---|
| **800（本包默认）** | 600 | 200 | ~0.19 |
| 1200 | 1000 | 300 | ~0.16 |
| 2000 | 1800 | 500 | ~0.12 |

生成方式：`scripts/build_expansion_subset.py --total 1200`（或 2000），得到新的 sha256 与 manifest 后再冻结；规则与排除集不变。方案 §8 明确"统计精度和标签成本决定规模，不为凑 2000 无条件扩大"。

## 7. 状态

- [x] 题单冻结（本文件 + `data/manifests/pool800_v1.json` + 两个 jsonl 哈希）
- [x] 精度测算（§4）
- [ ] 有卡探针 + smoke（需 GPU）
- [ ] 采集 1200 条新增轨迹（需 GPU）
- [ ] 标签签核 + 第二 judge 全量一致性
- [ ] 分析与报告更新（§5.5）
