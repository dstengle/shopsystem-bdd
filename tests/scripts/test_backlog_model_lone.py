"""A model line that restates an event or an actor (b647, batches r120, r121): laid in place of the line of its
phrase or name, put back as the model held it before the lay, a new one taken out; and the member lines an object's
restatement leaves out (drafting r70)."""
import backlog_model
import backlog_model_elements

BODY = ["object note", "  attributes: text (text)", "", "event a note is added: raised by notes.add",
        "actor the person kind of agent", ""]
EVENT = "event a note is added: raised by notes.add; delivery: at least once"


def test_an_event_restated_in_place():
    laid = backlog_model.merged(BODY, [EVENT])
    assert laid == BODY[:3] + [EVENT] + BODY[4:]


def test_an_actor_restated_in_place():
    assert backlog_model.merged(BODY, ["actor the person"]) == BODY[:4] + ["actor the person"] + BODY[5:]


def test_an_event_put_back():
    laid = backlog_model.merged(BODY, [EVENT])
    assert backlog_model.unmerged(laid, [EVENT], lambda header, op, lines: BODY) == BODY


def test_a_new_event_appended_and_taken_out():
    new = "event a note is filed: raised by notes.file"
    laid = backlog_model.merged(BODY, [new])
    assert laid == BODY[:5] + ["", new, ""]
    assert backlog_model.unmerged(laid, [new], lambda header, op, lines: BODY) == BODY


def test_left_out_names_the_members_a_restatement_cuts():
    body = ["object note", "  attributes: text (text)", "  relations: carries → tag (many)"]
    chunk = [("object note", ["  attributes: text (text)"])]
    assert backlog_model_elements.left_out(body, chunk) == ["relations: carries → tag (many)"]
    assert backlog_model_elements.left_out(body, [("object note", ["  lifecycle status: a → b"])]) == []
