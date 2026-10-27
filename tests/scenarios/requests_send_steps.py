"""features/requests.feature's steps about what an asker sends an upstream and what the upstream takes in (requests r28, r30
to r34, r39, r41 to r44): the repositories are built by requests_world_steps; a When runs `work` in one of them."""
import json
import re
import shlex
import shutil

from pytest_bdd import given, parsers, then, when

from . import requests_world_steps as world
from .requests_steps import write_request
from .requests_world_steps import GOOD, home, local_text, pending, request_rel, sections_of, sibling, text_of

ROLE = r"(?P<who>the upstream|the asker(?: \S+)?|the product level \S+|ctx-u)"
WHERE = r"(?P<where>its own repository|the asker (?P<aname>\S+)'s repository|the upstream \S+'s repository)"


@given(parsers.re(r"an upstream (?P<name>ctx-\S+) that keeps no request"))
def an_upstream(repo, context, name):
    world.upstream(repo, context, name)


@given("the asker ctx-a keeps a request q7 from its own asker ctx-b")
def asker_keeps_q7(repo, context):
    write_request(world.asker_repo(repo, context, "ctx-a"), {}, "q7", "ctx-b", None, "upstream", "one", [])


@given("a file lines.md with two lines in strict EARS in the asker ctx-a's repository")
def lines_in_the_askers_repository(repo, context):
    path = sibling(repo, "ctx-a")
    world.make_repo(path, "ctx-a")
    (path / "lines.md").write_text("\n".join(GOOD) + "\n")


@given("the asker ctx-a's repository has no checkout of the upstream's repository")
def no_checkout(repo, context):
    world.upstream(repo, context, "ctx-u")
    asker = world.asker_repo(repo, context, "ctx-a")
    world.publish_kept(repo, context)
    assert not list((asker / ".shop" / "work" / "requests").glob("q*.md"))


@then("work made no checkout of the upstream's repository")
def made_no_checkout(context):
    asker = context["askers"]["ctx-a"]
    assert not (asker / request_rel("q1")).exists() and not (asker / "spec" / "index.md").read_text().count("ctx-u")


@given(parsers.re(r"a request (?P<ident>q\d+) to the upstream ctx-u from the asker (?P<asker>\S+) whose turn is the "
                  r"(?P<turn>asker|upstream)'s, with one line whose line outcome is question"))
def a_request_to_the_upstream(repo, context, ident, asker, turn):
    world.upstream(repo, context, "ctx-u")
    if asker != "ctx-u":
        world.asker_repo(repo, context, asker)
    write_request(repo, context, ident, asker, None, turn, "one", ["question"])
    world.publish_kept(repo, context)


@given(parsers.re(r"the upstream ctx-u keeps a request (?P<ident>q\d+) from the asker (?P<asker>\S+) whose turn is the asker's, "
                  r"with one line whose line outcome is question"))
def upstream_keeps_a_request(repo, context, ident, asker):
    world.upstream(repo, context, "ctx-u")
    write_request(repo, context, ident, asker, None, "asker", "one", ["question"])
    world.publish_kept(repo, context)


def request_item(ident, asker, title="Show the queue"):
    return {"kind": "request", "id": ident, "asker": asker, "title": title, "lines": GOOD, "sources": [], "thread": "t1",
            "raised_for": None, "delegation": None}


def answer_item(asker, text, ident="q2"):
    return {"kind": "answer", "request": ident, "question": 1, "text": text, "asker": asker}


@given(parsers.parse('the asker ctx-a has sent ctx-u a request q1, and on q2 the answer "{answer}" to that question and the '
                     'passing of q2\'s turn, none of which ctx-u has taken in'))
def asker_has_sent_three(repo, context, answer):
    world.asker_repo(repo, context, "ctx-a")
    world.send(repo, context, "ctx-a", request_item("q1", "ctx-a"))
    world.send(repo, context, "ctx-a", answer_item("ctx-a", answer))
    world.send(repo, context, "ctx-a", {"kind": "turn", "request": "q2", "asker": "ctx-a"})


@given(parsers.re(r"a listing of what has been sent to ctx-u shows (?P<shown>q1 and both messages|none of them yet)"))
def a_listing_shows(repo, context, shown):
    if shown != "none of them yet":
        pending(repo, context)     # the upstream's copy of the remote's refs has them


SENT = r'(?P<sent>a request (?P<rid>q\d+)|on (?P<on>q\d+) the answer "(?P<answer>[^"]*)" to the question "[^"]*")'


@given(parsers.re(r"a repository registered under the asker id (?P<aid>\S+), which (?:the upstream )?(?P<up>ctx-\S+) "
                  r"(?P<allow>allows|does not allow) for the asker (?P<asker>\S+), that has sent " + SENT + r" naming the asker (?P=asker)"))
def registered_and_sent(repo, context, aid, up, allow, asker, sent, rid, on, answer):
    if "upstream" not in context:
        world.upstream(repo, context, up)
    world.asker_repo(repo, context, asker, asker_id=aid, allowed=allow == "allows")
    world.send(repo, context, asker, request_item(rid, asker) if rid else answer_item(asker, answer, on))


@given(parsers.re(r'the asker (?P<asker>\S+) has sent ctx-u (?:a request (?P<rid>q\d+)|on (?P<on>q\d+) an answer to the question '
                  r'"[^"]*"), whose (?:title|text) reads "(?P<text>[^"]*)"'))
