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
ALWAYS = ("--by-tag",)     # a cli-only option argparse requires of its command (`features count --by-tag`)
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
    options += [("`%s`" % o, None) for o in op.cli_only if o in ALWAYS]
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
    found = THENS.get(template) or (NEGATED.get(term) if template == "ThenDoesNot" else None)
    return found[0] if found else (template, term)


def _spell(np, operation):
    """A parameter named by a Then ("the tier") as its option ("the `--tier` option")."""
    found = re.fullmatch(r"(?:the|a|an) (.+)", np or "")
    if not operation or found is None:
        return np
    service = operation.split(".")[0]
    ops = [contract().operations[operation]] + [o for i, o in contract().operations.items()
                                                if i.split(".")[0] == service and i != operation]
    param = next((o.parameters[found.group(1)] for o in ops if found.group(1) in o.parameters), None)
    return "the `%s` option" % param.option if param is not None and param.option else np


# the operations whose request the handlers took as an event (the person merges the pull request on the host)
EVENTS = {"batches.merge": "merge"}
# the words a capability's handlers know a kind by, before the domain contract renamed it
RENAMES = {"requests": {"context request": "request", "entry": "comment"},
           "intake": {"context request": "request", "entry": "comment"},
           "batches": {"proposed change": "pull request", "kept change": "commit", "workspace": "worktree",
                       "context request": "request", "entry": "comment"},
           "telemetry": {"proposed change": "pull request"},
           "migration-tools": {"this plugin": "`migrate`"},
           "backlog": {"shared workspace": "upstream branch", "workspace name": "branch name",
                       "workspace": "git branch"}}
# the verbs a capability's handlers know a state by, before the reword: (new term, old term, old third person)
VERB_RENAMES = {"batches": [("break", "fail", "fails"), ("succeed", "pass", "passes"), ("meet", "pass", "passes")],
                "backlog": [("meet", "pass", "passes")], "readiness": [("meet", "pass", "passes")]}


def _renamed(call, node):
    """The kinds the handlers of the capability the scenario moved from know by an older word, said so."""
    table = RENAMES.get(origin(node), {})
    def say(text):
        for new, old in table.items():
            if new.startswith("this "):     # a phrase said whole
                text = text.replace(new, old) if text else text
                continue
            text = re.sub(r"\b(the|a|an|no|every|this|each|that) %s(s?)\b" % new, r"\1 %s\2" % old,
                          text) if text else text
        return text
    call.text, call.subject = say(call.text), say(call.subject)
    call.nps = [say(np) for np in call.nps]
    call.kind = table.get(call.kind, call.kind)
    if call.template.startswith("Given") or call.template.endswith("K_A"):
        call.term = table.get(call.term, call.term)
    if call.template in ("GivenDoes", "GivenDoesNot") and call.term == "holds" and call.nps == ["this repository"]:
        call.term = call.event = "check out"        # a workspace that holds this repository is checked out there
        call.subject, call.nps = "this repository", [call.subject]
        call.text = "this repository checks out %s" % call.nps[0]


def _reverbed(call, node):
    for new, old, said in VERB_RENAMES.get(origin(node), []):
        if new == "meet" and call.nps != ["this readiness bar"]:   # a bar check is still met
            continue
        if call.template in ("GivenDoes", "GivenDoesNot", "ThenDoes", "ThenDoesNot") and call.term == new:
            call.term = call.event = old
            call.text = re.sub(r"\b%ss\b" % new, said, call.text, count=1)
            call.text = re.sub(r"\b%s\b" % new, old, call.text, count=1)


def _owner(call, node, kind):
    """A request's thing named as what a `kind` has ("the context request c1 has the turn t1"): the `kind` it is
    of, as the CLI's handlers name a request's thing by its request."""
    texts = [s.name for s in scenario(node).steps] if scenario(node) else []
    out = []
    for name in call.names:
        found = [m for t in texts for m in re.findall(r"^the %s (\w+) (?:has|holds) the [a-z ]+ %s$" % (kind, name), t)]
        out.append(found[0] if found else name)
    call.names = out


def legacy(call, context, node, known):
    """`call` re-keyed for the CLI's handlers (in place): `known(key)` says whether a handler or a chain has a key."""
    _renamed(call, node)
    _reverbed(call, node)
    t = call.template
    if t == "WhenRequests" and origin(node) in RENAMES:
        _owner(call, node, "context request")
    if t == "WhenRequests" and call.term in EVENTS:     # what the handlers took as an event, not a command
        context["requested"] = (call.term, "`%s`" % contract().operations[call.term].command)
        call.template = "WhenHappens"
        call.term = call.event = EVENTS[call.term]
        return call
    if t == "WhenRequests":
        commands, options, without = command(call.term, call.params + _things(call))
        chosen = next((c for c in commands if known(("WhenRuns", c))), commands[-1])
        context["requested"] = (call.term, chosen)
        call.template, call.term, call.command = "WhenRuns", chosen, chosen
        call.options, call.without = options, without
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
    if template == "ThenNotifies":     # the party told is the hook's session, not what the output shows
        text = re.sub(r" notifies (the|this) [a-z ]+? [a-z]*\d* ?of ", " notifies ", text, count=1)
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
            except (Exception, pytest.fail.Exception) as err:  # noqa: BLE001  (any failure tries the next key)
                first = first or err
                if not node._shop_more:
                    raise first from None
            finally:
                node._shop_alt = 0
        raise first
    return run
