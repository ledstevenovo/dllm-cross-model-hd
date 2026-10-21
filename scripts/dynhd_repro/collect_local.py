#!/usr/bin/env python
"""Local DynHD collection wrapper (step-1 execution contract).

Runs the upstream ``dynhd.cli.collect_traces`` pipeline through explicit interface
patches: local frozen subset, offline provisional/reviewed labels, per-item seeds,
start/saved/failed events, generation fingerprint, feature pre-checks and fixtures.

正式采集必须经过本入口；CPU 替身（--fixture）只写入 engineering/selftest/。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
UPSTREAM = REPO / "references/repos/DynHD"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(UPSTREAM))

import torch  # noqa: E402

import common  # noqa: E402
import fixtures  # noqa: E402

from dynhd.cli import collect_traces as upstream  # noqa: E402
from dynhd.data import save_trace_with_prompt_emb as upstream_save  # noqa: E402
from dynhd.data.io import load_trace as upstream_load_trace  # noqa: E402
from dynhd.labeling import OpenAIChatLabeler as UpstreamLabeler  # noqa: E402
from dynhd.model import DreamDiffusionSampler, DreamModel, LLaDAModel, LLaDASampler  # noqa: E402

STATE: Dict[str, Any] = {}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DynHD local collection (see plan step 1)")
    parser.add_argument("--model", choices=["llada", "dream"], required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--subset", required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dataset", default="triviaqa", choices=["triviaqa", "hotpotqa", "commonsenseqa"])
    parser.add_argument("--labels", choices=["provisional", "reviewed"], default="provisional")
    parser.add_argument("--labels-file")
    parser.add_argument("--only-question-ids")
    parser.add_argument("--fixture", choices=["trivial", "fault"])
    parser.add_argument("--fault-plan")
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--num-steps", type=int)
    parser.add_argument("--gen-length", type=int, default=64)
    parser.add_argument("--collection-seed", type=int, default=20261020)
    return parser


def family_of(model_path: str) -> str:
    return "dream" if "dream" in model_path.lower() else "llada"


class RecordingLabeler:
    """Wrap any labeler so every failure lands in the run's failed events (stage=label)."""

    def __init__(self, inner):
        self.inner = inner

    def label_one(self, *args, **kwargs):
        item = fixtures.Context.current()
        try:
            return self.inner.label_one(*args, **kwargs)
        except Exception as error:
            _record_failure(item, "label", error)
            raise


class ProvisionalLabeler:
    """Offline proposal: upstream substring matcher, no network. label 0=correct, 1=hallucination."""

    def label_one(self, question=None, ground_truth=None, generated=None) -> Dict[str, Any]:
        item = fixtures.Context.current()
        text = str(generated or "")
        if not text.strip():
            fixtures.Context.provisional_kind = "refusal_empty"
            return {"label": 1, "rationale": "provisional: empty output"}
        match = UpstreamLabeler.check_correctness_match(text, ground_truth)
        fixtures.Context.provisional_kind = "correct" if match == 0 else "incorrect"
        return {"label": int(match), "rationale": "provisional: offline substring proposal"}


class ReviewedLabeler:
    """Reviewed re-collection: labels must come from a human-reviewed file and match the answer hash."""

    def __init__(self, labels_file: Path):
        self.rows = {}
        for line in labels_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                key = row.get("question_id") or row.get("sample_id")
                self.rows[key] = row

    def label_one(self, question=None, ground_truth=None, generated=None) -> Dict[str, Any]:
        item = fixtures.Context.current()
        row = self.rows.get(item["question_id"]) or self.rows.get(item["id"])
        if row is None:
            raise RuntimeError(f"reviewed labels missing question {item['question_id']}")
        if row.get("human_reviewed") is not True:
            raise RuntimeError("reviewed labels must carry human_reviewed=true")
        label = int(row.get("label", -1))
        if label not in (0, 1):
            raise RuntimeError(f"reviewed label must be 0/1, got {row.get('label')}")
        expected = row.get("generated_text_sha256")
        if expected and expected != common.sha256_text(str(generated or "")):
            raise RuntimeError("reviewed answer hash does not match the regenerated answer")
        if row.get("source_trace_path") and row.get("source_trace_sha256"):
            if common.sha256_file(Path(row["source_trace_path"])) != row["source_trace_sha256"]:
                raise RuntimeError("reviewed source trace hash mismatch")
        fixtures.Context.provisional_kind = "reviewed"
        return {"label": label, "rationale": f"reviewed: {row.get('label_source', 'human')}"}


