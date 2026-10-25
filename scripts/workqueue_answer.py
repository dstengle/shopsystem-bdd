"""`work answer`: the person's answer to a work-item's question (capability work-queue, r9, r13, r14)."""
import datetime

import workqueue
from workqueue import Refused

# The status of the stage that asked, by the status the work-item moved to awaiting-answer from: an implementer asks
# while its work-item is claimed, and started from ready.
ASKED_FROM = {"claimed": "ready"}

# Unicode's mandatory line breaks (r15): LF, VT, FF, CR, NEL, LS, PS.
LINE_BREAKS = "\n\x0b\x0c\r\x85  "


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
    if any(c in text for c in LINE_BREAKS):
        raise Refused("the answer has a line break in it; an answer is one line")
    if "/" in name:     # <initiative>/<name> (r30): that initiative's file, whatever other initiatives hold the name
        initiative, name = (name.split("/", 1) + [""])[:2]
        workqueue.entry(initiative, "initiative")
        workqueue.entry(name, "name")
        path = workqueue.Path(root) / workqueue.WORK / initiative / (name + ".md")
    else:
        path = workqueue.find(root, name)
        initiative = path.parent.name
    if workqueue.agrees(root, initiative, name) != "awaiting-answer":
        raise Refused("%s is not awaiting-answer; work answer answers only an awaiting-answer work-item or capability-proposal" % name)
    proposal = "\nkind: capability-proposal\n" in workqueue.read(path, root).split("\n---\n", 1)[0] + "\n"
    status = "awaiting-answer" if proposal else asked_from(root, path, name)
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
        if not proposal:
            workqueue.move(root, initiative, name, status, by="work answer")
    if proposal:     # a proposal's answer is written only: no transition, no log line (r24, r9)
        workqueue.committed(root, [str(path.relative_to(root))], "work answer: %s" % name, write)
    else:
        workqueue.committed(root, workqueue.rels_of(root, path), "work answer: %s awaiting-answer -> %s" % (name, status), write)
    return status
