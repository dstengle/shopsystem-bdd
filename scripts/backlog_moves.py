"""The commands that change an item of the backlog (capability backlog), each one commit of that item's file, with a
message naming the item by its label (workflow simplification plan 2, D3, D5)."""
import workqueue
from backlog_items import (
    PROVENANCES,
    RATINGS,
    Item,
    Refused,
    commit,
    find,
    items,
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


CLOSED = ("delivered", "refused", "withdrawn")


def rate(root, name, value=None, urgency=None, size=None):
    """Set each rating given, to one of the glossary's values (r4, D6); an item that is closed keeps its ratings."""
    given = {k: v for k, v in (("value", value), ("urgency", urgency), ("size", size)) if v is not None}
    for key, rating in given.items():
        if rating not in RATINGS[key]:
            raise Refused("work rate: the %s %s is not one of %s" % (key, rating, ", ".join(RATINGS[key])))
    item = find(root, name)
    if not given:
        raise Refused("work rate: %s: give --value, --urgency or --size" % label(item))
    if item.status in CLOSED:
        raise Refused("work rate: %s is %s; work rate takes an item that is not %s" % (label(item), item.status,
                                                                                     either(CLOSED)))
    for key, rating in given.items():
        setattr(item, key, rating)
    commit(root, item, "work rate: %s %s" % (label(item), " ".join("%s=%s" % kv for kv in given.items())))
    return item


def cycle(root, name, on):
    """The path from `on` back to `name` over `depends_on`, as names, or None: the cycle a dependency of `name` on
    `on` would close. Each item is visited once, so a cycle written by hand ends the walk."""
    by_name = {i.name: i for i in items(root)}
    stack, seen = [[on]], {on}
    while stack:
        path = stack.pop()
        if path[-1] == name:
            return path
        for nxt in reversed(by_name[path[-1]].depends_on if path[-1] in by_name else ()):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(path + [nxt])
    return None


def depend(root, name, on):
    """Write the dependency of `name` on `on` in `name`'s file (r5): an item there is not, itself, a dependency it
    already has and one that closes a cycle are refused."""
    item, target = find(root, name), find(root, on)
    if on == name:
        raise Refused("work depend: %s cannot depend on itself" % label(item))
    if on in item.depends_on:
        raise Refused("work depend: %s already depends on %s" % (label(item), label(target)))
    path = cycle(root, name, on)
    if path is not None:
        by_name = {i.name: i for i in items(root)}
        raise Refused("work depend: %s on %s closes the cycle %s" % (label(item), label(target), " -> ".join(
            label(by_name[n]) for n in [name] + path)))
    item.depends_on += (on,)
    commit(root, item, "work depend: %s on %s" % (label(item), label(target)))
    return item
