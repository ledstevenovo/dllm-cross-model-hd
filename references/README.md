# 论文与上游复现代码快照

本目录打包5个参考仓库在固定提交的全部Git跟踪文件，以及一一对应的5篇论文。不是我们已经复现成功的声明。仓库Git历史、未跟踪本地文件、环境和下载缓存不包含在快照内。

| 代码目录 | 上游 | 固定版本 | 对应论文 |
|---|---|---|---|
| repos/DynHD | https://github.com/qyy11-com/DynHD | 6c099ad | papers/2603.16459_DynHD.pdf |
| repos/FActScore | https://github.com/shmsw25/FActScore | f28272d | papers/2305.14251_FActScore.pdf |
| repos/long-form-factuality | https://github.com/google-deepmind/long-form-factuality | 9d27158 | papers/2403.18802_LongFact_SAFE.pdf |
| repos/Lost-in-Diffusion | https://github.com/ZeroLoss-Lab/Lost-in-Diffusion | ed158d4 | papers/2604.10556_LostInDiffusion.pdf |
| repos/RemeDi | https://github.com/maple-research-lab/RemeDi | 2e1b19d | papers/2509.23653_RemeDi.pdf |

manifest.json记录完整提交号、每文件SHA256与字节数、论文来源与SHA256。上游代码保持原内容与许可证，不自动赋予本项目的新许可。RemeDi该提交没有单独LICENSE文件，保留原README与来源，不将其改称MIT或Apache授权。论文的作者、引用和原始条款保持原样。

Lost-in-Diffusion包含其上游跟踪的Dream/LLaDA/Fast-dLLM等子目录，整体保留。模型下载和依赖安装仍按各目录README独立完成；这些快照不意味着与本项目CPU环境兼容，也不包含未公开数据/模型权重。
