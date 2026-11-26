"""A frame of a fixed phrase before a kind (b796): on a verb naming an operation, words of no kind after the verb
read before the object (`Frame: <actor> lists the characters of <note>.`, as grammar 4 reads it), the senses of a
verb told apart by their fixed phrases, and a frame that does not read named as its entry writes it."""
import spec_frames
import spec_lexicon

NAMES = {"agent", "note", "checklist", "member"}


def verb(frame, operation="checklists.characters", written=()):
    return spec_lexicon.Term(term="list", category="event", frame=frame, frames=(frame,), operation=operation,
                             written=written)


def test_a_fixed_phrase_before_a_kind_reads_on_a_verb_naming_an_operation():
    assert spec_frames.frame(verb("agent lists the characters of note"), NAMES) == spec_frames.Frame(
        "agent", "note", None, fixed="the characters of")
    assert spec_frames.frame(verb("agent lists the chores of the member"), NAMES).object == "member"


def test_a_fixed_phrase_does_not_read_on_a_verb_naming_no_operation():
    assert spec_frames.frame(verb("agent lists the characters of note", operation=""), NAMES) is None


def test_a_frame_that_does_not_read_is_named_as_written_with_no_unrelated_nearest_names():
    term = verb("agent lists note checklist", written=("<actor> lists <note> <checklist>",))
    said = spec_frames.misread(term, NAMES, shown=True)
    assert said.startswith('the Frame: "<actor> lists <note> <checklist>." does not read at "note checklist"'), said
    assert "nearest" not in said and spec_frames.FIXED in said


def test_senses_of_one_kind_told_apart_by_their_fixed_phrase_do_not_overlap():
    kinds = [spec_lexicon.Term(term=k, category="kind") for k in ("agent", "note")]
    length = verb("agent shows the length of note", operation="checklists.length")
    show = verb("agent shows note", operation="checklists.show")
    shown = [spec_lexicon.Term(**{**t.__dict__, "term": "show"}) for t in (length, show)]
    assert spec_frames.overlapping(spec_lexicon.Lexicon(terms=kinds + shown)) == set()
    again = [spec_lexicon.Term(**{**t.__dict__, "term": "show"}) for t in (show, show)]
    assert spec_frames.overlapping(spec_lexicon.Lexicon(terms=kinds + again)) == {"show"}
