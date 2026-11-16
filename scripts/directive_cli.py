"""The directives' commands of `work` (capability conversation, b20), added to `work` by conversation_cli: `work
directive` (the person's words kept as a quote and a live directive citing it, or a directive of an existing quote),
`work directives` (the live ones, `--all` every one, `--hook` what the SessionStart hook prints), `work promote` and
`work drop` (a live directive reviewed), and `work show directive-<n>` (the directive with its quote)."""
import json
import sys
from pathlib import Path

import conversation_quote
import directive
from backlog_view import cell
from shop_files import Refused
from transcripts import Refused as ReadRefused

is_directive = directive.is_directive


def add_parsers(sub):
    p = sub.add_parser("directive", help="keep a short-term direction of the person: their words as a quote and a "
                                         "live directive citing it, .shop/directives/<n>.md, in one commit")
    p.add_argument("words", nargs="?", help="the person's words, as they wrote them")
    p.add_argument("--session", help="the session whose transcript holds them (default: the one the hook kept)")
    p.add_argument("--transcript", help="the transcript file itself")
    p.add_argument("--quote", help="a quote quote-<n> already kept, in place of the words")
    p = sub.add_parser("directives", help="the live directives, with id, date, age and words")
    p.add_argument("--all", action="store_true", help="every directive, with its status")
    p.add_argument("--hook", action="store_true", help="the SessionStart hook: the live directives' words under one "
                                                       "line, nothing when none is live, never failing")
    p = sub.add_parser("promote", help="a live directive promoted to what it became, written first")
    p.add_argument("name", help="the directive, directive-<n>")
    p.add_argument("--to", required=True, help="an item b<n>, a design-decision's id or CLAUDE.md")
    p = sub.add_parser("drop", help="a live directive dropped, with the reason")
    p.add_argument("name", help="the directive, directive-<n>")
    p.add_argument("--why", required=True, help="the reason it is dropped")


def refused(command, why):
    print("work %s: %s" % (command, why), file=sys.stderr)
    return 1


def write(args):
    if (args.words is None) == (args.quote is None):
        return refused("directive", "give the person's words or --quote quote-<n>, one of them")
    try:
        if args.quote is not None:
            found = directive.from_quote(args.root, args.quote)
        else:
            found = directive.write(args.root, args.words, args.session, args.transcript)
    except (Refused, ReadRefused) as why:
        return refused("directive", why)
    print("%s citing %s" % (directive.label(found), found.quote))
    return 0


def listing(args):
    if args.hook:
        try:
            text = directive.hook_text(Path.cwd())
        except Exception:  # noqa: BLE001  (a hook never fails a session's start)
            return 0
        if text:
            print(text)
        return 0
    try:
        found = [d for d in directive.directives(args.root) if args.all or d.status == "live"]
    except Refused as why:
        return refused("directives", why)
    if not found:
        print("there is no %sdirective in %s/" % ("" if args.all else "live ", directive.DIRECTIVES.as_posix()))
        return 0
    head = ["id", "date", "age", *(["status"] if args.all else []), "words"]
    out = ["| %s |" % " | ".join(head), "|%s" % ("---|" * len(head))]
    for d in found:
        row = [d.name, d.date, directive.age(d), *([d.status] if args.all else []), d.words]
        out.append("| %s |" % " | ".join(cell(c) for c in row))
    print("\n".join(out))
    return 0


def promote(args):
    try:
        found = directive.promote(args.root, args.name, args.to)
    except Refused as why:
        return refused("promote", why)
    print("%s promoted to %s" % (directive.label(found), found.promoted_to))
    return 0


def drop(args):
    try:
        found = directive.drop(args.root, args.name, args.why)
    except Refused as why:
        return refused("drop", why)
    print("%s dropped: %s" % (directive.label(found), found.why))
    return 0


def show(args, show_quote):
    """`work show directive-<n>`: the directive's label, status, date and what it became, then its quote as `work show
    quote-<n>` prints it; with --json one object `{"directive": {...}, "quote": {...}}`."""
    try:
        found = directive.find(args.root, args.target)
        quote = conversation_quote.find(args.root, found.quote)
    except Refused as why:
        return refused("show", why)
    if args.json:
        fields = {"name": found.name, "status": found.status, "date": found.date, "quote": found.quote,
                  "words": found.words, "promoted_to": found.promoted_to, "why": found.why}
        print(json.dumps({"directive": fields, **conversation_quote.as_json(quote)}))
        return 0
    print(directive.label(found))
    print("  status: %s" % found.status)
    print("  date: %s" % found.date)
    if found.promoted_to:
        print("  promoted to: %s" % found.promoted_to)
    if found.why:
        print("  why dropped: %s" % found.why)
    print()
    args.target = quote.name
    return show_quote(args)


COMMANDS = {"directive": write, "directives": listing, "promote": promote, "drop": drop}
