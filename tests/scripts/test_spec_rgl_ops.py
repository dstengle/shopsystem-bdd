"""spec_rgl_ops: a request with its parameters in grammar 4 (the domain contract design, §5.1), generated from the
domain-model fixture's operations: an object slot, a fixed object, a valued, a text, a some, a no, a flag and an object
parameter, "without a X and a Y" both absent, and "the p" a response names."""
import pathlib

import pytest
import spec_grammar4
import spec_rgl_ops
import toolchain

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"
KEEP = ", the notes service shall keep the note."


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def tree(line):
    parsed = spec_grammar4.parse(FIXTURE, line)
    assert parsed.tree, parsed.refusal
    return parsed.tree


def test_the_funs_of_each_operations_parameters():
    vocab, srcs = spec_grammar4.sources(FIXTURE)
    funs = spec_rgl_ops.funs(vocab)
    assert funs["o_notes_add_priority_v_high"] == ("notes.add", "priority", "v:high")
    assert funs["o_notes_add_reminder_Flag"] == ("notes.add", "reminder", "Flag")
    assert funs["o_notes_label_tag_Is_k_tag"] == ("notes.label", "tag", "Is")
    assert funs["p_text_NP"] == (None, "text", "NP")
    assert not any(f.startswith("o_notes_label_note") for f in funs)        # the object is the frame's slot
    assert not any(f.startswith(("o_notes_list", "o_notes_file")) for f in funs)    # no parameter said
    context = srcs["Context.gf"]
    assert "q_add_" in context and "k_agent_Request : k_agent_Arg -> k_agent_Req -> Trig" in context
    assert "o_notes_label_tag_Some" not in context        # an object parameter is said by its noun phrase


@pytest.mark.parametrize("params, funs", [
    (" with the text `milk` and the priority `high`", ["o_notes_add_text_Is", "o_notes_add_priority_v_high"]),
    (" with a text", ["o_notes_add_text_Some"]),
    (" without a text and a priority", ["o_notes_add_Without", "o_notes_add_text_No", "o_notes_add_priority_No"]),
    (" with the reminder and without a priority", ["o_notes_add_WithWithout", "o_notes_add_reminder_Flag"]),
    (" without the reminder", ["o_notes_add_reminder_NoFlag"]),
])
def test_a_request_with_its_parameters(params, funs):
    found = tree("When the person adds a note%s%s" % (params, KEEP))
    assert "k_agent_Request" in found and all(f in found for f in funs), found


def test_an_object_slot_an_object_parameter_and_a_fixed_object():
    assert "o_notes_label_tag_Is_k_tag" in tree("When the person labels a note with a tag, the notes service shall "
                                                "keep the tag.")
    assert "e_list_action_" in tree("When the person lists the notes, the notes service shall complete the request.")
    assert "e_file_action_" in tree("When the person files a note" + KEEP)


def test_a_parameter_is_named_and_a_value_outside_its_values_is_refused():
    assert "p_text_NP" in tree("If the person adds a note without a text, then the notes service shall refuse the "
                               "request and name the text.")
    # session's call: a parameter's values are the grammar's, so a value it does not declare does not parse
    assert spec_grammar4.parse(FIXTURE, "When the person adds a note with the priority `urgent`" + KEEP).refusal
    # a request with its parameters is said in a response too, its doer the requester (response-request, b543)
    assert "k_service_ActReq_k_agent" in tree("When the person files a note, the notes service shall add the note "
                                              "with a text.")
