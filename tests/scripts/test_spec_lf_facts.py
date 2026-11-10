"""spec_lf_facts (the CNL 4 design, section 7.4, I12a): a codified-2 requirement's logical form as check.lp's facts,
and `model logic` over them, in the smallest codified-2 context with a capability of the lines each test gives."""
import pathlib
import sys

import pytest
import spec_context
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

RUN = "When the person runs `work start`, "


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


def codes(tmp_path, *lines):
    return [f.code for f in spec_solve.run(world(tmp_path, *lines), capability="thing")]


def test_a_run_is_its_command_and_a_response_its_act(tmp_path):
    out = facts(tmp_path, RUN + "`work` shall exit with an error naming a stage.")
    assert 'form("thing#r1",when).' in out
    assert 'trig("thing#r1",ran,"`work start`",a_the_person,none).' in out
    assert 'resp("thing#r1",1,pos,exit_error,a_work,x4).' in out


def test_an_option_is_part_of_the_command_run(tmp_path):
    out = facts(tmp_path, "When the person runs `work backlog` with the `--json` option, `work` shall exit "
                          "successfully.")
    assert 'trig("thing#r1",ran,"`work backlog` `--json`",a_the_person,none).' in out
    assert 'resp("thing#r1",1,pos,exit_ok,a_work,none).' in out


def test_the_pre_state_and_the_object_restrictions(tmp_path):
    out = facts(tmp_path, "While a stage is `open`, when the person runs `work start` on the stage, `work` shall not "
                          "print a stage whose status is `done`.")
    assert 'form("thing#r1",while_when).' in out
    assert 'cond("thing#r1",x1,t_status,v_open,pos).' in out
    assert 'trig("thing#r1",ran,"`work start`",a_the_person,x1).' in out
    assert 'oattr("thing#r1",x5,t_status,v_done).' in out
    assert 'resp("thing#r1",1,neg,print,a_work,x5).' in out


def test_change_nothing_is_the_checks_change_nothing(tmp_path):
    out = facts(tmp_path, RUN + "`work` shall change nothing.")
    assert 'resp("thing#r1",1,pos,change_nothing,a_work,none).' in out


def test_every_keeps_its_object_and_only_obliges_nothing(tmp_path):
    out = facts(tmp_path, RUN + "`work` shall print every stage.", "A session shall change only files in its worktree.")
    assert 'each("thing#r1",x4).' in out
    assert 'only("thing#r2",1,e_change,x1,x2).' in out
    assert 'rrel("thing#r2",r_file_in_worktree,x2,x3).' in out
    assert not [f for f in out if f.startswith('resp("thing#r2"')]


def test_every_clashes_with_a_forbidden_thing_of_its_kind(tmp_path):
    assert codes(tmp_path, RUN + "`work` shall print every stage.",
                 RUN + "`work` shall not print a stage whose status is `done`.") == ["L1"]


def test_a_stage_obliged_clashes_only_with_one_of_its_own_kind(tmp_path):
    assert codes(tmp_path, RUN + "`work` shall print a stage whose status is `open`.",
                 RUN + "`work` shall not print a stage whose status is `done`.") == []


def test_only_clashes_with_a_change_known_to_fall_outside_it(tmp_path):
    only = "A session shall end only stages whose status is `open`."
    line = "While a stage is `%s`, when the person runs `work start` on the stage, a session shall end the stage."
    assert codes(tmp_path / "out", only, line % "done") == ["L1"]
    assert codes(tmp_path / "in", only, line % "open") == []
    assert codes(tmp_path / "any", "A session shall change only files in its worktree.",
                 "When a session ends a stage, the session shall change a file.") == []


def test_an_actor_is_a_doer_of_its_kind(tmp_path):
    assert codes(tmp_path, RUN + "`work` shall print a stage.", RUN + "a tool shall not print a stage.") == ["L1"]
    assert 'akind(a_work,k_tool).' in spec_context.load(tmp_path).domain


def test_a_line_with_no_translation_is_refused_naming_it(tmp_path):
    ctx = spec_context.load(world(tmp_path, RUN + "`work` shall print a stage or a file."))
    assert "no translation" in ctx.refused["thing#r1"]


def test_a_state_verb_restricts_an_object_by_its_subject(tmp_path):
    out = facts(tmp_path, "When a session ends a stage, `work` shall print every session that follows the stage.")
    assert 'orel("thing#r1",e_follow,x4,x2).' in out and 'each("thing#r1",x4).' in out


def test_a_negated_row_or_state_of_an_object_is_onrel(tmp_path):
    """b240 phase 12: "a stage that no session follows", "a stage that the person does not follow" (on an `every`
    object or not) are `onrel`, which, as `onattr`, clashes only with the same negated restriction."""
    pos, neg = RUN + "`work` shall print a stage %s.", RUN + "`work` shall not print a stage%s."
    assert 'onrel("thing#r1",x4,e_follow,o,kind(k_session)).' in facts(tmp_path, pos % "that no session follows")
    assert 'onrel("thing#r1",x4,e_follow,o,a_the_person).' in facts(tmp_path, pos % "that the person does not follow")
    assert codes(tmp_path, pos % "that no session follows", neg % " that no session follows") == ["L1"]
    assert codes(tmp_path, pos % "that no session follows", neg % " whose status is `done`") == []
    assert codes(tmp_path, RUN + "`work` shall print a stage.", neg % " that no session follows") == []
    ctx = spec_context.load(world(tmp_path, RUN + "`work` shall print every session that does not follow a stage.",
                                  "When a session ends a stage, `work` shall print every session that does not "
                                  "follow the stage."))
    assert not ctx.refused, ctx.refused


