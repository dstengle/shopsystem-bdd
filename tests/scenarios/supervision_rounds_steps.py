"""supervision's steps about the rounds `work run` starts for an answered capability-proposal: the apply round and the
formulate round, read from the stand-in's record and from log.jsonl."""
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_world import commit_all, log_lines, starts, write

DIR = ".shop/work/i1"


def quoted(text):
    return re.findall(r'"([^"]*)"', text)


@given(parsers.re(r"i1's capability-proposal p1 is awaiting-answer, its ## Questions section with (?P<asked>.+?),? and its "
                  r"Answers section with (?P<answered>.+)$"))
def answered_proposal(repo, asked, answered):
    bullets = lambda texts: "".join("- %s\n" % t for t in quoted(texts))
    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\nargues: [thing]\n"
          "adds: [thing#r1]\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n\n## Questions\n\n%s\n## Answers\n\n%s"
          % (full("capability-proposal", "p1"), full("initiative", "i1"), bullets(asked), bullets(answered)))
    commit_all(repo, "an answered capability-proposal")


@given("i1's capability-proposal p1 is drafted")
def drafted_proposal(repo):
    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: drafted\nargues: [thing]\n"
          "adds: [thing#r1]\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n" % (
              full("capability-proposal", "p1"), full("initiative", "i1")))
    commit_all(repo, "a drafted capability-proposal")


def gate_question(text):
    """The question as one string: the decision, its readings, and the mark on the recommended one."""
    ask, first, second, marked = quoted(text)
    return "%s Readings: %s%s, %s%s" % (ask, first, " (recommended)" if marked == first else "",
                                         second, " (recommended)" if marked == second else "")


@given(parsers.re(r"the gate round's result gives the question (?P<text>.+), and every round ends$"))
def gate_result(plan, text):
    plan["initiative-round"] = {"status": "DONE", "questions": [gate_question(text)]}


@then(parsers.re(r"p1's ## Questions holds (?P<text>.+)$"))
def questions_hold(repo, text):
    held = ["\n".join(b) for b in bullets((repo / DIR / "p1.md").read_text(), "Questions")]
    assert any(gate_question(text) == " ".join(b.split())[2:] for b in held), held


def bullets(text, heading):
    section = text.split("\n## %s\n" % heading, 1)[1].split("\n## ", 1)[0]
    found = []
    for line in section.splitlines():
        if line.startswith("- "):
            found.append([line])
        elif line.strip() and found:
            found[-1].append(line)
    return found


@then("a round of the kind gate was started for p1")
def gate_started(repo, context):
    assert len(rounds(repo, "gate")) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)


@then("the gate round's brief asks for the gate as questions, each a decision with its readings and the recommended "
      "reading marked")
def gate_brief_asks(repo):
    brief = rounds(repo, "gate")[0]["brief"]
    assert "questions" in brief and "readings" in brief and "recommended" in brief, brief


@given("every round ends")
def every_round_ends(plan):
    plan["initiative-round"] = {"status": "DONE"}


@given("every round ends and every worker gives DONE")
def every_round_ends_and_done(plan):
    plan["default"] = {"status": "DONE"}
    plan["initiative-round"] = {"status": "DONE"}


def rounds(repo, kind):
    return [c for c in starts(repo) if c["agent"].endswith("initiative-round") and "# %s of p1" % kind in c["brief"]]


def position(repo, **wanted):
    """The index in log.jsonl of the first line holding every field of `wanted`, else None."""
    for number, line in enumerate(log_lines(repo)):
        if line.get("work-item") == "p1" and all(line.get(k) == v for k, v in wanted.items()):
            return number
    return None


@then(parsers.re(r'a round of the kind apply was started for p1, given the answers (?P<answers>.+)$'))
def apply_started(repo, context, answers):
    found = rounds(repo, "apply")
    assert len(found) == 1, (found, context["done"].stdout, context["done"].stderr)
    for answer in quoted(answers):
        assert "Answer: %s" % answer in found[0]["brief"], (answer, found[0]["brief"])


@then("p1's transition to approved was made once the apply round had ended")
def approved_after_apply(repo, context):
    ended, moved = position(repo, stage="apply", event="end"), position(repo, after="approved")
    assert ended is not None and moved is not None and ended < moved, (log_lines(repo), context["done"].stderr)


@then("a round of the kind formulate was started for p1 after the apply round had ended")
def formulate_after_apply(repo, context):
    ended, began = position(repo, stage="apply", event="end"), position(repo, stage="formulate", event="start")
    assert len(rounds(repo, "formulate")) == 1, (starts(repo), context["done"].stderr)
    assert ended is not None and began is not None and ended < began, (log_lines(repo), context["done"].stderr)


@then("p1's transition to formulated was made once the formulate round had ended")
def formulated_after_formulate(repo, context):
    ended, moved = position(repo, stage="formulate", event="end"), position(repo, after="formulated")
    assert ended is not None and moved is not None and ended < moved, (log_lines(repo), context["done"].stderr)
