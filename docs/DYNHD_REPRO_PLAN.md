# DynHD 复现方案（32GB 显存主机）

> v4.1 · 2026-10-21 · 状态：执行细则修订完成（含 v4 审阅补齐的 5 项实现契约与 2 条注记），待实现与验收；实验未执行
> 上位文档：docs/VGPU_32GB_完整实验方案.md（第9节增强基线）；论文 arXiv:2603.16459（EMNLP 2026 Findings，MIT 代码）。
> 硬件前提：按用户确认的 **32GB GPU 显存**规划；两模型依次加载，BF16、batch=1。记录实际设备与空闲显存；容量不替代完整采集实测。资格检查或完整采集 OOM 时停止该配置后续步骤，诊断后另立配置，不静默改精度或 offload。
> 平台范围：本方案绑定当前 Linux/AutoDL 主机（/root/autodl-tmp、平台 torch、既有快照与 venv 结论）；若改在本地 Windows 运行，路径、torch 与全部验证结论需重新核实。
> 目标定义：**方法级复现** —— 在本机冻结题库/划分与人工复核标签协议下，跑通官方实现的完整管线（采集→证据→训练→评测），得到可与我们主实验对比的域内检测指标；**不是**逐表复刻论文数字（其规模 2000 题、GPT-4o-mini 判分，与本项目不同）。

## v4/v4.1 修订与执行边界

本版保留步骤 0–8 及原研究范围，修正失败诊断时点、配置合并与标签绑定、原始数据保护、正式训练停止条件、工程数据入口和采集 seed。新增脚本与参数均为**待实现契约**，文中验收条件不代表已通过；本次仅修改方案，不执行安装、模型加载、采集、训练或清理。

v4.1 相对 v4 的变更（审阅补齐，均为实现契约层，不改变研究范围）：

1. 定义 CPU 替身入口与 monkeypatch 目标（`--fixture`、`_build_model_and_sampler` 替换、输出目录约束）；
2. 写死 provisional 二元映射与 `provisional_kind`；
3. 接通「仅 val 选阈值」的落盘与报告闭环（基于 report.py 逐题分数）；
4. 写死 valid/ 文件命名基准（`{pilot_index:06d}.pt`）；
5. 明确 reviewed 模式的使用场景与哈希失败规则；
6. 两条小注记：run manifest 记录 `dataset_arg_compat`；受控序列 decode 检查标注为离线单元检查。

主方案阶段 3–4（设备/BF16 检查与主项目单题→smoke20）可独立推进；其通过不能替代本方案 DynHD 包装器与采样器的验收。

## Steps

- [ ] 0 环境与接入（无卡）：建 .venv-dynhd、依赖、PYTHONPATH 接入固定快照、跑官方单元测试
- [ ] 1 离线集成与替身验收（无卡）：包装器接口映射、fixture 入口、验收子集（最长 prompt）、valid/excluded 目录与分模型 split、CPU 端到端（同一包装入口）
- [ ] 2 有卡单题与对齐验证：按各自 tokenizer 选最长 prompt、显存、Dream shift 抽查、观测无干扰、T 预定义分支
- [ ] 3 smoke20 工程验收（有卡，两模型）：全链路跑通，不产生研究指标
- [ ] 4 pilot200 采集（有卡，两模型共 400 条）：失败诊断留档、新 run 重试、按 question_id 合并
- [ ] 5 标签复核（无卡+人工）：事前固定剔除规则；分模型判标签；valid/excluded 落盘与分模型 split 重建
- [ ] 6 训练与评测（GPU/CPU）：check_valid 入口断言、固定阈值、3 种子、bootstrap 区间、失败率三视图
- [ ] 7 报告与交付（无卡）：证据汇总、偏差清单、归因与规模限制
- [ ] 8 可选/决策：扩到 800–2000；跨模型评估与严格同生成对照

## 0. 环境与接入（无卡）

上游快照（只读、不修改）：`references/repos/DynHD`，固定提交 `6c099ad`（已在 manifest 中逐文件哈希）。旧版记录的 `/root/autodl-tmp/repos/DynHD` 临时副本一致性不作为本次实时证据；执行前重新核验快照与 manifest，本方案不安排删除。

