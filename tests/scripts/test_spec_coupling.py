"""spec_coupling's words (checking r144): a word two areas' layers define couples them, whichever two of the areas
that define it."""
import spec_coupling
import spec_vocabulary


def _entry(term, layer):
    return spec_vocabulary.Entry(term, "noun", "", "", "spec/vocabulary/%s.md" % layer, layer)


def test_a_word_three_areas_define_couples_every_two_of_them(monkeypatch):
    layers = ["a", "b", "c", spec_vocabulary.SHARED]
    monkeypatch.setattr(spec_vocabulary, "entries", lambda root: [_entry("note", x) for x in layers])
    found = {}
    spec_coupling._words("root", found)
    assert {k: v["words"] for k, v in found.items()} == {
        ("b", "a"): {"note"}, ("c", "a"): {"note"}, ("c", "b"): {"note"}}


def test_a_word_one_area_defines_twice_couples_nothing(monkeypatch):
    monkeypatch.setattr(spec_vocabulary, "entries", lambda root: [_entry("note", "a"), _entry("note", "a")])
    found = {}
    spec_coupling._words("root", found)
    assert found == {}
