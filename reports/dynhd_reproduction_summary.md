# DynHD 复现交付汇总（方法级复现，缩小规模）

日期：2026-10-22。范围：`docs/DYNHD_REPRO_PLAN.md` 步骤 0–6 全部完成，证据见各 reports/dynhd_*.json。

## 1. 环境与上游核验

- 上游快照 36 文件 sha256 全一致，官方单元测试：Ran 7 tests in 7.445s - OK
- CPU 验收断言：22/22 通过
- 单题对齐：hook 逐值比对 LLaDA/Dream 各 5/5 与 5/5；观测无干扰均为真

## 2. pilot200 采集

| 模型 | 落盘 | 缺口 | 覆盖率 | 单题均值 | 加载 | 峰值显存 |
|---|---:|---:|---|---:|---:|---:|
| llada | 200 | 0 | complete | 2.2791s | 5.128s | 15.13 GiB |
| dream | 200 | 0 | complete | 2.102s | 4.38s | 14.47 GiB |

## 3. 标签与评测（reviewed，阈值主口径 0.5）

| 模型 | valid | 剔除 | 分区（train/val/test）| test AUROC（3 seed 均值 [min,max]）| 共同 test 集 |
|---|---:|---:|---|---|---|
| llada | 194 | 6 | 118/29/47 | 0.8824 [0.8730, 0.8911] | 44 题 |
| dream | 178 | 22 | 108/25/45 | 0.8093 [0.8029, 0.8149] | 44 题 |

## 4. 偏差与限制

- generation pipelines differ from the main project (DynHD samplers), so only per-pipeline in-domain results are reported
- Dream steps 64 / temperature 0.0 instead of the paper default 128 / 0.2 (main-table alignment)
- labels come from our reviewed rule sign-off, not GPT-4o-mini
- scale is pilot200 (test 47/45), so CIs are wide; expansion to 800-2000 is the next decision
- upstream passes generation_logits_hook_func=None which crashes the pinned Dream revision; the wrapper coerces it to the identity hook

- not a detector comparison across models
- pilot scale only
- test never used for tuning

## 5. 后续

- 扩池 800–2000（可选）：新题单 + 两模型采集 ~1h GPU + 人工复核 + 训练评测
- 与主项目主表并列报告时，只写「各自管线的域内结果」，不做检测器优劣归因

复现声明用词：**方法级复现（缩小规模、标签源不同）**。
