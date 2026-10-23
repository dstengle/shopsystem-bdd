"""features/work-queue.feature, bound to scripts/work and its library scripts/workqueue.py: every scenario, by `scenarios()`.

A Given writes the initiatives and work-items a scenario names under `repo`/.shop/work/; a When runs `work` once (or
makes one move through the library, as `work run` does) and keeps the files as they were (`context["before"]`); the
Then steps read what it printed and what it left.
"""
import datetime
import errno
import importlib
import json
import os
import re
import shlex
import sys
import types

from pytest_bdd import given, parsers, scenarios, then, when

from .conftest import INDEX, SCRIPTS, full
from .work_queue_add_steps import *
from .work_queue_answer_steps import *
from .work_queue_git_steps import *
from .work_queue_git_steps import init
from .work_queue_withdraw_steps import *

MOVER = "supervision"     # the script that moves work-items in these scenarios

scenarios("work-queue.feature")


def item_text(name, status, initiative="i1", kind="work-item"):
    return "---\nid: %s\nkind: %s\npart_of: initiative/%s\nstatus: %s\n---\n\n# %s\n" % (
        full(kind, name), kind, initiative, status, name)


def write(repo, rel, text):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def initiative(repo, ident):
    init(repo)     # `work add` and `work retry` commit what they change (r9)
    write(repo, "spec/index.md", INDEX)
    write(repo, ".shop/work/%s/initiative.md" % ident, "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", ident))


def snapshot(repo):
    """Every file under the repository, its text read so that a file that is not UTF-8 compares too."""
    return {str(p.relative_to(repo)): p.read_bytes().decode("utf-8", "surrogateescape") for p in repo.rglob("*") if p.is_file()}


def fields(path):
    head = path.read_text().split("---\n")[1]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


# --- Given ----------------------------------------------------------------------------------------------------

@given(parsers.parse("an initiative {ident} under .shop/work/ with no work-item {name}"))
def no_item(repo, ident, name):
    initiative(repo, ident)


@given(parsers.re(r"an initiative (?P<ident>i\d+) under \.shop/work/ whose work-items? (?P<items>(?:(?!, its last).)+?)"
                  r"(?:, its question asked by (?P<asker>an? \w+))?"
                  r"(?: and whose capability-proposal (?P<proposal>\w+) is (?P<pstatus>\w+))?$"))
def with_items(repo, ident, items, asker, proposal, pstatus):
    initiative(repo, ident)
    for pair in items.replace(" and whose work-item ", ", ").replace(" and ", ", ").split(", "):
        name, status = pair.split(" is ")
        write(repo, ".shop/work/%s/%s.md" % (ident, name), item_text(name, status, ident))
        if status == "awaiting-answer":     # the log gives the stage that asked: the status it moved from (r14)
            started = {"a researcher": "drafted", "a planner": "researched", "an implementer": "claimed", "a reviewer": "done"}
            write(repo, ".shop/work/%s/log.jsonl" % ident, log_line(name, started[asker or "an implementer"], status))
        if status == "ready" and not (repo / ".shop/work" / ident / "log.jsonl").exists():
            write(repo, ".shop/work/%s/log.jsonl" % ident, log_line(name, "planned", status))
    if proposal:
        write(repo, ".shop/work/%s/%s.md" % (ident, proposal), item_text(proposal, pstatus, ident, "capability-proposal"))


def log_line(name, before, after):
    return json.dumps({"time": "2026-10-19T10:00:00+00:00", "work-item": name, "before": before, "after": after,
                       "by": "someone"}) + "\n"


@given(parsers.parse(".shop/work/i1/log.jsonl has one line, {name}'s transition from {before} to {after}"))
def one_line(repo, name, before, after):
    write(repo, ".shop/work/i1/log.jsonl", log_line(name, before, after))


@given(parsers.parse(".shop/work/i1/log.jsonl's last line for {name} is its transition to {after}"))
def last_for(repo, name, after):
    write(repo, ".shop/work/i1/log.jsonl", log_line(name, "drafted", "researched") + log_line(name, "researched", after)
          + log_line("w9", "planned", "ready"))


