# TRE run 目录索引（轨迹 ↔ 标签 ↔ 结果 ↔ judge）

日期：2026-10-24 05:15。目录命名在多次迭代中不统一（早期用配置字符串、后期用语义名），
本表是唯一的对应依据。

## 对照表

| 轨迹目录（`data/trajectories/tre_repro/`） | 题单 | 标签目录（`data/tre_repro/labels/`） | 结果（`results/tre_repro/`） | judge |
|---|---|---|---|---|
| `llada_triviaqa_fp16_L128_S64_B128_v3` | triviaqa_eval800 | `llada_triviaqa_fp16_L128_S64_B128_v3`（deepseek）· `llada_triviaqa_l128_longcat`（LongCat，主用） | `llada_triviaqa_fp16_L128_S64_B128_v3` · `llada_triviaqa_l128_longcat` | 两者都有 |
| `llada_triviaqa_fp16_L64_S64_B64_v1` | triviaqa_eval800 | `llada_triviaqa_fp16_L64_S64_B64_v1`（deepseek）· `llada_triviaqa_l64_longcat` | 同名 + `llada_triviaqa_l64_longcat` | 两者都有 |
| `llada_triviaqa_fp16_L256_S64_B256_v1` | triviaqa_eval800 | `llada_triviaqa_l256_longcat` | `llada_triviaqa_l256_longcat` | LongCat |
| `dream_triviaqa_bf16_L128_S64_B128_v1` | triviaqa_eval800 | `dream_triviaqa_bf16_L128_S64_B128_v1`（vankit）· `dream_triviaqa_l128_longcat` | 同名 + `dream_triviaqa_l128_longcat` | 两者都有 |
| `dream_triviaqa_bf16_L64_S64_B64_v1` | triviaqa_eval800 | `dream_triviaqa_bf16_L64_S64_B64_v1` | `dream_triviaqa_bf16_L64_S64_B64_v1` | LongCat |
| `llada_hotpotqa_bare_fp16_L128_S64_B128_v1` | hotpotqa_bare800 | `llada_hotpotqa_bare_v1` | `llada_hotpotqa_bare_v1` | LongCat |
| `llada_hotpotqa_bare_fp16_L64_S64_B64_v1` | hotpotqa_bare800 | `llada_hotpotqa_bare_v1_L64` | `llada_hotpotqa_bare_v1_L64` | LongCat |
| `llada_hotpotqa_bare_bf16_L128_S64_B128_v1` | hotpotqa_bare800 | `llada_hotpotqa_bare_bf16_longcat` | `llada_hotpotqa_bare_bf16_longcat` | LongCat |
| `dream_hotpotqa_bare_bf16_L128_S64_B128_v1` | hotpotqa_bare800 | `dream_hotpotqa_bare_v1` | `dream_hotpotqa_bare_v1` | LongCat |
| `dream_hotpotqa_bare_bf16_L64_S64_B64_v1` | hotpotqa_bare800 | `dream_hotpotqa_bare_l64` | `dream_hotpotqa_bare_l64` | LongCat |
| `llada_hotpotqa_fp16_L128_S64_B128_v1` | hotpotqa_eval800 | `llada_hotpotqa_longcat`（主用）· 原 deepseek 目录已归档 | `llada_hotpotqa_longcat` · `llada_hotpotqa_fp16_L128_S64_B128_v1` | LongCat / deepseek |
| `llada_hotpotqa_fp16_L64_S64_B64_v1` | hotpotqa_eval800 | `llada_hotpotqa_ctx_l64` | `llada_hotpotqa_ctx_l64` | 采集中 |
| `dream_hotpotqa_bf16_L128_S64_B128_v1` | hotpotqa_eval800 | `dream_hotpotqa_bf16_L128_S64_B128_v1` | 同名 | LongCat |
| `dream_hotpotqa_bf16_L64_S64_B64_v1` | hotpotqa_eval800 | `dream_hotpotqa_ctx_l64` | `dream_hotpotqa_ctx_l64` | LongCat |
| `llada_hotpotqa_smoke20_fp16_v1` | hotpotqa_smoke20 | `llada_hotpotqa_smoke20_fp16_v1` | — （工程验收，不入主表） | LongCat |
| `llada_v3_smoke20_L128_S64_B128` | smoke20 | 同名 | — （工程验收） | — |
| `llada_v3_smoke20_repeat3_L128_S64_B128` | smoke20 | 同名 | — （确定性复验） | — |

## 命名规则（今后统一使用）

```
<model>_<dataset>[_<prompt>]_<precision>_L<genlen>_S<steps>_B<block>_v<n>
```

- `prompt` 省略 = 裸问题；`ctx` = 含上下文
- 标签与结果目录沿用**配置名**，不另起语义名，避免本表中的错位

## 为什么要写这张表

本夜出现过一次真实的目录错位（R2 的 800 题写到了 `data/trajectories/tre_repro` 之外），
以及多次"标签目录用语义名、轨迹目录用配置名"的不一致。这些都能靠一张映射表消除歧义。

复算任何一格时，**先查本表**，不要按名字猜。
