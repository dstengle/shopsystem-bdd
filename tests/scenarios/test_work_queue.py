"""features/work-queue.feature, bound to scripts/work and its library scripts/workqueue.py: every scenario, by `scenarios()`.

A Given writes the initiatives and work-items a scenario names under `repo`/.shop/work/; a When runs `work` once (or
makes one move through the library, as `work run` does) and keeps the files as they were (`context["before"]`); the
Then steps read what it printed and what it left.
"""
import shlex

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from .conftest import INDEX, full

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

@given("an initiative i1 under .shop/work/ with no work-item w1")
def no_w1(repo):
    initiative(repo, "i1")


# --- When -----------------------------------------------------------------------------------------------------

@when(parsers.parse("the agent runs `work {args}`"))
def run_work(repo, run, context, args):
    context["before"] = snapshot(repo)
    context["done"] = run("work", *shlex.split(args))


# --- Then -----------------------------------------------------------------------------------------------------

@then(parsers.parse(".shop/work/{initiative}/{name}.md is a drafted work-item {name2}"))
def drafted(repo, initiative, name, name2):
    data = fields(repo / ".shop/work/{}/{}.md".format(initiative, name))
    assert (data.get("id"), data.get("kind"), data.get("status")) == (full("work-item", name2), "work-item", "drafted"), data


@then(parsers.parse("its part_of is {part_of}, its under is {under} and its accepts is {accepts}"))
def given_fields(repo, part_of, under, accepts):
    data = fields(repo / ".shop/work/i1/w1.md")
    assert (data.get("part_of"), data.get("under"), data.get("accepts")) == (part_of, under, "[%s]" % accepts), data
