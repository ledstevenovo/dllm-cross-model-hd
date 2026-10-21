# DynHD 复现方案（当前 32GB 主机）

> v2 · 2026-10-21 · 状态：待评审（v1→v2 已按外部复核修订；未执行）
> 上位文档：docs/VGPU_32GB_完整实验方案.md（第9节增强基线）；论文 arXiv:2603.16459（EMNLP 2026 Findings，MIT 代码）。
> 平台范围：本方案绑定当前 Linux/AutoDL 主机（/root/autodl-tmp、平台 torch、既有快照与 venv 结论）；若改在本地 Windows 运行，路径、torch 与全部验证结论需重新核实。
> 目标定义：**方法级复现** —— 在本机冻结题库/划分与人工复核标签协议下，跑通官方实现的完整管线（采集→证据→训练→评测），得到可与我们主实验对比的域内检测指标；**不是**逐表复刻论文数字（其规模 2000 题、GPT-4o-mini 判分，与本项目不同）。

## Steps

- [ ] 0 环境与接入（无卡）：建 .venv-dynhd、依赖、PYTHONPATH 接入固定快照、跑官方单元测试
- [ ] 1 离线集成与替身验收（无卡）：本地题库/标签适配、冻结归属与有效样本索引映射、CPU 端到端替身演练
- [ ] 2 有卡单题与对齐验证：加载、最长 prompt 显存、证据形状/有限性、Dream shift 抽查、观测无干扰
- [ ] 3 smoke20 工程验收（有卡，两模型）：全链路跑通，不产生研究指标
- [ ] 4 pilot200 采集（有卡，两模型共 400 条）：先测 5 题标定耗时再全量
- [ ] 5 标签复核（无卡+人工）：事前固定剔除规则；分模型判标签；按有效样本重建索引映射
- [ ] 6 训练与评测（GPU/CPU）：冻结划分、3 种子、bootstrap 区间、失败率三视图
- [ ] 7 报告与交付（无卡）：证据汇总、偏差清单、归因与规模限制
- [ ] 8 可选/决策：扩到 800–2000；跨模型评估与严格同生成对照

## 0. 环境与接入（无卡）

上游快照（只读、不修改）：`references/repos/DynHD`，固定提交 `6c099ad`（已在 manifest 中逐文件哈希）。我在 `/root/autodl-tmp/repos/DynHD` 的临时副本与此快照逐文件一致，可直接删除。

```bash
cd /root/autodl-tmp/dllm-cross-model-hd
uv venv .venv-dynhd --python /root/miniconda3/bin/python3 --system-site-packages --seed
.venv-dynhd/bin/pip install transformers==4.46.2 accelerate==1.2.1 numpy==1.26.4 scikit-learn==1.5.0 PyYAML==6.0.1 tqdm==4.66.1
.venv-dynhd/bin/python -c "import torch, transformers, sklearn, yaml; print(torch.__version__, transformers.__version__)"
```

- 继承平台 torch 2.8.0+cu128（venv 内不装 torch），与 `.venv-llada/.venv-dream` 同套路；numpy/sklearn 用论文 pin，venv 内遮蔽平台版本。
- **不装** `datasets`（第1步会用本地题库替换其数据加载）；若将来要用其原生 HF 数据路径再补装。
- 不用 `pip install -e`（不想动上游目录），统一 `PYTHONPATH=references/repos/DynHD`。
- 运行官方测试：`cd references/repos/DynHD && PYTHONPATH=. /root/autodl-tmp/dllm-cross-model-hd/.venv-dynhd/bin/python -m unittest discover -s tests -v`
- 兜底（记录偏差）：若与平台 torch 2.8 不兼容 → venv 内装 `torch==2.5.1`（阿里云镜像可用）；若 LLaDA 远程代码在 transformers 4.46.2 报错 → 升 4.46.3（已在本机 `.venv-llada` 验证）。

验收：import 通过；官方单元测试通过；`pip freeze` 存 `reports/dynhd_env.json`。

## 1. 离线集成与替身验收（无卡）

新增（都在本仓库，不动上游快照）：

