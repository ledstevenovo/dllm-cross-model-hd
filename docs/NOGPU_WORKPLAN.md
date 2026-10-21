# 无卡模式工作清单（2026-10-22 起）

本文件是"不需要 GPU 就能一直推进"的执行清单，脚本为 `scripts/overnight_nogpu.sh`（可重入，`DRY_RUN=1` 只打印计划）。
GPU 只在**采集/重采**时需要；此清单中的每一步都不占用 GPU，可在无卡模式或本地完成。

## 0. 为什么可以无卡推进

- 权重缓存与推理环境已在持久盘（`/root/autodl-tmp/hf-cache`、`.venv-llada`、`.venv-dream`、`.venv-dynhd`），切无卡不删盘即可复用；
- 已有轨迹已落盘：TRE 800 条、主项目 BF16 pilot200 ×2、smoke20 ×2、DynHD pilot200 ×2；
- 训练/评测/标注/统计/报告全部是 CPU 或 API（judge）任务。

**唯一约束**：切无卡会重启容器，正在跑的进程会被杀。切换前 `screen -ls` 必须为空。

## 1. 三项待办（本次采纳口径后）

| # | 任务 | 预计 | 命令 / 产物 |
|---|---|---|---|
| 1 | 备份打包 + 独立复算 | 打包 ~5 分钟 / 复算 ~10 分钟 | `scripts/overnight_nogpu.sh` 步骤 1；产物 `/root/autodl-tmp/backup_<date>/{tre_repro,main_project,dynhd_repro}.tar.gz` + `MANIFEST.sha256` |
| 2 | 主项目签核 → 特征 → 阶段 7 | 1–1.5 小时 | 步骤 2–3；产物 `data/labels/*.reviewed.jsonl`、`data/features/pilot200_*.parquet`、`results/stage7/{main,ablations}` |
| 3 | DynHD 步骤 7 交付汇总 | 30–40 分钟 | 步骤 4；产物 `reports/dynhd_reproduction_summary.{md,json}` |

一键全跑（后台）：`screen -dmS overnight bash scripts/overnight_nogpu.sh`

## 2. 之后的无卡任务队列

| 优先级 | 任务 | 需要 GPU？ | 说明 |
|---|---|---|---|
| 1 | **阶段 7 结果解读与报告** | 否 | 看迁移缺口是否稳定，决定是否扩池（主方案 §8 决策门） |
| 2 | **标签质量证据** | 否（第二 judge 需 API） | ≥50 题人工抽查；第二 judge 100 题一致性（补充，不改主表） |
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
cat /root/autodl-tmp/overnight_logs/driver.log     # 每步 rc
ls results/stage7/main && cat reports/overnight_*_summary.md
screen -ls                                          # 为空才可切无卡
```

## 5. 红线（无卡也不变）

- 权重、轨迹、结果目录不入 Git；标签必须 `human_reviewed=true` + `human:<reviewer>` 才进正式指标；
- 不用测试集调参；不伪造人工来源；不静默改精度/EOS 口径；
- 一个 label 文件只对应一个 judge / 一套口径。
