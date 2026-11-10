"""The backlog's commands of `work` (capability backlog): their parsers, what they print, and their dispatch, so that
scripts/work stays small. Every line names an item by its label, `b3 "Fix the parser"` (design goal 10)."""
import argparse
import json
import sys

import backlog_forms
import backlog_items
import backlog_lines
import backlog_moves
import backlog_view


class _LineParser(argparse.ArgumentParser):
    """`work line b1 --into CAP TEXT`: argparse (before 3.12) gives the optional positional TEXT nothing at `b1` and
    then finds TEXT left over after the options; it is taken as TEXT here, as is one word after `--`."""

    def parse_known_args(self, args=None, namespace=None):
        found, extras = super().parse_known_args(args, namespace)
        if found.text is None and len(extras) == 1 and not extras[0].startswith("-"):
            found.text = extras.pop()
        elif found.text is None and len(extras) == 2 and extras[0] == "--":
            found.text, extras = extras[1], []
        return found, extras


def add_parsers(sub):
    """The backlog's subcommands, beside `work`'s own."""
    p = sub.add_parser("idea", help="write a new item of the backlog that is idea, and commit it")
    p.add_argument("title")
    p.add_argument("--provenance", default="own", choices=backlog_items.PROVENANCES)
    p.add_argument("--note", help="a line under the item's ## Notes")
    p = sub.add_parser("backlog", help="every item of the backlog, a table a state, in rank order, with what each waits on")
    p.add_argument("--json", action="store_true", help="print one JSON object instead of tables")
    p = sub.add_parser("shape", help="move an item that is idea to shaped")
    p.add_argument("name")
    p.add_argument("--note", help="a line under the item's ## Notes")
    p = sub.add_parser("refuse", help="move an item that is idea or shaped to refused, with the reason")
    p.add_argument("name")
    p.add_argument("reason")
    p = sub.add_parser("rate", help="set an item's value, urgency or size, to the glossary's values")
    p.add_argument("name")
    for key, values in backlog_items.RATINGS.items():
        p.add_argument("--" + key, help=", ".join(values))
    p = sub.add_parser("depend", help="write in an item that it depends on another item (--on), or drop a dependency it has (--drop)")
    p.add_argument("name")
    on = p.add_mutually_exclusive_group(required=True)
    on.add_argument("--on", help="the item it depends on")
    on.add_argument("--drop", help="an item it depends on, the dependency to drop")
    p = sub.add_parser("ready", help="move an item that is shaped to ready, when it passes the readiness bar")
    p.add_argument("name")
    p = sub.add_parser("line", help="write a requirement line (or a term bullet, relation row, given block, universal "
                       "condition or upstream entry) into an item's ## Requirements, and commit it")
    p.__class__ = _LineParser
    p.add_argument("name")
    p.add_argument("--into", help="the codified capability the line (term, relation row, given block) goes into")
    where = p.add_mutually_exclusive_group()
    where.add_argument("--group", help="the title of the new group the line opens (default: the item's title)")
    where.add_argument("--in", dest="in_group", help="the item's group g<n> the line joins")
    p.add_argument("text", nargs="?", help="the requirement line (or --term)")
    p.add_argument("--retires", metavar="CAP#rN", help="the live requirement `<capability>#r<n>` the line replaces: "
                   "its id goes under the block's retired:, the line into that capability; with --universal, the "
                   "live universal condition `universal#U<n>` it replaces")
    p.add_argument("--term", help="a term bullet for the capability's ## Terms, in place of a line")
    p.add_argument("--recodify", metavar="CAP", help="the codified capability the item switches to the new language: "
                   "`language: codified-2` written into its block (`universal`: spec/universal.md)")
    p.add_argument("--relation", help="a row `| from | word | to | cardinality |` for the capability's ## Relations")
    p.add_argument("--given", nargs=2, metavar=("GROUP", "BLOCK"),
                   help="the given block of the item's group g<n> in the capability: example data, one line a row")
    p.add_argument("--universal", help="a universal condition for spec/universal.md, with no --into")
    p.add_argument("--upstream", help="an upstream entry `bounded-context/<path>: ..., github: <owner>/<name>` for "
                   "spec/index.md's ## Upstreams, with no --into")


def cmd_idea(args):
    item = backlog_moves.idea(args.root, args.title, args.provenance, args.note)
    return moved(item)


def moved(item):
    print("%s %s" % (backlog_items.label(item), item.status))
    return 0


def cmd_shape(args):
    return moved(backlog_moves.shape(args.root, args.name, args.note))


def cmd_refuse(args):
    return moved(backlog_moves.refuse(args.root, args.name, args.reason))


def cmd_rate(args):
    return moved(backlog_moves.rate(args.root, args.name, args.value, args.urgency, args.size))


