"""The smoke test of the other tools on the converted spec (the GF conversion's design §18, point 22): each runs on the
live repository, exits 0 and prints something. `tools map` measures one small test module, so the map is cheap; it is
written where every map is, under the git-ignored `.shop/scratch/tools/`."""
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
MEASUREMENTS = ROOT / ".shop" / "records" / "measurements"


def run(*argv):
    done = subprocess.run([sys.executable, *map(str, argv)], cwd=ROOT, capture_output=True, text=True, timeout=600)
    assert done.returncode == 0, "%s exited %d:\n%s%s" % (argv, done.returncode, done.stdout, done.stderr)
    assert done.stdout.strip(), "%s printed nothing" % (argv,)
    return done.stdout


def kept_measurement():
    """The first measurement record `measure show` reads (an older record may predate the measurement kind)."""
    for path in sorted(MEASUREMENTS.glob("*.md")):
        done = subprocess.run([sys.executable, str(SCRIPTS / "measure"), "show", str(path)], cwd=ROOT,
                              capture_output=True, text=True)
        if done.returncode == 0:
            return path
    pytest.fail("no kept measurement under %s is read by `measure show`" % MEASUREMENTS)


def test_measure_shows_a_kept_measurement():
    run(SCRIPTS / "measure", "show", kept_measurement().relative_to(ROOT))


def test_the_coverage_tools_map_and_answer():
    run(SCRIPTS / "tools", "map", "--json", "--", "tests/scripts/test_spec_read.py")
    run(SCRIPTS / "tools", "tests-of", "scripts/work")
    run(SCRIPTS / "tools", "untested", "--json", "scripts/spec_read.py")


@pytest.mark.parametrize("argv", [["count", "--by-tag"], ["list", "--tag", "@g1"], ["bindings"]])
def test_features_reads_the_generated_features(argv):
    run(SCRIPTS / "features", *argv)
