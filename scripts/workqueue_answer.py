"""`work answer`: the person's answer to a work-item's question (capability work-queue, r9, r13, r14)."""
import datetime
from pathlib import Path

import workqueue
from workqueue import Refused

# The status of the stage that asked, by the status the work-item moved to awaiting-answer from: an implementer asks
# while its work-item is claimed, and started from ready.
ASKED_FROM = {"claimed": "ready"}


def asked_from(root, path, name):
    """The status the stage that asked the question of `name` started from, by log.jsonl's last move into awaiting-answer."""
    moves = [line for line in workqueue.logged(path.parent / "log.jsonl", root)
             if line.get("work-item") == name and line.get("after") == "awaiting-answer"]
    if not moves or not isinstance(moves[-1].get("before"), str):
        raise Refused("log.jsonl gives no transition of %s to awaiting-answer; work answer has no status to return it to" % name)
    return ASKED_FROM.get(moves[-1]["before"], moves[-1]["before"])


def answer(root, name, text):
    """Write `text` with today's date under the awaiting-answer work-item `name`'s `## Answers` and return it to the
    status the stage that asked started from; return that status."""
    path = workqueue.find(root, name)
    initiative = path.parent.name
    if workqueue.agrees(root, initiative, name) != "awaiting-answer":
        raise Refused("%s is not awaiting-answer; work answer answers only an awaiting-answer work-item" % name)
    status = asked_from(root, path, name)
    if "\n" in text or "\r" in text:
        raise Refused("the answer has a newline in it; an answer is one line")
    line = "- %s: %s\n" % (datetime.date.today().isoformat(), text)

    def write():
        body = workqueue.read(path, root)
        if "\n## Answers\n" in body:
            head, tail = body.split("\n## Answers\n", 1)
            rest = tail.split("\n## ", 1)
            section = rest[0].rstrip("\n") + "\n" + line
            body = head + "\n## Answers\n" + section + ("\n## " + rest[1] if len(rest) > 1 else "")
        else:
            body = body.rstrip("\n") + "\n\n## Answers\n" + line
        path.write_text(body)
        workqueue.move(root, initiative, name, status, by="work answer")
    workqueue.committed(root, workqueue.rels_of(root, path), "work answer: %s awaiting-answer -> %s" % (name, status), write)
    return status
