# TRE 在「RTX 4080 SUPER-32GB」实例上的复现方案（v2，现场核验后更新）

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: plan（代码实验复现规划）
- Origin Date: 2026-10-21（v1）；同日 v2 更新
- Verification Status: 本实例硬件、LLaDA FP16 真实单题、TRE 公式实现、原论文数值、仓库接口、references/ 快照均已在**本机实机核验**（证据见附录A/B）；800 题主采集、自动 judge、Dream 仍未执行
- Version Label: tre_repro_4080super32_v2
- 文档性质：执行方案，不是实验完成报告。除附录A记录的一次单题工程验收外，未运行正式采集、未调用 judge、未修改采集代码。
- 当前仓库基线：27f8be1（references/ 主线范围修正后的 HEAD，见附录B）；执行时以实际 git commit 和代码哈希为准。

## 更新摘要（v1 → v2）

| # | v1 状态 | v2 结论 |
|---|---|---|
| 1 | 「4080 SUPER-32GB」标签待实测 | **实测通过**：`NVIDIA GeForce RTX 4080 SUPER`，可用总显存 31.5 GiB（33,796,456,448 B），CC 8.9。见 §0.1 |
| 2 | LLaDA FP16 路线待验证 | **实测跑通**：8,015,581,184 参数全 FP16 加载，64 forward = 64 步，开关观察一致，峰值 15.0 GiB。见 §5、附录A |
| 3 | 论文以本地 PDF `D:/…` 为据 | 该路径为 Windows 路径，本机不存在；改用 arXiv v1（abs + HTML），六格数值与协议已逐条核对。见 §2、§8 |
| 4 | 表 1 的 128/64 含义不明 | 论文 Fig.3 图注明确为 **total diffusion steps**，不是输出长度；输出长度仍未公开。见 §2 缺口4 |
| 5 | EOS/EOT 后位置是否计分不明 | 仍不明，但**已量化其影响**：验收样本中后 EOT 位置占原始 TRE 质量 70.2%。v2 预注册主口径。见 §3、§7 |
| 6 | judge 用 GPT-4o mini，需外部配置 | 本机 `api.openai.com` 不可达；**改用本实例可达的 moma 端点 `deepseek-v4.1-flash`** 作为可执行 judge（已实测），并保留可切换 provider 的实现；差异入 `protocol_diff.md`。见 §4.4 |
| 7 | 题单来源与 split 待定 | `trivia_qa rc.nocontext/test` 的答案为 `<unk>`／无别名，**不可用**（仓库 build.toml 已记录）；现有 raw_qa 全部来自 HF validation split。见 §4.2 |
| 8 | 资源数字 62GB RAM / 50GB 盘 | 实测 503 GiB RAM；`/root/autodl-tmp` 150 GB、可用 119 GB，权重缓存已占 30 GB。见 §10 |
| 9 | — | 新增 `references/`：论文与上游仓库快照，已逐字节核验；提供 prompt/split/judge 口径旁证与 baseline 来源评估。见 §9、附录B |
| 10 | — | references/ 范围经修正（27f8be1）：**六篇主线论文齐全**，**4 个作者仓库**（TraceDet、DynHD、TDGNet、Lost in Diffusion）；**TRE 与 DeMTS 未确认可下载的作者仓库，已明确记录、不用其他代码替代**。见附录B |
| 11 | — | 新增同源实现旁证（§2.1）：DeMTS 与 TRE 作者重叠且公开了生成与标注协议，TraceDet/DynHD 提供步数、prompt 与 judge 口径参照；TRE 论文 PDF 已随仓库自包含（= arXiv v1，哈希一致） |

---

## 0. 两个前提的结论

### 0.1 实例标签与实际显存（已闭环：通过）

NVIDIA 标准版 RTX 4080 SUPER 为 16GB；本实例实测为 **31.5 GiB** 可用总显存的单卡，满足正式路线的显存前提。实测记录（2026-10-21）：

- `nvidia-smi`：`NVIDIA GeForce RTX 4080 SUPER`，32760 MiB，驱动 595.71.05（界面 CUDA 13.2），无其他进程占用。
- PyTorch：`torch 2.8.0+cu128`，runtime CUDA 12.8，`torch.cuda.is_available()=True`，capability `(8, 9)`，`mem_get_info()=(33,526,841,344, 33,796,456,448)`，`is_bf16_supported()=True`，FP16 matmul 有限值。
- 型号仍按平台商品名记录；非标配置不改变结论，但**不据此推断带宽、独占程度或与标准 16GB 版一致的性能**。

### 0.2 TRE 原文是 FP16，不是 BF16（已闭环：原文确认 + 本机可运行）

原文附录 C.4 明确写 float16 加载；temperature=0，top_p/top_k 不设，cfg_scale=0.0（arXiv v1 HTML 原文核对）。同时本实例已实机跑通 LLaDA FP16 单题（附录A）。因此：

- **主路线A：原文对齐复现。** LLaDA FP16，不量化、不训练基座。
- **路线B：BF16 实现变体。** 单独记录为差异实验，不称为原文配置。BF16 在本卡也可用，作为 FP16 出问题时的对照。
- **Dream FP16 当前是阻塞项。** 固定版本原生 entropy 排序在 FP16 下可能因 epsilon 下溢出现 NaN；采集器在 CLI 与运行时 hook 双重拒绝（`validate_precision` + `logits_hook`），且 Dream 原生 sampler 源码以 sha256 锁定。不得关闭保护直接跑，也不得用 T4 NF4 数据替代；Dream 只有在解决该实现差异后才进入同精度正式复现。

---

## 1. 目标与复现层级

| 层级 | 交付 | 能说明什么 |
|---|---|---|
| R0 工程验收 | 真实 FP16 单题、20题轨迹，公式与位置抽查 | 模型与采集/评分路径可信；不能说明论文 AUROC 已复现。**单题部分已完成（附录A），20 题与位置抽查待做** |
| R1 核心结果复现（第一目标） | LLaDA + TriviaQA，尽量对齐的 800 题初始池与 judge 过滤，TRE AUROC | 单模型单数据集结果；所有未对齐项必须披露 |
| R2 核心 TRE 主表扩展 | 两模型、三数据集、原表 128/64 两个步数预算的 TRE 行 | TRE 核心主表结果；不等于已复现所有比较方法 |
| R3 完整论文实验 | 各类 baseline、表 2/3 消融、效率和敏感性实验 | 需要额外特征、训练、重复采样与独立预算 |

