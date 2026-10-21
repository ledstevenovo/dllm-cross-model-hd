# 隔夜无卡运行汇总（生成于 2026-10-22 05:59）

- git HEAD: `dea597a Overnight no-GPU pass: transfer matrix, TRE analyses, stability study, DynHD delivery`
- 工作树: 干净
- 步骤标记: 12/12 完成，全部完成
- 队列结束标记: 是

## 1. 主项目迁移矩阵（pilot200 reviewed，dataset=all）

| 特征集 | 方向 | LR（95% CI） | MLP（95% CI） |
|---|---|---|---|
| relative_normalized | LLaDA 域内 | 0.887 [0.77,0.97] n=48 | 0.750 [0.60,0.88] n=48 |
| relative_normalized | Dream 域内 | 0.800 [0.59,0.97] n=45 | 0.782 [0.61,0.93] n=45 |
| relative_normalized | LLaDA → Dream | 0.779 [0.59,0.93] n=45 | 0.732 [0.54,0.88] n=45 |
| relative_normalized | Dream → LLaDA | 0.494 [0.30,0.70] n=48 | 0.502 [0.37,0.65] n=48 |
| entropy_raw | LLaDA 域内 | 0.848 [0.72,0.95] n=48 | 0.703 [0.55,0.85] n=48 |
| entropy_raw | Dream 域内 | 0.803 [0.60,0.97] n=45 | 0.803 [0.62,0.95] n=45 |
| entropy_raw | LLaDA → Dream | 0.820 [0.63,0.97] n=45 | 0.756 [0.60,0.90] n=45 |
| entropy_raw | Dream → LLaDA | 0.830 [0.69,0.94] n=48 | 0.579 [0.41,0.75] n=48 |

- 已知异常格 `relative_normalized+LR` Dream→LLaDA: AUROC 0.494 [0.30,0.70]；分层：hotpotqa n=20 AUROC 0.141；triviaqa n=28 AUROC 0.583（小样本层驱动，见 initial_observations）

## 2. 多种子稳健性（5 seeds，bootstrap 500）

| 方向 | rel+LR | ent+LR | rel+MLP | ent+MLP |
|---|---|---|---|---|
| LLaDA → LLaDA | 0.887 (σ 0.000) | 0.848 (σ 0.000) | 0.756 (σ 0.023) | 0.706 (σ 0.012) |
| LLaDA → Dream | 0.779 (σ 0.000) | 0.820 (σ 0.000) | 0.751 (σ 0.047) | 0.789 (σ 0.036) |
| Dream → LLaDA | 0.494 (σ 0.000) | 0.830 (σ 0.000) | 0.489 (σ 0.043) | 0.512 (σ 0.041) |
| Dream → Dream | 0.800 (σ 0.000) | 0.803 (σ 0.000) | 0.764 (σ 0.018) | 0.813 (σ 0.031) |

每一格为 5 个种子的 AUROC 均值（σ 为种子间标准差）。

## 3. 特征重要性（LR，置换 20 次，dataset=all）

| 格 | base AUROC | 置换 top-2（正=重要） | LOO top-1 |
|---|---|---|---|
| Dream → Dream entropy_raw | 0.803 | entropy_change (+0.008)；revealing_entropy (-0.006) | revealing_entropy (+0.012) |
| Dream → LLaDA entropy_raw | 0.830 | revealing_entropy (+0.044)；late_entropy (+0.040) | revealing_entropy (+0.027) |
| Dream → Dream relative_normalized | 0.800 | revealing_entropy_vocab_normalized (+0.018)；entropy_change_vocab_normalized (+0.017) | revealing_entropy_vocab_normalized (+0.019) |
| Dream → LLaDA relative_normalized | 0.494 | mean_uncertainty (+0.079)；revealing_entropy_vocab_normalized (+0.064) | mean_entropy_vocab_normalized (+0.031) |
| LLaDA → Dream entropy_raw | 0.820 | revealing_entropy (+0.439)；middle_entropy (+0.177) | revealing_entropy (+0.060) |
| LLaDA → LLaDA entropy_raw | 0.848 | revealing_entropy (+0.457)；middle_entropy (+0.283) | early_entropy (-0.000) |
| LLaDA → Dream relative_normalized | 0.779 | revealing_entropy_vocab_normalized (+0.025)；revealed_fraction (+0.000) | mean_entropy_vocab_normalized (+0.005) |
| LLaDA → LLaDA relative_normalized | 0.887 | reveal_progress_entropy_vocab_normalized (+0.046)；revealing_entropy_vocab_normalized (+0.025) | mean_reveal_progress (+0.023) |


## 4. 稳定性重采样（300 repeats，簇级重采样）

