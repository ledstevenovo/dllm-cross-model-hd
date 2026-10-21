# TRE R0 验收报告（LLaDA FP16，L128/S64/B128，prompt③，seed 20261021）

- 运行目录：`data/trajectories/tre_repro/llada_v3_smoke20_L128_S64_B128`
- 环境：Python 3.12.3、torch 2.8.0+cu128、transformers 4.46.3、NVIDIA GeForce RTX 4080 SUPER（capability [8, 9]）
- 解码：{'gen_length': 128, 'steps': 64, 'block_size': 128, 'temperature': 0.0}，precision=float16，seed=20261021
- 加载耗时：7.08s；状态：completed

## 1. 机械校验

| 检查项 | 结果 |
|---|---|
| 样本数 | 20/20 |
| 逐文件 SHA256 | 全部一致 |
| trace 内部检查（熵有限/揭示单调/无 MASK 残留/覆盖完整/forward 数） | problems=0 |
| 观察开关一致性（observer） | 20/20 verified |
| 揭示节奏 | 每步恰好 2 token（128/64 配置，全部 1280 步） |
| 最终 token == 揭示步记录的 argmax | 失败 0/2560 个位置 |
| 用记录统计重放揭示集合（见 1.1） | 完全一致 1079/1280 步 |
| 重复 3 题（同 seed、新目录） | 3/3 最终 token 完全相同 |

### 1.1 揭示集合重放的差异说明（已定位，不构成协议偏离）

用记录的 FP32 `top1_probability` 重放「块内掩码位置取 top-k 置信度」时，1280 步中有 201 步选出的位置集合不同；
逐例核对后，差异全部发生在近并列的位置上（|Δp| ≤ 3.46e-04，即 FP16 分辨率量级），原因：

- 采集器与冻结参考 `references/repos/Lost-in-Diffusion/LLaDA/generate.py`（sha256 `aafeca55…`）一致，
  都在 **模型 dtype** 上做 softmax 取置信度（FP16），而 trace 记录的是 **FP32** 统计；
- 因此重放用的是「四舍五入后的置信度」，在近并列处会与 FP16 采样决策互换；
- 方向与规则本身一致：`torch.topk(confidence)`（最高置信度优先）、仅当前块、`get_num_transfer_tokens` 均匀分配。

结论：采样规则与冻结上游一致；轨迹自洽（TRE 用实际揭示表 + FP32 熵）。该精度细节写入 protocol_diff。

## 2. 解码与分数诊断（不替换主口径）

| 指标 | 值 |
|---|---|
| 有效长度 min/中位/max | 1 / 9.0 / 40 |
| 终止类型 | {'eot': 20} |
| 空答 / 截断 | 0 / 0 |
| 停止 token 数（均值，共 128 位置） | 115.05（平均占比 89.9%） |
| TRE 分解均值：可见回答 / 终止 token / 其后尾部 | 8.8457 / 0.8559 / 9.4383 |
| 尾部占比（tail/total）均值 | 53.3% |

说明：首个 EOT 之后的位置持续采样为 EOT（占比约 90%），因此尾部贡献不可忽略；主口径仍为全位置原始 TRE，
`tre_effective` / 尾部诊断按 §3 预注册口径并列报告。

## 3. 人工抽查表（20 题全表，供 ≥5 条签核）