首轮停止点定为 R1。TRE 不需要 train/dev 拟合、LR/MLP 训练或跨模型迁移矩阵（现行 `offline.py evaluate` 是那套流程，见 §7）。本计划不把 pilot200（120/30/50）设为前置条件。

---

## 2. 原文依据与尚未公开清楚的项

**论文来源（v2 更新）**：arXiv:2607.22661v1，标题 *TRE: Training-Free Hallucination Detection for Diffusion Language Models*，v1 日期 2026-06-29，许可 CC BY 4.0。

- 入口：<https://arxiv.org/abs/2607.22661>；正文：<https://arxiv.org/html/2607.22661v1>（本机实测可达，用于逐条核对协议与表 1/2/3 数值）。
- 论文副本已随仓库自包含：`references/papers/2607.22661_TRE.pdf`，sha256 `a682389e…cdfe6`，**与 arXiv v1 原始 PDF 逐字节一致**（本机复核，见附录B）；该哈希正是 v1 方案里 `D:/…` 所引用的同一文件，Windows 路径不再需要。
- `references/CODE_AVAILABILITY.md` 记录：截至 2026-10-21 **未确认 TRE 可下载的作者仓库**（论文正文无代码链接；GitHub 题名与已知共同作者检索未见对应实现）。状态是「未找到」而不是「确定未开源」；本项目 `src/trace_schema.py` 是独立公式实现，不是作者源码。
- 论文 HTML 未声明开源，也不等于作者没有公开代码；但**不能假定可复用官方 TRE 代码与固定题单**。

| 项目 | 原文已确认 | 本方案的处理 | 核验状态（v2） |
|---|---|---|---|
| 模型 | LLaDA-8B-Instruct、Dream-7B-Instruct | 先LLaDA，Dream独立验收 | 已确认 |
| 数据集 | TriviaQA、HotpotQA、CommonsenseQA | 首轮TriviaQA，后补另外两者 | 已确认 |
| 题量 | 每个 benchmark 从官方 evaluation split 随机取 800 问答 | 800 是初始题池；judge 过滤后可能少于 800，不补题凑数 | 已确认（C.4） |
| 精度 | float16 | 主路线 `--precision float16` | 已确认并实机跑通 |
| 采样 | temperature 0；top_p/top_k 未设；cfg_scale 0.0 | 与当前 LLaDA greedy/CFG0 路线一致 | 已确认 |
| 打分 | 一次生成的去噪熵，无检测器训练 | 原始 TRE 作主分数，不用长度归一化版替换 | 已确认 |
| 标签 | GPT-4o mini 语义一致性判断；初判错误再判一次；不一致剔除 | 单独实现 judge 流程，保存两次原始判定 | 已确认；judge 模型改为本机可达者（§4.4），记为差异 |
| 主指标 | AUROC（表 1 以百分数展示） | 另附 AP/95%CI 作补充，不混称论文原指标 | 已确认 |
| 原硬件 | 单卡 Quadro RTX 6000 24GB，顺序运行 | 替换成经实测的 31.5 GiB 单卡；性能不可直接归因于算法 | 已确认 |
| 128/64 列 | Fig.3 图注称其为 **total diffusion steps** | 不得解释为输出长度；steps 与 gen_length 的组合仍未公开 | **已收窄** |

**正式 800 题采集前必须解决/登记的协议缺口（v2 更新）：**

1. **evaluation split 具体指哪个 config/split。** 已查明一部分：`trivia_qa` 的 `rc.nocontext` **test split 全部为 `<unk>`／无别名，不可用**（`configs/datasets/build.toml` 有记录）；同社区、同模型、同数据集的 DynHD 实现使用 **validation split**（`trivia_qa/rc`、`hotpot_qa/distractor`、`commonsense_qa`）。仍不能确定原文用的是哪一个 split 的哪一批 ID，**结论与选择必须写进 `protocol_diff.md`**。
2. 原作者 800 题 ID 与抽样 seed 是否可得；若不可得，固定自选 seed 并公开 ID 清单，报告题单差异。
3. 精确 prompt、是否提供 Hotpot 上下文、CSQA 选项格式、chat template 与答案格式。**旁证**：DynHD 对 LLaDA 用「裸问题 + chat template」，无额外指令前缀；CSQA 用「Choose the best option and output only its letter (A–E).」+ 选项块。本项目现行 prompt v1 含 `Answer the question with a short factual answer.` 前缀，属于自定义清洗的一部分，**与两条旁证都不完全一致**，须显式选择并登记。
4. 表 1 中 128/64 列的实际生成预算：已确认是**总扩散步数**；对应 steps、gen_length、block、各模型揭示策略仍未公开（旁证：DynHD 默认 `gen_length=128`，LLaDA `num_steps=64`、Dream `num_steps=128`；本采集器要求 `steps ≤ gen_length`）。不能把这组数字直接当输出长度。
5. EOS/EOT 之后位置是否纳入分数、是否丢掉空/截断回答、原文熵实现精度与 mask/reveal 时点。**该缺口影响很大，已量化**（§3、§7）。论文正文未出现 EOS/truncation 相关描述。
6. judge 的精确提示词、可固定的模型 snapshot、调用参数及异常输出处理。原文只说明「问题 + 参考答案 + 生成回答 → 语义一致性」并给出二次判定规则，未给提示词；DynHD/DeMTS/TraceDet 的公开实现与提示词可直接参考（§2.1、§4.4）。

### 2.1 同源实现旁证（v2.1 新增，用于减少协议歧义，不是 TRE 作者协议）

以下三项均来自 `references/` 快照，可在 `protocol_diff.md` 中作为「我们为什么这样选」的依据；**它们不能替代原文未公开的设定**，采用哪一项必须在报告里写明。