```bash
cd /root/autodl-tmp/dllm-cross-model-hd
uv venv .venv-dynhd --python /root/miniconda3/bin/python3 --system-site-packages --seed
.venv-dynhd/bin/pip install transformers==4.46.2 accelerate==1.2.1 numpy==1.26.4 scikit-learn==1.5.0 PyYAML==6.0.1 tqdm==4.66.1
.venv-dynhd/bin/python -c "import torch, transformers, sklearn, yaml; print(torch.__version__, transformers.__version__)"
```

- 继承平台 torch 2.8.0+cu128（venv 内不装 torch），与 `.venv-llada/.venv-dream` 同套路；numpy/sklearn 用论文 pin，venv 内遮蔽平台版本。
- **不装** `datasets`（第1步会用本地题库替换其数据加载）；若将来要用其原生 HF 数据路径再补装。
- 不用 `pip install -e`（不想动上游目录），统一 `PYTHONPATH=references/repos/DynHD`。
- 在子 shell 运行官方测试，避免改变后续工作目录：`(cd references/repos/DynHD && PYTHONPATH=. /root/autodl-tmp/dllm-cross-model-hd/.venv-dynhd/bin/python -m unittest discover -s tests -v)`。其余命令均在 `/root/autodl-tmp/dllm-cross-model-hd` 执行。
- 兜底（记录偏差）：若与平台 torch 2.8 不兼容 → venv 内装 `torch==2.5.1`（阿里云镜像可用）；若 LLaDA 远程代码在 transformers 4.46.2 报错 → 升 4.46.3（已在本机 `.venv-llada` 验证）。

验收：import 和官方单元测试通过；原始 `pip freeze` 存 `reports/dynhd_pip_freeze.txt`，将 Python/torch/CUDA/依赖版本、命令及退出码整理成合法 JSON：`reports/dynhd_env.json`。既有 venv 的加载记录仅作候选依据，本环境须重新验收。

## 1. 离线集成与替身验收（无卡）

**目录约定（正式训练只读 pilot200/valid；工程数据独立）**：

```
/root/autodl-tmp/dynhd_repro/
  traces/<model>/pilot200/raw/<run_id>/         # 上游直出；每次 run 必须新目录（上游 exist_ok=False）
  traces/<model>/pilot200/valid/                # 复核后有效样本（唯一正式训练输入）
  traces/<model>/pilot200/excluded/             # 剔除留档
  traces/<model>/pilot200/failures/<run_id>.jsonl
  splits/<model>/pilot200.json                  # 分模型 split
  splits/<model>/index_map.json                 # 索引↔question_id 双向映射
  subsets/<model>_acceptance.jsonl              # 单题验收子集（含最长 prompt 题）
  manifests/<model>/<run_id>.json               # 配置指纹、有序任务清单与环境
  traces/<model>/pilot200/merged/<merge_id>/    # 同配置成功样本的合并快照
  acceptance/<model>/raw/<run_id>/              # 单题验收，不默认并入 pilot
  engineering/smoke20/<model>/<run_id>/         # provisional 数据与工程训练结果
  engineering/selftest/<test_id>/               # CPU 替身，禁止进入正式目录
  results/<model>_pilot200/<experiment_id>/seed{42,43,44}/
```

**`scripts/dynhd_repro/collect_local.py`（包装器）——接口映射必须显式实现**：

