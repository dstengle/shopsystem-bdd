"""The messages of a session's transcript (capability conversation; workflow simplification plan 8, D2 and D4): the
person's prompts and the session's text of each turn, read from Claude Code's `<session>.jsonl` in file order, without
tool uses, tool results, thinking, system reminders, meta, sidechain, compaction-summary or local-command rows; the
message of the person a quote's words cite, and the messages around it. A row with no type is refused naming the file
and line (0018). Standard library only."""
import re
from dataclasses import dataclass
from datetime import datetime

from measure_read import Refused, json_rows, moment

AROUND = 2
REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL)
COMMAND = ("<command-", "<local-command-")


@dataclass(frozen=True)
class Message:
    ident: str
    who: str
    at: datetime
    text: str


def _texts(content):
    """The text of a row's content: the string itself, else its `text` blocks joined by a blank line."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n\n".join(b["text"] for b in content
                       if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str))


def _persons(row):
    """The person's words in a `user` row, or "" when the row is not a message of the person."""
    if row.get("isMeta") or row.get("isCompactSummary"):
        return ""
    text = REMINDER.sub("", _texts((row.get("message") or {}).get("content"))).strip()
    return "" if text.startswith(COMMAND) else text


def _lines(path):
    """The number of each non-blank line of `path`, in the order json_rows gives their rows."""
    return [n for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").split("\n"), 1)
            if line.strip()]


def messages(path):
    """The messages of the transcript at `path`, in file order (D2): a person's message closes the session's turn,
    whose ident and time are those of its first row with text."""
    found, turn = [], None

    def close():
        if turn:
            found.append(Message(turn[0], "session", turn[1], "\n\n".join(turn[2])))

    for number, row in zip(_lines(path), json_rows(path), strict=True):
        where = "%s:%d" % (path, number)
        kind = row.get("type")
        if not isinstance(kind, str):
            raise Refused("%s has no type; the shape of %s is not known" % (where, path.name))
        if kind not in ("user", "assistant") or row.get("isSidechain"):
            continue
        if kind == "user":
            text = _persons(row)
            if text:
                close()
                turn = None
                found.append(Message(row.get("uuid") or where, "person", moment(row.get("timestamp"), where), text))
            continue
        text = _texts((row.get("message") or {}).get("content")).strip()
        if text and turn is None:
            turn = (row.get("uuid") or where, moment(row.get("timestamp"), where), [])
        if text:
            turn[2].append(text)
    close()
    return found


def normal(text):
    """`text` with its whitespace collapsed to one space, stripped."""
    return " ".join(str(text).split())


def cited(found, words):
    """The index of the newest message of the person in `found` whose text holds `words`, whitespace collapsed and case
    kept; None when there is none (D4)."""
    want = normal(words)
    for index in range(len(found) - 1, -1, -1):
        if found[index].who == "person" and want in normal(found[index].text):
            return index
    return None


def around(found, index, n=AROUND):
    """The message at `index` with the `n` messages before it and the `n` after it, as many as exist."""
    return found[max(0, index - n):index + n + 1]
