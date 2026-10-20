# 当前状态（已暂停）

写于用户要求暂停时。交接细节见 `HANDOFF.md`，这里只记「做了什么、什么还没做」。

## 已提交的 4 个提交

| commit | 内容 |
|---|---|
| `e9c8001` | 初版管线：schema / 归一化 / 冻结 prompt / 哈希划分 / 标签协议 / 构建器 / uv.lock / pyproject.toml |
| `42e6da1` | 金标泄漏规则收紧为「仅金标 value 命中即剔除」+ `build_dataset.py --dry-run` |
| `d125343` | 冻结题池 + smoke20 / small200 + `.gitattributes` + 构建清单 |
| `f8f888a` | `HANDOFF.md` |

## 数据准备闭环：已完成并验证

- 冻结池 **16,606 条 / 16,605 个 cluster**：train 9,922｜validation 2,481｜test 4,182 cluster（4,183 条）｜smoke20 20。
- **泄漏检查全部为 0**：cluster 跨 split、同文问题跨 split、重复 sample_id、smoke 混入研究池、small200 不在 test。任一不过脚本拒绝落盘。
- **可复现性已实测**：两次独立构建的 10 个输出文件 sha256 **逐字节一致**，仅 `git_commit` 与时间戳不同。
- 权威清单 `data/manifests/build_dataset_latest.json`，其中 `code.git_commit = 42e6da1`。
- 冻结 prompt 指纹 `sha256:0de959aec7090589f83e17ef5ac034a76266f87f2452449bc94a8ff35753356b`。

## 暂停时仍未提交的改动

- `src/labeling.py`：**修复拒绝语检测的真 bug**。原文用 `normalize_text()`（保留标点）去匹配按「标点已变空格」写成的正则，
  导致 `"I don't know."` 被判为 `incorrect` —— 即被算进幻觉正类，正是该模块要避免的混淆。
  已改为 `collapse_whitespace(remove_punctuation(normalize_text(text)))`。
  **影响面**：只影响标签，而标签尚未产出（`data/labels/` 为空），**不影响已冻结的题池产物**。
- `tests/conftest.py`、`tests/test_textnorm.py`：新建，**从未运行**。
- 计划中的其余 5 个测试文件：**未写**。

## 未完成

1. `tests/`：计划 7 个文件（textnorm / prompts / labeling / splitting / schema / artifacts / build_dataset），现有 2 个；`pytest` 未跑过。
2. `docs/`：`DATASET.md`、`LABEL_PROTOCOL.md`、`ENVIRONMENT.md`、根 `README.md`、`data/README.md` 全部未写。
3. 独立复核脚本（不 import `src/`，从 JSONL 重新推导不变量）未写。

## 环境要害（细节见 `HANDOFF.md` §3）

uv 的 `lock`/`sync` 需一次性提权；`tempfile` 在本沙箱有缺陷（`0o700` 目录不可写），靠 `_pyfix/sitecustomize.py` 绕过；
Git Bash 的 `curl` 不可用，一律用 `urllib`；控制台默认 GBK，须 `PYTHONIOENCODING=utf-8`；
`.gitattributes` 把 `data/**` 标为 `-text`，**不要删**（否则 fresh clone 后 manifest 的哈希校验会失败）。
