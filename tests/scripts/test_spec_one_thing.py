"""spec_one_thing (b420, design-decision 0111): a request's object is one thing; the frames two readings differ by."""
from types import SimpleNamespace

import spec_meaning
import spec_one_thing


def np(det, kind="k_note"):
    return spec_meaning.read("%s_One (%s_Simple (%s_Det %s (%s_UseN %s_n)))" % ((kind,) * 3 + (det,) + (kind,) * 2))


def verb(term, operation, frames, texts):
    return SimpleNamespace(term=SimpleNamespace(term=term, operation=operation, frames=texts), frames=frames,
                           texts=texts)


VOCAB = SimpleNamespace(verbs=[
    verb("remove", "notes.remove", [("agent", (((), "note"),))], ("agent removes note",)),
    verb("follow", "", [("agent", (((), "note"),))], ("agent follows note",)),
    verb("list", "notes.show", [("agent", (((), "checklist"),))], ("agent lists checklist",)),
    verb("list", "notes.browse", [("agent", ((("the", "checklists"), None),))], ("agent lists the checklists",)),
])


def trigger(vp):
    return ["k_agent_Event", ["k_agent_One", "a_the_person_1"], vp]


def test_a_plural_a_count_every_and_an_and_list_are_several_things():
    assert not spec_one_thing.several(np("DetA")) and not spec_one_thing.several(np("DetThe"))
    for det in ("DetThePl", "DetPl", "DetEvery", "DetTwo"):
        assert spec_one_thing.several(np(det)), det
    assert spec_one_thing.several(["k_note_And", ["k_note_Two", np("DetA")[1], np("DetA")[1]]])


def test_a_request_with_a_plural_object_is_found_only_in_a_trigger_and_only_of_an_operation():
    assert spec_one_thing.plural(VOCAB, trigger(["e_remove_action_1_1", np("DetThePl")]))[0] == "remove"
    assert spec_one_thing.plural(VOCAB, trigger(["e_remove_action_1_1", np("DetA")])) is None
    assert spec_one_thing.plural(VOCAB, trigger(["e_follow_action_2_1", np("DetThePl")])) is None
    response = ["k_service_Act_k_service", "PPos", ["e_remove_action_1_1", np("DetEvery")]]
    assert spec_one_thing.plural(VOCAB, response) is None


def test_two_readings_by_two_frames_of_one_verb_name_both():
    a, b = trigger("e_list_action_4_1"), trigger(["e_list_action_3_1", np("DetThePl", "k_checklist")])
    assert spec_one_thing.frames(VOCAB, a, b) == ['"agent lists the checklists" (notes.browse)',
                                                  '"agent lists checklist" (notes.show)']
    assert spec_one_thing.frames(VOCAB, a, a) == []
