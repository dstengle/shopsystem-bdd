"""supervision's steps about the questions `work run` has answered under a request's delegation (r77, r78)."""
import json
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_rounds_steps import DIR, apply_did_its_work
from .supervision_world import commit_all, git, section, starts, write

ANSWER = "The delegation covers it."


@given(parsers.re(r'i1 fulfils the request q1, which gives the delegation "(?P<delegation>[^"]+)"$'))
def fulfils_with_delegation(repo, context, delegation):
    context["delegation"] = delegation
    write(repo, DIR + "/initiative.md", "---\nid: %s\nkind: initiative\nstatus: started\nfulfils: q1\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/requests/q1.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n"
          'delegation: "%s"\n---\n\n## Lines\n1. Something.\n' % (full("request", "q1"), delegation))
    commit_all(repo, "i1 fulfils q1, which gives a delegation")


@given(parsers.re(r'i1\'s capability-proposal p1 is awaiting-answer, its ## Questions section with "(?P<question>[^"]+)" and '
                  r"no answer$"))
def unanswered_proposal(repo, question):
    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\nargues: [thing]\n"
          "adds: [thing#r1]\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n\n## Questions\n\n- %s\n"
          % (full("capability-proposal", "p1"), full("initiative", "i1"), question))
    commit_all(repo, "an unanswered capability-proposal")


def asked_by_the_log(repo):
    """The log gives w1's move into awaiting-answer, from drafted, as a work-item that was asked about has."""
    write(repo, DIR + "/log.jsonl", json.dumps({"time": "2026-10-19T10:00:00+00:00", "work-item": "w1", "before": "drafted",
                                                "after": "awaiting-answer", "by": "work run"}) + "\n")
    commit_all(repo, "w1 asked")


@given(parsers.re(r"each session given a question under the delegation (?P<reply>answers it|leaves it for the person), and "
                  r"every round ends and every worker gives DONE$"))
def sessions_reply(repo, plan, reply):
    asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["initiative-round"] = {"status": "DONE"}
    apply_did_its_work(plan)
    plan["delegation-answerer"] = {"fields": {"answer": ANSWER}} if reply == "answers it" else {}


@given(parsers.re(r'i1\'s work-item w1 is awaiting-answer, its ## Questions section with "(?P<one>[^"]+)" and "(?P<two>[^"]+)", '
                  r"each with no answer$"))
def two_unanswered(repo, one, two):
    write(repo, DIR + "/w1.md", "---\nid: %s\nkind: work-item\npart_of: %s\nstatus: awaiting-answer\nunder: thing\n"
          "accepts: [thing#r1]\n---\n\n## Questions\n\n- %s\n- %s\n" % (full("work-item", "w1"), full("initiative", "i1"), one, two))
    commit_all(repo, "a work-item with two unanswered questions")


@given(parsers.re(r'i1\'s work-item w1 is awaiting-answer on its reviewer\'s question "(?P<question>[^"]+)", with no answer$'))
def reviewer_unanswered(repo, question):
    write(repo, DIR + "/w1.md", "---\nid: %s\nkind: work-item\npart_of: %s\nstatus: awaiting-answer\nunder: thing\n"
          "accepts: [thing#r1]\n---\n\n## Questions\n\n- %s\n" % (full("work-item", "w1"), full("initiative", "i1"), question))
    write(repo, DIR + "/log.jsonl", "".join(json.dumps({"time": "2026-10-19T10:0%d:00+00:00" % i, "work-item": "w1", "before": b,
                                                        "after": a, "by": "work run"}) + "\n"
                                            for i, (b, a) in enumerate([("ready", "claimed"), ("claimed", "done"),
                                                                        ("done", "awaiting-answer")])))
    commit_all(repo, "w1 asked by its reviewer")


@given(parsers.re(r'the session answering under the delegation answers "(?P<answer>[^"]+)", an answer that '
                  r"(?P<verdict>asks for a change|accepts the work-item as it is), and every worker gives DONE$"))
def session_answers_with_verdict(repo, plan, answer, verdict):
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = {"fields": {"answer": answer, "verdict": "change" if verdict.startswith("asks") else "accept"}}


@then(parsers.re(r"w1's transition from awaiting-answer to (?P<status>ready|done) was made once the session had answered$"))
def moved_after_answer(repo, context, status):
    moves = [json.loads(l) for l in (repo / (DIR + "/log.jsonl")).read_text().splitlines()]
    asked = max(i for i, m in enumerate(moves) if m.get("after") == "awaiting-answer")
    assert any(m.get("work-item") == "w1" and m.get("before") == "awaiting-answer" and m.get("after") == status
               for m in moves[asked + 1:]), (moves, context["done"].stderr)
    assert answers_of(repo, "w1").strip(), moves


@given(parsers.re(r'the session given "(?P<one>[^"]+)" under the delegation answers "(?P<a1>[^"]+)", the session given '
                  r'"(?P<two>[^"]+)" answers "(?P<a2>[^"]+)", and every round ends and every worker gives DONE$'))
def each_answers(repo, plan, one, a1, two, a2):
    asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["initiative-round"] = {"status": "DONE"}
    plan["question:" + one] = {"fields": {"answer": a1}}
    plan["question:" + two] = {"fields": {"answer": a2}}


