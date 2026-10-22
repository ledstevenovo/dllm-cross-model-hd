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
| 3 | **DynHD 可选扩池准备** | 题单冻结无卡，采集需卡 | `pick_longest` / 题单冻结 / split 脚本都已就绪 |
| 4 | **TRE R2 准备** | 题单/prompt 冻结无卡，采集需卡 | HotpotQA / CSQA 格式与 prompt 需先冻结并登记 |
| 5 | **论文级整理** | 否 | 把 TRE R1（78.34%，CI 74.92–81.72）、阶段 7 矩阵、DynHD 域内结果整理成可发表报告 |
| 6 | **备份策略固化** | 否 | 每次大采集后重新打包并核对 `MANIFEST.sha256` |

## 3. 需要 GPU 时才开卡的清单（备查）

- 主项目扩池 800–2000：`scripts/collect_llada.py` / `collect_dream.py`，新题单与新输出目录；
- TRE R2：每格 800 题，`--precision float16 --gen-length 128 --steps 64 --block-size 128`；
- DynHD 扩池：`scripts/dynhd_repro/collect_local.py`，`traces/<model>/.../raw/<new_run_id>`；
- 开卡后先跑一次设备/BF16 探针（`docs/VGPU_32GB_完整实验方案.md` 第 3 节），再开始采集。

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
