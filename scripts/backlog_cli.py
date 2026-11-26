"""The backlog's commands of `work` (capability backlog): their parsers, what they print, and their dispatch, so that
scripts/work stays small. Every line names an item by its label, `b3 "Fix the parser"` (design goal 10)."""
import argparse
import json
import sys

import backlog_items


class _LineParser(argparse.ArgumentParser):
    """`work line b1 --into CAP TEXT`: argparse (before 3.12) gives the optional positional TEXT nothing at `b1`, then
    finds TEXT left over; it is taken as TEXT here, as are one word after `--` and a bullet opening with "- " (b800)."""

    def parse_known_args(self, args=None, namespace=None):
        found, extras = super().parse_known_args(args, namespace)
        if found.text is None and len(extras) == 1 and (not extras[0].startswith("-") or extras[0].startswith("- ")):
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
    p = sub.add_parser("reopen", help="move an item that is ready back to shaped, so that its lines can change")
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
                   "live universal condition `universal#U<n>` it replaces; each design-decision whose enforced_by names "
                   "the requirement is named")
    p.add_argument("--retirement-list", metavar="FILE", help="a file of pairs `<capability>#r<n> <line>`, each line "
                   "retiring its live requirement as --retires does, all in one commit; refused whole on an id no "
                   "requirement has")
    p.add_argument("--no-line", action="store_true", help="with --retires: the live requirement retired with no line "
                   "replacing it, its id under the block's retired: and no line written")
    p.add_argument("--reword", metavar="CAP#rN", help="the item's own line `<capability>#r<n>` the requirement line "
                   "takes the place of, keeping its id and group")
    p.add_argument("--remove", metavar="CAP#rN|CAP", help="the item's own line `<capability>#r<n>` taken out, "
                   "an id it retires reinstated, or a bare <capability>: its whole block and model lines")
    p.add_argument("--term", action="append", help="a term bullet for the capability's ## Terms (with a domain "
                   "model, a vocabulary entry for its area), in place of a line; given again, all in one commit")
    p.add_argument("--recodify", metavar="CAP", help="the codified capability the item switches to the new language: "
                   "`language: codified-2` written into its block (`universal`: spec/universal.md)")
    p.add_argument("--relation", help="a row `| from | word | to | cardinality |` for the capability's ## Relations; "
                   "with a domain model, `<object>: <phrase> → <object> (<cardinality>)` for its area's model")
    p.add_argument("--model", help="with a domain model: model lines for the area of the capability --into names")
    p.add_argument("--given", nargs=2, metavar=("GROUP", "BLOCK"),
                   help="the given block of the item's group g<n> in the capability: example data, one line a row")
    p.add_argument("--universal", help="a universal condition for spec/universal.md, with no --into")
    p.add_argument("--capability", help="a capability new to the context, written as a block of the item with "
                   "--narrator, --group (service or guarantees, default service) and its purpose as the text")
    p.add_argument("--narrator", help="with --capability: who the new capability's lines speak for")
    for module in ("backlog_capability", "backlog_adapter", "backlog_pack") + EDITS:
        __import__(module).add_arguments(p)
    p.add_argument("--upstream", help="an upstream entry `bounded-context/<path>: ..., github: <owner>/<name>` for "
                   "spec/index.md's ## Upstreams, with no --into")


def cmd_idea(args):
    import backlog_moves
    item = backlog_moves.idea(args.root, args.title, args.provenance, args.note)
    return moved(item)


def moved(item):
    print("%s %s" % (backlog_items.label(item), item.status))
    return 0


def cmd_shape(args):
    import backlog_moves
    return moved(backlog_moves.shape(args.root, args.name, args.note))


def cmd_refuse(args):
    import backlog_moves
    return moved(backlog_moves.refuse(args.root, args.name, args.reason))


def cmd_reopen(args):
    import backlog_moves
    return moved(backlog_moves.reopen(args.root, args.name))


def cmd_rate(args):
    import backlog_moves
    return moved(backlog_moves.rate(args.root, args.name, args.value, args.urgency, args.size))


def cmd_depend(args):
    import backlog_moves
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


PIECES = ("text", "term", "relation", "given", "universal", "upstream", "recodify", "model")
EDITS = ("backlog_area_move", "backlog_import", "backlog_model_edit", "backlog_piece_edit", "backlog_reinstate", "backlog_retire", "backlog_serves", "backlog_relied")  # their own `work line`s


def _change_shape(args):
    """The options of `work line --reword` or `--remove` refused before the item is read: one of them, alone."""
    others = [k for k in PIECES[1:] + ("into", "retires", "group", "in_group") if getattr(args, k) is not None]
    if (args.reword is not None) == (args.remove is not None) or others:
        raise backlog_items.Refused("work line: --reword takes a requirement line and --remove none, one of them, "
                                    "with no other option")


