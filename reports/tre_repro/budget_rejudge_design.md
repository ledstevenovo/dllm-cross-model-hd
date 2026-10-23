# 预算效应重算：判据（在 LongCat 重判结果出现之前）

日期：2026-10-23 22:10。

## 问题

我昨天报的预算效应混入了 judge 效应：

| 格 | L128 的 judge | L64 的 judge |
|---|---|---|
| Dream / TriviaQA | vankit | **LongCat** |
| LLaDA / TriviaQA | deepseek | deepseek（不同标签目录） |

已知换 judge 在 HotpotQA 上造成 **0.063** 的差异，而预算效应本身只有 0.03–0.10——
**两者同量级，不可分**。

## 处置

用 **LongCat 重判 3 个 TriviaQA run**（LLaDA L128、LLaDA L64、Dream L128；
Dream L64 本来就是 LongCat），全部重算。已发布的标签不动，新版放 `*_longcat` 目录。

这样四个格子就在同一个 judge 下：

| 格 | L128 | L64 |
|---|---|---|
| Dream / TriviaQA | `dream_triviaqa_l128_longcat` | `dream_triviaqa_bf16_L64_S64_B64_v1`（原即 LongCat） |
| LLaDA / TriviaQA | `llada_triviaqa_l128_longcat` | `llada_triviaqa_l64_longcat` |

## 判据（写死）

记同 judge 下的预算效应为 Δ = AUROC(L64) − AUROC(L128)。

| Δ（Dream） | Δ（LLaDA） | 结论 |
|---|---|---|
| 都 > +0.03 | 都 > +0.03 | 缩短 block **普遍有益**，与"位置少=信息少"的直觉相反 |
| 都 < −0.03 | 都 < −0.03 | 缩短 block **普遍有害**，之前 Dream 的 +0.105 是 judge 假象 |
| 符号相反 | | 效应**模型相关**，不能用单一机制解释 |
| 任一落在 ±0.03 内 | | 该格**无可检测差异**，不宣称方向 |

阈值 0.03 取自重判后预计的 CI 半宽（n≈800，正类率 ~57%，AUROC~0.85 → SE≈0.015）。

## 同时要核对的

1. **正类率是否随 judge 变化**（HotpotQA 上 deepseek→LongCat 使正类率 12.1%→17.9%）；
2. 若 LongCat 与 vankit 在 TriviaQA 上也差很多，说明**这个数据集同样 judge 敏感**，
   那么所有跨 judge 的格子（含 5 格汇总表）都需要重新标注不确定性。

## 不做的事

- 不为了"救"某个结论而挑选 judge；
- 不合并新旧标签（仍是一份文件一个 judge）；
- 若重判后预算效应消失，**如实报告它之前是 judge 假象**。
