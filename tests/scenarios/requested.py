"""A request's step taken to the CLI adapter (the domain contract design, §6.2, §9.4): the generated scenarios say a
request of an operation and the request pack's acts (`WhenRequests decisions.enter`, `ThenRefuses`, `ThenReturns`,
`ThenKeeps`, ...); the handlers act through the CLI. `legacy` re-keys a step's Call through `spec/adapters/cli.toml`
in one place: a request becomes the command the contract names with each parameter as its option (`WhenRuns`
`work decision`, `without` the `--tier` option), a session that starts the hook its capability answers with, and
each act of the request pack the CLI's spelling of it (refuse, print, exit, commit), its subject the program the
scenario requested last, a parameter it names as its option (the tier as the `--tier` option). `origin` gives the
capability a scenario's group moved from (spec/moves.json), or the one `ADDED` names for a group added since (b309),
which the handlers of that capability's world know it by. Not a handler module: vocab4 and vocab import it."""
import json
import re
from functools import cache
from pathlib import Path

import adapter_cli

if __package__:
    from . import requested_words as W
else:   # loaded by path, as vocab4 is
    import requested_words as W

ROOT = Path(__file__).resolve().parents[2]
REQUEST = ("WhenRequests", "ThenRefuses", "ThenReturns", "ThenReturnsNot", "ThenCompletes", "ThenFails",
           "ThenNotifies", "ThenKeeps")
# a session that starts: the SessionStart hook's command each capability's scenarios are told by (hooks/hooks.json)
STARTS = {"directives": ("`work directives`", "`--hook`"), "request-watch": ("`work watch --hook`", None),
          "items": ("`work names`", "`--hook`"), "upgrades": ("`migrate status --hook`", None)}
# what the CLI's handlers call an act of the request pack, or a verb the reworded lines say for theirs: each tried in
# turn (`trying`) until one handler takes the step
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")
THENS = {"ThenRefuses": [("ThenDoes", "refuse")], "ThenReturns": [("ThenPrints", None), ("ThenDoes", "write")],
         "ThenReturnsNot": [("ThenPrintsNot", None)], "ThenCompletes": [("ThenExitsOk", None)],
         "ThenFails": [("ThenExitsErr", None)], "ThenNotifies": [("ThenPrints", None)],
         "ThenKeeps": [("ThenDoes", v) for v in KEEPS]}
NEGATED = {"keep": [("ThenDoesNot", v) for v in KEEPS], "notify": [("ThenPrintsNot", None)],
           "change": [("ThenDoesNot", v) for v in ("change", "rewrite", "relocate", "rename")]}
VERBS = {"change": ("rewrite", "relocate", "rename", "commit", "change")}
# a command whose flagged key is another capability's handler: this capability's runs it plain with the flag
PLAIN = {("design-model-check", "`spec decisions --check`"): "`spec decisions`"}
ALWAYS = ("--by-tag",)
DEFAULT = {"specification.renew": "--write", "scenarios.audit": "--check"}     # a cli-only option argparse requires of its command (`features count --by-tag`)
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


# groups added since the move whose scenarios an old capability's handlers take, as its moved groups' (b309); a
# group whose own capability has handlers of its own is not listed
ADDED = {"consistency#g33": "design-model-check", "consistency#g34": "design-model-check",     # b418
         "consistency#g36": "design-model-check",                                # b543: a response's request
         **{"consistency#g%d" % n: "design-model-check" for n in (37, 38, 39)},  # b545: a request followed
         "consistency#g40": "design-model-check",                                # b571: a request with none
         **{"consistency#g%d" % n: "design-model-check" for n in (41, 42, 43)},  # b579: count, only; b569
         "drafting#g25": "readiness", "reviews#g6": "batches",   # b354: a term of a new capability; b449
         "reviews#g7": "batches", "reviews#g8": "batches",      # b491: task branches merged in task order
         "drafting#g28": "readiness",                            # b458: the decisions a retired requirement enforces
         "measurement#g10": "telemetry", "measurement#g11": "batch-measurement",    # b420: compare's frames of two
         "measurement#g12": "telemetry",                                         # b73: test runs, opening time
         "items#g31": "backlog", "items#g32": "backlog",                         # b431: work reopen
         "parsing#g19": "design-model-check", "parsing#g20": "design-model-check",     # b452: spec parse --item
         "parsing#g22": "design-model-check",
         **{"items#g%d" % n: "backlog" for n in (33, 34, 38, 39, 42, 43, 44, 45, 46, 47)},   # b281: work merge, work annotate; b465, b484; b480
         "items#g35": "readiness", "items#g36": "readiness",                     # b281: a ready item checked again
         **{"items#g%d" % n: "backlog" for n in range(48, 53)},                 # b459: work retitle, work split
         "items#g40": "readiness",                                               # b444: a construct uncatalogued
         "items#g41": "readiness",                                               # b477: a model line breaks a rule
         "items#g53": "readiness", "items#g54": "readiness",                     # b516: universal conditions only
         "items#g55": "readiness",                                               # b581: two groups of one title
         "items#g64": "readiness", "items#g65": "readiness",                     # b654: moves its only lines
         **{"items#g%d" % n: "backlog" for n in range(56, 64)},                 # b578, b585: tracking's operations
         **{"checking#g%d" % n: "design-model-check" for n in range(52, 58)},
         "checking#g63": "design-model-check",                                   # b538: an attribute's senses
         "reviews#g9": "batches", "reviews#g10": "batches",     # b492: a base merge resubmitted; b370: the rule catalogue's checks
         "reviews#g11": "batches", "reviews#g12": "batches",    # b69: a batch reopened with the person's finding
         **{"context-requests#g%d" % n: "requests" for n in (51, 52, 54, 55, 56)},    # b68: a thread out of step; b71
         **{"context-requests#g%d" % n: "requests" for n in (53, 57, 58, 59)}}    # b42: a term proposal