| 包装器参数 | 转换到上游 | 说明 |
|---|---|---|
| `--model {llada,dream}`、`--config PATH` | 选择对应 config | model 与 config 模型族必须一致，不一致即报错 |
| `--subset PATH` | 替换 `_load_dataset_items` | 读本地 JSONL（id=sample_id、question、answer=gold_answer+aliases） |
| `--limit N` | 同时向上游传 `--num-samples N` | 先按 only-question-ids 过滤再按固定顺序取 N 条，不足即报错；省略时传过滤后实际数量，不落到上游默认 2000 |
| `--dataset triviaqa` | 直通，包装器默认 triviaqa | 仅满足上游 choices；真实题库来源写入 meta/run manifest |
| `--labels provisional\|reviewed`、`--labels-file` | 替换 `OpenAIChatLabeler` | 初次采集默认 provisional；reviewed 要求 labels-file 且校验回答/轨迹绑定。config 保留 method=openai 仅作兼容，不发起 API 请求 |
| `--only-question-ids PATH` | 过滤本地题库 | 失败重试专用 |
| `--fixture {trivial\|fault}`、`--fault-plan PATH` | 替换 `_build_model_and_sampler` | 仅 CPU 替身；规则见下方 fixture 条目 |
| `--run-id ID`、`--output-dir DIR` | 直通 `--output-dir` | 每次 run 新目录 |
| `--num-steps/--gen-length` | 直通 | 主配置 64/64 |
| `--collection-seed INTEGER` | 包装器设置，不传给上游 argparse | 默认 20261020；按 question_id 稳定派生逐题 seed，与训练 seed 分开 |
| `--split` | 不使用 | 本地子集自带划分，传默认值 |

- 提示词对齐：`_question_content` 换成仓库冻结 prompt 的题面文本（Dream/LLaDA 仍各走 chat template）。
- **元数据修正**：包装 `save_trace_with_prompt_emb`，把上游硬编码的 `labeling_method="openai"`（collect_traces.py:208）改写为真实来源（`offline_match_proposal`/`human_reviewed`）并保留理由字段；自检断言 meta 中不残留 "openai"。
- **provisional 二元映射（写死）**：`correct→0`、`incorrect→1`、`refusal_empty/incomplete_truncated/format_failure→1`；meta 记 `provisional=true` 与 `provisional_kind`。仅工程用途，不进入任何指标口径。
- **reviewed 模式规则**：仅用于补采/重采已复核题目；labeler 调用时校验回答哈希、保存钩子校验 trace 哈希；任一不符 → 该题失败并记录，**不自动降级为 provisional**。常规首采一律 provisional，复核后经 relabel 落 valid。
- **fixture 入口（CPU 替身）**：`--fixture {trivial|fault}` 替换 `_build_model_and_sampler`，返回确定性合成 sampler；`fault` 依 `--fault-plan` 注入形状/标签/保存失败。运行强制 `--output-dir` 位于 `engineering/selftest/` 下，否则报错。
- **monkeypatch 目标注记**：上游在 `collect_traces.py:15–18` 直接导入相关名字，所有替换必须打在 `dynhd.cli.collect_traces` 模块属性上（`_load_dataset_items`、`OpenAIChatLabeler`、`save_trace_with_prompt_emb`、`_build_model_and_sampler`），打在 `dynhd.data`/`dynhd.labeling` 源模块上无效。合成 sampler 接口约定：`tokenizer.apply_chat_template/encode/decode`；`sample(...) -> {clean_text, features, prompt_emb}`，且与真实路径同样保持"一题一次 sample"。
- **任务 ID 与失败诊断**：加载过滤后的有序任务清单并校验 ID 唯一；每次 sample 从清单绑定当前 question_id 并核验实际 prompt，禁止根据题面反查 ID（不同 ID 可有相同题面）。若上游"一题一次 sample"契约改变则停止适配。
  1. sample 前写 start 事件并 flush，包含 ID、run_id、逐题 seed、配置指纹与时间。
  2. sample 异常时写 `{question_id, run_id, stage, exception, actual_T, ts}` 后 re-raise；实际 T 无法取得时为 null，不能伪造。
  3. **sample 正常返回后、交还上游之前**检查 features 类型、形状与有限性。形状不符先记录实际 T，再让上游原校验报错；非有限值等上游未校验项由包装器报错。不得依赖 save 钩子捕获先于保存发生的异常。
  4. 标签器和保存函数也包装分阶段异常；只有 .pt 写入并可重载校验后才记 saved，记录原始文件哈希。
  5. 中断后以"预期任务清单 − 可校验成功文件"计算待重试缺口，结合 start/saved/failed 事件核验，包括尚未开始的题。不能只补采已写 failed 的题；已 flush 的 start 可辅助定位进程被杀位置。
