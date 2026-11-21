"""`work batch done` re-runs the tests that failed first (b474, batch_rerun) and a test marked `budget` is retried
once before it fails (tests/scripts/conftest.py)."""
import pathlib
import subprocess
import sys
from types import SimpleNamespace

import batch_rerun
import batch_tasks
import pytest
from shop_files import Refused

CONFTEST = pathlib.Path(__file__).resolve().parent / "conftest.py"

OUTPUT = """\
..F.E
=========================== short test summary info ============================
FAILED tests/scripts/test_a.py::test_one - AssertionError: assert 1 == 2
FAILED tests/scripts/test_a.py::test_two[x-1]
ERROR tests/scripts/test_b.py::test_three - RuntimeError: boom
ERROR tests/scripts/test_c.py
2 failed, 2 passed, 2 errors in 0.12s
"""


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True, capture_output=True)
    return tmp_path


def test_the_failed_ids_are_read_off_pytest_s_summary():
    assert batch_rerun.failed(OUTPUT) == ["tests/scripts/test_a.py::test_one", "tests/scripts/test_a.py::test_two[x-1]",
                                          "tests/scripts/test_b.py::test_three", "tests/scripts/test_c.py"]
    assert batch_rerun.failed("all good\n3 passed in 0.1s\n") == []


def test_the_ids_are_kept_in_the_git_dir_per_task_never_in_the_tree(repo):
    assert batch_rerun.kept(repo, "batch-1-t1") == []
    batch_rerun.keep(repo, "batch-1-t1", ["tests/x.py::test_a", "tests/x.py::test_b"])
    assert batch_rerun.kept(repo, "batch-1-t1") == ["tests/x.py::test_a", "tests/x.py::test_b"]
    assert batch_rerun.kept(repo, "batch-1-t2") == []
    assert str(batch_rerun.where(repo, "batch-1-t1")).startswith(str(repo / ".git"))
    status = subprocess.run(["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True).stdout
    assert status == ""
    batch_rerun.keep(repo, "batch-1-t1", [])
    assert batch_rerun.kept(repo, "batch-1-t1") == []


class Runner:
    """A stand-in for run_tests: each call's args recorded, each answered by the next (exit, output)."""

    def __init__(self, *answers):
        self.answers, self.calls = list(answers), []

    def __call__(self, args):
        self.calls.append(list(args))
        code, out = self.answers.pop(0)
        return "pytest " + " ".join(args), SimpleNamespace(returncode=code, stdout=out, stderr="")


def test_with_nothing_kept_the_whole_run_is_made_and_its_failures_kept(repo):
    run = Runner((1, "FAILED tests/x.py::test_a - boom\n"))
    _, done = batch_rerun.tests(repo, "batch-1-t1", run)
    assert run.calls == [[]] and done.returncode == 1
    assert batch_rerun.kept(repo, "batch-1-t1") == ["tests/x.py::test_a"]


def test_a_kept_failure_that_still_fails_is_refused_without_the_whole_run(repo):
    batch_rerun.keep(repo, "batch-1-t1", ["tests/x.py::test_a"])
    run = Runner((1, "FAILED tests/x.py::test_a - boom\n"))
    _, done = batch_rerun.tests(repo, "batch-1-t1", run)
    assert run.calls == [["tests/x.py::test_a"]] and done.returncode == 1
    assert batch_rerun.kept(repo, "batch-1-t1") == ["tests/x.py::test_a"]


def test_once_the_kept_failures_pass_the_whole_run_is_made_and_a_pass_forgets_them(repo):
    batch_rerun.keep(repo, "batch-1-t1", ["tests/x.py::test_a"])
    run = Runner((0, "1 passed\n"), (0, "9 passed\n"))
    _, done = batch_rerun.tests(repo, "batch-1-t1", run)
    assert run.calls == [["tests/x.py::test_a"], []] and done.returncode == 0
    assert batch_rerun.kept(repo, "batch-1-t1") == []


def test_a_focused_run_that_fails_naming_no_test_falls_back_to_the_whole_run(repo):
    batch_rerun.keep(repo, "batch-1-t1", ["tests/gone.py::test_a"])
    run = Runner((4, "ERROR: not found: tests/gone.py::test_a\n"), (1, "FAILED tests/x.py::test_b\n"))
    _, done = batch_rerun.tests(repo, "batch-1-t1", run)
    assert run.calls == [["tests/gone.py::test_a"], []] and done.returncode == 1
    assert batch_rerun.kept(repo, "batch-1-t1") == ["tests/x.py::test_b"]


def test_tests_pass_runs_a_task_s_failures_first(repo):
    (repo / ".shop").mkdir()
    (repo / ".shop/delivery.toml").write_text('[batch]\ntests = "python3 -m pytest -q -p no:cacheprovider"\n')
    (repo / "test_a.py").write_text("def test_ok():\n    pass\n\ndef test_bad():\n    assert False\n")
    with pytest.raises(Refused) as first:
        batch_tasks.tests_pass(repo, repo, "work batch done", key="batch-1-t1")
    assert "test_a.py::test_bad" in str(first.value)
    assert batch_rerun.kept(repo, "batch-1-t1") == ["test_a.py::test_bad"]
    with pytest.raises(Refused) as again:
        batch_tasks.tests_pass(repo, repo, "work batch done", key="batch-1-t1")
    assert "-p no:cacheprovider test_a.py::test_bad`" in str(again.value)
    (repo / "test_a.py").write_text("def test_ok():\n    pass\n\ndef test_bad():\n    pass\n")
    batch_tasks.tests_pass(repo, repo, "work batch done", key="batch-1-t1")
    assert batch_rerun.kept(repo, "batch-1-t1") == []


def run_budget(tmp_path, body):
    (tmp_path / "pytest.ini").write_text("[pytest]\nmarkers =\n    budget: retried once\n")
    (tmp_path / "test_t.py").write_text("import pathlib\nimport pytest\n\nCOUNT = pathlib.Path(__file__).parent / "
                                        "'count'\n\n\n" + body)
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:xdist",
                           "-p", "conftest", str(tmp_path)], cwd=tmp_path, capture_output=True, text=True,
                          env={**batch_tasks.scripts_env(), "PYTHONPATH": str(CONFTEST.parent)})


COUNTED = """
@pytest.mark.budget
def test_slow():
    n = int(COUNT.read_text()) if COUNT.exists() else 0
    COUNT.write_text(str(n + 1))
    assert n >= %d
"""


def test_a_budget_test_over_its_budget_once_passes_on_its_retry(tmp_path):
    done = run_budget(tmp_path, COUNTED % 1)
    assert done.returncode == 0, done.stdout + done.stderr
    assert (tmp_path / "count").read_text() == "2"


def test_a_budget_test_over_its_budget_twice_fails(tmp_path):
    done = run_budget(tmp_path, COUNTED % 5)
    assert done.returncode == 1, done.stdout + done.stderr
    assert (tmp_path / "count").read_text() == "2"


def test_a_test_with_no_budget_mark_is_not_retried(tmp_path):
    done = run_budget(tmp_path, (COUNTED % 1).replace("@pytest.mark.budget\n", ""))
    assert done.returncode == 1
    assert (tmp_path / "count").read_text() == "1"