def origin(node):
    """The capability the scenario's group moved from (`decision-tiers`), else the one `ADDED` names for a group added
    since the move (b309), else its own capability."""
    cap, found = capability(node), scenario(node)
    if found is None:
        return None
    for tag in sorted(found.tags):
        if re.fullmatch(r"g\d+", tag) and "%s#%s" % (cap, tag) in _moved():
            return _moved()["%s#%s" % (cap, tag)].split("#")[0]
        if re.fullmatch(r"g\d+", tag) and "%s#%s" % (cap, tag) in ADDED:
            return ADDED["%s#%s" % (cap, tag)]
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
    options += [("`%s`" % o, None) for o in op.cli_only if o in ALWAYS]
    if operation in DEFAULT and not words:      # the option the command takes for the operation's plain request
        words.append(DEFAULT[operation])
        options.append(("`%s`" % DEFAULT[operation], None))
    options += [("`--hook`", None)] if op.hook else []     # a hook's operation: its command run as the hook
    longest = " ".join([base] + words)
    valued = " ".join([longest] + ["%s %s" % (o.strip("`"), v.strip("`")) for o, v in options if v is not None])
    found = ["`%s`" % valued] if valued != longest else []
    return found + ["`%s`" % longest] + (["`%s`" % base] if words else []), options, without


def commands(program):
    """Every command key (with backticks) a request of `program`'s operations is taken to: each command, and each
    with one of its flags; and the hooks' commands of `program`."""
    found = {c for c, flag in STARTS.values() if flag is None and c.strip("`").split()[0] == program}
    for op in contract().operations.values():
        if op.hook is None and op.command.split()[0] == program:
            found.add("`%s`" % op.command)
            found |= {"`%s %s`" % (op.command, p.option) for p in op.parameters.values() if p.flag}
    return sorted(found)


@cache
def _slots(operation):
    """{preposition: parameter} of the frames the vocabulary gives the verb of `operation` (`over <supersedes>`)."""
    found = {}
    for path in sorted((ROOT / "spec" / "vocabulary").glob("*.md")):
        for line in path.read_text().splitlines():
            if "→ operation %s." % operation in line or line.rstrip().endswith("→ operation %s" % operation):
                found.update({prep: param for prep, param in re.findall(r" (\w+) <([a-z -]+)>", line)})
    return found


def _things(call):
    """(parameter, "the K x") of each thing the request's frame names whose kind is a parameter of its operation
    (`recodifies the capability c1 in the item i1`: the capability), the parameters said apart not repeated."""
    op = contract().operations[call.term]
    said = {p for p, _ in call.params}
    found = re.findall(r"(?=\bthe ((?:[a-z-]+ ){0,2}?[a-z-]+) ([a-z]+\d+)\b)", call.text)
    out = [(k, "the %s %s" % (k, n)) for k, n in found if k in op.parameters and k not in said]
    for prep, param in _slots(call.term).items():       # a thing in a frame's slot: `over the design-decision d2`
        thing = re.search(r"\b%s (the [a-z -]+? [a-z]+\d+|`[^`]+`)" % prep, call.text)
        if thing and param in op.parameters and param not in said | {k for k, _ in out}:
            out.append((param, thing.group(1)))
    codes = [c for c in re.findall(r"`[^`]+`", call.text) if c not in {v for _, v in call.params}]
    open_ = [p for p, param in op.parameters.items() if param.option and p not in said | {k for k, _ in out}]
    return out + list(zip(open_, codes))      # a code the frame names: the first option left (`universal`)


def lookup_key(handlers, template, term):
    """For `features vocab --check`: the old key a request's step is taken to, else the key itself."""
    if template == "WhenRequests" and term in EVENTS:
        return "WhenHappens", EVENTS[term]
    if template == "WhenRequests" and term in contract().operations:
        commands, _, _ = command(term)
        return next((("WhenRuns", c) for c in commands if handlers(("WhenRuns", c))), ("WhenRuns", None))
    if template == "WhenHappens" and term == "start":
        return "WhenRuns", None
    for table in W.RENAMES.values():     # a kind the handlers know by its older word
        if term in table and (template.startswith("Given") or template.endswith("K_A")):
            return template, table[term]
    found = THENS.get(template) or (NEGATED.get(term) if template == "ThenDoesNot" else None)
    return found[0] if found else (template, term)


