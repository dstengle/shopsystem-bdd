"""features/work-queue.feature, bound to scripts/work and its library scripts/workqueue.py: every scenario, by `scenarios()`.

A Given writes the initiatives and work-items a scenario names under `repo`/.shop/work/; a When runs `work` once (or
makes one move through the library, as `work run` does) and keeps the files as they were (`context["before"]`); the
Then steps read what it printed and what it left.
"""
import importlib
import shlex
import sys

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from .conftest import INDEX, SCRIPTS, full

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
    write(repo, "spec/index.md", INDEX)
    write(repo, ".shop/work/%s/initiative.md" % ident, "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", ident))


def snapshot(repo):
    return {str(p.relative_to(repo)): p.read_text() for p in (repo / ".shop").rglob("*") if p.is_file()}


def fields(path):
    head = path.read_text().split("---\n")[1]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


# --- Given ----------------------------------------------------------------------------------------------------

@given(parsers.parse("an initiative {ident} under .shop/work/ with no work-item {name}"))
def no_item(repo, ident, name):
    initiative(repo, ident)


@given(parsers.re(r"an initiative (?P<ident>i\d+) under \.shop/work/ whose work-items? (?P<items>.+?)"
                  r"(?: and whose capability-proposal (?P<proposal>\w+) is (?P<pstatus>\w+))?$"))
def with_items(repo, ident, items, proposal, pstatus):
    initiative(repo, ident)
    for pair in items.replace(" and ", ", ").split(", "):
        name, status = pair.split(" is ")
        write(repo, ".shop/work/%s/%s.md" % (ident, name), item_text(name, status, ident))
    if proposal:
        write(repo, ".shop/work/%s/%s.md" % (ident, proposal), item_text(proposal, pstatus, ident, "capability-proposal"))


# --- When -----------------------------------------------------------------------------------------------------

@when(parsers.parse("the agent runs `work {args}`"))
def run_work(repo, run, context, args):
    context["before"] = snapshot(repo)
    context["done"] = run("work", *shlex.split(args))


@when(parsers.parse("the script moves {name} to {status}"))
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

@then(parsers.parse(".shop/work/{initiative}/{name}.md is a drafted work-item {name2}"))
def drafted(repo, initiative, name, name2):
    data = fields(repo / ".shop/work/{}/{}.md".format(initiative, name))
    assert (data.get("id"), data.get("kind"), data.get("status")) == (full("work-item", name2), "work-item", "drafted"), data


@then(parsers.parse("its part_of is {part_of}, its under is {under} and its accepts is {accepts}"))
def given_fields(repo, part_of, under, accepts):
    data = fields(repo / ".shop/work/i1/w1.md")
    assert (data.get("part_of"), data.get("under"), data.get("accepts")) == (part_of, under, "[%s]" % accepts), data


@then(parsers.parse(".shop/work/{initiative}/{name}.md is as it was"))
def as_it_was(repo, context, initiative, name):
    rel = ".shop/work/%s/%s.md" % (initiative, name)
    assert (repo / rel).read_text() == context["before"][rel]
    assert snapshot(repo) == context["before"]


@then("work says the work-item already exists")
def says_exists(context):
    err = context["done"].stderr
    assert "already exists" in err and "Traceback" not in err, err


@then("it exits non-zero")
def exits_non_zero(context):
    assert context["done"].returncode != 0, context["done"]


@then(parsers.parse("work prints {pairs}"))
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
    assert fields(repo / ".shop/work/{}/{}.md".format(initiative, name)).get("status") == status
