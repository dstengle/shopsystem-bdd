"""The transcripts of a batch's sessions (capability telemetry; workflow simplification plan 7, D2, D4, D6): each
distinct request of every transcript under a directory with its model and tokens, each subagent's type and
description from its meta file, and the root's own project directory in Claude Code's store. Rows are read through
measure_read, so a shape not known is refused, naming the file and line (0018). No message text is read. Standard
library only."""
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from measure_read import Refused, assistant_rows, moment, request_key, store_dir

WRITES = ("cache_write_5m_tokens", "cache_write_1h_tokens")


@dataclass
class Request:
    key: object
    session: str
    agent: str | None
    at: datetime
    model: str | None
    input_tokens: int
    cache_write_5m_tokens: int
    cache_write_1h_tokens: int
    cache_read_tokens: int
    output_tokens: int

    @property
    def new_input_tokens(self):
        return self.input_tokens + self.cache_write_5m_tokens + self.cache_write_1h_tokens


def _tokens(usage):
    """(input, 5 min write, 1 h write, cache read, output) of a usage: the writes by their time to live, a write with
    no breakdown priced as 5 min."""
    split = usage.get("cache_creation")
    if isinstance(split, dict):
        five, hour = split.get("ephemeral_5m_input_tokens", 0) or 0, split.get("ephemeral_1h_input_tokens", 0) or 0
    else:
        five, hour = usage.get("cache_creation_input_tokens", 0) or 0, 0
    return (usage.get("input_tokens", 0) or 0, five, hour, usage.get("cache_read_input_tokens", 0) or 0,
            usage["output_tokens"])


def requests_of(directory):
    """Every distinct request of every `*.jsonl` under `directory`, by time: a request written in several rows counted
    once (across files too), each token field the maximum over its rows, its time the earliest. A missing directory gives []."""
    found = {}
    if not Path(directory).is_dir():
        return []
    for path in sorted(Path(directory).rglob("*.jsonl")):
        for number_, row, message, usage, stamp, who in assistant_rows(path):
            agent = row.get("agentId", row.get("agent")) or None
            key = request_key(row, message, path, number_)
            if isinstance(key, tuple):
                key = (who, agent, stamp)   # no id: the same row in two files is one request (plan 7 review M4)
            at, tokens = moment(stamp, path), _tokens(usage)
            old = found.get(key)
            if old:
                tokens = tuple(max(a, b) for a, b in zip(tokens, (
                    old.input_tokens, old.cache_write_5m_tokens, old.cache_write_1h_tokens, old.cache_read_tokens,
                    old.output_tokens)))
                at = min(at, old.at)
            found[key] = Request(key, who, agent, at,
                                 message.get("model") or (old.model if old else None), *tokens)
    return sorted(found.values(), key=lambda r: r.at)


def _metas(directory):
    """(agent id, meta) of each `agent-<id>.meta.json` under `directory`; a meta file that is not a JSON object is
    refused, naming it."""
    if not Path(directory).is_dir():
        return
    for path in sorted(Path(directory).rglob("agent-*.meta.json")):
        try:
            meta = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            meta = None
        if not isinstance(meta, dict):
            raise Refused("%s is not a JSON object; the shape of %s is not known" % (path, path.name))
        yield path.name[len("agent-"):-len(".meta.json")], meta


def _text(value):
    return value if isinstance(value, str) else None


def agent_types(directory):
    """{agent id: (agentType, description)} of each subagent's meta file under `directory`."""
    return {agent: (_text(meta.get("agentType")), _text(meta.get("description"))) for agent, meta in _metas(directory)}


def parents(directory):
    """{agent id: the agent id that dispatched it} of each subagent's meta file under `directory` that names one
    (`parentAgentId`)."""
    return {agent: meta["parentAgentId"] for agent, meta in _metas(directory) if _text(meta.get("parentAgentId"))}


def project_dir(root):
    """Claude Code's directory of the sessions started in `root`: the store's projects/ and the resolved root with
    every character that is not a letter or a digit written `-`."""
    return store_dir() / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(Path(root).resolve()))
