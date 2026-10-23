"""measure's readers: an initiative's log.jsonl, its stages' session.json, and Claude Code transcripts (raw, or the
slim export). A file of a shape not known is refused, naming it; no figure is guessed. Standard library only."""
import datetime
import json
import os
from pathlib import Path


class Refused(Exception):
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
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
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


def read_log(path):
    """log.jsonl's rows, each with its `time` as a datetime."""
    rows = json_rows(path)
    for row in rows:
        row["at"] = moment(row.get("time"), path)
    return rows


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def read_session_json(path):
    """The figures of one stage's session.json (what `claude -p --output-format json` printed): its id, turns, cost
    and tokens of each kind."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        data = None
    usage = data.get("usage") if isinstance(data, dict) else None
    if not isinstance(usage, dict) or not all(number(usage.get(k)) for k in ("input_tokens", "output_tokens")):
        raise Refused("%s is not a session.json of a shape measure knows (no usage with input and output tokens)" % path)
    if not (number(data.get("total_cost_usd")) and number(data.get("num_turns"))):
        raise Refused("%s is not a session.json of a shape measure knows (no total_cost_usd and num_turns)" % path)
    return {"session": data.get("session_id"), "turns": data["num_turns"], "cost": data["total_cost_usd"],
            "output_tokens": usage["output_tokens"],
            "new_input_tokens": usage["input_tokens"] + usage.get("cache_creation_input_tokens", 0),
            "cache_read_tokens": usage.get("cache_read_input_tokens", 0)}


def read_session_jsons(runs):
    """Every session.json under an initiative's runs/ directory, by session id."""
    found = {}
    for path in sorted(Path(runs).glob("*/*/session.json")):
        figures = read_session_json(path)
        found[figures["session"]] = figures
    return found


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


def round_trips(session):
    """The distinct requests of `session`'s own rows in its transcript in Claude Code's store (any project
    directory), or None when no transcript is found. A subagent's rows are not the session's."""
    found = sorted((store_dir() / "projects").glob("*/%s.jsonl" % session))
    if not found:
        return None
    path = found[0]
    return len({request_key(row, message, path, number_)
                for number_, row, message, _, _, who in assistant_rows(path)
                if who == session and not (row.get("agentId") or row.get("agent") or row.get("isSidechain"))})


def read_transcripts(directory):
    """The sessions in the transcripts under `directory`: per session id its start, tokens and the session that
    dispatched it. A row is Claude Code's own (timestamp, sessionId, agentId, message.usage) or the slim export's
    (time, session, agent, usage); a subagent's rows name the session that dispatched it as their session."""
    sessions = {}
    for path in sorted(Path(directory).rglob("*.jsonl")):
        requests = {}
        for number_, row, message, usage, stamp, who in assistant_rows(path):
            key = request_key(row, message, path, number_)
            old = requests.get(key)
            requests[key] = {
                "who": who, "agent": row.get("agentId", row.get("agent")),
                "at": min(moment(stamp, path), old["at"]) if old else moment(stamp, path),
                "output_tokens": max(usage["output_tokens"], old["output_tokens"] if old else 0),
                "new_input_tokens": usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0),
                "cache_read_tokens": usage.get("cache_read_input_tokens", 0)}
        for request in requests.values():
            ident = request["agent"] or request["who"]
            one = sessions.setdefault(ident, {"session": ident, "start": request["at"], "output_tokens": 0,
                                              "new_input_tokens": 0, "cache_read_tokens": 0,
                                              "dispatched_by": request["who"] if request["agent"] else None})
            one["start"] = min(one["start"], request["at"])
            for kind in ("output_tokens", "new_input_tokens", "cache_read_tokens"):
                one[kind] += request[kind]
    return sessions
