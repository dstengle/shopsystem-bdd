"""Handlers of features/requests.feature's conversation on an issue: `work offer`, `fits`, `propose`, `accept`, `sync`
and `watch` run on the requests the Givens wrote, each on its issue in the stand-in gh (requests_world.py), with the
comments the Givens put on them; what `work` posted and closed is read back from the stand-in's calls, and what it
recorded from the requests' `## Comments`. An issue a Given names is an open ask on this context's own repository
that no request has."""
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
HANDLERS = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith("requests_handlers.py"))
ASK = ("~~~shop-request\nstep: ask\nrequest: request/ex.com/prod/other/q7\nasker: bounded-context/ex.com/prod/other\n"
       "title: a new ask\nask: I need a thing\n~~~\n")


@handler("GivenK", "foreign entry")
def given_foreign_entry(step):
    step.context.setdefault("foreign", {})[step.names[0]] = "a foreign answer %s" % step.names[0]


@handler("GivenK", "issue")
def given_issue(step):
    """An open issue on the repository's own GitHub repository (`ex/ctx`) whose body is an ask's block of fields."""
    found = Q.issues(step)
    url = "https://github.com/%s/issues/%d" % (Q.OWN_REPO, 50 + len(found))
    found[url] = {"title": "a new ask", "body": ASK, "state": "OPEN", "comments": []}
    Q.write_issues(step, found)
    step.context.setdefault("issues", {})[step.names[0]] = url
    step.context.setdefault("says", {})[step.names[0]] = url


def held_before(step):
    for path in (step.repo / ".shop" / "requests").glob("q*.md"):
        step.context.setdefault("held_before", {})[path.name] = path.read_text()


@handler("WhenRuns", "`work sync`")
def work_sync(step):
    HANDLERS.prepare_all(step)
    held_before(step)
    HANDLERS.run_work(step, "sync")


@handler("WhenRuns", "`work watch`")
def work_watch(step):
    """One poll, at once, so no scenario can wait: `--every 0 --polls 1`."""
    HANDLERS.prepare_all(step)
    held_before(step)
    HANDLERS.run_work(step, "watch", "--every", "0", "--polls", "1")


@handler("WhenRuns", "`work watch --forward`")
def work_watch_forward(step):
    """GitHub's events through the stand-in's `gh webhook forward`: what the Givens wrote is taken out of the
    stand-in's issues and kept pending (`gh-pending.json`), so the watch's check at its start finds nothing; the
    stand-in's forward puts it back and posts the event once that check is done. One wait of at most 20 s."""
    HANDLERS.prepare_all(step)
    held_before(step)
    step.context.setdefault("before_run", []).append(Q.pend)
    HANDLERS.run_work(step, "watch", "--forward", "--every", "20", "--polls", "1")


@handler("WhenRuns", "`work offer`")
@handler("WhenRuns", "`work fits`")
@handler("WhenRuns", "`work propose`")
@handler("WhenRuns", "`work accept`")
def work_step(step):
    name = step.names[-1]
    word = step.term.strip("`").split()[1]
    path = HANDLERS.path_of(step, name)
    if word == "accept":
        R.codify(step)
        path.write_text(path.read_text().replace("1. line 1\n", "1. %s\n" % R.PASSING, 1)
                        .replace("## Resolution\n", "## Into\n1. work-queue\n\n## Resolution\n", 1))
    q = HANDLERS.prepare(step, name)
    rest = {"offer": ["--note", "This may serve."], "fits": ["--serves", "thing#r1"],
            "propose": ["--line", HANDLERS.GOOD], "accept": []}[word]
    HANDLERS.run_work(step, word, q, *rest)


def calls(step, *words):
    return [argv for argv in Q.gh_calls(step) if argv[:len(words)] == list(words)]


def of_issue(np):
    """`gh issue create` for an issue, `gh issue comment` for a comment."""
    return ("issue", "create") if "issue" in np.split() else ("issue", "comment")


@handler("ThenDoes", "post")
def then_posts(step):
    assert calls(step, *of_issue(step.nps[-1])), (step.text, Q.gh_calls(step))


@handler("ThenDoes", "close")
def then_closes(step):
    assert calls(step, "issue", "close"), (step.text, Q.gh_calls(step))


def held(step, name, text=None):
    """How often the comment `name`'s URL is under its request's `## Comments` (in `text`, else as the file is)."""
    path = HANDLERS.path_of(step, Q.comment(step, name)["request"])
    text = path.read_text() if text is None else text
    return text.split("## Comments", 1)[-1].count(step.context["comments"][name] + " ")


@handler("ThenDoesNot", "write")
def writes_not(step):
    """A comment held before the run is held once still; one that was not is held not at all. A foreign entry is in
    no request."""
    if "generated" in step.context:     # feature-file-tools' overstated file (r21)
        return shared("shop_feature_file_tools_handlers", "feature_file_tools_handlers.py").unoverstated(step)
    name = step.names[0]
    if name in step.context.get("foreign", {}):
        for path in (step.repo / ".shop" / "requests").glob("q*.md"):
            assert step.context["foreign"][name] not in path.read_text(), (step.text, path.read_text())
        return
    path = HANDLERS.path_of(step, Q.comment(step, name)["request"])
    before = step.context.get("held_before", {}).get(path.name, "")
    assert held(step, name) == held(step, name, before), step.text
