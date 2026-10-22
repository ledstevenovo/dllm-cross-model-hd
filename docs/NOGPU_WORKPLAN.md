# 无卡模式工作清单（2026-10-22 起）

本文件是"不需要 GPU 就能一直推进"的执行清单，脚本为 `scripts/overnight_nogpu.sh`（可重入，`DRY_RUN=1` 只打印计划）。
GPU 只在**采集/重采**时需要；此清单中的每一步都不占用 GPU，可在无卡模式或本地完成。

## 0. 为什么可以无卡推进

- 权重缓存与推理环境已在持久盘（`/root/autodl-tmp/hf-cache`、`.venv-llada`、`.venv-dream`、`.venv-dynhd`），切无卡不删盘即可复用；
- 已有轨迹已落盘：TRE 800 条、主项目 BF16 pilot200 ×2、smoke20 ×2、DynHD pilot200 ×2；
- 训练/评测/标注/统计/报告全部是 CPU 或 API（judge）任务。

**唯一约束**：切无卡会重启容器，正在跑的进程会被杀。切换前 `screen -ls` 必须为空。

## 1. 隔夜队列（12 步，2026-10-22 夜实际执行）

一键全跑（后台，推荐参数）：

```bash
cd /root/autodl-tmp/dllm-cross-model-hd
STABILITY_REPEATS=800 STABILITY_MAX_SECONDS=12600 STOP_AFTER_MIN=600 CYCLES=4 \
  screen -dmS overnight bash scripts/overnight_nogpu.sh
screen -dmS guard bash scripts/overnight_guard.sh     # 独立守护，每 5 分钟
```

步骤与产物（`.done/NN_*` 标记断点续跑，重跑自动跳过）：

| 步 | 内容 | 无卡实测 | 产物 |
|---|---|---|---|
| 01 | 备份打包 | ~10 s | `/root/autodl-tmp/backup_<date>/*.tar.gz` + `MANIFEST.sha256` |
| 02 | 标签签核 + 特征抽取 | ~5 min | `data/labels/*.reviewed.jsonl`、`data/features/pilot200_*.parquet` |
| 03 | 阶段 7 迁移矩阵 | ~20 min | `results/stage7/{main,ablations}/`（失败降级：单特征集 + bootstrap 200） |
| 04 | TRE 离线分析（29 分数族） | ~7 min | `reports/tre_repro/offline_analysis.json` |
| 05 | TRE 簇级置换检验（10000 次） | ~8 min | `reports/tre_repro/permutation_test.json`（失败降级 2000 次） |
| 06 | 多种子矩阵（5 seeds） | ~38 min | `reports/main_project_multiseed.{json,csv}` |
| 07 | 特征重要性（LOO + 置换） | ~2 min | `reports/main_project_importance.{json,csv}` |
| 08 | 稳定性重采样（800 次/格） | ~2.8–3.5 h | `reports/main_project_stability.{json,csv}` |
| 09 | DynHD 交付汇总 | ~2 s | `reports/dynhd_reproduction_summary.{md,json}` |
| 10 | 标签一致性（无 key 自动跳过） | – | `overnight_logs/10_label_consistency.log` |
| 11 | 晨检报告 | ~10 s | `reports/overnight_<date>_summary.md` |
| 12 | 提交推送（`reports/ scripts/ docs/`） | ~5 s | 远端 main |

稳定性重采样说明（0.5 核实测 ~1.6 s/次重拟合）：

- 每格耗时 ≈ REPEATS × 1.6 s；8 个组合全部完成 ≈ 8 × REPEATS × 1.6 s（800 次 ≈ 2.8 h）；
- `STABILITY_MAX_SECONDS` 为整步硬上限：到点按组合边界停止，已完成的组合保留、未完成组合标 `partial` 并写入 `missing_combos`，检查点保留可续跑（`<out>.checkpoint.json`，已 gitignore）；
- 每个组合使用由 `--seed` + 组合键派生的独立确定性 RNG，续跑结果与不中断一致。

一键晨间汇总：`.venv/bin/python scripts/morning_digest.py` → `reports/morning_digest.md`（跨产物关键数字 + provenance + partial 告警）。

## 2. 之后的无卡任务队列

