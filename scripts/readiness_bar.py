"""The readiness bar (capability readiness; workflow simplification plan 3, D6-D9, D11): an item is passing when every
request line of the item is settled and its requirement lines are well-formed: they parse in grammar 4
(spec_language), they bring no problem of the lexicon (v_t4 to v_t13) that the lexicon without them does
not have (readiness r15), they bring no violation of a `model.lp` rule of `model check` that
names a group or a requirement of theirs (v15k, v15l, v15n alike: b77, b333) or an element of its model lines (v_m4,
b477), `model logic` finds no L0 and no L1 naming them and reads each of them (r41), and
`features generate` writes a scenario for each of their groups that has a step; every stage after the lexicon's runs
whatever the stages before it found, so one run names every failing line (b305). The lines are checked on a copy of `spec/` under the temporary directory
with the item's lines laid in, removed afterwards whatever happens; `spec/` itself is never written. The copy is held
(spec_held) so its inputs are statted once a state and each line parsed once; the result before the lay is kept on
disk (readiness_before); a lay's parse misses are parsed side by side (spec_prefetch); and the bar runs no `spec
annotate`, compares no v_a5 or v_a6 and runs no entailment (decision 0112, b430). The `check` design-decisions that a
capability of the item's lines rests on run their tests on the root checkout, each once a process (plan 6, D13)."""
import contextlib
import io
import re
import shutil
import tempfile
from pathlib import Path

import backlog_chore
import backlog_forms
import backlog_lines
import features_generate
import model_decisions
import readiness_before
import request_moves
import request_text
import spec_catalogued
import spec_held
import spec_language
import spec_lexicon
import spec_prefetch
import spec_read
import spec_rgl_vocab
import spec_solve
from backlog_items import rel_of


def request_lines(root, item):
    """(number, text, line outcome or None) of each line of the item's request that is not `rewritten` (D11): a
    rewritten line is no longer the item's, its counter-proposal is."""
    request = getattr(item, "request", None)
    if request is None:
        return []
    found = request_moves.sections(root, request)
    outcomes = found["Outcomes"]
    return [(int(n), found["Lines"][n], outcomes.get(n)) for n in sorted(found["Lines"], key=int)
            if outcomes.get(n) != "rewritten"]


def unsettled(root, item):
    """A reason for each request line of the item that is not settled."""
    return ["line %d of request %s is %s, not settled: %s" % (n, item.request, outcome or "unanswered", text)
            for n, text, outcome in request_lines(root, item) if outcome not in request_text.SETTLED]


def _parses(copy, blocks):
    """The id of each of the item's requirements, and universal conditions (b43), that does not parse in grammar 4
    (spec_language), with its reason."""
    reasons = {}
    statements = [("%s#%s" % (b.capability, rid), text) for b in blocks for g in b.groups
                  for rid, text in g.requirements] + [("universal#%s" % uid, text) for uid, text in blocks.universal]
    for ident, text in statements:
        parsed = spec_language.parse(copy, text)
        if parsed.tree is None:
            hint = spec_language.hint(copy, text)
            reasons[ident] = "%s: %s; parsed up to: %s; nearest words: %s" % (
                ident, parsed.refusal, hint["prefix"] or "nothing", ", ".join(hint["near"]) or "none")
    return reasons


# The rules the bar names by a stage of its own, or that read the features the copy does not have: a parse (v_p1, v_p2)
# by `_parses`, a scenario (v_s1-v_s3) by `_scenarios` (b333).
# Nor v_a5 and v_a6, the adapter contract's annotations, which the bar does not write (decision 0112); nor v_a3 and
# v_a4, the contract against its program, which the copy does not hold and an item's change has not yet built (b445):
# none names an item's group or requirement, and `spec check` checks them on the built tree. Skipped, so that the rule
# catalogue does not take the bar for where they are implemented (model_rules.skipped, b467).
SKIPPED_RULES = {"v_a3", "v_a4", "v_a5", "v_a6"}
OWN_STAGE = {"v_p1", "v_p2", "v_s1", "v_s2", "v_s3"} | SKIPPED_RULES


def _violations(copy):
    """(the violations of every `model.lp` rule `model check` finds in the copy, as (code, args), {code: label}), read
    through `model`'s facts as `model check` reads them (b333)."""
    from model_check import solve
    from model_facts import Model
    relations, labels = solve(Model(copy).read())
    return {(name, tuple(str(a) for a in args)) for name, args in relations
            if name.startswith("v") and name not in OWN_STAGE}, labels


