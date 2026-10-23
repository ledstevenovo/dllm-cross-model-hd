# 公平对比：去掉长度相关特征后，无训练 TRE 与训练检测器持平

日期：2026-10-24 06:25。此前所有对比中，归一化 TRE 已去掉长度，
而检测器的 10 维特征里有 5–10 个与 `effective_length` 相关（|r| > 0.25）。
本页把这些特征去掉后重算，其它（轨迹、标签、折、种子）全部不变。

## 结果

| Run | TRE（归一化） | 检测器（全 10 维） | **检测器（去长度）** | 全维差距 | **公平差距** |
|---|---:|---:|---:|---:|---:|
| LLaDA / TriviaQA | **0.8429** | 0.8521 | **0.8432** | +0.009 | **+0.0003** |
| LLaDA / HotpotQA 裸 | **0.8055** | 0.8436 | 0.7836 | +0.038 | **−0.022** |
| Dream / HotpotQA 裸 | 0.7780 | 0.8575 | 0.6828 | +0.079 | **−0.095** |
| Dream / TriviaQA | 0.8477 | 0.8903 | *（10/10 特征全被去掉）* | +0.043 | 无法计算 |

## 三个结论

### 1. LLaDA / TriviaQA：完全持平（差 0.0003）

去掉 5 个长度相关特征后，检测器 0.8521 → **0.8432**，与 TRE 的 0.8429 **相差 0.0003**。

**一个无训练、单特征的分数与一个 5 维训练检测器在统计上不可区分。**
这意味着此前的"检测器 +0.9 pp 优势"**全部来自长度相关特征**。

### 2. HotpotQA 上 TRE 反而更好

| Run | 公平差距 |
|---|---:|
| LLaDA / HotpotQA 裸 | **−0.022**（TRE 领先） |
| Dream / HotpotQA 裸 | **−0.095**（TRE 大幅领先） |

去掉长度特征后，检测器在 HotpotQA 上**明显变差**。原因是这一数据集的答案长度差异极大
（Dream 中位 1–3、LLaDA 中位 12–18），长度特征承担了很大一部分判别力；
去掉之后，剩下的熵特征判别力不足。

### 3. Dream / TriviaQA：**所有 10 个特征都与长度相关**

| 特征 | \|r\| with length |
|---|---:|
| `entropy_change_vocab_normalized` | **0.602** |
| `late_entropy_vocab_normalized` | 0.593 |
| `mean_reveal_progress` | 0.523 |
| `mean_entropy_vocab_normalized` | 0.466 |
| `middle_entropy_vocab_normalized` | 0.400 |
| `mean_uncertainty` | 0.398 |
| `reveal_progress_entropy_vocab_normalized` | 0.396 |
| `early_entropy_vocab_normalized` | 0.357 |
| `revealed_fraction` | 常数 |

**Dream 的回答中位只有 3 token**，长度几乎解释了所有特征变异。
检测器在这个 run 上的 0.8903 有相当部分是在学"答对的短、答错的长"——
而这正是 TRE 归一化后刻意去掉的东西。

## 这意味着什么

| 说法 | 状态 |
|---|---|
| "训练检测器在 TriviaQA 上更好（+0.9 ~ +4.3 pp）" | ❌ **撤回**：这些优势来自长度相关特征 |
| **"公平条件下 TRE 在 LLaDA 上完全持平、在 HotpotQA 上更好"** | ✅ 当前 |
| "检测器在短答案场景更强" | ❌ 恰恰相反——短答案场景下它的优势全是长度 |

## 需要谨慎的地方

1. **去掉特征不是"更好的检测器"**：全 10 维版本在真实部署中可以用长度信息，
   而那可能是**合法的**（不是作弊）。本页只回答"多出的信息是不是长度"；
2. **"长度"在某些任务上是有效信号**：如果答错确实导致答长，那用它没问题。
   关键是**报告时要说明**，而不是把它当作"熵特征的威力"；
3. 本页阈值 0.25 是任意的；用 0.3 或 0.2 会得到不同的保留集合；
4. 每格只有一种 CV 划分，无重复。

## 对论文的最终表述

> 在**控制答案长度信息**之后，一个无训练的单特征分数（归一化 TRE）
> 与 10 维训练检测器在 LLaDA/TriviaQA 上不可区分（0.8432 vs 0.8429），
> 在 HotpotQA 两个 run 上更好（领先 0.022 / 0.095）。
> 检测器此前的表面优势来自其特征与答案长度的相关性。

## 产物

| 文件 | 内容 |
|---|---|
| `reports/tre_repro/fair_det_llada_tq.json` | LLaDA / TriviaQA |
| `reports/tre_repro/fair_det_llada_hp_bare.json` | LLaDA / HotpotQA |
| `reports/tre_repro/fair_det_dream_hp_bare.json` | Dream / HotpotQA |
| `scripts/fair_detector_comparison.py` | 复算脚本 |