class ValidatingSampler:
    """Wrap any sampler; enforce features [steps, 3] finite and record timing/memory."""

    def __init__(self, inner, steps: int):
        self.inner = inner
        self.steps = int(steps)

    def __getattr__(self, name):
        return getattr(self.inner, name)

    def sample(self, *args, **kwargs):
        item = fixtures.Context.current()
        try:
            if torch.cuda.is_available():
                torch.cuda.reset_peak_memory_stats()
            started = __import__("time").perf_counter()
            result = self.inner.sample(*args, **kwargs)
            elapsed = __import__("time").perf_counter() - started
            stats = {"elapsed_seconds": round(elapsed, 4), "actual_T": None}
            if torch.cuda.is_available():
                stats["peak_memory_bytes"] = {"allocated": int(torch.cuda.max_memory_allocated()),
                                              "reserved": int(torch.cuda.max_memory_reserved())}
            features = result.get("features")
            if not isinstance(features, torch.Tensor):
                raise RuntimeError(f"features must be a tensor, got {type(features)}")
            shape = tuple(features.shape)
            stats["actual_T"] = int(shape[0]) if len(shape) == 2 else None
            if len(shape) != 2 or shape[1] != 3:
                raise RuntimeError(f"features must be [T,3], got {shape}")
            if shape[0] != self.steps:
                raise RuntimeError(f"actual_T={shape[0]} differs from requested steps={self.steps}")
            if not bool(torch.isfinite(features).all()):
                raise RuntimeError("features contain non-finite values")
            STATE.setdefault("item_stats", {})[item["id"]] = stats
            return result
        except Exception as error:
            stats = STATE.setdefault("item_stats", {}).get(item["id"], {})
            _record_failure(item, "sample", error, actual_t=stats.get("actual_T"))
            raise


def _events() -> common.EventLog:
    log = STATE.get("events")
    if log is None:
        log = common.EventLog(Path(STATE["output_dir"]) / "events.jsonl")
        STATE["events"] = log
    return log


def _record_failure(item: Dict[str, Any], stage: str, error: Exception, actual_t: Optional[int] = None) -> None:
    row = {"sample_id": item["id"], "question_id": item.get("question_id"), "run_id": STATE["run_id"],
           "stage": stage, "exception": f"{type(error).__name__}: {error}", "actual_T": actual_t}
    STATE.setdefault("failures", {})[item["id"]] = row
    try:
        _events().write("failed", **row)
    except Exception:
        pass


def _patched_load_dataset_items(name: str, split: str, limit: int):
    items = STATE["items"]
    if limit != len(items):
        raise RuntimeError(f"inner loader asked for {limit} items but task list has {len(items)}")
    return [{"id": it["id"], "question": it["question"], "answer": it["answer"]} for it in items]


def _patched_question_content(item: Dict[str, Any]) -> str:
    our = STATE["index"][item["id"]]
    fixtures.Context.set_item(our)
    _events().write("start", sample_id=our["id"], question_id=our["question_id"], run_id=STATE["run_id"],
                    item_seed=our["item_seed"], generation_fingerprint=STATE["fingerprint"],
                    prompt_sha256=common.sha256_text(our["prompt"]), stage="sample")
    STATE.setdefault("started", set()).add(our["id"])
    return our["prompt"]


