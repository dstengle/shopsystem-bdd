"""domain_envelope: the one response every operation answers with (the domain contract design, §5.4)."""
import json

import pytest

import domain_envelope
from domain_envelope import Response
from shop_refused import Refused


def test_the_four_fields():
    response = Response("returned", content={"id": "b12"})
    assert response.as_dict() == {"outcome": "returned", "content": {"id": "b12"}, "errors": [], "notices": []}


def test_errors_only_with_a_refusal_or_a_failure():
    with pytest.raises(ValueError):
        Response("refused")
    with pytest.raises(ValueError):
        Response("failed")
    with pytest.raises(ValueError):
        Response("done", errors=[{"reason": "no tier", "names": ["parameter:tier"]}])
    assert Response("refused", errors=[{"reason": "no tier", "names": ["parameter:tier"]}]).errors


def test_an_unknown_outcome_refused():
    with pytest.raises(ValueError):
        Response("ran")


def test_broken_is_no_domain_outcome():
    assert "broken" not in domain_envelope.DOMAIN
    assert set(domain_envelope.DOMAIN) == {"done", "returned", "refused", "passed", "failed"}
    response = domain_envelope.broken(OSError("disk full"))
    assert response.outcome == "broken" and response.errors == [{"reason": "disk full", "names": []}]


def test_a_notice_beside_a_done_outcome():
    notice = {"reason": "not shared", "names": ["shared store"]}
    assert Response("done", notices=[notice]).as_dict()["notices"] == [notice]


def test_a_refusal_read_into_a_response():
    response = domain_envelope.refused(Refused("no tier given", reason="no tier", names=["parameter:tier"]))
    assert response.as_dict() == {"outcome": "refused", "content": None,
                                  "errors": [{"reason": "no tier", "names": ["parameter:tier"]}], "notices": []}


def test_an_old_refusal_reads_its_message_as_its_reason():
    response = domain_envelope.refused(Refused("the title is one line of text"))
    assert response.errors == [{"reason": "the title is one line of text", "names": []}]


def test_the_json_shape_read_back():
    response = Response("refused", errors=[{"reason": "no summary", "names": ["parameter:summary"]}])
    text = response.json()
    assert json.loads(text) == response.as_dict()
    assert domain_envelope.read(text) == response
