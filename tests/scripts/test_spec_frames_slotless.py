"""A frame that takes no noun phrase (b811): in a context with a domain model a thin `Frame:` names its slots in angle
brackets; one with no slot, or none naming a kind, an actor or a parameter of its operation, is a v_t13 naming the
frame as written, never read as a frame of `thing`."""
import shutil
from pathlib import Path

import pytest
import spec_frames
import spec_lexicon

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "docs-checklists"
VOCABULARY = Path("spec") / "vocabulary" / "checklists.md"
READS = "Frame: <actor> lists <checklist>."


def lexicon(tmp_path, frame):
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, tmp_path / part)
    path = tmp_path / VOCABULARY
    path.write_text(path.read_text().replace(READS, "Frame: %s." % frame, 1))
    return spec_lexicon.read(tmp_path)


def contents(lex):
    return next(t for t in lex.of("event") if t.operation == "checklists.contents")


@pytest.mark.parametrize("frame", ["the person lists a checklist", "<member> lists the books"])
def test_a_frame_that_takes_no_noun_phrase_is_misread_naming_it(tmp_path, frame):
    term = contents(lexicon(tmp_path, frame))
    assert term.slotless == (frame,)
    said = spec_frames.misread(term, spec_frames.names(spec_lexicon.Lexicon([term])), shown=True)
    assert said == 'the Frame: "%s." takes no noun phrase: %s' % (frame, spec_frames.SLOTS)


@pytest.mark.parametrize("frame", ["<actor> lists <checklist>", "<actor> lists the checklists",
                                   "the person lists <checklist>"])
def test_a_frame_with_a_slot_of_a_kind_or_an_actor_takes_a_noun_phrase(tmp_path, frame):
    term = contents(lexicon(tmp_path, frame))
    assert term.slotless == ()
    assert "takes no noun phrase" not in (spec_frames.misread(term, {"agent", "checklist"}) or "")
