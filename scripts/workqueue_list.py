"""`work list` and `work show <target>` (capability work-queue, r34-r39).

`list` reads the whole queue under .shop/work/, ended initiatives among it; `show` gives one initiative (as `work status`
does) or one work-item. Both only read. The requests an initiative raised into an upstream are read from this context's own
record, .shop/work/<initiative>/raised.jsonl, one JSON object a line (upstream, request, initiative, status), the last
line of a request giving its last known status; the upstream is never reached.
"""
import json
from pathlib import Path

import workqueue
import workqueue_status
from workqueue import Refused

RAISED = "raised.jsonl"


def initiatives(root):
    """(name, status) of each initiative under .shop/work/."""
    work = Path(root) / workqueue.WORK
    for name in sorted((p.parent.name for p in work.glob("*/initiative.md")), key=workqueue_status.natural):
        yield name, workqueue.frontmatter(workqueue.read(work / name / "initiative.md", root))[0].get("status")


def waiting(root, initiative):
    """The requests `initiative` raised that its record does not give as delivered: (upstream, request, status)."""
    path = Path(root) / workqueue.WORK / initiative / RAISED
    last = {}
    lines = workqueue.read(path, root).splitlines() if path.is_file() else []
    for number, line in enumerate(lines, 1):
        if line.strip():
            try:
                found = json.loads(line)
                last[(found["upstream"], found["request"])] = found["status"]
            except (ValueError, KeyError, TypeError):
                raise Refused("%s line %d is not a record of a raised request (upstream, request, status)" % (path, number))
    return [(u, r, s) for (u, r), s in last.items() if s != "delivered"]


def listing(root, as_json):
    found = list(initiatives(root))
    requests = list(workqueue.requests(root))
    items = list(workqueue.items(root))
    if as_json:
        print(json.dumps({"initiatives": [{"initiative": n, "status": s} for n, s in found],
                          "requests": [{"request": n, "status": s} for n, s, _, _ in requests],
                          "work-items": [{"work-item": n, "initiative": i, "status": s} for i, n, s in items]}))
        return 0
    for name, status in found:
        print("initiative %s %s" % (name, status))
        for upstream, request, state in waiting(root, name):
            print("initiative %s waiting on %s (in %s, %s)" % (name, request, upstream, state))
    for name, status, _, _ in requests:
        print("request %s %s" % (name, status))
    for initiative, name, status in items:
        print("work-item %s/%s %s" % (initiative, name, status))
    return 0


def work_item(root, target, as_json):
    path = workqueue.find(root, target)
    text = workqueue.read(path, root)
    data = workqueue.frontmatter(text)[0]
    if data.get("kind") is None:
        raise Refused("%s has no kind (a work-item or an initiative is what work show shows)" % target)
    if data.get("kind") != "work-item":
        raise Refused("%s is a %s, not a work-item or an initiative that work show shows" % (target, data.get("kind")))
    status = data.get("status")
    questions = workqueue_status.section(text, "Questions")[len(workqueue_status.section(text, "Answers")):]
    if as_json:
        print(json.dumps({"work-item": target, "initiative": path.parent.name, "status": status, "questions": questions}))
    else:
        print("work-item %s/%s %s" % (path.parent.name, target, status))
        for question in questions:
            print("  question: %s" % question)
    return 0


def show(root, target, as_json):
    """Print where `target`, an initiative or a work-item, stands; return the exit status."""
    workqueue.entry(target, "target")
    for name, status, turn, _ in workqueue.requests(root):     # r25: a request, with its status and whose turn it is
        if name == target:
            print(json.dumps({"request": name, "status": status, "turn": turn}) if as_json else "%s %s %s" % (name, status, turn))
            return 0
    if (Path(root) / workqueue.WORK / target / "initiative.md").is_file():
        return workqueue_status.status(root, target, as_json)
    return work_item(root, target, as_json)