- `scripts/dynhd_repro/collect_local.py`：薄封装，monkeypatch `dynhd.cli.collect_traces`：
  - `_load_dataset_items` → 读 `data/raw_qa/subsets/{smoke20,pilot200}.jsonl`（`id=sample_id`、`question=question`、`answer=gold_answer+gold_aliases`）；
  - `OpenAIChatLabeler` → 本地标签器（`--labels provisional|reviewed --labels-file …`）：provisional 用 `offline.py label` 的自动匹配提案并在 meta 标注 `provisional=true`；reviewed 读人工复核结果；
  - 提示词对齐：把 `_question_content` 换成仓库冻结 prompt 的题面文本（Dream/LLaDA 仍各走 chat template）——与主实验一致；
  - 采集配置：主表 `--num-steps 64 --gen-length 64`、Dream `temperature=0.0`、`alg=entropy`、`alg_temp=0.0`；
  - 记录包装：per-item 耗时、实际 T、单题峰值显存（allocated/reserved 与 `mem_get_info`）写 sidecar `timings.jsonl`；
  - **元数据修正**：包装 `save_trace_with_prompt_emb`，把上游硬编码的 `labeling_method="openai"`（collect_traces.py:208）改写为真实来源（`offline_match_proposal`/`human_reviewed`）并保留理由字段；自检断言 meta 中不残留 "openai"；
  - 调用上游 `main()` 本体（保留其校验/行为），只替换上述入口。
- `configs/dynhd_repro/llada_local.yaml`、`dream_local.yaml`：`model_path` 指向绝对快照目录（绕开其 `HF_HUB_OFFLINE` 兜底只认 `~/.cache/huggingface/hub` 的问题）：
  - LLaDA：`/root/autodl-tmp/hf-cache/hub/models--GSAI-ML--LLaDA-8B-Instruct/snapshots/08b83a6feb34df1a6011b80c3c00c7563e963b07`
  - Dream：`/root/autodl-tmp/hf-cache/hub/models--Dream-org--Dream-v0-Instruct-7B/snapshots/05334cb9faaf763692dcf9d8737c642be2b2a6ae`
- `scripts/dynhd_repro/make_split.py`：**冻结的是 question_id→划分归属**（120/30/50），不是索引。为每个模型的「有效样本目录」生成 `split.json` 与 `index_map.json`（索引↔question_id 双向映射），并断言：每个有效样本恰属一个分区、分区归属与冻结表完全一致、无越界。
- `scripts/dynhd_repro/relabel.py`：复核结果写回 `label`（`correct→0`、`incorrect→1`）。**剔除不得用删文件或哨兵标签实现**——上游 `load_trace_dir`（io.py:30）按现存文件排序、`train_detector` 要求 split 恰好覆盖全部文件且 label 只能是 0/1，二者都会因此出错。做法：被剔除样本复制到 `excluded/` 留档，有效样本单独成目录，再按冻结归属重建索引映射；报告每个模型每个分区的剔除数与有效样本数。
- `scripts/dynhd_repro/report.py`：汇总为 `reports/dynhd_*.json`。

验收（CPU 替身演练）：伪造 12 条 trace（6/6 两类）→ `train_detector --device cpu` → `eval_detector`，确认与上游行为一致；证据存 `reports/dynhd_offline_selftest.json`。此结果只证明管线，不进入任何指标。另外断言两条：(a) 改写后的 meta 不含 "openai"；(b) 删 2 条样本后重建的索引映射仍指向同一 question_id，且训练不再报 split 覆盖错误。

## 2. 有卡单题与对齐验证

在 `.venv-dynhd` 跑（`export HF_HUB_OFFLINE=1`），先 LLaDA 后 Dream、单题（用子集中 **token 长度最长** 的题，覆盖最大 prompt；另跑一题 EOS/边界案例）：

```bash
.venv-dynhd/bin/python scripts/dynhd_repro/collect_local.py \
  --config configs/dynhd_repro/llada_local.yaml \
  --subset data/raw_qa/subsets/smoke20.jsonl --limit 1 \
  --num-steps 64 --gen-length 64 \
  --output-dir /root/autodl-tmp/dynhd_repro/traces/llada/single
# 同命令换 dream_local.yaml
```

必须逐项确认（写入 `reports/dynhd_singleq.json`）：

