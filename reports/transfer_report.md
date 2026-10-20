# 迁移评测准备状态

真实迁移矩阵尚未产生，原因是没有真实模型轨迹及已审核回答标签。当前可运行的离线流程和命令见README。

results/synthetic_demo/evaluation包含10组特征×2检测器×4方向及数据集分层、目标域监督参照、AUROC/AP/F1/ECE/Brier与question-ID bootstrap。training_audit记录源训练/验证ID、超参与阈值；predictions和detectors.joblib用于复算。该目录全部是工程夹具，不是研究结果。

跨数据集轴与无scaler、另一随机种子的调用也包含在acceptance流程中。正式实验需分别收集固定解码配置、运行多个seed并审核错误/边界案例，然后判断迁移缺口和扩到800–2000题的必要性。