def _patched_build_model_and_sampler(model_path: str, device: str, inference: Dict[str, Any], steps: int):
    if STATE.get("fixture"):
        model = fixtures.FixtureModel(steps=steps)
        inner = fixtures.FixtureSampler(model, steps=steps, fault_plan=STATE["fault_plan"])
        return STATE["family"], model, ValidatingSampler(inner, steps)
    import time
    started = time.perf_counter()
    if STATE["family"] == "dream":
        model = DreamModel(model_path, device=device)
        common.coerce_dream_logits_hook(model)
        inner = DreamDiffusionSampler(
            model,
            num_steps=steps,
            temperature=float(inference.get("temperature", 0.2)),
            top_p=inference.get("top_p", 0.95),
            top_k=inference.get("top_k"),
            alg=str(inference.get("dream_alg", "entropy")),
            alg_temp=float(inference.get("dream_alg_temp", 0.0)),
        )
        STATE["load_seconds"] = round(time.perf_counter() - started, 3)
        return "dream", model, ValidatingSampler(inner, steps)
    model = LLaDAModel(model_path, device=device)
    STATE["load_seconds"] = round(time.perf_counter() - started, 3)
    return "llada", model, ValidatingSampler(LLaDASampler(model, num_steps=steps), steps)


def _patched_labeler_factory(*args, **kwargs):
    return STATE["labeler"]


def _patched_save(path: str, *, features, label: int, meta: Dict[str, Any], prompt_emb) -> None:
    item = fixtures.Context.current()
    plan = (STATE.get("fault_plan") or {}).get("per_item", {}).get(item["id"], {})
    try:
        if plan.get("save_failure"):
            raise RuntimeError(f"fixture save failure for {item['id']}")
        mode = "test_fixture" if STATE.get("fixture") else STATE["labels_mode"]
        meta = dict(meta)
        meta["labeling_method"] = "offline_match_proposal" if mode == "provisional" else mode
        meta["provisional"] = mode == "provisional"
        meta["test_fixture"] = bool(STATE.get("fixture"))
        meta["provisional_kind"] = fixtures.Context.provisional_kind
        meta["label_source"] = ("assistant:offline-proposal" if mode == "provisional"
                                else ("test_fixture" if mode == "test_fixture" else "human:reviewed"))
        meta["run_id"] = STATE["run_id"]
        meta["generation_fingerprint"] = STATE["fingerprint"]
        meta["collection_seed"] = STATE["collection_seed"]
        meta["item_seed"] = item["item_seed"]
        meta["dataset_arg_compat"] = "triviaqa"
        meta["prompt_sha256"] = common.sha256_text(item["prompt"])
        meta["answer_sha256"] = common.sha256_text(str(meta.get("generated_text", "")))
        stats = STATE.get("item_stats", {}).get(item["id"], {})
        for key in ("elapsed_seconds", "actual_T", "peak_memory_bytes"):
            if key in stats:
                meta[key] = stats[key]
        if "openai" in json.dumps(meta).lower():
            raise RuntimeError("metadata still mentions openai after rewrite")
        upstream_save(path, features=features, label=int(label), meta=meta, prompt_emb=prompt_emb)
        reloaded = upstream_load_trace(path)  # durability/format check before acknowledging
        if int(reloaded["label"]) != int(label):
            raise RuntimeError("reloaded trace label mismatch")
        file_sha = common.sha256_file(Path(path))
        _events().write("saved", sample_id=item["id"], question_id=item["question_id"],
                        run_id=STATE["run_id"], file=Path(path).name, file_sha256=file_sha,
                        label=int(label), provisional=meta["provisional"],
                        provisional_kind=meta["provisional_kind"])
        STATE.setdefault("saved", {})[item["id"]] = file_sha
    except Exception as error:
        _record_failure(item, "save", error)
        raise