| 优先级 | 任务 | 需要 GPU？ | 说明 |
|---|---|---|---|
| 1 | ~~**阶段 7 结果解读与报告**~~ ✅ **已完成（10-22 05:53）** | 否 | 稳定性判决：迁移缺口 = **Dream 源域的方向性缺失**（同方向仅 `entropy_raw+LR` 稳定迁移 0.838；`rel+LR` 0.514 ≈ 随机，非负迁移）。证据：`reports/stage7_initial_observations.md` §5、`reports/main_project_stability.json`、`reports/morning_digest.md`。是否扩池待你决策 |
| 2 | **标签质量证据** | 否（第二 judge 用 LongCat API） | ✅ **已完成（10-22）**：第二 judge 覆盖率 373/373、一致率 0.957/κ 0.896（DynHD 0.970/κ 0.933）；**人工抽查 50 条已完成**：人工 vs 规则 0.900（κ 0.733）、人工 vs judge 0.960（κ 0.884），7 条分歧人工裁决 5:2 站 judge（judge 的 2 次失利均为上游缺陷题）。证据页 `reports/label_quality_evidence.md`，明细 `reports/label_spotcheck_summary.json` |
| 2b | **主项目扩池准备（§8 决策门）** | 否（冻结可在无卡完成） | ✅ **题单已冻结（10-22，规模 2000）**：`data/manifests/pool2000_v1.json` + `reports/expansion_pack_v2.md`（规则、排除 1192 簇、1200/300/500 按簇全局划分、哈希、精度测算：test ≈450/方向使异常格 CI 宽度降到 ≈0.12）。采集需卡：1800 新题 × 2 模型 = 3600 条（5090 实测约 1.5–2 h）。**v1 的 800 规模题单已作废并删除** |
| 3 | **DynHD 可选扩池准备** | 题单冻结无卡，采集需卡 | `pick_longest` / 题单冻结 / split 脚本都已就绪 |
| 4 | **TRE R2 准备** | 题单/prompt 冻结无卡，采集需卡 | HotpotQA / CSQA 格式与 prompt 需先冻结并登记 |
| 5 | **论文级整理** | 否 | 把 TRE R1（78.34%，CI 74.92–81.72）、阶段 7 矩阵、DynHD 域内结果整理成可发表报告 |
| 6 | **备份策略固化** | 否 | 每次大采集后重新打包并核对 `MANIFEST.sha256` |

## 2c. 5090 迁移（2026-10-22 有卡）

实例从 RTX 4080 SUPER（sm_89）迁到 RTX 5090（sm_120）。有卡资格与设备一致性结论：

- **环境资格通过**（`reports/gpu_env_probe_{llada,dream}.json`）：torch 2.8.0+cu128 的 wheel 架构表含 sm_120；BF16 原生支持，BF16 matmul 与 FP32 参考一致；SDPA flash/mem-efficient 可用；31.36 GiB。
- **真实加载与 smoke20 通过**：LLaDA 5.0 s / 15.0 GiB，Dream 4.8 s / 14.3 GiB；两模型各 20/20，`--verify-observer` 全过；单题 1.34 s / 1.36 s（4080S 为 2.27 / 2.09 s）。
- **BF16 跨架构不逐位可复现**（`reports/device_consistency_pilot200.json`）：pilot200 LLaDA 上 token 全同 87.5%、答案文本变化 10.5%、规则标签翻转 **3/200 = 1.5%**；同机重跑 10/10 全同、熵差 0.0，说明差异来自架构内核而非不确定性。
- **采集设备规则（新增，必须遵守）**：扩池的新增轨迹，**两个模型必须在同一设备上采集**。禁止把 5090 的新 LLaDA 轨迹与 4080S 的旧 Dream 轨迹拼进同一张迁移矩阵——跨设备差异会与"跨模型缺口"混淆。pilot200 既有轨迹原样保留（其内部同设备、自洽），不重采、不替换。
- **pool2000 题单预检通过**：1800 道新题，LLaDA 最长 108 token / Dream 最长 106 token（上下文 4096、生成预算 64），与 pilot 无重复题干、无空 gold、无跨 split 簇；同 `--name` 复算 sha256 一致，题单不动。

## 2d. pool2000 扩池采集与后续队列（2026-10-22 起）

规模已由用户定为 **2000/模型**（`reports/expansion_pack_v2.md`）。采集在 screen `pool2000` 中后台运行：

```bash
screen -dmS pool2000 bash scripts/run_pool2000_collect.sh   # 已在 18:09 启动
screen -ls                                                   # 确认存活
tail -f /root/autodl-tmp/pool2000_logs/driver.log             # 看每步 rc
```

