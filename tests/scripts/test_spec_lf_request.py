"""spec_lf_request: a request with its parameters in the logical form (the domain contract design, §5.1): the atoms
`request`, `param` and `noparam` and their lines in `model parse --form`, "the request" the trigger's, "the p" a
parameter, and example data after "with the <parameter>"."""
import pathlib
import re

import pytest
import spec_context
import spec_example
import spec_grammar4
import spec_lexicon
import spec_lf
import spec_rgl_steps
import spec_steps4
import toolchain

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def form(line):
    vocab = spec_grammar4.load(FIXTURE)[0]
    parsed = spec_grammar4.parse(FIXTURE, line)
    assert parsed.tree, parsed.refusal
    return spec_lf.show(spec_lf.form(vocab, parsed.tree))


def test_a_request_with_two_parameters_one_absent():
    assert form("When the person adds a note with the text `milk` and without a priority, the notes service shall "
                "keep the note.") == """shall [x1: agent the person (constant), x3: thing `milk` (parameter), \
x4: service the notes service (constant)]
  when [x2: note]
    request(e1, notes.add, subject: x1, object: x2)
    param(e1, text, x3)
    noparam(e1, priority)
  response
    keep(e2, subject: x4, object: x2)"""


def test_a_value_a_flag_some_and_a_thing():
    said = form("When the person adds a note with the priority `high` and the reminder, the notes service shall keep "
                "the note.")
    assert "param(e1, priority, `high`)" in said and "param(e1, reminder, on)" in said
    assert "param(e1, text, some)" in form("When the person adds a note with a text, the notes service shall keep "
                                           "the note.")
    said = form("When the person labels a note with a tag, the notes service shall keep the tag.")
    assert "when [x2: note, x3: tag]" in said and "param(e1, tag, x3)" in said and "keep(e2, subject: x4, object: x3)" in said


def test_a_request_with_no_parameter_said():
    said = form("When the person lists the notes, the notes service shall complete the request.")
    assert "request(e1, notes.list, subject: x1, the notes)" in said


def test_the_request_is_the_triggers_and_the_text_a_parameter():
    said = form("If the person adds a note without a text, then the notes service shall refuse the request and name "
                "the text.")
    assert 'x4: request "the request the trigger makes" (indexical)' in said
    assert "x5: parameter text (constant)" in said
    assert "refuse(e2, subject: x3, object: x4)" in said and "name(e3, subject: x3, object: x5)" in said


def test_an_act_of_a_response_keeps_its_event():
    said = form("When the person files a note, the notes service shall archive the note.")
    assert "request(e1, notes.file, subject: x1, object: x2)" in said and "archive(e2, subject: x3, object: x2)" in said


def test_example_data_after_with_the_parameter():
    known = spec_example.constants(spec_lexicon.read(FIXTURE), FIXTURE)
    line = "When the person adds a note with the text `milk` and the priority `high`, the notes service shall keep it."
    assert spec_example.parameters(line, known) == ["milk"]
    assert spec_example.parameters("When the person runs `notes add` with the `--x` option.", known) == [
        "notes add", "--x"]     # no code names a command or an option in a request context


# --- the twins of grammar/language.md's sections on parameters and on the request's own things --------------------
REQUEST = pathlib.Path(__file__).parent / "fixtures" / "request-4"
SECTIONS = re.compile(r'^### ("with the p v"|"this request").*?(?=^### |^## )', re.MULTILINE | re.DOTALL)
BLOCK = re.compile(r"^```reading\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


def twins():
    text = (pathlib.Path(__file__).resolve().parents[2] / "grammar" / "language.md").read_text()
    return [b.split("\n", 1)[0] for m in SECTIONS.finditer(text) for b in BLOCK.findall(m.group(0))
            if "\nrefused: " not in b]


def test_the_sections_have_their_twins():
    assert len(twins()) >= 10


@pytest.mark.parametrize("line", twins())
def test_each_twin_translates_to_facts_and_to_steps(line):
    found, why = spec_context.Four(REQUEST).facts("thing#r1", line)
    assert why is None and found[1], why
    vocab = spec_rgl_steps.load(REQUEST)[0]
    assert spec_steps4.cases(vocab, [("thing#r1", spec_lf.form(vocab, spec_grammar4.parse(REQUEST, line).tree))])
