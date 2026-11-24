"""domain_model_props: an operation's and an event's properties read off their model lines, and v_m8 of one that
refers to what the model does not declare (b547, checking r66, r67)."""
import domain_model
import domain_model_check
import pytest
from shop_refused import Refused

BLOCK = """object order

service payments
  operation charge(order)  idempotent by order; compensated by refund; followed by an order is charged
    outcomes: done → the order | refused: no order
  operation refund(order)  outcomes: done → the order

event an order is charged: raised by payments.charge; delivery: at least once, in order; when: the order is paid
"""


def _model(tmp_path, block):
    (tmp_path / "spec" / "model").mkdir(parents=True)
    (tmp_path / "spec" / "model" / "a.md").write_text("---\narea: a\nkind: core\n---\n\n```model\n" + block + "```\n")
    return domain_model.read(tmp_path)


def test_an_operation_line_carries_its_properties(tmp_path):
    model = _model(tmp_path, BLOCK)
    charge = model.services["payments"].operation("charge")
    assert [p.text for p in charge.properties] == ["idempotent by order", "compensated by refund",
                                                   "followed by an order is charged"]
    assert [o.kind for o in charge.outcomes] == ["done", "refused"] and [n for n, _ in charge.raw] == ["order"]
    assert not model.services["payments"].operation("refund").properties


def test_an_event_line_carries_its_delivery_and_when(tmp_path):
    event = _model(tmp_path, BLOCK).events[0]
    assert (event.phrase, event.operation) == ("an order is charged", "charge")
    assert [p.text for p in event.properties] == ["delivery: at least once, in order", "when: the order is paid"]


def test_properties_that_refer_to_what_the_model_declares_pass(tmp_path):
    assert domain_model_check.problems(_model(tmp_path, BLOCK)) == []


@pytest.mark.parametrize("prop", ["idempotent by amount", "compensated by unfile", "followed by an order is lost"])
def test_a_property_that_refers_to_nothing_declared_is_v_m8(tmp_path, prop):
    block = BLOCK.replace("idempotent by order; compensated by refund; followed by an order is charged", prop)
    assert [(c, s) for c, s, _ in domain_model_check.problems(_model(tmp_path, block))] == [
        ("v_m8", "payments.charge %s" % prop)]


def test_an_event_segment_that_is_no_property_is_refused(tmp_path):
    with pytest.raises(Refused, match="delivery: <text>"):
        _model(tmp_path, BLOCK.replace("; when:", "; whenever:"))