- 输出：`data/trajectories/bf16_pool2000/{llada,dream}`（1800 题 × 2 模型，bf16/64-64-64/seed 20261020/`--verify-observer`）；
- 设备资格在采集**之前**写入 `pool2000_logs/gpu_env_probe_*.json`，两模型均确认 RTX 5090 / sm_120（同设备规则见 §2c）；
- 预计 1.5–2 小时；中断后加 `--resume` 续采（若留 `.collection.lock`，先核实锁内 PID 已不存在再删）；
- 失败处理按 §5 的升级规则执行，不重复询问。

采集完成后的顺序（每步产物都可复算）：

| 步 | 命令 | 说明 |
|---|---|---|
| 1 | `scripts/offline.py label --questions data/raw_qa/subsets/pool2000_v1.jsonl --generations .../pool2000/<model>/generations.jsonl --output data/labels/pool2000_<model>.proposals.jsonl` | 工具提案 |
| 2 | `scripts/draft_signoff_review.py --questions data/raw_qa/subsets/pool2000_v1.jsonl --run-root data/trajectories/bf16_pool2000 --prefix pool2000 --sheet reports/pool2000_draft_review.md` | 签核规则（脚本自带 400/400 回归自检，规则漂移即拒跑） |
| 3 | `scripts/finalize_reviewed_labels.py --input data/labels/pool2000_<model>.draft_review.jsonl --out data/labels/pool2000_<model>.reviewed.jsonl --reviewer ledstevenovo` | 人工签核后晋升 |
| 4 | `scripts/offline.py extract --questions ... --traces ... --labels ... --output data/features/pool2000_<model>.parquet` | 特征 |
| 5 | `scripts/judge_consistency_parallel.py --subset data/raw_qa/subsets/pool2000_v1.jsonl --trajectories data/trajectories/bf16_pool2000 --labels data/labels --prefix pool2000 --samples-per-model 0 --out reports/pool2000_label_consistency.json --workers 8` | 第二 judge 全覆盖（8 并发实测 373 条约数分钟；必须报告 coverage） |
| 6 | `scripts/offline.py evaluate --features <combined> --feature-sets entropy_raw relative_normalized --kinds lr mlp --bootstrap 1000 --axis model` | 迁移矩阵（另跑 `--axis dataset` 分层） |
| 7 | `scripts/stability_study.py --repeats 300`（两个 seed）→ `scripts/multiseed_transfer.py` | 稳定性与多种子 |
| 8 | 更新 `reports/paper_draft.md` §3 表格与 `reports/stage7_initial_observations.md` | 按预注册判据（§6.7）下结论 |

**预注册判据（先写死，不得事后调整）**：`rel+LR Dream→LLaDA` 的 95% CI 上界 <0.6 且 `ent+LR` 同方向 CI 下界 >0.7 → "Dream 源域方向性缺口"成立；否则按"未复现"报告。

## 2e. TRE R2（HotpotQA）协议冻结（2026-10-22 22:36，在任何 R2 轨迹出现之前）

R1 只覆盖 LLaDA × TriviaQA × 一个预算；原文表 1 有 2 模型 × 3 数据集 × 2 预算。R2 补 HotpotQA。

