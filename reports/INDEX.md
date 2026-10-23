# 结论文档索引（2026-10-23）

项目里已有 47 份报告，跨越多次结论变更与撤回。本页是**单一入口**：每条结论、当前状态、
证据文件、以及是否被推翻。

## 一、当前有效的结论

| # | 结论 | 关键数字 | 证据 |
|---|---|---|---|
| 1 | 域内正确性检测稳定可用（2000 题） | AUROC 0.799–0.871，8/8 格 p ≤ 1e-4 | `paper_draft.md` §3.1、`results/pool2000/main/` |
| 2 | 跨模型迁移普遍成立但中度衰减 | 16/16 格 > 0.5（0.60–0.87），全部 p ≤ 4e-4 | `paper_draft.md` §3.2、`pool2000_permutation.json` |
| 3 | 迁移**方向性不对称**，但无断裂 | LLaDA→Dream 代价 +0.007；Dream→LLaDA +0.112 | `transfer_asymmetry.md` |
| 4 | 稳定性：16/16 格重采样 P(>0.5) ≥ 0.88 | 双种子 300 次/格 | `pool2000_stability_two_seeds.json` |
| 5 | 标签质量：第二 judge 全覆盖一致率 0.933、κ 0.840 | 1000/1000 | `pool2000_label_consistency.json` |
| 6 | 主结论对标签来源稳健（固定同样本只换标签） | 排序完全一致 | `label_source_robustness.md` |
| 7 | **TRE 在四个格子上都显著** | 0.70–0.80，全部 p = 1e-4 | `tre_repro/four_cells.md` |
| 8 | 协议匹配的两格偏差仅 −3.9 / −4.4 pp（两模型一致） | 偏差是系统性的 | `tre_repro/four_cells.md` |
| 9 | **TRE vs 训练检测器取决于数据量** | TriviaQA 检测器 +6.5/+9.5；HotpotQA TRE +2.6 | `tre_repro/tre_vs_detectors.md` |
| 10 | HotpotQA 反转的原因是**小样本+高维** | 短答层仅 32 正类，检测器 0.40–0.41 | 同上（分层检验） |
| 11 | R2 的标签分歧已三方裁决 | 126/142 站 judge，仲裁后 0.706 | `tre_repro/r2_adjudication_report.md` |
| 12 | DynHD 方法级复现 | 22/22 断言，test 0.88/0.81 | `dynhd_reproduction_summary.md` |
| 13 | **TRE 的跨模型"迁移"：AUROC 迁移，阈值不迁移** | 两方向 AUROC 等于域内值；阈值准确率 0.38 / 0.63 | `tre_repro/tre_cross_model_transfer.md` |
| 14 | **复述不是 HotpotQA 差距的原因**（已证伪） | 复述率差 400 倍，同 judge 下 AUROC 只差 0.026 | `tre_repro/recitation_hypothesis_verdict.md` |
| 15 | **HotpotQA 标签跨 judge 不稳定** | 同一批轨迹 0.682（deepseek）vs 0.745（LongCat） | `tre_repro/r2_same_judge_result.md` |

## 二、已撤回的结论（保留记录，勿再引用）

| 旧结论 | 撤回原因 | 更正文件 |
|---|---|---|
| **"Dream 源域方向性缺口，三个组合停在随机"** | 预注册判据未通过；扩池后 16/16 格全部显著 | `pool2000_verdict.md`、`pool2000_learning_curve.md` |
| "缺口是尺度对齐问题，对齐可修复 0.494→0.850" | 前提消失：不对齐本就 0.752；对齐后仅 0.764，且部分格变差 | `pool2000_supplementary_checks.md` |
| "进度/长度特征不可跨模型（会崩到 0.47）" | 扩池后方向反转：进度类 +0.21~+0.29 | `pool2000_featureset_ablation.md` |
| **"单特征 `late_entropy` 优于所有组合"** | 只在 1/4 方向领先 0.014（CI 重叠），其余三方向落后 0.04–0.05 | `late_entropy_correction.md` |
| "R2 对标签口径敏感、0.542 接近随机" | 0.542 来自不适用的规则标注器；三方裁决 126/142 站 judge | `tre_repro/r2_adjudication_report.md` |
| "`ent+MLP` 的失败另有机制（开放问题）" | 扩池后不失败（0.680，p ≤ 1e-4） | `pool2000_verdict.md` |
| "R2 比原文低 17.4 pp" | 那是 deepseek 标签；同 judge（LongCat）下是 **−11.1**，差额主要是 judge 效应 | `tre_repro/r2_same_judge_result.md` |
| "LLaDA 有复述倾向（模型缺陷）" | 只在被给了上下文时复述；主项目裸问题 prompt 下 0/500 撞预算 | `tre_repro/recitation_hypothesis.md` |

