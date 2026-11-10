"""A prepositional verb (b106, design call 1): in `Frame: agent subscribes to stage.` the preposition is the verb's,
read before its object in every fun of the verb, and a `Frame:` that does not read names the word it stopped at.
Parsed in a copy of the typed glossary fixture with the verb added."""
import pathlib
import shutil
import sys

import pytest
import spec_frames
import spec_grammar
import spec_lexicon

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

FIXTURE = pathlib.Path(__file__).resolve().parent / "fixtures" / "glossary"
VERB = "- **subscribe** (verb, action): Frame: agent subscribes to stage.\n"


@pytest.fixture(scope="module")
def root(tmp_path_factory):
    toolchain.require()
    copy = tmp_path_factory.mktemp("prepositional")
    shutil.copytree(FIXTURE, copy, dirs_exist_ok=True)
    index = copy / "spec" / "index.md"
    index.write_text(index.read_text().rstrip("\n") + "\n" + VERB)
    return copy


def entry(frame):
    return spec_lexicon.entry("- **subscribe** (verb): Frame: %s." % frame, "spec/index.md")


def test_the_preposition_after_the_verb_is_the_verbs():
    names = {"agent", "stage", "text"}
    assert spec_frames.read(entry("agent subscribes to stage"), names) == (
        spec_frames.Frame("agent", "stage", None, "to"), None)
    assert spec_frames.frame(entry("agent subscribes for stage to text"), names) == (
        spec_frames.Frame("agent", "stage", "text", "for"))
    assert spec_frames.frame(entry("agent subscribes stage in text"), names) == (
        spec_frames.Frame("agent", "stage", "text", None, "in"))


def test_a_frame_that_does_not_read_names_the_word():
    names = {"agent", "stage"}
    assert spec_frames.read(entry("agent subscribes to widget"), names) == (None, ("widget", "object"))
    assert spec_frames.read(entry("robot subscribes to stage"), names) == (None, ("robot", "subject"))
    assert spec_frames.read(entry("agent follows stage"), names)[1][1].startswith("verb subscribes")
    assert spec_frames.read(spec_lexicon.entry("- **subscribe** (verb): a thing.", "spec/index.md"), names) == (
        None, None)


def test_every_fun_says_the_preposition_before_the_object(root):
    line = ("While a session does not subscribe to a stage, when a session subscribes to the stage, `work` shall "
            "subscribe to the stage.")
    tree = spec_grammar.parse(root, line).tree
    assert tree and spec_grammar.linearise(root, tree) == line


def test_a_line_without_the_preposition_is_refused_naming_it(root):
    parsed = spec_grammar.parse(root, "When the person runs `work start`, `work` shall subscribe a stage.")
    assert parsed.tree is None
    assert parsed.refusal == "refused: the verb subscribe takes its object after to: agent subscribes to stage"


def test_a_misframed_verb_is_v_t13_naming_the_word_and_the_nearest_kinds(root):
    lex = spec_lexicon.read(root)
    found = [p for p in spec_lexicon.problems(lex) if p[1] == "subscribe"]
    assert found == []
    names = spec_frames.names(lex)
    assert spec_frames.misread(entry("agent subscribes to stages"), names) == (
        'the Frame: does not read at "stages": the verb\'s object is a kind or an actor of the glossary '
        '(nearest: stage, step)')
