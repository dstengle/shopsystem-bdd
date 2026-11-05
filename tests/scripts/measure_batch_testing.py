"""What the batch measurement's script tests share (workflow simplification plan 7): Claude Code's raw transcript rows
written by hand into a store of the test's own, a main session's and a subagent's, with a subagent's meta file."""
import json
from pathlib import Path

USAGE = {"input_tokens": 10, "output_tokens": 20, "cache_read_input_tokens": 30, "cache_creation_input_tokens": 0}


def store_rows(session, times, agent=None, model="claude-opus-5-5", usage=None, rows_per_request=1):
    """Claude Code's raw rows: one request at each of `times` (ISO strings), `requestId` `<session|agent>-q<n>`, each
    request written in `rows_per_request` rows with its usage repeated."""
    rows = []
    for n, at in enumerate(times, 1):
        for _ in range(rows_per_request):
            row = {"type": "assistant", "timestamp": at, "sessionId": session,
                   "requestId": "%s-q%d" % (agent or session, n),
                   "message": {"model": model, "usage": dict(usage or USAGE)}}
            if agent:
                row.update(agentId=agent, isSidechain=True)
            rows.append(json.dumps(row))
    return "".join(r + "\n" for r in rows)


def write_session(project, session, text):
    path = Path(project) / ("%s.jsonl" % session)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_agent(project, session, agent, text, agent_type=None, description=None):
    folder = Path(project) / session / "subagents"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ("agent-%s.jsonl" % agent)).write_text(text, encoding="utf-8")
    if agent_type is not None or description is not None:
        meta = {"agentType": agent_type, "description": description}
        (folder / ("agent-%s.meta.json" % agent)).write_text(json.dumps(meta), encoding="utf-8")
    return folder / ("agent-%s.jsonl" % agent)
