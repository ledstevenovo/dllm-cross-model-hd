#!/usr/bin/env python
"""Step-1 CPU acceptance driver for the DynHD adapter.

Runs the whole self-test through the production wrapper and scripts, then writes
reports/dynhd_offline_selftest.json:

  A. 13 items (12 normal, 6/6 classes, +1 shape failure, two identical question texts)
  B. label failure + save failure injection
  C. interruption -> gap -> re-collect -> merge; config mismatch refused; duplicates
  D. reviewed label hash mismatch refused (no downgrade)
  E. engineering check, make_split, check_valid rejects fixture data, relabel keeps raw intact
  F. upstream CPU train -> eval on the fixture traces
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO / "references/repos/DynHD"))
import common  # noqa: E402

SELFTEST_ROOT = common.REPRO_ROOT / "engineering/selftest"
SMOKE = REPO / "data/raw_qa/subsets/smoke20.jsonl"
ENV = {**os.environ, "PYTHONPATH": str(REPO / "references/repos/DynHD"),
       "HF_HOME": "/root/autodl-tmp/hf-cache", "HF_HUB_OFFLINE": "1"}
PY = sys.executable


def run(cmd, cwd=REPO):
    started = time.time()
    proc = subprocess.run([str(part) for part in cmd], cwd=str(cwd), env=ENV,
                          capture_output=True, text=True)
    return {"cmd": " ".join(str(part) for part in cmd), "exit": proc.returncode,
            "seconds": round(time.time() - started, 2),
            "stdout_tail": (proc.stdout or "")[-1500:], "stderr_tail": (proc.stderr or "")[-1500:]}


def wrapper(subset, out, run_id, *, fault_plan=None, extra=(), model="llada"):
    cmd = [PY, SCRIPT_DIR / "collect_local.py", "--model", model,
           "--config", REPO / f"configs/dynhd_repro/{model}_local.yaml",
           "--subset", subset, "--fixture", "fault" if fault_plan else "trivial",
           "--run-id", run_id, "--output-dir", out, *extra]
    if fault_plan:
        cmd += ["--fault-plan", fault_plan]
    return run(cmd)


def write_subset(path: Path, rows):
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n")


def main() -> int:
    if SELFTEST_ROOT.exists():
        shutil.rmtree(SELFTEST_ROOT)
    root = SELFTEST_ROOT / "run"
    root.mkdir(parents=True)
    report = {"date": time.strftime("%Y-%m-%d"), "root": str(root), "scenarios": {}, "assertions": [], "ok": True}
    smoke_rows = [json.loads(line) for line in SMOKE.read_text(encoding="utf-8").splitlines() if line.strip()]

    def check(name, condition, detail=""):
        report["assertions"].append({"name": name, "ok": bool(condition), "detail": detail})
        if not condition:
            report["ok"] = False

    # ---------- A. 13 items: 12 normal (6/6) + 1 shape failure + duplicate question text
    rows = [dict(row) for row in smoke_rows[:12]]
    dup = dict(rows[0]); dup["sample_id"] = rows[0]["sample_id"] + "dup"
    rows.append(dup)
    splits = ["train"] * 7 + ["validation"] * 2 + ["test"] * 4
    for position, row in enumerate(rows):
        row["split"] = splits[position]
    subset13 = root / "acceptance13.jsonl"
    write_subset(subset13, rows)
    # deterministic labels with both classes in train and val: index parity
    labels13 = {row["sample_id"]: (0 if i % 2 == 0 else 1) for i, row in enumerate(rows)}
    plan13 = {"labels": labels13, "per_item": {rows[12]["sample_id"]: {"shape_failure": True}}}
    plan13_path = root / "plan13.json"
    plan13_path.write_text(json.dumps(plan13, ensure_ascii=False))
    run_a = root / "runA"
    result_a = wrapper(subset13, run_a, "runA", fault_plan=plan13_path)
    report["scenarios"]["A_shape_failure"] = result_a
    gaps_a = {row["sample_id"]: row for row in json.loads((run_a / "gaps.json").read_text())["gaps"]}
    shape_id = rows[12]["sample_id"]
    check("A: exit is non-zero", result_a["exit"] != 0, f"exit={result_a['exit']}")
    check("A: 12 traces saved", len(list(run_a.glob('*.pt'))) == 12, f"files={len(list(run_a.glob('*.pt')))}")
    check("A: shape failure recorded with actual_T",
          gaps_a.get(shape_id, {}).get("actual_T") == 63, json.dumps(gaps_a.get(shape_id)))
    check("A: two identical question texts kept distinct",
          rows[0]["question"] == dup["question"] and rows[0]["sample_id"] != dup["sample_id"])

    # ---------- B. label failure + save failure
    rows_b = [dict(row) for row in smoke_rows[12:15]]
    for row in rows_b:
        row["split"] = "train"
    subset_b = root / "three.jsonl"
    write_subset(subset_b, rows_b)
    plan_b = {"labels": {rows_b[0]["sample_id"]: 0, rows_b[1]["sample_id"]: 1},
              "per_item": {rows_b[1]["sample_id"]: {"label_failure": True},
                           rows_b[2]["sample_id"]: {"save_failure": True}}}
    plan_b_path = root / "planB.json"; plan_b_path.write_text(json.dumps(plan_b, ensure_ascii=False))
    run_b = root / "runB"
    result_b = wrapper(subset_b, run_b, "runB", fault_plan=plan_b_path)
    report["scenarios"]["B_label_save_failure"] = result_b
    gaps_b = {row["sample_id"]: row for row in json.loads((run_b / "gaps.json").read_text())["gaps"]}
    check("B: exit is non-zero", result_b["exit"] != 0)
    check("B: 1 saved", len(list(run_b.glob('*.pt'))) == 1)
    check("B: label stage failure recorded", gaps_b.get(rows_b[1]["sample_id"], {}).get("stage") == "label")
    check("B: save stage failure recorded", gaps_b.get(rows_b[2]["sample_id"], {}).get("stage") == "save")

    # ---------- C. interruption -> gap -> re-collect -> merge
    rows_c = [dict(row) for row in smoke_rows[15:20]] + [dict(smoke_rows[0])]
    rows_c[5] = dict(rows_c[5]); rows_c[5]["sample_id"] = rows_c[5]["sample_id"] + "c6"
    for row in rows_c:
        row["split"] = "train"
    subset_c = root / "six.jsonl"
    write_subset(subset_c, rows_c)
    plan_c = {"labels": {row["sample_id"]: (0 if i < 3 else 1) for i, row in enumerate(rows_c)},
              "per_item": {rows_c[3]["sample_id"]: {"abort": True}}}
    plan_c_path = root / "planC.json"; plan_c_path.write_text(json.dumps(plan_c, ensure_ascii=False))
    plan_c2 = {"labels": plan_c["labels"]}  # refill runs: the interruption was transient
    plan_c2_path = root / "planC2.json"; plan_c2_path.write_text(json.dumps(plan_c2, ensure_ascii=False))
    run_c1 = root / "runC1"
    result_c1 = wrapper(subset_c, run_c1, "runC1", fault_plan=plan_c_path)
    report["scenarios"]["C1_interrupted"] = result_c1
    gaps_c1 = [row["sample_id"] for row in json.loads((run_c1 / "gaps.json").read_text())["gaps"]
               if row["state"] == "not_started"]
    check("C1: abort exit code 3", result_c1["exit"] == 3, f"exit={result_c1['exit']}")
    check("C1: 3 saved / 3 not started", len(list(run_c1.glob('*.pt'))) == 3 and len(gaps_c1) == 3)

    ids_file = root / "gap_ids.txt"
    ids_file.write_text("\n".join(gaps_c1) + "\n")
    run_c2 = root / "runC2"
    result_c2 = wrapper(subset_c, run_c2, "runC2", fault_plan=plan_c2_path, extra=["--only-question-ids", ids_file])
    report["scenarios"]["C2_gap_refill"] = result_c2
    check("C2: gap refill saves 3", len(list(run_c2.glob('*.pt'))) == 3 and result_c2["exit"] == 0)

    merged = root / "mergedC"
    result_merge = run([PY, SCRIPT_DIR / "merge_runs.py", "--inputs", run_c1, run_c2, "--out", merged])
    report["scenarios"]["C_merge"] = result_merge
    check("C: merge OK with 6 samples", result_merge["exit"] == 0 and len(list(merged.glob('*.pt'))) == 6)

    run_c3 = root / "runC3"
    result_c3 = wrapper(subset_c, run_c3, "runC3", fault_plan=plan_c2_path, extra=["--only-question-ids", ids_file])
    duplicate_default = run([PY, SCRIPT_DIR / "merge_runs.py", "--inputs", run_c2, run_c3, "--out", root / "merged_dup"])
    duplicate_prefer = run([PY, SCRIPT_DIR / "merge_runs.py", "--inputs", run_c2, run_c3, "--out", root / "merged_prefer", "--prefer", "runC3"])
    report["scenarios"]["C_duplicate_default"] = duplicate_default
    report["scenarios"]["C_duplicate_prefer"] = duplicate_prefer
    check("C: duplicate merge fails by default", duplicate_default["exit"] != 0)
    check("C: --prefer resolves same-config duplicates", duplicate_prefer["exit"] == 0)

    run_d = root / "runD"
    result_d = wrapper(subset_b, run_d, "runD", fault_plan=plan_b_path, extra=["--collection-seed", "424242"])
    mismatch = run([PY, SCRIPT_DIR / "merge_runs.py", "--inputs", run_c1, run_d, "--out", root / "merged_mismatch"])
    report["scenarios"]["C_config_mismatch"] = mismatch
    check("C: different fingerprint refused", mismatch["exit"] != 0)

    # ---------- D. reviewed label with wrong answer hash must fail (no downgrade)
    reviewed_rows = [{"sample_id": rows_b[0]["sample_id"], "question_id": rows_b[0]["question_id"],
                      "label": 0, "human_reviewed": True, "label_source": "human:selftest",
                      "reviewed_at": "2026-10-21T00:00:00Z", "generated_text_sha256": "0" * 64}]
    labels_file = root / "reviewed_wrong.jsonl"
    labels_file.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in reviewed_rows) + "\n")
    subset_e = root / "one.jsonl"
    write_subset(subset_e, [dict(rows_b[0], split="train")])
    run_e = root / "runE"
    result_e = wrapper(subset_e, run_e, "runE", fault_plan=plan_b_path,
                       extra=["--labels", "reviewed", "--labels-file", labels_file])
    report["scenarios"]["D_reviewed_hash_mismatch"] = result_e
    check("D: reviewed hash mismatch fails the item", result_e["exit"] != 0 and not list(run_e.glob('*.pt')))

    # ---------- E. checks and relabel
    eng = run([PY, SCRIPT_DIR / "check_engineering.py", "--data-dir", run_a,
               "--out", root / "check_engineering.json"])
    report["scenarios"]["E_engineering"] = eng
    check("E: check_engineering accepts fixture traces", eng["exit"] == 0)

    split_out = root / "splits/pilot200.json"
    index_map_out = root / "splits/index_map.json"
    split_result = run([PY, SCRIPT_DIR / "make_split.py", "--subset", subset13, "--valid-dir", run_a,
                        "--out", split_out, "--index-map", index_map_out])
    report["scenarios"]["E_make_split"] = split_result
    check("E: make_split builds a covering split", split_result["exit"] == 0)

    relabel_labels = root / "relabel_labels.jsonl"
    relabel_rows = []
    for i, row in enumerate(rows[:12]):
        relabel_rows.append({"sample_id": row["sample_id"], "question_id": row["question_id"],
                             "decision": "include" if i < 10 else "exclude",
                             "label": 0 if i % 2 == 0 else 1,
                             "human_reviewed": True, "label_source": "human:selftest-fixture",
                             "reviewed_at": "2026-10-21T00:00:00Z",
                             "generated_text_sha256": common.sha256_text(f"fixture answer for {row['sample_id']}"),
                             "exclude_reason": "selftest exclude"})
    relabel_labels.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in relabel_rows) + "\n")
    valid_dir = root / "pilot200/valid"; excluded_dir = root / "pilot200/excluded"
    relabel_result = run([PY, SCRIPT_DIR / "relabel.py", "--subset", subset13, "--raw-dir", run_a,
                          "--labels-file", relabel_labels, "--valid-dir", valid_dir,
                          "--excluded-dir", excluded_dir, "--report", root / "relabel.json"])
    report["scenarios"]["E_relabel"] = relabel_result
    relabel_report = json.loads((root / "relabel.json").read_text()) if (root / "relabel.json").exists() else {}
    check("E: relabel wrote 10 valid + 2 excluded and raw unchanged",
          relabel_result["exit"] == 0 and relabel_report.get("included") == 10
          and relabel_report.get("excluded") == 2 and relabel_report.get("raw_unchanged") is True)
    validity = run([PY, SCRIPT_DIR / "check_valid.py", "--model", "llada", "--valid-dir", valid_dir,
                    "--split", split_out, "--index-map", index_map_out, "--out", root / "check_valid.json"])
    report["scenarios"]["E_check_valid_rejects_fixture"] = validity
    check("E: check_valid rejects fixture data (needs real reviewed labels)", validity["exit"] != 0)

    # ---------- F. upstream CPU train -> eval on fixture traces
    train_out = root / "train"
    train_result = run([PY, "-m", "dynhd.cli.train_detector", "--data-path", run_a, "--out-dir", train_out,
                        "--device", "cpu", "--seed", "42", "--split", split_out,
                        "--max-steps", "64", "--prompt-dim", "8", "--hidden-dim", "16",
                        "--epochs-stage1", "2", "--epochs-stage2", "3", "--batch-size", "4", "--verbose"])
    report["scenarios"]["F_train"] = train_result
    check("F: CPU training完成", train_result["exit"] == 0 and (train_out / "detector.pt").exists())
    eval_result = run([PY, "-m", "dynhd.cli.eval_detector", "--data-path", run_a,
                       "--ckpt", train_out / "detector.pt", "--split", split_out,
                       "--split-part", "test", "--device", "cpu", "--threshold", "0.5"])
    report["scenarios"]["F_eval"] = eval_result
    check("F: CPU eval runs on the test partition", eval_result["exit"] == 0)

    out_path = REPO / "reports/dynhd_offline_selftest.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"assertions: {sum(1 for a in report['assertions'] if a['ok'])}/{len(report['assertions'])} ok")
    for assertion in report["assertions"]:
        print(("  ok  " if assertion["ok"] else "  FAIL") , assertion["name"], assertion["detail"])
    print("selftest:", "OK" if report["ok"] else "FAILED", "->", out_path)
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