def cmd_depend(args):
    if args.drop is not None:
        item = backlog_moves.undepend(args.root, args.name, args.drop)
        try:
            dropped = backlog_items.label(backlog_items.find(args.root, args.drop))
        except backlog_items.Refused:
            dropped = "%s (missing)" % args.drop
        print("%s no longer depends on %s" % (backlog_items.label(item), dropped))
        return 0
    item = backlog_moves.depend(args.root, args.name, args.on)
    print("%s depends on %s" % (backlog_items.label(item), backlog_items.label(backlog_items.find(args.root, args.on))))
    return 0


PIECES = ("text", "term", "relation", "given", "universal", "upstream", "recodify")


def cmd_line(args):
    """`work line`: it parses nothing; `work ready` is the check (D5). One piece a run: a line, or one flag's piece."""
    given = [k for k in PIECES if getattr(args, k) is not None]
    if len(given) != 1:
        raise backlog_items.Refused("work line: give one of a requirement line, --term, --relation, --given, "
                                    "--universal, --upstream or --recodify")
    piece = given[0]
    if piece == "recodify":
        if args.into is not None or args.retires is not None:
            raise backlog_items.Refused("work line: --recodify takes no --into or --retires")
        item = backlog_lines.recodify(args.root, args.name, args.recodify)
        print("%s: %s recodified" % (backlog_items.label(item), args.recodify))
        return 0
    if args.retires is not None and piece == "universal":
        item, ident = backlog_forms.add_universal(args.root, args.name, args.universal, args.retires)
        print("%s: universal#%s retires %s" % (backlog_items.label(item), ident, args.retires))
        return 0
    if args.retires is not None:
        if piece != "text":
            raise backlog_items.Refused("work line: --retires takes a requirement line, not --%s" % piece)
        item, ident = backlog_lines.retire(args.root, args.name, args.retires, args.text, args.into, args.group,
                                           args.in_group)
        print("%s: %s retires %s" % (backlog_items.label(item), ident, args.retires))
        return 0
    if (args.into is None) != (piece in ("universal", "upstream")):
        raise backlog_items.Refused("work line: %s %s --into <capability>" % (
            "--" + piece if piece != "text" else "a requirement line", "takes no" if args.into else "takes"))
    if piece == "text":
        item, ident = backlog_lines.add_line(args.root, args.name, args.into, args.text, args.group, args.in_group)
        print("%s: %s" % (backlog_items.label(item), ident))
        return 0
    if piece == "universal":
        item, ident = backlog_forms.add_universal(args.root, args.name, args.universal)
        print("%s: universal#%s" % (backlog_items.label(item), ident))
        return 0
    if piece == "term":
        item, said = backlog_lines.add_term(args.root, args.name, args.into, args.term), "a term of %s" % args.into
    elif piece == "relation":
        item = backlog_forms.add_relation(args.root, args.name, args.into, args.relation)
        said = "a relation row of %s" % args.into
    elif piece == "given":
        item = backlog_forms.add_given(args.root, args.name, args.into, *args.given)
        said = "a given block of %s#%s" % (args.into, args.given[0])
    else:
        item, said = backlog_forms.add_upstream(args.root, args.name, args.upstream), "an upstream entry"
    print("%s: %s" % (backlog_items.label(item), said))
    return 0


def cmd_ready(args):
    """`work ready`: the bar's warnings on stderr, the item's label and `ready` on stdout."""
    item, warnings = backlog_moves.ready(args.root, args.name)
    for warning in warnings:
        print("work ready: warning: %s" % warning, file=sys.stderr)
    return moved(item)


def cmd_backlog(args):
    """`work backlog`: it only reads, and commits nothing."""
    if args.json:
        print(json.dumps(backlog_view.as_json(args.root)))
    else:
        print(backlog_view.tables(args.root), end="")
    return 0


def withdraw(args):
    """`work withdraw b<n>`."""
    return moved(backlog_moves.withdraw(args.root, args.name))


def answer(args):
    """`work answer b<n> TEXT`."""
    return moved(backlog_moves.answer(args.root, args.name, args.answer))


COMMANDS = {"idea": cmd_idea, "shape": cmd_shape, "refuse": cmd_refuse, "rate": cmd_rate, "depend": cmd_depend,
            "backlog": cmd_backlog, "line": cmd_line, "ready": cmd_ready}


def show(args):
    """`work show b<n>`: the item, its label first; with --json one object `{"item": {...}}`."""
    item = backlog_items.find(args.root, args.target)
    if args.json:
        items = backlog_items.items(args.root)
        print(json.dumps({"item": backlog_view.row_json(item, {i.name: i for i in items},
                                                        backlog_view.rank_of(item, items), args.root)}))
        return 0
    print(backlog_items.label(item))
    for key in ("status", "provenance", *backlog_items.RATINGS):
        print("  %s: %s" % (key, getattr(item, key) or "-"))
    by_name = {i.name: i for i in backlog_items.items(args.root)}
    print("  depends on: %s" % (", ".join(backlog_items.label(by_name[n]) if n in by_name else "%s (missing)" % n
                                          for n in item.depends_on) or "-"))
    for heading, text in item.sections.items():
        print("\n## %s\n\n%s" % (heading, text))
    return 0
