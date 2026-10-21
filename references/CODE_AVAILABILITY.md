# 六篇主线论文的代码获取核查

日期：2026-10-21。代码“找到”仅指可下载且有作者/论文关联证据，不表示复现完整性已审计。

- TraceDet：https://github.com/chang-sx/TraceDet 。作者仓库README给出论文2510.01274，已保存固定revision全部跟踪文件。
- DynHD：https://github.com/qyy11-com/DynHD 。论文PDF直接给出该地址，之前快照继续有效。
- TDGNet：https://github.com/arshiahemmat/tdgnet_code 。第一作者账号；README列出同名论文、同一作者列表、arXiv2602.08048及项目页，已下载。作者网站https://arshiahemmat.com/tdgnet/ 的Code链接虽为失效REPO_URL占位，但不能据此认定没有代码；直接仓库搜索确认了实际源码仓库。arshiahemmat/tdgnet仅为网页，不拿它冒充实现。
- Lost in Diffusion：https://github.com/ZeroLoss-Lab/Lost-in-Diffusion 。论文PDF和代码README可互相对应，之前快照继续有效。
- TRE：https://arxiv.org/abs/2607.22661 。本地PDF未列作者GitHub实现链接；本轮网页检索、GitHub题名/ID搜索、已知共同作者qyy11-com与yixinliu233仓库列表未确认对应源码。状态为“未找到可确认作者仓库”，不写成“确定未开源”。本项目src/trace_schema.py是独立公式实现，不是作者源码。
- DeMTS：https://arxiv.org/abs/2608.14632 。本地PDF未列源码URL；本轮GitHub方法名/ID、网页检索及已知共同作者仓库列表未确认对应实现。同样只记录当前获取缺口，不伪造仓库占位或移植其他方法冒名。

若后续取得TRE/DeMTS作者URL，需核对论文、作者、许可、实际文件和commit，再增补完整快照；不能依据同名搜索命中直接上传。