- **生成指纹**：规范化配置 JSON 后做 SHA-256，覆盖模型/checkpoint/tokenizer revision、上游/包装器代码版本或内容哈希、prompt/template、精度、采样参数（temperature/alg/alg_temp/top_p/top_k 等）、生成长度、请求步数、特征配置、collection_seed 与派生算法版本。run_id、时间、路径、过滤列表不参与生成指纹；完整运行配置与环境仍存 manifest。每题另存输入 token IDs 或其哈希、题库与冻结归属清单哈希、逐题 seed、回答哈希与源 trace 哈希。
- **采集 seed**：`item_seed = int.from_bytes(SHA256(UTF8(str(collection_seed) + ":" + question_id)).digest()[:4], "big")`。禁止 Python 内置 hash；每题在 prompt_emb/生成前设置 Python、NumPy、torch CPU/CUDA RNG；补采不受任务顺序影响。不承诺跨设备/版本位级确定，仍做重复性验证。
- run manifest 额外记录 `dataset_arg_compat: "triviaqa"`，避免后人把兼容字段当作真实题库来源。

**新增脚本**：

- `pick_longest.py`：用**各模型自己的 tokenizer + chat template** 对 pilot200 全量题目渲染最终输入并计长，输出 `<model>_acceptance.jsonl`：每模型 2 题——最长 prompt 一题 + 最短 gold 答案一题（仅作 EOS/边界探针，不保证生成 EOS；若重合选下一条不同 ID，长度并列按 ID 排序），写死 question_id 与 token 长度，选择不依赖文件顺序（smoke20 不保证覆盖最长输入，不作为依据）。
- `make_split.py`：冻结 question_id→划分归属（120/30/50）；为 valid 目录生成 `split.json` 与 `index_map.json`，断言全集覆盖、分区归属一致、无越界。
- `relabel.py`：读取只读 raw/merged，按 ID、生成指纹、回答哈希和源 trace 哈希校验复核标签；在内存更新 label/来源，以临时文件＋原子替换写独立 valid 文件。**不硬链接、不原地修改 raw/merged**，写前/写后核验 raw 哈希不变。excluded 留存原样本与排除理由；`correct→0`、`incorrect→1`。正式来源包括 `human_reviewed=true`、`provisional=false`、reviewer/source、复核时间与绑定哈希。**valid/ 与 excluded/ 文件命名基准写死为 `{pilot_index:06d}.pt`**（pilot_index = `pilot200.jsonl` 行序，与冻结归属同基准）；`index_map.json` 以该基准做索引↔question_id 双向映射，check_valid 的"排序一致"检查按此定义。
- `merge_runs.py`：先校验所有输入生成指纹一致、清单兼容、逐题 seed/输入哈希一致、文件可重载，再按 ID 合并到新 merged 目录。配置不一致一律拒绝；重复 ID 默认报错，`--prefer <run_id>` 仅解决**同配置**重复，不绕过指纹校验。记录选中 raw、哈希与选择理由；回答或选中 trace 变化时必须重新校验标签绑定。
- `check_valid.py`（正式入口）：只接受 pilot200/valid；非空、ID 唯一、全部 human-reviewed 且无 provisional、label∈{0,1}、标签绑定有效、生成指纹一致、特征/embedding 有限且维度合规；文件排序与 index_map 一致，split 恰好覆盖全集且归属正确，三分区非空，train/val 各含两类。失败返回非零，打印每分区类别数。
- `check_engineering.py`（工程入口）：限定 engineering 目录，检查形状、映射与训练所需类别，可接受 provisional 或 `test_fixture`；不得伪装成 human-reviewed。工程输入与输出不得进入正式 valid/results。

- `report.py`：汇总为 `reports/dynhd_*.json`；保存逐 ID 的 label/score、trace 哈希、seed、分区；val 选阈值与共同 test 视图均基于该逐题分数，不重训。

**验收（CPU 替身，经正式采集同一包装入口）**：13 个唯一 ID，其中 12 条正常（6/6 两类）＋1 条形状失败；含两个相同题面、不同 ID。断言原始 run 非零退出、12 条落盘、失败 ID 与实际 T 正确。另注入标签/保存失败，模拟中断后未开始任务；验证新 run 补采与合并、异配置拒绝、重复默认失败/显式 prefer 选择、标签哈希不符拒绝、raw 哈希不变。以 test_fixture 数据跑工程检查和 CPU train→eval；正式 check_valid 必须拒绝该数据，不伪造人工来源。真实 reviewed 正向路径在人工复核后验收。证据 `reports/dynhd_offline_selftest.json`。

