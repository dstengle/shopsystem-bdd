"""spec_steps4_request: a request with its parameters as Gherkin steps (the domain contract design, §5.1), and the
step grammar 4 reading them back (features_vocab4's `WhenRequests` with the operation and its parameters, the request
pack's Thens); `features generate` on the domain-model fixture writes a feature whose steps all read."""
import pathlib
import shutil
import subprocess
import sys

import features_vocab4
import pytest
import spec_grammar4
import spec_lf
import spec_rgl_steps
import spec_steps4
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "domain-model"


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def steps(line):
    vocab, gram = spec_rgl_steps.load(FIXTURE)
    parsed = spec_grammar4.parse(FIXTURE, line)
    assert parsed.tree, parsed.refusal
    form = spec_lf.form(vocab, parsed.tree)
    return [(k, spec_rgl_steps.text(gram, t)) for k, t in spec_steps4.read(vocab, [("notebook#r1", form)])]


def test_the_when_of_a_request_with_a_code_a_value_and_an_absent_parameter():
    assert steps("When the person adds a note with the text `milk` and without a priority, the notes service shall "
                 "keep the note.") == [
        ("given", "a note n1"),
        ("when", "the person adds the note n1 with the text `milk` and without a priority"),
        ("then", "the notes service keeps the note n1")]


def test_a_thing_a_parameter_names_is_brought_in_and_the_parameter_named():
    assert steps("When the person labels a note with a tag, the notes service shall keep the tag.") == [
        ("given", "a note n1"), ("given", "a tag t1"),
        ("when", "the person labels the note n1 with the tag t1"), ("then", "the notes service keeps the tag t1")]
    assert steps("If the person adds a note without a text and the reminder, then the notes service shall refuse the "
                 "request and name the text.")[-3:] == [
        ("when", "the person adds the note n1 without a text and the reminder"),
        ("then", "the notes service refuses this request"), ("then", "the notes service names the text")]



def test_a_given_text_value_is_said_as_its_code_and_reads_back():
    """A value of an attribute no entry lists (a text's) is the code itself, never a placeholder (b413)."""
    notes = REPO / "docs" / "examples" / "notes-cli"
    vocab, gram = spec_rgl_steps.load(notes)
    parsed = spec_grammar4.parse(notes, "While the title of a note is `milk`, when the person removes the note, the "
                                        "notes service shall set the status of the note to `removed`.")
    assert parsed.tree, parsed.refusal
    form = spec_lf.form(vocab, parsed.tree)
    said = [(k, spec_rgl_steps.text(gram, t)) for k, t in spec_steps4.read(vocab, [("notes#r1", form)])]
    assert ("given", "the title of the note n1 is `milk`") in said
    assert features_vocab4.step(notes, "given", "the title of the note n1 is `milk`").template == "GivenK_A"

@pytest.mark.parametrize("keyword, text, template, attrs", [
    ("when", "the person adds the note n1 with the text `milk` and the priority `high`", "WhenRequests",
     {"operation": "notes.add", "params": [("text", "`milk`"), ("priority", "`high`")], "without": []}),
    ("when", "the person adds the note n1 with the reminder and without a text", "WhenRequests",
     {"params": [("reminder", True), ("text", None)], "without": ["text"]}),
    ("when", "the person labels the note n1 with the tag t1", "WhenRequests",
     {"operation": "notes.label", "params": [("tag", "the tag t1")]}),
    ("when", "the person lists the notes", "WhenRequests", {"operation": "notes.list", "params": []}),
    ("then", "the notes service refuses this request", "ThenRefuses", {"term": "the notes service"}),
    ("then", "the notes service keeps the note n1", "ThenKeeps", {}),
    ("then", "the notes service completes this request", "ThenCompletes", {}),
    ("then", "the notes service names the text", "ThenDoes", {"term": "name"}),
])
def test_the_step_grammar_reads_a_request_back(keyword, text, template, attrs):
    call = features_vocab4.step(FIXTURE, keyword, text)
    assert call.template == template
    for name, value in attrs.items():
        assert getattr(call, name) == value, name


def test_features_generate_writes_the_fixtures_feature_and_its_steps_read(tmp_path):
    shutil.copytree(FIXTURE, tmp_path, dirs_exist_ok=True)
    scripts = REPO / "scripts"
    run = subprocess.run([sys.executable, str(scripts / "features"), "generate", "--check"], cwd=tmp_path,
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    feature = (tmp_path / "features" / "notebook.feature").read_text()
    assert "When the person adds the note n1 with a text and the priority `high`" in feature
    kw = None
    for line in feature.splitlines():
        keyword, _, text = line.strip().partition(" ")
        if keyword in ("Given", "When", "Then", "And"):
            kw = {"Given": "given", "When": "when", "Then": "then"}.get(keyword, kw)
            assert features_vocab4.step(tmp_path, kw, text).template