| 格 | AUROC 均值（σ） | 5–95% 分位 | P(>0.5/>0.7/>0.8) | 有效/请求 |
|---|---|---|---|---|
| Dream → Dream entropy_raw LR | 0.817 (σ 0.086) | 0.657–0.945 | 1.00/0.91/0.61 | 300/300 |
| Dream → LLaDA entropy_raw LR | 0.838 (σ 0.079) | 0.698–0.947 | 1.00/0.95/0.70 | 300/300 |
| LLaDA → Dream entropy_raw LR | 0.804 (σ 0.087) | 0.658–0.951 | 1.00/0.88/0.53 | 300/300 |
| LLaDA → LLaDA entropy_raw LR | 0.868 (σ 0.067) | 0.742–0.964 | 1.00/0.99/0.85 | 300/300 |
| Dream → Dream entropy_raw MLP | 0.779 (σ 0.107) | 0.600–0.929 | 0.98/0.79/0.48 | 300/300 |
| Dream → LLaDA entropy_raw MLP | 0.555 (σ 0.150) | 0.303–0.796 | 0.63/0.18/0.05 | 300/300 |
| LLaDA → Dream entropy_raw MLP | 0.772 (σ 0.088) | 0.623–0.908 | 1.00/0.79/0.38 | 300/300 |
| LLaDA → LLaDA entropy_raw MLP | 0.708 (σ 0.087) | 0.561–0.861 | 0.99/0.51/0.14 | 300/300 |
| Dream → Dream relative_normalized LR | 0.793 (σ 0.089) | 0.640–0.933 | 1.00/0.84/0.51 | 300/300 |
| Dream → LLaDA relative_normalized LR | 0.514 (σ 0.136) | 0.301–0.757 | 0.55/0.08/0.02 | 300/300 |
| LLaDA → Dream relative_normalized LR | 0.778 (σ 0.098) | 0.617–0.931 | 0.98/0.81/0.44 | 300/300 |
| LLaDA → LLaDA relative_normalized LR | 0.874 (σ 0.056) | 0.769–0.953 | 1.00/0.99/0.89 | 300/300 |
| Dream → Dream relative_normalized MLP | 0.770 (σ 0.090) | 0.619–0.907 | 1.00/0.81/0.38 | 300/300 |
| Dream → LLaDA relative_normalized MLP | 0.514 (σ 0.156) | 0.283–0.773 | 0.50/0.14/0.03 | 300/300 |
| LLaDA → Dream relative_normalized MLP | 0.752 (σ 0.130) | 0.494–0.918 | 0.94/0.72/0.39 | 300/300 |
| LLaDA → LLaDA relative_normalized MLP | 0.769 (σ 0.087) | 0.618–0.908 | 1.00/0.80/0.37 | 300/300 |

- **异常格 `relative_normalized+LR` Dream→LLaDA 在重采样下**：均值 0.514，P(>0.5)=0.55（即 P(≤0.5)=0.45），5–95% 分位 0.301–0.757
分位是重采样离散度，不是总体置信区间；阈值未在稳定性循环中重新调优。

## 5. TRE R1（judge 800 题：507 正 / 293 负）

| 分数族（Top5） | AUROC（95% CI） |
|---|---|
| tre_length_normalized | 0.8370 [0.807,0.863] |
| time_hard_last_30 | 0.8341 [0.805,0.863] |
| time_hard_last_30_average | 0.8341 [0.805,0.863] |
| revealing_entropy | 0.8314 [0.801,0.859] |
| tre_effective | 0.8270 [0.797,0.855] |

- 主口径 `tre`: AUROC 0.7834
| 置换检验 | 结果 |
|---|---|
| 置换检验 tre | p=1.00e-04（null mean 0.500） |
| 置换检验 tre_effective | p=1.00e-04（null mean 0.500） |
| 置换检验 tre_length_normalized | p=1.00e-04（null mean 0.500） |


## 6. DynHD 复现交付

- CPU 验收断言: 22/22
- LLaDA test AUROC（3 seeds 均值）: 0.8824
- Dream test AUROC（3 seeds 均值）: 0.8093
- 共同测试集 n=44: LLaDA 0.8757 / Dream 0.8180
- 记录的偏差 5 条，限制 3 条（见 reports/dynhd_reproduction_summary.md）

## 7. 注意事项

- 单次矩阵不能用于检测器优劣结论；稳定性分位仅为重采样离散度。
- test 层每方向仅 18–48 条，跨模型多数格 CI 覆盖 0.5；结论以「是否出现稳定迁移缺口」为准。
- `data/labels/*.reviewed.jsonl` 为 gitignore 文件，只存在于工作区与夜间备份包。