## 三、方法学教训（本项目最有借鉴价值的部分）

### 3.1 五项检验全部没能发现问题

pilot200 的"方向性缺口"通过了：

1. bootstrap CI（1000 次，簇级）
2. 双种子簇级重采样（600 次/格）
3. 簇级置换检验（10000 次）
4. 5 个随机种子
5. 一次独立的机制诊断（尺度对齐，0.494→0.850）

**全部没能发现真正的问题：测试集只有 48 条。**

| 检验 | 为什么不够 |
|---|---|
| bootstrap CI | CI 宽 [0.29, 0.71] 是警告；它同时容纳 0.5 与 0.75 |
| 簇级重采样 | 在固定 48 条上重采，测样本内变异，不是抽样误差 |
| 置换检验 | p=0.53 只说"这 48 条排序不像有信号" |
| 多种子 | 只反映训练随机性，数据不变结论不变 |
| 机制诊断 | 可以为一个**噪声值**编出可信的机制故事 |

**唯一有效的检验是换一批样本重测。**

### 3.2 同类错误的三个实例

本项目在 24 小时内犯了同一个错误三次：

1. **pilot200 缺口**：把 48 题分布的极端值当作机制；
2. **`late_entropy` 最优**：把一格的点估计最大值当作规律（四方向对照后撤回）；
3. **标签来源比较**：第一次用"不同样本"比"不同标签"，把抽样差异当成标签效应
   （固定样本后重做，见 `label_source_robustness.md`）。

共同模式：**在单个条件下取极值，然后推广**。防范方法是先问"这个比较的样本是否相同、
方向是否一致"。

## 四、复现路径

```bash
# 域内/跨模型矩阵（2000 题）
.venv/bin/python scripts/offline.py evaluate \
  --features results/pool2000/features_combined.parquet \
  --output results/pool2000/main --bootstrap 1000 --axis model

# 预注册判据
.venv/bin/python scripts/pool2000_verdict.py \
  --matrix results/pool2000/main/transfer_matrix.csv --out reports/pool2000_verdict.json

# 学习曲线（解释小样本假象）
.venv/bin/python scripts/pool2000_learning_curve.py

# 簇级置换
.venv/bin/python scripts/main_permutation.py \
  --predictions results/pool2000/main/predictions.csv --permutations 10000

# TRE vs 检测器
.venv/bin/python scripts/tre_vs_detectors.py --run <run> --questions <q> --judgments <j> --out <o>

# TRE 打分
.venv/bin/python scripts/score_tre_repro.py --run <run> --questions <q> \
  --judgments <j> --output <o> --judge-prompt data/tre_repro/judge_prompt_v3.txt
```

## 五、进行中与未完成

| 任务 | 状态 | 预计 |
|---|---|---|
| Dream × HotpotQA 采集 | **进行中**（147/800，12:15） | 15:13 |
| 其判分 + 打分 + 检测器对比 | 已排入 screen，自动接续 | ~16:00 |
| HotpotQA L64 | 脚本就绪，未跑 | ~4.5 h GPU |
| TRE 与检测器在 2000 题上的受控对比 | 需 128 token 重采 | ~2.5 h GPU |
| HotpotQA 标签人工抽查 | 未做 | 人工 |
| **裸问题 HotpotQA 对照** | **判分中**（500/800，18:03） | ~18:20 |
