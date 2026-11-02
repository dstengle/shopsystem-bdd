"""supervise_merge: a scenario that failed gets one run alone however many runs it failed in (r219), and one that passes
that run alone counts as passing whatever another run gave (r222); a run with an error, a failure that is not a
scenario, or a rerun that ran no test is not taken back."""
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import supervise  # noqa: F401  (its import order settles the modules' circular imports)
import supervise_merge
from supervise_merge import Merge

NODE = "tests/scenarios/test_thing.py::test_it_closes"
FAILED = "FAILED %s - boom\nSCENARIO %s\n" % (NODE, NODE)     # work_items names the failed tests that are scenarios


def ran(args, code, out=""):
    return SimpleNamespace(args=args, returncode=code, stdout=out, stderr="")


class Stubbed(Merge):
    def __init__(self, root):
        self.root, self.branch, self.logged, self.moves = root, "i1", [], []
        self.suite_out = FAILED

    def under_work(self, tree, name):
        return []

    def suite_record(self, tree, suite):
        return "Suite", ran(suite, 1, self.suite_out)

    def log(self, **fields):
        self.logged.append(fields)

    def move(self, *args):
        self.moves.append(args)


@pytest.fixture
def merge(monkeypatch, tmp_path):
    alone, alone_passes, rerun_out = [], [], ["1 passed"]

    def run(command, **_):
        if any("::" in c for c in command):
            alone.append(command)
            passed = alone_passes[len(alone) - 1]
            return ran(command, 0 if passed else 1, rerun_out[0] if passed else "boom")
        return ran(command, 1, FAILED)

    monkeypatch.setattr(supervise_merge.subprocess, "run", run)
    monkeypatch.setattr(supervise_merge, "git", lambda *a, **k: SimpleNamespace(stdout="x\n", returncode=0))
    monkeypatch.setattr(supervise_merge, "with_scripts", dict)
    tests = {"work_item": ["pytest", "-n", "auto", "--work-item", "w1"], "suite": ["pytest", "-n", "auto", "--work-item", "w1", "--whole-suite"]}
    return Stubbed(tmp_path), tests, alone, alone_passes, rerun_out


def test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges(merge):
    stubbed, tests, alone, passes, _ = merge
    passes.extend([True, False])     # a second alone run would fail: it must not happen
    assert stubbed.merge("w1", stubbed.root, tests) is None
    assert len(alone) == 1
    assert "--whole-suite" in alone[0]
    assert [alone[0][i + 1] for i, a in enumerate(alone[0]) if a == "-n"] == ["0"]     # no other -n value


def test_a_scenario_failing_in_both_runs_and_failing_alone_refuses_the_merge_after_one_run_alone(merge):
    stubbed, tests, alone, passes, _ = merge
    passes.extend([False, True])
    question = stubbed.merge("w1", stubbed.root, tests)
    assert question and "boom" in question
    assert len(alone) == 1


def test_the_question_gives_the_first_run_of_a_scenario_that_failed_only_in_the_suite_run(merge):
    stubbed, tests, alone, passes, _ = merge
    other = "tests/scenarios/test_other.py::test_other"
    stubbed.suite_out = FAILED + "FAILED %s - bang\nSCENARIO %s\n" % (other, other)
    passes.extend([True, False])     # NODE passes alone, OTHER does not
    question = stubbed.merge("w1", stubbed.root, tests)
    assert "bang" in question and " ".join(tests["suite"]) in question
    assert "FAILED %s - bang" % other in question.partition("`%s`" % " ".join(alone[1]))[0]
    assert "boom" in question.partition("`%s`" % " ".join(alone[1]))[2]
    assert not [l for l in stubbed.logged if l.get("event") == "rerun"]


def test_a_failing_run_with_an_error_line_is_not_taken_back(merge):
    stubbed, tests, alone, passes, _ = merge
    stubbed.suite_out = "=== short test summary info ===\n" + FAILED + "ERROR tests/scenarios/test_x.py::t - setup\n"
    passes.append(True)
    assert stubbed.merge("w1", stubbed.root, tests)
    assert not alone


def test_a_failing_node_that_is_not_a_scenario_is_not_taken_back(merge):
    stubbed, tests, alone, passes, _ = merge
    stubbed.suite_out = "FAILED tests/scripts/test_y.py::test_y - boom\n"     # in a module that has scenarios( in it
    passes.append(True)
    assert stubbed.merge("w1", stubbed.root, tests)
    assert not alone


def test_a_suite_command_with_no_n_gets_none_for_the_rerun(merge):
    stubbed, tests, alone, passes, _ = merge
    tests["suite"] = ["pytest", "--work-item", "w1", "--whole-suite"]
    passes.append(True)
    assert stubbed.merge("w1", stubbed.root, tests) is None
    assert "-n" not in alone[0]


def test_an_error_count_in_a_failing_scenarios_captured_output_does_not_keep_it_from_being_taken_back(merge):
    stubbed, tests, _, passes, _ = merge
    stubbed.suite_out = FAILED + "Found 2 errors.\n1 failed, 3 passed in 1.0s\n"
    passes.append(True)
    assert stubbed.merge("w1", stubbed.root, tests) is None


def test_an_error_count_in_the_final_line_keeps_a_run_from_being_taken_back(merge):
    stubbed, tests, alone, passes, _ = merge
    stubbed.suite_out = FAILED + "1 failed, 3 passed, 1 error in 1.0s\n"
    passes.append(True)
    assert stubbed.merge("w1", stubbed.root, tests)
    assert not alone


def test_a_rerun_that_ran_no_test_counts_as_failed(merge):
    stubbed, tests, alone, passes, rerun_out = merge
    rerun_out[0] = "1 deselected"
    passes.append(True)
    assert stubbed.merge("w1", stubbed.root, tests)
    assert len(alone) == 1
