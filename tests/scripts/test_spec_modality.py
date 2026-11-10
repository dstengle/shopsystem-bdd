"""Modality in grammar 4 (the CNL 4 design, section 4.5, I17): "may" a permission, "always" and "never" a necessity
of no trigger, each parsed, linearised back word for word and read into its form's modality; "may not" and a line of
"shall" and "may" refused by the reading rules."""
import pathlib
import sys

import pytest
import spec_grammar
import spec_grammar4
import spec_lf
import spec_lf_read

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
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
