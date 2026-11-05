"""Claude Code's transcript rows written by hand for the conversation tests (plan 8, Task 2): the person's prompt, the
session's text, thinking, a tool use and its result, each a raw row of `<session>.jsonl`, and CONVERSATION, six
messages with a tool use and its result inside the second turn of the session. A test helper, not a test module."""
import json
from pathlib import Path


def _row(kind, content, uuid, at, session, **extra):
    row = {"type": kind, "uuid": uuid, "timestamp": at, "sessionId": session,
           "message": {"role": "user" if kind == "user" else "assistant", "content": content}}
    row.update(extra)
    return row


def person(text, uuid, at, session="s-1", **extra):
    """The person's prompt: `text` a string, or a list of content blocks as given."""
    return _row("user", text, uuid, at, session, **extra)


def session_text(text, uuid, at, session="s-1", msg="m", **extra):
    """One assistant row with one text block; `msg` is its API message's id (a turn spans many)."""
    row = _row("assistant", [{"type": "text", "text": text}], uuid, at, session, **extra)
    row["message"]["id"] = msg
    return row


def thinking(text, uuid, at, session="s-1", msg="m", **extra):
    row = _row("assistant", [{"type": "thinking", "thinking": text, "signature": "x"}], uuid, at, session, **extra)
    row["message"]["id"] = msg
    return row


def tool_use(name, uuid, at, session="s-1", msg="m", tool="t-1", **extra):
    block = {"type": "tool_use", "id": tool, "name": name, "input": {"command": "cat /etc/secret-path"}}
    row = _row("assistant", [block], uuid, at, session, **extra)
    row["message"]["id"] = msg
    return row


def tool_result(text, uuid, at, session="s-1", tool="t-1", **extra):
    return _row("user", [{"type": "tool_result", "tool_use_id": tool, "content": text}], uuid, at, session, **extra)


def write(project, session, rows):
    """`<project>/<session>.jsonl` holding `rows`, one JSON object a line."""
    project = Path(project)
    project.mkdir(parents=True, exist_ok=True)
    path = project / ("%s.jsonl" % session)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def at(minute):
    return "2026-11-05T10:%02d:00.000Z" % minute


TEXTS = ["Please write the plan for the parser.", "I will write it.", "Keep the turns of the conversation, all of them.",
         "Done: the turns are kept.", "Now the names table, please.", "The names table is printed."]
CONVERSATION = [
    person(TEXTS[0], "u1", at(1)),
    session_text(TEXTS[1], "a1", at(2), msg="m1"),
    person(TEXTS[2], "u2", at(3)),
    tool_use("Bash", "a2", at(4), msg="m2"),
    tool_result("TOOL OUTPUT secret", "u3", at(5)),
    session_text(TEXTS[3], "a3", at(6), msg="m3"),
    person(TEXTS[4], "u4", at(7)),
    session_text(TEXTS[5], "a4", at(8), msg="m4"),
]
IDENTS = ["u1", "a1", "u2", "a3", "u4", "a4"]
