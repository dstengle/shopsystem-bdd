"""The readiness bar (capability readiness; workflow simplification plan 3, D6-D9, D11): an item is passing when every
request line of the item is settled and its requirement lines are well-formed: they parse in the context's grammar,
`model logic` finds no L0 and no L1 naming them, and `features generate` writes a scenario for each of their groups
that is not logic-only. The lines are checked on a copy of `spec/` under the temporary directory with the item's lines
laid in, removed afterwards whatever happens; `spec/` itself is never written."""
import contextlib
import io
import shutil
import tempfile
from pathlib import Path

import backlog_lines
import features_generate
import spec_grammar
import spec_read
import spec_solve
import workqueue_request
from backlog_items import rel_of


def request_lines(root, item):
    """(number, text, line outcome or None) of each line of the item's request that is not `rewritten` (D11): a
    rewritten line is no longer the item's, its counter-proposal is."""
    request = getattr(item, "request", None)
    if request is None:
        return []
    found = workqueue_request.sections(root, request)
    outcomes = found["Outcomes"]
    return [(int(n), found["Lines"][n], outcomes.get(n)) for n in sorted(found["Lines"], key=int)
            if outcomes.get(n) != "rewritten"]


def unsettled(root, item):
    """A reason for each request line of the item that is not settled."""
    return ["line %d of request %s is %s, not settled: %s" % (n, item.request, outcome or "unanswered", text)
            for n, text, outcome in request_lines(root, item) if outcome not in workqueue_request.SETTLED]


def _parses(copy, blocks):
    reasons = []
    for block in blocks:
        for group in block.groups:
            for rid, text in group.requirements:
                parsed = spec_grammar.parse(copy, text)
                if parsed.tree is None:
                    hint = spec_grammar.hint(copy, text)
                    reasons.append("%s#%s: %s; parsed up to: %s; nearest words: %s" % (
                        block.capability, rid, parsed.refusal, hint["prefix"] or "nothing",
                        ", ".join(hint["near"]) or "none"))
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


def _scenarios(copy, blocks):
    """A reason for each group of a service capability that `features generate` writes no scenario for, unless it is
    logic-only (D9); a guarantees capability has no scenarios."""
    reasons = []
    for block in blocks:
        path = backlog_lines.capability_file(copy, block.capability)
        if spec_read.capability(path).frontmatter.get("group") == "guarantees" or not block.groups:
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


def well_formed(root, item):
    """(reasons, warnings) of the item's requirement lines, checked on a copy of `spec/` with them laid in (D6, D7, D9).
    An item with no line is not passing."""
    blocks = backlog_lines.read(item, rel_of(item.name))
    mine = set(backlog_lines.ids(blocks))
    if not mine:
        return ["it has no requirement line: give it one with `work line`"], []
    copy = Path(tempfile.mkdtemp(prefix="readiness-"))
    try:
        backlog_lines.lay(root, item, copy)
        reasons = ["%s.md: %s" % (b.capability, p) for b in blocks
                   for p in spec_read.capability(backlog_lines.capability_file(copy, b.capability)).problems]
        reasons = reasons or _parses(copy, blocks)
        if reasons:
            return reasons, []
        reasons, warnings = _logic(copy, mine)
        return reasons + _scenarios(copy, blocks), warnings
    finally:
        shutil.rmtree(copy, ignore_errors=True)


def check(root, item):
    """(reasons, warnings): the request lines not settled, then the well-formed reasons (D8)."""
    reasons, warnings = well_formed(root, item)
    return unsettled(root, item) + reasons, warnings
