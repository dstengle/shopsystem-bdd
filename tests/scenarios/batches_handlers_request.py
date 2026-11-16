"""The request a delivered item was taken in from, in features/batches.feature (r40, b6): the world's request q9
(readiness_world's) made `accepted`, its line accepted and on its issue, and the Thens of what `work batch merged` did
to it: its status and side, its resolution (each recorded line's requirement id and the merge commit), the resolve
comment posted, the issue closed and the request committed. Each is in world_four's chain of the batches' scenarios
and returns False for a step that is not about the request."""
import json
import sys

import backlog_items
import request_text

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts


class _Lazy:
    """A world module another handler module loads, looked up when a step runs."""
    def __init__(self, name):
        self.name = name

    def __getattr__(self, attr):
        return getattr(sys.modules[self.name], attr)


R, Q = _Lazy("shop_readiness_world"), _Lazy("shop_requests_world")


def _path(step, name):
    rel = W.node_rel(step.context, name)
    return step.repo / rel if rel else None


def _field(path, key, value):
    text = path.read_text()
    lines = [("%s: %s" % (key, value)) if line.startswith("%s: " % key) else line for line in text.split("\n")]
    path.write_text("\n".join(lines))


@four("GivenK_A", "request", "batches")
def request_is(step):
    """`the status of the request r2 is `accepted``: the request is accepted, its line 1 accepted, on its issue."""
    if not step.names or " is not " in step.text or _path(step, step.names[0]) is None:
        return False
    path, value = _path(step, step.names[0]), step.values[0].strip("`")
    _field(path, "status", value)
    if value == "accepted":
        path.write_text(request_text.with_entries(path.read_text(), "Outcomes", ["1. accepted"]))
    Q.with_issue(step, path)


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)


def _request(step):
    """The path of the scenario's request whose status a Given set."""
    name = next(n for n, (kind, _) in step.context["nodes"].items() if kind == "request" and n != R.REQUEST)
    return _path(step, name)


def _issue(step):
    return W.field(_request(step), "issue")


@four("ThenDoes", "set", "batches")
def sets(step):
    """The status (`status:`) or the side (`turn:`) of the request is the value."""
    np = step.nps[0]
    key = "status" if np.startswith("the status of the request ") else "turn" if np.startswith(
        "the side of the request ") else None
    if key is None:
        return False
    _done(step)
    got = W.field(_path(step, step.names[0]), key)
    assert got == step.values[0].strip("`"), (step.text, got)


@four("ThenDoes", "write", "batches")
def writes_resolution(step):
    """The request's `## Resolution`, empty before the run, holds each line the item recorded, as its requirement id
    and the merge commit gh gave."""
    if parts(step)[1][0] != "resolution":
        return False
    _done(step)
    path = _request(step)
    rel = path.relative_to(step.repo).as_posix()
    had = request_text.entries(W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel)), "Resolution")
    oid = next(iter(json.loads((T.outside(step) / "gh-state.json").read_text()).values()))["mergeCommit"]["oid"]
    item = next(n for n, f in step.context["given"]["item"].items() if f.get("batch"))
    recorded = backlog_items.find(step.repo, B.ident(item)).request_lines
    wanted = ["%d. %s %s" % (n, ident, oid) for ident, n in recorded.items()]
    got = request_text.entries(path.read_text(), "Resolution")
    assert not had and wanted and got == wanted, (step.text, had, got, wanted)


@four("ThenDoes", "post", "batches")
def posts(step):
    """A comment of the step `resolve` on the request's issue."""
    if parts(step)[1][0] != "comment":
        return False
    _done(step)
    comments = Q.issues(step)[_issue(step)]["comments"]
    assert any("step: resolve" in c["body"] for c in comments), (step.text, comments)


@four("ThenDoes", "close", "batches")
def closes(step):
    if parts(step)[1][0] != "issue":
        return False
    _done(step)
    assert Q.issues(step)[_issue(step)]["state"] == "CLOSED", (step.text, Q.issues(step))
    step.context.setdefault("closed", {})[step.names[0]] = _issue(step)


@four("ThenDoes", "has", "batches")
def has_issue(step):
    """The request has the issue the run closed."""
    if [k for k, _ in parts(step)] != ["request", "issue"]:
        return False
    assert step.context.get("closed", {}).get(step.names[1]) == _issue(step), (step.text, step.context.get("closed"))


@four("ThenDoes", "commit", "batches")
def commits(step):
    if parts(step)[1][0] != "request":
        return False
    _done(step)
    B.in_commits(step, _request(step).relative_to(step.repo).as_posix())
