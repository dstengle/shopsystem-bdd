"""b272: "only" and a count over a row of a response's object ("print a worktree that holds only files whose version
is `2.0.0`", "... that holds at most three files") as check.lp's facts, kept and read by no rule (decision 0093), and
their Thens in the generated feature, said of the object; in the smallest codified-2 context."""
import pathlib
import sys

import pytest
import spec_context
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

RUN = "When the person runs `work start`, `work` shall "
ONLY = RUN + "print a worktree that holds only files whose version is `2.0.0`."
AT_MOST = RUN + "print a worktree that holds at most three files."


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def world(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    return tmp_path


def facts(tmp_path, *lines):
    ctx = spec_context.load(world(tmp_path, *lines))
    assert not ctx.refused, ctx.refused
    return [f for s in ctx.statements for f in ctx.facts[s.id]]


def test_only_over_a_row_is_a_restriction_of_the_object(tmp_path):
    out = facts(tmp_path, ONLY)
    assert 'resp("thing#r1",1,pos,print,a_work,x4).' in out
    assert any(f.startswith('oonly("thing#r1",x4,') and f.endswith(",o,x5).") for f in out), out
    assert 'yattr("thing#r1",x5,t_version,v_2_0_0).' in out
    assert not any(f.startswith(("only(", "orel(")) for f in out), out


def test_a_count_over_a_row_is_a_restriction_of_the_object(tmp_path):
    out = facts(tmp_path, AT_MOST)
    assert any(f.startswith('ocount("thing#r1",x4,') and f.endswith(",o,x5,most,3).") for f in out), out
    assert [f for f in out if f.startswith("resp(")] == ['resp("thing#r1",1,pos,print,a_work,x4).']
    assert not any(f.startswith("count(") for f in out), out


def test_they_clash_with_nothing_and_entail_nothing(tmp_path):
    found = spec_solve.run(world(tmp_path, ONLY, AT_MOST, RUN + "print a worktree."), capability="thing")
    assert [f.code for f in found] == [], found
    assert spec_solve.unread(tmp_path, "thing") == []


def test_their_thens_say_the_property_of_the_object(tmp_path):
    import features_generate
    world(tmp_path, ONLY, AT_MOST, RUN.replace("start", "stop") + "print a worktree that holds exactly three files.")
    text = features_generate.generate(str(tmp_path), str(tmp_path / "spec" / "capabilities" / "thing.md"))
    assert "    Then the worktree w1 holds only files whose version is `2.0.0`\n" in text
    assert "    Then the worktree w1 holds at most three files\n" in text
    assert "    Then the worktree w1 holds exactly three files\n" in text
