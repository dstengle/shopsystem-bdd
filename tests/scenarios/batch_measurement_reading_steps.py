"""batch-measurement's steps for how measure reads files: a line break inside a JSON string, times ending in Z."""
import json
import os
import time

from pytest_bdd import given, parsers, then

from .batch_measurement_transcripts import slim_session


@given(parsers.parse("the text of one of those messages holds U+{code} inside its JSON string"))
def text_holds(world, code):
    session = list(world.store)[-1]
    rows = [json.loads(line) for line in world.store[session].splitlines()]
    rows[0]["message"]["content"] = [{"type": "text", "text": "before%safter" % chr(int(code, 16))}]
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    assert chr(int(code, 16)) in text
    world.store[session] = text


@given(parsers.parse("the session's local time zone is UTC+{hours:d}:00"))
def local_zone(request, hours):
    old = os.environ.get("TZ")

    def restore():
        if old is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old
        time.tzset()
    request.addfinalizer(restore)
    os.environ["TZ"] = "UTC-%d" % hours       # POSIX spells the sign the other way round
    time.tzset()


@given(parsers.parse("the directory sessions holds the transcript {session}, starting at {starts} and ending at "
                     "{ends}"))
def directory_holds_one(world, session, starts, ends):
    world.transcripts["sessions/%s.jsonl" % session] = slim_session(session, None, starts, ends, 10, 5, 20)


@then("measure exits successfully")
def exits_successfully(world):
    assert world.code == 0, world.err


@then(parsers.parse("the measurement gives the session {session}"))
def gives_session(world, session):
    found = [s["session"] for s in world.figures()["sessions"]]
    assert session in found, found
