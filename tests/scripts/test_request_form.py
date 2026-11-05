"""The comment form of a request's issue (requests r32, r33): one block of fields, read back as it was rendered; a
body with no block is no form, and a block that does not parse is unreadable, saying why."""
import pytest
import request_form

OFFER = "Capability work-queue:\n\n## Behaviour\n~~~\nnot the end\n\nthe end"


def test_a_form_reads_back_as_it_was_rendered():
    body = request_form.render({"turn": "asker", "step": "offer", "offer": OFFER},
                               {"Outcomes": {"2": "accepted", "1": "refused"}, "Lines": {"3": "a line"}}, "Free text.")
    assert body.startswith("~~~shop-request\nstep: offer\n") and body.endswith("\nFree text.\n")
    form = request_form.parse(body)
    assert form.step == "offer" and form.fields["offer"] == OFFER and form.fields["turn"] == "asker"
    assert form.sections == {"Outcomes": {"1": "refused", "2": "accepted"}, "Lines": {"3": "a line"}}


def test_line_ends_from_github_are_read():
    assert request_form.parse(request_form.render({"step": "fits"}).replace("\n", "\r\n")).step == "fits"


def test_a_body_with_no_block_is_no_form():
    assert request_form.parse("Please merge it now.") is None
    assert not request_form.is_form("Please merge it now.")


@pytest.mark.parametrize("body, why", [
    ("~~~shop-request\nstep: turn\nthis is no field\n~~~\n", "no field"),
    ("~~~shop-request\nturn: asker\n~~~\n", "no step"),
    ("~~~shop-request\nstep: merge\n~~~\n", "no step"),
    ("~~~shop-request\nstep: turn\nline: x\n~~~\n", "needs a number"),
    ("~~~shop-request\nstep: turn\nstatus 2: x\n~~~\n", "takes no number"),
    ("~~~shop-request\nstep: turn\nstep: ask\n~~~\n", "twice"),
    ("~~~shop-request\nstep: turn\n~~~\n~~~shop-request\nstep: ask\n~~~\n", "2 blocks")])
def test_a_block_that_does_not_parse_is_unreadable(body, why):
    assert request_form.is_form(body)
    with pytest.raises(request_form.Unreadable, match=why):
        request_form.parse(body)
