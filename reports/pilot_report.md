# Pilot readiness（CPU工程阶段）

数据：pilot200 = 120 train / 30 validation / 50 test，每个backbone共用。smoke20独立工程调试；small200纯测试。来源、当前划分、近重复和字节重建证据见各审计JSON。

轨迹读取、特征提取、TRE/简单基线、LR/MLP与四格矩阵已用400条模拟轨迹做工程演练。模拟配置4步×8生成位置，数值/标签人为构造，不是原计划64步×64 token的真实pilot。

待GPU阶段：两模型各20道BF16运行；至少5条逐步检查；显存峰值、平均耗时、轨迹体积、失败/重试率、EOS与实际forward次数、同seed重现性。当前这些字段均为“未测量”，不得从模拟耗时外推4090D/T4吞吐。
