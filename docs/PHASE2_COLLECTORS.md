# 第2阶段：采集器使用与本地验收

两套真实模型采集器已实现：collect_llada.py / collect_dream.py。代码路径已用CPU替身模型验证，**真实7B/8B、CUDA/BF16、云端依赖与显存仍未验收**。不用开启云端GPU来运行下面的本地测试。

## 1. 环境与测试（无卡）

CPU项目环境和推理环境分开。原CPU锁仍不含torch。独立采集器测试环境使用Python3.12：

```bash
uv venv --python 3.12 .venv-collector-test
uv pip install --python .venv-collector-test/bin/python torch==2.13.0 --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv-collector-test/bin/python -r requirements/collector-cpu-tests.txt -r pyproject.toml
.venv-collector-test/bin/python -m pytest
.venv-collector-test/bin/python scripts/verify_collectors_cpu.py
```

Windows将bin/python换成Scripts/python.exe。本机测试环境复用了已有CPU torch，未下载权重。完整CPU演练用40条替身轨迹运行两套实际适配器，每条64步×64位置；Dream调用固定revision原生生成器，LLaDA与另一份参考循环核对。新目录首跑会真实执行，已有完成目录则显式resume验证；需要新的演练用 --output results/collectors_cpu_new。

`uv run pytest`在无torch的CPU项目环境会跳过两个torch采集器测试文件，不能代替上面的独立环境测试。保存恢复测试不需要torch，始终运行。

## 2. 云端推理环境准备（安装/下载可在无卡模式）

保留平台base的torch2.8.0/CUDA12.8，分别建venv；如复用平台torch，可用 --system-site-packages，随后通过import检查版本，避免继承旧numpy/pandas等二进制包冲突。不要运行CPU测试torch安装命令来覆盖云端CUDA torch。

本机无卡记录（2026-10-21）：已建立 .venv-llada（transformers 4.46.3、sentencepiece 0.2.2）与 .venv-dream（transformers 4.46.2），两者以 --system-site-packages 继承平台 torch 2.8.0+cu128（torch.version.cuda=12.8），venv 内未安装 torch；权重缓存 HF_HOME=/root/autodl-tmp/hf-cache（HF_HUB_CACHE 指向其 hub/）。用生产加载路径在 HF_HUB_OFFLINE=1 下完成 CPU 真实加载检查：LLaDA 8,015,581,184 参数、29.1s；Dream 7,615,616,512 参数、78.1s（含 Dream 原生生成源码锁校验），全部 bfloat16/CPU，未回退官方旧组合。两套 venv 的 fixture CLI 单题演练通过。CUDA/BF16 算子、显存与真实生成仍未验证；单题真实 forward 与 smoke20 仍是有卡门槛。证据见 reports/phase2_env_prep.json，权重下载/校验报告在 /root/autodl-tmp/model-download-reports/。

LLaDA候选依赖 requirements/collector-llada.txt 使用模型config标注的transformers4.46.3；Dream使用官方4.46.2。这些是配置起点，不代表实际模型兼容已通过。两环境都要另有CUDA torch。先在正确推理venv确认torch.version.cuda、驱动兼容、实际GPU和BF16支持，失败后再隔离回退，不全局升级平台环境。

真实加载固定configs/models中的模型/tokenizer/code revision；可使用HF_HOME指向已下载的持久云盘缓存。bitsandbytes仅NF4备选需要，不加入BF16必需环境。NF4 loader会检查Linear4bit确实存在；任何精度都不静默切换到其他模式。

## 3. 先单题（有卡）

在仓库根、相应模型推理venv执行：

```bash
.venv-llada/bin/python scripts/collect_llada.py --questions data/raw_qa/subsets/smoke20.jsonl --output data/trajectories/bf16_smoke_llada --limit 1 --verify-observer
.venv-dream/bin/python scripts/collect_dream.py --questions data/raw_qa/subsets/smoke20.jsonl --output data/trajectories/bf16_smoke_dream --limit 1 --verify-observer
```

默认cuda、bf16、64输出位置/64请求步、单block、temperature0、seed20261020。LLaDA固定CFG0/low_confidence；Dream原生entropy/alg_temp0。v1只支持上述greedy模式，不接受随机采样、CFG或Dream多block的模糊近似。LLaDA可显式设置满足整除条件的多block。

