"""Unit tests of decision-tiers r4 and r5 (workflow simplification plan 6, D5): `model decisions --check` checks the
index, then runs each `check` decision's tests in the repository, one pytest run a decision with the repository's
`addopts` cleared and nothing written, and names each failing decision. The scenarios are bound in
tests/scenarios/test_decision_tiers.py; these check what their steps do not (a test that does not run, the
repository's own settings, the files left behind, the runs side by side)."""

import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import model_decisions

SCRIPT = ROOT / "scripts" / "model"
PATH = "ex.com/prod/ctx"


@pytest.fixture
def repo(tmp_path_factory):
    root = tmp_path_factory.mktemp("repo")
    write(root, "spec/index.md", "---\nid: bounded-context/%s\n---\n# ctx\n" % PATH)
    return root


@pytest.fixture
def outside(tmp_path_factory):
    """A directory outside the repository, where a test leaves the mark that it ran."""
    return tmp_path_factory.mktemp("outside")


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def decision(root, name, tier="check", enforced_by=None):
    entries = "enforced_by: [%s]\n" % ", ".join(enforced_by) if enforced_by else ""
    write(root, "spec/decisions/%s.md" % name, "---\nid: design-decision/%s/%s\nsummary: s\nstatus: accepted\n"
          "tier: %s\n%s---\n# %s\n\n## Decision\nSo.\n" % (PATH, name, tier, entries, name))


def a_test(root, outside, name, body="pass", head=""):
    """tests/test_<name>.py: test_<name> marks that it ran outside the repository, then runs `body`."""
    write(root, "tests/test_%s.py" % name, "%sdef test_%s():\n    open(%r, 'a').write(%r)\n    %s\n"
          % (head, name, str(outside / "ran"), name + "\n", body))
    return "tests/test_%s.py::test_%s" % (name, name)


def ran(outside):
    mark = outside / "ran"
    return mark.read_text().split() if mark.exists() else []


def check(root):
    subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "decisions"], capture_output=True, check=True)
    return subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "decisions", "--check"],
                          capture_output=True, text=True)


def ident(name):
    return "design-decision/%s/%s" % (PATH, name)


def test_a_passing_check_decision_holds(repo, outside):
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a")])
    r = check(repo)
    assert r.returncode == 0, r.stdout + r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "spec/decisions/index.md is current", r.stdout
    assert "holds    spec/decisions/a.md (%s): tests/test_a.py::test_a" % ident("a") in lines, r.stdout
    assert lines[-1] == "1 check decisions: 1 hold, 0 failing", r.stdout


def test_a_failing_test_names_its_decision(repo, outside):
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a")])
    decision(repo, "b", enforced_by=[a_test(repo, outside, "b", body="assert 1 == 2, 'the bar is broken'")])
    r = check(repo)
    assert r.returncode == 1, r.stdout
    assert "failing  spec/decisions/b.md (%s): tests/test_b.py::test_b: exit 1" % ident("b") in r.stdout, r.stdout
    assert any(line.startswith("    ") and "the bar is broken" in line for line in r.stdout.splitlines()), r.stdout
    assert "holds    spec/decisions/a.md" in r.stdout, r.stdout
    assert r.stdout.splitlines()[-1] == "2 check decisions: 1 hold, 1 failing", r.stdout


def test_a_check_decision_with_no_test_is_failing(repo):
    decision(repo, "a")
    r = check(repo)
    assert r.returncode == 1, r.stdout
    assert "failing  spec/decisions/a.md (%s): names no test" % ident("a") in r.stdout, r.stdout


def test_only_check_decisions_run(repo, outside):
    write(repo, "tests/test_r.py", "def test_r():\n    assert False\n")
    decision(repo, "r", tier="requirement", enforced_by=["thing#r1"])
    decision(repo, "j", tier="judgement")
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a")])
    r = check(repo)
    assert r.returncode == 0, r.stdout
    assert "spec/decisions/r.md" not in r.stdout and "spec/decisions/j.md" not in r.stdout, r.stdout
    assert ran(outside) == ["a"], ran(outside)
    assert r.stdout.splitlines()[-1] == "1 check decisions: 1 hold, 0 failing", r.stdout


def test_a_stale_index_still_runs_the_tests(repo, outside):
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a")])
    subprocess.run([sys.executable, str(SCRIPT), "--root", str(repo), "decisions"], capture_output=True, check=True)
    write(repo, "spec/decisions/index.md", "# Decisions\n\nnothing here\n")
    r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(repo), "decisions", "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 1, r.stdout
    assert "spec/decisions/index.md is not what `model decisions` writes: run it" in r.stdout, r.stdout
    assert "holds    spec/decisions/a.md" in r.stdout, r.stdout
    assert ran(outside) == ["a"]


