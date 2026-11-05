"""The trace of `pr-review` (workflow simplification plan 5, D19): a guarantees capability has no feature file, so no
strict xfail holds its ids. Instead each id out of `unbuilt:` must have a test named `test_r<n>_...` in one of the
files of `PR_REVIEW_TESTS`, and each id still in `unbuilt:` must have none."""
import re
from pathlib import Path

import spec_unbuilt

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PR_REVIEW_TESTS = ("test_batch_findings.py", "test_batch_brief.py", "test_batch_reviewed.py", "test_batch_fix_loop.py",
                   "test_agent_pr_reviewer.py", "test_skill_building_a_batch.py")
CAP = REPO / "spec" / "capabilities" / "pr-review.md"


def named_tests():
    found = set()
    for name in PR_REVIEW_TESTS:
        path = HERE / name
        if path.is_file():
            found |= set(re.findall(r"(?m)^def test_(r[1-9]\d*)_", path.read_text()))
    return found


def ids():
    return set(re.findall(r"(?m)^- \[(r[1-9]\d*)\] ", CAP.read_text()))


def test_every_built_pr_review_line_has_its_test():
    built = ids() - spec_unbuilt.unbuilt(REPO).get("pr-review", set())
    missing = sorted(built - named_tests(), key=lambda r: int(r[1:]))
    assert not missing, "pr-review ids out of unbuilt: with no test_r<n>_ test: %s" % ", ".join(missing)


def test_no_unbuilt_pr_review_line_has_a_test_yet():
    early = sorted(spec_unbuilt.unbuilt(REPO).get("pr-review", set()) & named_tests(), key=lambda r: int(r[1:]))
    assert not early, "pr-review ids still in unbuilt: with a test_r<n>_ test: %s" % ", ".join(early)