def _broken(copy, blocks, before):
    """A reason for each violation of a `model.lp` rule that names a group or a requirement of the item, naming it and
    the rule (and any other node the violation names), and for each that names none of them but an element of the
    item's model lines by a domain model rule (`v_m<n>`: v_m4 of a reason no line states, b477), naming the model line by its element and the rule,
    unless the violation is in `before`, the copy's before the item's lines were laid (b77, b333)."""
    mine = {"%s#%s" % (b.capability, g.id) for b in blocks for g in b.groups} | set(backlog_lines.ids(blocks))
    found, labels = _violations(copy)
    reasons = []
    for name, args in sorted(found - before):
        short = [a.rsplit("/", 1)[-1] for a in args]       # capability/<context>/<name>#g<n> as <name>#g<n>
        for k, node in enumerate(short):
            if node in mine:
                others = short[:k] + short[k + 1:]
                reasons.append("%s: %s %s%s" % (node, name, labels.get(name, ""),
                                                ": with %s" % ", ".join(others) if others else ""))
        if name.startswith("v_m") and not set(short) & mine:    # a domain model rule over its model lines (b477)
            reasons += _modelled(blocks, name, labels.get(name, ""), args)
    return list(dict.fromkeys(reasons))


def model_elements(blocks):
    """{qualified id: what the refusal calls it} of each element the item's model lines declare or restate: an
    object or a service by its name, an operation as `<service>.<operation>` (b477)."""
    import backlog_model
    found = {}
    for model in getattr(blocks, "models", ()):
        for header, members in backlog_model.chunks(model.lines):
            kind, _, rest = header.partition(" ")
            name = rest.split(" kind of ", 1)[0].strip()
            if kind not in ("object", "service") or not name:
                continue
            found.setdefault(name, "%s %s" % (kind, name))
            for member in members if kind == "service" else ():
                op = re.match(r"\s*operation\s+([\w-]+)", member)
                if op:
                    found["%s.%s" % (name, op.group(1))] = "operation %s.%s" % (name, op.group(1))
    return found


def _modelled(blocks, name, label, args):
    """The reason of a violation the lay brings that names an element of the item's model lines (the most specific
    one: an operation before its service), naming the model line by its element and the rule, else none."""
    elements = model_elements(blocks)
    for arg in args:
        hit = elements.get(arg) or next((elements[e] for e in sorted(elements, key=len, reverse=True)
                                         if arg.startswith(e + ".")), None)
        if hit:
            others = [a for a in args if a != arg]
            return ["the model line of %s (%s model): %s %s%s" % (
                hit, ", ".join(m.area for m in blocks.models), name, label,
                ": with %s" % ", ".join(others) if others else "")]
    return []


def _logic(copy, mine, conditions=(), unparsed=()):
    """(reasons, warnings) of `model logic` on the copy: an L0, and an L1 naming one of `mine`, refuse (D6), and so
    does each of `mine` and of the item's universal conditions `conditions` (`U<n>`) that it reads no translation of
    (`spec_solve.unread`, r41), an unread requirement elsewhere not, nor one named in `unparsed` already (b305); an L3
    naming one of them is a warning."""
    reasons, warnings = [], []
    for f in spec_solve.run(copy, entail=False):        # no L2 and no L8 (decision 0112)
        said = "%s %s" % (f.code, f.text)
        if f.code == "L0" or (f.code == "L1" and set(f.ids) & mine):
            reasons.append(said)
        elif f.code == "L3" and set(f.ids) & mine:
            warnings.append(said)
    named = {**{i: i for i in mine}, **{u: "universal#%s" % u for u in conditions}}
    reasons += ["%s: no translation: %s" % (named[i], why) for i, why in spec_solve.unread(copy)
                if i in named and named[i] not in unparsed]
    return list(dict.fromkeys(reasons)), list(dict.fromkeys(warnings))


def _scenarios(copy, blocks, unparsed=()):
    """A reason for each group of a service capability that `features generate` writes no scenario for, unless it is
    logic-only (D9); a guarantees capability has no scenarios, and a capability a line of which is in `unparsed`
    (`<capability>#r<n>`) none checked, its parse named already (b305)."""
    reasons = []
    broken = {ident.split("#", 1)[0] for ident in unparsed}
    for block in blocks:
        path = backlog_lines.capability_file(copy, block.capability)
        if (spec_read.capability(path).frontmatter.get("group") == "guarantees" or not block.groups
                or block.capability in broken):
            continue
        skipped = {}
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                features_generate.generate(copy, path, skipped)
        except features_generate.GenerateError as err:
            reasons.append("%s: %s" % (block.capability, err))
            continue
        for group in block.groups:
            gid = "%s#%s" % (block.capability, group.id)
            if gid in skipped:
                reasons.append("%s has no scenario: %s" % (gid, skipped[gid]))
    return reasons


