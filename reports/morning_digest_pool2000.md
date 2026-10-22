# 隔夜无卡运行汇总（生成于 2026-10-23 05:21）

- git HEAD: `9e4e793 Record the R2 design and pre-compute the risk that its positive rate is tiny`
- 工作树: 有未提交改动（见 git status）
- 步骤标记: 12/12 完成，全部完成
- 队列结束标记: 是

## 1. 迁移矩阵（2000 题/模型（pool2000 reviewed，dataset=all））

| 特征集 | 方向 | LR（95% CI） | MLP（95% CI） |
|---|---|---|---|
| relative_normalized | LLaDA 域内 | 0.813 [0.77,0.85] n=491 | 0.773 [0.73,0.82] n=491 |
| relative_normalized | Dream 域内 | 0.871 [0.84,0.91] n=449 | 0.794 [0.75,0.84] n=449 |
| relative_normalized | LLaDA → Dream | 0.865 [0.83,0.90] n=449 | 0.739 [0.69,0.78] n=449 |
| relative_normalized | Dream → LLaDA | 0.752 [0.70,0.80] n=491 | 0.600 [0.55,0.65] n=491 |
| entropy_raw | LLaDA 域内 | 0.799 [0.76,0.84] n=491 | 0.765 [0.72,0.81] n=491 |
| entropy_raw | Dream 域内 | 0.853 [0.81,0.89] n=449 | 0.807 [0.76,0.85] n=449 |
| entropy_raw | LLaDA → Dream | 0.854 [0.82,0.89] n=449 | 0.839 [0.80,0.88] n=449 |
| entropy_raw | Dream → LLaDA | 0.671 [0.62,0.72] n=491 | 0.680 [0.63,0.73] n=491 |

- `relative_normalized+LR` Dream→LLaDA: AUROC 0.752 [0.70,0.80]；分层：hotpotqa n=238 AUROC 0.698；triviaqa n=253 AUROC 0.769。预注册判据：见 reports/pool2000_verdict.json

## 2. 多种子稳健性（5 seeds，bootstrap 300）

| 方向 | rel+LR | ent+LR | rel+MLP | ent+MLP |
|---|---|---|---|---|
| LLaDA → LLaDA | 0.813 (σ 0.000) | 0.799 (σ 0.000) | 0.783 (σ 0.008) | 0.768 (σ 0.010) |
| LLaDA → Dream | 0.865 (σ 0.000) | 0.854 (σ 0.000) | 0.784 (σ 0.041) | 0.836 (σ 0.005) |
| Dream → LLaDA | 0.752 (σ 0.000) | 0.671 (σ 0.000) | 0.686 (σ 0.051) | 0.590 (σ 0.056) |
| Dream → Dream | 0.871 (σ 0.000) | 0.853 (σ 0.000) | 0.827 (σ 0.020) | 0.818 (σ 0.008) |

每一格为 5 个种子的 AUROC 均值（σ 为种子间标准差）。

## 3. 特征重要性（LR，置换 20 次，dataset=all）

| 格 | base AUROC | 置换 top-2（正=重要） | LOO top-1 |
|---|---|---|---|
| Dream → Dream entropy_raw | 0.853 | revealing_entropy (+0.370)；middle_entropy (+0.078) | revealing_entropy (+0.011) |
| Dream → LLaDA entropy_raw | 0.671 | revealing_entropy (+0.259)；middle_entropy (+0.145) | revealing_entropy (+0.058) |
| Dream → Dream relative_normalized | 0.871 | revealing_entropy_vocab_normalized (+0.335)；mean_uncertainty (+0.114) | revealing_entropy_vocab_normalized (+0.010) |
| Dream → LLaDA relative_normalized | 0.752 | revealing_entropy_vocab_normalized (+0.224)；mean_uncertainty (+0.171) | reveal_progress_entropy_vocab_normalized (+0.032) |
| LLaDA → Dream entropy_raw | 0.854 | revealing_entropy (+0.429)；early_entropy (+0.011) | revealing_entropy (+0.017) |
| LLaDA → LLaDA entropy_raw | 0.799 | revealing_entropy (+0.341)；entropy_change (+0.050) | revealing_entropy (+0.030) |
| LLaDA → Dream relative_normalized | 0.865 | revealing_entropy_vocab_normalized (+0.068)；early_entropy_vocab_normalized (+0.067) | reveal_progress_entropy_vocab_normalized (+0.010) |
| LLaDA → LLaDA relative_normalized | 0.813 | early_entropy_vocab_normalized (+0.088)；reveal_progress_entropy_vocab_normalized (+0.087) | reveal_progress_entropy_vocab_normalized (+0.013) |


## 4. 稳定性重采样（300（两种子合并） repeats，簇级重采样）

| 格 | AUROC 均值（σ） | 5–95% 分位 | P(>0.5/>0.7) | 有效/请求 |
|---|---|---|---|---|
| Dream → Dream entropy_raw LR | 0.854 (σ 0.018) | 0.825–0.881 | 1.00/1.00/0.99 | 300/300 |
| Dream → LLaDA entropy_raw LR | 0.697 (σ 0.057) | 0.594–0.784 | 0.99/0.51/0.01 | 300/300 |
| LLaDA → Dream entropy_raw LR | 0.855 (σ 0.019) | 0.825–0.886 | 1.00/1.00/1.00 | 300/300 |
| LLaDA → LLaDA entropy_raw LR | 0.797 (σ 0.024) | 0.760–0.836 | 1.00/1.00/0.53 | 300/300 |
| Dream → Dream entropy_raw MLP | 0.804 (σ 0.029) | 0.754–0.844 | 1.00/1.00/0.53 | 300/300 |
| Dream → LLaDA entropy_raw MLP | 0.578 (σ 0.067) | 0.470–0.687 | 0.88/0.03/0.00 | 300/300 |
| LLaDA → Dream entropy_raw MLP | 0.769 (σ 0.111) | 0.543–0.851 | 0.99/0.95/0.63 | 300/300 |
| LLaDA → LLaDA entropy_raw MLP | 0.757 (σ 0.029) | 0.711–0.804 | 1.00/0.98/0.11 | 300/300 |
| Dream → Dream relative_normalized LR | 0.869 (σ 0.019) | 0.834–0.896 | 1.00/1.00/1.00 | 300/300 |
| Dream → LLaDA relative_normalized LR | 0.758 (σ 0.039) | 0.694–0.814 | 1.00/0.93/0.15 | 300/300 |
| LLaDA → Dream relative_normalized LR | 0.863 (σ 0.019) | 0.829–0.889 | 1.00/1.00/0.99 | 300/300 |
| LLaDA → LLaDA relative_normalized LR | 0.813 (σ 0.023) | 0.775–0.849 | 1.00/1.00/0.68 | 300/300 |
| Dream → Dream relative_normalized MLP | 0.811 (σ 0.029) | 0.764–0.860 | 1.00/1.00/0.63 | 300/300 |
| Dream → LLaDA relative_normalized MLP | 0.664 (σ 0.055) | 0.562–0.738 | 0.99/0.31/0.01 | 300/300 |
| LLaDA → Dream relative_normalized MLP | 0.776 (σ 0.081) | 0.618–0.843 | 0.99/0.91/0.41 | 300/300 |
| LLaDA → LLaDA relative_normalized MLP | 0.754 (σ 0.030) | 0.710–0.801 | 1.00/0.96/0.06 | 300/300 |

- **`relative_normalized+LR` Dream→LLaDA 在重采样下**：均值 0.758，P(>0.5)=1.00，P(>0.7)=0.93，5–95% 分位 0.694–0.814
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