@given(parsers.re(r'the session answering under the delegation answers "(?P<answer>[^"]+)", and every worker gives DONE$'))
def session_answers(repo, plan, answer):
    if not (repo / DIR / "log.jsonl").exists():     # a reviewer's question (r120) has its own log
        asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = {"fields": {"answer": answer}}


@given(parsers.re(r'the session answering under the delegation ends at its turn limit, its result file answering '
                  r'"(?P<answer>[^"]+)", and every worker gives DONE$'))
def session_at_turn_limit(repo, plan, answer):
    asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = {"fields": {"answer": answer}, "subtype": "error_max_turns", "num_turns": 26}


@then(parsers.re(r'w1\'s question "(?P<question>[^"]+)" has no answer$'))
def question_unanswered(repo, question):
    text = (repo / (DIR + "/w1.md")).read_text()
    assert question in section(text, "Questions") and not section(text, "Answers").strip(), text


STAGE = DIR + "/runs/w1"


@then("the initiative branch has a commit of the answering session's stage directory, its notes.md included, and of "
      "log.jsonl's lines for that session")
def record_committed(repo, context):
    files = git(repo, "ls-tree", "-r", "--name-only", "HEAD", "--", STAGE).split()
    assert any(f.endswith("-answer/notes.md") for f in files), (files, context["done"].stderr)
    assert any(f.endswith("-answer/brief.md") for f in files), files
    assert "answer" in git(repo, "show", "HEAD:" + DIR + "/log.jsonl")


@then("nothing of that stage directory or of log.jsonl is left uncommitted")
def record_clean(repo):
    assert git(repo, "status", "--porcelain", "--", STAGE, DIR + "/log.jsonl") == ""


def given_to(repo, question):
    found = [c for c in starts(repo) if c["agent"].endswith("delegation-answerer") and question in c["brief"]]
    assert len(found) == 1, (question, starts(repo))
    return found[0]["brief"]


def read_list(brief):
    return re.search(r"^Read \(paths in your worktree\):\n((?:- .*\n)*)", brief, re.MULTILINE).group(1).replace("- ", "").split()


def given_only(repo, context, name, files):
    question = section((repo / (DIR + "/%s.md" % name)).read_text(), "Questions").strip()[2:]
    brief = given_to(repo, question)
    assert read_list(brief) == files.split(" and "), brief
    assert context["delegation"] in brief and ".shop/work/" not in brief.split("Run directory:")[0] and "spec/" not in brief, brief


@then(parsers.re(r'(?P<name>w1|p1)\'s question was given to a session of its own, given the question, the delegation "[^"]+", '
                 r"(?P<files>\S+(?: and \S+)?), and nothing else$"))
def question_given(repo, context, name, files):
    given_only(repo, context, name, files)
    other = "p1" if name == "w1" else "w1"
    brief = given_to(repo, section((repo / (DIR + "/%s.md" % name)).read_text(), "Questions").strip()[2:])
    assert section((repo / (DIR + "/%s.md" % other)).read_text(), "Questions").strip()[2:] not in brief, brief


@then(parsers.re(r'"(?P<question>[^"]+)" was given to (?:a|another) session of its own, given the question, the delegation '
                 r'"[^"]+", (?P<files>\S+(?: and \S+)?), and nothing else$'))
def asked_question_given(repo, context, question, files):
    brief = given_to(repo, question)
    assert read_list(brief) == files.split(" and "), brief
    assert context["delegation"] in brief and ".shop/work/" not in brief.split("Run directory:")[0] and "spec/" not in brief, brief
    for other in re.findall(r'^- (.*)$', section((repo / (DIR + "/w1.md")).read_text(), "Questions"), re.MULTILINE):
        assert other == question or other not in brief, brief


@then(parsers.re(r'the brief of the session answering "(?P<question>[^"]+)" asks it to give in its result whether its answer '
                 r"asks for a change or accepts (?P<name>\w+) as it is$"))
def brief_asks_verdict(repo, context, question, name):
    brief = given_to(repo, question)
    assert "verdict" in brief and "`change`" in brief and "`accept`" in brief, (brief, context["done"].stderr)


def answers_of(repo, name):
    return section((repo / (DIR + "/%s.md" % name)).read_text(), "Answers")


@then("w1's question and p1's question each have the session's answer")
def have_answer(repo, context):
    for name in ("w1", "p1"):
        assert ANSWER in answers_of(repo, name), (name, context["done"].stdout, context["done"].stderr)


@then("w1's question and p1's question have no answer, w1 and p1 awaiting-answer")
def have_none(repo, context):
    for name in ("w1", "p1"):
        text = (repo / (DIR + "/%s.md" % name)).read_text()
        assert not answers_of(repo, name).strip() and "status: awaiting-answer" in text, (name, text)


@then(parsers.re(r'w1\'s answer to "(?P<question>[^"]+)" is "(?P<answer>[^"]+)", naming the delegation "(?P<delegation>[^"]+)"$'))
def answer_names_delegation(repo, context, question, answer, delegation):
    text = (repo / (DIR + "/w1.md")).read_text()
    asked = [l for l in section(text, "Questions").splitlines() if l.strip()]
    at = [i for i, l in enumerate(asked) if question in l]
    assert at, text
    bullets = re.split(r"\n(?=- )", section(text, "Answers").strip())
    assert len(bullets) > at[0], (text, context["done"].stderr)
    first, *rest = bullets[at[0]].splitlines()
    assert first.endswith(": " + answer), bullets
    assert any(delegation in line and line.strip().startswith("by:") for line in rest), bullets
