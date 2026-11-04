"""The commands that change an item of the backlog (capability backlog), each one commit of that item's file, with a
message naming the item by its label (workflow simplification plan 2, D3, D5)."""
import workqueue
from backlog_items import PROVENANCES, Item, Refused, commit, label, next_name, one_line


def text_line(text, what):
    """One line of text for an item's body: a heading's `#` would read as the file's own."""
    text = one_line(text, what)
    if text.startswith("#"):
        raise Refused("the %s starts with #, which would read as a heading" % what)
    return text


def idea(root, title, provenance="own", note=None):
    """Write a new item that is `idea` and commit it (r1); adding an idea starts no work."""
    title = one_line(title, "title")
    if provenance not in PROVENANCES:
        raise Refused("the provenance %s is not one of %s" % (provenance, ", ".join(PROVENANCES)))
    sections = {"Notes": text_line(note, "note")} if note is not None else {}
    name = next_name(root)
    item = Item(name=name, ident="item/%s/%s" % (workqueue.context_path(root), name), title=title, status="idea",
                provenance=provenance, sections=sections)
    commit(root, item, "work idea: %s idea" % label(item))
    return item
