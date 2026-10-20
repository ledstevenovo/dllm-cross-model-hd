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