def _generation_fingerprint(config: Dict[str, Any], family: str, args) -> str:
    inference = config.get("inference", {})
    payload = {
        "collector_version": "dynhd-local-v1",
        "model_family": family,
        "model_config": config.get("model", {}),
        "inference": {k: inference.get(k) for k in ("num_steps", "temperature", "top_p", "top_k",
                                                    "dream_alg", "dream_alg_temp")},
        "features": config.get("features", {}),
        "gen_length": args.gen_length,
        "steps": args.num_steps or inference.get("num_steps", 64),
        "prompt_source": "repo-frozen-subset-v1",
        "collection_seed": args.collection_seed,
        "seed_derivation": common.SEED_DERIVATION_VERSION,
        "dataset_arg_compat": "triviaqa",
        "code": {
            "upstream_collect_traces": common.sha256_file(UPSTREAM / "dynhd/cli/collect_traces.py"),
            "upstream_io": common.sha256_file(UPSTREAM / "dynhd/data/io.py"),
            "wrapper": common.sha256_file(SCRIPT_DIR / "collect_local.py"),
            "common": common.sha256_file(SCRIPT_DIR / "common.py"),
            "fixtures": common.sha256_file(SCRIPT_DIR / "fixtures.py"),
        },
    }
    return common.fingerprint(payload)


