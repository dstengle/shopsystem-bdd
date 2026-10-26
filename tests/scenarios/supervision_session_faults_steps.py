"""supervision's steps about a session of a round or of an answer that ends badly, or gives what its stage gives (r87, r88,
r89, r90, r128, r132): the stand-in is told how the session ends and what its result file holds."""
import re

from pytest_bdd import given, parsers

from .conftest import feature
from .supervision_delegation_steps import asked_by_the_log, fulfils_with_delegation
from .supervision_faults_steps import awaiting_with_questions
from .supervision_intake_steps import round_with_question

ENDING = (r"ends in an error|ends at its turn limit|ends with no error and before its turn limit, having written no "
          r"result file")
ENDS = {"ends in an error": {"subtype": "error_during_execution", "num_turns": 7},
        "ends at its turn limit": {"subtype": "error_max_turns", "num_turns": 26},
        "ends with no error and before its turn limit, having written no result file": {"result": "none"}}
SESSION_ENDS = {"ends in an error": ENDS["ends in an error"], "ends at its turn limit": ENDS["ends at its turn limit"],
                "ends with no error and before its turn limit, writing no result file": ENDS[
                    "ends with no error and before its turn limit, having written no result file"]}


def changes(text):
    """The change list of "a change list that adds thing#r4 on thing"."""
    found = {"capability": "thing"}
    for verb, ids in re.findall(r"(adds|changes|removes) (\S+#r\d+(?: and \S+#r\d+)*)", text):
        found[verb] = re.findall(r"\S+#r\d+", ids)
    return [found]


def scenario_commit(ids):
    """The formulate round's stand-in committing features/thing.feature with a scenario tagged for each of `ids`."""
    tagged = [("@r1", "it answers")] + [("@r" + i.split("#r")[1], "it does what %s asks" % i) for i in ids]
    return {"status": "DONE", "commit": {"features/thing.feature": feature("thing", *tagged)}}


def given_by(text, step):
    """The result fields and questions `text` ("the question "Q"", "a change list that ...") says a result holds."""
    asked = re.findall(r'"([^"]+)"', text)
    if text.startswith("the question"):
        step["questions"] = asked
    if "a change list that" in text:
        step["fields"] = {"changes": changes(text)}
    return step


@given(parsers.re(r"the researcher's session ends at its turn limit, its result file giving a file set of "
                  r"(?P<files>\S+) and no question, and every other session gives DONE$"))
def researcher_at_turn_limit(plan, files):
    plan["default"] = {"status": "DONE"}
    plan["code-scout"] = dict(ENDS["ends at its turn limit"], status="DONE", fields={"fileset": [files]})


@given(parsers.re(r"the (?P<kind>gate|apply|integrate) round for (?P<node>p1|i1) (?P<ending>%s)(?:, its result giving "
                  r"(?P<giving>.+?))?(?P<others>, and every other session gives DONE)?$" % ENDING))
def round_ends_badly(plan, kind, node, ending, giving, others):
    if others:
        plan["default"] = {"status": "DONE"}
    plan["round:" + kind] = given_by(giving or "", dict(ENDS[ending], status="DONE"))


@given(parsers.re(r"i1 fulfils the request q1, which gives the delegation \"(?P<delegation>[^\"]+)\", and i1's work-item w1 "
                  r"is awaiting-answer, its ## Questions section with \"(?P<question>[^\"]+)\" and no answer$"))
def delegated_unanswered(repo, context, delegation, question):
    fulfils_with_delegation(repo, context, delegation)
    awaiting_with_questions(repo, "w1", question, None)
    asked_by_the_log(repo)


@given(parsers.re(r"the session answering w1's question \"[^\"]+\" under the delegation (?P<ending>ends in an error), its "
                  r"result file answering \"(?P<answer>[^\"]+)\", and every other session gives DONE$"))
def answering_ends(plan, ending, answer):
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = dict(ENDS[ending], status="DONE", fields={"answer": answer})


@given(parsers.re(r"the (?P<stage>answering session|integrate round|apply round|formulate round|intake round|gate round)'s "
                  r"result gives (?P<what>.+), and every other session gives DONE$"))
def stage_gives(plan, stage, what):
    plan["default"] = {"status": "DONE"}
    asked = re.findall(r'"([^"]+)"', what)
    if stage == "answering session":
        plan["delegation-answerer"] = {"status": "DONE", "fields": {"answer": asked[0]}}
    elif stage == "intake round":
        round_with_question(plan, asked[0])
    elif stage == "gate round":
        plan["round:gate"] = {"status": "DONE", "questions": asked}
    elif stage == "formulate round":     # its scenario is its output: committed when the row gives one, else none
        if "a scenario for" in what:
            plan["round:formulate"] = scenario_commit(re.findall(r"\S+#r\d+", what))
    else:
        plan["round:" + stage.split()[0]] = {"status": "DONE", "fields": {"changes": changes(what)}}
        if stage == "apply round":     # the formulate round that follows it gives the scenario for what it added
            plan["round:formulate"] = scenario_commit(changes(what)[0].get("adds", []))


@given(parsers.re(r"the apply round for p1 ends, and the formulate round's result gives a scenario for thing#r4 and the "
                  r"questions (?P<text>.+), and every other session gives DONE$"))
def formulate_gives_questions(plan, text):
    plan["default"] = {"status": "DONE"}
    plan["round:apply"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", "adds": ["thing#r4"]}]}}
    plan["round:formulate"] = {"status": "DONE", "questions": re.findall(r'"([^"]+)"', text)}


@given(parsers.re(r"the session answering under the delegation (?P<ending>ends in an error|ends with no error and before "
                  r"its turn limit, having written no result file)(?:, its result file answering \"(?P<answer>[^\"]+)\")?"
                  r", and every worker gives DONE$"))
def answering_session_ends(repo, plan, ending, answer):
    asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = dict(ENDS[ending], status="DONE", fields={"answer": answer} if answer else {})


@given(parsers.re(r"the session answering under the delegation writes notes.md beside its brief and (?P<ending>ends in an "
                  r"error|ends at its turn limit|ends with no error and before its turn limit, writing no result file)$"))
def answering_writes_notes(repo, plan, ending):
    asked_by_the_log(repo)
    plan["default"] = {"status": "DONE"}
    plan["delegation-answerer"] = dict(SESSION_ENDS[ending], status="DONE", notes={"notes.md": "what the session found\n"})
