"""The requester of the request a reply trigger is on (b728, scenarios#r46): the doer of the context's line whose
response requests the operation, else the actor the operation's model line gives, else refused naming the operation."""
from types import SimpleNamespace

import pytest
import spec_steps4_boxes
import spec_steps4_request
from spec_lf_core import Ref

ASKER = Ref("x3", "service", "constant", "the decisions service")


def reader(asks=None, by=()):
    vocab = SimpleNamespace(operations={"registry.publish": SimpleNamespace(by=by)},
                            actors=[("the person", "agent"), ("the decisions service", "service")],
                            elements={"the person": "actor the person", "the decisions service": "service decisions"})
    return SimpleNamespace(vocab=vocab, asks=dict(asks or {}))


def test_the_doer_of_the_line_that_asks_is_the_requester():
    assert spec_steps4_request.requester(reader({"registry.publish": ASKER}, ("the person",)), "registry.publish") \
        is ASKER


def test_with_no_line_that_asks_the_actor_of_the_model_line_is_the_requester():
    found = spec_steps4_request.requester(reader(by=("decisions",)), "registry.publish")
    assert (found.kind, found.origin, found.value) == ("service", "constant", "the decisions service")


def test_a_context_that_gives_no_requester_is_refused_naming_the_operation():
    with pytest.raises(spec_steps4_boxes.TraceError, match="registry.publish"):
        spec_steps4_request.requester(reader(), "registry.publish")
