"""The 10 s ceiling (design-r3 §7): the root conftest reports each test whose setup, call and teardown together take
longer than `$SHOPSYSTEM_TEST_CEILING` seconds (10 by default), and does not fail the run for it."""
import os
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]


def run(tmp_path, ceiling):
    project = tmp_path / "project"
    if not project.exists():
        project.mkdir()
        shutil.copy(REPO / "conftest.py", project / "conftest.py")
        (project / "pytest.ini").write_text("[pytest]\n")
        (project / "test_it.py").write_text("import time\n\n\ndef test_slow():\n    time.sleep(0.3)\n\n\n"
                                             "def test_quick():\n    pass\n")
    env = dict(os.environ, SHOPSYSTEM_TEST_CEILING=ceiling, PYTHONPATH=str(REPO / "scripts"))
    done = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:xdist", "-p", "no:cacheprovider", "-q"],
                          cwd=project, env=env, capture_output=True, text=True, timeout=120)
    return done


def test_a_test_over_the_ceiling_is_reported_and_the_run_passes(tmp_path):
    done = run(tmp_path, "0.1")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "tests over the 0.1 s ceiling:" in done.stdout
    line = next(l for l in done.stdout.splitlines() if "test_slow" in l)
    assert line.endswith("test_it.py::test_slow") and float(line.split()[0]) >= 0.3
    assert "test_quick" not in done.stdout.split("ceiling:", 1)[1]


def test_no_test_over_the_ceiling_prints_nothing(tmp_path):
    done = run(tmp_path, "5")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "tests over the" not in done.stdout