| 实现 | 与 TRE 的关系 | 生成/采样 | prompt 与答案格式 | 标签来源 |
|---|---|---|---|---|
| **DeMTS**（2608.14632v1，作者含 Yue Tan / Yanyu Qian / Yixin Liu，与 TRE 重叠） | 同作者群的近邻工作，协议最可能接近 | 每数据集 1600 train + 200 val + 200 test，seed 42；**去噪步数 64 或 128**；逐步记录 token-wise 预测熵与 token ID（与 trace-v1 的信息粒度相同） | TriviaQA：`Answer the question concisely. … Question: {q}`；HotpotQA：给定 `{context}` 并要求「只用上下文作答」；CSQA：选项 A–E + 「只选一个、输出 `<answer>X</answer>`」；全部答案用 `<answer></answer>` 包裹 | **Qwen3-8B** 自动判定 hallucination（TriviaQA/HotpotQA），CSQA 用规则匹配；标注提示词已在附录 E.2 公开 |
| **TraceDet**（2510.01274，TRE 表 1 的监督 baseline） | 同类方法，代码已入库 | 生成轨迹逐 token 熵；检测器训练 | 开放域 QA 用外部 judge | **Qwen3-8B** 作外部 judge，并报告与人工一致性（TriviaQA 90%、HotpotQA 84%）；多选题用直接比对 |
| **DynHD**（2603.16459） | 同社区方法，代码已入库 | LLaDA：`num_steps=64`、`temperature=0`；Dream：`num_steps=128`、`temperature=0.2`、`alg=entropy` | LLaDA 用「裸问题 + chat template」，无指令前缀；CSQA 用字母格式 | **GPT-4o mini**（`temperature=0`、`max_retries=3`），提示词公开在 `repos/DynHD/dynhd/labeling/openai_gpt4omini.py` |

要点：

- 三条旁证都把 **64/128 当作去噪步数**，且都出现「每步记录 token 级预测熵」的做法，与 §3 的口径一致；**gen_length/block 仍未在任何一篇里明确**，缺口 4 只能部分收窄。
- **prompt 的三种写法互不相同**（DeMTS 的 `<answer></answer>`、DynHD 的裸问题、我们 prompt v1 的短答指令），说明 prompt 在不同论文间本就不统一；原文未公开，只能选择一种并登记差异。
- judge 侧：**四篇里两篇用本地 Qwen3-8B，两篇用 GPT-4o mini**（DynHD/DeMTS/TraceDet 已在 §2.1 列明，TRE 用 GPT-4o mini）。这为 §4.4 的 judge 选择提供了旁证：本地可固定的开源 judge 在本领域是常规做法。

找不到的项写进 `protocol_diff.md`，不能填成「与原文一致」。可以继续做明示差异的协议近似复现；不能升级为完全一致的数值复现。不要先花大量 GPU 采集，再发现 prompt 或标签口径错了。

---

## 3. TRE 定义和实现检查

令 H[t,i] 是第 t 步、揭示前对位置 i 的预测分布的自然对数熵，R[t] 是本步实际从 MASK 变成非 MASK 的位置：

$$
S_{TRE}=\sum_{t=1}^{T}\frac{t}{T}\sum_{i\in R_t}H_{t,i}.
$$

检查要点（v2 逐条核验）：

- t 从 1 开始；T 是实际观测步数，另记请求预算与实际 forward 次数。**已核验**：manifest 记录 `steps`（实际观测）与 `requested_steps`，`actual_forward_count` 与步数相等（64/64 验收中 64 == 64）。
- 本步新揭示 token 的熵先求**和**，不是每步平均；仅一次原始生成，不为 TRE 额外采样。**已核验**：实现为 `sum_t (t/T) * Σ_{i∈R_t} H`，与论文式(3)的「质量和而非平均」一致。
- 预测分布在采样噪声、temperature 和 top-k/top-p 变换前观察；不修改原始 logits/原始解码顺序。**已核验**：`entropy_distribution` 记录为 `FP32 predictive logits before sampling transforms`；`logits_statistics` 在 GPU 内 FP32 归约，NaN/+inf/全掩码行直接报错。
- Dream 先确认 hook 处已经 shift，不能重复 shift；LLaDA 使用自身位置对齐。**已核验**：Dream hook 走 `already_shifted=True` 且与锁定源码 sha256 比对；LLaDA 记录 `logit_alignment=identity`。
- `extract_features(...)["tre"]` 对**全部生成位置**按公式计算；`tre_effective`（仅有效回答位置）与 `tre_length_normalized` 是不同变体，单独报告。**已核验**并已量化差异：验收样本 T=64、有效长度 L=5，`tre=7.370904` 对 `tre_effective=2.199339`，**后 EOT 位置贡献 70.2% 的原始质量**。另注意 64 步/64 长度配置下每步恰好揭示 1 个 token（`revealed.sum(axis=1)` 全为 1），因此式(3)的质量和与平均在该配置下等价；步数大于长度或 block 配置变化时不再等价。
- 当前统计用 FP32，在 FP16 基座上计算；记录统计 dtype。原作者若使用不同计算精度，也进入差异清单。
- 当前 trace-v1 只接受单调揭示（`reveal & ~mask`、重复揭示、mask 迁移不一致都会报错）；原文敏感性实验提到 remasking 策略，不能据此用该契约伪造重掩码轨迹。相关扩展另做方案。**旁证**：`references/repos/DynHD` 的 LLaDA sampler 自带 `_remask_step`，`references/repos/RemeDi` 是专门的重掩码工作，可作为将来扩展的参考实现。

**预注册口径（避免事后挑选）**：原文未定义 EOS/EOT 后位置与有效长度处理。为避免用目标 AUROC 反选口径，R1 主分数固定为**原始 `tre`（全部生成位置）**，`tre_effective`/`tre_length_normalized` 作为并列报告的稳健性变体；两者都在 `scores.csv` 中保存，主表口径一旦冻结不得因结果好坏更改。

本地单测手算例：两步的揭示熵分别为 2 和 3，则 TRE=0.5×2+1×3=4。**真实轨迹上另做了一次独立复算**（不调用 `extract_features`，直接按公式求和），数值与实现完全一致（附录A）。

---

## 4. 无卡阶段A：数据、协议、环境与 judge 准备

### 4.1 代码和存储（实测更新）

```bash
cd /root/autodl-tmp/dllm-cross-model-hd   # 本实例实测路径；换机器先 df -h / free -h
git status --short
git pull --ff-only                        # 现已可拉到 27f8be1
git rev-parse HEAD
uv sync --locked
uv run pytest                             # 实测 82 通过
```

- 本实例实测：RAM 503 GiB；`/root/autodl-tmp`（`/dev/md0`）150 GB、可用 119 GB；根分区 overlay 30 GB、可用 25 GB。**不要把小分区当持久盘**。
- **权重已就绪，不需要联网下载**：`HF_HOME=/root/autodl-tmp/hf-cache`（30 GB），LLaDA 6 分片与 Dream 4 分片按 `configs/models/*.json` 的固定 revision 缓存，逐文件哈希已复核。运行采集时建议 `HF_HUB_OFFLINE=1`。
- 本实例网络实测：`arxiv.org`、`pypi.org`、`github.com` 可达；**`huggingface.co` 与 `api.openai.com` 不可达**。若确需重新下载数据集/权重，用镜像并登记：`export HF_ENDPOINT=https://hf-mirror.com`（实测可达）。
- 仅当缓存缺失时才需要下载；模型文件不提交 GitHub。

