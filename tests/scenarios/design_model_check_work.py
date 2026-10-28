"""design-model-check's malformed work directories and work files (r124)."""
import re

from pytest_bdd import given, parsers

from .conftest import I1, THING, cap, full
from .design_model_check_problems import _initiative_with


@given(parsers.parse("a repository with a work directory .shop/work/i1 in which {case}"))
def malformed_work(world, case):
    def part(**changes):
        fm = {"id": full("work-item", "p1"), "kind": "work-item", "part_of": "initiative/i1", "status": "drafted",
              "under": "thing", "check": "true"}
        fm.update(changes)
        world.write(".shop/work/i1/p1.md", "---\n" + "".join("%s: %s\n" % (k, v) for k, v in fm.items() if v is not None) + "---\n")
    world.good()
    if case == "there is no initiative.md":
        part()
        return
    world.initiative()
    typed = re.fullmatch(r"the part p1\.md has the kind ([\w-]+) and the status ([\w-]+)", case)
    item = re.fullmatch(r"the work-item w1\.md with status (\w+) accepts thing#r2, (.*)", case)
    if case == "initiative.md has no id":
        _initiative_with(world, "id: %s\n" % I1, "")
    elif case == "initiative.md has no status":
        _initiative_with(world, "status: started\n", "")
    elif case == "the part p1.md has no id":
        part(id=None)
    elif case == "the part p1.md has the kind banana":
        part(kind="banana")
    elif case == "the part p1.md has no status":
        part(status=None)
    elif typed:
        kind, status = typed.groups()
        part(id=full(kind, "p1"), kind=kind, status=status)
    elif item:
        status, why = item.groups()
        if "guarantees" in why:
            world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
        elif "retired" in why:
            world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], retired="[r2]"))
        world.work_item(status=status, accepts="[thing#r2]")
    elif case == "initiative.md has the priority high":
        _initiative_with(world, "priority: 1", "priority: high")
    else:
        assert case == "initiative.md has a date written 16/10/2026", case
        _initiative_with(world, "date: 2026-10-15", "date: 16/10/2026")
