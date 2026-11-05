"""The messages of a session's transcript (capability conversation; workflow simplification plan 8, D2 and D4): the
person's prompts and the session's text of each turn, read from Claude Code's `<session>.jsonl` in file order, without
tool uses, tool results, thinking, system reminders, meta, sidechain, compaction-summary, local-command or `!`
bash-mode rows, notifications of background tasks or any row Claude Code wrote rather than the person (an `origin` of
a kind other than `human`, an interruption marker); a slash command is the person's message `/<name> <args>`
(plan 8's review, Q1); a carriage return is a newline, so what is rendered reads back as it is (M2). The
message of the person a quote's words cite, and the messages around it. A row with no type is refused naming the file
and line (0018). Standard library only."""
import re
from dataclasses import dataclass
from datetime import datetime

from transcripts import Refused, json_rows, moment

AROUND = 2
REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL)
COMMAND = ("<command-", "<local-command-", "<bash-", "<task-notification>", "[Request interrupted by user")
SLASH = re.compile(r"<command-name>(.*?)</command-name>", re.DOTALL)
ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.DOTALL)


@dataclass(frozen=True)
class Message:
    ident: str
    who: str
    at: datetime
    text: str


def _texts(content):
    """The text of a row's content: the string itself, else its `text` blocks joined by a blank line; `\r\n` and `\r`
    written `\n`."""
    if isinstance(content, list):
        content = "\n\n".join(b["text"] for b in content
                              if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str))
    return content.replace("\r\n", "\n").replace("\r", "\n") if isinstance(content, str) else ""


def _slash(text):
    """`/<name> <args>` of a slash command's row, or None when `text` names no command."""
    name = SLASH.search(text)
    if name is None:
        return None
    args = ARGS.search(text)
    words = "/" + name.group(1).strip().lstrip("/")
    return ("%s %s" % (words, args.group(1).strip())).strip() if args else words


def _persons(row):
    """The person's words in a `user` row, or "" when the row is not a message of the person."""
    origin = row.get("origin")
    if row.get("isMeta") or row.get("isCompactSummary") or (isinstance(origin, dict) and origin.get("kind") != "human"):
        return ""
    text = REMINDER.sub("", _texts((row.get("message") or {}).get("content"))).strip()
    slash = _slash(text) if text.startswith(("<command-name>", "<command-message>")) else None
    if slash is not None:
        return slash
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
        where, ident = "%s:%d" % (path, number), "%s:%d" % (path.name, number)
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
                found.append(Message(row.get("uuid") or ident, "person", moment(row.get("timestamp"), where), text))
            continue
        text = _texts((row.get("message") or {}).get("content")).strip()
        if text and turn is None:
            turn = (row.get("uuid") or ident, moment(row.get("timestamp"), where), [])
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
