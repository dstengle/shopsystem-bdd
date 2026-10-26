"""supervision's steps about the rounds `work run` starts for an answered capability-proposal: the apply round and the
formulate round, read from the stand-in's record and from log.jsonl."""
import json
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_world import commit_all, git, log_lines, starts, write

DIR = ".shop/work/i1"


def quoted(text):
    return re.findall(r'"([^"]*)"', text)


ASKED_FROM = {"gate": "drafted", "formulate": "approved"}     # the status a proposal moved from into awaiting-answer


@given(parsers.re(r"i1's capability-proposal p1 is awaiting-answer, (?:its adds naming (?P<adds>.+?), )?its ## Questions "
                  r"section with (?P<asked>.+?),? and its Answers section with (?P<answered>.+)$"))
def answered_proposal(repo, asked, answered, adds=None):
    """The proposal as the person left it; "given by its gate round" or "given by its formulate round" writes the move
    into awaiting-answer that round made, as log.jsonl keeps it."""
    bullets = lambda texts: "".join("- %s\n" % t for t in quoted(texts))
    ids = ", ".join(re.findall(r"\S+#r\d+", adds)) if adds else "thing#r1"
    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\nargues: [thing]\n"
          "adds: [%s]\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n\n## Questions\n\n%s\n## Answers\n\n%s"
          % (full("capability-proposal", "p1"), full("initiative", "i1"), ids, bullets(asked), bullets(answered)))
    by = re.search(r"given by its (gate|formulate) round", asked)
    if by:
        write(repo, DIR + "/log.jsonl", json.dumps({"time": "2026-10-15T00:00:00+00:00", "work-item": "p1",
                                                    "before": ASKED_FROM[by.group(1)], "after": "awaiting-answer", "by": "work run"}) + "\n")
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


@given("the gate round's result gives no question, and every round ends")
def gate_result_no_question(plan):
    plan["initiative-round"] = {"status": "DONE", "questions": []}


@then(parsers.re(r"p1's ## Questions holds (?P<text>\".+)$"))
def questions_hold(repo, text):
    held = ["\n".join(b) for b in bullets((repo / DIR / "p1.md").read_text(), "Questions")]
    asked = [gate_question(text)] if len(quoted(text)) == 4 else quoted(text)     # a gate's reading, or each question as given
    for question in asked:
        assert any(question == " ".join(b.split())[2:] for b in held), (question, held)


@then("p1's ## Questions holds one question, asking for the approval of p1's lines as drafted")
def questions_hold_approval(repo):
    held = [" ".join(" ".join(b).split())[2:] for b in bullets((repo / DIR / "p1.md").read_text(), "Questions")]
    assert len(held) == 1, held
    assert "approv" in held[0].lower() and "p1" in held[0] and "as drafted" in held[0], held


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


@given("the integrate round for i1 gives DONE, and every round ends")
def integrate_gives_done(plan):
    plan["initiative-round"] = {"status": "DONE"}


@then("the initiative branch has a commit of the integrate round's stage directory with i1's change to started")
def integrate_stage_committed(repo, context):
    stage = git(repo, "ls-files", "--", DIR + "/runs/i1").split()
    assert any("-integrate/" in p for p in stage), (stage, context["done"].stderr)
    for commit in git(repo, "log", "--format=%H", "--", DIR + "/runs/i1").split():
        files = git(repo, "show", "--name-only", "--format=", commit).split()
        if any("-integrate/" in f for f in files) and "status: started" in git(repo, "show", commit + ":" + DIR + "/initiative.md"):
            return
    raise AssertionError((git(repo, "log", "--stat", "--format=%H %s"), context["done"].stderr))


def rounds(repo, kind, name="p1"):
    return [c for c in starts(repo) if c["agent"].endswith("initiative-round") and "# %s of %s" % (kind, name) in c["brief"]]


@given(parsers.re(r"i1 is proposed and fulfils the request q1, whose (?P<text>lines? .+)$"))
def proposed_fulfilling(repo, text, status="proposed"):
    outcomes = {}
    for numbers, word in re.findall(r"lines? ([\d ]+?(?: and \d+)?) (?:have |has )?the line outcome (\w+)", text):
        for n in re.findall(r"\d+", numbers):
            outcomes[int(n)] = word
    write(repo, DIR + "/initiative.md", "---\nid: %s\nkind: initiative\nstatus: %s\nfulfils: q1\n---\n" % (full("initiative", "i1"), status))
    write(repo, ".shop/work/requests/q1.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n---\n\n## Lines\n%s\n"
          "## Outcomes\n%s" % (full("request", "q1"), "".join("%d. Line %d text.\n" % (n, n) for n in range(1, 4)),
                               "".join("%d. %s\n" % (n, w) for n, w in sorted(outcomes.items()))))
    commit_all(repo, "i1 is proposed and fulfils q1")


@given("i1 is proposed and fulfils no request")
def proposed_fulfilling_none(repo):
    write(repo, DIR + "/initiative.md", "---\nid: %s\nkind: initiative\nstatus: proposed\n---\n" % full("initiative", "i1"))
    commit_all(repo, "i1 is proposed and fulfils no request")


@given("i1 is proposed and fulfils the request q9, which the queue does not hold")
def proposed_fulfilling_missing(repo):
    write(repo, DIR + "/initiative.md", "---\nid: %s\nkind: initiative\nstatus: proposed\nfulfils: q9\n---\n" % full("initiative", "i1"))
    commit_all(repo, "i1 is proposed and fulfils q9")


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
def second_not_refused(repo, context):
    """Not refused over anything left uncommitted under .shop/work/ (r10), and got as far as starting its round."""
    done = context["done"]
    if rounds(repo, "integrate", "i1"):     # a run that began a round: its second run begins one again (r93, r96)
        assert "not committed" not in done.stderr and len(rounds(repo, "integrate", "i1")) == 2, (
            done.returncode, done.stdout, done.stderr, starts(repo))
    else:
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


@then(parsers.re(r'a round of the kind (?P<kind>apply|formulate) was started for p1, given the answers? (?P<answers>.+)$'))
def apply_started(repo, context, kind, answers):
    found = rounds(repo, kind)
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


@then(parsers.re(r"(?P<name>p1) is (?P<status>drafted)$"))
def proposal_status(repo, context, name, status):
    text = (repo / DIR / (name + ".md")).read_text()
    assert "\nstatus: %s\n" % status in text, (text, context["done"].stdout, context["done"].stderr)


@then("p1's transition to formulated was made once the formulate round had ended")
def formulated_after_formulate(repo, context):
    ended, moved = position(repo, stage="formulate", event="end"), position(repo, after="formulated")
    assert ended is not None and moved is not None and ended < moved, (log_lines(repo), context["done"].stderr)
