# DynHD 复现方案（当前 32GB 主机）

> v3 · 2026-10-21 · 状态：待评审（v1 初稿 → v2 第一轮复核修订 → v3 第二轮复核修订；未执行）
> 上位文档：docs/VGPU_32GB_完整实验方案.md（第9节增强基线）；论文 arXiv:2603.16459（EMNLP 2026 Findings，MIT 代码）。
> 平台范围：本方案绑定当前 Linux/AutoDL 主机（/root/autodl-tmp、平台 torch、既有快照与 venv 结论）；若改在本地 Windows 运行，路径、torch 与全部验证结论需重新核实。
> 目标定义：**方法级复现** —— 在本机冻结题库/划分与人工复核标签协议下，跑通官方实现的完整管线（采集→证据→训练→评测），得到可与我们主实验对比的域内检测指标；**不是**逐表复刻论文数字（其规模 2000 题、GPT-4o-mini 判分，与本项目不同）。

## Steps

- [ ] 0 环境与接入（无卡）：建 .venv-dynhd、依赖、PYTHONPATH 接入固定快照、跑官方单元测试
- [ ] 1 离线集成与替身验收（无卡）：包装器接口映射、验收子集（最长 prompt）、valid/excluded 目录与分模型 split、CPU 端到端（同一包装入口）
- [ ] 2 有卡单题与对齐验证：按各自 tokenizer 选最长 prompt、显存、Dream shift 抽查、观测无干扰、T 预定义分支
- [ ] 3 smoke20 工程验收（有卡，两模型）：全链路跑通，不产生研究指标
- [ ] 4 pilot200 采集（有卡，两模型共 400 条）：失败诊断留档、新 run 重试、按 question_id 合并
- [ ] 5 标签复核（无卡+人工）：事前固定剔除规则；分模型判标签；valid/excluded 落盘与分模型 split 重建
- [ ] 6 训练与评测（GPU/CPU）：check_valid 入口断言、固定阈值、3 种子、bootstrap 区间、失败率三视图
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

**目录约定（先定死，训练只读 valid/）**：

```
/root/autodl-tmp/dynhd_repro/
  traces/<model>/pilot200/raw/<run_id>/         # 上游直出；每次 run 必须新目录（上游 exist_ok=False）
  traces/<model>/pilot200/valid/                # 复核后有效样本（唯一训练输入）
  traces/<model>/pilot200/excluded/             # 剔除留档
  traces/<model>/pilot200/failures/<run_id>.jsonl
  splits/<model>/pilot200.json                  # 分模型 split
  splits/<model>/index_map.json                 # 索引↔question_id 双向映射
  subsets/<model>_acceptance.jsonl              # 单题验收子集（含最长 prompt 题）
  results/<model>_pilot200/...
```

**`scripts/dynhd_repro/collect_local.py`（包装器）——接口映射必须显式实现**：

| 包装器参数 | 转换到上游 | 说明 |
|---|---|---|
| `--model {llada,dream}` | 选择对应 config | 决定性绑定 |
| `--subset PATH` | 替换 `_load_dataset_items` | 读本地 JSONL（id=sample_id、question、answer=gold_answer+aliases） |
| `--limit N` | 同时向上游传 `--num-samples N` | 保证上游 `len(items)==sample_count` 校验通过；严格返回 N 条，不足即报错 |
| `--dataset triviaqa` | 直通 | 仅为满足上游 argparse choices；真实题库来源写入 meta/run manifest |
| `--labels provisional\|reviewed`、`--labels-file` | 替换 `OpenAIChatLabeler` | config 的 `labeling.method` 保留 `"openai"` 以通过上游校验 |
| `--only-question-ids PATH` | 过滤本地题库 | 失败重试专用 |
| `--run-id ID`、`--output-dir DIR` | 直通 `--output-dir` | 每次 run 新目录 |
| `--num-steps/--gen-length` | 直通 | 主表 64/64 |
| `--split` | 不使用 | 本地子集自带划分，传默认值 |

- 提示词对齐：`_question_content` 换成仓库冻结 prompt 的题面文本（Dream/LLaDA 仍各走 chat template）。
- **元数据修正**：包装 `save_trace_with_prompt_emb`，把上游硬编码的 `labeling_method="openai"`（collect_traces.py:208）改写为真实来源（`offline_match_proposal`/`human_reviewed`）并保留理由字段；自检断言 meta 中不残留 "openai"。
- **失败诊断**（上游失败不保存 .pt，不能靠 relabel 事后留档）：包装两个 sampler 的 `sample` 方法——① 进入前按当前 prompt 反查 question_id，向 `failures/<run_id>.jsonl` 写 `start` 记录并 flush；② 捕获异常 → 写 `{question_id, run_id, stage, exception, actual_T, ts}` 后 re-raise（保留上游失败清单与退出码）；③ 形状校验失败发生在 sample 返回后 → 由 save 前钩子补记。进程被 OOM 杀死时至少留下 start 记录。

