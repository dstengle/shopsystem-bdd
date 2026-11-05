"""A batch's sessions (capability telemetry; workflow simplification plan 7, D4, D6): the requests of its transcripts
that count inside its window, one entry for each main session and each subagent, with its role, session time, tokens
and cost, and the totals by role. Standard library only."""
import re
from itertools import pairwise

import measure_build
import measure_cost

IDLE = 300
ROLES = ("planning", "implementing", "review", "fixing")
WORDS = (("review", "review"), ("fix", "fixing"), (re.compile(r"t[1-9]\d*$"), "implementing"))


def role_of(agent, kind, started, first_review, batch=None):
    """D6, the first rule that applies: a main session plans; a pr-reviewer reviews; a subagent described
    `<this batch> review|fix|t<k> ...` has that role; one described otherwise (another batch's, or the session's own
    helper) plans (plan 7 review M1, M2); else one with no description started before the first review (or with
    none) implements, and one started after it fixes."""
    if agent is None:
        return "planning"
    agent_type, description = kind
    if agent_type and agent_type.endswith("pr-reviewer"):
        return "review"
    words = (description or "").split()
    if len(words) >= 2 and batch is not None and words[0] == batch:
        for word, role in WORDS:
            if word == words[1] if isinstance(word, str) else word.match(words[1]):
                return role
    if words:
        return "planning"
    return "implementing" if first_review is None or started < first_review else "fixing"


def _second(moment):
    return moment.replace(microsecond=0)


def _inside(moment, window):
    return window[0] <= _second(moment) <= window[1]


def session_time(moments):
    """The sum of the gaps between consecutive moments that are at most IDLE seconds."""
    gaps = [(b - a).total_seconds() for a, b in pairwise(moments)]
    return sum(g for g in gaps if g <= IDLE)


def sessions_of(requests, types, window, first_review, table, batch=None, parents=None):
    """D4's counting: a main session's requests inside the window (both ends inclusive, at the second), a subagent
    whole when its first request is inside it. A subagent that is not counted so but is the parent (`parents`,
    {agent: its parent agent}) of one that is, is the batch's driver: planning, counted like a main session (plan 7
    review Q2). One entry each, in order started, `driver` true for a main session and a driver; each entry's
    `unpriced` is {model: requests} of the requests that have no price, for the caller to gather, and its `cost` is
    None when none of its requests has a price (M5)."""
    groups = {}
    for request in sorted(requests, key=lambda r: r.at):
        groups.setdefault((request.session, request.agent), []).append(request)
    whole = {agent for (_, agent), mine in groups.items() if agent and _inside(mine[0].at, window)}
    drivers = {(parents or {}).get(agent) for agent in whole} - whole - {None}
    found = []
    for (session, agent), mine in groups.items():
        driver = agent is None or agent in drivers
        mine = [r for r in mine if _inside(r.at, window)] if driver else (mine if agent in whole else [])
        if not mine:
            continue
        kind = types.get(agent, (None, None)) if agent else (None, None)
        costs = [(r, measure_cost.cost(r, table)) for r in mine]
        unpriced = {}
        for r, c in costs:
            if c is None:
                unpriced[r.model] = unpriced.get(r.model, 0) + 1
        priced = [c for _, c in costs if c is not None]
        seconds = session_time([r.at for r in mine])
        found.append((mine[0].at, {"session": session, "agent": agent, "agent_type": kind[0],
                      "role": "planning" if driver else role_of(agent, kind, _second(mine[0].at), first_review, batch),
                      "driver": driver,
                      "started": mine[0].at.isoformat(), "requests": len(mine), "session_time_seconds": round(seconds),
                      "output_tokens": sum(r.output_tokens for r in mine),
                      "new_input_tokens": sum(r.new_input_tokens for r in mine),
                      "cache_read_tokens": sum(r.cache_read_tokens for r in mine),
                      "cost": round(sum(priced), 6) if priced else None, "unpriced": unpriced}))
    return [entry for _, entry in sorted(found, key=lambda pair: pair[0])]


def roles_of(sessions):
    """Every role of ROLES, with its sessions, session time, tokens and cost summed (zeros included)."""
    out = {}
    for role in ROLES:
        mine = [s for s in sessions if s["role"] == role]
        seconds = sum(s["session_time_seconds"] for s in mine)
        out[role] = {"sessions": len(mine), "session_time_seconds": seconds,
                     "session_time": measure_build.duration(seconds),
                     **{k: sum(s[k] for s in mine) for k in measure_build.KINDS},
                     "cost": round(sum(s["cost"] or 0 for s in mine), 6)}
    return out
