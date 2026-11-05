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


def _role(sessions, cost):
    return {"sessions": sessions, "session_time_seconds": 60 * sessions, "session_time": "%d minutes" % sessions,
            "output_tokens": 100, "new_input_tokens": 200, "cache_read_tokens": 300, "cost": cost}


# A complete measurement of a batch (D9), the figures `measure show` and `measure compare` read.
FIGURES = {
    "batch": "batch-2", "status": "merged", "pull_request": "https://github.com/ex/ctx/pull/2",
    "items": [{"item": "b1", "title": "Abandon", "status": "delivered"},
              {"item": "b2", "title": "Exit", "status": "delivered"}],
    "window": {"started": "2026-11-01T10:00:00+00:00", "first_review": "2026-11-01T10:30:00+00:00",
               "built": "2026-11-01T11:00:00+00:00", "closed": "2026-11-01T12:00:00+00:00"},
    "wall_time_seconds": 7200, "wall_time": "2 hours", "waiting_for_merge_seconds": 3600,
    "session_time_seconds": 600, "session_time": "10 minutes",
    "tokens": {"output_tokens": 400, "new_input_tokens": 800, "cache_read_tokens": 1200},
    "cost": 1.0, "unpriced": {}, "prices_as_of": "2026-10-06",
    "cost_by_role": {"planning": _role(1, 0.4), "implementing": _role(1, 0.3), "review": _role(1, 0.2),
                     "fixing": _role(1, 0.1)},
    "sessions": [{"session": "s-1", "agent": None, "agent_type": None, "role": "planning",
                  "started": "2026-11-01T10:00:00+00:00", "requests": 3, "session_time_seconds": 60,
                  "output_tokens": 100, "new_input_tokens": 200, "cache_read_tokens": 300, "cost": 0.4},
                 {"session": "s-1", "agent": "a1", "agent_type": "shopsystem-bdd:pr-reviewer", "role": "review",
                  "started": "2026-11-01T10:30:00+00:00", "requests": 2, "session_time_seconds": 60,
                  "output_tokens": 100, "new_input_tokens": 200, "cache_read_tokens": 300, "cost": 0.2}],
    "sessions_from": "/store/projects/-repo", "sessions_found": 2,
    "reviews": [{"review": 1, "result": "fix-now", "findings": 1}],
    "findings": [{"finding": "f1", "review": 1, "grade": "Important", "triage": "fix now", "item": "b1"}],
    "findings_by_grade": {"Critical": 0, "Important": 1, "Minor": 0},
    "findings_by_triage": {"fix now": 1, "observation": 0, "drop": 0},
    "defects": {"review": {"b1": 1}, "after_merge": {}, "per_item": 0.5},
    "knobs": {"batch_size": 4, "items": 2, "changed_lines": 40, "size_limit": 1000, "reviews": 1,
              "readiness_bar": "mechanical"},
    "goals": {"wall_time_seconds": 7200, "cost": 1.0, "defects_per_item": 0.5},
}


def write_measurement(root, date, figures):
    """The record of a batch's measurement written as `measure batch` writes it, dated `date`; its path."""
    import measure_batch_show
    import measure_write
    path = measure_write.path_of(root, figures["batch"], date)
    measure_write.write(path, measure_write.text_of(root, figures["batch"], date, figures,
                                                    measure_batch_show.summary(figures)))
    return path