### 4.2 准备复现题单（待执行工作）

新建独立目录 `data/tre_repro/`；不要修改已冻结的跨模型研究池（`data/raw_qa/`、`data/manifests/pilot200.json`）。每条保持现有 QARecord 所需字段（question_id、sample_id、cluster_id、dataset、split、question、gold_answer/aliases、prompt、source 等），并保存原始来源 revision/config/source_split/行号。

- `questions/triviaqa_eval800.jsonl`：新的复现评测题单，split 统一 `test`（采集器只接受 train/validation/test/smoke）。
- `questions/smoke20.jsonl`：工程专用，不纳入正式 800 题评分。**建议从 TriviaQA 重建一份**，使 R0 验收与 R1 同分布、同 prompt 口径。
- `questions_manifest.json`：raw SHA、ID 清单、抽样 seed、prompt 与过滤规则。

**题池事实（本机核验）**：

- `data/raw_qa/triviaqa/{train,validation,test}.jsonl` = 5900/1483/2532 条，**全部来自 HF `trivia_qa` `rc.nocontext` 的 `validation` split**（共 9915 条，全部有金标）；三条文件只是仓库自己的 60/15/25 cluster 划分，**不是** HF 的 train/validation/test。hotpotqa 同理（4019/998/1654，`distractor` validation）。
- 该池已做自定义清洗：85% Jaccard 去重、重复行折叠（TriviaQA validation 17,944 → 9,960 行）、ID 撞车聚簇、**gold-in-prompt 剔除（25,349 行中剔除 790）**、smoke20 先于划分切出。直接拿它抽 800 题属于协议变化。
- 若为接近原文从 raw 重新抽样：本机**没有** `data/raw_download/`（被 .gitignore），需经镜像重下并保留 raw revision/行号；保留自然题面/选项，不擅自执行额外 gold 筛除；另做泄漏/题型诊断。
- **补充口径建议**：把「与 DynHD 一致（validation split、自然题面）」和「与原文一致的未知 split」两种选择写进 `protocol_diff.md`，不要混用；每个比较方法必须使用完全相同的回答与过滤后题目集合。
- **prompt 与答案格式（三条互斥选项，必须写明）**：① 沿用本项目 prompt v1（`Answer the question with a short factual answer.`）；② 采用 DeMTS 的写法（同作者群、最接近原文：TriviaQA `Answer the question concisely.`、HotpotQA 给 `{context}` 并要求只用上下文、答案统一包 `<answer></answer>`）；③ 采用 DynHD 的裸问题。选定后连同**答案抽取规则**与**有效长度/EOS 口径**一起冻结（②会改变文本抽取方式），并在 `protocol_diff.md` 记录未选的两项。HotpotQA 是否提供上下文同样在此决定（DeMTS 提供、TRE 未说明）。
- **.gitignore 需补一条**：现有 `data/labels/` 规则不覆盖 `data/tre_repro/labels/`，`judge_raw.jsonl`（含完整回答与 judge 原文）可能被提交；正式采集前加上忽略规则，只把小型清单入库。

### 4.3 推理环境（实测版本）

原 CPU `.venv` 不装 torch（`pyproject.toml` 明确不声明）；推理用 `.venv-llada`、`.venv-dream`，以 `--system-site-packages` 继承平台 torch，venv 内不装 torch。

| 环境 | 实测 |
|---|---|
| `.venv-llada` | Python 3.12.3、torch 2.8.0+cu128、transformers 4.46.3、CUDA 可用 |
| `.venv-dream` | torch 2.8.0+cu128、transformers 4.46.2 |
| `.venv`（CPU 工具/离线分析） | `uv run pytest` 82 通过 |
| `.venv-collector-test`（采集器验收，含 CPU torch） | 100 项，另有 `scripts/verify_collectors_cpu.py` 端到端 |

依赖候选 `requirements/collector-llada.txt`、`requirements/collector-dream.txt`；**保留平台 CUDA torch，不能安装 CPU 测试 torch 覆盖它**。真实 CUDA/BF16/FP16 检查以有卡实测为准（本轮已完成 FP16 检查）。

### 4.4 judge：本机可执行的等价实现 + 差异登记（v2 重写）

论文 judge 不是当前的别名匹配器（`src/labeling.py`），也不是要求所有样本人工签字的跨模型主评测口径。

**论文对齐流程（不变）**：

1. 给 judge 问题、全部可接受参考答案、完整待评回答，请其判断语义正确性（关注事实而非表面重叠）。
2. 初判 correct：保留，y=0。
3. 初判 incorrect：用相同输入再独立判一次；两次均 incorrect 才保留，y=1。
4. incorrect→correct：剔除，保留两次原始记录和原因。
5. 无法解析、调用失败或未知判定：进入待处理状态，不能自动当 incorrect、不能静默跳过。

**judge 模型的三条可选路线（v2.1 新增，择一并登记）**：

| 路线 | 与原文关系 | 可行性（本机实测） | 代价 |
|---|---|---|---|
| A 本地 Qwen3-8B | 与 TRE 不同，但**与 DeMTS、TraceDet 的做法一致**（§2.1） | 未实测，但 8B FP16 约 16 GB 显存，本卡可容纳；权重需经镜像下载并固定 revision | 需自建服务与提示词；完全离线、无 API 依赖、可固定 snapshot |
| B moma 端点 `deepseek-v4.1-flash` | 与 TRE 不同（模型/供应商/版本均不同） | **已实测可达**：temperature=0、支持 JSON 输出、单次 0.5–2.1 s、4 路并发正常 | 依赖本机网络与用户凭据配额；无不可变 snapshot，需记录调用时间与原始响应 |
| C GPT-4o mini（原文） | 原文口径 | 本机 `api.openai.com` 不可达且无密钥 | 需要代理或其他机器 |

选择原则：主表只用一个 judge 并写明；若能拿到第二路，则在固定 100 题子集上做**跨 judge 一致性检查**作为补充证据（不改主表口径）。无论选哪条，**TRE 原文 judge 的提示词仍未公开**，我们的提示词必须自行冻结并存档，不能声称与原文相同。

