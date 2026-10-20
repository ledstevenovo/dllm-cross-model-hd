> 历史交接快照：下文属于 DeepSeek 暂停时状态，部分划分、标签规则和环境描述已被后续修复替代。当前状态请读 README.md、STATUS.md 与 reports/takeover_progress.md。

# 交接说明 — dLLM 跨模型幻觉检测 · 数据准备阶段

> 面向接手者（人或 Codex）。读完 §0–§4 即可安全继续；§5 是剩余工作。

## 0. 快速接手

```bash
cd D:/paper/dllm-cross-model-hd
source scripts/env.sh                        # 设置 $PY / PYTHONPATH / 编码 / uv 目录
"$PY" scripts/download_raw.py                # 重新下载原始 parquet（已 gitignore，需先跑）
"$PY" scripts/build_dataset.py --dry-run     # 全流程 + 全部校验，不写盘
"$PY" scripts/build_dataset.py               # 重生成 data/raw_qa + manifest
"$PY" -m pytest -q                           # 测试：tests/ 尚未编写，见 §5
```

当前 `git log`：`d125343`（数据）← `42e6da1`（代码，**manifest 记录的 git_commit**）← `e9c8001`（初版）。
`data/manifests/build_dataset_latest.json` 是权威清单；工作树干净。

## 1. 目标与范围

研究目标（来自 `D:/paper/dLLM_跨模型幻觉检测_实验计划.md` v1.0）：在一个 dLLM 的去噪轨迹上训练幻觉检测器，
零样本迁移到另一个 dLLM（LLaDA-8B-Instruct ↔ Dream-7B-Instruct）。

**本次只做数据准备闭环**，已完成：下载 → 统一 schema → 去重 → 全局划分 → smoke20/small200 →
单一 no-context prompt → 标签协议 → 简单答案匹配 → manifest。**不涉及任何模型推理、torch 或 GPU。**

## 2. 现状与已验证证据

冻结池 **16,606 条 / 16,605 个 cluster**，落盘于 `data/raw_qa/`：

| split | clusters | records | TriviaQA | HotpotQA |
|---|---|---|---|---|
| train | 9,922 | 9,922 | 5,903 | 4,019 |
| validation | 2,481 | 2,481 | 1,483 | 998 |
| test | 4,182 | 4,183 | 2,529 | 1,654 |
| smoke20 | 20 | 20 | 12 | 8 |

- 流水线计数：读入 25,349 行 → 剔除 790 条可抄题（triviaqa 64 / hotpotqa 726）→ 保留 24,559 →
  折叠 7,953 个重复行 → 16,606 条。1 个标识符冲突簇（`bb_956`，一问两答）因此贡献 2 条记录。
- **泄漏检查全部为 0 并通过**：cluster 跨 split、同文问题跨 split、重复 sample_id、
  smoke 混入研究池、small200 不在 test。任一不过则脚本拒绝落盘。
- **可复现性已实测**：两次独立构建（`build_dataset_20261020T100241Z_f166b7a7` 与
  `..._T103213Z_f166b7a7`，同一配置指纹）的 10 个输出文件 **sha256 完全一致**，只有
  `git_commit` 与时间戳不同。
- schema 校验：`checked 16606, problems 0, duplicate_sample_ids 0`。
- 冻结 prompt 指纹 `sha256:0de959aec7090589f83e17ef5ac034a76266f87f2452449bc94a8ff35753356b`；
  配置指纹 `sha256:f166b7a7eab2a937700ec832c8dc1689120036c4448567fa38b090c14334faf5`。
- `small200` 抽自 test（121 triviaqa / 69 bridge / 10 comparison）；`smoke20` 在划分**之前**就已剔除。

## 3. 环境陷阱（必读，全部实测）

1. **`uv` 只能用于 `lock`/`sync`，且必须提权一次。** DSH 沙箱禁止子进程管道捕获 stdout，uv 探测解释器
   正好依赖它，会报 `Failed to query Python interpreter ... 拒绝访问。(os error 5)`。用
   `pwsh` + `sandbox_permissions: danger-full-access`（**带 `justification`**，否则报
   `invalid escalation`）跑一次即可。**日常跑 Python 只需 `"$PY"`，不需要提权。**