**新增脚本**：

- `pick_longest.py`：用**各模型自己的 tokenizer + chat template** 对 pilot200 全量题目渲染最终输入并计长，输出 `<model>_acceptance.jsonl`：每模型 2 题——最长 prompt 一题 + 最短 gold 答案一题（EOS/边界探针），写死 question_id 与 token 长度，选择不依赖文件顺序（smoke20 不保证覆盖最长输入，不作为依据）。
- `make_split.py`：冻结 question_id→划分归属（120/30/50）；为 valid 目录生成 `split.json` 与 `index_map.json`，断言全集覆盖、分区归属一致、无越界。
- `relabel.py`：复核结果落到 `valid/`（复制或硬链接），`excluded/` 留档；重建该模型的索引映射；`correct→0`、`incorrect→1`；剔除不得用删文件或哨兵标签（上游按现存文件排序、split 必须全覆盖、label 只能 0/1）。
- `merge_runs.py`：按 question_id 合并多个 raw run 的成功样本；重复 question_id 默认报错，除非显式 `--prefer <run_id>`；输出合并/去重计数报告。
- `check_valid.py`（训练入口断言，必须先跑）：valid 目录非空；全部样本已 reviewed（无 provisional）；label∈{0,1}；文件排序与 `index_map.json` 完全一致；split 索引 = valid 全集且分区归属正确；打印各分区样本/类别数；任一不过 → 非零退出，不启动训练。
- `report.py`：汇总为 `reports/dynhd_*.json`。

**验收（CPU 替身演练，必须走与正式采集相同的包装入口）**：12 条替身（6/6 两类）+ 人为制造 1 条形状失败 → 断言：12 条落盘；失败诊断 jsonl 含该 question_id；`merge_runs` 去重规则生效；`check_valid` 通过（并在制造 provisional 时按预期失败）；改写后的 meta 不含 "openai"。证据 `reports/dynhd_offline_selftest.json`。

## 2. 有卡单题与对齐验证

单题子集用 `pick_longest.py` 生成的验收子集（不依赖文件顺序）：

```bash
export HF_HUB_OFFLINE=1
.venv-dynhd/bin/python scripts/dynhd_repro/collect_local.py \
  --model llada --config configs/dynhd_repro/llada_local.yaml \
  --subset /root/autodl-tmp/dynhd_repro/subsets/llada_acceptance.jsonl --limit 2 \
  --num-steps 64 --gen-length 64 --run-id single \
  --output-dir /root/autodl-tmp/dynhd_repro/traces/llada/pilot200/raw/single
# 同命令换 --model dream / dream_local.yaml / dream_acceptance.jsonl
```

必须逐项确认（写入 `reports/dynhd_singleq.json`）：

1. bf16 单卡加载成功（不静默 offload）；覆盖**该模型最长 prompt** 的完整 prompt_emb 提取与全部 64 步；记录加载耗时、单题耗时、allocated/reserved 峰值与设备空闲显存；
2. 证据 `features` 形状 `[64,3]`、全部有限、分布合理（与论文的 mean/max/top-k 语义一致）；
3. **Dream hook 对齐抽查**：对同题固定 5 步，用手工 forward 复核 hook 收到的是 shift 后 logits（主项目审计结论：该固定 revision 的 native hook 已是 after-shift；此处只需在 DynHD 采样路径里复现该结论）；
4. **观测无干扰**：同题、同 seed，`feature_extractor=None` 与开启采集的最终 token 必须一致；
5. 生成文本非空、EOS 截断语义正常（沿用其 decode 规则）；记录两题 question_id 与 token 长度；
6. 提前终止的**预定义分支**（跑 pilot 之前写死）：T=64 → 正常；可复现的系统性 T<64 → 另立 run_id 与替代步数配置，单独报告、绝不与主 run 混用；零星 T<64 → 该样本标记无效并调查原因，不静默改写或补齐。

## 3. smoke20 工程验收（有卡）

- 两模型各 20 题（同 question_id），provisional 标签，跑通 collect→train→eval。
- 明确：**smoke 不报研究指标**；20 题只用来看流程、耗时、失败率、实际 T。
- 记录：每模型失败/重试数（其 collector 失败即整体报错，不静默丢样本）；Dream 是否出现 T < 64 的提前终止（按第 2 步预定义分支处理，见风险 4）。
- 证据：`reports/dynhd_smoke20.json`。

## 4. pilot200 采集（有卡）

