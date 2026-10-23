# 主表复现性核对（2026-10-23 14:20）

## 做了什么

从 `results/pool2000/features_combined.parquet` **重新运行** `evaluate_transfer`，
与已发布的 `results/pool2000/main/transfer_matrix.csv` 逐格比对。

## 结果

| 方向 | 特征集 | 重跑 | 已发布 | 一致 |
|---|---|---:|---:|---|
| Dream→Dream | entropy_raw | 0.8533 | 0.8533 | ✅ |
| Dream→LLaDA | entropy_raw | 0.6711 | 0.6711 | ✅ |
| Dream→Dream | relative_normalized | 0.8713 | 0.8713 | ✅ |
| Dream→LLaDA | relative_normalized | **0.7519** | **0.7519** | ✅ |
| LLaDA→Dream | entropy_raw | 0.8538 | 0.8538 | ✅ |
| LLaDA→LLaDA | entropy_raw | 0.7991 | 0.7991 | ✅ |
| LLaDA→Dream | relative_normalized | 0.8654 | 0.8654 | ✅ |
| LLaDA→LLaDA | relative_normalized | 0.8126 | 0.8126 | ✅ |

**8/8 逐位一致**（容差 1e-9）。bootstrap 次数不同（200 vs 1000）只影响 CI，不影响点估计。

## 为什么这条值得单独记录

这份表的**核心数字**（`rel+LR Dream→LLaDA = 0.752`）是推翻 pilot200 结论的依据，
也是整个扩池实验的判决基础。它必须能被独立重算。

本次核对证明：

1. 结果**不依赖**已保存的 predictions/模型文件，从原始特征表即可重算；
2. 点估计**完全确定**（同 seed 同数据 → 同数字），不是随机波动；
3. 前面那条"限制回 pilot200 的 200 题可逐位复现旧值"的检验，与本条一起构成双向可复现性：
   **旧值能从新表复现，新值能从原始特征复现**。

## 结论

主表可复算，判决基础稳固。
