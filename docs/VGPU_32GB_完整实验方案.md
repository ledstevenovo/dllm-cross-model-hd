# vGPU 32GB 完整主线实验方案

日期：2026-10-21。针对截图：Ubuntu22.04、Python3.12、PyTorch2.8.0、镜像CUDA12.8；每GPU CPU12核、RAM62GB、标称显存32GB、数据盘50GB、驱动580.105.08（界面标CUDA13.0）。界面不是运行验收：GPU名称、实际空闲显存、BF16支持以实例输出为准。“空闲GPU 0/8”表示该页面当时没有空闲配额，需确认实例确已获得GPU。

目标：LLaDA-8B-Instruct与Dream-7B-Instruct，TriviaQA/HotpotQA，BF16轨迹→TRE→LR/MLP→双向迁移→最小消融。两模型顺序加载，不要求同时驻留。T4 NF4方案保留为独立备选，不混入BF16主表。

## 运行模式约定

- 【无卡】不需要GPU，可在本地或平台确认的无卡模式运行。无卡不保证免费；CPU/云盘/网络计费及停止后持久性需按平台规则确认。
- 【有卡】必须实例已分配GPU、CUDA可用。只把加载验证、真实生成与轨迹采集安排在这里。
- 切换模式前核对持久盘挂载路径；不能假定停止实例、无卡切换和销毁实例等价。所有模式共用同一份代码、缓存和运行清单。

## 0.【无卡】迁移与数据核验

```bash
git clone git@github.com:ledstevenovo/dllm-cross-model-hd.git
cd dllm-cross-model-hd
git rev-parse HEAD
uv sync --locked
uv run pytest
uv run python scripts/audit_dataset.py
uv run python scripts/audit_near_duplicates.py
```

已有仓库时用git pull --ff-only，不重复克隆。SSH须已配置GitHub公钥。当前冻结数据在仓库内，无需每次重新下载/重建。原始逐题来源复核需要先运行download_raw.py，再运行audit_raw.py；重建会更新manifest，应在开始真实采集前完成并重新冻结。

保留smoke20作为工程专用；pilot200含120 train / 30 validation / 50 test。small200是纯测试集，不能用于调参或代替pilot200。两个backbone共用question_id及全局划分。

## 1.【无卡】磁盘与原始权重准备

截图50GB数据盘可能不足以同时放两套原始权重、CUDA环境和缓存。建议先扩容至至少80GB持久空间，或按模型顺序下载/采集并核验备份后再有计划清理缓存。不要在唯一副本未备份时删除任何数据。

检查实际挂载和可用空间：`df -h`、`free -h`。在确认的持久目录内设HF_HOME，将模型下载与运行结果都放在该目录。不要把系统临时目录当持久云盘。模型revision取configs/models/llada.json与dream.json；按固定revision下载并校验分片完整性、大小与哈希。仅下载不需要GPU，下载时间不应占用有卡时段。模型文件不提交GitHub。

## 2.【无卡】隔离环境与采集代码准备

CPU环境维持uv+.venv和现有锁，不把torch加入CPU锁。平台预装的torch2.8.0/CUDA12.8先作为候选推理环境，记录实际版本，不声称两模型已兼容。

LLaDA官方README建议transformers4.38.2，Dream建议transformers4.46.2、torch2.5.1。分别建立独立推理venv；候选先尝试使用平台torch2.8.0，只有模型导入/加载失败才在相应隔离环境回退到官方组合。不要直接全局升级transformers或覆盖平台镜像。官方旧版本组合如不适用于Python3.12，可另建Python3.11推理环境；CPU工具仍保留原环境。CUDA wheel版本不必等于驱动界面显示的“CUDA13.0”，应核验驱动兼容性及torch.version.cuda。

**真实模型采集适配器尚未实现，是执行前必须补的工作。** 拟新增collect_llada.py / collect_dream.py，不提供不存在脚本的可执行命令。无卡阶段完成参数解析、持久化、断点恢复、trace-v1契约测试、manifest、CPU夹具测试和Dream shift源码核对；真实forward和hook时点在有卡阶段验证。

契约：保存pre-reveal熵/top1概率/可选top1 token、MASK与实际新揭示位置，统计FP32，GPU即时归约后只转CPU小数组。全词表logits不跨步保存。保留原始prompt与chat-wrapper后token IDs、checkpoint/tokenizer/代码revision、seed、实际T/forward次数、EOS/有效长度、precision和环境。断点续跑只跳过配置一致且校验通过的样本。

## 3.【有卡】设备与BF16资格检查

```bash
nvidia-smi
python - <<'PY'
import torch
print('torch', torch.__version__, 'runtime CUDA', torch.version.cuda)
print('available', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU', torch.cuda.get_device_name(0))
    print('capability', torch.cuda.get_device_capability(0))
    print('free,total bytes', torch.cuda.mem_get_info())
    print('BF16', torch.cuda.is_bf16_supported())
PY
```

在实际推理venv运行上面探测，不是仅检查平台base环境。验收GPU可用、足够空闲显存、原生BF16算子及单次真实forward通过。vGPU-32GB/A10机是商品标签，不能据此认定物理GPU型号、吞吐或共享方式。若BF16不支持，不将FP16或NF4当作BF16替代主表；另设兼容性诊断结果，评估换实例。

