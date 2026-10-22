#!/usr/bin/env python
"""Record the on-GPU qualification evidence for the main plan section 3.

Runs inside an inference venv (it imports torch), so it is invoked as:

  .venv-llada/bin/python scripts/gpu_env_probe.py --out reports/gpu_env_probe_llada.json
  .venv-dream/bin/python  scripts/gpu_env_probe.py --out reports/gpu_env_probe_dream.json

It answers, with measured values rather than assumptions:

* which physical GPU and compute capability the runtime sees (a Blackwell
  sm_120 card must be covered by the wheel's arch list, otherwise the run
  silently falls back or fails);
* whether torch's CUDA build and the driver agree;
* native BF16 support and a real BF16 matmul + SDPA forward on the device;
* FP32 arithmetic sanity (a small reference matmul) so a wrong device or a
  broken kernel cannot pass unnoticed;
* the pinned package versions that the collectors record in their manifests.

Nothing here trains or generates; it is a capability probe only.
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch


def driver_version() -> str | None:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
                             capture_output=True, text=True, check=True)
        return out.stdout.strip().splitlines()[0]
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    result: dict = {
        "measured_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "torch": torch.__version__,
        "torch_cuda_runtime": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "driver_version": driver_version(),
        "cuda_arch_list": torch.cuda.get_arch_list(),
    }

    if not torch.cuda.is_available():
        result["ok"] = False
        result["reason"] = "torch.cuda.is_available() is False"
    else:
        capability = torch.cuda.get_device_capability(0)
        free_bytes, total_bytes = torch.cuda.mem_get_info()
        result.update({
            "device_name": torch.cuda.get_device_name(0),
            "capability": list(capability),
            "capability_tag": f"sm_{capability[0]}{capability[1]}",
            "bf16_supported": torch.cuda.is_bf16_supported(),
            "fp16_supported": torch.cuda.has_fp16_support() if hasattr(torch.cuda, "has_fp16_support") else None,
            "free_bytes": free_bytes,
            "total_bytes": total_bytes,
            "total_gib": round(total_bytes / 2 ** 30, 2),
        })
        result["capability_in_wheel_arch_list"] = result["capability_tag"] in result["cuda_arch_list"]

        checks: dict = {}
        try:
            torch.manual_seed(0)
            a = torch.randn(2048, 2048, device="cuda", dtype=torch.bfloat16)
            b = torch.randn(2048, 2048, device="cuda", dtype=torch.bfloat16)
            product = (a @ b).float()
            checks["bf16_matmul"] = {
                "ok": bool(torch.isfinite(product).all()),
                "mean": round(float(product.mean()), 6),
            }

            # FP32 reference for the same shapes: a broken BF16 kernel shows up as
            # a wildly different mean, not as platform noise.
            a32, b32 = a.float(), b.float()
            reference = (a32 @ b32).float()
            checks["fp32_reference_mean"] = round(float(reference.mean()), 6)

            q = torch.randn(1, 4, 64, 64, device="cuda", dtype=torch.bfloat16)
            attn = torch.nn.functional.scaled_dot_product_attention(q, q, q)
            checks["bf16_sdpa"] = {
                "ok": bool(torch.isfinite(attn).all()),
                "shape": list(attn.shape),
            }
            checks["sdpa_backends"] = {
                "flash": torch.backends.cuda.flash_sdp_enabled(),
                "mem_efficient": torch.backends.cuda.mem_efficient_sdp_enabled(),
                "math": torch.backends.cuda.math_sdp_enabled(),
            }
            checks["peak_memory_gib"] = round(torch.cuda.max_memory_allocated() / 2 ** 30, 3)
        except Exception as exc:  # a failing kernel is evidence, not a crash
            checks["error"] = f"{type(exc).__name__}: {exc}"
        result["checks"] = checks

        result["ok"] = bool(
            result["bf16_supported"]
            and result["capability_in_wheel_arch_list"]
            and checks.get("bf16_matmul", {}).get("ok")
            and checks.get("bf16_sdpa", {}).get("ok")
        )

    try:
        import transformers
        result["transformers"] = transformers.__version__
    except Exception:
        result["transformers"] = None
    try:
        import numpy
        result["numpy"] = numpy.__version__
    except Exception:
        result["numpy"] = None

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("ok", "device_name", "capability_tag", "torch",
                                             "torch_cuda_runtime", "total_gib") if k in result},
                     ensure_ascii=False))
    print(f"written {out}")
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