- 先各自测 5 题标定 t；再两模型各 200 题（120/30/50 冻结划分），共 400 条 `.pt`，直出到 `traces/<model>/pilot200/raw/<run_id>/`。
- 配置沿用 smoke 通过的实际配置；不同配置必须新 run 目录，不覆盖。
- **失败与重试流程**：上游对失败样本不落 .pt 且 `exist_ok=False` 禁止向原目录续跑 → 失败清单来自 `failures/<run_id>.jsonl`；只对失败 question_id 用 `--only-question-ids` 发起**新 run**；全部结束后用 `merge_runs.py` 合并、去重；未解决的缺口必须在报告中列出，不静默丢样本。
- 记录：加载/单题耗时、显存峰值、实际 T 分布、失败/重试/合并计数；给出 `T采集=200*t_llada+200*t_dream+加载/IO` 的表达与实际值。
- 证据：`reports/dynhd_pilot200_collect.json`。

## 5. 标签复核（无卡+人工）

- **事前固定**：剔除规则（拒答/截断/格式失败不进入主指标）与三个报告视图在人工复核开始前写死，复核过程中不改变口径。
- `offline.py label` 提案 → 人工复核 → reviewed 标签（`human_reviewed=true`，human 来源）；**同题不同模型的回答分别判标签**。
- 复核结果经 `relabel.py` 落成 `valid/`，剔除样本留档 `excluded/`，并按冻结归属为该模型重建 `split.json` + `index_map.json`（两模型的剔除情况不同 → 分模型 split，不复用同一份索引）。
- 报告三视图：① 全量回答的失败率与覆盖率（拒答/截断/格式失败率作为模型行为指标）；② 有效回答上的检测指标；③ **模型间并列比较用共同有效题集（且限定在冻结 test 分区内）**。
- 训练前置检查：Stage1 至少 1 条 factual；分层划分 ≥3 条/类；val 两类都有——不足时报告不足，不硬凑。
- 证据：`reports/dynhd_labels.json`（含每个视图的题数）。

## 6. 训练与评测（GPU/CPU）

先跑断言（不通过不训练），再训练；每模型独立目录与 split：

```bash
export PYTHONPATH=references/repos/DynHD
.venv-dynhd/bin/python scripts/dynhd_repro/check_valid.py \
  --model llada \
  --valid-dir /root/autodl-tmp/dynhd_repro/traces/llada/pilot200/valid \
  --split /root/autodl-tmp/dynhd_repro/splits/llada/pilot200.json
.venv-dynhd/bin/python -m dynhd.cli.train_detector \
  --data-path /root/autodl-tmp/dynhd_repro/traces/llada/pilot200/valid \
  --out-dir /root/autodl-tmp/dynhd_repro/results/llada_pilot200/detector \
  --device cuda --seed 42 --split /root/autodl-tmp/dynhd_repro/splits/llada/pilot200.json \
  --max-steps 64 --prompt-dim 256 --hidden-dim 256 \
  --epochs-stage1 10 --epochs-stage2 30 --batch-size 32 --verbose
.venv-dynhd/bin/python -m dynhd.cli.eval_detector \
  --data-path /root/autodl-tmp/dynhd_repro/traces/llada/pilot200/valid \
  --ckpt /root/autodl-tmp/dynhd_repro/results/llada_pilot200/detector/detector.pt \
  --split /root/autodl-tmp/dynhd_repro/splits/llada/pilot200.json \
  --split-part test --device cuda
# Dream 同命令替换路径与 split
```

**统计口径（写死）**：

- **阈值**：主口径固定 0.5。若需按 validation 选阈值，必须预先声明（在 val 上以 F1 选择），test 只评一次；**禁止看 test F1 再调阈值**。
- **3 个训练种子（42/43/44）**：分别报告每种子指标与均值±范围；**不把 3 个种子的预测合并成独立测试样本**。
- **bootstrap**：按 question 分组、只在单一模型的冻结 test 分区内重采样（1000 次）；重采样遇到单类别（AUROC 未定义）时记录并跳过，报告**有效重采样次数/总次数**；单类别子集 AUROC 留空。
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
| 生成管线 | DynHD 自带采样器（LLaDA 自实现 / Dream 原生） | 我们的采集器 | 不同管线 → 仅「各自管线的域内结果」，不归因检测器 |
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
12. **失败样本无 .pt**（确定）：上游失败不保存，`exist_ok=False` 禁止原目录续跑 → 包装写失败诊断 + 新 run 重试 + `merge_runs` 去重合并，缺口显式报告。

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
- 训练只读 `valid/`，且必须先过 check_valid 断言；不向已存在的 run 目录续跑。
- 权重/轨迹/结果不入 Git；不在无卡阶段冒称有卡验收。
- 不改冻结 prompt 与冻结划分归属；偏差只记录，不静默放宽。
- 不把「各自管线的域内结果」表述成检测器优劣对比；test 不参与阈值/超参选择。
