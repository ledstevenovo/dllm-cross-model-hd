# 数据卡（当前聚簇版本）

## 来源与实验口径

- TriviaQA `mandarjoshi/trivia_qa` 的 `rc.nocontext/validation`。
- HotpotQA `hotpotqa/hotpot_qa` 的 `distractor/validation`，不提供原始段落给模型。
- TriviaQA test 下载后确认答案不可用，不参与题池。

来源 revision、文件大小与 SHA256 固定在 `configs/datasets/sources.lock.json`。下载器拒绝与锁不一致的文件，构建器同时核对 raw_index 与来源锁。原始数据许可与归属请查 [TriviaQA](https://huggingface.co/datasets/mandarjoshi/trivia_qa) 和 [HotpotQA](https://huggingface.co/datasets/hotpotqa/hotpot_qa) 原页面。

这是从上游 validation 自建的研究 train/validation/test，不是官方测试协议。使用上游 held-out 数据不能证明基座预训练未见过这些问题；不作预训练去污染声明。

## 当前规模与划分

16,606条 / 16,594簇：train 9,919条（9,913簇）；validation 2,481条；test 4,186条（4,180簇）；smoke 20条。

以 `(dataset, raw_id)`、归一化完全相同问题及 token-set Jaccard≥0.85 的问题做联合聚簇，按簇确定性哈希划分。12对高重合问题经独立实现复核，均在同一簇、同一 split。此规则检测词面近重复，不保证识别任意语义改写。保守合簇可包含共享大量词的不同问题，目的是避免跨 split 泄漏；不将同簇问题宣称为语义等价。

DeepSeek 旧版 train 9,922 / test 4,183 的划分已被当前版本替代。修订发生在模型采集前；下游必须使用最新 manifest。上游原始行及历史 manifest 保留，可审计变更。

- smoke20：工程调试，独立于研究划分，不报告研究指标。
- small200：保留的纯 test 子集，不能训练/调参。
- pilot200：120 train / 30 validation / 50 test，每簇取一个代表题，分层按哈希选择；两模型使用相同列表。

哈希 split 在同簇ID不变时稳定；新增问题/合并簇可能改变簇ID。固定池的 top-k 子集可复现，但扩池后成员不保证不变。

## 字段与清洗

每条包含 schema_version、sample_id、question_id、cluster_id、dataset、split、question、question_normalized、gold_answer、gold_aliases、gold_normalized_aliases、answer_type、answer_source_field、prompt、模板版本与指纹、source。source 保留固定 revision、原始文件哈希、原始行号和折叠行号。多 seed 生成应使用不同 sample_id，保留相同 question_id。

规范化采用 NFKC、小写、ASCII标点转空格、删除英文冠词、折叠空白；与官方 SQuAD 删除标点的行为不同。标注不能冒充官方 EM。去掉空问题/不可用答案及题面可直接复制 canonical gold 的问题；只检查归一化后≥3字符的 token 序列，不因别名短语出现就删题。保留原文本与别名，记录筛选偏差；这不是完整的所有答案泄漏检测。

raw_audit.json 记录一处同ID上游答案差异：`triviaqa__qz_4576`，Tony / Tony (Manero).。保留最早行，自动提案仍需人工审核；不把两种表达自动认作事实矛盾。

## 验证

独立脚本均不导入构建用 src 模块：audit_dataset.py 核对字节、字段与子集；audit_raw.py 逐题核对原始 parquet；audit_near_duplicates.py 用不同词序的前缀枚举复查近重复。verify_rebuild.py 在新目录重新构建并比较10个产物哈希。这是独立实现审计，不声称已由另一位人类研究者签字。
