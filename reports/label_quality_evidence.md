# 标签质量证据：第二 judge 一致性（2026-10-22）

## 主项目（迁移矩阵/稳定性所用 reviewed 标签）

- judge：`LongCat-2.5-Preview`，冻结提示词 `judge_prompt_v3` （sha256 2d125bea4f6a…），温度 0
- 抽样：100 条，完成 100 条（seed 20261021）
- **总体一致率 0.960**，**Cohen's κ = 0.908**

| 模型 | n | 一致率 | 规则标签 incorrect 占比 | judge incorrect 占比 |
|---|---|---|---|---|
| dream | 50 | 0.960 | 0.68 | 0.68 |
| llada | 50 | 0.960 | 0.68 | 0.68 |

- 不一致 4 条；明细见 `main_label_consistency.json`（disagreements 字段）与 `main_label_consistency.rows.jsonl`，并已全部进入人工抽查表（`reports/label_spotcheck_sheet.md/.csv`）。

### 分歧示例（最多 5 条，完整清单见 `label_spotcheck_sheet.md`）

| 模型 | 问题（截断） | 规则 | judge | judge 理由（截断） |
|---|---|---|---|---|
| llada | Were Triumph of the Will and The End of America both made in the same year? | correct | incorrect | The proposed answer states Triumph of the Will was released in 1955, but it was actually released in 1935. This is a material factual error. |
| llada | The actor John Wayne was known by what nickname? | incorrect | correct | John Wayne's nickname was 'The Duke'; 'Duke' is a semantically equivalent short form matching the reference answer. |
| dream | Which person, William Blake Herron or John Carpenter, held more diverse roles in the movie | incorrect | correct | The proposed answer 'John Carpenter' correctly identifies the person who held more diverse roles in the movie industry. The reference answer |
| dream | Who succeeded Prince Rainier of Monaco? | correct | incorrect | The proposed answer 'Prince Albert II' refers to Albert II of Monaco who succeeded Rainier III. However, all reference answers refer to Prin |

## DynHD 复现（规则标签）

- judge：`LongCat-2.5-Preview`，冻结提示词 `judge_prompt_v3` （sha256 2d125bea4f6a…），温度 0
- 抽样：100 条，完成 100 条（seed 20261021）
- **总体一致率 0.970**，**Cohen's κ = 0.933**

| 模型 | n | 一致率 | 规则标签 incorrect 占比 | judge incorrect 占比 |
|---|---|---|---|---|
| dream | 50 | 0.980 | 0.64 | 0.66 |
| llada | 50 | 0.960 | 0.66 | 0.70 |

- 不一致 3 条；明细见 `dynhd_label_consistency.json`（disagreements 字段）与 `dynhd_label_consistency.rows.jsonl`，并已全部进入人工抽查表（`reports/label_spotcheck_sheet.md/.csv`）。

### 分歧示例（最多 5 条，完整清单见 `label_spotcheck_sheet.md`）

| 模型 | 问题（截断） | 规则 | judge | judge 理由（截断） |
|---|---|---|---|---|
| llada | Are Roger Waters and Tom Johnston both musicians? | correct | incorrect | While it correctly answers yes to the question, it adds a material factual error: Roger Waters is a bassist/vocalist, not a drummer. |
| llada | Chimaja Appawas the younger brother of a general of the Maratha Empire in India, who serve | correct | incorrect | The answer correctly names 'Peshwa (prime minister)' but misattributes the role to Chimaja Appa. Historically, the Peshwa to Chhatrapati Sha |
| dream | Who succeeded Prince Rainier of Monaco? | correct | incorrect | The proposed answer 'Prince Albert II' does not match any of the supplied reference answers. All reference answers refer to Prince Albert, t |

## 说明

- 本证据是**补充**：正式指标仍使用 reviewed 规则签核标签，第二 judge 不改任何标签；
- 两套判分使用同一冻结提示词与同一 judge 模型/端点，可与 TRE R1 的 judge 口径直接对照；
- 人工抽查表按“全部不一致 + 一致中补齐至 ≥50 条”生成，供人工独立复核后填写判定。

