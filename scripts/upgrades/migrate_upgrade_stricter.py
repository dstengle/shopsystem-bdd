"""The 0.45.0 upgrade step "the stricter rules" (b851, b853, upgrades r48): it rewords no line and no entry, and
- reports, as `notes`, each term and transition that rules made stricter since 0.38.0 fail now, read off `spec check`'s
  solve of the tree the steps before it left (model_check's `solve`): each term whose `Frame:` v_t13 now refuses (text
  after it, no slot in angle brackets, a slot that names nothing: b811, b840), each vocabulary entry whose part of
  speech does not fit its element (v_t22, b825), each lifecycle transition an operation of another area performs
  (v_m9, b610), and each requirement of a codified-2 capability grammar 4 refuses on that tree, by id with the
  refusal (spec_language's, spec_refusal4's naming the verb and the frame: a subject an actor's Frame: no longer takes,
  b847, b853: `refused`), for a session to reword;
- writes spec/index.md's `## Composition` in the index form (spec_composition, b606), so the first `work batch start`
  after the upgrade does not drop its old subsections unseen."""
import re
from pathlib import Path

import spec_composition
import spec_grammar4
import spec_language
import spec_read

from upgrades.migrate_upgrade_ids import Changes

NAME = "the stricter rules"
CODES = ("v_t13", "v_t22", "v_m9")


def word(term):
    """A term as `spec check` names it, `term/<path>/the-desk-service`, or a word: the word, `the desk service`."""
    return term.rsplit("/", 1)[-1].replace("-", " ") if term.startswith("term/") else term


def found(root):
    """Each violation of CODES in the tree at `root`, as (code, args of strings), in `spec check`'s order."""
    from model_check import solve
    from model_facts import Model
    return [(name, [str(a) for a in args]) for name, args in solve(Model(root).read())[0] if name in CODES]


def line(code, args):
    if code == "v_m9":
        obj, attribute, before, after = args
        return ("%s: %s %s, %s, %s, %s: the transition %s → %s of the %s of %s is performed by an operation of "
                "another area" % (NAME, code, obj, attribute, before, after, before, after, attribute, obj))
    return "%s: %s %s: %s" % (NAME, code, word(args[0]), re.sub(r"\s+", " ", args[1]))


def refused(root):
    """A note of each live requirement of a codified-2 capability that grammar 4 refuses, `<cap>#r<n>: <refusal>`,
    by file and id; a spec grammar 4 cannot be built of said in one note."""
    said = []
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")):
        capability = spec_read.capability(path, (spec_read.MARKER4,))
        said += [(capability.name, r) for g in capability.groups for r in g.requirements]
    try:
        why = [(name, r.id, spec_language.parse(root, r.text).refusal) for name, r in said]
    except Exception as error:      # noqa: BLE001 -- a vocabulary GF cannot compile: said, the upgrade goes on
        return ["%s: grammar 4 could not be built of this spec, so no requirement was parsed: %s" % (NAME, error)]
    return ["%s: %s#%s: %s" % (NAME, name, ident, re.sub(r"\s+", " ", why)) for name, ident, why in why if why]


def plan(root):
    root = Path(root)
    changes = Changes()
    changes.notes = []
    index = root / "spec" / "index.md"
    if not index.is_file() or not spec_grammar4.marked(root):
        return changes
    text = index.read_text()
    composed = spec_composition.composed(root, text)
    if composed != text:
        changes.texts["spec/index.md"] = composed
    changes.notes = [line(code, args) for code, args in found(root)] + refused(root)
    return changes