def well_formed(root, item, others=()):
    """(reasons, warnings) of the item's requirement lines, checked on a copy of `spec/` with them laid in (D6, D7, D9),
    over the lines of `others` (a batch's items picked before it, plan 4 D7). An item with no line is not passing,
    unless it retires a requirement (b271)."""
    if backlog_chore.read(item) is not None:        # a chore in place of lines (b316): its check is done's to run
        return backlog_chore.unlined(item), []
    blocks = backlog_lines.read(item, rel_of(item.name))
    mine = set(backlog_lines.ids(blocks))
    if not mine and not any(b.retired for b in blocks) and not blocks.adapters:     # an operation table (b355)
        return ["it has no requirement line: give it one with `work line`"], []
    copy = Path(tempfile.mkdtemp(prefix="readiness-"))
    try:
        shutil.copytree(Path(root) / "spec", copy / "spec")      # backlog_lines.lay, the lexicon read before the item
        spec_catalogued.copy(root, copy)        # parsing#r6 refuses on the copy as in the context (b444)
        for other in others:
            backlog_lines.lay_onto(copy, other)
        with spec_held.held(copy):          # the copy's inputs statted once a state, each line parsed once (b430)
            return _laid(copy, item, blocks, mine)
    finally:
        shutil.rmtree(copy, ignore_errors=True)


def _laid(copy, item, blocks, mine):
    """well_formed's stages on the copy: the state before the lay (readiness_before), the lay, then each stage."""
    outer = spec_rgl_vocab.outer(copy)

    def unlaid():
        spec_prefetch.prefetch(copy, spec_prefetch.texts(copy))
        return set(spec_lexicon.problems(spec_lexicon.read(copy), outer)), _violations(copy)[0]
    before, before_lay = readiness_before.before(copy, unlaid)
    doubled = backlog_forms.laid_already(copy, blocks)      # an upstream an item picked before lays (b476)
    backlog_lines.lay_onto(copy, item)
    reasons = ["%s.md: %s" % (b.capability, p) for b in blocks
               for p in spec_read.capability(backlog_lines.capability_file(copy, b.capability)).problems]
    reasons += ["universal.md: %s" % p for p in spec_read.read_universal(copy).problems] if blocks.universal else []
    reasons += ["the lexicon: %s %s: %s" % found for found in spec_lexicon.problems(spec_lexicon.read(copy), outer)
                if found not in before]                                                             # r15
    if reasons:                  # a broken lexicon breaks grammar 4's compile: no stage after it runs
        return doubled + reasons, []
    spec_prefetch.prefetch(copy, spec_prefetch.texts(copy))     # the lay's misses side by side, after the lexicon
    unparsed = _parses(copy, blocks)       # every stage after it runs whatever it finds, each line named once (b305)
    reasons, warnings = _logic(copy, mine, [uid for uid, _ in blocks.universal], unparsed)
    return (doubled + list(unparsed.values()) + _broken(copy, blocks, before_lay) + reasons
            + _scenarios(copy, blocks, unparsed), warnings)


_RAN = {}     # (resolved root, decision's path): its run, once a process (D13)


def rested_on(root, blocks):
    """The `check` decisions that a capability of the blocks rests on, matched by the id's last segment (a capability
    writes `design-decision/<slug>` or the full id), in file order, each once."""
    slugs = set()
    for block in (b for b in blocks if not b.new):       # a capability the item makes rests on nothing yet (b317)
        path = backlog_lines.capability_file(root, block.capability)
        if path.is_file():
            slugs |= {str(d).rstrip("/").rsplit("/", 1)[-1]
                      for d in spec_read.capability(path).frontmatter.get("rests_on") or ()}
    return [d for d in model_decisions.decisions(root) if d.runs and d.ident.rsplit("/", 1)[-1] in slugs]


def decision_reasons(root, blocks):
    """A reason for each `check` decision the item's capabilities rest on whose tests do not hold (D13)."""
    reasons = []
    for decision in rested_on(root, blocks):
        key = (str(Path(root).resolve()), decision.rel)
        if key not in _RAN:
            _RAN[key] = model_decisions.run(Path(root), decision)
        ran, slug = _RAN[key], decision.ident.rsplit("/", 1)[-1]
        if ran.holds:
            continue
        if not decision.tests:
            reasons.append("design-decision %s (check) names no test" % slug)
            continue
        reasons.append("design-decision %s (check) fails: %s: %s" % (slug, ", ".join(decision.tests), ran.why))
    return reasons


def check(root, item, others=()):
    """(reasons, warnings): the request lines not settled, then the well-formed reasons (D8), laid over `others`, then
    the `check` decisions the item's capabilities rest on that fail (D13); the item's own ids are the only ones whose
    L1 refuses."""
    reasons, warnings = well_formed(root, item, others)
    blocks = backlog_lines.read(item, rel_of(item.name))
    return unsettled(root, item) + reasons + decision_reasons(root, blocks), warnings
