"""Handlers of features/requests.feature's conversation on an issue (requests r27-r41, intake r7): `work offer`,
`fits`, `propose`, `accept` and `sync` run on the requests world_nodes.py writes, each on the issue requests_world.py
gives it in the stand-in gh; what `work` posted and closed is read back from the stand-in's calls.

A comment a Given names is a comment on the issue of the request q1 (written when no Given wrote it): `unrecorded`
is a readable comment the request does not hold, `not unrecorded` one it holds already, `unreadable` one whose block
of fields does not parse."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


def shared(name, file):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
Q = shared("shop_requests_world", "requests_world.py")
R = shared("shop_readiness_world", "readiness_world.py")
NODES = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith("world_nodes.py"))
HANDLERS = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith("requests_handlers.py"))
local = W.local
READABLE = "~~~shop-request\nstep: turn\nstatus: awaiting-upstream\nturn: upstream\nanswer 1: The work queue\n~~~\n"
UNREADABLE = "~~~shop-request\nstep: turn\nthis is no field\n~~~\n"


def request_path(step, name="q1"):
    if not W.node_rel(step.context, name):
        NODES.write_node(step, "request", name, "open")
    path = step.repo / W.node_rel(step.context, name)
    Q.with_issue(step, path)
    return path


@handler("GivenK", "comment")
def given_comment(step):
    """A readable comment on q1's issue, `<issue>#issuecomment-<k>`, k counting the comments."""
    request_path(step)
    found = Q.issues(step)
    comments = found[Q.ISSUE]["comments"]
    url = "%s#issuecomment-%d" % (Q.ISSUE, 100 + len(comments))
    comments.append({"url": url, "body": READABLE})
    Q.write_issues(step, found)
    step.context.setdefault("comments", {})[step.names[0]] = url
    step.context.setdefault("says", {})[step.names[0]] = url


@handler("GivenK_C", "comment")
def given_comment_condition(step):
    """unrecorded: as written; not unrecorded: held under the request's `## Comments`; unreadable: its block broken."""
    word, url = step.text.split(" is ", 1)[1], step.context["comments"][step.names[0]]
    if word == "not unrecorded":
        path = request_path(step)
        path.write_text(path.read_text().rstrip("\n") + "\n\n## Comments\n1. %s turn\n" % url)
    elif word == "unreadable":
        found = Q.issues(step)
        for comment in found[Q.ISSUE]["comments"]:
            if comment["url"] == url:
                comment["body"] = UNREADABLE
        Q.write_issues(step, found)


@handler("WhenRuns", "`work sync`")
def work_sync(step):
    for path in (step.repo / ".shop" / "requests").glob("q*.md"):
        step.context.setdefault("held_before", {})[path.name] = path.read_text()
    HANDLERS.run_work(step, "sync")


@handler("WhenRuns", "`work watch`")
def work_watch(step):
    """One poll, at once, so no scenario can wait: `--every 0 --polls 1`."""
    for path in (step.repo / ".shop" / "requests").glob("q*.md"):
        step.context.setdefault("held_before", {})[path.name] = path.read_text()
    HANDLERS.run_work(step, "watch", "--every", "0", "--polls", "1")


@handler("WhenRuns", "`work offer`")
@handler("WhenRuns", "`work fits`")
@handler("WhenRuns", "`work propose`")
@handler("WhenRuns", "`work accept`")
def work_step(step):
    name = step.names[-1]
    word = step.term.strip("`").split()[1]
    if word == "accept":
        R.codify(step)
        path = step.repo / W.node_rel(step.context, name)
        path.write_text(path.read_text().replace("1. line 1\n", "1. %s\n" % R.PASSING, 1)
                        .replace("## Resolution\n", "## Into\n1. work-queue\n\n## Resolution\n", 1))
    HANDLERS.prepare(step, name)
    rest = {"offer": ["--note", "This may serve."], "fits": ["--serves", "thing#r1"],
            "propose": ["--line", HANDLERS.GOOD], "accept": []}[word]
    HANDLERS.run_work(step, word, name, *rest)


def calls(step, *words):
    return [argv for argv in Q.gh_calls(step) if argv[:len(words)] == list(words)]


@handler("ThenDoes", "post")
def then_posts(step):
    """An issue: `gh issue create`; a comment: `gh issue comment` on the request's issue."""
    if step.nps[-1].startswith("the issue"):
        assert calls(step, "issue", "create"), (step.text, Q.gh_calls(step))
    else:
        assert calls(step, "issue", "comment"), (step.text, Q.gh_calls(step))


@handler("ThenDoes", "close")
def then_closes(step):
    assert calls(step, "issue", "close"), (step.text, Q.gh_calls(step))


def held(step, name):
    """How often the comment `name`'s URL is under q1's `## Comments`."""
    text = (step.repo / W.node_rel(step.context, "q1")).read_text()
    return text.split("## Comments", 1)[-1].count(step.context["comments"][name] + " ")


@local("ThenDoes", "comment")
def writes_comment(step):
    if step.term != "write":
        return False
    assert held(step, step.names[0]) == 1, (step.text, held(step, step.names[0]))


@handler("ThenDoesNot", "write")
def writes_not(step):
    """A comment held before the run is held once still; one that was not is held not at all."""
    name = step.names[0]
    before = step.context.get("held_before", {}).get("q1.md", "")
    assert held(step, name) == (1 if step.context["comments"][name] + " " in before else 0), step.text
