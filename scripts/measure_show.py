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
SESSIONS = ("session", "started", "dispatched_by", "output_tokens", "new_input_tokens", "cache_read_tokens")


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
    line = lambda cells: " | ".join(str(c).ljust(w) for c, w in zip(cells, widths)).rstrip()  # noqa: E731
    return "\n".join([line(head), "-+-".join("-" * w for w in widths)] + [line(r) for r in rows])


def section(title, head, found):
    keys = [h.replace(" ", "_") for h in head]
    return "%s\n%s\n" % (title, table([h.replace("_", " ") for h in head], [[f.get(k) for k in keys] for f in found]))


def show(path):
    figures = figures_of(path)
    totals = figures.get("totals", {})
    out = [section("stages", STAGES, figures.get("stages", [])),
           section("work-items", ITEMS, figures.get("work_items", [])),
           "totals\n%s\n" % table(["total", "value"], [(name, totals.get(key)) for name, key in TOTALS])]
    if "sessions" in figures:
        out.append(section("sessions", SESSIONS, figures["sessions"]))
    return "\n".join(out)


def ratio(first, second):
    if not isinstance(first, (int, float)) or not isinstance(second, (int, float)) or not first:
        return "-"
    return "%g" % round(second / first, 2)


def compare(first, second):
    one, two = figures_of(first).get("totals", {}), figures_of(second).get("totals", {})
    rows = []
    for name, key in TOTALS:
        if key == "time":
            key = "time_seconds"
            shown = (one.get("time"), two.get("time"))
        else:
            shown = (cell(one.get(key)), cell(two.get(key)))
        rows.append((name, *shown, ratio(one.get(key), two.get(key))))
    return table(["total", "a", "b", "ratio"], rows) + "\n"