**路线 B 细节（若选 moma）**：`POST https://zhenze-huhehaote.cmecloud.cn/v1/chat/completions`，`model=deepseek-v4.1-flash`，`temperature=0`，支持 `response_format={"type":"json_object"}`；单次判定约 0.5–2.1 s，4 路并发正常；响应含 `reasoning_content`（推理 token 会占用输出与费用），解析须宽容。凭据从环境变量读取（例如 `MOMA_API_KEY`），**密钥不写入仓库、不写入本 MD**；本机该凭据存在于 opencode 凭据库，脚本可读取但不得提交其值。

- 该选择是**明确的 judge 差异**：模型、版本、供应商、提示词均与论文不同，必须写入 `protocol_diff.md`，并在报告里说明「标签集合因此可能与原文不同，数值不可直接与表 1 等号对齐」。
- 端点没有类似 `gpt-4o-mini-2024-07-18` 的不可变 snapshot：记录 `model` 字符串、端点、调用时间，保存全部原始响应；建议对固定小样本（如 100 题）在采集前后各判一次，检测服务端漂移。路线 A 的 Qwen3-8B 反而可以固定到 HF revision，这一点优于路线 B。
- 参考实现：`references/repos/DynHD/dynhd/labeling/openai_gpt4omini.py`（MIT）已给出参数化客户端（model / base_url / temperature / max_retries / timeout、保存判定理由、提示词「…is the proposed answer correct? … respond only with "yes" or "no"」）；`references/papers/2608.14632_DeMTS.pdf` 附录 E.2 则给出 Qwen3-8B 的完整判定提示词（流利性/相关性/支撑性/精确匹配/语义匹配/未知答案六条规则）。可照此结构实现，但**提示词必须自行冻结**，不能假定与论文相同。
- **建议增设一致性小测**：用第二路 judge（路线 A 或路线 B 中未选的那个）对同一批 100 题独立判定，报告标签一致率与不一致样本。这是补充证据，不改主表口径。
- 外部调用与费用需在实际执行前配置；本 MD 不调用 API、不含密钥。人工抽查可作为标签质量补充，但未经单独标注，不覆盖论文 judge 主表。

**预先约定结构**：`paper_judgments.jsonl` 每行包含 sample_id、question_id、judge_first（correct/incorrect）、judge_second（初判 incorrect 时必须有）、`status`（done/needs_review）、以及 judge 来源元数据（model、base_url、temperature、prompt_sha256、请求/响应原文、时间、token 用量）。不要为了绕过当前评估器而伪造 `human_reviewed=true`。

---

## 5. 有卡阶段B：硬件与 FP16 单题验收（已部分执行，记录在案）

探针（已执行，附录A）：

```bash
nvidia-smi
.venv-llada/bin/python - <<'PY'
import torch
print('torch', torch.__version__, 'runtime CUDA', torch.version.cuda)
assert torch.cuda.is_available()
print('device', torch.cuda.get_device_name(0))
print('capability', torch.cuda.get_device_capability(0))
print('free,total', torch.cuda.mem_get_info())
x = torch.ones((32, 32), device='cuda', dtype=torch.float16)
print('FP16 matmul finite', bool(torch.isfinite(x @ x).all()))
PY
```

已执行的单题命令（**工程验收，不是论文协议**：用的是现有 `smoke20.jsonl` 第一题（HotpotQA）与 prompt v1）：

```bash
env HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1 \
.venv-llada/bin/python scripts/collect_llada.py \
  --questions data/raw_qa/subsets/smoke20.jsonl \
  --output <新的空目录> \
  --precision float16 --gen-length 64 --steps 64 --block-size 64 \
  --limit 1 --verify-observer
```

观察开/关同 seed 的最终 token 必须相同（`observer_verified` 落盘）；核对 pre-reveal 熵、mask、reveal、EOS/EOT 与文本；至少抽查实际步。加载耗时、峰值显存和单题时间由 manifest 记录，不能拿 T4 NF4 的约 14 秒/题直接估 FP16 吞吐。

**R0 剩余工作（正式采集前）**：用 4.2 的 `smoke20`（TriviaQA、冻结 prompt）重跑单题并留档；跑整份 20 题；人工抽查 ≥5 条；对 ≥3 题做位置/时点抽查（逐步核对 mask/reveal/EOS 与文本）；把结果写入 `reports/tre_repro/`。

若实际换到 16GB 设备：不直接启动正式 800 题任务，先记录失败配置，或明确转为量化/卸载变体，不悄悄改变正式复现协议。

---

## 6. 有卡阶段C：20题与正式采集

单题通过后，**换新输出目录**跑完整 smoke20（去掉 `--limit`）；题单签名改变不可 resume 进单题目录（已实测：改变 `--limit` 后 `--resume` 报 `run config/input/environment/code fingerprint changed`；同参数重跑则 `All samples already validated; no model loaded.`）。人工抽查至少 5 条、重复至少 3 题，确认错误/空/截断有可解释记录。

协议缺口登记完成后，正式 800 题命令如下；示例 64/64 必须换成已冻结的论文参数（见 §2 缺口4）。若确认原协议不是此配置，先改命令/运行记录，再采集：

```bash
env HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1 \
.venv-llada/bin/python scripts/collect_llada.py \
  --questions data/tre_repro/questions/triviaqa_eval800.jsonl \
  --output data/trajectories/tre_repro/llada_triviaqa_fp16_protocolA \
  --precision float16 --gen-length 128 --steps 64 --block-size 128
```

（`--gen-length/--steps/--block-size` 为占位示例：`steps` 必须 ≤ `gen_length` 且能被块数整除；冻结值以 §2 缺口4 的结论为准。）

- `--verify-observer` 先在 smoke 检验，不默认把正式每题再生成一遍（它会把生成时间加倍）。
- 固定参数后中断重启可加 `--resume`；输入、环境、code hash、precision 等改变会拒绝恢复。损坏已提交轨迹不静默重算（`committed trace missing or hash mismatch`）；强杀残留锁需确认旧进程结束后人工处理。
- 若 OOM：先确认 batch1、单模型、无梯度、无全词表历史或 attention 缓存、没有其他 GPU 进程。不要静默改 NF4、CPU offload、输出长度或 block 后仍称原配置复现。资源不足时记录失败配置并换资源，或明确转为变体实验。
- **吞吐实测**：64 步 × 8B FP16 单次生成约 1.26 s（含 observer 的双次生成共 2.52 s），峰值约 15.0 GiB。按此估算单模型单数据集 800 题约 20 分钟量级；128 步、更长输出按比例上升。正式前仍以 smoke 均时为准。

---

## 7. 无卡阶段D：打分、标注和统计

