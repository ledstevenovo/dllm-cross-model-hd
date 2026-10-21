# TRE 复现协议差异表（protocol_diff.md，初稿 v1）

日期：2026-10-21。上位文档：`docs/TRE_4080SUPER_32GB_复现方案.md`（v3.1）。
原则：**原文未公开或与本机做法不同的项全部登记，不写"与原文一致"**；可继续做明示差异的协议近似复现，但不升级为完全一致的数值复现。

## 1. 与原文（arXiv:2607.22661v1）的差异清单

| # | 项目 | 原文状态 | 本机做法 | 影响与登记 |
|---|---|---|---|---|
| 1 | 题单与抽样 | 从官方 evaluation split 随机取 800，ID/seed 未公开 | 自冻结池（`rc.nocontext` **validation** 来源；官方 test 全为 `<unk>` 不可用），seed 20261021，800 题 ID 全公开；与池内 train/validation 簇级不相交 | 数值不可直接对齐；R1 为明示差异的方法复现 |
| 2 | prompt | 精确 prompt/chat template 未公开 | prompt③：裸问题 + 原生 chat template 仅一次包裹；题单含 prompt 文本与指纹 | 与 DeMTS/DynHD 的写法都不同（§2.1 旁证），登记 |
| 3 | 生成长度/步数 | 表 1 的 128/64 是**总扩散步数**；gen_length/block/揭示策略未公开 | 自定 L128/S64/B128（每步 2 token），R0 预检+smoke20 已通过；揭示规则与冻结参考逐项一致 | 自定协议，不称"已冻结的论文参数" |
| 4 | 采样 | temperature 0、cfg 0、top_p/top_k 不设 | 与原文一致（greedy、CFG0） | — |
| 5 | 精度 | float16 | 一致（`--precision float16`，无量化） | — |
| 6 | EOS/EOT 处理 | 之后位置是否计入分数、空/截断处理未公开 | 首个停止 token 前的文本为可见回答；**主分数为全位置原始 TRE**，`tre_effective`/尾部占比为并列诊断（预注册，不按 AUROC 切换）；R0 实测首个 EOT 后约 90% 位置继续采样为 EOT | 尾部贡献显著（均值 53.3%），登记并双口径报告 |
| 7 | judge | GPT-4o mini，未给提示词/snapshot/异常处理 | J2：moma `deepseek-v4.1-flash`，`judge_prompt_v3.txt`（sha256 `2d125bea…`）冻结；初判 incorrect 再真实二判，不一致剔除；API/schema 异常进 `needs_review`；无不可变 snapshot，逐次记录返回元数据 | 标签集合可能与原文不同；数值不可与表 1 等号对齐 |
| 8 | 官方代码 | 截至 2026-10-21 未确认作者仓库 | 独立实现（`src/trace_schema.py` 等），公式按 §4.1 式(3)/式(4) 与附录 B 式(58)/(59) 核对；手算例与真实轨迹均独立复算一致 | 登记为独立实现 |
| 9 | 硬件 | 单卡 Quadro RTX 6000 24GB | RTX 4080 SUPER 31.5 GiB（非标商品标签已记录）；FP16 单题峰值约 16 GiB | 与算法无关，登记 |
| 10 | 置信度计算精度（R0 新发现） | 未公开 | 采集器在**模型 dtype（FP16）**上做 softmax 取揭示置信度，与冻结上游参考 `references/repos/Lost-in-Diffusion/LLaDA/generate.py`（sha256 `aafeca55…`）逐项一致；trace 统计为 FP32。因此用记录统计重放揭示集合时，1280 步中 201 步在近并列（\|Δp\| ≤ 3.46e-04）处互换 | 采样规则无偏离；重放差异为记录精度现象，登记 |

## 2. R1 配置冻结表（R0 后填实）

| 项目 | 冻结值（本机实测，2026-10-21） |
|---|---|
| 模型与精度 | LLaDA-8B-Instruct，float16，batch1，无量化、无训练 |
| revision | `configs/models/llada.json`：`08b83a6feb34df1a6011b80c3c00c7563e963b07`（tokenizer 同） |
| prompt | ③裸问题 + 原生 chat template 一次包裹（`prompt_template_version=v3-bare-question`，逐题指纹在题单） |
| 生成 | gen_length 128、steps 64、block_size 128、temperature 0、cfg_scale 0；top_p/top_k 不设 |
| seed | 抽样 20261021；生成 seed 20261021（题单 `sample_id` 与命令一致） |
| 揭示策略 | `llada_low_confidence_greedy`：块内掩码位置按 FP16 置信度 `torch.topk`（最高优先），`get_num_transfer_tokens` 均匀分配（每步 2 token）；与冻结参考一致 |
| 特殊 token | MASK 126336；EOS 126081；EOT 126348；停止集合 {126081,126348}；首个停止 token 前的文本为可见回答，仍保存全部 128 个生成 token |
| 终止行为（R0 实测） | 20/20 由 EOT 触发；首个 EOT 后其余位置继续生成 EOT（均值 115.05/128，89.9%） |
| judge | J2 moma `deepseek-v4.1-flash`；`data/tre_repro/judge_prompt_v3.txt`（sha256 `2d125bea4f6a5d5a5f97cbb48666c1c872f093d9356a00b09283dc88e5bd46cd`）；temperature 0、JSON 输出；并发 4、超时 120s、最多 3 次退避重试 |
| 主分数 | 全生成位置原始 TRE；`tre_effective`、`tre_length_normalized`、尾部占比为并列诊断 |

## 3. 证据索引

- R0 验收：`reports/tre_repro/pilot_report.md`；原始检查 JSON `/root/autodl-tmp/tre_logs/r0_smoke20_checks.json`
- R0 运行：`data/trajectories/tre_repro/llada_v3_smoke20_L128_S64_B128`（+ repeat3 目录）
- 冻结题单：`data/tre_repro/questions/{smoke20,triviaqa_eval800}.jsonl`、`questions_manifest.json`
- judge 提示词：`data/tre_repro/judge_prompt_v3.txt`
- 评分入口：`scripts/score_tre_repro.py`

（本文件为初稿，R0 人工抽查签核与 J2 连通性测试后按需更新；更新须重记 SHA256。）
