"""supervision's steps about what a worker's result gives (r4, r31, r61, r129 to r133): its stage's output, its
questions and its status, and where the questions and the transitions are seen to go."""
import re

from pytest_bdd import given, parsers, then

from .supervision_tests_steps import THING_FEATURE, THING_STEPS
from .supervision_world import (
    NEEDS_FEATURE,
    ROLES,
    calls,
    commit_all,
    item_text,
    log_lines,
    section,
    write,
)

STAGES = {"researcher": "research", "planner": "plan", "implementer": "implement", "reviewer": "review"}
FILE = r"[\w-]+[./][\w./-]*"


@given(parsers.re(r"the (?P<who>researcher|planner|implementer|reviewer)'s result gives (?P<rest>.+?), and every other "
                  r"(?:worker|session) gives DONE$"))
def result_gives(repo, plan, who, rest):
    """What the stand-in's session of `who` gives: the outcome, the questions, and each part of its stage's output,
    which the stand-in gives unless this says there is none."""
    plan["default"] = {"status": "DONE"}
    step = plan.setdefault(ROLES[who], {})
    status = re.search(r"the outcome (\w+)", rest)
    if status:
        step["status"] = status.group(1)
    asked = re.findall(r'"([^"]+)"', rest)
    if asked:
        step["questions"] = asked
    given_fields = step.setdefault("fields", {})
    files = re.search(r"(?:file set|`fileset`) of (%s(?: and %s)?)" % (FILE, FILE), rest)
    if files:
        given_fields["fileset"] = files.group(1).split(" and ")
    for word, field in (("no file set", "fileset"), ("no plan", "plan"), ("no findings", "findings")):
        if word in rest:
            given_fields[field] = None
    if who == "implementer":
        doing = re.search(r"the implementer (committing .+|writing .+)$", rest)
        if doing and doing.group(1).startswith("writing "):
            step["write"] = {"feature.txt": "the feature\n"}
        else:
            step["commit"] = {"feature.txt": "the feature\n"}
            if "scenarios fail" in rest:
                step["commit"]["scenarios-fail"] = "\n"


@given(parsers.re(r"each implementer's result gives no question, each implementer committing a file named for its "
                  r"work-item once two implementers have started, w2's implementer ending before w1's, and every other "
                  r"worker gives DONE$"))
def implementers_give(repo, plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-implementer"] = {"commit": {"{work_item}.txt": "the feature\n"}, "meet": 2,
                               "hold": {"w1": {"log": str(repo / ".shop/work/i1/log.jsonl"), "work_item": "w2"}}}


@given("each work-item's scenarios and the whole suite pass on its branch")
def suite_passes(repo):
    assert not (repo / "scenarios-fail").exists() and not (repo / "suite-fail").exists()


@given(parsers.re(r'the work-item\'s scenarios pass only where feature.txt is, and the whole suite fails only on "it waits", '
                  r"tagged @r2, while i1's work-item w2, accepting thing#r2, is awaiting-answer$"))
def suite_fails_only_on_expected(repo):
    write(repo, "tests.py", NEEDS_FEATURE)
    write(repo, ".shop/work/i1/w2.md", item_text("w2", "awaiting-answer").replace("thing#r1", "thing#r2"))
    write(repo, "features/thing.feature", THING_FEATURE)
    write(repo, "tests/test_thing.py", THING_STEPS)
    (repo / ".shop/delivery.toml").unlink()
    commit_all(repo, "the scenarios need feature.txt, and the suite fails only on what w2 accepts")


@given(parsers.re(r"the researcher's session (?P<ending>ends in an error|ends at its turn limit|exits with an error|"
                  r"leaves output that holds no JSON result)$"))
def researcher_session_ends(plan, ending):
    ends = {"ends in an error": {"subtype": "error_during_execution", "num_turns": 7},
            "ends at its turn limit": {"subtype": "error_max_turns", "num_turns": 26},
            "exits with an error": {"exit": 1},
            "leaves output that holds no JSON result": {"stdout": "no result here, only words"}}
    plan["code-scout"] = dict(ends[ending], status="DONE")


def end_and_move(repo, who, name, before, after):
    """Whether log.jsonl has `who`'s stage's end and, after it, the transition of `name` (from `before` when given)."""
    lines = log_lines(repo)
    ended = [n for n, l in enumerate(lines) if l.get("work-item") == name and l.get("stage") == STAGES[who]
             and l.get("event") == "end"]
    moved = [n for n, l in enumerate(lines) if l.get("work-item") == name and l.get("after") == after
             and (before is None or l.get("before") == before)]
    return bool(ended and moved and ended[-1] < moved[-1]), lines


@then(parsers.re(r"(?P<name>\w+)'s transition (?:from (?P<before>[\w-]+) )?to (?P<after>[\w-]+) was made once the "
                 r"(?P<who>researcher|planner|implementer|reviewer)(?:'s session)? had ended$"))
def transition_after_end(repo, context, name, before, after, who):
    made, lines = end_and_move(repo, who, name, before, after)
    assert made, (lines, context["done"].stdout, context["done"].stderr)


@then(parsers.re(r"(?P<name>\w+) made no transition to awaiting-answer$"))
def no_transition_to_asking(repo, name):
    assert not [l for l in log_lines(repo) if l.get("work-item") == name and l.get("after") == "awaiting-answer"]


@then(parsers.re(r"(?P<name>\w+)'s ## Questions holds (?P<asked>\"[^\"]+\"(?: and \"[^\"]+\")?)$"))
def work_item_questions_hold(repo, name, asked):
    held = section((repo / (".shop/work/i1/%s.md" % name)).read_text(), "Questions")
    for question in re.findall(r'"([^"]+)"', asked):
        assert question in held, (question, held)


@then(parsers.re(r"(?P<name>\w+)'s ## Questions holds a question naming (?P<missing>.+) as missing$"))
def question_names_missing(repo, name, missing):
    held = section((repo / (".shop/work/i1/%s.md" % name)).read_text(), "Questions")
    assert missing in held and "missing" in held, (missing, held)


@then(parsers.re(r"the planner's brief has the researcher's questions (?P<asked>\"[^\"]+\"(?: and \"[^\"]+\")?)$"))
def planner_brief_has(repo, context, asked):
    briefs = [c["brief"] for c in calls(repo) if c["event"] == "start" and c["agent"].endswith("bdd-planner")]
    assert len(briefs) == 1, (briefs, context["done"].stderr)
    for question in re.findall(r'"([^"]+)"', asked):
        assert "- %s" % question in briefs[0], (question, briefs[0])


@then("`work run` wrote no question naming a missing output")
def no_missing_question(repo):
    for path in (repo / ".shop/work/i1").glob("*.md"):
        assert not re.search(r"\bmissing\b", section(path.read_text(), "Questions")), path.read_text()
