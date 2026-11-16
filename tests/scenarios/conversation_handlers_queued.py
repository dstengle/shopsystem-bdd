"""conversation's queued message (b52), beside conversation_handlers.py: a message of the person Claude Code gave the
session while it worked on a turn, written into the session's transcript as the `queued_command` attachment row the
harness keeps it in, inside the turn of the session that follows the person's message m1."""
import hashlib
import sys
from pathlib import Path

from vocab import handler

HERE = Path(__file__).resolve().parent
C = sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / "conversation_handlers.py").encode()).hexdigest()[:12]]
T = C.T


@handler("GivenK", "queued message")
def given_queued(step):
    """A queued message of the person: its words and its row's uuid, kept for the transcript the When writes."""
    name = step.names[0]
    C.talk(step)["messages"][name] = "queued-%s" % name
    C.talk(step).setdefault("queued", {})[name] = "Add a backlog item for %s, sent mid-turn." % name


def rows(step):
    """The transcript's rows: CONVERSATION with each queued message's row after the session's tool use of its second
    turn, before the tool's result."""
    queued = [T.queued(text, C.talk(step)["messages"][name], T.at(4))
              for name, text in C.talk(step).get("queued", {}).items()]
    return T.CONVERSATION[:4] + queued + T.CONVERSATION[4:]


def words(step):
    """The words `work quote` is run on: the queued message's the step names, else the person's message m1's."""
    named = [n for n in step.names if n in C.talk(step).get("queued", {})]
    return C.talk(step)["queued"][named[0]] if named else T.TEXTS[C.CITED]
