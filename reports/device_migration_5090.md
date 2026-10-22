# 设备迁移验收：RTX 4080 SUPER (sm_89) → RTX 5090 (sm_120)

日期：2026-10-22。定位：**有卡资格验收 + 设备一致性诊断**。不是新实验结论，不修改任何已冻结的主表。

## 1. 环境资格（通过）

脚本 `scripts/gpu_env_probe.py`，证据 `reports/gpu_env_probe_{llada,dream}.json`。

| 项 | LLaDA venv | Dream venv |
|---|---|---|
| GPU / capability | RTX 5090 / `sm_120` | RTX 5090 / `sm_120` |
| torch / CUDA runtime | 2.8.0+cu128 / 12.8 | 2.8.0+cu128 / 12.8 |
| 驱动 | 595.80 | 595.80 |
| wheel 架构表含 sm_120 | 是（sm_70…sm_100, sm_120） | 是 |
| BF16 原生支持 | 是 | 是 |
| BF16 matmul vs FP32 参考均值 | −0.03113 / −0.03111 | 同 |
| SDPA flash / mem-efficient | 可用 / 可用 | 可用 / 可用 |
| 总显存 | 31.36 GiB | 31.36 GiB |
| transformers | 4.46.3 | 4.46.2 |

单题与 smoke20（`--verify-observer`，即观测开关前后 token 必须一致）：

| 模型 | 加载 | 单题均值（4080S） | 显存峰值 allocated / reserved | smoke20 | 观测无干扰 | 失败 |
|---|---|---|---|---|---|---|
| LLaDA | 5.0 s | 1.338 s（2.227 s） | 15.01 / 15.13 GiB | 20/20 | 通过 | 0 |
| Dream | 4.8 s | 1.362 s（2.088 s） | 14.34 / 14.56 GiB | 20/20 | 通过 | 0 |

5090 比 4080S 快约 1.6–1.7×，显存占用相同（未触发不同 kernel 的显存差异）。

## 2. 跨设备一致性（BF16 不逐位可复现）

`scripts/device_consistency.py` → `reports/device_consistency_pilot200.json`。pilot200 全 200 题在两台机上以**完全相同的配置**（bf16 / 64-64-64 / temp 0 / seed 20261020 / `--verify-observer`）各采一次。

| 指标 | LLaDA | Dream |
|---|---|---|
| final token 完全相同 | 175/200（87.5%） | 187/200（93.5%） |
| 有效长度改变 | 13/200（最大 Δ14） | 8/200（最大 Δ2） |
| 抽取答案文本改变 | 21/200（10.5%） | 13/200（6.5%） |
| **按签核规则的标签翻转** | **3/200（1.5%）** | **7/200（3.5%）** |
| 特征相对变化 中位 / p90 | 0.42% / 8.5% | 0.41% / 5.6% |

对照组（同机 5090 重跑 10 题）：token 10/10 相同，熵最大绝对差 0.0 → **5090 本身完全确定**，上表差异全部来自 sm_89 与 sm_120 的 kernel 差异，不是随机性或 bug。

标签翻转方向是双向的（LLaDA：incorrect→correct 1、correct→incorrect 2；Dream：incorrect→correct 4、correct→incorrect 1、incorrect→format_failure 2），没有系统性偏向 → 属于噪声，不构成精度偏移。

## 3. 结论：冻结结论对设备不敏感

把 5090 重采的 pilot200 用**同一签核规则**重新打标（该规则已对 400 条 reviewed 标签逐条复现，见 `tests/test_signoff_rule.py`），重跑整张迁移矩阵（`/root/autodl-tmp/probe5090/stage7/transfer_matrix.csv`）：

| 项 | 结果 |
|---|---|
| 16 格逐格 \|ΔAUROC\| | 均值 0.030，最大 0.100（`Dream 域内 rel+MLP`） |
| 与 4080S 矩阵的相关 | Pearson 0.931 |
| 相对 0.5 的方向一致性 | **16/16** |
| 异常格 `rel+LR Dream→LLaDA` | 0.494 → **0.495** |

即：**"Dream 源域方向性缺口"这一核心结论在换设备后原样重现**；域内与 LLaDA→Dream 仍稳定迁移，`rel+LR Dream→LLaDA` 仍停在随机水平。单格波动 ≤0.10，与 CI 宽度（±0.15–0.20）相当，属于该规模下的正常噪声。

## 4. 由此确定的采集规则

1. **扩池的新增轨迹，两个模型必须在同一设备上采集**。禁止把 5090 的新 LLaDA 与 4080S 的旧 Dream 拼进同一张迁移矩阵：跨设备差异（10% 答案文本变化）与"跨模型缺口"同量级，会污染结论。
2. **pilot200 既有轨迹原样保留、不重采**：其内部同设备自洽，且第 3 节已证明其结论在另一设备上可重现。
3. 跨设备重采只作为**诊断证据**留档，不进入主表、不替换 reviewed 标签。5090 重采的标签文件带 `5090 device rerun (diagnostic only)` 备注并放在仓库外的 `/root/autodl-tmp/probe5090/`。
4. 后续任何新设备（含换回 4080S）都先跑 `scripts/gpu_env_probe.py` + 本诊断（可只跑 20 题快速版），再决定是否混用轨迹。

## 5. 产物

| 产物 | 路径 |
|---|---|
| 环境探针 | `reports/gpu_env_probe_{llada,dream}.json` |
| 一致性诊断 | `reports/device_consistency_pilot200.json`（含逐题明细） |
| 5090 重采轨迹 | `/root/autodl-tmp/probe5090/pilot200_5090/`（不入库） |
| 5090 迁移矩阵 | `/root/autodl-tmp/probe5090/stage7/`（不入库） |
| 探针脚本 | `scripts/gpu_env_probe.py` |
| 诊断脚本 | `scripts/device_consistency.py` |
| 签核规则（入库版） | `src/signoff_rule.py` + `tests/test_signoff_rule.py` |
| 签核复核脚本 | `scripts/draft_signoff_review.py` |