| # | question | gold | 生成文本 | 有效长度 | 终止 |
|---|---|---|---|---|---|
| 1 | Which Chinese dynasty ruled from the 14th to the 17th centur | Ming | 'The Chinese dynasty that ruled from the 14th to the 17th century was t' | 23 | eot |
| 2 | Which classic sci-fi novel divides the human species into th | THE TIME MACHINE | 'The classic sci-fi novel that divides the human species into the gentl' | 40 | eot |
| 3 | Who is the protagonist and narrator of Robert Louis Stevenso | 'DAVID BALFOUR' | 'Captain Brown' | 2 | eot |
| 4 | Precisely where were the Winter Olympics of 1932 and 1980 bo | Lake Placid | 'The Winter Olympics of 1932 were held in Oslo, Germany, and the Winter' | 34 | eot |
| 5 | "The names of how many states of the USA start and end with  | 3 | '2' | 1 | eot |
| 6 | Which number Beethoven symphony is known as ‘The Pastoral’? | SIXTH | 'The Sixth' | 2 | eot |
| 7 | In humans, Gorham disease affects which part of the body? | Bones | 'Gorham disease affects the kidneys.' | 8 | eot |
| 8 | In 1984, in Bophal, India, there was a leak of 30 tons of me | UNION CARBIDE | 'Union Carb' | 2 | eot |
| 9 | "Damon Runyon's two stories ""The Idyll of Miss Sarah Brown" | Guys and Dolls | 'Damon Runyon\'s two stories "The Idyll of Miss Sarah Brown" and "Blood ' | 32 | eot |
| 10 | A Suffolk Punch is what kind of animal? | Horse | 'A Suffolk Punch is a breed of dog.' | 9 | eot |
| 11 | Which US president did Anthony Hopkins play in a film whose  | Nixon | 'John Jefferson' | 2 | eot |
| 12 | what is the 21st letter of the Greek alphabet? | Phi | 'The 21st letter of the Greek alphabet is Opsilon.' | 14 | eot |
| 13 | "The song ""I Could Be So Good For You"" was from which Brit | Minder | 'The song "I Could Be So Good For You" is from the British TV series "T' | 21 | eot |
| 14 | "Which character did Robert De Niro portray in the film ""Ta | Travis Bickle | 'Robert De Niro portrayed the character of Travis Bickle in the film "T' | 19 | eot |
| 15 | Espiritu Santo is the largest island of which island republi | VANUATU | 'Espiritu Santo is the largest island of the island republic of St. .' | 16 | eot |
| 16 | Which business organisation took over the Somerfield chain o | THE CO-OPERATIVE | 'Tda' | 2 | eot |
| 17 | Who is currently fifth in line to the Throne? | PRINCESS BEATRICE | 'Prince William of Kent' | 4 | eot |
| 18 | A garboard is a range of planks on what? | Ship | 'A garboard is a range of planks on a ship.' | 12 | eot |
| 19 | In baseball, where do the Orioles come from? | Baltimore | 'The Baltimore Orioles come from Baltimore, Maryland.' | 9 | eot |
| 20 | From which continent does the world's smallest bear the Sun  | (SOUTH EAST) ASIA | 'The Sun Bear originates from Asia.' | 7 | eot |

## 4. R1 配置冻结表（按 R0 实际行为填实）

| 项目 | 冻结值（本机实测） |
|---|---|
| 模型与精度 | LLaDA-8B-Instruct，float16，batch1，无量化/无训练 |
| revision | 见 `configs/models/llada.json`（`08b83a6f…`），tokenizer 同 revision |
| prompt | ③裸问题 + 原生 chat template 一次包裹（题单含 prompt 与指纹） |
| 生成 | gen_length 128、steps 64、block_size 128、temperature 0、cfg 0；top_p/top_k 不设 |
| 揭示策略 | `llada_low_confidence_greedy`（块内 top-k 最高置信度；每步 2 token），与冻结参考逐项一致 |
| 特殊 token | mask 126336；EOS 126081；EOT 126348；停止集合 {126081,126348}；首个停止 token 前的文本为可见回答 |
| 终止行为（R0 实测） | 20/20 由 EOT 触发；首个 EOT 后其余位置继续生成 EOT（均值 115.05/128） |
| seed | 抽样 20261021；生成 20261021（命令显式传入） |
| judge | J2 moma deepseek-v4.1-flash；`judge_prompt_v3.txt`（sha256 `2d125bea…`） |
| 主分数 | 全生成位置原始 TRE；有效区域与尾部为并列诊断 |

证据文件：`/root/autodl-tmp/tre_logs/r0_smoke20_checks.json`、`/root/autodl-tmp/tre_logs/collect.log`（20 题）、重复运行目录 `data/trajectories/tre_repro/llada_v3_smoke20_repeat3_L128_S64_B128`。
