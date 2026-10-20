# CPU阶段完成与验收记录

范围：实验计划中无需4090D的准备和离线工程。日期2026-10-20。环境uv+.venv，不使用Conda叠加，不安装torch/CUDA，不运行模型推理。所有本轮改动未提交；未修改其他上游checkout。

## 逐项验收

| 工作 | 完成证据 |
|---|---|
| 数据来源/配置/模型元数据固定 | configs/datasets/sources.lock.json；configs/models/{llada,dream}.json；原始parquet哈希已核验，未下载模型权重 |
| 数据清洗、统一ID/schema、重复聚簇 | scripts/build_dataset.py；16,606条；12对Jaccard≥.85同簇同split；reports/raw_audit.json、near_duplicate_audit.json |
| 全局划分、工程/研究子集 | train 9,919；validation 2,481；test 4,186；smoke20；small200纯test；新增pilot200=120/30/50；data/manifests/pilot200.json |
| Prompt与标签协议 | v1 no-context prompt指纹保持；docs/LABEL_PROTOCOL.md；数字先Decimal比较、非匹配待复核；真实主指标只纳入human来源审核标签 |
| 来源与防泄漏独立验证 | audit_dataset/audit_raw/audit_near_duplicates均不导入src；全量行/哈希/问题/答案/簇/子集通过；语义改写检测不作完备性保证 |
| 可复现构建 | reports/reproducibility.json：新目录从原始parquet重建，10个处理产物逐字节一致 |
| 统一轨迹接口 | src/trace_schema.py；pre-reveal统计、mask/reveal合法性、token范围、reveal_step、有效长度和元数据校验；不保存全词表logits |
| TRE与基础特征 | 原文§4式(3)/(4)已核对，reports/tre_definition_check.json含PDF哈希；手算回归；全位置/有效长度/长度归一化版本明确区分 |
| 特征与检测器 | offline.py extract/evaluate；10组特征、LR/16隐藏单元MLP；源train scaler与训练，源validation超参/阈值，冻结模型评分 |
| 迁移/统计/消融 | 四方向、目标域监督参照、同目标迁移代价、AUROC/AP/F1/ECE/Brier、question-ID bootstrap、长度/数据集分层、独立跨数据集轴、无scaler及另一seed |
| 可追溯产物 | parquet及输入清单、模型、逐样本预测、coverage、training_audit、结果表、代码/输入哈希、环境、精度、seed、耗时 |
| 测试与端到端 | reports/acceptance.json：12条命令通过，75项单测通过；400条模拟轨迹→40个模型→4,000预测→240行指标；独立rank AUROC/源scaler/冻结预测审计通过 |
| 图像检查 | transfer.png与feature_distributions.png已打开视觉检查，标题明确SYNTHETIC；不将人为植入的完美分离解读为研究效果 |

## 验证入口

在项目根执行：

```powershell
uv sync --locked
uv run python scripts/acceptance.py
```

本机Windows Store Python受沙箱启动限制，本次以既有`.venv/Scripts/python.exe`在已批准外部执行运行。uv sync --locked --offline确认环境一致。所有CPU验收命令、退出码、耗时和输出保存在acceptance.json。最终又核验了三个模拟结果目录manifest的代码/输出哈希、数据构建代码哈希与pilot来源manifest哈希；未发现漂移。40/8/4个已训练模型对应的候选拟合均没有ConvergenceWarning。

## 证据边界与下一步

本阶段完成的是工程与数据准备，真实实验成功标准仍未满足：没有真实BF16轨迹、人工审核标签、真实AUROC或迁移缺口结论。T4可先做独立量化smoke；4090D先两模型各20题BF16 pilot、抽查至少5条步骤，再采pilot200。按原计划单独记录显存、速度、失败/重试、EOS和实际forward次数；两模型依次加载。正式研究结果必须使用同精度、固定协议、可靠标签，之后再决定是否扩800–2000题。

独立审计指独立代码实现，未冒称另一位人类研究者/队友已签字。远语义近重复、预训练污染、上游Tony/Tony (Manero).表达差异与自动匹配限制均在数据卡/失败分析保留。TraceDet/DynHD等增强基线和长文本扩展仍按计划等待P0真实结果，不提前启动。
