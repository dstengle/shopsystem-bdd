"""adapter_provider (b550): a contract's term lines read in the glossary's entry form, a renamed word in every place
the contract names it, and the terms read into an adapter spec's lexicon; the scenarios of checking r106-r109 drive
the clash and the assumed description."""
import adapter_provider
import spec_lexicon

OBJECTS = {"note": {"attributes": ["text (text)", "status: draft | active | retired"],
                    "relations": ["carries → tag (many)"]},
           "tag": {}}


def test_a_verb_s_slots_are_read_as_kinds():
    assert adapter_provider.bullet("add (verb, action): Forms: adds, added. Frame: <actor> adds <note>.", OBJECTS,
                                   {}) == "- **add** (verb, action): Forms: adds, added. Frame: agent adds note."
    assert adapter_provider.bullet("carry (verb, state): Forms: carries, carried. Frame: <from> carries <to>.",
                                   OBJECTS, {}).endswith("Frame: note carries tag.")


def test_an_attribute_takes_its_values_or_its_type_off_its_object():
    assert adapter_provider.bullet("status (attribute of note)", OBJECTS, {}) == (
        "- **status** (attribute of note): Values (adjective): `draft`, `active`, `retired`.")
    assert adapter_provider.bullet("text (attribute of note)", OBJECTS, {}).endswith("Type: text.")


def test_a_renamed_word_is_read_under_its_new_word_everywhere():
    renamed = {"note": "kept note"}
    assert adapter_provider.bullet("note (noun): A short text. Plural: notes.", OBJECTS, renamed) == (
        "- **kept note** (noun): A short text. Plural: kept notes.")
    assert adapter_provider.bullet("status (attribute of note)", OBJECTS, renamed).startswith(
        "- **status** (attribute of kept note)")
    assert adapter_provider.bullet("carry (verb, state): Frame: <from> carries <to>.", OBJECTS, renamed).endswith(
        "Frame: kept note carries tag.")


def test_a_term_with_no_text_is_an_entry():
    found = spec_lexicon.entry(adapter_provider.bullet("the notes service (proper noun)", OBJECTS, {}), "c")
    assert found is not None and found.term == "the notes service" and found.category == "actor"


def test_a_line_that_is_no_term_is_none():
    assert adapter_provider.bullet("no part of speech", OBJECTS, {}) is None
