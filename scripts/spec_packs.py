"""The packs of a bounded context (the CNL 4 design, call 10): files of terms a context imports.

A plugin pack is `grammar/packs/<name>.md` of the plugin, a context's own pack `spec/packs/<name>.md` (with a `source:`
naming where it was copied from); both hold term entries under `## Glossary`, in the glossary's entry form, and may
hold `## Relations` and `## Definitions`. `spec/index.md` imports packs in its frontmatter: `imports: [cli, time]`.

The layers, lowest first (`layers`): each imported pack in the order listed, then the glossary of `spec/index.md`,
then each capability's `## Terms`. A word a higher layer defines that an imported pack defines too carries
`Redefines: <pack>` on its entry, else it is unmarked (v_t16); an import that names no pack is v_t17. The requirement
grammar of codified-1 does not read the packs' words: `model lexicon` and these checks do, and grammar 4
(spec_rgl_vocab) reads them as its layers.
"""
import re
from pathlib import Path

import spec_lexicon

PLUGIN = Path(__file__).resolve().parents[1] / "grammar" / "packs"
IMPORTS = re.compile(r"^imports:\s*\[(?P<names>[^\]]*)\]\s*$", re.MULTILINE)


def _frontmatter(text):
    found = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    return found.group(1) if found else ""


def imports(root):
    """The names `spec/index.md` imports, in its order."""
    path = Path(root) / "spec" / "index.md"
    found = IMPORTS.search(_frontmatter(path.read_text())) if path.is_file() else None
    return [n.strip() for n in found.group("names").split(",") if n.strip()] if found else []


def path_of(root, name):
    """The file of the pack `name`: the context's own, else the plugin's; None when neither has it."""
    for path in (Path(root) / "spec" / "packs" / ("%s.md" % name), PLUGIN / ("%s.md" % name)):
        if path.is_file():
            return path
    return None


def terms(path, where):
    return [t for t in (spec_lexicon.entry(b, where) for b in spec_lexicon._bullets(path.read_text(), "Glossary"))
            if t]


def redefines(term):
    """The packs an entry's `Redefines:` names."""
    return [n.strip() for n in spec_lexicon._field(term.text, "Redefines").split(",") if n.strip()]


def missing(root):
    """The imported names no pack is (v_t17)."""
    return [n for n in imports(root) if path_of(root, n) is None]


def layers(root, lexicon=None):
    """Every term with its layer, lowest first: (layer, term), a pack's layer `pack <name>`, the context's the file
    that holds the entry."""
    root = Path(root)
    out = []
    for name in imports(root):
        path = path_of(root, name)
        if path is not None:
            where = path.relative_to(root).as_posix() if path.is_relative_to(root) else "grammar/packs/%s.md" % name
            out += [("pack %s" % name, t) for t in terms(path, where)]
    lexicon = lexicon or spec_lexicon.read(root)
    return out + [(t.where, t) for t in lexicon.terms]


def unmarked(root, lexicon=None):
    """Each of the context's terms that an imported pack defines too, with the packs its entry does not name in
    `Redefines:`, as {(where, term): [pack, ...]} (v_t16)."""
    by_pack, out = {}, {}
    for layer, t in layers(root, lexicon):
        if layer.startswith("pack "):
            by_pack.setdefault(t.term, []).append(layer[len("pack "):])
            continue
        unnamed = [p for p in by_pack.get(t.term, []) if p not in redefines(t)]
        if unnamed:
            out[(t.where, t.term)] = unnamed
    return out


def problems(root, lexicon=None):
    """v_t16 and v_t17 as (code, subject, message)."""
    out = [("v_t17", n, "spec/index.md imports the pack %s, which neither grammar/packs/ nor spec/packs/ has" % n)
           for n in missing(root)]
    out += [("v_t16", term, "%s: the pack %s defines %s too; mark the entry Redefines: %s" % (
        where, ", ".join(packs), term, ", ".join(packs))) for (where, term), packs in unmarked(root, lexicon).items()]
    return sorted(out)