回传 run 目录、生成文本和 manifest，核对 SHA。对同一批生成回答执行 4.4 的 judge 流程。TRE 主分析不需要 train/dev，也不需要先训练 LR/MLP。

**当前 `offline.py evaluate` 不能直接当 TRE 论文复现入口（已核验）**：`validate_frame` 强制「exactly two backbones」；`eligible()` 只收 `human_reviewed=true` 的 correct/incorrect；`extract()` 要求真实标签 `label_source=human:<reviewer/run>`；`evaluate` 默认要求全表 BF16（`--allow-nonbf16` 仅为调试/量化隔离）。单模型自动 judge 评测应独立计算，不添加假目标模型、假训练集或假人工标签绕过限制。

可复用：`src.trace_schema.load_trace`、`extract_features(...)["tre"]`、`src.evaluation.binary_metrics/grouped_bootstrap`。下面是独立评分的参考片段（需先有全部真实轨迹与合法 judge 文件；保存为新脚本时应补齐输入与 schema 测试）：

```python
import json
from pathlib import Path
import numpy as np
from src.trace_schema import load_trace, extract_features
from src.evaluation import binary_metrics, grouped_bootstrap

run = Path('data/trajectories/tre_repro/llada_triviaqa_fp16_protocolA')
judgments = [json.loads(line) for line in Path(
    'data/tre_repro/labels/paper_judgments.jsonl').read_text(encoding='utf-8').splitlines()]
assert len({r['sample_id'] for r in judgments}) == len(judgments)
by_id = {r['sample_id']: r for r in judgments}
assert all(r['status'] == 'done' for r in by_id.values()), 'needs_review 必须单独处理，不能当 incorrect'
y, scores, scores_eff, qids, dropped, seen = [], [], [], [], [], set()
for path in sorted((run / 'traces').glob('*.npz')):
    meta, arrays = load_trace(path)
    assert not meta.get('synthetic', False) and meta['precision'] == 'float16'
    r = by_id[meta['sample_id']]
    assert r['question_id'] == meta['question_id']
    seen.add(meta['sample_id'])
    first = r['judge_first']
    assert first in ('correct', 'incorrect')
    if first == 'incorrect':
        assert r.get('judge_second') in ('correct', 'incorrect')
        if r['judge_second'] == 'correct':
            dropped.append(meta['sample_id'])
            continue
    f = extract_features(meta, arrays)
    y.append(int(first == 'incorrect'))
    scores.append(f['tre'])                # 预注册主口径：全部生成位置
    scores_eff.append(f['tre_effective'])  # 并列报告的稳健性变体
    qids.append(meta['question_id'])
assert seen == set(by_id), 'judge/trajectory coverage mismatch'
assert len(set(y)) == 2, 'AUROC requires both classes'
print(binary_metrics(y, scores))
print(binary_metrics(y, scores_eff))
print(grouped_bootstrap(y, scores, qids, repeats=1000, seed=20261021))
print('kept', len(y), 'judge disagreements', len(dropped))
```

主表同时报告：初始 N、完成 N、初判 correct/incorrect、二判分歧剔除数、待处理数、保留 N、正负类数、AUROC、95%CI，以及 `tre` 与 `tre_effective` 两种口径。AP 只作补充；正类统一为幻觉/incorrect，TRE 越大风险越高。未完成 judge 的样本不能直接排除后当作完整 800 题结果。

将每题 score、judge 原始记录、过滤原因及结果 CSV 另存文件。bootstrap 按 question_id 抽样，作为本次补充统计；如原作者未报告 CI，不将我们的 CI 说成原论文标准。不能用目标 AUROC 来反向选择 prompt、题单、EOS 口径、主分数口径或最好 seed。

---

## 8. 与论文表 1 比较

下表为 arXiv v1 表 1 的 TRE 行（百分数；已逐格核对）。预算标签沿用原表含义（总扩散步数）：

| 模型 | 数据集 | 原表128列 | 原表64列 |
|---|---|---:|---:|
| LLaDA-8B-Instruct | TriviaQA | 82.2 | 86.5 |
| LLaDA-8B-Instruct | HotpotQA | 85.6 | 88.1 |
| LLaDA-8B-Instruct | CommonsenseQA | 79.0 | 75.0 |
| Dream-7B-Instruct | TriviaQA | 83.9 | 84.8 |
| Dream-7B-Instruct | HotpotQA | 80.6 | 81.0 |
| Dream-7B-Instruct | CommonsenseQA | 77.7 | 78.4 |

每格比较须列明：原文值、本次值、差值（百分点）、本次CI、保留样本数和协议差异（含 split、prompt、judge、EOS/口径、steps/gen_length）。不能因为「落在±2个百分点」就自动宣布成功；也不因单次偏差就认定方法无效。题单、judge、prompt、版本、位置对齐和样本正例率均可解释差异，应逐项核查，不为凑数调测试集。

R1 完成后，先扩 LLaDA 的两个其他数据集与另一预算，再解决 Dream 并扩展。按两个模型×三个数据集×两个步数预算、每格初始 800 题估计，TRE 核心表可能需要 9600 次主生成；未包含 smoke、复验、多采样 baseline 或失败重试，不能把此数当完整论文总成本。

---

## 9. 消融与完整论文范围

先验证公式与位置，不直接套用跨模型工程的特征消融表当作论文表 2/3。

- 空间消融：all/unrevealed/revealing/revealed token evidence；按原文式(2)和表 2/3 核对时间窗口及聚合定义。**旁证**：论文表 2/3 的变体名与数值已核对（LLaDA：All tokens / Unrevealed / Revealed / Average / Exponential / Hard last-30% / TRE）。
- 时间消融：average/exponential/hard last-30%/linear TRE；先确认指数权重及边界处理，不能凭名称猜公式。
- 长度、步数、remasking：需要新生成且可能需要新轨迹契约（trace-v1 只支持单调揭示），独立预算。
- 原表 CCS/TSV/TraceDet 等监督方法需要自己的训练协议；Semantic Entropy/Lexical Similarity 等可能需要多次生成，不能由一次 TRE 轨迹「顺手复现」。
- **代码来源现状（v2.1）**：
  - 已入库作者代码：**TraceDet**（MIT，表 1 的监督 baseline；`train_main.py`/TimeHalu 需用生成轨迹训练，其 `DLLM_generate/` 与 `metric_qwen.py` 给出生成与 Qwen judge 参考）、**DynHD**（MIT，轨迹熵 + 参考轨迹检测器，论文当时无代码）、**TDGNet**（MIT，第一作者仓库）。
  - **TDGNet 需要的信息量远大于 trace-v1**：它消费 attention 与 hidden-state 关键帧（K 个 `[N,N]` 注意力 + `[N,D]` 隐藏状态，T+1 个快照），需另建采集 profile，不能由现有熵轨迹推导。
  - **TRE 与 DeMTS 未确认可下载的作者仓库**（`references/CODE_AVAILABILITY.md`），本轮不用其他代码替代。
  - **CCS / TSV / EigenScore 属于通用（非 dLLM 专用）baseline**：CCS/TSV 是隐层表征类方法，EigenScore 需要多次采样，均不在 `references/` 内，若要复现须另做实现与资源审计。
  - Lost-in-Diffusion（含 LLaDA 解码参考实现）、FActScore、LongFact/SAFE、RemeDi 作为参考保留（非本轮六篇主线）。