@given(parsers.parse("a repository with spec/index.md and no initiative {ident}"))
def no_initiative(repo, ident):
    write(repo, "spec/index.md", INDEX)


@given(parsers.parse(".shop/work/i1/log.jsonl gives {name}'s last transitions as {moves}"))
def last_moves(repo, name, moves):
    """"to ready, then from ready to claimed, then to failed": each a line; a "to" with no "from" comes from the status
    the line before gave (drafted for the first)."""
    lines, before = [], "drafted"
    for move in moves.split(", then "):
        found = re.match(r"(?:from (\S+) )?to (\S+)$", move)
        before = found.group(1) or before
        lines.append(log_line(name, before, found.group(2)))
        before = found.group(2)
    write(repo, ".shop/work/i1/log.jsonl", "".join(lines))


@given(parsers.parse("an initiative {ident} under .shop/work/ and no spec/index.md"))
def no_index(repo, ident):
    initiative(repo, ident)
    (repo / "spec/index.md").unlink()


@given(parsers.parse("an initiative {ident} under .shop/work/ and a spec/index.md with no id"))
def index_no_id(repo, ident):
    initiative(repo, ident)
    write(repo, "spec/index.md", "---\ntitle: ctx\n---\n# ctx\n")


@given(parsers.parse("an initiative {ident} under .shop/work/ and a spec/index.md whose id is {ident2}"))
def index_short_id(repo, ident, ident2):
    initiative(repo, ident)
    write(repo, "spec/index.md", "---\nid: %s\n---\n# ctx\n" % ident2)


@given(parsers.parse(".shop/work/i1/{name}.md is not UTF-8 text"))
def not_utf8(repo, name):
    (repo / (".shop/work/i1/%s.md" % name)).write_bytes(b"\xff\xfe---\nkind: work-item\n---\n")


@given(parsers.parse("an initiative {ident} under .shop/work/ with a work-item {name} that has no status"))
def no_status(repo, ident, name):
    initiative(repo, ident)
    write(repo, ".shop/work/%s/%s.md" % (ident, name), "---\nid: %s\nkind: work-item\n---\n\n# %s\n" % (full("work-item", name), name))


@given(parsers.parse("an initiative {ident} under .shop/work/ with a work-item {name} that has no frontmatter"))
def no_frontmatter(repo, ident, name):
    initiative(repo, ident)
    write(repo, ".shop/work/%s/%s.md" % (ident, name), "# %s\n\nstatus: drafted\n" % name)


@given(".shop/work/i1/log.jsonl has a line that is not JSON")
def log_not_json(repo):
    write(repo, ".shop/work/i1/log.jsonl", log_line("w1", "drafted", "researched").replace("researched", "drafted", 1)
          + "not json\n")


@given(".shop/work/i1/log.jsonl cannot be written")
def log_cannot_be_written(repo, monkeypatch):
    """The disk fills as the move's line is written: half the line goes in, then ENOSPC. As root as well as not."""
    write(repo, ".shop/work/i1/log.jsonl", "")
    workqueue = importlib.import_module("workqueue") if str(SCRIPTS) in sys.path else (
        sys.path.insert(0, str(SCRIPTS)) or importlib.import_module("workqueue"))

    def full(fd, data):
        os.write(fd, data[: len(data) // 2])
        raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))
    monkeypatch.setattr(workqueue, "os", types.SimpleNamespace(**dict(vars(os), write=full)), raising=False)


# --- When -----------------------------------------------------------------------------------------------------

@when(parsers.parse("the session runs `work {args}`"))
def run_work(repo, run, context, args):
    context["before"] = snapshot(repo)
    context["done"] = run("work", *shlex.split(args))


@when(parsers.parse("the session runs `work {args}` with a newline and `{extra}` in the {option} value"))
def run_work_newline(repo, run, context, args, extra, option):
    argv = shlex.split(args)
    at = argv.index(option) + 1
    argv[at] = argv[at] + "\n" + extra
    context["before"] = snapshot(repo)
    context["done"] = run("work", *argv)


