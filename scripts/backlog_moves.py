"""The commands that change an item of the backlog (capability backlog), each one commit of that item's file, with a
message naming the item by its label (workflow simplification plan 2, D3, D5)."""
import workqueue
from backlog_items import (
    PROVENANCES,
    Item,
    Refused,
    commit,
    find,
    label,
    next_name,
    one_line,
)

# The moves of an item's status that a command makes, before -> after: the glossary's transitions of `status` of item
# by `work shape`, `work refuse`, `work withdraw` and `work answer`.
TRANSITIONS = {"work shape": {"idea": "shaped"},
               "work refuse": {"idea": "refused", "shaped": "refused"},
               "work withdraw": {"idea": "withdrawn", "shaped": "withdrawn", "ready": "withdrawn",
                                 "needs-input": "withdrawn"},
               "work answer": {"needs-input": "shaped"}}


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


def either(words):
    words = list(words)
    return words[0] if len(words) == 1 else "%s or %s" % (", ".join(words[:-1]), words[-1])


def move(root, name, command, change=None):
    """Move the item `name` by its command's row, let `change` write into it, and commit it; a status the row lacks is
    refused, naming it (r3)."""
    item = find(root, name)
    row = TRANSITIONS[command]
    if item.status not in row:
        raise Refused("%s: %s is %s; %s takes an item that is %s" % (command, label(item), item.status, command,
                                                                    either(row)))
    before, item.status = item.status, row[item.status]
    if change is not None:
        change(item)
    commit(root, item, "%s: %s %s -> %s" % (command, label(item), before, item.status))
    return item


def add_note(item, note):
    if note is not None:
        had = item.sections.get("Notes")
        item.sections["Notes"] = "%s\n%s" % (had, note) if had else note


def shape(root, name, note=None):
    """`idea` -> `shaped` (r2), with a line under ## Notes when one is given."""
    note = text_line(note, "note") if note is not None else None
    return move(root, name, "work shape", lambda item: add_note(item, note))


def refuse(root, name, reason):
    """`idea` or `shaped` -> `refused` (r13, r14), the reason under ## Refused."""
    reason = text_line(reason, "reason")
    return move(root, name, "work refuse", lambda item: item.sections.__setitem__("Refused", reason))


def withdraw(root, name):
    """`idea`, `shaped`, `ready` or `needs-input` -> `withdrawn` (r9-r12)."""
    return move(root, name, "work withdraw")


def answer(root, name, text):
    """`needs-input` -> `shaped` (r16): the question and its answer under ## Answers, and ## Question removed (D17)."""
    text = text_line(text, "answer")

    def write(item):
        question = item.sections.pop("Question", None)
        pair = ("- Q: %s\n  A: %s" % (" ".join(question.split()), text)) if question else "- A: %s" % text
        had = item.sections.get("Answers")
        item.sections["Answers"] = "%s\n%s" % (had, pair) if had else pair
    return move(root, name, "work answer", write)