1. bf16 单卡加载成功（不静默 offload）；覆盖最长 prompt 的完整 prompt_emb 提取与全部 64 步；记录加载耗时、单题耗时、allocated/reserved 峰值与设备空闲显存；
2. 证据 `features` 形状 `[64,3]`、全部有限、分布合理（与论文的 mean/max/top-k 语义一致）；
3. **Dream hook 对齐抽查**：对同题固定 5 步，用手工 forward 复核 hook 收到的是 shift 后 logits（主项目审计结论：该固定 revision 的 native hook 已是 after-shift；此处只需在 DynHD 采样路径里复现该结论，防漏 shift/重复 shift）；
4. **观测无干扰**：同题、同 seed，`feature_extractor=None` 与开启采集的最终 token 必须一致；
5. 生成文本非空、EOS 截断语义正常（沿用其 decode 规则）；
6. 提前终止的**预定义分支**（跑 pilot 之前写死）：T=64 → 正常；可复现的系统性 T<64 → 另立 run_id 与替代步数配置，单独报告、绝不与主 run 混用；零星 T<64 → 该样本标记无效并调查原因，不静默改写或补齐。

## 3. smoke20 工程验收（有卡）

- 两模型各 20 题（同 question_id），provisional 标签，跑通 collect→train→eval。
- 明确：**smoke 不报研究指标**；20 题只用来看流程、耗时、失败率、实际 T。
- 记录：每模型失败/重试数（其 collector 失败即整体报错，不静默丢样本）；Dream 是否出现 T < 64 的提前终止（按第 2 步预定义分支处理，见风险 4）。
- 证据：`reports/dynhd_smoke20.json`。

## 4. pilot200 采集（有卡）

- 先各自测 5 题标定 t；再两模型各 200 题（120/30/50 冻结划分），共 400 条 `.pt`，放 `/root/autodl-tmp/dynhd_repro/traces/{llada,dream}/pilot200/`。
- 配置沿用 smoke 通过的实际配置；不同配置必须新 run 目录，不覆盖。
- 记录：加载/单题耗时、显存峰值、实际 T 分布、失败与缺口；给出 `T采集=200*t_llada+200*t_dream+加载/IO` 的表达与实际值。
- 证据：`reports/dynhd_pilot200_collect.json`。

## 5. 标签复核（无卡+人工）

- **事前固定**：剔除规则（拒答/截断/格式失败不进入主指标）与三个报告视图在人工复核开始前写死，复核过程中不改变口径。
- `offline.py label` 提案 → 人工复核 → reviewed 标签（`human_reviewed=true`，human 来源）；**同题不同模型的回答分别判标签**。
- 二元映射：`correct→0`、`incorrect→1`；被剔除样本留档 `excluded/`，有效样本按冻结归属重建索引映射（见第 1 步）。
- 报告三视图：① 全量回答的失败率与覆盖率（拒答/截断/格式失败率作为模型行为指标）；② 有效回答上的检测指标；③ **模型间并列比较时用共同有效题集**（其余情况注明题集差异，防止两模型实际评的是不同难度的题集）。
- 训练前置检查：Stage1 至少 1 条 factual；分层划分 ≥3 条/类；val 两类都有——不足时报告不足，不硬凑。
- 证据：`reports/dynhd_labels.json`（含每个视图的题数）。

## 6. 训练与评测（GPU/CPU）

用**冻结划分**（不用其内部 70/15/15），每模型独立：

```bash
export PYTHONPATH=references/repos/DynHD
.venv-dynhd/bin/python -m dynhd.cli.train_detector \
  --data-path /root/autodl-tmp/dynhd_repro/traces/llada/pilot200 \
  --out-dir /root/autodl-tmp/dynhd_repro/results/llada_pilot200/detector \
  --device cuda --seed 42 --split /root/autodl-tmp/dynhd_repro/splits/pilot200.json \
  --max-steps 64 --prompt-dim 256 --hidden-dim 256 \
  --epochs-stage1 10 --epochs-stage2 30 --batch-size 32 --verbose
.venv-dynhd/bin/python -m dynhd.cli.eval_detector \
  --data-path /root/autodl-tmp/dynhd_repro/traces/llada/pilot200 \
  --ckpt /root/autodl-tmp/dynhd_repro/results/llada_pilot200/detector/detector.pt \
  --split /root/autodl-tmp/dynhd_repro/splits/pilot200.json \
  --split-part test --device cuda
```

