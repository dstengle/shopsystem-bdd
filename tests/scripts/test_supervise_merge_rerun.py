"""supervise_merge: a scenario that failed gets one run alone however many runs it failed in (r219), and one that passes
that run alone counts as passing whatever another run gave (r222)."""
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import supervise  # noqa: E402,F401  (its import order settles the modules' circular imports)
import supervise_merge  # noqa: E402
from supervise_merge import Merge  # noqa: E402

NODE = "tests/test_thing.py::test_it_closes"


def ran(args, code, out=""):
    return SimpleNamespace(args=args, returncode=code, stdout=out, stderr="")


class Stubbed(Merge):
    def __init__(self, root):
        self.root, self.branch, self.logged, self.moves = root, "i1", [], []

    def under_work(self, tree, name):
        return []

    def suite_record(self, tree, suite):
        return "Suite", ran(suite, 1, "FAILED %s - boom\n" % NODE)

    def log(self, **fields):
        self.logged.append(fields)

    def move(self, *args):
        self.moves.append(args)


@pytest.fixture
def merge(monkeypatch, tmp_path):
    alone = []

    def run(command, **_):
        if any("::" in c for c in command):
            alone.append(command)
            return ran(command, 0 if alone_passes[len(alone) - 1] else 1, "boom")
        return ran(command, 1, "FAILED %s - boom\n" % NODE)

    alone_passes = []
    monkeypatch.setattr(supervise_merge.subprocess, "run", run)
    monkeypatch.setattr(supervise_merge, "git", lambda *a, **k: SimpleNamespace(stdout="x\n", returncode=0))
    monkeypatch.setattr(supervise_merge, "with_scripts", lambda: {})
    tests = {"work_item": ["pytest", "-n", "auto", "--work-item", "w1"], "suite": ["pytest", "--whole-suite"]}
    stubbed = Stubbed(tmp_path)
    return stubbed, tests, alone, alone_passes


def test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges(merge):
    stubbed, tests, alone, passes = merge
    passes.extend([True, False])     # a second alone run would fail: it must not happen
    assert stubbed.merge("w1", tmp_path_of(stubbed), tests) is None
    assert len(alone) == 1 and "-n" not in alone[0]
    assert [l["scenario"] for l in stubbed.logged if l.get("event") == "rerun"] == [NODE]


def test_a_scenario_failing_in_both_runs_and_failing_alone_refuses_the_merge_after_one_run_alone(merge):
    stubbed, tests, alone, passes = merge
    passes.extend([False, True])
    question = stubbed.merge("w1", tmp_path_of(stubbed), tests)
    assert question and "boom" in question
    assert len(alone) == 1


def tmp_path_of(stubbed):
    return stubbed.root
