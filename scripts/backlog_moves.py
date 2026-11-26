"""The commands that change an item of the backlog (capability backlog), each one commit of that item's file, with a
message naming the item by its label (workflow simplification plan 2, D3, D5)."""
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
    shaping_note,
)
from plumbing import shop_files

# The moves of an item's status that a command makes, before -> after: the glossary's transitions of `status` of item
# by `work shape`, `work refuse`, `work withdraw`, `work answer`, `work ready` and `work reopen`, and tracking's
# operations execution requests (backlog_lifecycle, b578).
TRANSITIONS = {"work shape": {"idea": "shaped"},
               "work refuse": {"idea": "refused", "shaped": "refused"},
               "work withdraw": {"idea": "withdrawn", "shaped": "withdrawn", "ready": "withdrawn",
                                 "needs-input": "withdrawn"},
               "work answer": {"needs-input": "shaped"},
               "work ready": {"shaped": "ready"},
               "work reopen": {"ready": "shaped"},
               "work allocate": {"ready": "in-batch"},
               "work deliver": {"in-batch": "delivered"},
               "work restore": {"in-batch": "ready"},
               "work suspend": {"in-batch": "needs-input"}}


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
    item = Item(name=name, ident="item/%s/%s" % (shop_files.context_path(root), name), title=title, status="idea",
                provenance=provenance, sections=sections)
    commit(root, item, "work idea: %s idea" % label(item))
    return item


def either(words):
    words = list(words)
    return words[0] if len(words) == 1 else "%s or %s" % (", ".join(words[:-1]), words[-1])


def moved(item, command, change=None, reason=None):
    """Move `item` by its command's row in memory and let `change` write into it, a status the row lacks refused,
    naming it (r3) and the operation's declared `reason` when it has one (items r60-r63); the status it had."""
    row = TRANSITIONS[command]
    if item.status not in row:
        said = "%s: %s is %s; %s takes an item that is %s" % (command, label(item), item.status, command, either(row))
        raise Refused(said + (": %s" % reason if reason else ""), reason=reason, names=["item:%s" % item.name])
    before, item.status = item.status, row[item.status]
    if change is not None:
        change(item)
    return before


def move(root, name, command, change=None, reason=None):
    """Move the item `name` by its command's row (`moved`) and commit it."""
    item = find(root, name)
    before = moved(item, command, change, reason)
    commit(root, item, "%s: %s %s -> %s" % (command, label(item), before, item.status))
    return item


def add_note(item, note):
    if note is not None:
        from backlog_note import with_note
        with_note(item, note)


def shape(root, name, note=None):
    """`idea` -> `shaped` (r37), with a line under ## Notes when one is given; an idea with no shaping note and no
    `--note` refused, naming the option (r43)."""
    note = text_line(note, "note") if note is not None else None

    def write(item):
        if note is None and not shaping_note(item):
            raise Refused("work shape: %s has no shaping note; give it one with the --note option" % label(item))
        add_note(item, note)
    return move(root, name, "work shape", write)


def refuse(root, name, reason):
    """`idea` or `shaped` -> `refused` (r13, r14), the reason under ## Refused."""
    reason = text_line(reason, "reason")
    return move(root, name, "work refuse", lambda item: item.sections.__setitem__("Refused", reason))


def withdraw(root, name, reason):
    """`idea`, `shaped`, `ready` or `needs-input` -> `withdrawn` (items#r42), the reason under its `## Withdrawn` as
    `work merge` keeps its own (b465)."""
    reason = text_line(reason, "reason")
    return move(root, name, "work withdraw", lambda item: item.sections.__setitem__("Withdrawn", reason))


def reopen(root, name):
    """`ready` -> `shaped` (items#r31), so that its lines can change before `work ready` again; an item that is not
    `ready` refused, naming it (items#r32)."""
    return move(root, name, "work reopen", reason="item not ready")


def answer(root, name, text):
    """`needs-input` -> `shaped` (r16): the question and its answer under ## Answers, and ## Question removed (D17)."""
    text = text_line(text, "answer")

    def write(item):
        question = item.sections.pop("Question", None)
        pair = ("- Q: %s\n  A: %s" % (" ".join(question.split()), text)) if question else "- A: %s" % text
        had = item.sections.get("Answers")
        item.sections["Answers"] = "%s\n%s" % (had, pair) if had else pair
    return move(root, name, "work answer", write)


def ready(root, name):
    """`shaped` -> `ready` (items#r1, r2): refused with every reason the bar gives, so nothing is committed (D8); a
    `ready` item checked again, kept as it is when it passes (items#r35) and refused with the reasons when it does not
    (items#r36); any other item refused, naming it (items#r37). The bar checks a copy of the item with its ids
    renumbered past its capabilities', as the pick does, so ids a merged batch took do not refuse it; the item keeps
    its own ids (items#r66, r67, b648). The item and the bar's warnings."""
    import copy

    import backlog_lines
    import readiness_bar
    warnings = []

    def check(item):
        renumbered = copy.deepcopy(item)
        backlog_lines.renumber(root, renumbered, {})
        reasons, warns = readiness_bar.check(root, renumbered)
        if reasons:
            raise Refused("work ready: %s is not passing:\n%s" % (label(item), "\n".join("  " + r for r in reasons)))
        warnings.extend(warns)
    item = find(root, name)
    if item.status == "ready":
        check(item)
        return item, warnings
    if item.status != "shaped":
        raise Refused("work ready: %s is %s; work ready takes an item that is shaped or ready" % (
            label(item), item.status))
    return move(root, name, "work ready", check), warnings


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
    """Write the dependency of `name` on `on` in `name`'s file (r5): an item there is not, one refused or withdrawn,
    itself, a dependency it already has and one that closes a cycle are refused."""
    item, target = find(root, name), find(root, on)
    if on == name:
        raise Refused("work depend: %s cannot depend on itself" % label(item))
    if target.status in ("refused", "withdrawn"):     # it is never delivered: it would block for good (Q1)
        raise Refused("work depend: %s is %s; %s would be blocked by it for good" % (
            label(target), target.status, label(item)))
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


def undepend(root, name, on):
    """The dependency of `name` on `on` dropped from its file (plan 4, D27); `on` need not be an item there is. A
    dependency `name` does not have is refused."""
    item = find(root, name)
    if on not in item.depends_on:
        raise Refused("work depend: %s does not depend on %s" % (label(item), on))
    item.depends_on = tuple(d for d in item.depends_on if d != on)
    commit(root, item, "work depend: %s no longer on %s" % (label(item), on))
    return item
