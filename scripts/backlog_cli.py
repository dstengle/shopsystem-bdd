"""The backlog's commands of `work` (capability backlog): their parsers, what they print, and their dispatch, so that
scripts/work stays small. Every line names an item by its label, `b3 "Fix the parser"` (design goal 10)."""
import json

import backlog_items
import backlog_moves


def add_parsers(sub):
    """The backlog's subcommands, beside `work`'s own."""
    p = sub.add_parser("idea", help="write a new item of the backlog that is idea, and commit it")
    p.add_argument("title")
    p.add_argument("--provenance", default="own", choices=backlog_items.PROVENANCES)
    p.add_argument("--note", help="a line under the item's ## Notes")


def cmd_idea(args):
    item = backlog_moves.idea(args.root, args.title, args.provenance, args.note)
    print("%s %s" % (backlog_items.label(item), item.status))
    return 0


COMMANDS = {"idea": cmd_idea}


def show(args):
    """`work show b<n>`: the item, its label first; with --json one object `{"item": {...}}`."""
    item = backlog_items.find(args.root, args.target)
    if args.json:
        print(json.dumps({"item": backlog_items.as_dict(item)}))
        return 0
    print(backlog_items.label(item))
    for key in ("status", "provenance", *backlog_items.RATINGS):
        print("  %s: %s" % (key, getattr(item, key) or "-"))
    print("  depends on: %s" % (", ".join(item.depends_on) or "-"))
    for heading, text in item.sections.items():
        print("\n## %s\n\n%s" % (heading, text))
    return 0
