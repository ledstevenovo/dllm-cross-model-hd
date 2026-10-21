# 当前研究直接相关的六篇论文

本目录以这六项为主线。PDF均已包含；能确认的作者仓库保存固定提交的全部跟踪文件，缺代码不拿其他论文的仓库代替。

| 方法 | 论文 | 作者代码快照/状态 |
|---|---|---|
| TRE | [PDF](papers/2607.22661_TRE.pdf) | 未确认可下载的作者仓库；[项目内独立公式实现](../src/trace_schema.py)，不是作者源码 |
| TraceDet | [PDF](papers/2510.01274_TraceDet.pdf) | [代码](repos/TraceDet)，来源chang-sx/TraceDet |
| DynHD | [PDF](papers/2603.16459_DynHD.pdf) | [代码](repos/DynHD)，来源qyy11-com/DynHD |
| DeMTS | [PDF](papers/2608.14632_DeMTS.pdf) | 未确认可下载的作者仓库 |
| TDGNet | [PDF](papers/2602.08048_TDGNet.pdf) | [代码](repos/TDGNet)，来源第一作者arshiahemmat/tdgnet_code |
| Lost in Diffusion | [PDF](papers/2604.10556_LostInDiffusion.pdf) | [代码](repos/Lost-in-Diffusion)，来源ZeroLoss-Lab/Lost-in-Diffusion |

[research_index.json](research_index.json)逐篇对应；[manifest.json](manifest.json)记录各已上传仓库的完整revision、逐文件哈希和论文SHA256。[CODE_AVAILABILITY.md](CODE_AVAILABILITY.md)记录代码获取证据与缺口。

快照含全部Git跟踪源文件，保留原许可证与可执行权限；不含Git历史、未跟踪缓存、虚拟环境及另行下载权重。不声称源码下载即代表论文结果已复现，尤其TDGNet仍需准备原方法所需轨迹。

## 此前额外上传的参考（不是本轮六项主线）

FActScore、long-form-factuality、RemeDi及其对应论文仍保留原位置，避免未经请求删除资料；它们不替代上表任何缺失的仓库。RemeDi原提交没有单独LICENSE，不增授或改称MIT/Apache授权。所有上游许可/署名保持原样。
