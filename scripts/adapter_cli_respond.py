"""The CLI adapter's side of a response (the domain contract design, §5.4, §6.1): `--json` on every subcommand, a
command's handler run and its response read off, then rendered for a person (as each command prints today) or, under
`--json`, as the envelope on stdout (domain_envelope's JSON).

`prepare` gives each leaf subparser `--json` (one it defines itself kept, marked `own_json`: the command printed its
own JSON object before the envelope, now its `content`) and the parser it was parsed by (`parser`). `respond` runs a
handler: a `Response` it returns is the response; else its exit and what it printed are read: a `Refused` raised a
refusal (its reason and the business references it names; for a person its message with each reference spelled as
the command's parser spells it, `--summary`), any other exception `broken`, a check (`args.check`, or a command
`checks` names) passed or failed by its exit, an exit 1 of any other command refused, else done, or returned when the
command printed its own JSON object. Under `--json` the content is that object, or the text it printed."""
import contextlib
import io
import json
import sys

import domain_envelope
from domain_envelope import Response
from shop_refused import Refused


def leaves(parser):
    """Each parser under `parser` that has no subcommands of its own, with its command words."""
    subs = [a for a in parser._actions if a.__class__.__name__ == "_SubParsersAction"]
    if not subs:
        yield (), parser
        return
    for action in subs:
        for word, child in action.choices.items():
            for words, leaf in leaves(child):
                yield (word,) + words, leaf


def prepare(parser):
    """`--json` on every leaf subparser that lacks it; each leaf's `parser` and `own_json` set as defaults."""
    for _, leaf in leaves(parser):
        own = any("--json" in a.option_strings for a in leaf._actions)
        if not own:
            leaf.add_argument("--json", action="store_true",
                              help="print the response as one JSON object: outcome, content, errors, notices")
        leaf.set_defaults(own_json=own, parser=leaf)
    return parser


def spelling(parser, names=None):
    """A business reference's CLI spelling by `parser`: a parameter as its option (by the argparse dest, through
    `names`, {parameter: dest}, where the two differ), a positional as its name; any other reference its own name."""
    names = names or {}

    def spell(ref):
        kind, _, name = ref.partition(":")
        if kind != "parameter" or parser is None:
            return name or ref
        dest = names.get(name, name.replace(" ", "_").replace("-", "_"))
        for action in parser._actions:
            if action.dest == dest:
                return action.option_strings[0] if action.option_strings else dest
        return name
    return spell


class _Tee(io.StringIO):
    def __init__(self, through):
        super().__init__()
        self.through = through

    def write(self, text):
        self.through.write(text)
        return super().write(text)


def _content(text, own):
    if own:
        try:
            return json.loads(text)
        except ValueError:
            pass
    return text if text.strip() else None


def _read(result, code, out, err, args, checks):
    """The response of a handler that returned `result` (a Response, or an exit) having printed `out` and `err`."""
    if isinstance(result, Response):
        return result
    own = getattr(args, "own_json", False)
    content = _content(out, own)
    reasons = [line.strip() for line in err.splitlines() if line.strip()]
    if getattr(args, "check", False) is True or checks:
        if code == 0:
            return Response("passed", content)
        return Response("failed", content, [domain_envelope.error(r) for r in reasons or ["the check failed"]])
    if code:
        return Response("refused", content, [domain_envelope.error(r) for r in reasons or ["refused"]])
    return Response("returned" if own else "done", content)


def respond(tool, handler, args, checks=False, names=None):
    """Run `handler(args)` and give its exit; under `args.json` print its response's envelope on stdout."""
    spell = spelling(getattr(args, "parser", None), names)
    if not getattr(args, "json", False):
        try:
            result = handler(args)
        except Refused as why:
            sys.stderr.write("%s: %s\n" % (tool, why.spelled(spell)))
            return 1
        if isinstance(result, Response):
            return 1 if result.outcome in domain_envelope.ERRING else 0
        return result
    out, err = io.StringIO(), _Tee(sys.stderr)
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                result = handler(args)
            except SystemExit as stop:
                result = stop.code if isinstance(stop.code, int) else (0 if stop.code is None else 1)
        response = _read(result, result if isinstance(result, int) else 0, out.getvalue(), err.getvalue(), args,
                         checks)
    except Refused as why:
        sys.stderr.write("%s: %s\n" % (tool, why.spelled(spell)))
        response = domain_envelope.refused(why)
    except Exception as exc:  # noqa: BLE001 -- a failure outside the domain: broken, said on stderr too
        sys.stderr.write("%s: %s\n" % (tool, exc))
        response = domain_envelope.broken(exc)
    print(response.json())
    return 1 if response.outcome in domain_envelope.ERRING else 0
