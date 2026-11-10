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
    ctx = spec_context.load(world(tmp_path, "When a session ends a stage, `work` shall not print every session that "
                                            "follows the stage."))
    assert "no translation" in ctx.refused["thing#r1"]


def test_a_state_verb_restricts_an_object_by_its_subject(tmp_path):
    out = facts(tmp_path, "When a session ends a stage, `work` shall print every session that follows the stage.")
    assert 'orel("thing#r1",e_follow,x4,x2).' in out and 'each("thing#r1",x4).' in out


def test_a_blank_cardinality_is_any_number_and_one_is_functional(tmp_path):
    """Call 14 (b115): in a codified-2 context `file | in | worktree` (blank) relates a file to any number of
    worktrees, though its word is a preposition; `worktree | of | session | one` is functional."""
    domain = spec_context.load(world(tmp_path, RUN + "`work` shall exit successfully.")).domain
    assert "fun(r_worktree_of_session)." in domain
    assert "fun(r_file_in_worktree)." not in domain


def test_a_negated_restriction_of_an_object_keeps_its_negation(tmp_path):
    """A `not` box over an object's restrictions (I12b's negated scopes): "a stage whose status is not `done`" is no
    `done` stage, and "a session that does not follow a stage" follows no stage, whatever the line's polarity."""
    out = facts(tmp_path, RUN + "`work` shall print a stage whose status is not `done`.",
                RUN + "`work` shall not print a session that does not follow a stage.")
    assert 'nattr("thing#r1",x4,t_status,v_done).' in out
    assert not [f for f in out if f.startswith('oattr("thing#r1"')]
    assert 'nrel("thing#r2",e_follow,x4,kind(k_stage)).' in out
    assert not [f for f in out if f.startswith('orel("thing#r2"')]


def test_a_negated_scope_narrows_what_a_line_obliges(tmp_path):
    every = "When a session ends a stage, `work` shall print every session that does not follow the stage."
    end = "When a session ends a stage, `work` shall not print a session%s."
    assert codes(tmp_path / "out", every, end % " that follows the stage") == []
    assert codes(tmp_path / "in", every, end % "") == ["L1"]
    done = RUN + "`work` shall print every stage whose status is not `done`."
    assert codes(tmp_path / "done", done, RUN + "`work` shall not print a stage whose status is `done`.") == []
    assert codes(tmp_path / "open", done, RUN + "`work` shall not print a stage whose status is `open`.") == ["L1"]