## 2. 有卡单题与对齐验证

单题子集用 `pick_longest.py` 生成的验收子集（不依赖文件顺序）：

```bash
export HF_HUB_OFFLINE=1
export PYTHONPATH=/root/autodl-tmp/dllm-cross-model-hd/references/repos/DynHD
.venv-dynhd/bin/python scripts/dynhd_repro/collect_local.py \
  --model llada --config configs/dynhd_repro/llada_local.yaml \
  --subset /root/autodl-tmp/dynhd_repro/subsets/llada_acceptance.jsonl --limit 2 \
  --num-steps 64 --gen-length 64 --collection-seed 20261020 --labels provisional --run-id single \
  --output-dir /root/autodl-tmp/dynhd_repro/acceptance/llada/raw/single
# 同命令换 --model dream / dream_local.yaml / dream_acceptance.jsonl
```

必须逐项确认（写入 `reports/dynhd_singleq.json`）：

1. bf16 单卡加载成功（不静默 offload）；覆盖**该模型最长 prompt** 的完整 prompt_emb 提取与全部 64 步；记录加载耗时、单题耗时、allocated/reserved 峰值与设备空闲显存；
2. 证据 `features` 形状 `[64,3]`、全部有限、分布合理（与论文的 mean/max/top-k 语义一致）；
3. **Dream hook 对齐抽查**：对同题固定 5 步，用手工 forward 复核 hook 收到的是 shift 后 logits（主项目审计结论：该固定 revision 的 native hook 已是 after-shift；此处只需在 DynHD 采样路径里复现该结论）；
4. **观测无干扰**：同题、同 seed，`feature_extractor=None` 与开启采集的最终 token 必须一致；
5. 生成文本非空；记录实际 EOS/mask、生成长度及 decode 截断位置（沿用上游规则）。探针未产生 EOS 则标记"未覆盖"，用受控 token 序列补充 decode 单元检查（该检查为离线单元检查，不依赖 GPU）；gold 答案短不等于 EOS 已验收。记录两题 ID 与最终输入 token 长度；
6. 提前终止的**预定义分支**（跑 pilot 之前写死）：T=64 → 正常；可复现的系统性 T<64 → 另立 run_id 与替代步数配置，单独报告、绝不与主 run 混用；零星 T<64 → 该样本标记无效并调查原因，不静默改写或补齐。

## 3. smoke20 工程验收（有卡）

- 两模型各 20 题（同 question_id），provisional 标签，放 `engineering/smoke20/<model>/<run_id>/`，经 check_engineering 后跑 collect→train→eval；不调用正式 check_valid、不写正式 valid/results。自然输出单类则记录真实 smoke 训练条件不足，不改标签；训练连通性由独立 CPU 替身证明。
- 明确：**smoke 不报研究指标**；20 题只用来看流程、耗时、失败率、实际 T。
- 记录：每模型失败/重试数（其 collector 失败即整体报错，不静默丢样本）；Dream 是否出现 T < 64 的提前终止（按第 2 步预定义分支处理，见风险 4）。
- 证据：`reports/dynhd_smoke20.json`。

## 4. pilot200 采集（有卡）

- 先各自测 5 题标定 t；再两模型各 200 题（120/30/50 冻结划分），共 400 条 `.pt`，直出到 `traces/<model>/pilot200/raw/<run_id>/`。
- 配置沿用 smoke 通过的实际配置；不同配置必须新 run 目录，不覆盖。
- **失败与重试**：按任务清单、诊断与可校验文件计算失败及未开始缺口，用 only-question-ids 启动新 run，保持生成指纹与逐题 seed。全部完成后先核验配置再合并；prefer 不绕过指纹；未解决缺口显式报告。验收/标定 run 默认不并入 pilot，避免重复与来源混淆。

- 记录：加载/单题耗时、显存峰值、实际 T 分布、失败/重试/合并计数；给出 `T采集=200*t_llada+200*t_dream+加载/IO` 的表达与实际值。
- 证据：`reports/dynhd_pilot200_collect.json`。