--verify-observer会额外做一次不记录轨迹的同seed解码，并要求最终token完全相同。它不把对照forward混入轨迹或资源计时，但会增加运行时间。仍需人工抽查至少每模型5条真实步骤。

## 4. 每模型20题及恢复（有卡）

去掉limit会改变题单签名，**不能用同一输出目录resume单题到20题**。单题通过后使用新目录：

```bash
.venv-llada/bin/python scripts/collect_llada.py --questions data/raw_qa/subsets/smoke20.jsonl --output data/trajectories/bf16_smoke20/llada --verify-observer
.venv-dream/bin/python scripts/collect_dream.py --questions data/raw_qa/subsets/smoke20.jsonl --output data/trajectories/bf16_smoke20/dream --verify-observer
```

同一命令加 --resume 重启：代码、环境、模型revision、题单内容、精度、seed、解码参数或observer配置不一致会拒绝恢复。已完成NPZ要重新校验schema和SHA256；损坏或缺失会报错，不静默覆盖。未写完的.partial不视为完成；完整NPZ写完而manifest中断的孤儿文件仅在run fingerprint和sample ID一致时接纳。不要修改目录内已有NPZ/manifest。

每个run目录由.collection.lock保护单写者。正常异常和Ctrl+C会释放锁；强杀/断电残留锁时先核对锁内host/pid并确认原进程已终止，再人工移除该锁文件。程序不会猜测进程死亡并抢锁。

## 5. 产物与离线接入（无卡）

每个输出目录含manifest.json、generations.jsonl和traces/<sample-id-hash>.npz。NPZ与manifest逐题提交；generations.jsonl在完成、可控异常或恢复后统一重建，避免大样本时反复扫描所有历史NPZ。强杀后该导出文件可暂时缺失/落后，以manifest/NPZ为准，恢复后重建。路径不直接使用question ID，避免路径字符造成越界。sample_id为question_id__seedN；question_id保持冻结题ID，用于防泄漏与问题bootstrap。

manifest保存代码哈希、题单指纹、模型/依赖/配置、模型dtype/device计数、状态、错误和各文件SHA256。NPZ记录FP32熵、top1概率、top1 token、MASK、真实揭示集合、reveal_step、最终token、prompt/token IDs、实际forward计数、EOS/EOT、精度与资源数据。熵在采样变换前计算；Dream hook已shift，不再shift；同时识别LLaDA eot和Dream im_end，裁切有效回答但保留全部生成token。

对每个run单独处理：

```bash
uv run python scripts/offline.py label --questions data/raw_qa/subsets/smoke20.jsonl --generations data/trajectories/bf16_smoke20/llada/generations.jsonl --output data/labels/smoke_llada.proposals.jsonl
uv run python scripts/offline.py extract --questions data/raw_qa/subsets/smoke20.jsonl --traces data/trajectories/bf16_smoke20/llada/traces --labels data/labels/smoke_llada.proposals.jsonl --output data/features/smoke_llada.parquet
```

Dream替换目录和文件名即可。smoke只做工程审计，不传给evaluate训练/测试。正式pilot200使用同一采集命令换题单和新输出目录；所有正确/错误标签人工审核后，分别导出两个parquet，再用pandas.concat合并进入双向评测。不同precision/长度/步数/revision不混入同一主表。

## 6. 本地验收的边界

CPU替身会明确synthetic=true，真实默认synthetic=false；不存在载入失败后自动退回假模型的路径。fixture演练需要显式 --fixture，结果放results/，不能混入真实轨迹目录。CPU原生生成器测试证明接口、位置映射和保存链路，不证明真实权重下的数值、GPU算子、显存、模型质量与生成一致性。云端单题/20题检查仍为独立验收门槛。


## 审查后增加的保护

- 固定checkpoint和tokenizer为完整40位小写commit SHA；自定义配置也不能使用main/tag/短SHA，否则加载前拒绝。
- 固定Dream原生entropy采样器在FP16下存在epsilon下溢、排序NaN风险。当前拒绝Dream float16与nf4_fp16；支持BF16主线和FP32诊断。不能为了跑T4静默改变原采样语义。LLaDA的NF4入口仍需实际兼容性验收。
- NPZ flush/fsync后再replace，再同步POSIX父目录，之后才持久化manifest；Windows的Python没有可移植目录fsync接口，因此Windows只验证文件同步/调用顺序。尚未做真实断电或云盘故障测试。
