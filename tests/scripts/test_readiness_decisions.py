"""The tier-1 decision checks in the readiness bar (workflow simplification plan 6, D13): each `check` design-decision
that a capability of an item's lines rests on (`rests_on:`) runs its tests on the root checkout, and a failing one is a
reason the item is not passing. A decision no capability of the item rests on is not run, and each runs once a
process."""
import pathlib
import re
import sys

import backlog_items
import model_decisions
import pytest
import readiness_bar
from backlog_testing import git, work, write_item
from test_backlog_lines import ABANDON, FROBNICATE

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

FULL = "design-decision/ex.com/prod/ctx/c"


@pytest.fixture
def outside(tmp_path_factory):
    return tmp_path_factory.mktemp("outside")


def rest_on(repo, outside, rests_on="design-decision/c", passing=False, entries="[tests/test_c.py::test_c]"):
    """spec/decisions/c.md, a `check` decision enforced by tests/test_c.py::test_c (failing unless `passing`), which
    marks outside the repository that it ran; work-queue rests on `rests_on`; all committed."""
    toolchain.require()
    (repo / "spec" / "decisions").mkdir(exist_ok=True)
    (repo / "spec" / "decisions" / "c.md").write_text(
        "---\nid: %s\nsummary: s\nstatus: accepted\ntier: check\nenforced_by: %s\n---\n# c\n\n## Decision\nSo.\n"
        % (FULL, entries))
    (repo / "tests").mkdir(exist_ok=True)
    (repo / "tests" / "test_c.py").write_text("def test_c():\n    open(%r, 'a').write('c')\n    assert %s\n"
                                              % (str(outside / "ran"), passing))
    cap = repo / "spec" / "capabilities" / "work-queue.md"
    cap.write_text(re.sub(r"(?m)^rests_on: .*$", "rests_on: [%s]" % rests_on if rests_on else "rests_on: []",
                          cap.read_text(), count=1))
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "a check decision")


def shaped(repo, name="b1", text=ABANDON):
    write_item(repo, name, status="shaped")
    done = work(repo, "line", name, "--into", "work-queue", text)
    assert done.returncode == 0, done.stderr


@pytest.mark.parametrize("form", ["design-decision/c", FULL])
def test_a_failing_check_decision_the_capability_rests_on_is_a_reason(ready_repo, outside, form):
    rest_on(ready_repo, outside, rests_on=form)
    shaped(ready_repo)
    done = work(ready_repo, "ready", "b1")
    assert done.returncode == 1, done.stdout
    assert "design-decision c (check) fails: tests/test_c.py::test_c: exit 1" in done.stderr, done.stderr
    assert backlog_items.find(ready_repo, "b1").status == "shaped"


def test_a_passing_check_decision_readies(ready_repo, outside):
    rest_on(ready_repo, outside, passing=True)
    shaped(ready_repo)
    done = work(ready_repo, "ready", "b1")
    assert done.returncode == 0, done.stderr
    assert backlog_items.find(ready_repo, "b1").status == "ready"
    assert (outside / "ran").exists()


def test_a_decision_the_capability_does_not_rest_on_is_not_run(ready_repo, outside):
    rest_on(ready_repo, outside, rests_on=None)
    shaped(ready_repo)
    done = work(ready_repo, "ready", "b1")
    assert done.returncode == 0, done.stderr
    assert not (outside / "ran").exists()


def test_a_check_decision_with_no_test_is_a_reason(ready_repo, outside):
    rest_on(ready_repo, outside, entries="[]")
    shaped(ready_repo)
    done = work(ready_repo, "ready", "b1")
    assert done.returncode == 1, done.stdout
    assert "design-decision c (check) names no test" in done.stderr, done.stderr


def test_each_decision_runs_once_a_process(ready_repo, outside, monkeypatch):
    rest_on(ready_repo, outside, passing=True)
    shaped(ready_repo, "b1")
    shaped(ready_repo, "b2")
    calls = []
    real = model_decisions.run

    def counted(root, decision, timeout=model_decisions.TIMEOUT):
        calls.append(decision.rel)
        return real(root, decision, timeout)
    monkeypatch.setattr(model_decisions, "run", counted)
    monkeypatch.setattr(readiness_bar, "_RAN", {})
    for name in ("b1", "b2"):
        assert readiness_bar.check(ready_repo, backlog_items.find(ready_repo, name))[0] == []
    assert calls == ["spec/decisions/c.md"], calls


def test_the_decisions_come_after_the_lines(ready_repo, outside):
    rest_on(ready_repo, outside)
    shaped(ready_repo, text=FROBNICATE)
    done = work(ready_repo, "ready", "b1")
    assert done.returncode == 1, done.stdout
    reasons = [x for x in done.stderr.splitlines() if x.startswith("  ")]
    assert "frobnicate" in reasons[0] and "design-decision c (check) fails" in reasons[-1], done.stderr


def test_a_superseded_check_decision_is_not_run(ready_repo, outside):
    """Review M2: a decision no longer in force refuses no item."""
    rest_on(ready_repo, outside)
    path = ready_repo / "spec" / "decisions" / "c.md"
    path.write_text(path.read_text().replace("status: accepted", "status: superseded"))
    assert readiness_bar.rested_on(ready_repo, backlog_lines_of(ready_repo)) == []


def backlog_lines_of(repo):
    shaped(repo)
    item = backlog_items.find(repo, "b1")
    return readiness_bar.backlog_lines.read(item, readiness_bar.rel_of(item.name))
