"""value-compare and value-same over two senses of one attribute word (b287): the version of a worktree compared with
the version of a file, read by `model logic` over the one value order's cells, and the Givens `features generate`
writes of it, each side a value of its own sense."""
import pathlib
import subprocess
import sys

import pytest
import spec_context
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

FEATURES = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "features"
SENSE = ("- **version** (attribute of worktree): the release a worktree is checked out at. Values (noun): `1.0.0`, "
         "`3.0.0`. Order: by number.\n")
LINE = "While %s, when a session writes the file, `work` shall %s the file."
WORKTREE, FILE = "the version of the `a` worktree", "the version of a file"


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def world(tmp_path, lines, name="thing"):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines), name)
    index = tmp_path / "spec" / "index.md"
    index.write_text(index.read_text() + SENSE)


def codes(tmp_path, *lines):
    world(tmp_path, lines)
    ctx = spec_context.load(tmp_path)
    assert not ctx.refused, ctx.refused
    return [f.code for f in spec_solve.run(tmp_path, capability="thing")]


@pytest.mark.parametrize("second, clash", [
    ("%s is after %s" % (FILE, WORKTREE), False),     # the worktree's after the file's and the file's after it: never
    ("%s is before %s" % (FILE, WORKTREE), True),
    ("%s is the same as %s" % (FILE, WORKTREE), False),
])
def test_two_comparisons_across_two_senses_clash_only_where_values_meet_both(tmp_path, second, clash):
    found = codes(tmp_path, LINE % ("%s is after %s" % (WORKTREE, FILE), "print"), LINE % (second, "not print"))
    assert ("L1" in found) == clash, found


def test_a_comparison_across_two_senses_is_given_a_value_of_each_sense(tmp_path):
    world(tmp_path, [LINE % ("%s is after %s" % (WORKTREE, FILE), "print")], "c1")
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=tmp_path, capture_output=True,
                          text=True)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    text = (tmp_path / "features" / "c1.feature").read_text()
    assert "the version of the `a` worktree is `1.0.0`" in text and "the version of the file f1 is `0.0.0`" in text, text


def test_two_senses_ordered_as_listed_with_different_lists_are_not_compared(tmp_path):
    line = LINE % ("the priority of a stage is after the priority of a file", "print")
    codified2_world.context(tmp_path, "ex.com/prod/ctx", [line], "thing")
    index = tmp_path / "spec" / "index.md"
    index.write_text(index.read_text() + "- **priority** (attribute of file): how soon a file is wanted. Values "
                     "(adjective): `a`, `b`. Order: as listed.\n")
    ctx = spec_context.load(tmp_path)
    assert "the senses of priority have different value orders" in str(ctx.refused), ctx.refused
    cans = [f for f in ctx.domain if f.startswith("tcan(t_priority")]
    assert len(cans) == 2 and len({f.split(",")[1] for f in cans}) == 2, cans
