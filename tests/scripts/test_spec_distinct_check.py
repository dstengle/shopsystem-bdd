"""Identity and distinctness (b240, construct #2), the check and the steps: `distinct(R,X,Y)` in the check's facts,
two referents of one line never one thing of a pair; a trigger of one act on each of "two Ks" a trigger of each act,
two lines firing on one act when each act of either is one of the other's, so that two lines on one act whose states
differ only in which things are one never clash (the twin of design-model-check r276-r278); `features generate`
names two distinct things with two names and gives a When of each act."""
import pathlib
import subprocess
import sys

import clingo
import pytest
import spec_context
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
CHECK = REPO / "grammar" / "check.lp"
FEATURES = REPO / "scripts" / "features"
GIVE = "When a session gives a file to %s, `work` shall %s the file."
WRITE = "When a session writes %s, `work` shall %s the worktree."


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def codes(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    ctx = spec_context.load(tmp_path)
    assert not ctx.refused, ctx.refused
    return [f.code for f in spec_solve.run(tmp_path, capability="thing")]


@pytest.mark.parametrize("first, second, clash", [
    ((GIVE % ("another session", "print")), (GIVE % ("the same session", "not print")), False),
    ((GIVE % ("a different session", "print")), (GIVE % ("the same session", "not print")), False),
    ((GIVE % ("another session", "print")), (GIVE % ("a session", "not print")), True),
    ((GIVE % ("another session", "print")), (GIVE % ("a different session", "not print")), True),
])
def test_another_k_is_never_the_k_before_it(tmp_path, first, second, clash):
    assert ("L1" in codes(tmp_path, first, second)) == clash


@pytest.mark.parametrize("first, second, clash", [
    # the twin of r276-r278: two lines on one act in two states, the two files in one worktree or in two
    ("a file in a worktree and another file in the same worktree", ("a file in a worktree and another file in a "
                                                                   "different worktree"), False),
    ("two files in a worktree", "a file in a worktree and another file in a different worktree", False),
    ("two files in a worktree", "a file in a worktree and another file in the same worktree", True),
    ("two files in a worktree", "two files in a worktree", True),
    # one file written is not the act of two written
    ("two files in a worktree", "a file in a worktree", False),
])
def test_two_lines_on_one_act_clash_only_where_their_states_meet(tmp_path, first, second, clash):
    assert ("L1" in codes(tmp_path, WRITE % (first, "print"), WRITE % (second, "not print"))) == clash


def test_two_ks_in_a_response_are_each_an_act(tmp_path):
    assert "L1" in codes(tmp_path, "When a session ends a stage, `work` shall write two files.",
                         "When a session ends a stage, `work` shall not write a file.")


# one line whose two distinct sessions name one code: under every unification they are one thing, so it never fires
LINE = ('form("{r}",when). cnl4("{r}"). role("{r}",x1,k_session). role("{r}",x2,k_file). role("{r}",x3,k_session). '
        'trig("{r}",does,e_give,x1,pair(x2,x3)). resp("{r}",1,{pol},print,a_work,x2). ')
DOM = "kind(k_session). kind(k_file). actor(a_work). "
CODED = 'named("{r}",x1,"`s`"). named("{r}",x3,"`s`"). '


def clashes(facts):
    ctl = clingo.Control(["--enum-mode=brave", "--warn=none"])
    ctl.load(str(CHECK))
    ctl.add("base", [], facts)
    ctl.ground([("base", [])])
    last = []
    ctl.solve(on_model=lambda m: last.__setitem__(slice(None), [str(s) for s in m.symbols(shown=True)]))
    return [a for a in last if a.startswith("clash(")]


def test_two_distinct_referents_are_never_one_thing_of_a_pair():
    a = LINE.format(r="a", pol="pos") + CODED.format(r="a")
    b = LINE.format(r="b", pol="neg") + CODED.format(r="b")
    assert clashes(DOM + a + b)
    assert not clashes(DOM + a + 'distinct("a",x3,x1). ' + b)


def generated(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines), "c1")
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=tmp_path, capture_output=True,
                          text=True)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    text = (tmp_path / "features" / "c1.feature").read_text()
    return [line.strip() for line in text.splitlines() if line.strip().startswith(("Given", "And", "When", "Then"))]


def test_the_steps_name_two_distinct_things_with_two_names(tmp_path):
    assert generated(tmp_path, GIVE % ("another session", "print")) == [
        "Given a session s1", "And a file f1", "And a session s2",
        "When the session s1 gives the file f1 to the session s2", "Then `work` prints the file f1"]


def test_the_steps_give_a_when_of_each_act_of_two_ks(tmp_path):
    steps = generated(tmp_path, WRITE % ("two files in a worktree", "print"))
    assert steps[-3:] == ["When the session s1 writes the file f1", "And the session s1 writes the file f2",
                          "Then `work` prints the worktree w1"]
    assert "And the worktree w1 holds the file f2" in steps