def main(argv: Optional[list] = None) -> int:
    args = build_parser().parse_args(argv)
    config = upstream.load_yaml_config(args.config)
    model_path = str(config.get("model", {}).get("model_path", ""))
    if not model_path:
        raise ValueError("config.model.model_path is required")
    family = family_of(model_path)
    if family != args.model:
        raise ValueError(f"--model {args.model} does not match config model_path family {family}")
    if args.labels == "reviewed" and not args.labels_file:
        raise ValueError("--labels reviewed requires --labels-file")
    if args.fixture == "fault" and not args.fault_plan:
        raise ValueError("--fixture fault requires --fault-plan")
    if args.fault_plan and args.fixture is None:
        raise ValueError("--fault-plan requires --fixture")

    output_dir = Path(args.output_dir).resolve()
    if args.fixture:
        selftest_root = (common.REPRO_ROOT / "engineering/selftest").resolve()
        if selftest_root not in output_dir.parents and output_dir != selftest_root:
            raise ValueError(f"fixture runs must stay under {selftest_root}")
    if output_dir.exists():
        raise FileExistsError(f"run directory already exists: {output_dir}")

    items = common.load_pool(Path(args.subset), Path(args.only_question_ids) if args.only_question_ids else None, args.limit)
    for item in items:
        item["item_seed"] = common.derive_item_seed(args.collection_seed, item["id"])

    fault_plan = None
    if args.fixture:
        fault_plan = json.loads(Path(args.fault_plan).read_text()) if args.fault_plan else {}
        if args.labels == "reviewed":
            labeler: Any = ReviewedLabeler(Path(args.labels_file))
        else:
            labeler = fixtures.FixtureLabeler(fault_plan)
    elif args.labels == "reviewed":
        labeler = ReviewedLabeler(Path(args.labels_file))
    else:
        labeler = ProvisionalLabeler()
    labeler = RecordingLabeler(labeler)

    STATE.clear()
    STATE.update({
        "items": items, "index": {it["id"]: it for it in items}, "family": family,
        "run_id": args.run_id or common.run_id_or_default(args.model, None),
        "output_dir": str(output_dir), "labeler": labeler, "labels_mode": args.labels,
        "fixture": args.fixture, "fault_plan": fault_plan or {}, "collection_seed": args.collection_seed,
        "events": None, "failures": {}, "saved": {}, "started": set(),
        "fingerprint": _generation_fingerprint(config, family, args),
        "config_path": str(Path(args.config).resolve()),
    })

    upstream._load_dataset_items = _patched_load_dataset_items
    upstream._question_content = _patched_question_content
    upstream._build_model_and_sampler = _patched_build_model_and_sampler
    upstream.OpenAIChatLabeler = _patched_labeler_factory
    upstream.save_trace_with_prompt_emb = _patched_save

    inner_argv = ["collect_traces", "--config", str(Path(args.config).resolve()), "--dataset", args.dataset,
                  "--split", "local", "--num-samples", str(len(items)),
                  "--gen-length", str(args.gen_length), "--output-dir", str(output_dir)]
    if args.num_steps is not None:
        inner_argv += ["--num-steps", str(args.num_steps)]

    exit_code = 0
    error_text = None
    saved_argv = sys.argv
    try:
        sys.argv = inner_argv
        upstream.main()
    except fixtures.AbortRun as error:
        exit_code, error_text = 3, f"aborted: {error}"
    except SystemExit as error:
        exit_code = int(error.code) if isinstance(error.code, int) else 1
        error_text = f"SystemExit({error.code})"
    except Exception as error:  # upstream raises RuntimeError when any item failed
        exit_code, error_text = 1, f"{type(error).__name__}: {error}"
    finally:
        sys.argv = saved_argv

    output_dir.mkdir(parents=True, exist_ok=True)
    events = _events()
    if error_text:
        events.write("run_failed", run_id=STATE["run_id"], error=error_text)
    saved_ids = set(STATE["saved"])
    failed = STATE.get("failures", {})
    gaps = []
    for item in items:
        if item["id"] in saved_ids:
            continue
        if item["id"] in failed:
            row = dict(failed[item["id"]]); row["state"] = "failed"
        else:
            row = {"sample_id": item["id"], "question_id": item["question_id"], "run_id": STATE["run_id"],
                   "stage": "not_started", "exception": None, "actual_T": None, "state": "not_started"}
        gaps.append(row)

    manifest = {
        "run_id": STATE["run_id"], "model_family": family, "config": config,
        "config_path": STATE["config_path"], "generation_fingerprint": STATE["fingerprint"],
        "collection_seed": args.collection_seed, "seed_derivation": common.SEED_DERIVATION_VERSION,
        "labels_mode": "test_fixture" if args.fixture else args.labels,
        "fixture": args.fixture, "dataset_arg_compat": "triviaqa",
        "task_list": [{"sample_id": it["id"], "question_id": it["question_id"], "item_seed": it["item_seed"]} for it in items],
        "task_list_sha256": common.fingerprint([it["id"] for it in items]),
        "environment": {"python": sys.version.split()[0], "torch": torch.__version__,
                        "transformers": __import__("transformers").__version__,
                        "cuda_available": torch.cuda.is_available()},
        "load_seconds": STATE.get("load_seconds"),
        "saved_count": len(saved_ids), "failed_count": len(failed),
        "not_started_count": sum(1 for g in gaps if g["state"] == "not_started"),
        "exit_code": exit_code, "error": error_text,
    }
    (output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    (output_dir / "gaps.json").write_text(json.dumps({"run_id": STATE["run_id"], "gaps": gaps}, indent=2, ensure_ascii=False) + "\n")
    if gaps:
        with open(output_dir / "failures.jsonl", "w", encoding="utf-8") as fh:
            for row in gaps:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        mirror = common.pilot_layout(output_dir)
        if mirror is not None:
            mirror.mkdir(parents=True, exist_ok=True)
            (mirror / f"{STATE['run_id']}.jsonl").write_text(
                "\n".join(json.dumps(row, ensure_ascii=False) for row in gaps) + "\n")
    events.write("run_finished", run_id=STATE["run_id"], exit_code=exit_code,
                 saved=len(saved_ids), failed=len(failed), not_started=manifest["not_started_count"])
    events.close()
    print(f"[wrapper] run={STATE['run_id']} saved={len(saved_ids)} failed={len(failed)} "
          f"not_started={manifest['not_started_count']} exit={exit_code}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
