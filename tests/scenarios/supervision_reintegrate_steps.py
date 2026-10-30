"""supervision's steps about a capability-proposal an apply round sends back to integration (r140-r143, r147, r148): the
apply round that applies nothing, the integrate round `work run` starts for the proposal, what that round is given and what
becomes of the proposal and of the drafts of the round before."""
import json
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_formulate_steps import entry
from .supervision_integrate_steps import DRAFT, DRAFTS
from .supervision_rounds_steps import DIR, position, proposed_fulfilling, quoted, rounds
from .supervision_world import commit_all, git, log_lines, starts, write

FIRST = "# thing\nThe thing as the first integrate round drafted it.\n"
NOTHING = "p1's answers give what its drafts do not hold"


@given(parsers.re(r"i1 is started and fulfils the request q1, whose (?P<text>lines? .+)$"))
def started_and_fulfilling(repo, text):
    proposed_fulfilling(repo, text, "started")


@given(parsers.re(r'i1\'s ledger holds the line "(?P<line>[^"]*)"$'))
def ledger_holds(repo, line):
    write(repo, DIR + "/ledger.md", "- %s\n" % line)
    commit_all(repo, "i1's ledger")


@given(parsers.re(r"the apply round for (?P<name>[pg])1 applies nothing, giving that (?P=name)1's answers give what its drafts do not hold"
                  r"(?:, and no change list)?$"))
def apply_applies_nothing(plan, name):
    plan["round:apply"] = {"status": "DONE", "fields": {"nothing_applied": NOTHING}}


@given(parsers.re(r"i1's capability-proposal p1 is awaiting-answer, written from the change list of i1's integrate round, "
                  r"whose drafts are kept at (?P<path>\S+) with (?P<file>\S+)$"))
def written_from_first_round(repo, path, file):
    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\nargues: [thing]\n"
          "adds: [thing#r4]\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n\n# thing\n\n"
          "The drafts of this proposal are in %s.\n" % (full("capability-proposal", "p1"), full("initiative", "i1"), path))
    write(repo, path + file, FIRST)
    commit_all(repo, "p1 is awaiting-answer, written from i1's first integrate round")


@given(parsers.re(r'(?P<name>[pg]1)\'s ## Questions section holds "(?P<asked>[^"]*)", given by its gate round, and its Answers '
                  r'section "(?P<answered>[^"]*)"$'))
def questions_and_answers(repo, name, asked, answered):
    file = repo / DIR / (name + ".md")
    file.write_text(file.read_text().rstrip("\n") + "\n\n## Questions\n\n- %s\n\n## Answers\n\n- %s\n" % (asked, answered))
    write(repo, DIR + "/log.jsonl", json.dumps({"time": "2026-10-15T00:00:00+00:00", "work-item": name, "before": "drafted",
                                                "after": "awaiting-answer", "by": "work run"}) + "\n")
    commit_all(repo, "%s's questions and answers" % name)


@given(parsers.re(r"i1's capability-proposal p1, for thing, is awaiting-answer, its adds naming thing#r4 and thing#r5, its "
                  r"changes naming thing#r2 and its removes naming thing#r3$"))
def held_with_all_lists(repo):
    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\nargues: [thing]\n"
          "adds: [thing#r4, thing#r5]\nchanges: [thing#r2]\nremoves: [thing#r3]\ndate: 2026-10-15\n---\n\n# thing\n\n"
          "The drafts of this proposal are in old/.\n" % (full("capability-proposal", "p1"), full("initiative", "i1")))
    commit_all(repo, "p1 is awaiting-answer, naming ids in all three lists")


@given(parsers.re(r'i1\'s glossary-proposal g1 is awaiting-answer, its adds naming the term "ledger", its changes the term '
                  r'"shelf" and its removes the term "loan"$'))
def held_glossary(repo):
    write(repo, DIR + "/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: awaiting-answer\nadds: [term/ledger]\n"
          "changes: [term/shelf]\nremoves: [term/loan]\ndate: 2026-10-15\n---\n\n# glossary\n\n"
          "The drafts of this proposal are in old/.\n" % (full("glossary-proposal", "g1"), full("initiative", "i1")))
    commit_all(repo, "g1 is awaiting-answer, naming terms in all three lists")


