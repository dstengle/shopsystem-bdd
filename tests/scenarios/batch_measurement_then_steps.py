"""batch-measurement's When and Then steps: the run of `measure initiative`, and what the measurement and the
refusals show. The measurement's figures are read back from its record (World.figures)."""
import shlex

from pytest_bdd import parsers, then, when


@when(parsers.re(r"the session runs measure (?P<command>initiative .*)"))
def runs(world, measure_run, command):
    measure_run(*shlex.split(command.replace("with no --replace", "").replace(" with ", " ")))


@then(parsers.parse("one measurement is written for {name}"))
def one_written(world, name):
    assert world.code == 0, world.err
    assert len(world.written()) == 1 and world.written()[0].endswith("-%s.md" % name), world.written()


@then(parsers.parse("it is at {path}"))
def it_is_at(world, path):
    assert (world.repo / path).is_file(), world.written()


@then("measure initiative refuses because the initiative has no log.jsonl")
def refuses_no_log(world):
    assert world.code != 0 and "log.jsonl" in world.err, world.err


@then("nothing is written")
def nothing_written(world):
    assert world.written() == [], world.written()


@then(parsers.parse("measure refuses, naming {file}"))
def refuses_naming(world, file):
    name = "session.json" if file.startswith("the session.json") else "sessions/s-9.jsonl"
    assert world.code != 0 and name in world.err, world.err


@then("measure initiative refuses because the measurement exists")
def refuses_exists(world):
    assert world.code != 0 and "exists" in world.err, world.err


@then("the measurement is as it was")
def as_it_was(world):
    assert world.existing.read_text() == world.before


@then(parsers.parse("the measurement {path} is written over"))
def written_over(world, path):
    assert world.code == 0, world.err
    assert (world.repo / path).read_text() != world.before


@then(parsers.parse("it gives {count:d} stages"))
def gives_stages(world, count):
    assert world.figures()["totals"]["stages"] == count
    assert len(world.figures()["stages"]) == count


@then("measure exits with an error")
def exits_with_error(world):
    assert world.code not in (0, None)


def stage_of(world, item, stage):
    found = [s for s in world.figures()["stages"] if s["work-item"] == item and s["stage"] == stage]
    assert len(found) == 1, world.figures()["stages"]
    return found[0]


NUMBERS = {"turns": "turns", "output tokens": "output_tokens", "new input tokens": "new_input_tokens",
           "cache-read tokens": "cache_read_tokens"}


@then("the measurement gives the stage")
def gives_stage(world, datatable):
    head, row = datatable
    wanted = dict(zip(head, row))
    got = stage_of(world, wanted["work-item"], wanted["stage"])
    for column, value in wanted.items():
        if column in ("work-item", "stage", "agent", "session", "took"):
            key = {"work-item": "work-item"}.get(column, column)
            assert str(got[key]) == value, (column, got)
        elif column == "cost":
            assert "%.2f" % got["cost"] == value, got
        else:
            assert str(got[NUMBERS[column]]) == value, (column, got)


@then("the measurement gives no time for how long the stage took")
def gives_no_time(world):
    for stage in world.figures()["stages"]:
        assert "took" not in stage and "took_seconds" not in stage, stage


def item_of(world, name):
    found = [w for w in world.figures()["work_items"] if w["work-item"] == name]
    assert len(found) == 1, world.figures()["work_items"]
    return found[0]


@then(parsers.parse("the measurement gives {item} those {count:d} transitions"))
def gives_transitions(world, item, count):
    got = [(t["from"], t["to"]) for t in item_of(world, item)["transitions"]]
    assert got == world.expected and len(got) == count, got


@then(parsers.parse("it gives {item} {awaiting:d} time to awaiting-ruling and {failed:d} time to failed"))
def gives_counts(world, item, awaiting, failed):
    got = item_of(world, item)
    assert (got["awaiting_ruling"], got["failed"]) == (awaiting, failed), got


@then(parsers.parse("it gives {item} the commits {first} and {second}"))
def gives_commits(world, item, first, second):
    subjects = sorted(c["subject"] for c in item_of(world, item)["commits"])
    assert subjects == sorted([first, second]), subjects


@then(parsers.parse("it does not give {item} the commit {commit}"))
def not_commit(world, item, commit):
    assert commit not in [c["subject"] for c in item_of(world, item)["commits"]]


@then("the measurement gives the totals")
def gives_totals(world, datatable):
    wanted = dict(zip(*datatable))
    got = world.figures()["totals"]
    assert str(got["stages"]) == wanted["stages"] and str(got["sessions"]) == wanted["sessions"], got
    for column in ("output tokens", "new input tokens", "cache-read tokens"):
        assert str(got[NUMBERS[column]]) == wanted[column], (column, got)
    assert "%.2f" % got["cost"] == wanted["cost"], got
    assert got["time"] == wanted["time"], got


@then("the measurement gives the sessions")
def gives_sessions(world, datatable):
    got = {s["session"]: s for s in world.figures()["sessions"]}
    wanted = [dict(zip(datatable[0], row)) for row in datatable[1:]]
    assert sorted(got) == sorted(w["session"] for w in wanted), sorted(got)
    for row in wanted:
        for column in ("output tokens", "new input tokens", "cache-read tokens"):
            assert str(got[row["session"]][NUMBERS[column]]) == row[column], (row, got[row["session"]])


@then(parsers.parse("it gives neither {first} nor {second}"))
def gives_neither(world, first, second):
    found = [s["session"] for s in world.figures()["sessions"]]
    assert first not in found and second not in found, found


@then(parsers.re(r'the measurement holds none of "(?P<a>[^"]*)", "(?P<b>[^"]*)" or "(?P<c>[^"]*)"'))
def holds_none(world, a, b, c):
    text = world.record().read_text()
    for content in (a, b, c):
        assert content not in text, content