def asker_sent_instruction(repo, context, asker, rid, on, text):
    world.asker_repo(repo, context, asker)
    world.send(repo, context, asker, request_item(rid, asker, title=text) if rid else answer_item(asker, text, on))


def path_of(repo, context, who, where, aname):
    """The repository `who` runs in: the upstream's, or the asker's (made when it is not yet there)."""
    if who in ("the upstream", "ctx-u") or where.startswith("the upstream"):
        return home(repo, context)
    name = aname or (who.split(" ", 2)[2] if who.startswith("the product level") else who.split(" ", 2)[-1] if who != "the asker" else None)
    name = name or next(iter(context["askers"]))
    path = context["askers"].get(name) or world.asker_repo(repo, context, name)
    if (repo / "lines.md").exists() and not (path / "lines.md").exists():
        shutil.copy(repo / "lines.md", path / "lines.md")
    return path


@when(parsers.re(ROLE + r" (?P<what>answers that question with \"(?P<answer>[^\"]*)\"|runs `work (?P<args>[^`]+)`) in " + WHERE
                 + r"(?P<giving>, giving no side)?"))
def runs_in_a_repository(repo, run, context, who, what, answer, args, where, aname, giving):
    argv = ["reply", "q1", "1", answer] if answer is not None else shlex.split(args)
    from .requests_run_steps import stub_env     # `work run` runs with the stand-in claude (r40)
    context["ran_in"] = path_of(repo, context, who, where, aname)
    context["done"] = run("work", *argv, cwd=context["ran_in"], **({"env": stub_env(context)} if argv[0] == "run" else {}))


@when("the asker answers that question with \"{answer}\" in its own repository")
def asker_answers_in_its_repository(repo, run, context, answer):
    context["done"] = run("work", "reply", "q1", "1", answer, cwd=path_of(repo, context, "the asker", "its own repository", None))


@when("the upstream takes in what has been sent to it")
def takes_in(repo, run, context):
    context["done"] = run("work", "take-in", cwd=home(repo, context))


@then(parsers.re(r"the upstream keeps a new request from the asker (?P<asker>\S+)"))
def keeps_a_new_request(repo, context, asker):
    new = [i for _, _, i in pending(repo, context) if i["kind"] == "request" and i["asker"] == asker]
    assert len(new) == 1 and new[0]["id"] != "q1", (new, context["done"])


@then("the command is refused because an origin belongs to an internal request")
def refused_origin(context):
    assert "origin" in context["done"].stderr and "internal request" in context["done"].stderr, context["done"]


@then("the command is refused because the request names neither a request it is raised for nor a job-thread")
def refused_neither(context):
    err = context["done"].stderr
    assert "neither a request it is raised for nor a job-thread" in err, context["done"]


@then(parsers.re(r"the command is refused, naming (?P<asker>\S+)"))
def refused_naming_asker(context, asker):
    assert asker in context["done"].stderr, context["done"]


@then("the command is refused, naming the upstream as the side that writes line outcomes")
def refused_naming_upstream(context):
    err = context["done"].stderr
    assert "upstream is the side that writes line outcomes" in err, context["done"]


@then(parsers.re(r"(?P<ident>q\d+) holds (?P<written>.+) as the (?P<side>asker|upstream)'s part"))
def holds_as_part(repo, context, ident, written, side):
    found = sections_of(text_of(repo, context, ident))
    if side == "asker":
        answer, question = re.fullmatch(r'the answer "(.*)" to the question "(.*)"', written).groups()
        number = next(e.split(". ", 1)[0] for e in found["Questions"] if e.endswith(": " + question))
        assert "%s. %s" % (number, answer) in found["Answers"], found
    else:
        word, line = re.fullmatch(r"the line outcome (\S+) of line (\d+)", written).groups()
        assert "%s. %s" % (line, word) in found["Outcomes"], found


@then(parsers.re(r'(?:ctx-u|it) keeps (?P<ident>q\d+) from the asker (?P<asker>\S+?)(?:, titled "(?P<title>.+)")?'))
def keeps_taken_in(repo, context, ident, asker, title):
    text = local_text(repo, context, ident)
    assert text is not None and "asker: %s\n" % asker in text, (text, context["done"])
    assert title is None or "\n# %s\n" % title in text


@then(parsers.re(r"ctx-u keeps no request (?P<ident>q\d+)"))
def keeps_no_such_request(repo, context, ident):
    assert local_text(repo, context, ident) is None


@then(parsers.re(r"(?P<ident>q\d+) holds no answer"))
def holds_no_answer(repo, context, ident):
    assert sections_of(local_text(repo, context, ident))["Answers"] == []


@then(parsers.re(r"work tells the upstream it left (?P<left>.+) untaken because the asker id (?P<aid>\S+) is not one ctx-u allows "
                 r"for the asker (?P<asker>\S+)"))
def told_what_was_left(context, left, aid, asker):
    told = "left %s untaken because the asker id %s is not one ctx-u allows for the asker %s" % (left, aid, asker)
    assert told in context["done"].stdout, context["done"]


@then(parsers.re(r"(?P<ident>q\d+)'s status is as it was and (?P=ident) has no resolution"))
def status_as_it_was(repo, context, ident):
    kept = local_text(repo, context, ident)
    status = re.search(r"(?m)^status: (.*)$", kept).group(1)
    assert status == re.search(r"(?m)^status: (.*)$", context["written"]).group(1)
    assert sections_of(kept)["Resolution"] == [], json.dumps(kept)
