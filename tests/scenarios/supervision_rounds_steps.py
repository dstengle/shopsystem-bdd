"""supervision's steps about the rounds `work run` starts for an answered capability-proposal: the apply round and the
formulate round, read from the stand-in's record and from log.jsonl."""
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_world import commit_all, git, log_lines, starts, write

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


@given(parsers.re(r'the gate round gives the question "(?P<ask>[^"]*)" on p1, and every round ends$'))
def gate_gives_question(plan, ask):
    plan["initiative-round"] = {"status": "DONE", "questions": [ask]}


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


def rounds(repo, kind, name="p1"):
    return [c for c in starts(repo) if c["agent"].endswith("initiative-round") and "# %s of %s" % (kind, name) in c["brief"]]


@given(parsers.re(r"i1 is proposed and fulfils the request q1, whose (?P<text>lines? .+)$"))
def proposed_fulfilling(repo, text):
    outcomes = {}
    for numbers, word in re.findall(r"lines? ([\d ]+?(?: and \d+)?) (?:have |has )?the line outcome (\w+)", text):
        for n in re.findall(r"\d+", numbers):
            outcomes[int(n)] = word
    write(repo, DIR + "/initiative.md", "---\nid: %s\nkind: initiative\nstatus: proposed\nfulfils: q1\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/requests/q1.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n---\n\n## Lines\n%s\n"
          "## Outcomes\n%s" % (full("request", "q1"), "".join("%d. Line %d text.\n" % (n, n) for n in range(1, 4)),
                               "".join("%d. %s\n" % (n, w) for n, w in sorted(outcomes.items()))))
    commit_all(repo, "i1 is proposed and fulfils q1")


@given("i1 is proposed and fulfils no request")
def proposed_fulfilling_none(repo):
    write(repo, DIR + "/initiative.md", "---\nid: %s\nkind: initiative\nstatus: proposed\n---\n" % full("initiative", "i1"))
    commit_all(repo, "i1 is proposed and fulfils no request")


@then("no round of the kind integrate was started for i1")
def no_integrate_started(repo, context):
    assert not rounds(repo, "integrate", "i1"), (starts(repo), context["done"].stdout, context["done"].stderr)


@then("i1 is proposed")
def i1_is_proposed(repo, context):
    text = (repo / DIR / "initiative.md").read_text()
    assert "\nstatus: proposed\n" in text, (text, context["done"].stdout, context["done"].stderr)


@then("no branch is made for a round")
def no_round_branch(repo):
    branches = git(repo, "branch", "--list", "round/*")
    assert not branches.strip(), branches


@then("nothing under .shop/work/ is left uncommitted")
def work_committed(repo):
    left = git(repo, "status", "--porcelain", "--", ".shop/work")
    assert not left.strip(), left


@then("the second `work run` was not refused")
def second_not_refused(context):
    done = context["done"]
    assert done.returncode == 0 and "work:" not in done.stderr, (done.returncode, done.stdout, done.stderr)


@then(parsers.re(r"a round of the kind integrate was started for i1, given q1's lines 1 and 3, and not line 2$"))
def integrate_started(repo, context):
    found = rounds(repo, "integrate", "i1")
    assert len(found) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    brief = found[0]["brief"]
    assert "Line 1 text." in brief and "Line 3 text." in brief and "Line 2 text." not in brief, brief


@then("i1's transition to started was made when the integrate round for i1 was started")
def started_with_round(repo, context):
    moved = [n for n, l in enumerate(log_lines(repo)) if l.get("work-item") == "i1" and l.get("after") == "started"]
    began = [n for n, l in enumerate(log_lines(repo)) if l.get("work-item") == "i1" and l.get("stage") == "integrate"
             and l.get("event") == "start"]
    assert moved and began and moved[0] < began[0], (log_lines(repo), context["done"].stderr)
    assert "status: started" in (repo / DIR / "initiative.md").read_text()


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


@given(parsers.re(r"the gate round's session ends at its turn limit, its result giving the question (?P<text>.+) on p1$"))
def gate_at_turn_limit(plan, text):
    plan["initiative-round"] = {"status": "DONE", "questions": quoted(text), "subtype": "error_max_turns"}


@given(parsers.re(r"the apply round gives BLOCKED, asking (?P<text>.+)$"))
def apply_blocked(plan, text):
    plan["initiative-round"] = {"status": "DONE"}
    plan["round:apply"] = {"status": "BLOCKED", "questions": quoted(text)}


@given("the apply round ends, and the formulate round's session ends with no error and before its turn limit, having "
       "written no result file")
def formulate_without_result(plan):
    plan["initiative-round"] = {"status": "DONE"}
    plan["round:formulate"] = {"result": "none"}


@then(parsers.re(r"(?P<name>p1) is (?P<status>drafted)$"))
def proposal_status(repo, context, name, status):
    text = (repo / DIR / (name + ".md")).read_text()
    assert "\nstatus: %s\n" % status in text, (text, context["done"].stdout, context["done"].stderr)


@then("a round of the kind apply was started for p1")
def apply_was_started(repo, context):
    assert len(rounds(repo, "apply")) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)


@then("log.jsonl gives no transition made after the apply round had ended")
def no_transition_after_apply(repo, context):
    ended = position(repo, stage="apply", event="end")
    assert ended is not None, (log_lines(repo), context["done"].stderr)
    later = [l for l in log_lines(repo)[ended + 1:] if "after" in l]
    assert not later, (later, log_lines(repo), context["done"].stderr)


@then("`work run` names the formulate round of p1 and that it left no result it can read")
def names_formulate_without_result(context):
    err = context["done"].stderr
    assert "formulate round of p1" in err and "no result file" in err, err


@then("p1's transition to formulated was made once the formulate round had ended")
def formulated_after_formulate(repo, context):
    ended, moved = position(repo, stage="formulate", event="end"), position(repo, after="formulated")
    assert ended is not None and moved is not None and ended < moved, (log_lines(repo), context["done"].stderr)