def _changed(args):
    """`work line --reword <cap>#r<n> <line>` and `work line --remove <cap>#r<n>` (b14): an item's own line."""
    import backlog_reword
    if args.reword is not None:
        if args.text is None:
            raise backlog_items.Refused("work line: --reword %s takes the requirement line" % args.reword)
        item = backlog_reword.reword(args.root, args.name, args.reword, args.text)
        print("%s: %s reworded" % (backlog_items.label(item), args.reword))
    else:
        if args.text is not None:
            raise backlog_items.Refused("work line: --remove %s takes no requirement line" % args.remove)
        item = backlog_reword.remove(args.root, args.name, args.remove)
        print("%s: %s removed" % (backlog_items.label(item), args.remove))
    return 0


def _unreplaced(args):
    """`work line --no-line --retires <cap>#r<n>` (b271): the live requirement retired with no line replacing it."""
    import backlog_lines
    others = [k for k in PIECES + ("reword", "remove", "group", "in_group") if getattr(args, k) is not None]
    if args.retires is None or others:
        raise backlog_items.Refused("work line: --no-line takes --retires <capability>#r<n> (and --into), with no "
                                    "requirement line or other piece")
    item = backlog_lines.retire(args.root, args.name, args.retires, None, args.into)[0]
    print("%s: retires %s" % (backlog_items.label(item), args.retires))
    _enforcing(args)
    return 0


def _enforcing(args):
    """Each design-decision the retired requirement enforces, named (drafting r28)."""
    import decision_amend
    for line in decision_amend.enforcing(args.root, args.retires):
        print(line)


def _modelled(root):
    import domain_model
    return domain_model.exists(root)


def cmd_line(args):
    """`work line`: it parses nothing; `work ready` is the check (D5). One piece a run: a line, or one flag's piece."""
    import backlog_chore
    import backlog_forms
    import backlog_lines
    if args.reword is not None or args.remove is not None:
        _change_shape(args)
    backlog_chore.refuse_line(args.root, args.name)
    if args.capability is not None:
        import backlog_capability
        return backlog_capability.cmd(args)
    if args.expose is not None or args.withhold is not None:
        return __import__("backlog_adapter").cmd(args)
    if args.pack is not None:
        return __import__("backlog_pack").cmd(args)
    for module in EDITS:
        if __import__(module).given(args):
            return __import__(module).cmd(args)
    if args.retirement_list is not None:
        import backlog_retirements
        return backlog_retirements.cmd(args)
    if args.no_line:
        return _unreplaced(args)
    if args.reword is not None or args.remove is not None:
        return _changed(args)
    given = [k for k in PIECES if getattr(args, k) is not None]
    if len(given) != 1:
        raise backlog_items.Refused("work line: give one of a requirement line, --term, --relation, --model, "
                                    "--given, --universal, --upstream or --recodify")
    piece = given[0]
    backlog_forms.refuse_beside(args, piece)
    if piece == "recodify":
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
        _enforcing(args)
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
    if piece in ("term", "relation", "model") and (piece == "model" or _modelled(args.root)):
        import backlog_model
        item, said = backlog_model.add(args.root, args.name, args.into, **{piece: getattr(args, piece)})
    elif piece == "term":
        item = backlog_lines.add_term(args.root, args.name, args.into, args.term)
        said = "%s of %s" % ("a term" if len(args.term) == 1 else "%d terms" % len(args.term), args.into)
    elif piece == "relation":
        item = backlog_forms.add_relation(args.root, args.name, args.into, args.relation)
        said = "a relation row of %s" % args.into
    elif piece == "given":
        item = backlog_forms.add_given(args.root, args.name, args.into, *args.given)
        said = "a given block of %s#%s" % (args.into, args.given[0])
    else:
        item, said = backlog_forms.add_upstream(args.root, args.name, args.upstream), "an upstream entry"
    print("%s: %s" % (backlog_items.label(item), said))
    return backlog_lines.warn_terms(args.root, item, args.term if piece == "term" else ())   # b801


def cmd_ready(args):
    """`work ready`: the bar's warnings on stderr, the item's label and `ready` on stdout."""
    import backlog_moves
    item, warnings = backlog_moves.ready(args.root, args.name)
    for warning in warnings:
        print("work ready: warning: %s" % warning, file=sys.stderr)
    return moved(item)


def cmd_backlog(args):
    """`work backlog`: it only reads, and commits nothing."""
    import backlog_view
    if args.json:
        print(json.dumps(backlog_view.as_json(args.root)))
    else:
        print(backlog_view.tables(args.root), end="")
    return 0


def withdraw(args):
    """`work withdraw b<n> --reason R`."""
    import backlog_moves
    return moved(backlog_moves.withdraw(args.root, args.name, args.reason))


def answer(args):
    """`work answer b<n> TEXT`."""
    import backlog_moves
    return moved(backlog_moves.answer(args.root, args.name, args.answer))


COMMANDS = {"idea": cmd_idea, "shape": cmd_shape, "refuse": cmd_refuse, "rate": cmd_rate, "depend": cmd_depend,
            "backlog": cmd_backlog, "line": cmd_line, "ready": cmd_ready,
            "reopen": cmd_reopen}

