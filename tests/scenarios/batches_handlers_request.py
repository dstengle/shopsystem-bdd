"""The request a delivered item was taken in from, in features/batches.feature (r40, b6): the world's request q9
(readiness_world's) made `accepted`, its line accepted and on its issue, and `resolved`, what `work batch merged`
did to it when it resolves it (r105, b578): its status, its resolution (each recorded line's requirement id and the
merge commit), the resolve comment posted and the issue closed, which batches_handlers_tracking's Then reads."""
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


def resolved(step, name):
    """The context request `name` resolved by the run: `delivered` and in the asker's turn, its `## Resolution`, empty
    before the run, holding each line the item recorded as its requirement id and the merge commit gh gave, the request
    file among the files of the commits the run made, and the resolve comment posted on its issue, closed."""
    _done(step)
    path = _path(step, name)
    assert W.field(path, "status") == "delivered", (step.text, W.field(path, "status"))
    assert W.field(path, "turn") == "asker", (step.text, W.field(path, "turn"))
    rel = path.relative_to(step.repo).as_posix()
    changed = W.git(step.repo, "log", "--format=", "--name-only", "%s..HEAD" % step.context["head"]).split()
    assert rel in changed, (step.text, rel, changed)
    had = request_text.entries(W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel)), "Resolution")
    oid = next(iter(json.loads((T.outside(step) / "gh-state.json").read_text()).values()))["mergeCommit"]["oid"]
    item = next(n for n, f in step.context["given"]["item"].items() if f.get("batch"))
    recorded = backlog_items.find(step.repo, B.ident(item)).request_lines
    wanted = ["%d. %s %s" % (n, ident, oid) for ident, n in recorded.items()]
    got = request_text.entries(path.read_text(), "Resolution")
    assert not had and wanted and got == wanted, (step.text, had, got, wanted)
    issue = Q.issues(step)[W.field(path, "issue")]
    assert any("step: resolve" in c["body"] for c in issue["comments"]), (step.text, issue["comments"])
    assert issue["state"] == "CLOSED", (step.text, issue)