def test_a_no_box_with_a_not_inside_it_is_read_whole(tmp_path):
    """b238: "a stage has no line whose outcome is not `accepted`" is `nobox`, `nbrel` and `nbattr` (`neg`): it
    clashes with a line on a stage whose line is `accepted`, not with one on a stage whose line is `refused`; through
    two rows ("no worktree that holds a file whose version is not ..."), likewise."""
    line = ("While a stage has no line whose outcome is not `accepted`, when the person runs `work start`, `work` shall "
            "end the stage.")
    other = ("While a stage has a line whose outcome is `%s`, when the person runs `work start`, `work` shall not end "
             "the stage.")
    assert {'nobox("thing#r1",n1,k_line,none).', 'nbattr("thing#r1",n1,o1,t_outcome,v_accepted,neg).',
            'nbrel("thing#r1",n1,r_line_of_stage,o1,x1).'} <= set(facts(tmp_path, line))
    assert codes(tmp_path, line, other % "accepted") == ["L1"]
    assert codes(tmp_path, line, other % "refused") == []
    two = ("While a session has no worktree that holds a file whose version is not `2.0.0`, when the person runs "
           "`work start`, `work` shall print the session.")
    other = ("While a session has a worktree that holds a file whose version is `%s`, when the person runs `work "
             "start`, `work` shall not print the session.")
    assert codes(tmp_path, two, other % "2.0.0") == ["L1"]
    assert codes(tmp_path, two, other % "1.0.0") == []


def test_a_state_that_takes_no_object_is_a_one_place_fluent(tmp_path):
    """b219: "a stage stalls" (Frame: stage stalls.) is `crel(R,E,X,none,Pol)`; it and its negation exclude each
    other on one stage, as a state with an object does."""
    world(tmp_path, *[RUN.replace("When", "While a stage %s, when" % s) + "`work` shall %s the stage." % p
                      for s, p in (("stalls", "print"), ("does not stall", "not print"), ("stalls", "not print"))])
    index = tmp_path / "spec" / "index.md"
    index.write_text(index.read_text() + codified2_world.INTRANSITIVE[0])
    ctx = spec_context.load(tmp_path)
    assert not ctx.refused, ctx.refused
    assert 'crel("thing#r1",e_stall,x1,none,pos).' in ctx.facts["thing#r1"]
    assert 'crel("thing#r2",e_stall,x1,none,neg).' in ctx.facts["thing#r2"]
    found = spec_solve.run(tmp_path, capability="thing")
    assert [(f.code, f.ids) for f in found] == [("L1", ["thing#r1", "thing#r3"])], found


def test_every_in_a_condition_is_a_universal(tmp_path):
    """b197: "every K that P is v" in a While clause is codified-1's universal (`uall`, `uattr`, `ucond`): a pair is
    out where a K that meets it has another value, and clashes where every K is v."""
    line = "While every stage is `done`, when the person runs `work start`, `work` shall exit successfully."
    error = RUN.replace("When", "While a stage is `%s`, when") + "`work` shall exit with an error naming `work start`."
    out = facts(tmp_path, line, error % "done")
    assert {'uall("thing#r1",x1,k_stage).', 'ucond("thing#r1",x1,t_status,v_done,pos).'} <= set(out)
    assert codes(tmp_path, line, error % "done") == ["L1"]
    assert codes(tmp_path, line, error % "open") == []


def test_a_count_in_a_condition_is_a_k_when_it_admits_one(tmp_path):
    """b197: "at least two Ks that are v" in a While clause is a K that is v, its count kept (`ccount`); "at most one"
    says nothing the check reads."""
    line = "While %s `done`, when the person runs `work start`, `work` shall exit successfully."
    out = facts(tmp_path, line % "at least two stages are", line % "at most one stage is")
    assert {'role("thing#r1",x1,k_stage).', 'ccount("thing#r1",x1,least,2).'} <= set(out)
    assert not [f for f in out if f.startswith(("role(\"thing#r2\"", "cond(\"thing#r2\""))], out
    error = "While no stage is `done`, when the person runs `work start`, `work` shall exit with an error naming `work start`."
    assert codes(tmp_path, line % "at least two stages are", error) == []


def test_a_negated_attribute_of_an_object_is_onattr(tmp_path):
    """b197: "a stage whose status is not `done`" is `onattr`, which clashes only with the same negated restriction."""
    pos, neg = RUN + "`work` shall print a stage whose status is %s.", RUN + "`work` shall not print a stage%s."
    assert 'onattr("thing#r1",x4,t_status,v_done).' in facts(tmp_path, pos % "not `done`")
    assert codes(tmp_path, pos % "not `done`", neg % " whose status is not `done`") == ["L1"]
    assert codes(tmp_path, pos % "not `done`", neg % " whose status is `done`") == []
    assert codes(tmp_path, RUN + "`work` shall print a stage.", neg % " whose status is not `done`") == []