@pytest.mark.parametrize("case", ["not found", "collects nothing", "timed out"])
def test_a_test_that_does_not_run_is_failing(repo, outside, case):
    if case == "not found":
        a_test(repo, outside, "a")
        decision(repo, "a", enforced_by=["tests/test_a.py::test_nothing"])
        r = check(repo)
        assert r.returncode == 1 and "failing  spec/decisions/a.md" in r.stdout and ": exit 4" in r.stdout, r.stdout
    elif case == "collects nothing":
        write(repo, "tests/test_e.py", "")
        decision(repo, "a", enforced_by=["tests/test_e.py"])
        r = check(repo)
        assert r.returncode == 1 and "failing  spec/decisions/a.md" in r.stdout and ": exit 5" in r.stdout, r.stdout
    else:
        decision(repo, "a", enforced_by=[a_test(repo, outside, "a", body="__import__('time').sleep(5)")])
        found = model_decisions.check_tests(repo, timeout=1)
        assert [x.holds for x in found] == [False], found
        lines, ok = model_decisions.report(found)
        assert not ok and any(line.endswith("tests/test_a.py::test_a: timed out after 1 s") for line in lines), lines


def test_the_repositorys_addopts_do_not_deselect_a_named_test(repo, outside):
    write(repo, "pytest.ini", '[pytest]\naddopts = -m "not timing"\nmarkers =\n    timing: slow\n')
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a", head="import pytest\n\n\n@pytest.mark.timing\n")])
    r = check(repo)
    assert r.returncode == 0, r.stdout
    assert ran(outside) == ["a"], r.stdout
    assert "holds    spec/decisions/a.md" in r.stdout, r.stdout


def files(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if ".git" not in p.relative_to(root).parts)


def test_the_check_writes_nothing_in_the_repository(repo, outside):
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a")])
    decision(repo, "b", enforced_by=[a_test(repo, outside, "b", body="assert False")])
    subprocess.run([sys.executable, str(SCRIPT), "--root", str(repo), "decisions"], capture_output=True, check=True)
    before = files(repo)
    r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(repo), "decisions", "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 1, r.stdout
    assert sorted(ran(outside)) == ["a", "b"], r.stdout
    assert files(repo) == before, sorted(set(files(repo)) - set(before))


@pytest.mark.timing
def test_the_decisions_run_side_by_side(repo, outside):
    for name in "abc":
        decision(repo, name, enforced_by=[a_test(repo, outside, name, body="__import__('time').sleep(1)")])
    start = time.monotonic()
    found = model_decisions.check_tests(repo)
    took = time.monotonic() - start
    assert [x.holds for x in found] == [True] * 3, found
    assert took < 2.5, took


@pytest.mark.parametrize("case", ["skipped", "xfailed"])
def test_a_test_that_is_skipped_or_xfailed_is_failing(repo, outside, case):
    """Review S1: a skip or an xfail exits 0 and enforces nothing, so it does not hold."""
    body = "__import__('pytest').skip('no tool')" if case == "skipped" else "assert False"
    head = "" if case == "skipped" else "import pytest\n\n\n@pytest.mark.xfail\n"
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a", body=body, head=head)])
    r = check(repo)
    assert r.returncode == 1, r.stdout
    assert "failing  spec/decisions/a.md (%s): tests/test_a.py::test_a: not run: 1 %s" % (ident("a"), case) \
        in r.stdout, r.stdout


@pytest.mark.parametrize("entry", ["--co", "../outside.py"])
def test_an_entry_that_is_not_a_test_of_the_repository_is_failing(repo, outside, entry):
    """Review S2: an option, or a file outside the root, is never run and never holds."""
    a_test(repo, outside, "a")
    write(repo.parent, "outside.py", "def test_o():\n    pass\n")
    decision(repo, "a", enforced_by=[entry])
    r = check(repo)
    assert r.returncode == 1, r.stdout
    assert "failing  spec/decisions/a.md (%s): %s: not a test of this repository: %s" % (ident("a"), entry, entry) \
        in r.stdout, r.stdout
    assert model_decisions.wrong(repo, "check", [entry], []) == ["enforced_by %s: not a file of this repository"
                                                                  % entry]


def test_the_tests_run_under_the_projects_interpreter(repo, outside):
    """Review S3: a project's `.venv/bin/python` runs its decisions' tests."""
    stub = write(repo, ".venv/bin/python", "#!/bin/sh\necho stub-python-ran \"$@\" >> %s\nexec %s \"$@\"\n"
                 % (outside / "python", sys.executable))
    stub.chmod(0o755)
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a")])
    found = model_decisions.check_tests(repo)
    assert [x.holds for x in found] == [True], found
    assert "stub-python-ran" in (outside / "python").read_text()


@pytest.mark.parametrize("status", ["superseded", "rejected"])
def test_a_decision_not_in_force_is_not_run(repo, outside, status):
    """Review M2: history's tests never refuse anything."""
    decision(repo, "a", enforced_by=[a_test(repo, outside, "a", body="assert False")])
    path = repo / "spec/decisions/a.md"
    path.write_text(path.read_text().replace("status: accepted", "status: %s" % status))
    assert model_decisions.check_tests(repo) == []


def test_a_test_id_holding_a_hash_is_a_test():
    """Review M3: only `<capability>#r<n>` or `#r<a>-r<b>` is a requirement."""
    tests, reqs = model_decisions.split(["tests/test_c.py::test_c[a#b]", "work-queue#r1", "dmc#r22-r24"])
    assert (tests, reqs) == (["tests/test_c.py::test_c[a#b]"], ["work-queue#r1", "dmc#r22-r24"])
