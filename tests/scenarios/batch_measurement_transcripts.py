"""The transcripts batch-measurement's scenarios write: Claude Code's raw rows and the slim export's rows."""
import json

from .batch_measurement_world import DAY, stamp


def usage(out, new, read):
    return {"input_tokens": new, "cache_creation_input_tokens": 0, "cache_read_input_tokens": read,
            "output_tokens": out}


def slim_session(session, parent, starts, ends, out, new, read):
    """The slim export's rows of one session (or, with a `parent`, of a subagent it dispatched): its tokens on the
    first row, a closing row at the end."""
    who = {"session": parent or session, "agent": session if parent else None}
    rows = [dict(time=stamp(starts), type="assistant", model="m", usage=usage(out, new, read), **who),
            dict(time=stamp(ends), type="assistant", model="m", usage=usage(0, 0, 0), **who)]
    return "".join(json.dumps(r) + "\n" for r in rows)


def who_of(session, parent):
    return {"session": parent or session, "agent": session if parent else None}


def timed_session(session, parent, times, out, new, read):
    """The slim export's rows of one session, one assistant row at each of `times`; its tokens on the first."""
    rows = [dict(time=stamp(at), type="assistant", model="m", usage=usage(*(out, new, read) if n == 0 else (0, 0, 0)),
                 **who_of(session, parent)) for n, at in enumerate(times)]
    return "".join(json.dumps(r) + "\n" for r in rows)


def counted_session(session, parent, start, messages, requests):
    """The slim export's rows of one session: `messages` assistant rows over `requests` request ids, a second apart."""
    rows = [dict(time="%sT%s:%02d+00:00" % (DAY, start, n), type="assistant", model="m", usage=usage(0, 0, 0),
                 requestId="q%d" % (n % requests), **who_of(session, parent)) for n in range(messages)]
    return "".join(json.dumps(r) + "\n" for r in rows)


def tool_use_rows(session, parent, start, uses):
    """Rows of the request q0 of a session, each holding one tool-use block of the tool named: `uses` maps a tool
    name to its count."""
    names = [name for name, count in uses.items() for _ in range(count)]
    rows = [dict(time="%sT%s:59+00:00" % (DAY, start), type="assistant", model="m", usage=usage(0, 0, 0),
                 requestId="q0", content=[{"type": "tool_use", "id": "%s-t%d" % (session, n), "name": name,
                                           "input": {}}], **who_of(session, parent)) for n, name in enumerate(names)]
    return "".join(json.dumps(r) + "\n" for r in rows)


def compaction_rows(session, parent, start, count):
    """`count` compaction rows of a session."""
    rows = [dict(time="%sT%s:58+00:00" % (DAY, start), type="system", subtype="compact_boundary",
                 **who_of(session, parent)) for _ in range(count)]
    return "".join(json.dumps(r) + "\n" for r in rows)


def store_session(session, messages, requests):
    """Claude Code's own rows of one session in its store: `messages` assistant rows over `requests` request ids."""
    rows = [{"type": "assistant", "timestamp": stamp("10:%02d" % (n % 60)), "sessionId": session,
             "uuid": "u%d" % n, "requestId": "q%d" % (n % requests),
             "message": {"role": "assistant", "model": "m", "usage": usage(5, 1, 10), "content": []}}
            for n in range(messages)]
    return "".join(json.dumps(r) + "\n" for r in rows)


def raw_session(session, starts, ends, prompt, tool):
    """Claude Code's own rows of one session: a prompt, a reply that calls a tool."""
    rows = [
        {"type": "user", "timestamp": stamp(starts), "sessionId": session, "uuid": "u1",
         "message": {"role": "user", "content": prompt}},
        {"type": "assistant", "timestamp": stamp(ends), "sessionId": session, "uuid": "u2", "requestId": "q1",
         "message": {"role": "assistant", "model": "m", "usage": usage(50, 20, 300),
                     "content": [{"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": tool}}]}},
    ]
    return "".join(json.dumps(r) + "\n" for r in rows)
