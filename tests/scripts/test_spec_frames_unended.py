"""A frame is the last thing of its entry, and each slot it names refers to a kind, an actor or a parameter (b840): text
after a `Frame:` that starts no field is read into it, a v_t13 naming the frame; a slot of a frame in a context with a
domain model that names no kind, actor, parameter, imported pack's kind or object is a v_t13 naming the slot."""
import shutil
from pathlib import Path

import pytest
import spec_frames
import spec_lexicon

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "domain-model"
VOCABULARY = Path("spec") / "vocabulary" / "notes.md"
READS = "Frame: <actor> adds <note>."


@pytest.mark.parametrize("frames, unended", [
    (("<actor> adds <note>",), ()),
    (("<actor> adds <note>. Then it is kept",), (("<actor> adds <note>", "Then it is kept"),)),
    (("`a. b` returns video to caller",), ()),
    (("<actor> adds <note>", "<actor> adds <note> to <tag>. It is quick"),
     (("<actor> adds <note> to <tag>", "It is quick"),)),
])
def test_a_frame_that_text_follows_does_not_end_its_entry(frames, unended):
    assert spec_lexicon.unended(frames) == unended


def test_a_frame_before_another_field_or_frame_ends_its_entry():
    term = spec_lexicon.entry("- **add** (verb, action): to add. Frame: agent adds note. Frame: agent adds tag. "
                              "Redefines: cli.", "x")
    assert term.frames == ("agent adds note", "agent adds tag") and term.unended == ()


def lexicon(tmp_path, frame):
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")
    path = tmp_path / VOCABULARY
    path.write_text(path.read_text().replace(READS, "Frame: %s." % frame, 1))
    return spec_lexicon.read(tmp_path)


def add(lex):
    return next(t for t in lex.of("event") if t.operation == "notes.add")


def test_a_frame_with_text_after_it_is_misread_naming_the_frame(tmp_path):
    term = add(lexicon(tmp_path, "<actor> adds <note>. Then it is kept by the tester"))
    said = spec_frames.misread(term, spec_frames.names(spec_lexicon.Lexicon([term])), shown=True)
    assert said.startswith('the Frame: "<actor> adds <note>." does not end its entry, "Then it is kept by the '
                           'tester." follows it')


def test_a_slot_that_refers_to_nothing_is_misread_naming_the_slot(tmp_path):
    term = add(lexicon(tmp_path, "<actor> adds <gadget>"))
    assert term.unslotted == (("<actor> adds <gadget>", "gadget"),)
    said = spec_frames.misread(term, spec_frames.names(spec_lexicon.Lexicon([term])), shown=True)
    assert "names the slot <gadget>, which refers to no kind, no actor and no parameter" in said


@pytest.mark.parametrize("frame", ["<actor> adds <note>", "<agent> adds <note>", "<thing> adds <note>"])
def test_a_slot_of_a_kind_an_actor_or_thing_refers_to_one(tmp_path, frame):
    assert add(lexicon(tmp_path, frame)).unslotted == ()
