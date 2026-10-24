"""measure's reading of records: `show` prints a measurement's figures as tables, `compare` two measurements'
totals side by side with the ratio of the second to the first. Standard library only."""
import json
from pathlib import Path

from measure_read import Refused

TOTALS = (("stages", "stages"), ("sessions", "sessions"), ("output tokens", "output_tokens"),
          ("new input tokens", "new_input_tokens"), ("cache-read tokens", "cache_read_tokens"), ("cost", "cost"),
          ("time", "time"))
STAGES = ("work-item", "stage", "agent", "session", "took", "turns", "output_tokens", "new_input_tokens",
          "cache_read_tokens", "cost")
ITEMS = ("work-item", "transitions", "awaiting_answer", "failed", "commits")
SESSIONS = ("session", "started", "dispatched_by", "output_tokens", "new_input_tokens", "cache_read_tokens",
            "round_trips", "tool_uses", "dispatched", "compactions")


def totals_of(*given):
    """TOTALS, with the turns and round trips rows when a measurement gives them (an older one does not)."""
    extra = (("turns", "turns"), ("round trips", "round_trips"))
    rows = [r for r in extra if any(r[1] in g for g in given)]
    return TOTALS[:2] + tuple(rows) + TOTALS[2:]


def figures_of(path):
    """The figures of the measurement at `path`: the JSON block of its record."""
    where = Path(path)
    if not where.is_file():
        raise Refused("no measurement at %s" % path)
    try:
        return json.loads(where.read_text(encoding="utf-8").split("```json\n", 1)[1].split("\n```", 1)[0])
    except (IndexError, ValueError):
        raise Refused("%s is not a measurement" % path) from None


def cell(value):
    if isinstance(value, float):
        return "%.2f" % value
    if isinstance(value, (list, dict)):
        return str(len(value))
    return "" if value is None else str(value)


def table(head, rows):
    """Rows of cells under a head, columns aligned and separated by ' | '."""
    rows = [[cell(c) for c in row] for row in rows]
    widths = [max([len(str(h))] + [len(r[i]) for r in rows]) for i, h in enumerate(head)]
    line = lambda cells: " | ".join(str(c).ljust(w) for c, w in zip(cells, widths)).rstrip()
    return "\n".join([line(head), "-+-".join("-" * w for w in widths)] + [line(r) for r in rows])


def section(title, head, found):
    keys = [h.replace(" ", "_") for h in head]
    return "%s\n%s\n" % (title, table([h.replace("_", " ") for h in head], [[f.get(k) for k in keys] for f in found]))


def show(path):
    figures = figures_of(path)
    totals = figures.get("totals", {})
    stages = figures.get("stages", [])
    head = STAGES
    if any("round_trips" in s for s in stages):
        head = STAGES[:6] + ("round_trips",) + STAGES[6:]
    out = [section("stages", head, stages),
           section("work-items", ITEMS, figures.get("work_items", [])),
           "totals\n%s\n" % table(["total", "value"], [(n, totals.get(k)) for n, k in totals_of(totals)])]
    if "sessions" in figures:
        out.append(section("sessions", SESSIONS, [written(s) for s in figures["sessions"]]))
    if "request" in figures:
        out.append("request\n%s\n" % table(["request", "origin"], [(figures["request"]["id"], figures["request"]["origin"])]))
    return "\n".join(out)


def written(one):
    """A session entry with its tool uses as 'name count, ...' and its dispatched sessions as 'id, ...'."""
    uses, sent = one.get("tool_uses"), one.get("dispatched")
    return {**one, "tool_uses": None if uses is None else ", ".join("%s %s" % pair for pair in uses.items()),
            "dispatched": None if sent is None else ", ".join(sent)}


def session_totals(figures):
    """The round trips, tool uses (every use of every tool) and compactions over a measurement's sessions."""
    found = figures.get("sessions", [])
    return {"round_trips": sum(s.get("round_trips", 0) for s in found),
            "tool_uses": sum(sum(s.get("tool_uses", {}).values()) for s in found),
            "compactions": sum(s.get("compactions", 0) for s in found)}


def ratio(first, second):
    if not isinstance(first, (int, float)) or not isinstance(second, (int, float)) or not first:
        return "-"
    return "%g" % round(second / first, 2)


def compare(first, second):
    given = figures_of(first), figures_of(second)
    one, two = given[0].get("totals", {}), given[1].get("totals", {})
    rows = []
    for name, key in totals_of(one, two):
        if key == "time":
            key = "time_seconds"
            shown = (one.get("time"), two.get("time"))
        else:
            shown = (cell(one.get(key)), cell(two.get(key)))
        rows.append((name, *shown, ratio(one.get(key), two.get(key))))
    out = table(["total", "a", "b", "ratio"], rows) + "\n"
    if any("sessions" in g for g in given):
        a, b = session_totals(given[0]), session_totals(given[1])
        names = (("round trips", "round_trips"), ("tool uses", "tool_uses"), ("compactions", "compactions"))
        out += "\n" + table(["total", "a", "b", "ratio"],
                            [(n, a[k], b[k], ratio(a[k], b[k])) for n, k in names]) + "\n"
    return out
