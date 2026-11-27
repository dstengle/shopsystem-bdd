"""batch_timings (b73, b876, measurement r13): the durations of a batch's test runs, of its opening and of each phase
of its opening, kept in the git common dir and read back for `measure batch`."""
import subprocess

import batch_timings
import pytest


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return tmp_path


def test_kept_runs_and_opening_read_back_by_batch(repo):
    batch_timings.kept(repo, "batch-1", "opening", 95.4)
    batch_timings.kept(repo, "batch-1", "done", 21, "t1")
    batch_timings.kept(repo, "batch-2", "done", 40, "t1")
    batch_timings.kept(repo, "batch-1", "review", 30.6)
    found = batch_timings.figures(repo, "batch-1")
    assert [(r["kind"], r["task"], r["seconds"]) for r in found["test_runs"]] == [("done", "t1", 21),
                                                                                    ("review", None, 30.6)]
    assert found["test_time_seconds"] == 52 and found["opening_time_seconds"] == 95
    assert not (repo / ".shop").exists() and batch_timings.path(repo).is_file()


def test_a_failing_run_is_kept_too(repo):
    with pytest.raises(RuntimeError), batch_timings.timed(repo, "batch-1", "done", "t2"):
        raise RuntimeError("tests failed")
    [run] = batch_timings.figures(repo, "batch-1")["test_runs"]
    assert run["task"] == "t2" and run["passed"] is False


def test_nothing_kept_reads_as_no_figure(repo):
    batch_timings.path(repo).parent.mkdir(parents=True)
    batch_timings.path(repo).write_text("not json\n")
    assert batch_timings.figures(repo, "batch-1") == {"test_runs": [], "test_time_seconds": 0,
                                                      "opening_time_seconds": None, "opening_phases": []}


def test_the_phases_of_the_last_opening_read_back_apart_from_the_test_runs(repo):
    batch_timings.kept_phases(repo, "batch-1", {"lay": 3.0})
    batch_timings.kept(repo, "batch-1", "opening", 10)
    batch_timings.kept_phases(repo, "batch-1", {"pick and readiness checks": 4.2, "lay": 1.4})
    batch_timings.kept(repo, "batch-1", "phase", 0.4, phase="lay")
    batch_timings.kept(repo, "batch-1", "opening", 7)
    found = batch_timings.figures(repo, "batch-1")
    assert found["opening_phases"] == [{"phase": "pick and readiness checks", "seconds": 4},
                                       {"phase": "lay", "seconds": 2}]
    assert found["test_runs"] == [] and found["opening_time_seconds"] == 7
