"""Torch-free device/wheel architecture matching for the GPU qualification probe.

Kept separate from :mod:`scripts.gpu_env_probe` on purpose: the probe imports
torch, and the CPU-only project venv must still be able to test this logic.

An exact ``sm_XY`` entry in ``torch.cuda.get_arch_list()`` is a direct hit.  CUDA
also guarantees *minor-version binary compatibility* within one major version, so
a cubin built for ``sm_86`` runs on ``sm_89``.  That is the 4080 SUPER case: the
cu128 wheel lists sm_86 but not sm_89, and requiring an exact tag made the
reference device fail its own qualification while reproducing pilot200 bit for
bit.  Major versions are *not* compatible this way.
"""
from __future__ import annotations


def arch_covered(capability: tuple[int, int], arch_list: list[str]) -> tuple[bool, str]:
    """Return ``(covered, how)`` for a device capability against a wheel's arch list."""
    tag = f"sm_{capability[0]}{capability[1]}"
    if tag in arch_list:
        return True, "exact"
    same_major: list[tuple[int, str]] = []
    for entry in arch_list:
        if not entry.startswith("sm_"):
            continue
        digits = entry[3:]
        if len(digits) < 2 or not digits.isdigit():
            continue
        major, minor = int(digits[:-1]), int(digits[-1])
        if major == capability[0] and minor <= capability[1]:
            same_major.append((minor, entry))
    if same_major:
        best = max(same_major)[1]
        return True, f"minor-compatible ({best} cubin runs on {tag})"
    return False, "not covered by the wheel's arch list"
