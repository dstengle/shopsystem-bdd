"""The repository features/requests.feature's scenarios about who raises and who writes a request build (requests r25, r29 to
r34, r44, r45): one repository, which takes the identity of the role that runs a command in it.

A role's repository is spec/index.md giving the role's context, and, for an asker or the product level, an `## Upstreams`
bullet naming the upstream; the requests the roles keep are the ones in .shop/work/requests/. Nothing is sent between
repositories (the carrier is another work-item's), so what "the upstream keeps" is what this repository keeps.
"""
import re
import shlex

from pytest_bdd import given, parsers, then, when

from .requests_steps import request_rel, sections, write_request
from .requests_write_steps import GOOD, kept
from .work_queue_git_steps import init


def be(repo, name, upstream=None):
    """The repository as `name`'s: its context, and the upstream it asks when it is an asker."""
    init(repo)
    (repo / "spec").mkdir(exist_ok=True)
    bullet = "\n## Upstreams\n\n- bounded-context/%s: ../%s/spec\n" % (upstream, upstream) if upstream else ""
    (repo / "spec" / "index.md").write_text("---\nid: bounded-context/%s\n---\n# %s\n%s" % (name, name, bullet))


def role_of(context, who):
    """(context name, upstream it asks) of `who`: 'the asker ctx-a', 'the product level p1', 'the upstream ctx-u'/'the upstream'."""
    name = who.split()[-1] if who.split()[-1] != "upstream" else context["upstream"]
    return name, (None if who.startswith("the upstream") or name == context["upstream"] else context["upstream"])


def run_as(repo, run, context, who, argv):
    """Run `work <argv>` in the repository of `who`; remember which requests it kept before."""
    be(repo, *role_of(context, who))
    context["before"] = {p.stem for p in kept(repo)}
    context["done"] = run("work", *argv)
    return context["done"]


def new_request(repo, context):
    """The one request the last command kept."""
    new = {p.stem for p in kept(repo)} - context.get("before", set())
    assert len(new) == 1, (new, context.get("done"))
    return new.pop()


@given(parsers.parse("an upstream {name} that keeps no request"))
def named_upstream(repo, context, name):
    context["upstream"] = name
    be(repo, name)


@given(parsers.parse("the asker {name} keeps a request {ident} from its own asker {other}"))
def asker_keeps(repo, context, name, ident, other):
    be(repo, name, context["upstream"])
    write_request(repo, context, ident, other, None, "upstream", "one", [])


@given(parsers.parse("a request {ident} to the upstream {up} from the asker {asker} whose turn is the {side}'s, "
                     "with one line whose line outcome is question"))
def request_to_upstream(repo, context, ident, up, asker, side):
    context["upstream"] = up
    be(repo, asker, None if asker == up else up)
    write_request(repo, context, ident, asker, None, side, "one", ["question"])


@when(parsers.re(r"(?P<who>the asker \S+|the product level \S+|the upstream) runs `work (?P<args>[^`]+)` in its own repository"))
def runs_in_its_own(repo, run, context, who, args):
    run_as(repo, run, context, who, shlex.split(args))


@when(parsers.re(r"(?P<who>the asker|the upstream|ctx-u) runs `work (?P<args>[^`]+)` in (?P<where>the .+'s repository),"
                 r" giving no side"))
def runs_giving_no_side(repo, run, context, who, args, where):
    run_as(repo, run, context, where.removesuffix("'s repository"), shlex.split(args))


@when(parsers.re(r"(?P<who>the asker|ctx-u) answers that question with \"(?P<answer>[^\"]+)\" in (?P<where>the .+'s repository),"
                 r" giving no side"))
def answers_giving_no_side(repo, run, context, who, answer, where):
    run_as(repo, run, context, where.removesuffix("'s repository"), ["reply", "q1", "1", answer])


@when(parsers.re(r"(?P<who>the asker) runs `work (?P<args>[^`]+)` in (?P<where>the asker \S+'s repository)"))
def asker_runs_in(repo, run, context, who, args, where):
    run_as(repo, run, context, where.removesuffix("'s repository"), shlex.split(args))


@then("the upstream keeps one new request, whose status is open and whose turn is the upstream's")
def keeps_one_open(repo, context):
    text = (repo / request_rel(new_request(repo, context))).read_text()
    assert "status: open\n" in text and "turn: upstream\n" in text


@then("the upstream keeps one new request")
def keeps_one(repo, context):
    new_request(repo, context)


@then("its lines are the two lines of lines.md")
def lines_are(repo, context):
    assert sections(repo, new_request(repo, context))["Lines"] == ["%d. %s" % (n, line) for n, line in enumerate(GOOD, 1)]


@then(parsers.re(r"its asker is (?P<asker>\S+)(?: and its (?P<field>origins|job-thread) (?:are|is) (?P<named>.+))?"))
def names_asker(repo, context, asker, field, named):
    text = (repo / request_rel(new_request(repo, context))).read_text()
    assert "asker: %s\n" % asker in text, text
    if field == "origins":
        assert re.search(r"(?m)^source: \[o1, o2\]$", text), text
    elif field:
        assert re.search(r"(?m)^part_of: t1$", text), text


@then(parsers.parse("it names {ident} as the request it is raised for"))
def names_raised_for(repo, context, ident):
    text = (repo / request_rel(new_request(repo, context))).read_text()
    assert re.search(r"(?m)^raised_for: request/\S+/%s$" % re.escape(ident), text), text


@then("work prints that request's id")
def prints_new_id(repo, context):
    assert context["done"].stdout.strip() == new_request(repo, context)


@then("the command is refused because an origin belongs to an internal request")
def refused_origin(context):
    err = context["done"].stderr
    assert "origin" in err and "internal request" in err, context["done"]


@then("the command is refused because the request names neither a request it is raised for nor a job-thread")
def refused_neither(context):
    err = context["done"].stderr
    assert "neither a request it is raised for" in err and "job-thread" in err, context["done"]


@then(parsers.re(r"the command is refused, naming (?P<asker>ctx-\w+)"))
def refused_naming(context, asker):
    assert asker in context["done"].stderr, context["done"]


@then("the command is refused, naming the upstream as the side that writes line outcomes")
def refused_naming_upstream(context):
    err = context["done"].stderr
    assert "ctx-u" in err and "line outcomes" in err, context["done"]


@then(parsers.re(r"(?P<ident>q\d+) holds the answer \"(?P<answer>[^\"]+)\" to the question \"(?P<question>[^\"]+)\""
                 r" as the asker's part"))
def holds_answer_as_askers(repo, ident, answer, question):
    found = sections(repo, ident)
    number = next(e.split(". ", 1)[0] for e in found["Questions"] if e.endswith(": " + question))
    assert "%s. %s" % (number, answer) in found["Answers"]


@then(parsers.re(r"(?P<ident>q\d+) holds the line outcome (?P<word>\w+) of line (?P<n>\d+) as the upstream's part"))
def holds_outcome_as_upstreams(repo, ident, word, n):
    assert "%s. %s" % (n, word) in sections(repo, ident)["Outcomes"]
