# dLLM 跨模型幻觉检测：离线实验工具

本项目已具备数据准备、统一轨迹格式、TRE/统计特征、LR/小型 MLP、双向迁移与消融评测的 CPU 流程。**尚未运行真实 LLaDA/Dream，也没有真实幻觉检测结论。**

## 环境

Python 3.12/3.13；使用 uv + 项目内 `.venv`。无需 Conda，无 torch/CUDA 依赖。

```powershell
uv sync --locked
uv run pytest
uv run python scripts/audit_dataset.py --output reports/dataset_audit.json
uv run python scripts/audit_near_duplicates.py
```

当前机器已安装并锁定 CPU 依赖。Windows Store Python 在受限沙箱内无法启动现有 venv；本次通过已批准的外部执行验证，不代表所有机器都需要提权。详见 docs/ENVIRONMENT.md。

## 数据

```powershell
uv run python scripts/download_raw.py
uv run python scripts/build_dataset.py
uv run python scripts/build_pilot.py
uv run python scripts/verify_rebuild.py
```

数据来源 revision 和 SHA256 固定在 configs/datasets/sources.lock.json。处理数据及清单保留在 data/raw_qa 和 data/manifests。近重复聚簇已更新原始划分；使用最新 manifest，勿混用 DeepSeek 旧版 split。

- smoke20：工程专用，独立于研究数据。
- small200：保留的纯 test 子集，不能用来调参或训练。
- pilot200：120 train / 30 validation / 50 test，两模型共用这一组问题；小样本不保证两种标签都充足。

字段和限制见 docs/DATASET.md；标签规则和人工审核要求见 docs/LABEL_PROTOCOL.md。

## 不需要 GPU 的完整演练

```powershell
uv run python scripts/offline.py demo --output results/synthetic_demo --bootstrap 100
```

生成 400 条**模拟**轨迹，经过 NPZ 保存读取、特征 parquet、10 组特征 × LR/MLP、双向迁移矩阵、TRE 基线、置信区间和绘图。所有模拟产物均在 results/ 下，不混入真实数据。生成器人为植入的信号仅用来验证代码。

## 有真实轨迹之后

```powershell
uv run python scripts/offline.py label --generations data/generations/run.jsonl --output data/labels/proposals.jsonl
# 人工审核生成回答，保存 label_source 和 human_reviewed，再做以下步骤
uv run python scripts/offline.py extract --traces data/trajectories/run --labels data/labels/reviewed.jsonl --output data/features/run.parquet
uv run python scripts/offline.py evaluate --features data/features/run.parquet --output results/main --feature-sets entropy_raw relative_normalized --bootstrap 1000
```

`evaluate --help` 查看特征集、LR/MLP、随机种子、无 scaler 对照和独立跨数据集轴（--axis dataset）。更改长度/步数/block/精度时分别生成输入表与结果目录；正式输入默认要求 BF16，量化调试须显式 --allow-nonbf16 并单独报告。源 train 拟合 scaler 和检测器，源 validation 选超参与 F1 阈值；目标 test 只用于最终评分。所有正确/错误标签都要求审核，自动匹配提案不会进入主指标。

输出包括 transfer_matrix.csv、tre_baselines.csv、ablation.csv、coverage.json、predictions.csv、training_audit.json、detectors.joblib、两张图和 manifest.json。清单含代码哈希、输入哈希、精度、随机种子和依赖。joblib 是本地训练产物，仅加载自己可信的文件。

轨迹字段与公式依据见 docs/TRACE_AND_EVALUATION.md。4090D 阶段仍需真实模型对齐验证、BF16 pilot、标签审核与正式采集。

## 当前32GB环境完整方案

见 [vGPU 32GB完整实验方案](docs/VGPU_32GB_完整实验方案.md)，已按【无卡】准备/分析和【有卡】真实采集分步安排。截图镜像兼容性与BF16能力仍需上机核验。


## 第2阶段：真实模型采集器（已实现，本地验收）

入口：scripts/collect_llada.py / scripts/collect_dream.py。位置对齐、FP32统计、manifest、原子落盘与恢复已有CPU测试。真实7B/8B BF16与GPU单题/20题仍待上机验收。见 [采集器使用说明](docs/PHASE2_COLLECTORS.md)。

```bash
# 在独立的torch/transformers CPU测试环境运行，不下载模型权重
python scripts/verify_collectors_cpu.py --output results/collectors_cpu_new
```

普通CPU项目环境未安装torch时，采集器测试会明确skip；必须另运行说明中的独立采集器测试环境，不能用skip冒充通过。

## 论文与完整上游代码

[references/README.md](references/README.md) 按六篇主线论文组织PDF、已确认的作者代码快照、固定提交与逐文件哈希，并明确记录TRE/DeMTS的代码获取缺口。它们保持各自上游许可，与本项目采集器分开；不是已完成论文复现的声明。

主线论文资料现以 [六篇研究索引](references/README.md) 为准：TRE、TraceDet、DynHD、DeMTS、TDGNet、Lost in Diffusion。源码缺口逐篇记录，不以附加参考替代。
