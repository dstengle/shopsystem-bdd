"""`work request` and `work take-in` (capability requests r28, r30 to r32, r39 to r45): an asker's repository sends the request
it raises to its upstream's remote (`workqueue_sent`); the upstream takes in, from that remote, what was sent to it, and
keeps each as the fields of a request's form only (r43). Standard library only."""
import workqueue
import workqueue_request
import workqueue_sent
from workqueue import Refused


def raise_request(root, title, asker, lines_file, sources, thread, delegation=None, raised_for=None):
    """Refuse, writing and sending nothing, what r22, the lines file, r2, r32, r30, r31 and r45 refuse, in that order; then
    keep the request here, or, in an asker's repository, send it to its upstream (r28); return its name."""
    if delegation is not None and not delegation.strip():
        raise Refused("the delegation is empty")
    lines = workqueue_request.lines_of(lines_file)
    own = workqueue.context_path(root)
    if asker != own:
        raise Refused("this repository raises no request as %s; it is %s" % (asker, own))
    sending = workqueue_sent.asker(root) is not None
    if sending and sources:
        raise Refused("an origin (--source) belongs to an internal request; a request to an upstream gives --raised-for or --thread")
    if sending and thread is None and raised_for is None:
        raise Refused("the request names neither a request it is raised for nor a job-thread")
    if not sending and not sources and thread is None and raised_for is None:
        raise Refused(workqueue_request.NO_ORIGIN)
    if not sending:
        return workqueue_request.store(root, None, title, asker, lines, sources, thread, delegation, raised_for)
    name = workqueue_sent.next_request(root)
    workqueue_sent.send(root, {"kind": "request", "id": name, "asker": asker, "title": title, "lines": lines,
                               "sources": sources, "thread": thread, "raised_for": raised_for, "delegation": delegation})
    return name


def _left(item):
    """What an untaken item is called in the telling."""
    if item["kind"] == "request":
        return "the request %s" % item["id"]
    return "the %s on %s" % (item["kind"], item["request"])


def take_in(root):
    """Take in, from the upstream's remote, every request and message sent to it, in the order sent, and print one line for
    each it leaves untaken: the asker id it came under is not one the upstream allows for the asker it names (r41). An item
    taken in is off the remote; one left stays on it. A repository with no `[upstream]` setting takes in nothing."""
    conf = workqueue_sent.upstream(root)
    if conf is None:
        return
    own = workqueue.context_path(root)
    for who, number, item in workqueue_sent.sent(root, conf["remote"]):
        if item.get("asker") not in (conf.get("allow") or {}).get(who, []):
            print("left %s untaken because the asker id %s is not one %s allows for the asker %s"
                  % (_left(item), who, own, item.get("asker")))
            continue
        if item["kind"] == "request":
            lines = item["lines"]
            workqueue_request.strict(lines)
            workqueue_request.store(root, item["id"], item["title"], item["asker"], lines, item["sources"] or [],
                                    item["thread"], item["delegation"], item["raised_for"])
        elif item["kind"] == "answer":
            workqueue_request.reply(root, item["request"], item["question"], item["text"], taken_in=item["asker"])
        elif item["kind"] == "turn":
            workqueue_request.turn(root, item["request"])
        workqueue_sent.drop(root, who, number)
