"""The 0.34.0 upgrade step "value kinds" (b257): it changes no file, and reports, as `notes`, what a session declares and
rewords now that an attribute's values are adjectives or nouns (spec_value_kinds):
- each attribute entry of the glossary or a capability's `## Terms` that gives a plain `Values:` (`w_value_kind`), by
  file, for a session to write as `Values (adjective):` and `Values (noun):`;
- each line of a codified-2 file that says a value of such an attribute in the short form "x is `v`", by file and
  id with the value: once its attribute declares `v` a noun, the line is refused until it says the full form, "the T
  of the K is `v`" or "a K whose T is `v`".
Until a session declares them, every line parses as it did under 0.33."""
import re
from pathlib import Path

import spec_grammar4
import spec_lexicon
import spec_meaning
import spec_read
import spec_value_kinds
from migrate_upgrade_ids import Changes

NAME = "value kinds"


def undeclared(lexicon):
    """Each attribute entry with a plain `Values:`, as (file, term, kinds)."""
    return [(t.where, t.term, t.kinds) for t in lexicon.of("attribute") if spec_value_kinds.undeclared(t)]


def lines(root):
    """(capability, id, text) of each requirement of a capability file that says `language: codified-2`."""
    out = []
    for path in sorted((root / "spec" / "capabilities").glob("*.md")):
        cap = spec_read.capability(path, (spec_read.MARKER4,))
        out += [(path.stem, r.id, r.text) for g in cap.groups for r in g.requirements]
    return out


def short(root, terms):
    """Each (capability, id, attribute term, value) of a line that says a value of one of `terms` in the short form."""
    vocab = spec_grammar4.load(root)[0]
    ids = {"t_%s_%d" % (re.sub(r"[^a-z0-9]+", "_", t.term.lower()).strip("_") or "x", n): t
           for n, (t, _) in enumerate(vocab.attributes, 1)}
    out = []
    for cap, rid, text in lines(root):
        parsed = spec_grammar4.parse(root, text)
        tree = parsed.tree or (parsed.trees[0] if len(parsed.trees) == 1 else None)
        if not tree:
            continue
        for fun, _, values in spec_value_kinds.short_forms(spec_meaning.read(tree)):
            T = spec_value_kinds.SHORT.match(fun).group(1)
            t = ids.get(T)
            if t is not None and t.term in terms:
                out += [(cap, rid, t.term, v) for v in spec_value_kinds.values_of(values, t, T)]
    return list(dict.fromkeys(out))


def plan(root):
    root = Path(root)
    changes = Changes()
    if not (root / "spec" / "index.md").is_file() or not spec_grammar4.marked(root):
        return changes
    found = undeclared(spec_lexicon.read(root))
    changes.notes = ["%s: w_value_kind %s (attribute of %s), %s: declares neither Values (adjective): nor Values "
                     "(noun):" % (NAME, term, ", ".join(kinds), where) for where, term, kinds in found]
    changes.notes += ["%s: %s#%s says %s of the %s in the short form: if it is a noun, write the full form" % (
        NAME, cap, rid, value, term) for cap, rid, term, value in short(root, {term for _, term, _ in found})]
    return changes
