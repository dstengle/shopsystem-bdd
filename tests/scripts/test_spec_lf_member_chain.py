"""b315: a restriction of a response's object's K that reaches a second thing restricted in its turn, by a row to a
third thing or by a value ("a worktree that holds exactly the files that cover a line whose outcome is `accepted`",
"... that holds no file that covers the line of a stage"), read as spec_lf_member's `such(K,...)` and `all(K,...)`
with the second thing's own restriction, one hop and no further; in the smallest codified-2 context."""
import pathlib
import sys

import pytest
import spec_context
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

RUN = "When the person runs `work start`, `work` shall print a worktree that holds "
VALUED = RUN + "exactly the files that cover a line whose outcome is `accepted`."
NONE = RUN + "no file that covers the line of a stage."
FURTHER = RUN + "exactly the files that cover the line of a stage that a session follows."
LINE = "such(k_line,(t_outcome,v_accepted,pos))"
STAGED = "such(k_line,(%s,s,kind(k_stage),pos))"


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def world(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    return tmp_path


def onrels(tmp_path, *lines):
    ctx = spec_context.load(world(tmp_path, *lines))
    assert not ctx.refused, ctx.refused
    return [f for s in ctx.statements for f in ctx.facts[s.id] if f.startswith("onrel(")]


def test_a_value_of_the_second_thing_is_its_restriction(tmp_path):
    out = onrels(tmp_path, VALUED)
    assert len(out) == 2, out
    assert any(f.endswith(",o,all(k_file,(e_cover,s,%s,pos)))." % LINE) for f in out), out
    assert any(f.endswith(",o,such(k_file,(e_cover,s,%s,neg)))." % LINE) for f in out), out


def test_holds_no_k_that_p_reaches_the_third_thing(tmp_path):
    out = onrels(tmp_path, NONE)
    assert len(out) == 1, out
    row = out[0].split("such(k_line,(", 1)[1].split(",", 1)[0]
    assert out[0].endswith(",o,such(k_file,(e_cover,s,%s,pos)))." % (STAGED % row)), out


def test_lines_over_the_chain_and_over_a_value_are_each_read(tmp_path):
    other = NONE.replace("start", "stop")
    world(tmp_path, NONE, other, NONE.replace("the line of a stage", "a line whose outcome is `accepted`")
          .replace("start", "stop"))
    assert spec_solve.unread(tmp_path, "thing") == []


def test_a_chain_of_more_than_two_hops_has_no_reading(tmp_path):
    world(tmp_path, FURTHER)
    unread = spec_solve.unread(tmp_path, "thing")
    assert len(unread) == 1 and "negated restriction" in str(unread[0]), unread