## 5. 标签复核（无卡+人工）

- **事前固定**：剔除规则（拒答/截断/格式失败不进入主指标）与三个报告视图在人工复核开始前写死，复核过程中不改变口径。
- `offline.py label` 提案 → 人工复核 → reviewed 标签（`human_reviewed=true`，human 来源）；**同题不同模型的回答分别判标签**。
- 复核结果经 `relabel.py` 落成 `valid/`，剔除样本留档 `excluded/`，并按冻结归属为该模型重建 `split.json` + `index_map.json`（两模型的剔除情况不同 → 分模型 split，不复用同一份索引）。
- 报告三视图：① 全量回答的失败率与覆盖率（拒答/截断/格式失败率作为模型行为指标）；② 有效回答上的检测指标；③ **模型间并列比较用共同有效题集（且限定在冻结 test 分区内）**。
- 正式训练前置：train 两类均存在（含 Stage1 factual）、val 两类均存在、三分区非空；不重新分层或改变冻结归属。test 单类时 AUROC 留空。程序运行最低条件不等于统计样本充分；不足不造标签、不挪题。
- 证据：`reports/dynhd_labels.json`（含每个视图的题数）。

## 6. 训练与评测（GPU/CPU）

将以下内容保存为 Bash 脚本并用 `bash` 执行。依赖第 1 步脚本已实现验收；不代表当前已具备实现。先检查两模型数据和目标目录，再运行；任何非零退出均停止。experiment_id 必须唯一；失败恢复保留既有输出，另定新的 experiment_id，不覆盖。

```bash
#!/usr/bin/env bash
set -euo pipefail
cd /root/autodl-tmp/dllm-cross-model-hd
export PYTHONPATH="$PWD/references/repos/DynHD"
repro_root=/root/autodl-tmp/dynhd_repro
experiment_id=pilot200_v4_001
mkdir -p "$repro_root/results"
for model in llada dream; do
  .venv-dynhd/bin/python scripts/dynhd_repro/check_valid.py \
    --model "$model" \
    --valid-dir "$repro_root/traces/$model/pilot200/valid" \
    --split "$repro_root/splits/$model/pilot200.json"
  if [[ -e "$repro_root/results/${model}_pilot200/$experiment_id" ]]; then
    echo "Experiment output already exists: $model/$experiment_id" >&2
    exit 1
  fi
done
for model in llada dream; do
  for seed in 42 43 44; do
    seed_dir="$repro_root/results/${model}_pilot200/$experiment_id/seed$seed"
    mkdir -p "$seed_dir"
    .venv-dynhd/bin/python -m dynhd.cli.train_detector \
      --data-path "$repro_root/traces/$model/pilot200/valid" \
      --out-dir "$seed_dir" --device cuda --seed "$seed" \
      --split "$repro_root/splits/$model/pilot200.json" \
      --max-steps 64 --prompt-dim 256 --hidden-dim 256 \
      --epochs-stage1 10 --epochs-stage2 30 --batch-size 32 --verbose \
      > "$seed_dir/train.log" 2>&1
    for part in val test; do
      .venv-dynhd/bin/python -m dynhd.cli.eval_detector \
        --data-path "$repro_root/traces/$model/pilot200/valid" \
        --ckpt "$seed_dir/detector.pt" \
        --split "$repro_root/splits/$model/pilot200.json" \
        --split-part "$part" --threshold 0.5 --device cuda \
        > "$seed_dir/${part}_metrics.json"
    done
  done
done
```

训练期间 valid/split/index_map/标签清单只读，前后复核哈希。report.py 复用上游 checkpoint 加载与 predict_proba，保存逐 ID 的 label/score、trace 哈希、seed、分区，用于 bootstrap 与共同 test 视图；聚合指标 JSON 不能替代逐题预测。不得为导出预测重训练或按 test 选择 checkpoint。

**统计口径（写死）**：