@when(parsers.parse("the script makes {name}'s transition to {status}"))
def move(repo, context, name, status):
    """A move as `work run` makes it: through the library, in-process."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    workqueue = importlib.import_module("workqueue")
    context["before"] = snapshot(repo)
    try:
        workqueue.move(repo, "i1", name, status, by=MOVER)
        context["refused"] = None
    except workqueue.Refused as refused:
        context["refused"] = refused


# --- Then -----------------------------------------------------------------------------------------------------

@then(parsers.re(r"\.shop/work/(?P<initiative>[^/]+)/(?P<name>[^/]+)\.md is a drafted work-item (?P<name2>(?!whose)\S+)$"))
def drafted(repo, initiative, name, name2):
    data = fields(repo / f".shop/work/{initiative}/{name}.md")
    assert (data.get("id"), data.get("kind"), data.get("status")) == (full("work-item", name2), "work-item", "drafted"), data


@then(parsers.parse("its part_of is {part_of}, its under is {under} and its accepts is {accepts}"))
def given_fields(repo, context, part_of, under, accepts):
    data = fields(repo / ".shop/work/i1/{}.md".format(context.get("printed", "w1")))
    assert (data.get("part_of"), data.get("under"), data.get("accepts")) == (part_of, under, "[%s]" % accepts), data


@then("it exits with an error")
def exits_with_error(context):
    assert context["done"].returncode != 0, context["done"]


@then(parsers.re(r"work prints (?P<pairs>(?!one JSON object)\S+ with .+)"))
def prints_statuses(context, pairs):
    out = context["done"].stdout.splitlines()
    assert context["done"].returncode == 0, context["done"]
    for pair in pairs.replace(" and ", ", ").split(", "):
        name, status = pair.split(" with ")
        words = [line.replace("/", " ").split() for line in out]
        assert [w for w in words if name in w and status in w], (name, status, out)


@then(parsers.parse("it prints nothing about {name}"))
def nothing_about(context, name):
    assert name not in context["done"].stdout, context["done"].stdout


@then(parsers.parse(".shop/work/{initiative}/{name}.md gives {name2}'s status as {status}"))
def status_is(repo, initiative, name, name2, status):
    assert fields(repo / f".shop/work/{initiative}/{name}.md").get("status") == status


@then(".shop/work/i1/log.jsonl has two lines, the first as it was")
def two_lines(repo, context):
    lines = (repo / ".shop/work/i1/log.jsonl").read_text().splitlines(keepends=True)
    assert len(lines) == 2 and lines[0] == context["before"][".shop/work/i1/log.jsonl"], lines


@then(parsers.parse("its last line gives the time, {name}, {before} before, {after} after, and the script as who made the transition"))
def last_line(repo, name, before, after):
    last = json.loads((repo / ".shop/work/i1/log.jsonl").read_text().splitlines()[-1])
    when = datetime.datetime.fromisoformat(last.pop("time"))
    assert abs(datetime.datetime.now(datetime.UTC) - when) < datetime.timedelta(minutes=1), when
    assert last == {"work-item": name, "before": before, "after": after, "by": MOVER}, last


@then(parsers.parse("the transition is refused, naming {rel}, {mine} and {logged}"))
def refused(context, rel, mine, logged):
    refusal = context["refused"]
    assert refusal is not None, "the move was made"
    assert all(word in str(refusal) for word in (rel, mine, logged)), str(refusal)


@then(parsers.parse("{first} and {second} are as they were"))
def both_as_they_were(repo, context, first, second):
    for rel in (first, second):
        assert (repo / rel).read_text() == context["before"][rel], rel
    assert snapshot(repo) == context["before"]


@then(parsers.parse("work says that {reason}"))
def says(context, reason):
    err = context["done"].stderr
    assert "Traceback" not in err and reason in err, err


@then("nothing under the repository has changed")
def nothing_changed(repo, context):
    assert snapshot(repo) == context["before"]


@then(parsers.re(r"the transition is refused, naming (?P<rel>[^,]+)$"))
def refused_naming(context, rel):
    refusal = context["refused"]
    assert refusal is not None, "the move was made"
    assert rel in str(refusal), str(refusal)
