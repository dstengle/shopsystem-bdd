"""Modality in grammar 4 (the CNL 4 design, section 4.5, I17): "may" a permission, "always" and "never" a necessity
of no trigger, each parsed, linearised back word for word and read into its form's modality; "may not" and a line of
"shall" and "may" refused by the reading rules; in `model logic`, a "shall not" that forbids what a "may" permits an L7
and a necessity a premise of every pair (spec_lf_modal, grammar/check.lp)."""
import pathlib
import sys

import pytest
import spec_context
import spec_grammar
import spec_grammar4
import spec_lf
import spec_lf_read
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

FIXTURE = pathlib.Path(__file__).resolve().parents[2] / "tests" / "scripts" / "fixtures" / "codified-2"

LINES = {"A session may write a file.": "may",
         "When a session ends a stage, the session may write a file.": "may",
         "A session always follows a stage.": "always",
         "A session never has a worktree.": "never",
         "While a stage is `done`, a session never follows the stage.": "never"}


@pytest.fixture(scope="module")
def vocab():
    toolchain.require()
    return spec_grammar4.load(FIXTURE)[0]


def test_each_modal_line_round_trips_and_has_its_modality(vocab):
    for line, modality in LINES.items():
        p = spec_grammar4.parse(FIXTURE, line)
        assert p.tree is not None, (line, p.refusal)
        assert spec_grammar4.linearise(FIXTURE, p.tree) == spec_grammar.normalise(line)
        assert spec_lf.form(vocab, p.tree).modality == modality, line
        assert spec_lf_read.refusal(vocab, p.tree) is None, line


def test_a_necessity_is_one_clause_read_as_a_while_clause_is(vocab):
    form = spec_lf.form(vocab, spec_grammar4.parse(FIXTURE, "A session never follows a stage.").tree)
    assert [p.op for p in form.parts] == ["holds"]
    assert {r.origin for r in form.parts[0].refs} == {"while"}


def test_may_not_and_a_line_of_shall_and_may_are_refused(vocab):
    for line, says in (("A session may not write a file.", 'says "may not"'),
                       ("When a session ends a stage, the session may write a file, and `work` shall print the stage.",
                        'says both "may" and "shall"')):
        p = spec_grammar4.parse(FIXTURE, line)
        assert says in spec_lf_read.refusal(vocab, p.tree), line


def test_always_takes_no_trigger():
    p = spec_grammar4.parse(FIXTURE, "When a session ends a stage, a session always follows the stage.")
    assert p.tree is None


def world(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    return tmp_path


def found(tmp_path, *lines):
    return [(f.code, f.text) for f in spec_solve.run(world(tmp_path, *lines), capability="thing")]


def test_a_permission_is_a_may_act_and_a_necessity_a_premise(tmp_path):
    ctx = spec_context.load(world(tmp_path, "A session may write a file.", "A session always has a worktree."))
    assert not ctx.refused, ctx.refused
    assert 'resp("thing#r1",1,may,e_write,x1,x2).' in ctx.facts["thing#r1"]
    assert {'nec("thing#r2",always,r_worktree_of_session,k_worktree,k_session).', 'necsub("thing#r2",2).'} <= set(ctx.facts["thing#r2"])


def test_a_shall_not_that_forbids_what_a_may_permits_is_an_l7(tmp_path):
    assert found(tmp_path, "A session may write a file.",
                 "While a session follows a stage, the session shall not write a file.") == [
        ("L7", "thing#r2 forbids what thing#r1 permits: a session may write a file")]


def test_on_one_trigger_too_and_never_on_another_act(tmp_path):
    when = "When a session ends a stage, the session "
    assert [c for c, _ in found(tmp_path, when + "may write a file.", when + "shall not write a file.")] == ["L7"]
    assert found(tmp_path / "other", "A session may write a file.", "A session shall not end a stage.") == []


def test_a_necessity_puts_out_a_pair_whose_state_it_rules_out(tmp_path):
    pre = "While a session follows a stage, when the person runs `work start`, `work` shall "
    lines = (pre + "print the stage.", pre + "not print the stage.")
    assert [c for c, _ in found(tmp_path / "a", *lines)] == ["L1"]
    assert found(tmp_path / "b", *lines, "A session never follows a stage.") == []
    pre = "While a session has no worktree, when the person runs `work start`, `work` shall "
    lines = (pre + "print the session.", pre + "not print the session.")
    assert [c for c, _ in found(tmp_path / "c", *lines)] == ["L1"]
    assert found(tmp_path / "d", *lines, "A session always has a worktree.") == []


def test_a_necessity_under_while_has_no_translation(tmp_path):
    ctx = spec_context.load(world(tmp_path, "While a stage is `done`, a session never follows the stage."))
    assert "no translation of a necessity" in ctx.refused["thing#r1"]
