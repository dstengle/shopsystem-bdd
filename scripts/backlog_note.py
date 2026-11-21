"""`work annotate` and `work merge` (b281): a note added to an open item, and an open item withdrawn into the item that
takes its place, with the reason; each one commit of the item's file, read just before it is written so that what
another commit wrote to it is kept (backlog.annotate, backlog.merge)."""
from backlog_items import Refused, commit, find, label

OPEN = ("idea", "shaped", "ready", "needs-input")


def with_note(item, note):
    """`note` appended to the item's ## Notes; a ## Notes it has not yet goes first, never after ## Requirements."""
    had = item.sections.get("Notes")
    if had:
        item.sections["Notes"] = "%s\n%s" % (had, note)
    elif "Notes" in item.sections:
        item.sections["Notes"] = note
    else:
        item.sections = {"Notes": note, **item.sections}


def _open(item, command):
    if item.status not in OPEN:
        raise Refused("%s: %s is %s; %s takes an item that is %s" % (command, label(item), item.status, command,
                                                                    ", ".join(OPEN[:-1]) + " or " + OPEN[-1]))


def note(root, name, text):
    """A line under ## Notes of an item that is open (items#r38); a closed one refused, naming it (items#r39)."""
    from backlog_moves import text_line
    item = find(root, name)
    _open(item, "work annotate")
    with_note(item, text_line(text, "note"))
    commit(root, item, "work annotate: %s" % label(item))
    return item


def merge(root, name, into, reason):
    """An open item `withdrawn` into the item `into` (items#r33), `## Withdrawn` saying which and why; a closed item
    refused, naming it (items#r34), and a successor that is the item itself or closed refused, naming it."""
    from backlog_moves import text_line
    item = find(root, name)
    _open(item, "work merge")
    reason = text_line(reason, "reason")
    successor = find(root, into)
    if successor.name == item.name:
        raise Refused("work merge: %s cannot be merged into itself" % label(item))
    if successor.status in ("delivered", "refused", "withdrawn"):
        raise Refused("work merge: %s is %s; an item is merged into one that is not closed" % (
            label(successor), successor.status))
    before, item.status = item.status, "withdrawn"
    item.sections["Withdrawn"] = "Merged into %s: %s" % (label(successor), reason)
    commit(root, item, "work merge: %s %s -> withdrawn, into %s" % (label(item), before, label(successor)))
    return item


def add_parsers(sub):
    p = sub.add_parser("annotate", help="add a line to the ## Notes of an item that is idea, shaped, ready or needs-input")
    p.add_argument("name")
    p.add_argument("note")
    p = sub.add_parser("merge", help="withdraw an item that is idea, shaped, ready or needs-input into the item that "
                       "takes its place, with the reason")
    p.add_argument("name")
    p.add_argument("--into", required=True, help="the item that takes its place")
    p.add_argument("--reason", required=True, help="why, written under the item's ## Withdrawn")


def cmd_note(args):
    item = note(args.root, args.name, args.note)
    print("%s: a note" % label(item))
    return 0


def cmd_merge(args):
    item = merge(args.root, args.name, args.into, args.reason)
    print("%s %s" % (label(item), item.status))
    return 0


COMMANDS = {"annotate": cmd_note, "merge": cmd_merge}
