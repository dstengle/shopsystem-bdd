"""Context requests' Thens in the domain contract's words (§9.2) that the requests and intake handlers knew by
others: a request raised keeps its thread (the issue opened for it), the request has its thread, a request line has
its reason (intake's "the reason r3 is for the request line r1"). Each a `local` of ThenDoes, passing on any other
step."""
import sys

W = sys.modules["shop_work_queue_world"]


def _module(stem):
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


def _ours(step):
    return sys.modules["vocab"].origin(step.request.node) in ("requests", "intake")


@W.local("ThenDoes")
def thread(step):
    """`... keeps the thread t1`: the issue the request is raised on, opened; `the request c2 has the thread t1`."""
    if not _ours(step) or not step.nps or not step.nps[-1].startswith("the thread "):
        return False
    if step.term in ("write", "commit", "post", "keep"):
        issues = _module("requests_handlers_issues")
        assert issues.calls(step, "issue", "create"), (step.text, sys.modules["shop_requests_world"].gh_calls(step))
    elif step.term != "has":
        return False


@W.local("ThenDoes")
def line_has_reason(step):
    """`the request line r1 has the reason l1`: intake's `the reason l1 is for the request line r1`."""
    if not _ours(step) or step.term != "has" or not step.subject.startswith("the request line ") \
            or not step.nps[0].startswith("the reason "):
        return False
    if step.context["result"].returncode != 0:      # a refusal naming the reason it lacks: nothing was written
        return None
    step.subject, step.nps = step.nps[0], [step.subject]
    step.names = list(reversed(step.names))
    step.term = step.event = "for"
    step.text = "%s is for %s" % (step.subject, step.nps[0])
    return W.LOCAL[("ThenDoes", None)](step)
