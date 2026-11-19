"""shop_refused: the one refusal carries a business reason and the references it names (design §5.4)."""
from shop_refused import Refused


def test_an_old_raise_keeps_working():
    why = Refused("the title is one line of text")
    assert str(why) == "the title is one line of text"
    assert why.reason == "the title is one line of text" and why.names == []


def test_a_reason_and_names_beside_the_message():
    why = Refused("a design-decision gives --summary", reason="no summary", names=["parameter:summary"])
    assert str(why) == "a design-decision gives --summary"
    assert why.reason == "no summary" and why.names == ["parameter:summary"]


def test_a_message_spelled_by_the_adapter():
    why = Refused("a design-decision gives {names}", reason="missing parameters",
                  names=["parameter:summary", "parameter:wording"])
    assert str(why) == "a design-decision gives summary, wording"
    spelled = {"parameter:summary": "--summary", "parameter:wording": "--decision"}
    assert why.spelled(spelled.get) == "a design-decision gives --summary, --decision"
