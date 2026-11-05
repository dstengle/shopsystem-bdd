"""measure's readers: an initiative's log.jsonl, its stages' session.json, and Claude Code transcripts (raw, or the
slim export). A file of a shape not known is refused, naming it; no figure is guessed. Standard library only."""
import json
import re
from pathlib import Path

from transcripts import (
    Refused,
    assistant_rows,
    json_rows,
    moment,
    number,
    request_key,
    store_dir,
)


def read_log(path):
    """log.jsonl's rows, each with its `time` as a datetime."""
    rows = json_rows(path)
    for row in rows:
        row["at"] = moment(row.get("time"), path)
    return rows


def request_of(initiative, root):
    """The request `initiative` fulfils, as {"id": q<n>, "origin": "internal"|"external"}; None when its initiative.md
    names none. The request is read through `work`'s own reader. A link that cannot be read is refused."""
    import request_moves
    import workqueue
    path = Path(root) / ".shop" / "work" / initiative / "initiative.md"
    if not path.is_file():
        return None
    try:
        workqueue.read(path, root)
        head = path.read_text(encoding="utf-8").split("\n---", 1)[0]
        values = [v.strip() for v in re.findall(r"^fulfils:[ \t]*(.*)$", head, re.MULTILINE) if v.strip()]
        idents = {v.rsplit("/", 1)[-1] for value in values for v in re.split(r"[,\s]+", value) if v}
        if not idents:
            return None
        if len(idents) > 1:
            raise Refused("%s: the initiative fulfils more than one request: %s" % (path, ", ".join(sorted(idents))))
        ident = idents.pop()
        if "/" in ident or not (Path(root) / ".shop" / "work" / "requests" / (ident + ".md")).is_file():
            raise Refused("the queue does not hold the request %s (no %s)" % (
                ident, Path(".shop/work/requests") / (ident + ".md")))
        asker = request_moves.field(workqueue.read(request_moves.path_of(root, ident), root), "asker")
        if not asker:
            raise Refused("%s has no asker" % (Path(".shop/work/requests") / (ident + ".md")))
        internal = asker == "internal" or asker == "bounded-context/" + workqueue.context_path(root)
    except workqueue.Refused as why:
        raise Refused(str(why)) from None
    return {"id": ident, "origin": "internal" if internal else "external"}


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
    """Every session.json under an initiative's runs/ directory: the figures by session id, and each empty
    (zero-byte) one, which has no session id and gives no figures, as (work-item, stage, place, count): its run
    directory `<k>-<stage>` is the place-th (from 0, by the number k) of the count run directories of that stage.
    A directory not named `<k>-<stage>` with a whole-number k is left out."""
    found, empty, dirs = {}, set(), {}
    for path in Path(runs).glob("*/*"):
        k, _, stage = path.name.partition("-")
        if path.is_dir() and k.isdigit() and stage:
            dirs.setdefault((path.parent.name, stage), []).append((int(k), path))
    for (item, stage), runs_of in dirs.items():
        for place, (_, path) in enumerate(sorted(runs_of, key=lambda one: one[0])):
            if not (path / "session.json").is_file():
                continue
            if (path / "session.json").stat().st_size == 0:
                empty.add((item, stage, place, len(runs_of)))
                continue
            figures = read_session_json(path / "session.json")
            found[figures["session"]] = figures
    return found, empty


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


def tool_uses(message, path, number_):
    """(key, tool name) of each tool-use block of a message; the name only, never the tool's input."""
    content = message.get("content")
    for index, block in enumerate(content if isinstance(content, list) else []):
        if isinstance(block, dict) and block.get("type") == "tool_use":
            if not (isinstance(block.get("name"), str) and block["name"]):
                raise Refused("%s:%d has a tool use with no name; the shape of %s is not known" % (path, number_, path.name))
            yield block.get("id") or (number_, index), block["name"]


def compactions(path):
    """The session or subagent id of each compaction row (a system row of subtype compact_boundary) in `path`."""
    for number_, row in enumerate(json_rows(path), 1):
        if row.get("type") == "system" and row.get("subtype") == "compact_boundary":
            who = row.get("agentId", row.get("agent")) or row.get("sessionId", row.get("session"))
            if not (who and row.get("timestamp", row.get("time"))):
                raise Refused("%s:%d has no time or session; the shape of %s is not known" % (path, number_, path.name))
            yield who


def read_transcripts(directory):
    """The sessions in the transcripts under `directory`: per session id its start, the time of each of its messages,
    tokens, round trips (distinct requests), tool uses by tool name, compactions and the session that dispatched it.
    A row is Claude Code's own (timestamp, sessionId, agentId, message.usage) or the slim export's (time, session,
    agent, usage); a subagent's rows name the session that dispatched it as their session."""
    sessions = {}
    for path in sorted(Path(directory).rglob("*.jsonl")):
        requests, uses = {}, {}
        for number_, row, message, usage, stamp, who in assistant_rows(path):
            key = request_key(row, message, path, number_)
            for use, name in tool_uses(message, path, number_):
                uses[row.get("agentId", row.get("agent")) or who, use] = name
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
                                              "new_input_tokens": 0, "cache_read_tokens": 0, "times": [],
                                              "round_trips": 0, "tool_uses": {}, "compactions": 0,
                                              "dispatched_by": request["who"] if request["agent"] else None})
            one["start"] = min(one["start"], request["at"])
            one["times"].append(request["at"])
            one["round_trips"] += 1
            for kind in ("output_tokens", "new_input_tokens", "cache_read_tokens"):
                one[kind] += request[kind]
        for (ident, _), name in uses.items():
            if ident in sessions:
                sessions[ident]["tool_uses"][name] = sessions[ident]["tool_uses"].get(name, 0) + 1
        for ident in compactions(path):
            if ident in sessions:
                sessions[ident]["compactions"] += 1
    return sessions
