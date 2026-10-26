"""supervision's Then steps about a session that ended badly or gave what its stage gives (r87, r88, r128, r132, r134):
the fault a node holds and `work run` prints, the transitions after a round, the answers and the request's status."""
import re

from pytest_bdd import parsers, then

from .supervision_delegation_steps import DIR, answers_of
from .supervision_intake_steps import REQUEST, line_one_has_outcome, q1_holds_question
from .supervision_integrate_steps import listed, thing_of
from .supervision_world import git, log_lines, section

SESSION = r"researcher|gate round|apply round|integrate round|answering session"


def node_file(node):
    return "%s/%s" % (DIR, "initiative.md" if node == "i1" else node + ".md")


@then(parsers.re(r"`work run` recorded a fault of (?P<node>\w+): that the (?P<session>%s) (?P<ended>.+)$" % SESSION))
def fault_recorded(repo, context, node, session, ended):
    faults = section((repo / node_file(node)).read_text(), "Faults")
    assert ended in faults, (ended, faults, context["done"].stdout, context["done"].stderr)


@then(parsers.re(r"`work run` prints (?P<node>\w+) with the fault that the (?P<session>%s) (?P<ended>.+)$" % SESSION))
def fault_printed(context, node, session, ended):
    lines = context["done"].stdout.splitlines()
    at = [i for i, l in enumerate(lines) if re.fullmatch(r"\s*%s [\w-]+" % node, l)]
    assert at and any(ended in l for l in lines[at[0] + 1:]), (node, ended, context["done"].stdout)


def first_end(repo, kind, node):
    """The index in log.jsonl of the end of the `kind` stage of `node`, else None."""
    for number, line in enumerate(log_lines(repo)):
        if line.get("work-item") == node and line.get("stage") == kind and line.get("event") == "end":
            return number
    return None


@then(parsers.re(r"no transition of any node was made from the (?P<kind>\w+) round$"))
def no_transition_after_round(repo, context, kind):
    node = "i1" if kind == "integrate" else "p1"
    ended = first_end(repo, kind, node)
    assert ended is not None, (log_lines(repo), context["done"].stderr)
    later = [l for l in log_lines(repo)[ended + 1:] if "after" in l]
    assert not later, (later, context["done"].stderr)


@then(parsers.re(r"a round of the kind (?P<kind>gate|apply|integrate) was started for (?P<node>p1|i1)$"))
def round_started(repo, context, kind, node):
    starts = [l for l in log_lines(repo) if l.get("work-item") == node and l.get("stage") == kind and l.get("event") == "start"]
    assert len(starts) == 1, (log_lines(repo), context["done"].stderr)


@then(parsers.re(r"`work run` names the (?P<kind>\w+) round of (?P<node>\w+) and that it (?P<ended>.+)$"))
def names_round(context, kind, node, ended):
    out = context["done"].stdout + context["done"].stderr
    assert "%s round of %s" % (kind, node) in out and ended in out, out


@then(parsers.re(r"i1 has a drafted capability-proposal for thing, its adds naming thing#r4$"))
def has_thing_proposal(repo, context):
    text = thing_of(repo, "i1")
    assert "\nstatus: drafted\n" in text and listed(text, "adds") == ["thing#r4"], (text, context["done"].stderr)


@then(parsers.re(r'w1\'s answer to "(?P<question>[^"]+)" is "(?P<answer>[^"]+)"$'))
def answer_is(repo, context, question, answer):
    text = (repo / (DIR + "/w1.md")).read_text()
    assert question in section(text, "Questions") and answer in answers_of(repo, "w1"), (text, context["done"].stderr)


@then(parsers.re(r'q1\'s line 1 has that line outcome and its line 2 the question "(?P<question>[^"]+)"$'))
def line_outcome_and_question(repo, context, question):
    line_one_has_outcome(repo, context)
    q1_holds_question(repo, context, question)


@then("q1 is awaiting-asker, as `work turn` set it when the round passed the turn")
def q1_awaiting_asker(repo, context):
    assert "\nstatus: awaiting-asker\n" in (repo / REQUEST).read_text(), (context["done"].stdout, context["done"].stderr)


@then("`work run` made no change to q1's status after the round had ended")
def no_status_change_after_round(repo):
    wrote = git(repo, "log", "--format=%H", "-G", "^status:", "--", REQUEST).split()
    assert len(wrote) == 2, wrote     # the commit that wrote the request, and the round's merge holding what `work turn` wrote