- **正式报告要求**（非可选）：3 个训练种子（42/43/44）；每个分区的样本数与类别数；测试集按 question 分组的 bootstrap 95% 置信区间（1000 次重采样）；单类别子集的 AUROC 留空。
- 对照口径与归因限制：同题集、同划分、同标签协议、同 64 步；但**生成管线各自**（DynHD 用其采样器、主表用我们的采集器），指标差异同时含生成差异与检测差异——结论只能写「各自管线的域内结果」，**不得归因于检测器优劣**；严格同生成对照见第 8 步决策。
- 定位限制：200 题（test 50，单题≈2 个百分点）是 pilot，只用于决定是否扩池，不作为稳定结论依据。
- 证据：`reports/dynhd_eval_{llada,dream}.json`。

## 7. 报告与交付（无卡）

- `reports/dynhd_reproduction_summary.md` + `reports/dynhd_reproduction.json`：配置、代码/快照哈希、轨迹数、耗时、显存、失败率三视图、每个分区的样本/类别数、种子与置信区间、**偏差清单**（见下表）、归因限制与规模限制。
- 提交内容：脚本、configs、reports；**不提交**权重、轨迹、结果目录（`.gitignore` 已覆盖 `.venv*`、`results/`；轨迹放 `/root/autodl-tmp/dynhd_repro`）。
- 复现声明用词：只在这个阶段完成后写"方法级复现（缩小规模、标签源不同）"。

## 子集与对照口径（关键决策）

| 项 | DynHD 论文/默认 | 本方案（主表） | 说明 |
|---|---|---|---|
| 题库 | HF trivia_qa rc 前 2000 | 我们的 smoke20 / pilot200 | 同 question_id 是可比前提，但不等于同生成 |
| 生成管线 | DynHD 自带采样器（LLaDA 自实现 / Dream 原生） | 我们的采集器 | 不同管线 → 仅「各自管线的域内结果」，不归因检测器 |
| 提示词 | 原始问题 + 各自 chat template | 仓库冻结 prompt 题面 + 各自 chat template | 与主表一致；记录偏差 |
| LLaDA 步数 | 64 | 64 | 一致 |
| Dream 步数 | config 默认 128 | 64（与主表一致）；可选 128 | 偏差记录 |
| Dream 温度 | config 默认 0.2 | 0.0；alg=entropy，alg_temp=0.0 | 与主表一致；偏差记录 |
| 标签 | GPT-4o-mini judge | 我们的提案 + 人工复核（报告用 reviewed） | 协议差异必须声明 |
| 划分 | 内部 70/15/15（seed 42） | 冻结 120/30/50 | 与主实验对齐 |
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
9. **剔除与 split 冲突**（确定，若按删文件/哨兵标签实现）：上游按现存文件排序且 split 必须全覆盖 → 必须"冻结归属 + 有效样本重建索引映射"。
10. **平台范围**（提示）：本方案按 Linux/AutoDL 写；本地 Windows 运行需重新核实路径、torch、快照与 venv 结论。

## 8. 可选与决策

- 扩到 800–2000 题：按主方案第 8 节扩池后重跑，接近论文规模。
- 跨模型用 DynHD：需先决策共享问题表示的方案（同一句向量编码器替换两模型的 `prompt_emb`，并声明偏差），默认不做。
- 严格同生成对照：让两族检测器作用于同一批生成/轨迹（用 DynHD 采样器重采并让主检测器读同一轨迹，或反之），消除生成差异；工程量大，默认不做，列为决策项。

## 预算与时间（待标定）

| 阶段 | 预计 | 备注 |
|---|---|---|
| 0–1 | 1–1.5 h | 安装 + 官方测试 + CPU 替身 |
| 2 | 0.5–1 h | 两次模型加载（LLaDA 约 1–2 min，Dream 约 2–4 min）+ 最长 prompt 验证 + 对齐抽查 |
| 3 | 0.5–1 h | 40 题工程跑 |
| 4 | 待标定 | 先测 5 题；= 400×t + 加载/IO，参考价以订单为准 |
| 5 | 人工为主 | 400 条复核，是主要瓶颈 |
| 6 | < 0.5 h | 检测器小，可 GPU/CPU；含 3 种子 |

## 红线

- 不修改 `references/repos/DynHD`（保持快照可校验）；所有适配在新脚本里做。
- smoke 不报研究指标；正式数字必须 reviewed 标签；剔除规则事前固定，不改口径。
- 权重/轨迹/结果不入 Git；不在无卡阶段冒称有卡验收。
- 不改冻结 prompt 与冻结划分归属；偏差只记录，不静默放宽。
- 不把「各自管线的域内结果」表述成检测器优劣对比。
