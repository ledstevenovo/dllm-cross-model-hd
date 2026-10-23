# 同 judge 对照：用 LongCat 重判 R2，消除跨模型比较的 judge 混杂

日期：2026-10-23 16:20。

## 问题

| Run | judge | AUROC |
|---|---|---:|
| LLaDA / HotpotQA（R2） | deepseek + 三方仲裁 | 0.706 |
| Dream / HotpotQA | LongCat | 判分中 |

Dream 那份之所以换 judge，是因为 deepseek 端点从 2.6 s 退化到 12.3 s/次
（见 `dh_judge_switch.md`）。但这样一来，两个模型在**同一数据集**上的对比就混入了
judge 差异——正是本项目一直在避免的混杂。

## 处置

用 LongCat **重新判 R2 的全部 800 条**，输出到独立目录
`data/tre_repro/labels/llada_hotpotqa_longcat/`。

- **不改**已发布的 R2 标签文件（那份用 deepseek + 仲裁，是论文 §3.7 的依据）；
- 新的 LongCat 版本只用于**同 judge 对照**，即回答"两个模型在这个数据集上的差距有多少是模型、多少是 judge"；
- 不占 GPU（纯 API）。

## 能回答什么

1. **R2 的 0.706 对 judge 有多稳**：deepseek+仲裁 vs LongCat 全量，两个数字的差就是 judge 效应；
2. **跨模型差距是否真实**：Dream 的 AUROC 减去 LongCat 版 R2 的 AUROC，
   才是"同一 judge 下"的模型差异；
3. 若两者接近（judge 效应 <0.03），则之前用不同 judge 的比较也可以接受，
   只需把 judge 差异列为不确定性来源。

## 规则

- 两份标签**不合并**：各自是一个完整的单-judge 文件；
- 报告时同时给出两个 R2 数字（deepseek 0.706 / LongCat 待定），
  并说明哪一个用于什么目的；
- 若 LongCat 版与 deepseek 版差异很大（>0.05），则说明 HotpotQA 的标签在该数据集上
  **本质上不稳定**，那时应把 R2 的结论降级为"依赖 judge 的探索性结果"。

## 成本

800 条 × 1.6 次调用 × 3.5 s ≈ **75 分钟**，与 Dream 的判分并行，无 GPU 占用。
