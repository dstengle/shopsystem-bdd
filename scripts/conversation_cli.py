"""The conversation's commands of `work` (capability conversation; workflow simplification plan 8): `work quote`, their
parsers and dispatch, so that scripts/work stays small. A quote is named by its label, `quote-1 "<its words>"` (design
goal 10)."""
import sys
from pathlib import Path

import conversation_prompt
import conversation_quote
from measure_read import Refused as ReadRefused
from workqueue import Refused


def add_parsers(sub):
    """The conversation's subcommands, beside `work`'s own."""
    p = sub.add_parser("quote", help="copy the person's message holding these words, with the two messages before and "
                                     "after it, into .shop/quotes/<n>.md, and commit it")
    p.add_argument("words", nargs="?", help="the person's words, as they wrote them")
    p.add_argument("--session", help="the session whose transcript holds them (default: the one the hook kept)")
    p.add_argument("--transcript", help="the transcript file itself")
    p.add_argument("--hook", action="store_true", help="the UserPromptSubmit hook: keep the session and transcript "
                                                       "its stdin gives for work quote, printing nothing")


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


COMMANDS = {"quote": quote}
