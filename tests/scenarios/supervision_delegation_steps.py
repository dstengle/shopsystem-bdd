"""supervision's steps about the questions `work run` has answered under a request's delegation (r77, r78)."""
import json
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_rounds_steps import DIR
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
    plan["delegation-answerer"] = {"fields": {"answer": ANSWER}} if reply == "answers it" else {}


@given(parsers.re(r'the session answering under the delegation answers "(?P<answer>[^"]+)", and every worker gives DONE$'))
def session_answers(repo, plan, answer):
    asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = {"fields": {"answer": answer}}


@given(parsers.re(r'the session answering under the delegation ends at its turn limit, its result file answering '
                  r'"(?P<answer>[^"]+)", and every worker gives DONE$'))
def session_at_turn_limit(repo, plan, answer):
    asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = {"fields": {"answer": answer}, "subtype": "error_max_turns", "num_turns": 26}


@given("the session answering under the delegation ends in an error, having written notes.md beside its brief")
def session_in_error(repo, plan):
    asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = {"status": "DONE", "subtype": "error_during_execution", "num_turns": 7,
                                   "notes": {"notes.md": "what the session found\n"}}


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
