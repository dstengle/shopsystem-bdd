"""A batch's measurement read (capability telemetry; workflow simplification plan 7, D8, D12): its summary, the tables
written before the record's JSON block; `show` with its sessions; `compare` of two batches side by side with the
ratio of the second to the first; and a batch's name resolved to its newest measurement. Standard library only."""
import re
from pathlib import Path

import measure_write
from measure_show import cell, ratio, table
from transcripts import Refused

TOTALS = (("wall time", "wall_time"), ("session time", "session_time"), ("waiting for merge", "waiting_for_merge"),
          ("output tokens", "output_tokens"), ("new input tokens", "new_input_tokens"),
          ("cache-read tokens", "cache_read_tokens"), ("cost", "cost"))
SESSION_HEAD = ("session", "agent type", "role", "started", "requests", "session time", "output tokens",
                "new input tokens", "cache-read tokens", "cost")
COMPARED = ("tokens", "cost", "defects", "findings_by_grade", "knobs")
ROLE_HEAD = ("role", "sessions", "session time", "output tokens", "new input tokens", "cache-read tokens", "cost")


def _duration(seconds):
    import measure_cost
    return None if seconds is None else measure_cost.duration(seconds)


def _totals(figures):
    values = dict(figures.get("tokens", {}), wall_time=figures.get("wall_time"),
                  session_time=figures.get("session_time"),
                  waiting_for_merge=_duration(figures.get("waiting_for_merge_seconds")), cost=figures.get("cost"))
    return table(["total", "value"], [(name, values.get(key)) for name, key in TOTALS])


def summary(figures):
    """The totals, the cost by role, the review findings by grade, the defects and the knobs, as tables; then what
    the totals leave out (unpriced requests) or that no transcript was found."""
    roles = figures.get("cost_by_role", {})
    defects = figures.get("defects", {})
    review, after = defects.get("review", {}), defects.get("after_merge", {})
    out = ["totals\n%s\n" % _totals(figures),
           "cost by role\n%s\n" % table(list(ROLE_HEAD), [
               (role, r["sessions"], r["session_time"], r["output_tokens"], r["new_input_tokens"],
                r["cache_read_tokens"], r["cost"]) for role, r in roles.items()]),
           "review findings by grade\n%s\n" % table(["grade", "findings"], list(figures.get("findings_by_grade",
                                                                                        {}).items())),
           "defects\n%s\n" % table(["item", "review", "after merge"], [
               (item, review.get(item, 0), after.get(item, 0)) for item in sorted(set(review) | set(after))]
               + [("per item", defects.get("per_item"), "")]),
           "knobs\n%s\n" % table(["knob", "value"], list(figures.get("knobs", {}).items()))]
    if figures.get("unpriced"):
        out.append("unpriced (left out of the cost, prices as of %s): %s\n" % (figures.get("prices_as_of"), ", ".join(
            "%s %d request%s" % (m, n, "" if n == 1 else "s") for m, n in figures["unpriced"].items())))
    where, sessions = figures.get("sessions_from"), figures.get("sessions", [])
    if not figures.get("sessions_found"):
        out.append("no transcripts at %s\n" % where)
    elif not sessions:
        out.append("no session in the window at %s; a batch driven from another directory needs --sessions <the main "
                   "session's directory>\n" % where)
    elif not any(s.get("driver") or not s.get("agent") for s in sessions):
        out.append("no main session in the window at %s: a batch driven from a subagent or from another directory "
                   "needs --sessions <the main session's directory>\n" % where)
    return "\n".join(out)


def is_batch(figures):
    return isinstance(figures, dict) and "batch" in figures and "cost_by_role" in figures


def resolve(root, word):
    """The record `word` names: for `batch-<n>`, its newest measurement (by name, which is by date); else the path."""
    if not re.fullmatch(r"batch-[1-9]\d*", word):
        return Path(word)
    folder = Path(root) / measure_write.DIRECTORY
    found = sorted(p for p in folder.glob("*-%s.md" % word) if re.fullmatch(r"\d{4}-\d{2}-\d{2}-%s\.md" % word, p.name))
    if not found:
        raise Refused("no measurement of %s in %s/; run measure batch %s" % (word, measure_write.DIRECTORY.as_posix(),
                                                                            word))
    return found[-1]


def show(figures):
    """The summary and the sessions table."""
    rows = [(s["session"] if not s.get("agent") else "%s/%s" % (s["session"], s["agent"]), s.get("agent_type"),
             s["role"], s.get("started"), s.get("requests"), _duration(s.get("session_time_seconds")),
             s.get("output_tokens"), s.get("new_input_tokens"), s.get("cache_read_tokens"),
             "-" if s.get("cost") is None else s["cost"])
            for s in figures.get("sessions", [])]
    return "%s\nsessions\n%s\n" % (summary(figures), table(list(SESSION_HEAD), rows))


def _rows(figures):
    """(name, shown, value the ratio is of) of each row of `compare`, the sizes (knobs) last (plan 7 review M7)."""
    tokens, defects = figures.get("tokens", {}), figures.get("defects", {})
    out = [("wall time", figures.get("wall_time"), figures.get("wall_time_seconds")),
           ("session time", figures.get("session_time"), figures.get("session_time_seconds"))]
    out += [(name, tokens.get(key), tokens.get(key)) for name, key in TOTALS[3:6]]
    out += [("cost", figures.get("cost"), figures.get("cost")),
            ("defects per item", defects.get("per_item"), defects.get("per_item"))]
    out += [("%s cost" % role, r.get("cost"), r.get("cost")) for role, r in figures.get("cost_by_role", {}).items()]
    out += [("%s findings" % grade, n, n) for grade, n in figures.get("findings_by_grade", {}).items()]
    knobs = figures.get("knobs", {})
    sizes = (("items", "items"), ("changed lines", "changed_lines"), ("reviews", "reviews"))
    out += [(name, knobs.get(key), knobs.get(key)) for name, key in sizes]
    return out


def compare(a_name, a, b_name, b):
    """Two batches' totals, costs by role, findings by grade and sizes side by side, with the ratio of b to a; a batch's
    record without a figure of COMPARED is refused, naming it (plan 7 review M6)."""
    for name, figures in ((a_name, a), (b_name, b)):
        missing = [key for key in COMPARED if key not in figures]
        if missing:
            raise Refused("%s's measurement has no %s; measure it again with measure batch %s --replace" % (
                name, ", ".join(missing), name))
    second = {name: (shown, value) for name, shown, value in _rows(b)}
    rows = [(name, cell(shown), cell(second.get(name, (None, None))[0]), ratio(value, second.get(name, (None, None))[1]))
            for name, shown, value in _rows(a)]
    return table(["total", a_name, b_name, "ratio"], rows) + "\n"
