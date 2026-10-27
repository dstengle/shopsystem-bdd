"""red-green r1 with the agent-time analysis of 2026-10-27: a work-item's worker is refused --whole-suite; work run (no
worker) and the branch review are not."""
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def run(tmp_path, worker):
    (tmp_path / "test_one.py").write_text("def test_one():\n    pass\n")
    env = dict(os.environ, PYTHONPATH=str(ROOT / "scripts"))
    env.pop("SHOPSYSTEM_WORK_RUN_WORKER", None)
    env.pop("PYTEST_ADDOPTS", None)
    if worker:
        env["SHOPSYSTEM_WORK_RUN_WORKER"] = worker
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "work_items", "-p", "no:cacheprovider",
                           "--work-item", "w1", "--whole-suite", str(tmp_path)], cwd=tmp_path, capture_output=True,
                          text=True, env=env)


def test_a_work_items_worker_is_refused_the_whole_suite(tmp_path):
    done = run(tmp_path, "w1")
    assert done.returncode != 0 and "--whole-suite is refused to w1's worker" in done.stderr + done.stdout


def test_work_run_itself_runs_the_whole_suite(tmp_path):
    assert run(tmp_path, None).returncode == 0


def test_the_branch_review_runs_the_whole_suite(tmp_path):
    assert run(tmp_path, "the branch review").returncode == 0
