"""A batch's measurement read (capability telemetry; workflow simplification plan 7, D8, D12): its summary, the tables
written before the record's JSON block. Standard library only."""
from measure_show import table

TOTALS = (("wall time", "wall_time"), ("session time", "session_time"), ("waiting for merge", "waiting_for_merge"),
          ("output tokens", "output_tokens"), ("new input tokens", "new_input_tokens"),
          ("cache-read tokens", "cache_read_tokens"), ("cost", "cost"))
ROLE_HEAD = ("role", "sessions", "session time", "output tokens", "new input tokens", "cache-read tokens", "cost")


def _duration(seconds):
    import measure_build
    return None if seconds is None else measure_build.duration(seconds)


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
    if not figures.get("sessions_found"):
        out.append("no transcripts at %s\n" % figures.get("sessions_from"))
    return "\n".join(out)
