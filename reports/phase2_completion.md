# 第2阶段本地交付验收（2026-10-21）

已实现真实模型适配器scripts/collect_llada.py和collect_dream.py。当前完成本地工程范围；真实7B/8B、GPU/BF16、云端环境和20题真实轨迹仍需有卡验收。

| 要求 | 证据 |
|---|---|
| 两套采集器 | LLaDA与独立参考生成循环对照；Dream调用固定revision原生diffusion_generate；无观测/有观测token一致 |
| Shift与熵 | 原生Dream hook已shift，位置标记回归；FP32分块统计与NumPy参照一致；原logits不被修改 |
| Manifest与来源 | 题单/代码/环境/精度/协议指纹；模型/tokenizer完整SHA；实际torch forward计数、prompt IDs、EOS/EOT |
| 原子保存/恢复 | NPZ文件fsync→replace→POSIX目录sync→manifest文件fsync/replace/目录sync；配置变更/损坏拒绝；同签名完整孤儿接纳；单写者锁 |
| CPU测试 | 独立环境全套100 passed；原无torch环境82 passed、2个可选torch测试模块skip；不能以skip冒充采集器验证 |
| 实际采集路径演练 | 40条CPU替身轨迹，64步×64位置，观测对照、恢复、NPZ重读与特征计算通过 |
| 离线集成 | 两套输出接原label/extract CLI，得到40行synthetic parquet；未训练smoke检测器 |
| 干净迁移 | 从已暂存Git树导出全新目录，100项全部通过；修复首次克隆缺少.tmp父目录的测试启动缺陷 |
| 独立审查 | 单次新上下文审查提出3项Important，无Critical；作者以6项RED→GREEN回归及全套测试修复，未冒称二次独立批准 |

重要限制：Dream原生entropy FP16可能NaN，当前明确拒绝float16/NF4-FP16，避免静默偏离原采样语义；BF16主线和FP32诊断保留。Windows无可移植目录fsync，POSIX分支有调用顺序测试，尚未做真实断电测试。强杀遗留锁需确认旧进程死亡后人工处理。

日志/清单：phase2_tests.json、phase2_cpu_verification.json、phase2_offline_integration.json、phase2_export_verification.json。模型环境与命令见../docs/PHASE2_COLLECTORS.md。代码哈希在写交付记录前已与当前文件逐一核对。Git导出证据对应新增报告前的暂存树，后续仅增加交付文档/证据，不改变被测试的源代码。

未改动/提交用户正在编辑的docs/T4_传输清单.md；不上传虚拟环境、模型权重、缓存、原始大轨迹与模拟结果目录。