## 4.【有卡】单题→每模型20题 BF16 smoke

主配置：batch1、gen_length64、requested_steps64、temperature0、固定seed20261020；两模型依次加载。LLaDA单block64、CFG0、low_confidence；Dream选原实现支持的单调揭示策略并单独记录参数。不同模型不强行共享未支持的参数。保留EOS行为，不为满足固定步数篡改生成。

先每模型1题验证加载与轨迹，再完整smoke20。至少每模型抽查5条早/中/晚步，尤其Dream logits是否已shift；比较采集开关前后相同seed的最终tokens，确保观测不干扰采样。每模型再重复3题，记录非确定性。

测加载耗时、平均/中位单题时间、allocated/reserved显存峰值、进程占用、文件大小和失败/重试率。20题全部可追溯且校验通过才扩大采集。32GB是容量条件，不是单模型一定不OOM的保证。

## 5.【无卡】smoke审计与事实标签协议复核

回传NPZ与generation JSONL，核验文件哈希。使用offline.py label/extract时显式传 `--questions data/raw_qa/subsets/smoke20.jsonl`，默认研究池不含smoke。检查数值、mask迁移、EOS、有效长度及TRE。smoke不训练、不报告正式迁移指标。

人工核验正确/错误及边界输出。自动匹配只作提案；拒答、空、截断、格式失败分别保留，未匹配进入needs_review。正式correct/incorrect需要human_reviewed=true和human:<reviewer/run>来源。

## 6.【有卡】采集每模型pilot200

同一份pilot200=120/30/50，两模型各200题，总400条BF16轨迹，沿用已验收配置。每完成一条原子落盘并更新进度；故障恢复须校验配置/哈希，不重新跑已完成正确样本。不同precision、长度、步数、block或revision进入不同run目录。

计费预测先用实际smoke数据：`T采集=200*t_llada+200*t_dream+加载/I/O/重试`。截图价格1.58元/小时仅作当时参考，实际价格以订单为准；不能在未测吞吐时承诺总费用。

## 7.【无卡】第一份真实迁移矩阵与消融

完成标签复核，报告模型/数据集类别数、无效比例和审核覆盖率。若源train/dev缺少某类，不能凑标签或使用目标test调参；先按冻结规则补充源train/dev，保留原测试集。

用offline.py extract导出独立BF16特征表；evaluate输出TRE、LR/MLP、两域内+两跨模型、目标域监督参照、同目标迁移代价、AUROC/AUPRC/F1/ECE/Brier和question-ID bootstrap区间。阈值/归一化/超参只在源train/dev拟合。正式可用bootstrap1000；单类子集指标留空。

先entropy_raw与relative_normalized，再跑10组已有特征消融；with_stability要求采集top1_token。检查目标绝对性能，不能只看迁移差距变小。跨数据集用独立axis dataset报告。保存预测、模型、coverage、training_audit和输入/代码哈希。

## 8.【无卡决策→有卡采集→无卡分析】扩到800–2000题

pilot200是流程与初步研究验证，不保证统计功效。若标签可靠且出现稳定迁移缺口，按预先记录的抽样规则扩池，按簇保持全局划分，并在看新增测试结果前冻结新题单。每模型总题数800–2000包含train/dev/test，不是全部新增test；每个split都需要足够正负例。

【有卡】只采新增问题轨迹；未改变配置的已有有效样本可复用。
【无卡】审核标签、训练/评测、多seed重复和置信区间。统计精度和标签成本决定规模，不为凑2000无条件扩大。若TRE已足够强、域内信号弱或迁移缺口不稳定，先审计原因并按原研究计划调整方向。

## 9.【按需有卡/无卡】稳健性与增强基线

【无卡】现有轨迹上的时间/熵/揭示表示消融、阈值与校准诊断、检测器多seed、错误分析和画图。
【有卡】需要新生成的128/256长度、不同steps/block、生成seed变化；各自独立配置并先测显存/耗时。
【无卡】先适配TraceDet的离线接口；需要额外模型轨迹/hidden/attention时另安排有卡预算。DynHD/TDGNet/DeMTS等按P0结果决定，不一开始同时重训练。基座微调、全层attention与长文本claim-level不是本轮必做项。

## 10.【无卡】归档与释放资源

交付：真实BF16 pilot报告、baseline/transfer/ablation表、错误分析、图像、完整manifest和可复算预测。代码push GitHub；原始权重、轨迹和模型产物在持久云盘与本地/独立备份两处保存，核对哈希后再释放GPU。关闭GPU是否停止计费、无卡是否保留盘、销毁是否删除盘须按平台实际规则核对。

仓库当前CPU验收与模拟结果不能证明上述真实实验已完成。此文更新的是完整执行方案；采集器实现和上机验收仍需后续执行。

依据：原始实验计划、当前仓库接口、截图配置；模型兼容性参考 https://github.com/ML-GSAI/LLaDA 和 https://huggingface.co/Dream-org/Dream-v0-Instruct-7B 。平台镜像组合未实测。
