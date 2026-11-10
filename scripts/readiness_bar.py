"""The readiness bar (capability readiness; workflow simplification plan 3, D6-D9, D11): an item is passing when every
request line of the item is settled and its requirement lines are well-formed: they parse in the context's grammar,
they bring no problem of the lexicon (v_t4 to v_t13) that the lexicon without them does not have
(readiness r15), `model logic` finds no L0 and no L1 naming them, and `features generate` writes a scenario for each of their groups
that is not logic-only, with no step holding a bracketed placeholder (b46). The lines are checked on a copy of `spec/` under the temporary directory with the item's lines
laid in, removed afterwards whatever happens; `spec/` itself is never written. The `check` design-decisions that a
capability of the item's lines rests on run their tests on the root checkout, each once a process (plan 6, D13)."""
import contextlib
import io
import re
import shutil
import tempfile
from pathlib import Path

import backlog_lines
import features_generate
import model_decisions
import request_moves
import request_text
import spec_grammar
import spec_lexicon
import spec_read
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
    """A reason for each of the item's requirements, and universal conditions (b43), that does not parse."""
    reasons = []
    statements = [("%s#%s" % (b.capability, rid), text) for b in blocks for g in b.groups for rid, text in
                  g.requirements] + [("universal#%s" % uid, text) for uid, text in blocks.universal]
    for ident, text in statements:
        parsed = spec_grammar.parse(copy, text)
        if parsed.tree is None:
            hint = spec_grammar.hint(copy, text)
            reasons.append("%s: %s; parsed up to: %s; nearest words: %s" % (
                ident, parsed.refusal, hint["prefix"] or "nothing", ", ".join(hint["near"]) or "none"))
    return reasons


def _logic(copy, mine):
    """(reasons, warnings) of `model logic` on the copy: an L0, and an L1 naming one of `mine`, refuse (D6); an L3
    naming one of them is a warning."""
    reasons, warnings = [], []
    for f in spec_solve.run(copy):
        said = "%s %s" % (f.code, f.text)
        if f.code == "L0" or (f.code == "L1" and set(f.ids) & mine):
            reasons.append(said)
        elif f.code == "L3" and set(f.ids) & mine:
            warnings.append(said)
    return list(dict.fromkeys(reasons)), list(dict.fromkeys(warnings))


_STEP = re.compile(r"^    (Given|When|Then|And|But) (.*)$")
_PLACEHOLDER = re.compile(r"\[[A-Za-z_][A-Za-z0-9_]*\]")   # a Steps fun with no English, as GF writes it
_LITERAL = re.compile(r"`[^`]*`|\"[^\"]*\"")


def unworded(text):
    """{group id: [step text]} of the steps of a feature text that hold a bracketed placeholder (b46), outside a
    backticked or quoted literal; the group is the scenario's first tag."""
    found, group = {}, None
    for line in text.splitlines():
        if line.startswith("  @"):
            group = line.split()[0][1:]
        step = _STEP.match(line)
        if step and group and _PLACEHOLDER.search(_LITERAL.sub("", step.group(2))):
            found.setdefault(group, []).append(step.group(2))
    return found


def _scenarios(copy, blocks):
    """A reason for each group of a service capability that `features generate` writes no scenario for, unless it is
    logic-only (D9), and for each step of its scenario that holds a bracketed placeholder (b46); a guarantees
    capability has no scenarios."""
    reasons = []
    for block in blocks:
        path = backlog_lines.capability_file(copy, block.capability)
        if spec_read.capability(path).frontmatter.get("group") == "guarantees" or not block.groups:
            continue
        skipped = {}
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                text = features_generate.generate(copy, path, skipped)
        except features_generate.GenerateError as err:
            reasons.append("%s: %s" % (block.capability, err))
            continue
        placeholders = unworded(text)
        for group in block.groups:
            gid = "%s#%s" % (block.capability, group.id)
            if gid in skipped:
                reasons.append("%s has no scenario: %s" % (gid, skipped[gid]))
            reasons += ["%s has a step no step words: %s" % (gid, s) for s in placeholders.get(group.id, ())]
    return reasons


def well_formed(root, item, others=()):
    """(reasons, warnings) of the item's requirement lines, checked on a copy of `spec/` with them laid in (D6, D7, D9),
    over the lines of `others` (a batch's items picked before it, plan 4 D7). An item with no line is not passing."""
    blocks = backlog_lines.read(item, rel_of(item.name))
    mine = set(backlog_lines.ids(blocks))
    if not mine:
        return ["it has no requirement line: give it one with `work line`"], []
    copy = Path(tempfile.mkdtemp(prefix="readiness-"))
    try:
        shutil.copytree(Path(root) / "spec", copy / "spec")      # backlog_lines.lay, the lexicon read before the item
        for other in others:
            backlog_lines.lay_onto(copy, other)
        before = set(spec_lexicon.problems(spec_lexicon.read(copy)))
        backlog_lines.lay_onto(copy, item)
        reasons = ["%s.md: %s" % (b.capability, p) for b in blocks
                   for p in spec_read.capability(backlog_lines.capability_file(copy, b.capability)).problems]
        reasons += ["universal.md: %s" % p for p in spec_read.read_universal(copy).problems] if blocks.universal else []
        reasons += ["the lexicon: %s %s: %s" % found for found in spec_lexicon.problems(spec_lexicon.read(copy))
                    if found not in before]                                                             # r15
        reasons = reasons or _parses(copy, blocks)
        if reasons:
            return reasons, []
        reasons, warnings = _logic(copy, mine)
        return reasons + _scenarios(copy, blocks), warnings
    finally:
        shutil.rmtree(copy, ignore_errors=True)


_RAN = {}     # (resolved root, decision's path): its run, once a process (D13)


def rested_on(root, blocks):
    """The `check` decisions that a capability of the blocks rests on, matched by the id's last segment (a capability
    writes `design-decision/<slug>` or the full id), in file order, each once."""
    slugs = set()
    for block in blocks:
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
