# 无卡通宵结果（20261022，用时 66 分钟）

- 备份：`/root/autodl-tmp/backup_20261022`（102M）
- 未完成步骤： 无

## 标签与特征
{"input": "data/labels/pilot200_llada.draft_review.jsonl", "out": "data/labels/pilot200_llada.reviewed.jsonl", "rows": 200, "labels": {"incorrect": 142, "correct": 53, "format_failure": 5}, "reviewer": "ledstevenovo"}
{"input": "data/labels/smoke_dream.assistant_review.jsonl", "out": "data/labels/smoke_dream.reviewed.jsonl", "rows": 20, "labels": {"incorrect": 12, "format_failure": 4, "correct": 4}, "reviewer": "ledstevenovo"}
{"input": "data/labels/pilot200_dream.draft_review.jsonl", "out": "data/labels/pilot200_dream.reviewed.jsonl", "rows": 200, "labels": {"format_failure": 22, "incorrect": 124, "correct": 54}, "reviewer": "ledstevenovo"}
llada 200 {'incorrect': 142, 'correct': 53, 'format_failure': 5} eligible= 195
dream 200 {'incorrect': 124, 'correct': 54, 'format_failure': 22} eligible= 178
combined rows 400 models 2

## 阶段 7 迁移矩阵
Offline evaluation rows: 48 output: results/stage7/main
Offline evaluation rows: 24 output: results/stage7/ablations

## TRE 离线分析（主口径 tre 不变）
n=800 positive=507 | 29 scores
  tre_length_normalized              AUROC 0.8370 [0.8070, 0.8629] AUPRC 0.8907
  time_hard_last_30                  AUROC 0.8341 [0.8053, 0.8634] AUPRC 0.8701
  time_hard_last_30_average          AUROC 0.8341 [0.8053, 0.8634] AUPRC 0.8701
  revealing_entropy                  AUROC 0.8314 [0.8013, 0.8595] AUPRC 0.8874
  tre_effective                      AUROC 0.8270 [0.7972, 0.8553] AUPRC 0.8685
  max_entropy                        AUROC 0.8046 [0.7752, 0.8344] AUPRC 0.8754
  tre                                AUROC 0.7834 [0.7492, 0.8172] AUPRC 0.8275
  tre_vocab_normalized               AUROC 0.7834 [0.7492, 0.8172] AUPRC 0.8275
  space_revealing                    AUROC 0.7834 [0.7492, 0.8172] AUPRC 0.8275
  time_linear                        AUROC 0.7834 [0.7492, 0.8172] AUPRC 0.8275
  time_linear_average                AUROC 0.7834 [0.7492, 0.8172] AUPRC 0.8275
  late_entropy                       AUROC 0.7796 [0.7442, 0.8107] AUPRC 0.8520
wrote /root/autodl-tmp/dllm-cross-model-hd/reports/tre_repro/offline_analysis.json and /root/autodl-tmp/dllm-cross-model-hd/reports/tre_repro/offline_analysis.csv

## TRE 置换显著性
tre                        AUROC 0.7834 | null mean 0.4997 p95 0.5351 | p = 9.999e-05
tre_effective              AUROC 0.8270 | null mean 0.5001 p95 0.5351 | p = 9.999e-05
tre_length_normalized      AUROC 0.8370 | null mean 0.4999 p95 0.5347 | p = 9.999e-05
wrote /root/autodl-tmp/dllm-cross-model-hd/reports/tre_repro/permutation_test.json

## 多种子稳健性
  GSAI-ML/LLaDA-8B-Instr->GSAI-ML/LLaDA-8B-Instr relative_normalized  lr  AUROC 0.8867 [0.8867,0.8867] std 0.0000
  Dream-org/Dream-v0-Ins->GSAI-ML/LLaDA-8B-Instr entropy_raw          lr  AUROC 0.8854 [0.8854,0.8854] std 0.0000
  Dream-org/Dream-v0-Ins->GSAI-ML/LLaDA-8B-Instr entropy_raw          lr  AUROC 0.8750 [0.8750,0.8750] std 0.0000
  GSAI-ML/LLaDA-8B-Instr->GSAI-ML/LLaDA-8B-Instr entropy_raw          lr  AUROC 0.8646 [0.8646,0.8646] std 0.0000
  Dream-org/Dream-v0-Ins->Dream-org/Dream-v0-Ins entropy_raw          mlp AUROC 0.8494 [0.8059,0.9294] std 0.0508
  GSAI-ML/LLaDA-8B-Instr->GSAI-ML/LLaDA-8B-Instr entropy_raw          lr  AUROC 0.8477 [0.8477,0.8477] std 0.0000
  GSAI-ML/LLaDA-8B-Instr->GSAI-ML/LLaDA-8B-Instr entropy_raw          mlp AUROC 0.8469 [0.7812,0.8906] std 0.0404
wrote /root/autodl-tmp/dllm-cross-model-hd/reports/main_project_multiseed.json and /root/autodl-tmp/dllm-cross-model-hd/reports/main_project_multiseed.csv

## 特征重要性
Dream-v0-Instr -> LLaDA-8B-Instr relative_normalized  AUROC 0.4941 | top drop: mean_uncertainty
LLaDA-8B-Instr -> Dream-v0-Instr entropy_raw          AUROC 0.8197 | top drop: revealing_entropy
LLaDA-8B-Instr -> LLaDA-8B-Instr entropy_raw          AUROC 0.8477 | top drop: revealing_entropy
LLaDA-8B-Instr -> Dream-v0-Instr relative_normalized  AUROC 0.7788 | top drop: revealing_entropy_vocab_normalized
LLaDA-8B-Instr -> LLaDA-8B-Instr relative_normalized  AUROC 0.8867 | top drop: reveal_progress_entropy_vocab_normalized
wrote /root/autodl-tmp/dllm-cross-model-hd/reports/main_project_importance.json and /root/autodl-tmp/dllm-cross-model-hd/reports/main_project_importance.csv

## 稳定性重采样
[6 cells] Dream-v0-Ins relative_normalized  lr  300 repeats | 23.6 min this run
[8 cells] Dream-v0-Ins relative_normalized  mlp 300 repeats | 33.0 min this run
[10 cells] LLaDA-8B-Ins entropy_raw          lr  300 repeats | 39.6 min this run
[12 cells] LLaDA-8B-Ins entropy_raw          mlp 300 repeats | 50.0 min this run
[14 cells] LLaDA-8B-Ins relative_normalized  lr  300 repeats | 56.7 min this run
[16 cells] LLaDA-8B-Ins relative_normalized  mlp 300 repeats | 66.6 min this run
cross-model cells: 8 | best 0.8375 (Dream-v0-Instruct-7B->LLaDA-8B-Instruct), worst 0.5136
wrote /root/autodl-tmp/dllm-cross-model-hd/reports/main_project_stability.json and /root/autodl-tmp/dllm-cross-model-hd/reports/main_project_stability.csv

## DynHD 交付
- reports/dynhd_reproduction_summary.md / .json

## 早上验收
1. cat /root/autodl-tmp/overnight_logs/driver.log
2. cat reports/overnight_20261022_summary.md
3. screen -ls 为空后再切无卡
