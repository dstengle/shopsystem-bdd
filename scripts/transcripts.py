"""Claude Code's transcripts read, raw or the slim export: a JSON-lines file's rows, an ISO time, a transcript's
assistant rows checked, the key of a request, and Claude Code's own store. A file of a shape not known is refused,
naming it; no figure is guessed. Standard library and shop_refused."""
import datetime
import json
import os
from pathlib import Path

import shop_refused


class Refused(shop_refused.Refused):
    """What measure was asked cannot be done; the message says why, and nothing was written."""


def moment(text, where):
    """An ISO time as an aware datetime (a time with no offset is UTC)."""
    try:
        at = datetime.datetime.fromisoformat(str(text))
    except ValueError:
        raise Refused("%s: %r is not an ISO time" % (where, text)) from None
    return at if at.tzinfo else at.replace(tzinfo=datetime.UTC)


def json_rows(path):
    """The JSON object of each non-blank line of `path`; a line that is not one is refused, naming file and line."""
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            row = None
        if not isinstance(row, dict):
            raise Refused("%s:%d is not a JSON object; the shape of %s is not known" % (path, number, path.name))
        rows.append(row)
    return rows


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def assistant_rows(path):
    """Each assistant row of the transcript `path`, checked: (line number, row, message, usage, time, session)."""
    for number_, row in enumerate(json_rows(path), 1):
        if "type" not in row:
            raise Refused("%s:%d has no type; the shape of %s is not known" % (path, number_, path.name))
        if row["type"] != "assistant":
            continue
        message = row.get("message") if isinstance(row.get("message"), dict) else row
        usage, stamp = message.get("usage"), row.get("timestamp", row.get("time"))
        who = row.get("sessionId", row.get("session"))
        if not (isinstance(usage, dict) and number(usage.get("output_tokens")) and who and stamp):
            raise Refused("%s:%d has no time, session or usage; the shape of %s is not known" % (path, number_, path.name))
        yield number_, row, message, usage, stamp, who


def request_key(row, message, path, number_):
    return row.get("requestId") or message.get("id") or row.get("uuid") or (path, number_)


def store_dir():
    """Claude Code's own store: the directory CLAUDE_CONFIG_DIR names, else .claude in the home directory."""
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
