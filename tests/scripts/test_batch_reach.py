"""The tests a task's change reaches (b456, batch_reach), and the pytest plugin leaving the others out."""
import os
import subprocess
import sys
from pathlib import Path

import batch_git
import batch_reach

FILES = {
    "spec/capabilities/batches.md": "", "spec/capabilities/review.md": "", "spec/capabilities/items.md": "",
    "features/review.feature": "", "tests/scenarios/test_batches.py": "", "tests/scenarios/test_review.py": "",
    "tests/scenarios/test_items.py": "", "scripts/batch_tasks.py": "", "scripts/spec_lf.py": "",
    "tests/scripts/test_batch_done.py": "", "tests/scripts/test_lf.py": "import spec_lf\n",
    "tests/scripts/test_other.py": "", "tests/scripts/helper_testing.py": "import batch_tasks\n",
    "tests/scripts/test_helped.py": "from helper_testing import x\n",
}


def repo(tmp_path):
    for rel, text in FILES.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    for args in (("init", "-q", "-b", "main"), ("add", "-A"), ("-c", "user.name=t", "-c", "user.email=t@e",
                                                              "commit", "-q", "-m", "base")):
        batch_git.git(tmp_path, *args)
    return batch_git.git(tmp_path, "rev-parse", "HEAD").stdout.strip()


def change(tmp_path, *paths):
    for rel in paths:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text("changed\n")
    batch_git.git(tmp_path, "add", "-A")
    batch_git.git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@e", "commit", "-q", "-m", "change")
    return batch_git.git(tmp_path, "rev-parse", "HEAD").stdout.strip()


def test_the_items_capability_and_a_touched_feature_are_reached(tmp_path):
    since = repo(tmp_path)
    head = change(tmp_path, "features/review.feature", "src/x.txt")
    left = batch_reach.unreached(batch_git.git, tmp_path, since, head, ["batches#r78"])
    assert "tests/scenarios/test_items.py" in left
    assert not {"tests/scenarios/test_batches.py", "tests/scenarios/test_review.py"} & set(left)


def test_a_touched_module_reaches_its_tests_and_a_helpers(tmp_path):
    since = repo(tmp_path)
    head = change(tmp_path, "scripts/batch_tasks.py")
    left = batch_reach.unreached(batch_git.git, tmp_path, since, head, [])
    assert {"tests/scripts/test_lf.py", "tests/scripts/test_other.py"} <= set(left)
    assert not {"tests/scripts/test_batch_done.py", "tests/scripts/test_helped.py"} & set(left)


def test_a_touched_conftest_reaches_everything(tmp_path):
    since = repo(tmp_path)
    head = change(tmp_path, "tests/scripts/conftest.py")
    assert batch_reach.unreached(batch_git.git, tmp_path, since, head, []) == []


def test_the_plugin_leaves_unreached_tests_out(tmp_path):
    (tmp_path / "test_breaks.py").write_text("def test_breaks():\n    assert False\n")
    (tmp_path / "pytest.ini").write_text("[pytest]\n")
    scripts = str(Path(batch_reach.__file__).parent)
    env = dict(os.environ, PYTHONPATH=scripts, **{batch_reach.ENV: "test_breaks.py"})
    run = [sys.executable, "-m", "pytest", "-q", "-p", "work_items", "-p", "no:cacheprovider", "-n0"]
    done = subprocess.run(run + ["."], cwd=tmp_path, env=env, capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    env.pop(batch_reach.ENV)
    assert subprocess.run(run + ["."], cwd=tmp_path, env=env, capture_output=True, text=True).returncode == 1