- **阈值**：主口径固定 0.5（脚本落盘）。若启用按 validation 选择：用 report.py 已保存的**逐题 val 分数**在 val 上以 F1 选阈值，再在 test 上应用**一次**；固定 0.5 与 val 选择两个口径并列报告；禁止看 test F1 再调阈值，禁止据此重训或改 checkpoint。
- **3 个训练种子（42/43/44）**：分别报告每种子指标、三种子均值及 [min,max]，独立 checkpoint/预测文件；不把三个种子的预测当独立样本。
- **bootstrap**：RNG seed=20261021；每模型、每训练种子、每个 test 视图分别按 question 分组重采样 1000 次，取有效统计量 2.5/97.5 百分位。单类重采样只跳过该次 AUROC，不丢弃其他有定义指标；每项报告有效次数/总次数；原始子集单类或有效次数为零时 AUROC/区间留空。bootstrap 不重训练，与训练种子范围分别报告。
- **共同有效题集比较**：仅在冻结 test 分区内取两模型共同有效题集，报告题数；不跨分区拼接。
- 对照口径与归因限制：同题集、同划分、同标签协议、同 64 步；但**生成管线各自**（DynHD 用其采样器、主表用我们的采集器），指标差异同时含生成差异与检测差异——结论只能写「各自管线的域内结果」，**不得归因于检测器优劣**；严格同生成对照见第 8 步决策。
- 定位限制：200 题（test 50，单题≈2 个百分点）是 pilot，只用于决定是否扩池，不作为稳定结论依据。
- 证据：`reports/dynhd_eval_{llada,dream}.json`（含每种子、区间与有效重采样次数）。

## 7. 报告与交付（无卡）

- `reports/dynhd_reproduction_summary.md` + `reports/dynhd_reproduction.json`：配置、代码/快照哈希、轨迹数、耗时、显存、失败率三视图、每分区样本/类别数、种子与置信区间（含有效重采样次数）、失败/重试/合并计数、check_valid 输出摘要、**偏差清单**（见下表）、归因限制与规模限制。
- 提交内容：脚本、configs、reports；**不提交**权重、轨迹、结果目录（`.gitignore` 已覆盖 `.venv*`、`results/`；轨迹放 `/root/autodl-tmp/dynhd_repro`）。
- 复现声明用词：只在这个阶段完成后写"方法级复现（缩小规模、标签源不同）"。

## 子集与对照口径（关键决策）

| 项 | DynHD 论文/默认 | 本方案（主表） | 说明 |
|---|---|---|---|
| 题库 | HF trivia_qa rc 前 2000 | 我们的 smoke20 / pilot200 | 同 question_id 是可比前提，但不等于同生成 |
| 生成管线 | DynHD 自带采样器（LLaDA 自实现 / Dream 原生） | DynHD 复现仍用上游采样器；主实验用本项目采集器 | 两管线分开报告，不归因检测器优劣 |
| 提示词 | 原始问题 + 各自 chat template | 仓库冻结 prompt 题面 + 各自 chat template | 与主表一致；记录偏差 |
| LLaDA 步数 | 64 | 64 | 一致 |
| Dream 步数 | config 默认 128 | 64（与主表一致）；可选 128 | 偏差记录 |
| Dream 温度 | config 默认 0.2 | 0.0；alg=entropy，alg_temp=0.0 | 与主表一致；偏差记录 |
| 标签 | GPT-4o-mini judge | 我们的提案 + 人工复核（报告用 reviewed） | 协议差异必须声明 |
| 划分 | 内部 70/15/15（seed 42） | 冻结 120/30/50；分模型重建索引 | 与主实验对齐；剔除后按冻结归属重建 |
| 阈值 | 未固定 | 主口径 0.5；或仅 val 选择 | test 不参与调参 |
| 规模 | 2000 题 | 200 题/模型 | 规模限制声明 |

## 风险与处置