@given('the integrate round for p1 redrafts thing#r5 and gives DONE with a change list that adds thing#r5 on thing')
def integrate_redrafts_p1(plan):
    plan["round:integrate:p1"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", "adds": ["thing#r5"]}]},
                                  "write": {DRAFTS: DRAFT}}


@given('a round of the kind integrate is started for g1, redrafts the term "ledger" and gives DONE with a change list that adds '
       'the term "ledger" in the glossary')
def integrate_redrafts_g1(plan):
    plan["round:integrate:g1"] = {"status": "DONE", "fields": {"changes": [{"glossary": True, "adds": ["term/ledger"]}]},
                                  "write": {DRAFTS: DRAFT}}


@then(parsers.re(r"p1's adds name thing#r4 and thing#r5, its changes name thing#r2, and its removes name thing#r3$"))
def p1_keeps_lists(repo, context):
    text = (repo / DIR / "p1.md").read_text()
    held = lambda field: re.findall(r"\w+#r\d+", next(l for l in text.splitlines() if l.startswith(field + ":")))     # noqa: E731
    assert (held("adds"), held("changes"), held("removes")) == (["thing#r4", "thing#r5"], ["thing#r2"], ["thing#r3"]), (
        text, context["done"].stderr)


@then(parsers.re(r'g1\'s adds name the term "ledger", its changes the term "shelf", and its removes the term "loan"$'))
def g1_keeps_terms(repo, context):
    assert len(rounds(repo, "integrate", "g1")) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    text = (repo / DIR / "g1.md").read_text()
    held = lambda field: re.findall(r"term/\w+", next(l for l in text.splitlines() if l.startswith(field + ":")))     # noqa: E731
    assert (held("adds"), held("changes"), held("removes")) == (["term/ledger"], ["term/shelf"], ["term/loan"]), (
        text, context["done"].stderr)
    assert not (repo / DIR / "glossary.md").exists()


@given(parsers.re(r"the integrate round for p1 (?P<writes>writes spec/capabilities/thing\.md under its drafts path and )?"
                  r"gives DONE with a change list that (?P<text>.+) on thing$"))
def integrate_for_p1(plan, writes, text):
    plan["round:integrate:p1"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", **entry(text)}]},
                                  **({"write": {DRAFTS: DRAFT}} if writes else {})}


def integrate_brief(repo, context):
    found = rounds(repo, "integrate", "p1")
    assert len(found) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    return found[0]["brief"]


@then(parsers.re(r"a round of the kind integrate was started for (?P<name>[pg]1) after the apply round had ended$"))
def integrate_after_apply(repo, context, name):
    ended, began = position(repo, name, stage="apply", event="end"), position(repo, name, stage="integrate", event="start")
    assert len(rounds(repo, "integrate", name)) == 1, (starts(repo), context["done"].stderr)
    assert ended is not None and began is not None and ended < began, (log_lines(repo), context["done"].stderr)


@then("a round of the kind integrate was started for p1 after the formulate round had ended")
def integrate_after_formulate(repo, context):
    ended, began = position(repo, stage="formulate", event="end"), position(repo, stage="integrate", event="start")
    assert len(rounds(repo, "integrate", "p1")) == 1, (starts(repo), context["done"].stderr)
    assert ended is not None and began is not None and ended < began, (log_lines(repo), context["done"].stderr)


@then(parsers.re(r"no round of the kind formulate was started for (?P<name>[pg]1)$"))
def no_formulate_for_p1(repo, context, name):
    assert rounds(repo, "formulate", name) == [], (starts(repo), context["done"].stderr)


@then("p1 was awaiting-answer when the formulate round for p1 had ended")
def awaiting_when_formulate_ended(repo, context):
    ended = position(repo, stage="formulate", event="end")
    assert ended is not None, (log_lines(repo), context["done"].stderr)
    moved = [l for l in log_lines(repo)[:ended] if l.get("work-item") == "p1" and "after" in l]
    assert not moved or moved[-1]["after"] == "awaiting-answer", moved
    text = (repo / DIR / "p1.md").read_text()
    assert "\nstatus: formulated\n" not in text, text


