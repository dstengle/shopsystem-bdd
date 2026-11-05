"""The conversation's commands of `work` (capability conversation; workflow simplification plan 8): `work quote`,
`work show quote-<n>` and `work names`, their parsers and dispatch, so that scripts/work stays small. A quote is
named by its label, `quote-1 "<its words>"` (design goal 10)."""
import json
import sys
from pathlib import Path

import conversation_names
import conversation_prompt
import conversation_quote
from shop_files import Refused
from transcripts import Refused as ReadRefused

is_quote = conversation_quote.is_quote


def add_parsers(sub):
    """The conversation's subcommands, beside `work`'s own."""
    p = sub.add_parser("quote", help="copy the person's message holding these words, with the two messages before and "
                                     "after it, into .shop/quotes/<n>.md, and commit it")
    p.add_argument("words", nargs="?", help="the person's words, as they wrote them")
    p.add_argument("--session", help="the session whose transcript holds them (default: the one the hook kept)")
    p.add_argument("--transcript", help="the transcript file itself")
    p.add_argument("--hook", action="store_true", help="the UserPromptSubmit hook: keep the session and transcript "
                                                       "its stdin gives for work quote, printing nothing")
    p = sub.add_parser("names", help="every item and batch with its name beside its id, one table")
    p.add_argument("--hook", action="store_true", help="the SessionStart hook: the table under one line, nothing when "
                                                       "there is nothing to name, never failing")


def refused(command, why):
    print("work %s: %s" % (command, why), file=sys.stderr)
    return 1


def quote(args):
    if args.hook and args.words is not None:
        return refused("quote", "--hook takes no words")
    if args.hook:
        conversation_prompt.keep(Path.cwd(), sys.stdin.read())
        return 0
    try:
        found = conversation_quote.write(args.root, args.words, args.session, args.transcript)
    except (Refused, ReadRefused) as why:
        return refused("quote", why)
    print(conversation_quote.label(found))
    return 0


def show(args):
    """`work show quote-<n>`: the quote's label, its session and date, then each message it cites, the cited one
    marked (D7); with --json one object `{"quote": {...}}`."""
    try:
        found = conversation_quote.find(args.root, args.target)
    except Refused as why:
        return refused("show", why)
    if args.json:
        print(json.dumps(conversation_quote.as_json(found)))
        return 0
    print(conversation_quote.label(found))
    print("  session: %s" % found.session)
    print("  date: %s" % found.date)
    for m in found.messages:
        cited = ", cited" if m.ident == found.message else ""
        print("\n%s, %s%s:\n%s" % (conversation_quote.WHO[m.who], m.at.isoformat(), cited, m.text))
    return 0


def names(args):
    if args.hook:
        text = conversation_names.hook_text(Path.cwd())
        if text:
            print(text)
        return 0
    print(conversation_names.table(args.root))
    return 0


COMMANDS = {"quote": quote, "names": names}
