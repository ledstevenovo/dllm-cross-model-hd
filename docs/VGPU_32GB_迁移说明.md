# vGPU 32GB 迁移说明

本仓库包含CPU工具、冻结QA划分、配置、测试、审计证据和T4计划。模型权重、原始parquet、虚拟环境、缓存和批量实验输出不上传。

## Linux实例

```bash
git clone https://github.com/ledstevenovo/dllm-cross-model-hd.git
cd dllm-cross-model-hd
nvidia-smi
uv sync --locked
uv run pytest
uv run python scripts/audit_dataset.py
```

需要重新构建数据时：

```bash
uv run python scripts/download_raw.py
uv run python scripts/build_dataset.py
uv run python scripts/build_pilot.py
```

完整CPU演练：`uv run python scripts/acceptance.py`。它包含模拟轨迹生成，不是真实模型推理。新机器重新运行会生成自己的环境/审计记录；历史reports是原机器证据。

## 32GB GPU下一步

vGPU-32GB不是具体GPU型号。先记录GPU名称、compute capability、实际空闲显存、驱动和torch.cuda.is_bf16_supported()。若支持BF16且单模型实测能放下，优先官方BF16，而非沿用T4的NF4默认配置。两模型依次加载，batch=1，先20题smoke、64输出位置/64请求步。显存/速度均需实测。

模型revision固定在configs/models中。推理环境与CPU环境分离，使用模型官方兼容的Python/torch/transformers。不能仅用现有CPU环境直接加载模型。

真实模型采集器现已实现并通过CPU替身路径测试；使用scripts/collect_llada.py和collect_dream.py，命令见PHASE2_COLLECTORS.md。真实模型仍需验证Dream shift、pre-reveal熵和MASK/reveal时点。细节见TRACE_AND_EVALUATION.md和T4_15GB_执行计划.md；T4计划的量化策略只作低显存备选。

原始权重和轨迹放持久云盘，按revision缓存；完成后回传并核验文件再释放实例。正式结果与模拟结果/量化结果分目录，记录实际commit和配置。

## 数据与归属

QA文本来自公开TriviaQA与HotpotQA，用于研究；保留source provenance、原始引用和许可条件。见DATASET.md所链接的原始数据卡。此仓库公开可见，不包含未公开模型权重、凭据或上游完整代码checkout。
