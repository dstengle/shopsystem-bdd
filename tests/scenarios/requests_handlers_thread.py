"""Context requests' thread and its channel (b68, context-requests r51, r52, r54, r55; b71, r56): a request's thread is
the issue it is on in the stand-in gh (requests_world), its channel GitHub; a channel whose availability is `rejecting`
is a stand-in whose `gh issue close` fails (`$STUB_GH_FAIL`, requests_world.env), and a channel that does not provide
a thread one whose `gh issue view` fails; the thread `closed` is the issue's state in the stand-in once the command
ran. Each a `local` of work_queue_world's table, loaded after requests_handlers_givens so
it is tried first, passing on any step not of a thread or a channel or of another scenario than b68's groups'."""
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
Q = sys.modules["shop_requests_world"]


GROUPS = {"g51", "g52", "g54", "g55", "g56"}     # context-requests' groups of b68 and b71, the only scenarios these steps are taken in


def _ours(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "context-requests" and bool(GROUPS & found.tags)


def _threads(step):
    return step.context.setdefault("threads", {})


def _issue_of(step, request):
    return W.field(step.repo / W.node_rel(step.context, request), "issue")


def _url(step, name):
    """The issue of the thread `name`: the one a Given or a Then bound it to, else that of the one request a Given
    wrote; None when there is no such request (a request the run raised, whose thread requests_handlers_reword reads)."""
    if name not in _threads(step):
        requests = [n for n, (kind, _) in step.context.get("nodes", {}).items() if kind == "request" and n]
        if len(requests) != 1:
            return None
        _threads(step)[name] = _issue_of(step, requests[0])
    return _threads(step)[name]


@W.local("GivenK", "channel")
@W.local("GivenK", "thread")
def given_bare(step):
    if not _ours(step):
        return False


@W.local("GivenK_A", "channel")
def given_channel(step):
    """A channel whose availability is `rejecting`: GitHub refuses to close an issue."""
    if not _ours(step):
        return False
    if step.values and step.values[0].strip("`") == "rejecting" and " not " not in step.text:
        step.context["gh_fail"] = "issue close"


@W.local("GivenDoesNot")
def given_unprovided(step):
    """`the channel c2 does not provide the thread t1`: GitHub fails to show the issue."""
    if not _ours(step) or step.term != "provide":
        return False
    step.context["gh_fail"] = "issue view"


@W.local("GivenDoes")
def given_on_has(step):
    """`the thread t1 is on the channel c2`: every thread is on GitHub; `the context request c1 has the thread t1`:
    t1 is the issue the request is on."""
    if not _ours(step) or len(step.nps) != 1 or not step.nps[0].startswith(("the thread ", "the channel ")):
        return False
    if step.event == "on" and step.subject.startswith("the thread "):
        return None
    if step.event == "has" and step.nps[0].startswith("the thread "):
        url = _issue_of(step, step.names[0])
        _threads(step)[step.names[1]] = url
        step.context.setdefault("says", {})[step.names[1]] = url
        return None
    return False


@W.local("ThenDoes")
def then_thread(step):
    """`... sets the status of the thread t1 to `closed``: its issue's state in the stand-in; `the context request c1
    has the thread t1`: its record names that issue."""
    if not _ours(step) or not step.nps:
        return False
    if step.event == "set" and step.nps[0].startswith("the status of the thread "):
        url = _url(step, step.names[-1])
        assert url, ("no request whose thread is %s" % step.names[-1], step.text)
        state = Q.issues(step)[url]["state"]
        assert state == step.values[0].strip("`").upper(), (step.text, url, state)
        return None
    if step.event == "has" and step.nps[-1].startswith("the thread ") and _url(step, step.names[1]):
        assert _issue_of(step, step.names[0]) == _url(step, step.names[1]), step.text
        return None
    return False
