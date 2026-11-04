"""Intake (capability intake; workflow simplification plan 3, D10-D12): a request of this context taken in as an item
(`work intake`), and the item side of `work outcome` on a request an item was taken in from. The request files are
the ones workqueue_request.py keeps; `work intake` changes nothing in the request."""
import re

import workqueue
import workqueue_request
from backlog_items import Item, Refused, commit, items, label, next_name, one_line

TAKES = ("open", "awaiting-upstream")      # the upstream's turn


def provenance_of(root, asker):
    """`own` for this context's own asker, `product` for the product, `peer` for any other bounded context (D10)."""
    if asker == "internal" or asker in workqueue_request.own_askers(root):
        return "own"
    return "product" if (asker or "").startswith("product/") else "peer"


def linked(root, request):
    """The item taken in from `request`, or None."""
    return next((i for i in items(root) if i.request == request), None)


def title_of(text):
    found = re.search(r"(?m)^# (\S.*)$", text)
    return found.group(1).strip() if found else ""


def named(request, text):
    """How `work` names a request: `q<n> "<its title>"` (design goal 10)."""
    return '%s "%s"' % (request, title_of(text))


def intake(root, request):
    """Write the `shaped` item request `request` is taken in as, and commit it alone (D10): titled by the request's
    heading, asked by its asker, its provenance read off the asker. A request already taken in, and one that is not in
    the upstream's turn, are refused."""
    text = workqueue.read(workqueue_request.path_of(root, request), root)
    had = linked(root, request)
    if had is not None:
        raise Refused("work intake: %s was taken in already, as %s" % (named(request, text), label(had)))
    status = workqueue_request.field(text, "status")
    if status not in TAKES:
        raise Refused("work intake: %s is %s; work intake takes a request that is open or awaiting-upstream"
                      % (named(request, text), status))
    asker = workqueue_request.field(text, "asker")
    name = next_name(root)
    item = Item(name=name, ident="item/%s/%s" % (workqueue.context_path(root), name),
                title=one_line(title_of(text), "request's title"), status="shaped",
                provenance=provenance_of(root, asker), request=request, asked_by=asker,
                sections={"Notes": "taken in from request %s" % named(request, text)})
    commit(root, item, "work intake: %s -> %s shaped" % (named(request, text), label(item)))
    return item
