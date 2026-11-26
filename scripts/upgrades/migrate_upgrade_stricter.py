"""The 0.45.0 upgrade step "the stricter rules" (b851, upgrades r47): it rewords no line and no entry, and
- reports, as `notes`, each term and transition that rules made stricter since 0.38.0 fail now, read off `spec check`'s
  solve of the tree the steps before it left (model_check's `solve`): each term whose `Frame:` v_t13 now refuses (text
  after it, no slot in angle brackets, a slot that names nothing: b811, b840), each vocabulary entry whose part of
  speech does not fit its element (v_t22, b825), each lifecycle transition an operation of another area performs
  (v_m9, b610), for a session to reword;
- writes spec/index.md's `## Composition` in the index form (spec_composition, b606), so the first `work batch start`
  after the upgrade does not drop its old subsections unseen."""
import re
from pathlib import Path

import spec_composition
import spec_grammar4

from upgrades.migrate_upgrade_ids import Changes

NAME = "the stricter rules"
CODES = ("v_t13", "v_t22", "v_m9")


def word(term, root):
    """A term as `spec check` names it, `term/<path>/follow-up`, or a word: the word as its entry writes it, the term
    of the lexicon at `root` whose id is the node's (`follow-up`, its hyphen kept: b854), else the id's last part."""
    if not term.startswith("term/"):
        return term
    import spec_lexicon
    from model_facts import Model
    from model_spec import term_word
    node, model = term.rsplit("/", 1)[-1], Model(root)
    for t in spec_lexicon.read(root).terms:
        if model.term_id(" ".join(term_word(t).lower().split())).rsplit("/", 1)[-1] == node:
            return t.term
    return node


def found(root):
    """Each violation of CODES in the tree at `root`, as (code, args of strings), in `spec check`'s order."""
    from model_check import solve
    from model_facts import Model
    return [(name, [str(a) for a in args]) for name, args in solve(Model(root).read())[0] if name in CODES]


def line(code, args, root):
    if code == "v_m9":
        obj, attribute, before, after = args
        return ("%s: %s %s, %s, %s, %s: the transition %s → %s of the %s of %s is performed by an operation of "
                "another area" % (NAME, code, obj, attribute, before, after, before, after, attribute, obj))
    return "%s: %s %s: %s" % (NAME, code, word(args[0], root), re.sub(r"\s+", " ", args[1]))


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
    changes.notes = [line(code, args, root) for code, args in found(root)]
    return changes
