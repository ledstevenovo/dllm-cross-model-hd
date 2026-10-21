# SDD ledger — plan: docs/VGPU_32GB_完整实验方案.md (stage 2)

Scope: local implementation of real-model collectors and CPU evidence, then commit/push. GPU/model-weight acceptance remains pending.

Pre-flight: collectors produce trace-v1 NPZ; offline extraction consumes trace-v1 and question_id, while multi-seed sample_id differs. CLI must preserve question_id and emit combined generation-compatible rows.
Ruling: existing plan is a narrative runbook, not task-start machine format; retain that scope and use this ledger plus TDD cases rather than introducing a second planning framework.
Ruling: preserve user's modified docs/T4_传输清单.md; do not stage it.
Ruling: use native pinned Dream hooks (already shifted) rather than a reimplementation. Verify against the exact vendored Apache sampler.
Ruling: LLaDA v1 supports greedy low-confidence only, CFG=0; reject unsupported stochastic settings instead of approximating them.
Ruling: chat end-of-turn IDs must trim the effective answer just like EOS; full fixed-length token arrays remain stored.

Task 1: collector algorithm/statistics/shift — implemented; initial RED imports, GREEN sampler/reference/observer tests.
Task 2: atomic store/resume — implemented; config mismatch/corrupt hash/orphan adoption/lock tests.
Task 3: CLI/loading/manifests — implemented; explicit fixture mode runs same actual adapter path; native source guard and forward counts tested.
Task 4: full CPU verification, documentation, final review, commit/push — in progress.

Environment: separate ignored .venv-collector-test inherits already installed CPU torch 2.13.0; Transformers 4.46.2 installed there. CPU project lock not changed. No model weights/GPU inference.


Final review: fresh-context reviewer found three Important issues. All accepted for one TDD fix pass.
Final: fixed Dream FP16 native entropy NaN — explicit CLI/loader rejection plus raw-logits guard. FP16 regression reproduced NaN before fix; BF16/FP32 unchanged.
Final: fixed NPZ durability ordering — file fsync and POSIX directory sync before manifest ack; ordering/failure-injection tests RED then GREEN. Real power-loss and GPU tests remain out of local scope.
Final: fixed mutable revision bypass — require immutable full SHA for model/tokenizer before opening run/loading; RED rejection test then GREEN.
Final: Ruling: actual model/CUDA/VRAM/scientific quality set aside by reviewer — correctly retained as explicit on-GPU acceptance, not inferred from fixture results.
Final: Ruling: default T4 Dream NF4 plan is not safe with current native FP16 entropy — mark that route blocked pending a separately audited sampler, preserve BF16 mainline. No silent numerical patch to upstream sampler.
Final: minor (deferred): none.

Final: fixed clean-clone test bootstrap — fresh git archive exposed 85 passed/15 setup errors because configured .tmp/pytest parent was absent; conftest now creates only the missing parent, then rerun archive acceptance.

Task 4: local implementation complete — full CPU 100 passed; base CPU 82 passed/2 optional skips; clean Git export 100 passed; 40-trace reviewed CLI + offline join verified. Source hashes checked before staging delivery evidence. Commit/push delivery checked separately against remote main.

Stage 2 follow-on（无卡准备，2026-10-21）: 32GB方案第1–2节执行 — 权重缓存31,262,468,976字节（LLaDA 6分片16文件、Dream 4分片18文件）经独立复核逐文件哈希16/16+18/18全通过；.venv-llada（transformers4.46.3）与.venv-dream（4.46.2）以--system-site-packages继承平台torch2.8.0+cu128（venv内不装torch）；HF_HOME=/root/autodl-tmp/hf-cache；生产load_components离线CPU真实加载通过（LLaDA 29.1s/8,015,581,184参数；Dream 78.1s/7,615,616,512参数，含Dream源码锁校验），两venv fixture单题演练通过。有卡单题/smoke20、显存、BF16与驱动核验仍待执行。证据reports/phase2_env_prep.json。

TRE 复现线（2026-10-21/22）：R0 验收通过（LLaDA FP16、L128/S64/B128、prompt③、seed 20261021；20/20、逐文件哈希一致、observer 20/20、每步 2 token、token 赋值 0/2560 失败、重复 3/3 相同；揭示集合重放 1079/1280 步一致，其余为 FP16 置信度与 FP32 记录的近并列互换，规则与冻结参考逐项一致）；正式 800 题采集完成（800/800、problems 0、哈希一致、token 赋值 0/51200、有效长度 1/12/126、769 eot + 31 eos、空答/截断 0、尾部占比 0.563）。证据 reports/tre_repro/{pilot_report.md,protocol_diff.md,run800_summary.json}；judge（J2）待 API key 与客户端，评分入口 scripts/score_tre_repro.py 已就绪。

DynHD 复现线（2026-10-21/22）：步骤0（.venv-dynhd 继承平台 torch2.8.0+cu128、pinned 依赖、上游 7/7 测试、快照 36 文件哈希核验）→ 步骤1（scripts/dynhd_repro/ 全部脚本 + CPU 验收 22/22 断言：形状/标签/保存失败、中断补采合并、异配置拒绝、重复默认失败与 --prefer、reviewed 哈希绑定、raw 不变、正式 check_valid 拒绝 fixture 数据、CPU train→eval）→ 步骤2（两模型单题：LLaDA load 5.6s/峰值 15.1GiB、Dream 4.3s/14.5GiB；hook 对齐 5/5 逐值相等（LLaDA identity、Dream after-shift）；观测无干扰 token 完全一致；decode 规则与受控序列单元检查通过）。发现并修复上游 bug：Dream `generation_logits_hook_func=None` 在固定 revision 会崩，包装器加 None→identity shim（不改上游快照）。证据 reports/dynhd_{env,offline_selftest,singleq}.json；步骤3（smoke20）未执行。
