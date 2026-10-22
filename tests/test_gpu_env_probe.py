"""The GPU probe must not fail the reference device it is meant to qualify.

History: the probe originally required the device's exact ``sm_XY`` tag to appear
in ``torch.cuda.get_arch_list()``.  The cu128 wheel used here lists sm_86 but not
sm_89, so the 4080 SUPER -- the machine every pilot200 number came from -- reported
``ok=false`` while actually reproducing pilot200 bit for bit.  A qualification
check that rejects the reference device is a bug in the check, not evidence about
the device.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from gpu_arch import arch_covered  # noqa: E402

WHEEL = ["sm_70", "sm_75", "sm_80", "sm_86", "sm_90", "sm_100", "sm_120"]


def test_exact_match_is_a_direct_hit():
    assert arch_covered((12, 0), WHEEL) == (True, "exact")


def test_minor_version_compatibility_accepts_sm89_via_sm86():
    covered, how = arch_covered((8, 9), WHEEL)
    assert covered is True
    assert "sm_86" in how and "sm_89" in how


def test_newer_major_is_not_covered_by_an_older_one():
    # sm_90 cubins do not run on sm_100; major versions are not binary compatible.
    assert arch_covered((10, 0), ["sm_70", "sm_80", "sm_86", "sm_90"])[0] is False


def test_major_absent_from_the_wheel_is_not_covered():
    assert arch_covered((8, 0), ["sm_70", "sm_75"])[0] is False


def test_highest_compatible_minor_is_reported():
    _, how = arch_covered((8, 9), ["sm_80", "sm_86", "sm_120"])
    assert "sm_86" in how


def test_sm120_blackwell_still_needs_its_own_entry():
    # The 5090 relies on an exact sm_120 entry; sm_100 does not cover it.
    assert arch_covered((12, 0), ["sm_70", "sm_80", "sm_90", "sm_100"])[0] is False