1. **torch 2.8 vs pin 2.5.1**（低）：兜底 venv 内装 2.5.1，记录。
2. **LLaDA 远程代码 + transformers 4.46.2**（中）：本机 `.venv-llada` 的 4.46.3 已验证可加载；失败则升版并记录。
3. **Dream hook shift**（中高）：单题阶段 5 步抽查；固定 revision 已有主项目审计背书。
4. **Dream 提前终止导致 T≠64**（中）：其 collector 严格要求 `(steps,3)`，会直接报错；按第 2 步**预定义分支**处理（系统性 → 独立 run；零星 → 无效样本），不在事后临时改配置。
5. **标签类不足**（中）：Stage1 需要 factual；校验不过则报告不足，不挪测试集、不造标签。
6. **`prompt_emb` 维度跨模型不兼容**（确定存在）：LLaDA 4096 vs Dream 3584，官方投影器绑定源维度，**跨模型直接评测会报维度错误**。首轮默认只做域内；若要跨模型，见第8步决策。
7. **与主实验混表**（红线）：DynHD 轨迹/证据不进入主特征表；只以"同题集同划分下的独立复现结果"并列报告。
8. **标签来源误记**（确定）：上游 `collect_traces.py:208` 硬编码 `labeling_method="openai"`；只换标签器不够，必须由包装改写元数据并自检。
9. **剔除与 split 冲突**（确定，若按删文件/哨兵标签实现）：上游按现存文件排序且 split 必须全覆盖 → "冻结归属 + 有效样本（valid/）重建索引映射"，训练入口用 check_valid 断言目录与映射一致。
10. **平台范围**（提示）：本方案按 Linux/AutoDL 写；本地 Windows 运行需重新核实路径、torch、快照与 venv 结论。
11. **上游 CLI 校验兼容**（确定）：`--dataset`（choices）、`len(items)==sample_count`、`labeling.method=="openai"` 三处校验必须由包装按接口映射表满足，否则直接报错。
12. **失败样本可能无 .pt**：sample 返回前检查形状，标签/保存分阶段记录；任务清单核验成功文件后，补采失败与未开始的缺口。
13. **合并污染**：不同指纹禁止合并，prefer 不绕过校验；标签必须绑定选中回答及 trace。
14. **工程/正式混用**：smoke/fixture 仅走 engineering 检查；fixture 强制写入 `engineering/selftest/`；正式 valid 仅接收 reviewed 数据。
15. **原始证据改写**：raw/merged 只读，valid 独立写出，禁止 relabel 硬链接/原地改写。
16. **继续执行/种子覆盖**：正式脚本启用 set -euo pipefail，先检查两模型再训练，各 seed 独立目录。

## 8. 可选与决策

- 扩到 800–2000 题：按主方案第 8 节扩池后重跑，接近论文规模。
- 跨模型用 DynHD：需先决策共享问题表示的方案（同一句向量编码器替换两模型的 `prompt_emb`，并声明偏差），默认不做。
- 严格同生成对照：让两族检测器作用于同一批生成/轨迹（用 DynHD 采样器重采并让主检测器读同一轨迹，或反之），消除生成差异；工程量大，默认不做，列为决策项。

## 预算与时间（待标定）

| 阶段 | 预计 | 备注 |
|---|---|---|
| 0–1 | 1–1.5 h | 安装 + 官方测试 + 包装器/断言脚本 + CPU 替身（含失败注入） |
| 2 | 0.5–1 h | 两次模型加载（LLaDA 约 1–2 min，Dream 约 2–4 min）+ 最长 prompt 验证 + 对齐抽查 |
| 3 | 0.5–1 h | 40 题工程跑 |
| 4 | 待标定 | 先测 5 题；= 400×t + 加载/IO + 重试，参考价以订单为准 |
| 5 | 人工为主 | 400 条复核，是主要瓶颈 |
| 6 | < 0.5 h | 检测器小，可 GPU/CPU；含 3 种子 |

## 红线

- 不修改 `references/repos/DynHD`（保持快照可校验）；所有适配在新脚本里做。
- smoke 不报研究指标；正式数字必须 reviewed 标签；剔除规则事前固定，不改口径。
- 正式训练只读 reviewed 的 pilot200/valid，必须通过 check_valid；工程数据仅走 check_engineering。检查失败即停止，不覆盖已有 run/experiment/seed 目录。
- fixture/替身只写入 engineering/ 目录；provisional 映射不进任何指标口径。
- 权重/轨迹/结果不入 Git；不在无卡阶段冒称有卡验收。
- 不改冻结 prompt 与冻结归属；异配置禁止合并；raw 只读，标签绑定回答与 trace；偏差只记录，不静默放宽。
- 不把「各自管线的域内结果」表述成检测器优劣对比；test 不参与阈值/超参选择。