def _spell(np, operation, absent=()):
    """A parameter named by a Then ("the tier") as its option ("the `--tier` option"); a thing of a parameter's kind
    ("the line reason l1") so only when the request was made without that parameter."""
    found = re.fullmatch(r"(?:the|a|an) (.+?)( [a-z]+\d+)?", np or "")
    if not operation or found is None or found.group(2) and found.group(1) not in absent:
        return np
    service = operation.split(".")[0]
    ops = [contract().operations[operation]] + [o for i, o in contract().operations.items()
                                                if i.split(".")[0] == service and i != operation]
    param = next((o.parameters[found.group(1)] for o in ops if found.group(1) in o.parameters), None)
    return "the `%s` option" % param.option if param is not None and param.option else np


# the operations whose request the handlers took as an event (the person merges the pull request on the host)
EVENTS = {"batches.merge": "merge"}
def legacy(call, context, node, known):
    """`call` re-keyed for the CLI's handlers (in place): `known(key)` says whether a handler or a chain has a key."""
    said = list(call.nps)       # as the step says them, before the handlers' words (a parameter is spelled from these)
    W.renamed(call, origin(node))
    W.reverbed(call, origin(node))
    t = call.template
    if t == "WhenRequests" and call.term in EVENTS:     # what the handlers took as an event, not a command
        context["requested"] = (call.term, "`%s`" % contract().operations[call.term].command)
        call.template = "WhenHappens"
        call.term = call.event = EVENTS[call.term]
        return call
    if t == "WhenRequests":
        commands, options, without = command(call.term, call.params + _things(call))
        chosen = next((c for c in commands if known(("WhenRuns", c))), commands[-1])
        chosen = PLAIN.get((origin(node), chosen), chosen)
        if origin(node) in W.RENAMES and not chosen.startswith("`work outcome "):    # a request's command: on it
            W.owner(call, [s.name for s in scenario(node).steps] if scenario(node) else [], "context request")
        context["requested"], context["absent"] = (call.term, chosen), list(call.without)
        call.template, call.term, call.command = "WhenRuns", chosen, chosen
        call.options, call.without = options, without
        call.text = W.runs_text(call, chosen)
        return call
    if t == "WhenHappens" and call.term == "start" and capability(node) in STARTS:
        chosen, flag = STARTS[capability(node)]
        context["requested"] = (None, chosen)
        call.template, call.term, call.command, call.without = "WhenRuns", chosen, chosen, []
        call.options = [(flag, None)] if flag else []
        call.names = []     # a hook is given no instance
        return call
    operation, chosen = context.get("requested", (None, None))
    program = "`%s`" % chosen.strip("`").split()[0] if chosen else None
    if t == "ThenDoesNot" and call.term == "change" and call.nps == ["a file"]:    # the request changed nothing
        call.template, call.term = "ThenChangesNothing", None
        return call
    negated = t == "ThenDoesNot" and call.term in NEGATED
    if t in THENS or negated:
        if t == "ThenNotifies" or negated and call.term == "notify":
            told = call.nps[0] if call.nps else ""
            call.names = [n for n in call.names if n not in told.split()]
            call.nps = call.nps[1:]
        if t == "ThenRefuses":
            call.nps = [chosen] if chosen else []
        if t in ("ThenCompletes", "ThenFails"):     # "fails this check": no thing is named
            call.nps = []
        template, term = _pick(node, THENS[t] if t in THENS else NEGATED[call.term])
        call.text = W.retext(call.text, program, t, term or {"ThenPrints": "print"}.get(template), chosen)
        call.template, call.subject = template, program or call.subject
        call.term = term if term is not None else call.subject
        call.event = term or call.event
        return call
    if t == "ThenDoes" and call.term in VERBS:
        said = call.term
        call.term = call.event = _pick(node, [(t, v) for v in VERBS[call.term]])[1]
        call.text = call.text.replace(" %s " % W.S3.get(said, said), " %s " % W.S3.get(call.term, call.term + "s"), 1)
    if t.startswith("Then") and call.term == "name":
        spelled = [_spell(np, operation, context.get("absent", ())) for np in said]
        call.nps = [s if s != o else n for s, o, n in zip(spelled, said, call.nps)]
    if t.startswith("Then") and call.subject and call.subject.endswith(" service") and program:
        call.subject = program
        call.text = W.retext(call.text, program, t, None, chosen)
    return call


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
            except (Exception, pytest.fail.Exception) as err:  # noqa: BLE001  (any failure tries the next key)
                first = first or err
                if not node._shop_more:
                    raise first from None
            finally:
                node._shop_alt = 0
        raise first
    return run
