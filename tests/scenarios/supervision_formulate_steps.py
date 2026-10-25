"""supervision's steps about what a formulate round gives a capability-proposal, what an apply round's change list writes
into it (r83, r112, r113, r114), and the gate round that ends badly beside another node (r115)."""
import re

from pytest_bdd import given, parsers, then

from .supervision_rounds_steps import DIR, quoted
from .supervision_world import log_lines


@given("the formulate round for p1 gives DONE with no question")
def formulate_no_question(plan):
    plan["round:formulate"] = {"status": "DONE", "questions": []}


@given(parsers.re(r"the formulate round for p1 gives DONE with the questions (?P<text>.+)$"))
def formulate_questions(plan, text):
    plan["round:formulate"] = {"status": "DONE", "questions": quoted(text)}


@given(parsers.re(r"the apply round for p1 ends, and the formulate round for p1 gives DONE with the question (?P<text>.+)$"))
def apply_ends_formulate_question(plan, text):
    plan["initiative-round"] = {"status": "DONE"}
    plan["round:formulate"] = {"status": "DONE", "questions": quoted(text)}


def entry(text):
    """{"adds": [...], ...} of a phrase such as "adds thing#r4 and changes thing#r2"."""
    found = {}
    for verb, ids in re.findall(r"(adds|changes|removes) (\S+#r\d+(?: and \S+#r\d+)*)", text):
        found[verb] = re.findall(r"\S+#r\d+", ids)
    return found


@given(parsers.re(r"the apply round for p1 gives DONE with a change list that (?P<text>.+) on thing$"))
def apply_change_list(plan, text):
    plan["round:apply"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", **entry(text)}]}}


@given("every other round ends and every worker gives DONE")
def every_other_round_ends(plan):
    plan["default"] = {"status": "DONE"}
    plan["initiative-round"] = {"status": "DONE"}


@given(parsers.re(r"the gate round for p1 (?P<ending>.+), and every worker gives DONE$"))
def gate_ends_badly(plan, ending):
    plan["default"] = {"status": "DONE"}
    if ending.startswith("gives BLOCKED"):
        plan["round:gate"] = {"status": "BLOCKED", "questions": quoted(ending)}
    elif ending == "ends in an error":
        plan["round:gate"] = {"status": "DONE", "subtype": "error_during_execution"}
    elif ending == "ends at its turn limit":
        plan["round:gate"] = {"status": "DONE", "subtype": "error_max_turns"}
    else:
        plan["round:gate"] = {"result": "none"}


@then("p1's transition from approved to awaiting-answer was made once the formulate round had ended")
def awaiting_after_formulate(repo, context):
    lines = log_lines(repo)
    ended = next((n for n, l in enumerate(lines) if l.get("work-item") == "p1" and l.get("stage") == "formulate"
                  and l.get("event") == "end"), None)
    moved = next((n for n, l in enumerate(lines) if l.get("work-item") == "p1" and l.get("before") == "approved"
                  and l.get("after") == "awaiting-answer"), None)
    assert ended is not None and moved is not None and ended < moved, (lines, context["done"].stderr)


@then("p1 is awaiting-answer")
def proposal_awaiting(repo, context):
    text = (repo / DIR / "p1.md").read_text()
    assert "\nstatus: awaiting-answer\n" in text, (text, context["done"].stdout, context["done"].stderr)


@then(parsers.re(r"p1's adds name (?P<adds>.+) and not (?P<gone>\S+), its changes name (?P<changes>\S+), and its removes name nothing$"))
def lists_written(repo, adds, gone, changes):
    text = (repo / DIR / "p1.md").read_text()
    line = lambda field: next(l for l in text.splitlines() if l.startswith(field + ":"))
    assert line("adds") == "adds: [%s]" % adds, text
    assert gone not in line("adds"), text
    assert line("changes") == "changes: [%s]" % changes, text
    assert line("removes") == "removes: []", text
