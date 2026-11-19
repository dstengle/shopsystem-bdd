"""A request's step taken to the CLI adapter (the domain contract design, §6.2, §9.4): the generated scenarios say a
request of an operation and the request pack's acts (`WhenRequests decisions.enter`, `ThenRefuses`, `ThenReturns`,
`ThenKeeps`, ...); the handlers act through the CLI. `legacy` re-keys a step's Call through `spec/adapters/cli.toml`
in one place: a request becomes the command the contract names with each parameter as its option (`WhenRuns`
`work decision`, `without` the `--tier` option), a session that starts the hook its capability answers with, and
each act of the request pack the CLI's spelling of it (refuse, print, exit, commit), its subject the program the
scenario requested last, a parameter it names as its option (the tier as the `--tier` option). `origin` gives the
capability a scenario's group moved from (spec/moves.json), which the handlers of that capability's world know it
by. Not a handler module: vocab4 and vocab import it."""
import json
import re
from functools import cache
from pathlib import Path

import adapter_cli

ROOT = Path(__file__).resolve().parents[2]
REQUEST = ("WhenRequests", "ThenRefuses", "ThenReturns", "ThenReturnsNot", "ThenCompletes", "ThenFails",
           "ThenNotifies", "ThenKeeps")
# a session that starts: the SessionStart hook's command each capability's scenarios are told by (hooks/hooks.json)
STARTS = {"directives": "`work directives --hook`", "request-watch": "`work watch --hook`",
          "items": "`work names --hook`", "upgrades": "`migrate status --hook`"}
# what the CLI's handlers call an act of the request pack, or a verb the reworded lines say for theirs: each tried in
# turn (`trying`) until one handler takes the step
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite")
THENS = {"ThenRefuses": [("ThenDoes", "refuse")], "ThenReturns": [("ThenPrints", None), ("ThenDoes", "write")],
         "ThenReturnsNot": [("ThenPrintsNot", None)], "ThenCompletes": [("ThenExitsOk", None)],
         "ThenFails": [("ThenExitsErr", None)], "ThenNotifies": [("ThenPrints", None)],
         "ThenKeeps": [("ThenDoes", v) for v in KEEPS]}
NEGATED = {"keep": [("ThenDoesNot", v) for v in KEEPS], "notify": [("ThenPrintsNot", None)],
           "change": [("ThenDoesNot", v) for v in ("rewrite", "change", "relocate", "rename")]}
VERBS = {"change": ("rewrite", "relocate", "rename", "commit", "change")}
MOST = max(len(c) for c in [*THENS.values(), *NEGATED.values(), *VERBS.values()])


@cache
def contract():
    return adapter_cli.read(ROOT)


@cache
def _moved():
    return {new: old for old, new in json.loads((ROOT / "spec" / "moves.json").read_text()).items() if new}


def scenario(node):
    return getattr(getattr(node, "obj", None) or getattr(node, "function", None), "__scenario__", None)


def capability(node):
    """The capability of a scenario's feature (`decisions`), or None."""
    found = scenario(node)
    return Path(found.feature.filename).stem if found is not None else None


def origin(node):
    """The capability the scenario's group moved from (`decision-tiers`), else its own capability."""
    cap, found = capability(node), scenario(node)
    if found is None:
        return None
    for tag in sorted(found.tags):
        if re.fullmatch(r"g\d+", tag) and "%s#%s" % (cap, tag) in _moved():
            return _moved()["%s#%s" % (cap, tag)].split("#")[0]
    return cap


def command(operation, params=()):
    """The command (with backticks) that requests `operation`, its flags and code-valued positionals written into
    it as the old handler keys spell them, and the rest: ([commands, most specific first], options, without)."""
    op = contract().operations[operation]
    base, options, without, words = op.command, [], [], []
    for name, value in params:
        param = op.parameters.get(name)
        if param is None:
            continue
        if value is None:
            if param.option:
                without.append("`%s`" % param.option)
        elif param.positional is not None:
            if isinstance(value, str) and value.startswith("`"):
                words.append(value.strip("`"))
        elif param.flag or value is True:
            words.append(param.option)
            options.append(("`%s`" % param.option, None))
        else:
            options.append(("`%s`" % param.option, value))
    longest = " ".join([base] + words)
    return ["`%s`" % longest] + (["`%s`" % base] if words else []), options, without


def commands(program):
    """Every command key (with backticks) a request of `program`'s operations is taken to: each command, and each
    with one of its flags; and the hooks' commands of `program`."""
    found = {c for c in STARTS.values() if c.strip("`").split()[0] == program}
    for op in contract().operations.values():
        if op.hook is None and op.command.split()[0] == program:
            found.add("`%s`" % op.command)
            found |= {"`%s %s`" % (op.command, p.option) for p in op.parameters.values() if p.flag}
    return sorted(found)


