# 轨迹与离线评测契约

## 数据采集边界

`src/trace_schema.py` 的 trace-v1 是单调揭示、无 remasking 的紧凑接口。输入只含生成位置，prompt位置应在采集端去除。`entropy` / `top1_probability` / `mask_before` / `revealed` 为实际 T×L 数组；`final_tokens` 为 L 整数；可选 top1_token；保存时推导 reveal_step（1-based，未揭示为-1）。拒绝全词表 logits、NaN、越界概率、非法 mask 迁移、重复揭示与有效回答中仍为 MASK 的位置。

元数据必须记录 sample/question ID、模型/权重/tokenizer/代码 revision、环境、原始 user-content prompt、split、dataset、seed、实际 steps、gen_length、block_size、temperature、sampling_method、precision、生成文本、termination、effective_length、vocab_size。空输出允许 effective_length=0，输出类别仍由标签协议处理。真实采集还应附 requested_steps、实际 forward 次数、device、峰值显存、耗时、模型 chat wrapper 后的 prompt/token IDs 与 logit 对齐说明，写入运行 manifest。

采集顺序：模型 forward → **校准位置对应关系** → 对未加采样噪声的预测分布计算FP32统计 → 记录当前 mask → 记录实际选中揭示集合 → 更新 token。保留采样温度/置信度策略说明；统计是在采样变换前还是后必须显式记录，正式实验固定为预测分布（采样变换前）。summarize_logits 是 NumPy 数值参照；真实GPU采集应在GPU计算统计再搬回小数组，不搬运/保存全词表轨迹。

Dream 的参考实现存在 shift：本地 `repos/Lost-in-Diffusion/Dream/eval/eval.py:354` 使用 `[logits[:,:1], logits[:,:-1]]`。不能假设任意 hook 收到的 logits 都尚未shift；正式采集须结合固定 revision 源码及真实5条步骤抽查，防止漏shift/重复shift。LLaDA 与 Dream 的模型配置在 configs/models/ 下；仅核验了公开元数据，未证明推理环境兼容或显存足够。

## TRE 与特征定义

已核对本地 `2607.22661_TRE.pdf`：§4.1式(3)、§4.2式(4)，以及附录B式(58)/(59)。TRE = Σ(t/T)Σ(i∈本步新揭示集合)H[t,i]，t从1到T，熵用自然对数，不把每步新揭示 token 熵先求平均。公式实现已有手算测试；真实模型下的复现与原论文指标尚未验证。

- tre：全部生成位置的原始公式。
- tre_effective：只保留有效回答位置的变体。
- tre_length_normalized：tre_effective / 有效长度的扩展变体。
- mean_entropy、revealing_entropy、late_entropy：分别为有效位置全轨迹均值、新揭示位置均值、最后约1/3步均值。不是论文原始TRE的替代命名。
- 附加：早/中/晚统计、末初熵差、1-top1 confidence、平均绝对揭示步/相对进度、揭示比例、按已揭示比例加权的揭示熵、可选预测切换率。
- *_vocab_normalized：熵类数值 / log(vocab_size)，不宣称自动实现分布对齐。

FEATURE_SETS 包含 entropy_raw/normalized、early/middle/late_only、entropy_confidence、absolute_time、relative_time、relative_normalized、with_stability。未采 top1_token 时不能运行 with_stability。需要长度、步数、block 的实验用单独表运行，禁止把不同精度混在一张主表。

## 检测器与统计

源 train 拟合 StandardScaler 与 LR（C=.1/1/10）或16隐藏单元MLP（alpha=.001/.01，LBFGS）。源 validation AUROC 选超参、F1选阈值，然后冻结用于两个目标 test。--no-scale 可作源归一化对照。训练记录含每轮候选、收敛警告、选中参数、训练/验证ID与阈值；保存冻结检测器和逐样本预测。MLP未做额外概率校准，ECE/Brier用于诊断原始预测概率。

输出两域内、两跨模型方向；target-trained reference 对应矩阵对角线。迁移代价是在同一目标测试集上 target-trained AUROC 减 source-trained AUROC。多数据集时附分层结果；另用 --axis dataset 在每个backbone内做跨数据集轴，不混称跨模型。

以 incorrect 为正类，只纳入 human_reviewed=true 的 correct/incorrect。报告总量、类别数、审核后覆盖率和分模型/数据集/长度的基线。AUROC/AP在单类别子集留空。question_id分组bootstrap每次抽问题并带入全部重复seed行，报告95%分位区间与有效draw数；小样本区间仅作诊断。

## 模拟验收的含义

synthetic_demo 用真实问题ID搭配人工生成的数值轨迹/人工植入标签，严格标记 synthetic。它验证NPZ→parquet→检测器→迁移矩阵→绘图，不验证真实采集、事实标签质量、模型性能或H1–H4。模拟标签中的 human_reviewed=true 是测试夹具，label_source明确不是人类审核；不得复制到正式标签目录。
