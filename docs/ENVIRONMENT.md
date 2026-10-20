# 环境

Python 3.12/3.13、uv、项目内 .venv；pyproject.toml 与 uv.lock 是唯一依赖入口。CPU环境包含 numpy/pandas/pyarrow/scikit-learn/matplotlib/pytest，不装 torch/CUDA。标准安装：`uv sync --locked`；运行：`uv run pytest`。模型环境按backbone另建并固定PyTorch/CUDA版本。

本机已有venv基于Windows Store Python 3.13。受限沙箱内启动会报 Unable to create process；同一解释器在已批准的外部执行可正常运行全部测试。不要把这个沙箱限制误判为依赖损坏，也不需在uv上再叠Conda。

在PowerShell可用 `.venv/Scripts/python.exe` 运行README命令。需要时将 UV_CACHE_DIR 指向项目 .uvcache。绘图脚本已将 MPLCONFIGDIR 指向 .tmp/matplotlib；pytest临时文件定向 .tmp/pytest。旧 scripts/env.sh 和 _pyfix 是历史沙箱辅助，不是安装的必需依赖。

数据原文为UTF-8；JSONL/JSON/ID文件在.gitattributes中禁止行尾转换，以保持manifest哈希。无需保存API密钥。模型权重、原始下载、轨迹、特征与结果均由.gitignore保护（冻结QA研究划分已由原工程纳入版本控制）。