2. **`uv` 目录必须内指**，否则报 AppData 锁：`UV_CACHE_DIR` / `UV_PYTHON_INSTALL_DIR` /
   `UV_TOOL_DIR` / `UV_TOOL_BIN_DIR` / `TMPDIR` 全部指向仓库内（`scripts/env.sh` 已设）。
3. **`tempfile` 在本沙箱坏掉**：`os.mkdir(p, 0o700)` 建出的目录不可写，而 `tempfile.mkdtemp` 正是这么建的，
   导致 `pip`/`ensurepip` 解包失败。`_pyfix/sitecustomize.py` 重写了 `mkdtemp`/`mkstemp` 为默认权限创建，
   靠 `PYTHONPATH=…/_pyfix` 自动生效（`env.sh` 已设）。**该目录已 gitignore，且只在装包时需要**；
   正常跑构建/测试不需要它，但保留可避免复发。
4. **Git Bash 的 `curl` 不可用**（`schannel: SEC_E_NO_CREDENTIALS`）。所有下载走 Python `urllib`
   （`scripts/download_raw.py` 已是如此）。
5. **控制台默认 GBK，遇非 ASCII 直接崩**。`env.sh` 设了 `PYTHONIOENCODING=utf-8` 与 `PYTHONUTF8=1`。
6. **`.gitattributes` 是承重结构，别删。** 行尾被 Git 改写会让 fresh clone 的哈希校验失败，所以
   `*.jsonl` / `*.json` / `*.ids.txt` 标了 `-text`。
7. 环境：Python 3.13.14，`.venv` 与 `uv.lock` 严格一致（numpy 2.5.4 / pandas 3.0.6 / pyarrow 26.0.0 /
   pytest 9.1.1）。**未装 torch / scikit-learn**——检测器阶段再单独加依赖组。

## 4. 关键设计决策（附理由，勿轻易推翻）

- **划分单位是 cluster，不是行。** `cluster_id` 由 `(dataset, raw_id)` 与归一化问题文本共同决定；
  重复行折叠、标识符冲突变体（`base` / `base__alt1`）共享同一个 `cluster_id`，因此永不跨 split。
  `sample_id == question_id`；将来多种子采样时用 `sample_id = f"{question_id}__seed{k}"`。
- **划分用哈希分配，不切排序列表。** `assign_splits` 按 `sha256(seed,salt,cluster_id)` 落桶，
  `select_stratified` 按 `hash_rank` 取前 k。这样池子从 200 题扩到 2,000 题时，**已有分配不变**，
  不会因为扩容而重洗实验。
- **绝不使用 Python 内建 `hash()`**（按进程加盐，不可复现）。全部走 `hashlib.sha256`，用 `"\x1f"` 分隔。
- **只把金标 answer value 出现在题面视为泄漏。** 题面复现 alias 措辞不代表答案可抄
  （例：gold `Kilimanjaro` / alias `Highest mountain in Africa` / 题面即用该 alias），
  剔除会白白毁掉大量好题，所以 alias 命中**只计数不剔除**（`triviaqa:alias_phrase_in_prompt_kept 974`）。
  匹配用**归一化后的 token 序列相等**，非子串——否则 `Bull` 会误命中 `Bulldog`。
  剔除理由与样本存进 manifest 的 `excluded_copyable_questions`，可审计。开关是
  `configs/datasets/build.toml` 的 `cleaning.drop_gold_in_prompt`。
- **池只来自 held-out split**（triviaqa `rc.nocontext` 的 validation/test、hotpotqa `distractor` 的
  validation），原始训练语料无法泄进我们的评测划分。triviaqa test 被显式弃用（aliases 全空、value 全 `<unk>`），
  记在 manifest 的 `available_unused_inputs`。
- **prompt 是唯一冻结模板**，含版本号与指纹，`import` 时自校验（恰好一个 `{question}`、无其他花括号）；
  记录里存的是最终渲染文本 + 指纹，模型侧不得再拼模板。
- **标签五类互斥**：`correct` / `incorrect` / `refusal_empty` / `incomplete_truncated` / `format_failure`；
  阳性类只有 `incorrect`，三个弃答类可分别归并。匹配规则固定顺序：归一化精确 → 数值相等 → 是/否等价；
  **故意不做包含匹配**（`Paris` 不得匹配 `Paris, Texas`）。

## 5. 剩余工作