我们的 Mean Entropy、有效长度归一化 TRE 等可作为明确命名的额外对照，但不能重新命名成原论文 baseline。完整 R3 先做单独资源/实现审计，不阻塞 R1。

---

## 10. 资源、监控和预算（实测更新）

| 项目 | 安排 |
|---|---|
| GPU | 实测 `RTX 4080 SUPER`，可用 31.5 GiB，驱动 595.71.05；只做真实加载、单题/20题校验和正式生成；两模型顺序运行 |
| CPU/RAM | 实测 503 GiB RAM（v1 写的 62 GiB 是旧实例规格，已过时） |
| 磁盘 | `/root/autodl-tmp` 150 GB、可用 119 GB；权重缓存占 30 GB；轨迹与结果体积小 |
| 网络 | arXiv/PyPI/GitHub 可达；HF 与 OpenAI 官方域不可达（用镜像或本机端点，见 §4.1、§4.4） |
| 吞吐估计 | 同精度/同预算 smoke 均时 t 估 800×t（实测 64 步约 1.26 s/题，加加载、同步、I/O 和重试）；不引用量化卡速度替代 |
| Judge | 每次主生成至少一次判定，初判错误再一次；R1 约 800–1600 次正常判定，R2 约 9600–19200 次，另计异常重试；按实际 token 与提供方计费口径估算，不给未核验固定费用。moma 端点为本机可达的已用凭据渠道，注意配额与限流 |
| 活性监控 | 检查进程存在、GPU 利用率、日志最后更新时间与 manifest 样本数；不是只看显存占用 |
| 超时策略 | 先测单题时间；超过 max(10 分钟, 10×smoke中位数) 无进度时标记异常并检查，不自动杀进程/无限重试；硬超时须在实际运行前明确 |

每个 run 保留命令、commit/code hash、环境 freeze、设备探测、模型/tokenizer revision、题单 SHA、judge 与过滤设置、开始/结束时间、资源峰值、失败和重试。GPU 资源交还前，在本地/独立备份读取并核对轨迹、代码快照与环境文件；GitHub 仅保存代码/小型清单，不保存权重与大轨迹。

---

## 11. 输出与最终验收

建议独立目录，不覆盖 T4 或跨模型主线数据：

```text
data/tre_repro/
  questions/{smoke20,triviaqa_eval800,hotpotqa_eval800,csqa_eval800}.jsonl
  questions_manifest.json
  labels/{paper_judgments,discarded,judge_raw}.jsonl     # 需 .gitignore
data/trajectories/tre_repro/<model_dataset_precision_budget_run>/
  manifest.json
  generations.jsonl
  traces/*.npz
results/tre_repro/<run>/
  scores.csv
  metrics.json
  paper_comparison.csv
  figures/
reports/tre_repro/
  protocol_diff.md
  pilot_report.md
  reproduction_report.md
```

- [x] 设备实测满足约 32GB 路线；非标商品标签已记录（附录A）。
- [x] LLaDA FP16 真实单题跑通，观察开关一致、峰值显存留档（附录A）。
- [ ] 用 `tre_repro` 的 TriviaQA smoke20 与冻结 prompt 重跑单题、20 题，并做 ≥3 题位置/时点抽查。
- [ ] 原论文版本/题单/split/prompt/生成/judge 协议已固定；缺口（含 judge 换模型）写进 `protocol_diff.md`，不冒充一致。
- [ ] 主分数口径预注册为原始 `tre`；`tre_effective` 并列报告；EOS/EOT 处理显式记录。
- [ ] 初始 800 题与 judge 覆盖可追溯，分歧剔除、needs_review 与失败分别计数。
- [ ] 原始 TRE 按公式计算，与手算/独立复算一致（单题已通过，正式批次需再跑一次全量断言）；正类方向正确。
- [ ] 无训练、无测试集调参、无量化/精度混杂；差异表完整。
- [ ] 给出 AUROC、CI、N 及论文对照；不预设复现一定达到原值。
- [ ] Dream 是否复现、是否仅 BF16 变体、哪些 baseline 未做，逐项明确。
- [ ] 原始记录与代码环境有独立备份，可停止 GPU 后离线复算。

**当前结论：LLaDA FP16 的 TRE 核心复现具备执行条件，工程验收第一步已在本实例通过。** 严格数值对齐仍受原文协议缺口约束（尤其 split、prompt、EOS 口径）；judge 因本机网络限制改用可达模型，属已披露差异。**Dream FP16 当前明确待解决**，不能靠关闭保护或沿用 T4 NF4 数据绕过。

---

## 附录A 2026-10-21 现场核验证据

**A.1 设备与运行时**

- `nvidia-smi`：`NVIDIA GeForce RTX 4080 SUPER`，32760 MiB，驱动 595.71.05，无其他进程。
- torch 探针：`torch 2.8.0+cu128`、runtime CUDA 12.8、capability `(8, 9)`、`free,total=(33,526,841,344, 33,796,456,448)`、`bf16_supported=True`、`FP16 matmul finite=True`。
- 系统：RAM 503 GiB；`/root/autodl-tmp` 150 GB/可用 119 GB；`hf-cache` 30 GB。
- 测试：`.venv` → 82 通过；`.venv-collector-test` → 100 项；`scripts/verify_collectors_cpu.py` 可运行。

**A.2 真实 LLaDA FP16 单题（工程验收）**

命令（输出目录为临时目录，未写入仓库数据目录）：

```bash
env HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1 \
.venv-llada/bin/python scripts/collect_llada.py \
  --questions data/raw_qa/subsets/smoke20.jsonl \
  --output /tmp/opencode/llada_fp16_review \
  --precision float16 --gen-length 64 --steps 64 --block-size 64 --limit 1 --verify-observer
```

