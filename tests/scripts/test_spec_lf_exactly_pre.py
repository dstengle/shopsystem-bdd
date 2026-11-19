"""b309: holds-exactly in a precondition, read by `model logic`: "every K that P" with a restrictor of a K2 of its own
(`urex`) or of a value it has not (`unattr`), and the only half's "no" box with an inner `not` of a K2 of its own
(`nbnone`) or of a `not` of values; each half shown to put a pair out, in the smallest codified-2 context."""
import pathlib
import sys

import pytest
import spec_context
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

ON = ", when the person runs `work start` on the worktree, `work` shall %s the worktree."
COVERED = "While a worktree holds exactly the files that cover a line" + ON % "print"
UNVERSIONED = "While a worktree holds exactly the files whose version is not `2.0.0`" + ON % "print"


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def world(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    return tmp_path


def facts(tmp_path, line):
    ctx = spec_context.load(world(tmp_path, line))
    assert not ctx.refused, ctx.refused
    return {f.split("(", 1)[0]: f for s in ctx.statements for f in ctx.facts[s.id]}


def l1(tmp_path, *lines):
    return [f for f in spec_solve.run(world(tmp_path, *lines), "thing") if f.code == "L1"]


def test_every_k_that_vs_a_k2_and_its_only_half_are_read(tmp_path):
    found = facts(tmp_path, COVERED)
    assert found["urex"].endswith(",e_cover,s,k_line)."), found
    assert found["nbnone"].endswith(",e_cover,o1,s,k_line)."), found


def test_every_k_whose_value_is_not_v_is_read(tmp_path):
    found = facts(tmp_path, UNVERSIONED)
    assert found["unattr"].endswith(",t_version,v_2_0_0)."), found
    assert found["nbattr"].endswith(",t_version,v_2_0_0,pos)."), found


def test_a_file_that_covers_a_line_in_the_worktree_clashes(tmp_path):
    other = "While a worktree holds a file that covers a line" + ON % "not print"
    assert l1(tmp_path, COVERED, other)


def test_a_file_that_covers_no_line_in_the_worktree_puts_the_pair_out(tmp_path):
    other = "While a worktree holds a file that covers no line" + ON % "not print"
    assert not l1(tmp_path, COVERED, other)


@pytest.mark.parametrize("value, clash", [("1.0.0", True), ("2.0.0", False)])
def test_a_file_of_the_excluded_value_puts_the_pair_out(tmp_path, value, clash):
    other = "While a worktree holds a file whose version is `%s`" % value + ON % "not print"
    assert bool(l1(tmp_path, UNVERSIONED, other)) == clash