1. **`tests/`（未写）** —— `tests/conftest.py` 需把仓库根塞进 `sys.path`。计划文件与断言点：
   - `test_textnorm.py`：冠词/标点/大小写/空白；**不做重音折叠**（`cafe` 不匹配 `café`）；
     `extract_number` 收 `1,234` / `-3.5`、拒 `12%` / `12kg`；`strip_wrapping_quotes`；`is_yes_no`。
   - `test_prompts.py`：指纹等于上文字面值（回归闸）；`render_prompt` 只换 question；
     `answer_in_prompt` 的 token 边界（`Bull` 不匹配 `Bulldog`）；`assert_gold_not_in_prompt` 抛错路径。
   - `test_labeling.py`：`extract_candidate` 取**最后一个** `Answer:`；三条匹配规则；
     不做包含匹配；`classify_generation` 的优先级（空白→`format_failure`；命中即 `correct` 即使
     `hit_max_length`；拒绝语；空输出；复读题干→`format_failure`；截断；兜底 `incorrect`）。
   - `test_splitting.py`：同 seed/salt 确定性；比例和不为 1 时报错；`assign_splits` 全覆盖；
     `allocate_counts` 总数精确；`select_stratified` 在池扩容后选中集合不变。
   - `test_schema.py`：`finalize()` 回填派生字段；非法 split 被 `problems()` 抓到；`validate_records` 查重。
   - `test_artifacts.py`：**读已落盘产物**做自洽性校验（跨文件 sample_id 唯一、cluster 不跨 split、
     prompt 指纹一致、gold 不在题面、文件 sha256 与 manifest 对上）。这条最像"独立复核"。
   - `test_build_dataset.py`：`main(["--dry-run"])` 返回 0（需要 parquet，缺失时 skip）；纯函数单测。
2. **`docs/`（未写）**：`DATASET.md`（schema 字段、来源、计数、如何扩池）、`LABEL_PROTOCOL.md`
   （五类定义 + 三种评测口径 `EVAL_REGIMES` + 人工复核流程）、`ENVIRONMENT.md`（§3 的沉淀）、
   根 `README.md`、`data/README.md`。
3. 独立复核：复核人写一个**独立于 `src/`** 的脚本，从 `data/raw_qa/*.jsonl` 重新推导上述不变量，
   不得 import 构建代码（避免同源错误被继承）。这是计划 §4.3 与用户明确要求的交付项。

## 6. 文件地图

```
configs/datasets/build.toml    构建配置（来源映射、seed/salt、划分比例、子集大小、清洗开关）
scripts/env.sh                 唯一的环境入口：$PY / PYTHONPATH / 编码 / uv 目录
scripts/download_raw.py        urllib 幂等下载 + sha256 索引 → data/raw_download/raw_index.json
scripts/inspect_raw.py         parquet schema / 行数 / key 唯一性探查
scripts/build_dataset.py       主构建器（~845 行；--config / --repo-root / --dry-run）
src/schema.py                  QARecord 17 字段 + 校验
src/textnorm.py                SQuAD/HotpotQA 官方归一化（不做重音折叠）
src/prompts.py                 冻结 prompt 模板 + answer_in_prompt + 指纹
src/splitting.py               哈希划分 / 最大余额配比 / 分层抽样
src/labeling.py                五类标签 + 匹配规则 + 三种评测口径
src/io_utils.py                原子写 JSON/JSONL + sha256_file
data/raw_qa/{dataset}/{split}.jsonl            冻结池（已提交）
data/raw_qa/subsets/{smoke20,small200}.jsonl   子集 + 同名 .ids.txt（已提交）
data/manifests/build_dataset_latest.json       权威清单（已提交）
data/raw_download/                             原始 parquet，35M，gitignore，可由脚本重建
```

## 7. 红线

- **不要改** `PROMPT_TEMPLATE` / `PROMPT_TEMPLATE_VERSION`（会改指纹，下游轨迹全部作废）。要改就升版本。
- **不要让 Git 转换 `data/**` 的行尾**（`.gitattributes` 已保护，别绕开）。
- **不要提交**`.venv/`、`data/raw_download/`、`data/trajectories/`、`data/generations/`、`results/`、`reports/*.png`。
- **不要用无边界子串**做金标泄漏或答案匹配（`Bull`/`Bulldog`、`cafe`/`café` 都是实测踩过的坑）。
- **不要为了让检查通过而放宽校验**：`build_dataset.py` 在泄漏或 schema 不过时拒绝落盘，这是特性。
