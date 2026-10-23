# R2 结果对标签口径极敏感：规则标签给出 0.542，judge 给出 0.682

日期：2026-10-23。这是对 R2 报告的重要限定，必须与 `reports/tre_repro/r2_report.md` 一起读。

## 发现

对**同一批 786 条** R2 轨迹、同一个 TRE 分数，只换标签来源：

| 标签来源 | 正例数（incorrect） | AUROC |
|---|---:|---:|
| **judge**（vankit `deepseek-v4.1-flash`，冻结提示词 v3） | 95 | **0.6818** |
| **规则签核**（`src/signoff_rule.py`） | 174 | **0.5424** |

两者逐条一致率仅 **0.831**——远低于主项目的 0.933。

**换标签后 AUROC 从 0.682 掉到 0.542（接近随机）**。所以 R2 的"TRE 有效"这一结论**不稳健**。

## 为什么规则在 HotpotQA 上失效

逐条查了 142 条分歧，原因是**规则的设计前提不成立**：

### 规则判 correct、judge 判 incorrect（106 条）

规则的逻辑是"gold 子串命中即 correct"。但 HotpotQA 的回答常是**长句复述 + 自我矛盾**：

```
gold:  Eliot Cutler
answer: "...is Eliot Cutler. However, according to the context, Eliot Cutler finished
         in third place behind Republican Pau..."      ← 前半对、后半自相矛盾
```

规则看到 "Eliot Cutler" 就判对；judge 读到矛盾判错。**在长回答上，子串命中不等于答对。**

### 规则判 incorrect、judge 判 correct（36 条）

```
gold:  Jean-Loup Jacques Marie Chrétien
answer: "Jean-Loup Chrétien was born first."            ← 正确的简称
```

规则要求完整 token 序列匹配，简称/改写就失配。**在自然语言回答上，精确匹配过严。**

## 结论与处理

1. **R2 的 AUROC 0.682 依赖 judge 标签，不能被规则标签独立确认**；
2. **规则签核不适用于 HotpotQA**：它的两条假设（子串命中≈答对、精确匹配≈唯一）在
   "有上下文 + 长回答"的设置下同时失效。这不是规则写错了，而是它针对 TriviaQA 的
   短答案（"Alexander Pope"、"Germany"）设计的；
3. **R2 报告必须加上这条限定**：主数字用 judge 标签，规则标签给出 0.542，两者差 0.14；
4. 主项目（pool2000）不受影响：它的回答是短答案，规则 vs judge 一致率 0.933，
   且 `reports/label_source_robustness.md` 已证明排序稳健。

## 对"哪个更可信"的判断

**在 R2 上 judge 更可信**，理由是三条分歧样本都显示规则的系统性错误方向明确：

- 106 条"规则对、judge 错"里，规则是被**长回答中的正确片段**误导，而答案整体是错的
  （含自我矛盾的补充说明）；
- 36 条"规则错、judge 对"里，judge 正确接受了简称与改写。

judge 的行为符合"语义等价"的定义，规则的行为符合"字符串包含"的定义。TRE 要预测的是
**答案是否正确**，所以 judge 口径更贴近目标。

但这不意味着 0.682 可以放心引用——它只在一个 judge 上成立。诚实的表述是：

> R2 的 TRE AUROC 在 judge 口径下为 0.68（显著），但在规则口径下为 0.54（接近随机）。
> 两个口径的差异源于 HotpotQA 的长回答形态使规则签核失效。因此 R2 的效应量
> **对标签口径敏感**，不能与 R1（短答案、两口径一致率 0.93）等量齐观。

## 建议的后续（未执行）

- 对 R2 做一个**人工抽查**（50–100 条分歧），确定规则与 judge 谁更接近人工判断；
- 若规则确实系统性偏向"亚串命中"，则应给 HotpotQA 单独写一套规则（或只用 judge）；
- 在论文里把 R2 标为"标签口径待定"的探索性结果，不作主表结论。