结果（来自 manifest 与 trace 元数据）：

| 项 | 值 |
|---|---|
| 模型参数 | 8,015,581,184，全部 `torch.float16`，全部 `cuda:0` |
| 加载耗时 | 6.19 s（含 `from_pretrained`） |
| 生成 | `steps=64`、`requested_steps=64`、`actual_forward_count=64`、`temperature=0`、`block_size=64` |
| 观察开关 | `observer_verified=True`（同 seed 开/关观察最终 token 相同） |
| 耗时 | 2.515 s（含 observer 的两次完整生成） |
| 峰值显存 | allocated 16,113,636,352 B（15.0 GiB）；reserved 16,179,527,680 B（15.1 GiB） |
| 输出 | `John F. Kennedy.`，`termination=eot`，`effective_length=5`（gold 为 Charles Guiteau，属错误回答） |
| 熵 | 全部有限，最大 4.476（vocab 126464，ln≈11.75） |
| 分数 | `tre=7.370904`；`tre_effective=2.199339`；后 EOT 位置占 70.2% |
| 独立复算 | 按公式直接求和得 7.370904 / 2.199339，与 `extract_features` 完全一致 |
| 揭示节奏 | 64 步中每步揭示 1 个 token |
| 提交 | `code_commit=9b8cdf5…`（本轮拉取前） |

**A.3 resume 行为**

- 同 identity 重跑：`All samples already validated; no model loaded.`
- 改 `--limit` 后重跑：`ValueError: run config/input/environment/code fingerprint changed`。

**A.4 judge 端点可达性（本机）**

- `api.openai.com`、`huggingface.co`：连接失败（HTTP 000，DNS 结果异常）；`arxiv.org`、`pypi.org`、`github.com`、`hf-mirror.com`：可达。
- moma 端点 `https://zhenze-huhehaote.cmecloud.cn/v1`：可达；`deepseek-v4.1-flash` 在 `temperature=0` 下返回预期判定；支持 `response_format=json_object`；单次 0.5–2.1 s；4 路并发正常；响应含 `reasoning_content`。密钥值未记录于本文件。

---

## 附录B references/ 快照（范围于 27f8be1 修正）

**主线六篇论文与代码可用性**（`references/README.md`、`research_index.json`、`CODE_AVAILABILITY.md`）：

| 方法 | 论文 | 作者代码状态 | 备注 |
|---|---|---|---|
| TRE | `papers/2607.22661_TRE.pdf` | **未确认可下载的作者仓库**（记录为「未找到」，不是「确定未开源」） | 本项目 `src/trace_schema.py` 是独立公式实现，不是作者源码 |
| TraceDet | `papers/2510.01274_TraceDet.pdf` | 已入库 `repos/TraceDet`（chang-sx/TraceDet，`356337a`） | TRE 表 1 的监督 baseline；MIT |
| DynHD | `papers/2603.16459_DynHD.pdf` | 已入库 `repos/DynHD`（qyy11-com/DynHD，`6c099ad`） | MIT；提供采集配置与 judge 客户端 |
| DeMTS | `papers/2608.14632_DeMTS.pdf` | **未确认可下载的作者仓库** | 与 TRE 作者重叠，其公开协议是本方案的重要旁证（§2.1） |
| TDGNet | `papers/2602.08048_TDGNet.pdf` | 已入库 `repos/TDGNet`（arshiahemmat/tdgnet_code，`a2b5d43`） | 第一作者账号，README 列出同名论文/作者/arXiv；MIT |
| Lost in Diffusion | `papers/2604.10556_LostInDiffusion.pdf` | 已入库 `repos/Lost-in-Diffusion`（ZeroLoss-Lab/Lost-in-Diffusion，`ed158d4`） | **本项目 LLaDA 解码 pin 的来源** |

另有本轮之前上传的参考（非主线，保留原位）：`repos/FActScore`、`repos/long-form-factuality`、`repos/RemeDi` 及对应论文。

**本机核验结论（2026-10-21）**：

- 仓库文件逐文件 SHA256：**2315/2315 一致，0 缺失、0 不符**（7 个仓库）。
- 对每个上游做 blobless fetch 后逐文件比对 Git blob 哈希：**7/7 仓库路径集合与内容完全一致**，7 个固定提交均存在（新增的 TraceDet 56/56、TDGNet 30/30 亦逐字节一致）。
- 论文 PDF：9 个文件全部有哈希记录；`2607.22661_TRE.pdf` 与 `https://arxiv.org/pdf/2607.22661v1` **逐字节一致**（sha256 `a682389e…cdfe6`），即 v1 方案所引用的同一份文件；4 个新 PDF 的内嵌标题与文件名/arXiv 标题一致。
- `.gitattributes` 已含 `references/** -text`，保证快照字节稳定、行尾不被改写。
- `Lost-in-Diffusion/LLaDA/generate.py` 的 sha256 与 `configs/collection_sources.json` 锁定值一致 —— 采集器的 LLaDA 参考实现现在可离线复验。

**许可与合规注意**：

- `Lost-in-Diffusion/HalluLens` 为 **CC BY-NC 4.0（非商业）**，而本仓库 `pyproject.toml` 标 Proprietary：对外分发或商用前需排除该目录或在 `THIRD_PARTY_NOTICES.md` 显式标注。
- `repos/RemeDi` 原提交**没有 LICENSE 文件**：仅作只读参考，不得据以再授权或并入交付物；本轮上传也保持了原样说明。
- 其余主线仓库为 MIT（TraceDet/DynHD/TDGNet），long-form-factuality 为 Apache-2.0（`third_party/` 为 MIT）。

**仍存在的快照缺口**：

- 本项目 Dream 侧锁定的 `generation_utils.py`（sha256 `7f8ad0…`）来自 HF remote code，不在快照内（`Lost-in-Diffusion/Dream/` 引用远程实现；`Fast-dLLM/dream/model/generation_utils.py` 是不同文件）。建议把 `hf-cache/modules/transformers_modules/Dream-org/Dream-v0-Instruct-7B/<rev>/generation_utils.py`（Apache-2.0）纳入 `references/` 并登记哈希，使 Dream 的 shift/NaN 审计同样可离线复验。
- 引用来源的单文件体积：`Fast-dLLM` 的演示 mp4/gif（单个约 30 MB）不影响溯源，将来在意仓库体积时可单独瘦身。
