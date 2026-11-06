"""The side of a request this repository keeps (capability requests, r48-r51): received, its record kept in its
upstream's repository (this one) and asked by another bounded context, or sent, kept in its asker's (this one) and
answered by another. An internal request, and a record kept from before requests named their upstream, is neither,
and either side's commands run on it. Each side passes only its own turn, and only the asker replies."""
from request_text import field
from shop_files import Refused


def _own(root):
    # imported here: request_moves calls this module
    import request_moves

    return request_moves.own_askers(root)


def received(root, text):
    upstream, asker = field(text, "upstream"), field(text, "asker")
    return upstream in _own(root) and asker not in _own(root) | {"internal", None}


def sent(root, text):
    upstream = field(text, "upstream")
    return upstream is not None and upstream not in _own(root) and field(text, "asker") in _own(root)


def refuse_reply(root, text, ident):
    """r49: the asker answers in its own repository; a request this context received is not its to reply to."""
    if received(root, text):
        raise Refused("%s is a request this context received from %s; the asker replies" % (ident, field(text, "asker")))


def refuse_turn(root, text, ident):
    """r48, r50, r51: `work turn` passes only this side's own turn: the upstream's on a request received, the
    asker's on one sent."""
    if received(root, text) and field(text, "turn") == "asker":
        raise Refused("%s is in the asker's turn; %s, its asker, passes it" % (ident, field(text, "asker")))
    if sent(root, text) and field(text, "turn") != "asker":
        raise Refused("%s is in the upstream's turn; %s, its upstream, passes it" % (ident, field(text, "upstream")))
