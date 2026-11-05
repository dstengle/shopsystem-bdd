"""The requests of a batch's transcripts (telemetry, plan 7 D2, D4, D6): one request however many rows it is written
in, cache writes by their time to live, a subagent by its agent id and meta file, an unknown shape refused, and the
root's own project directory in Claude Code's store."""
import json

import backlog_testing  # noqa: F401  (the scripts directory on the path)
import measure_batch_read
import pytest
from measure_batch_testing import store_rows, write_agent, write_session
from transcripts import Refused

T0, T1 = "2026-11-05T10:00:00.500Z", "2026-11-05T10:00:01Z"


def test_a_request_in_several_rows_is_counted_once(tmp_path):
    """Review Focus 2."""
    rows = [json.loads(line) for line in store_rows("s", [T1] * 3).splitlines()]
    for row, out, at in zip(rows, (5, 9, 9), (T1, T0, T1)):
        row["message"]["usage"]["output_tokens"] = out
        row["timestamp"] = at
        row["requestId"] = "s-q1"
    write_session(tmp_path, "s", "".join(json.dumps(r) + "\n" for r in rows))
    (one,) = measure_batch_read.requests_of(tmp_path)
    assert one.output_tokens == 9
    assert one.at.isoformat().startswith("2026-11-05T10:00:00.5")


def test_cache_writes_are_read_by_their_time_to_live(tmp_path):
    usage = {"input_tokens": 1, "output_tokens": 1, "cache_creation_input_tokens": 13,
             "cache_creation": {"ephemeral_1h_input_tokens": 13, "ephemeral_5m_input_tokens": 0}}
    write_session(tmp_path, "s", store_rows("s", [T1], usage=usage))
    write_session(tmp_path, "t", store_rows("t", [T1], usage={"output_tokens": 1, "cache_creation_input_tokens": 7}))
    by = {r.session: r for r in measure_batch_read.requests_of(tmp_path)}
    assert by["s"].cache_write_1h_tokens == 13 and by["s"].cache_write_5m_tokens == 0
    assert by["t"].cache_write_5m_tokens == 7 and by["t"].cache_write_1h_tokens == 0
    assert by["s"].new_input_tokens == 14


def test_a_subagent_is_named_by_its_agent_id(tmp_path):
    write_agent(tmp_path, "s", "a1", store_rows("s", [T1], agent="a1"))
    (one,) = measure_batch_read.requests_of(tmp_path)
    assert (one.session, one.agent) == ("s", "a1")


def test_agent_types_are_read_from_meta(tmp_path):
    write_agent(tmp_path, "s", "a1", store_rows("s", [T1], agent="a1"), "shopsystem-bdd:pr-reviewer",
                "batch-1 review 1")
    assert measure_batch_read.agent_types(tmp_path) == {"a1": ("shopsystem-bdd:pr-reviewer", "batch-1 review 1")}
    bad = tmp_path / "s" / "subagents" / "agent-a2.meta.json"
    bad.write_text("[]")
    with pytest.raises(Refused, match="agent-a2.meta.json"):
        measure_batch_read.agent_types(tmp_path)


def test_an_unknown_row_is_refused_naming_it(tmp_path):
    write_session(tmp_path, "s", "not json\n")
    with pytest.raises(Refused, match=r"s\.jsonl:1"):
        measure_batch_read.requests_of(tmp_path)


def test_the_project_directory_of_a_root(monkeypatch):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/s")
    found = measure_batch_read.project_dir("/home/x/re.po/.claude/w")
    assert str(found) == "/s/projects/-home-x-re-po--claude-w"


def test_a_missing_directory_has_no_requests(tmp_path):
    assert measure_batch_read.requests_of(tmp_path / "none") == []