- **题单**：`data/tre_repro/questions/hotpotqa_eval800.jsonl`（800 题）+ `hotpotqa_smoke20.jsonl`（20 题工程验收），sha256 `37776b951f264ed0…` / `afc50dc495d02f31…`，manifest `data/tre_repro/questions_manifest_r2.json`。构建脚本 `scripts/build_tre_r2_questions.py`，`--check` 可复算。
- **抽样**：沿用 R1 的决策 B（从冻结池的 test 分区抽，不重下 raw）。`random.Random(20261021)`，按 question_id 排序取 820，前 800 评测、后 20 smoke → 两者构造上不相交。与池内 train/validation **簇级零重叠**（已断言）。
- **prompt 版本 v4**：HotpotQA 无上下文不可答，因此 prompt 是上下文接地式（`src.tre_repro.context_prompt`）：`Answer the question using only the context below.` + `Context:` + 段落 + `Question: … Answer:`。上下文按 `raw_id` 从 revision-pinned parquet 还原，渲染为 `Title: sentences`、段间空行，**整段文本连同 sha256 写进每条记录**。这是**新的 prompt 版本，不是对 v3 的修改**——R1 的两个题单文件仍逐字节不变（`--check` 已验证）。
- **契约扩展**：`TreQuestion` 新增 `context` 字段与 `prompt`/`prompt_style` 属性；加载器强制 `prompt` 可往返、`prompt_template_version` 与 `prompt_fingerprint` 一致。`score_tre_repro.py` 的 prompt 校验从「等于 question」改为「等于 question.prompt」。
- **可抄答案守卫改为只查 question**：HotpotQA 的答案本来就该出现在上下文里；只有答案出现在**问题**中才算坏题。实测 1654 题中 0 条命中。
- **长度预检**：LLaDA 含上下文均值 1475 token / 最大 3715；Dream 均值 1438 / 最大 3086；上下文 4096、生成 128 → 均无截断。
- **与 pool2000 的 115 题重叠**：两者都从同一个 HotpotQA test 池（1654 题）抽，`hotpotqa_eval800 ∩ pool2000_v1_new` = 115。已写入 manifest，不隐藏；两项研究协议不同（TRE 无检测器训练、主项目训练 LR/MLP），重叠只影响"同一批生成"的复用，不影响各自的指标口径。
- **配置**：LLaDA FP16，`L128/S64/B128`，seed 20261021，与 R1 完全一致（只换题单与 prompt 版本）。**Dream 走 BF16**：FP16/NF4 的原生 entropy 采样有 NaN 风险，`validate_precision` 会硬拒，这是既有保护，不为 R2 关闭。
- **judge 仍是 J2（moma deepseek-v4.1-flash）**。⚠️ 本机当前**没有可用凭据**（`MOMA_API_KEY` 未设；LongCat 的 key 调该端点返回 401）。轨迹可以先采，标签出不来。R1 的 800 条标签是此前判好并落盘的，不受影响。可选方案：用户提供 MOMA key，或改 J1（本地 Qwen3-8B）——后者属协议变更，须新开口径，禁止与 R1 的 J2 标签混用。
- **队列**：`scripts/run_gpu_queue.sh`（screen `gpuqueue`）等 pool2000 结束自动依次跑：R2 smoke20 → R2 800 → TriviaQA L64 → HotpotQA L64 → Dream HotpotQA BF16。

## 3. 需要 GPU 时才开卡的清单（备查）

- 主项目扩池 2000：`scripts/collect_llada.py` / `collect_dream.py`，题单 `data/raw_qa/subsets/pool2000_v1_new.jsonl`，输出 `data/trajectories/bf16_pool2000/`；**两模型同设备**（见 §2c），一键脚本 `scripts/run_pool2000_collect.sh`；
- TRE R2：每格 800 题，`--precision float16 --gen-length 128 --steps 64 --block-size 128`；
- DynHD 扩池：`scripts/dynhd_repro/collect_local.py`，`traces/<model>/.../raw/<new_run_id>`；
- 开卡后先跑一次设备/BF16 探针（`scripts/gpu_env_probe.py`），再开始采集。

## 4. 早上验收 3 步

```bash
cat /root/autodl-tmp/overnight_logs/driver.log        # 每步 rc / SKIP / FAIL
cat reports/overnight_$(date +%Y%m%d)_summary.md      # 队列自产摘要
.venv/bin/python scripts/morning_digest.py            # 跨产物一页汇总
ls results/stage7/main reports/main_project_stability.json
screen -ls                                            # 为空才可切卡
```

## 5. 失败升级规则（用户 2026-10-22 指令）

**某步最终失败时，不报告、直接修：**

1. 队列自身的重试（每步 3 次，5/20/45 秒退避）与降级（换小参数）先跑；
2. 失败后仍不成功 → 队列在下一轮看门狗周期再试（最多 4 轮）；
3. 仍失败 → 由会话 agent **立即派 subagent**：
   - 读该步日志 `overnight_logs/NN_*.log` 与 `driver.log` 中的 FAIL 行，
   - 定位根因（脚本 bug / 数据形状 / 依赖 / 资源），写出最小修复，
   - 修复后用同一命令重跑该步并核对产物，**不再重复询问用户**；
4. 修复必须留下痕迹：commit message 写明失败原因与修复内容；
5. 只有在需要用户输入（密钥、外部决策）时才升级到用户。

监控产物：
- `overnight_logs/monitor.log`：每 20 分钟一轮快照，出现 `ACTION_REQUIRED: failed steps: ...` 即表示需要修复；
- `overnight_logs/guard.log`：独立守护（每 5 分钟）记录会话重启与卡死重启动作。

## 6. 红线（无卡也不变）

- 权重、轨迹、结果目录不入 Git；标签必须 `human_reviewed=true` + `human:<reviewer>` 才进正式指标；
- 不用测试集调参；不伪造人工来源；不静默改精度/EOS 口径；
- 一个 label 文件只对应一个 judge / 一套口径。
