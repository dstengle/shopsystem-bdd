"""The batch summary (batches r102, r103, b580): what a batch cost, in dollars and in output, new input and cache-read
tokens, and how long it took (its wall time, its opening, its building, each test run and its review), each figure
under its name. `form` is the batch summary form the batch brief gives the batch's driver to reply with (r103); `of`
the batch summary of measure batch's figures (measure_batch's `figures_of`), which `work batch merged` returns (r102).

The building time runs from the batch's opening (its plan's first commit) to its first review (`-> in-review`), the
review time from there to its last `-> awaiting-merge`; a figure no record gives is written `unknown`."""
import datetime

import measure_cost

FORM = (("cost", "<dollars>"), ("output tokens", "<n>"), ("new input tokens", "<n>"), ("cache-read tokens", "<n>"),
        ("wall time", "<from the batch's opening until now>"),
        ("opening time", "<what work batch start took>"),
        ("building time", "<from the batch's opening to its first review>"),
        ("test runs", "<each run of work batch done and review: its kind, task and duration>"),
        ("review time", "<from its first review to awaiting-merge>"))
NAMES = tuple(name for name, _ in FORM)
UNKNOWN = "unknown"


def form():
    """The batch summary form: each figure of a batch summary under its name, with what it is."""
    return ["- %s: %s" % pair for pair in FORM]


def _between(window, start, end):
    if not window.get(start) or not window.get(end):
        return None
    began, ended = (datetime.datetime.fromisoformat(window[k]) for k in (start, end))
    return measure_cost.duration(round((ended - began).total_seconds()))


def _runs(runs):
    if not runs:
        return "none"
    return "%d: %s" % (len(runs), ", ".join("%s%s %s" % (r.get("kind"), " %s" % r["task"] if r.get("task") else "",
                                                         measure_cost.duration(round(r.get("seconds") or 0)))
                                            for r in runs))


def values(figures):
    """Each figure of the batch summary of measure batch's `figures`, by name, in the form's order."""
    tokens, window = figures.get("tokens", {}), figures.get("window", {})
    cost = figures.get("cost")
    found = {"cost": None if cost is None else "$%.2f" % cost,
             "output tokens": tokens.get("output_tokens"), "new input tokens": tokens.get("new_input_tokens"),
             "cache-read tokens": tokens.get("cache_read_tokens"), "wall time": figures.get("wall_time"),
             "opening time": figures.get("opening_time"),
             "building time": _between(window, "started", "first_review"),
             "test runs": _runs(figures.get("test_runs", [])),
             "review time": _between(window, "first_review", "built")}
    return [(name, UNKNOWN if found[name] is None else found[name]) for name in NAMES]


def of(figures):
    """The batch summary of measure batch's `figures`: each figure under its name, one a line."""
    return ["- %s: %s" % pair for pair in values(figures)]


def merged(root, name):
    """The batch summary `work batch merged` returns of the batch `name` (r102): its heading, then each figure of
    measure batch's figures; when they cannot be read, each figure `unknown` and why after the heading."""
    import measure_batch
    from transcripts import Refused
    try:
        return ["batch summary of %s" % name, *of(measure_batch.figures_of(root, name))]
    except Refused as why:
        return ["batch summary of %s (%s)" % (name, why), *of({})]