@then("no transition of p1 was made between the start of the formulate round for p1 and the start of the integrate round for p1")
def no_move_formulate_to_integrate(repo, context):
    began, ran = position(repo, stage="formulate", event="start"), position(repo, stage="integrate", event="start")
    assert began is not None and ran is not None and began < ran, (log_lines(repo), context["done"].stderr)
    between = [l for l in log_lines(repo)[began:ran] if l.get("work-item") == "p1" and "after" in l]
    assert not between, between


@then("no question naming the formulate round's output as missing was written under p1's ## Questions")
def no_missing_formulate_question(repo):
    text = (repo / DIR / "p1.md").read_text()
    held = text.split("\n## Questions\n", 1)[1].split("\n## ", 1)[0]
    assert "formulate round" not in held and "scenario" not in held.replace("Is a shelf one place or a list?", ""), held


@then(parsers.re(r'the integrate round for p1 was given the question "(?P<ask>[^"]*)" with its answer "(?P<answer>[^"]*)"$'))
def integrate_given_answer(repo, context, ask, answer):
    brief = integrate_brief(repo, context)
    assert "Question: %s\n  Answer: %s" % (ask, answer) in brief, brief


@then("it was given i1's ledger")
def integrate_given_ledger(repo, context):
    brief = integrate_brief(repo, context)
    assert "Ledger: %s/ledger.md" % DIR in brief, brief


@then("it was given q1's lines 1 and 3, and not line 2")
def integrate_given_lines(repo, context):
    brief = integrate_brief(repo, context)
    assert "Line 1 text." in brief and "Line 3 text." in brief and "Line 2 text." not in brief, brief


def integrate_span(repo):
    began, ended = position(repo, stage="integrate", event="start"), position(repo, stage="integrate", event="end")
    assert began is not None and ended is not None and began < ended, log_lines(repo)
    return began, ended


@then("p1 was awaiting-answer while the integrate round for p1 ran")
def awaiting_while_it_ran(repo):
    began, _ = integrate_span(repo)
    lines = log_lines(repo)
    moved = [l for l in lines[:began] if l.get("work-item") == "p1" and "after" in l]
    assert moved and moved[-1]["after"] == "awaiting-answer", lines


@then("no transition of p1 was made between the start and the end of the integrate round for p1")
def no_move_while_it_ran(repo):
    began, ended = integrate_span(repo)
    between = [l for l in log_lines(repo)[began:ended] if l.get("work-item") == "p1" and "after" in l]
    assert not between, between


@then("p1's transition to drafted was made once the integrate round for p1 had ended")
def drafted_after_integrate(repo, context):
    ended, moved = position(repo, stage="integrate", event="end"), position(repo, after="drafted")
    assert ended is not None and moved is not None and ended < moved, (log_lines(repo), context["done"].stderr)
    assert len([l for l in log_lines(repo) if l.get("work-item") == "p1" and l.get("after") == "drafted"]) == 1, log_lines(repo)


@then(parsers.re(r"(?P<path>\S+) is as the first integrate round wrote it$"))
def first_drafts_kept(repo, path):
    assert (repo / path).read_text() == FIRST, path


@then("no question naming the apply round's output as missing was written under p1's ## Questions")
def no_missing_apply_question(repo):
    text = (repo / DIR / "p1.md").read_text()
    held = text.split("\n## Questions\n", 1)[1].split("\n## ", 1)[0]
    assert quoted(held) == [] and "change list" not in held, held


@then("i1 has one capability-proposal for thing, and it is p1")
def one_proposal_for_thing(repo, context):
    found = [p.name for p in (repo / DIR).glob("*.md")
             if "kind: capability-proposal" in p.read_text() and re.search(r"^argues: \[thing\]$", p.read_text(), re.M)]
    assert found == ["p1.md"], (found, context["done"].stderr)
