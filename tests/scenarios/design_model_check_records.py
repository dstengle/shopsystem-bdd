"""design-model-check's Given "a repository in which {case}": a work-item's file name, a record, a decision, a status."""
import re

from pytest_bdd import given, parsers

from .conftest import CONTEXT, full
from .design_model_check_requests import request_text


@given(parsers.parse("a repository in which {case}"))
def malformed_record(world, context, case):
    x = full("design-decision", "x")
    decision = "---\nid: {}\nsummary: {}\ndate: 2026-01-01\nstatus: accepted\n---\n\n## Decision\nWe do it.\n"
    world.good()
    if case.startswith("a work-item in .shop/work/i1/"):
        world.initiative()
        if "i2/w3.md" in case or "i2/w4.md" in case:
            world.initiative("i2")
        names = re.findall(r"\.shop/work/(i\d)/(\S+)\.md", case)
        ids = re.findall(r"id (w\d)", case)
        for n, (initiative, name) in enumerate(names):
            world.work_item(ids[min(n, len(ids) - 1)], initiative, name)
    elif case == "a work directory .shop/work/i1 has the part p1.md with the kind capability-proposal and the status awaiting-answer":
        world.observation()
        world.initiative()
        world.proposal(status="awaiting-answer")
    elif case == "a request in .shop/work/requests/q1.md, of the form `work request` writes, has the status withdrawn":
        world.observation()
        world.write(".shop/work/requests/q1.md", request_text("q1", status="withdrawn"))
    elif case == "a decision under spec/decisions/ has no id":
        world.write("spec/decisions/0001-x.md", "---\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n\n## Decision\nWe do it.\n")
    elif case == "a decision under spec/decisions/ has no ## Decision section":
        world.write("spec/decisions/0001-x.md", "---\nid: %s\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n\nNo section.\n" % x)
    elif case == "a record under .shop/records/ with an id has the kind banana":
        world.write(".shop/records/note.md", "---\nid: %s\nkind: banana\n---\n" % full("review-finding", "n1"))
    elif case == "a frontmatter value is written as a folded block, with >":
        world.write("spec/decisions/0001-x.md", decision.format(x, ">-\n  folded"))
    elif case == "a frontmatter value is written as a literal block, with |":
        world.write("spec/decisions/0001-x.md", decision.format(x, "|\n  literal"))
    else:
        assert case == "a decision and an observation have the same id", case
        world.write("spec/decisions/0001-x.md", decision.format(x, "S"))
        world.write(".shop/records/observations.md", "# Observations\n\n## %s\nabout: %s\n" % (x, CONTEXT))
        context["same_id"] = x
