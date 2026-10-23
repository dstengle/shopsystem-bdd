"""The transcripts batch-measurement's scenarios write: Claude Code's raw rows and the slim export's rows."""
import json

from .batch_measurement_world import stamp


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