def lookup_key(handlers, template, term):
    """For `features vocab --check`: the old key a request's step is taken to, else the key itself."""
    if template == "WhenRequests" and term in contract().operations:
        commands, _, _ = command(term)
        return next((("WhenRuns", c) for c in commands if handlers(("WhenRuns", c))), ("WhenRuns", None))
    if template == "WhenHappens" and term == "start":
        return "WhenRuns", None
    found = THENS.get(template) or (NEGATED.get(term) if template == "ThenDoesNot" else None)
    return found[0] if found else (template, term)


def _spell(np, operation):
    """A parameter named by a Then ("the tier") as its option ("the `--tier` option")."""
    op = contract().operations.get(operation) if operation else None
    found = re.fullmatch(r"(?:the|a|an) (.+)", np or "")
    if op is None or found is None or found.group(1) not in op.parameters:
        return np
    param = op.parameters[found.group(1)]
    return "the `%s` option" % param.option if param.option else np


def legacy(call, context, node, known):
    """`call` re-keyed for the CLI's handlers (in place): `known(key)` says whether a handler or a chain has a key."""
    t = call.template
    if t == "WhenRequests":
        commands, options, without = command(call.term, call.params)
        chosen = next((c for c in commands if known(("WhenRuns", c))), commands[-1])
        context["requested"] = (call.term, chosen)
        call.template, call.term, call.command = "WhenRuns", chosen, chosen
        call.options, call.without = options, without
        return call
    if t == "WhenHappens" and call.term == "start" and capability(node) in STARTS:
        chosen = STARTS[capability(node)]
        context["requested"] = (None, chosen)
        call.template, call.term, call.command, call.options, call.without = "WhenRuns", chosen, chosen, [], []
        return call
    operation, chosen = context.get("requested", (None, None))
    program = "`%s`" % chosen.strip("`").split()[0] if chosen else None
    negated = t == "ThenDoesNot" and call.term in NEGATED
    if t in THENS or negated:
        if t == "ThenNotifies" or negated and call.term == "notify":
            told = call.nps[0] if call.nps else ""
            call.names = [n for n in call.names if n not in told.split()]
            call.nps = call.nps[1:]
        if t == "ThenRefuses":
            call.nps = [chosen] if chosen else []
        template, term = _pick(node, THENS[t] if t in THENS else NEGATED[call.term])
        call.text = _retext(call.text, program, t, term or {"ThenPrints": "print"}.get(template), chosen)
        call.template, call.subject = template, program or call.subject
        call.term = term if term is not None else call.subject
        call.event = term or call.event
        return call
    if t == "ThenDoes" and call.term in VERBS:
        said = call.term
        call.term = call.event = _pick(node, [(t, v) for v in VERBS[call.term]])[1]
        call.text = call.text.replace(" %s " % S3.get(said, said), " %s " % S3.get(call.term, call.term + "s"), 1)
    if t.startswith("Then") and call.term == "name":
        call.nps = [_spell(np, operation) for np in call.nps]
    if t.startswith("Then") and call.subject and call.subject.endswith(" service") and program:
        call.subject = program
        call.text = _retext(call.text, program, t, None, chosen)
    return call


S3 = {"refuse": "refuses", "return": "returns", "complete": "completes", "fail": "fails", "notify": "notifies",
      "keep": "keeps", "change": "changes", "print": "prints"}
WORDS = {"ThenRefuses": "refuses this request", "ThenCompletes": "completes the request",
         "ThenFails": "fails this check"}
SAID = {"ThenCompletes": "exits successfully", "ThenFails": "exits with an error"}


def _retext(text, program, template, verb, chosen):
    """The step's text as the CLI's handlers read it: "`work` writes the item i1" for "the backlog service keeps the
    item i1"; "`work` refuses `work decision`" for "... refuses this request"."""
    if program:
        text = re.sub(r"^the [a-z ]+ service ", program + " ", text)
    if template in WORDS:
        return text.replace(WORDS[template], SAID.get(template) or "refuses %s" % chosen)
    if verb is None:
        return text
    for new in ("keeps", "returns", "notifies", "changes"):
        text = re.sub(r"^(\S+) %s " % new, r"\1 %s " % S3.get(verb, verb + "s"), text)
    for new in ("keep", "return", "notify", "change"):
        text = re.sub(r"^(\S+) does not %s " % new, r"\1 does not %s " % verb, text)
    return text


def _pick(node, candidates):
    """The candidate key the step is tried with this time (`trying`), noting whether another is left."""
    alt = getattr(node, "_shop_alt", 0)
    node._shop_more = alt + 1 < len(candidates)
    return candidates[min(alt, len(candidates) - 1)]


def trying(step_function):
    """A step function that takes a step re-keyed to one of several keys (a thing kept: written, committed, posted
    or kept) to each in turn until one passes; the first failure when none does."""
    import pytest

    def run(text, request, docstring=None, datatable=None):
        node, first = request.node, None
        for alt in range(MOST):
            node._shop_alt, node._shop_more = alt, False
            try:
                return step_function(text, request, docstring, datatable)
            except (AssertionError, pytest.fail.Exception) as err:
                first = first or err
                if not node._shop_more:
                    raise first from None
            finally:
                node._shop_alt = 0
        raise first
    return run
