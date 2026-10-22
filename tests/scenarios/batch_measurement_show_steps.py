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


@when("the session runs measure show for it")
def runs_show(world, measure_run):
    measure_run("initiative", INITIATIVE)
    measure_run("show", world.shown)


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
