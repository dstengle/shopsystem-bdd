"""A batch's sessions after plan 7's review (M1, M2, M4, M5, S2 and the rulings' Q2): a subagent described otherwise
than for the batch plans, another batch's description gives no role here, the subagent that drove the batch is its
planning, a session priced nowhere has no cost, a request with no id is counted once, and the summary says when no
main session was counted."""
import datetime
import json

import measure_batch_read
import measure_batch_sessions as S
import measure_batch_show
import measure_cost
import pytest
from measure_batch_testing import FIGURES, store_rows, write_agent, write_session

T0 = datetime.datetime(2026, 11, 5, 10, 0, tzinfo=datetime.UTC)
REVIEW = T0 + datetime.timedelta(hours=1)
WINDOW = (T0, T0 + datetime.timedelta(days=1))
MINUTE = datetime.timedelta(minutes=1)


def one(agent, at, model="claude-opus-5-5", n=1):
    return measure_batch_read.Request("q-%s-%d" % (agent, n), "s", agent, at, model, 1, 0, 0, 0, 1)


def sessions(requests, types, parents=None):
    return S.sessions_of(requests, types, WINDOW, REVIEW, measure_cost.PRICES, batch="batch-1", parents=parents or {})


@pytest.mark.parametrize("kind, role", [
    (("Explore", "Find the parser"), "planning"),              # M1: described, not for the batch
    (("general-purpose", "batch-7 review 3"), "planning"),     # M2: another batch's description
    (("general-purpose", "batch-1 review 3"), "review"),
    ((None, None), "implementing"),                            # no meta: rule 4
])
def test_a_description_gives_a_role_only_for_this_batch(kind, role):
    (found,) = sessions([one("a1", T0 + 10 * MINUTE)], {"a1": kind})
    assert found["role"] == role


def test_the_subagent_that_drove_the_batch_plans():
    """Q2: a subagent whose first request is before the window, the parent of a counted batch subagent, is the
    batch's driver: planning, its requests inside the window counted like a main session's."""
    requests = [one("d", T0 - MINUTE, n=1), one("d", T0 + MINUTE, n=2), one("d", T0 + 3 * MINUTE, n=3),
                one("r", T0 + 2 * MINUTE), one("x", T0 - MINUTE)]
    types = {"d": ("general-purpose", "carry on plan 7"), "r": ("general-purpose", "batch-1 review 1"),
             "x": ("general-purpose", "something else")}
    found = {s["agent"]: s for s in sessions(requests, types, {"r": "d"})}
    assert set(found) == {"d", "r"}
    assert found["d"]["role"] == "planning" and found["d"]["requests"] == 2 and found["d"]["driver"]
    assert found["r"]["role"] == "review" and not found["r"]["driver"]


def test_a_subagent_that_is_its_own_batch_subagents_parent_is_counted_whole():
    """A counted subagent (its first request inside the window) that dispatched another keeps its own role."""
    requests = [one("t", T0 + MINUTE), one("h", T0 + 2 * MINUTE)]
    types = {"t": ("general-purpose", "batch-1 t1 b1"), "h": ("Explore", "find it")}
    found = {s["agent"]: s for s in sessions(requests, types, {"h": "t"})}
    assert found["t"]["role"] == "implementing" and not found["t"]["driver"]


def test_the_parents_are_read_from_the_meta_files(tmp_path):
    write_agent(tmp_path, "m", "r", store_rows("m", ["2026-11-05T10:00:00Z"], agent="r"), "general-purpose", "x")
    meta = tmp_path / "m" / "subagents" / "agent-r.meta.json"
    meta.write_text(json.dumps(dict(json.loads(meta.read_text()), parentAgentId="d")))
    write_agent(tmp_path, "m", "q", store_rows("m", ["2026-11-05T10:00:00Z"], agent="q"), "general-purpose", "y")
    assert measure_batch_read.parents(tmp_path) == {"r": "d"}


def test_a_session_priced_nowhere_has_no_cost():
    """M5: not 0, which reads as free."""
    (found,) = sessions([one(None, T0 + MINUTE, model="claude-new-9")], {})
    assert found["cost"] is None and found["unpriced"] == {"claude-new-9": 1}
    found.pop("unpriced")
    assert S.roles_of([found])["planning"]["cost"] == 0
    shown = measure_batch_show.show(dict(FIGURES, sessions=[found]))
    assert shown.rstrip().splitlines()[-1].rstrip().endswith("| -"), shown


def test_a_request_with_no_id_in_two_files_is_counted_once(tmp_path):
    """M4: the fallback key is the session, the agent and the time, not the file and line."""
    row = {"type": "assistant", "timestamp": "2026-11-05T10:00:00Z", "sessionId": "m",
           "message": {"model": "claude-opus-5-5", "usage": {"input_tokens": 1, "output_tokens": 2}}}
    write_session(tmp_path, "m", json.dumps(row) + "\n")
    write_session(tmp_path / "copy", "m", json.dumps(row) + "\n")
    assert len(measure_batch_read.requests_of(tmp_path)) == 1


def summary_of(sessions_, found=2):
    return measure_batch_show.summary(dict(FIGURES, sessions=sessions_, sessions_found=found))


def test_the_summary_says_when_no_main_session_was_counted():
    """S2: a batch driven from a subagent, or from another directory, measures planning 0; the summary says why."""
    review = dict(FIGURES["sessions"][1])
    text = summary_of([review])
    assert "no main session in the window at /store/projects/-repo" in text and "--sessions" in text, text
    assert "no main session" not in summary_of(FIGURES["sessions"])
    assert "no main session" not in summary_of([dict(review, role="planning", driver=True)])


def test_the_summary_says_when_no_session_was_in_the_window():
    """S2 and implementer's deviation 3: transcripts found, none counted."""
    text = summary_of([])
    assert "no session in the window at /store/projects/-repo" in text, text
    assert "no transcripts" not in text
    assert "no transcripts at" in summary_of([], found=0)
