"""batch-measurement's steps for `measure show` and `measure compare`: measurements a scenario starts from, the
run of each, and the tables they print."""
import json

from pytest_bdd import given, parsers, then, when

from .batch_measurement_world import INITIATIVE, MEASUREMENTS


def cells(line):
    return [c.strip() for c in line.split("|")]


def rows_of(out):
    """The printed lines that are table rows: their cells."""
    return [cells(line) for line in out.splitlines() if " | " in line]


@given(parsers.parse("the measurement {path} that measure wrote"))
def measure_wrote(world, path):
    world.stage("cart-1", "research", "10:00", "10:12", session="s-1")
    world.session("s-1", "cart-1", "research", 14, 3000, 2000, 50000, 0.42)
    world.shown = path


def wrote(world, path, stage):
    """A measurement record at `path` holding one stage, as an earlier `measure initiative` left it."""
    where = world.repo / path
    where.parent.mkdir(parents=True, exist_ok=True)
    figures = {"stages": [stage], "work_items": [], "totals": {"stages": 1, "sessions": 1}}
    where.write_text("# Measurement\n\n```json\n%s\n```\n" % json.dumps(figures))
    world.shown = path


@given(parsers.parse("the measurement {path} that measure wrote, giving work-item cart-1's research stage {turns:d} "
                     "turns and {trips:d} round trips"))
def measure_wrote_trips(world, path, turns, trips):
    wrote(world, path, {"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1",
                        "turns": turns, "round_trips": trips})


@given(parsers.parse("the measurement {path} that measure wrote, giving no round trips"))
def measure_wrote_no_trips(world, path):
    wrote(world, path, {"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1",
                        "turns": 14})


@when("the session runs measure show for it")
def runs_show(world, measure_run):
    if world.has_log:
        measure_run("initiative", INITIATIVE)
    measure_run("show", world.shown)


def stage_rows(out):
    """The printed stage table: its head and its rows, each a dict by column."""
    rows = rows_of(out)
    head = next(r for r in rows if r[:2] == ["work-item", "stage"])
    after = rows[rows.index(head) + 1:]
    return head, [dict(zip(head, r)) for r in after if len(r) == len(head)]


@then(parsers.parse("the printed stage of cart-1's research shows"))
def printed_stage_shows(world, datatable):
    _, stages = stage_rows(world.out)
    (got,) = [s for s in stages if s["work-item"] == "cart-1" and s["stage"] == "research"]
    for column, value in zip(*datatable):
        assert got[column] == value, (column, got)


@then("the stages are printed")
def stages_printed(world):
    assert world.code == 0, world.err
    _, stages = stage_rows(world.out)
    assert [s["work-item"] for s in stages] == ["cart-1"], world.out


@then("no round trips are printed")
def no_round_trips_printed(world):
    assert "round trips" not in world.out, world.out


def measurement(world, name, initiative, stages, output, cost):
    path = world.repo / MEASUREMENTS / ("%s.md" % name)
    path.parent.mkdir(parents=True, exist_ok=True)
    totals = {"stages": stages, "sessions": stages, "output_tokens": output, "new_input_tokens": 0,
              "cache_read_tokens": 0, "cost": float(cost), "time_seconds": 0, "time": "0 seconds"}
    path.write_text("# Measurement of %s\n\n```json\n%s\n```\n" % (
        initiative, json.dumps({"initiative": initiative, "stages": [], "work_items": [], "totals": totals})))
    return str(path.relative_to(world.repo))


@given(parsers.parse("the measurement {name} for {initiative}, whose totals are {stages:d} stages, {output:d} "
                     "output tokens and a cost of {cost}"))
def measurement_with_totals(world, name, initiative, stages, output, cost):
    world.named[name] = measurement(world, name, initiative, stages, output, cost)


@when("the session runs measure compare for a and b")
def runs_compare(world, measure_run):
    measure_run("compare", world.named["a"], world.named["b"])


@then("the measurement's figures are printed as tables")
def printed_as_tables(world):
    assert world.code == 0, world.err
    rows = rows_of(world.out)
    for head in (["work-item", "stage", "agent", "session"], ["total", "value"]):
        assert any(r[:len(head)] == head for r in rows), (head, world.out)
    assert any(r[:2] == ["cart-1", "research"] for r in rows), world.out
    assert any(r[0] == "output tokens" and r[1] == "3000" for r in rows), world.out


@then("the totals are printed side by side")
def totals_side_by_side(world, datatable):
    assert world.code == 0, world.err
    printed = rows_of(world.out)
    for wanted in datatable[1:]:
        assert list(wanted) in printed, (wanted, world.out)
