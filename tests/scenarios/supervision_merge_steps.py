"""supervision's steps about an integrate round whose change list names another capability the initiative holds a
capability-proposal for (r187): that proposal, the change list on two capabilities, and the lists read back."""
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_formulate_steps import entry
from .supervision_rounds_steps import DIR
from .supervision_world import commit_all, write


def names(text):
    return re.findall(r"[\w-]+#r\d+", text)


@given(parsers.re(r"i1's capability-proposal p2, for (?P<cap>\w+), is awaiting-answer, its adds naming (?P<adds>\S+), "
                  r"its changes naming (?P<changes>\S+) and its removes naming nothing$"))
def other_proposal(repo, cap, adds, changes):
    write(repo, DIR + "/p2.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\nargues: [%s]\n"
          "adds: [%s]\nchanges: [%s]\nremoves: []\ndate: 2026-10-15\n---\n\n# %s\n" % (
              full("capability-proposal", "p2"), full("initiative", "i1"), cap, adds, changes, cap))
    write(repo, "spec/capabilities/%s.md" % cap, "# %s\n" % cap)     # the capability exists, or the round's list naming it is refused (r107)
    commit_all(repo, "p2 is awaiting-answer")


@given(parsers.re(r"the integrate round for p1 gives DONE with a change list that (?P<first>.+) on thing, and "
                  r"(?P<second>.+) on other$"))
def integrate_on_two(plan, first, second):
    plan["round:integrate:p1"] = {"status": "DONE", "fields": {"changes": [
        {"capability": "thing", **entry(first)}, {"capability": "other", **entry(second)}]}}


@then(parsers.re(r"p2's adds name (?P<adds>.+), its changes name (?P<changes>.+), and its removes name (?P<removes>\S+)$"))
def p2_lists(repo, context, adds, changes, removes):
    text = (repo / DIR / "p2.md").read_text()
    held = lambda field: set(names(next(l for l in text.splitlines() if l.startswith(field + ":"))))
    assert (held("adds"), held("changes"), held("removes")) == (set(names(adds)), set(names(changes)), set(names(removes))), (
        text, context["done"].stderr)
