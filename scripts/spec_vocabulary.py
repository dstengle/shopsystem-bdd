"""The vocabulary of a context with a domain model (the domain contract design, §4.2): `spec/vocabulary/<area>.md`, one
layer an area (its frontmatter `area:`, else the file's stem), and `shared.md`, the layer every area reads. Each entry
names one model element: `- **design-decision** (noun) → object design-decision. Forms: design-decisions.`, the
element by domain_model's qualified id up to the first `. `, then a gloss and the fields spec_lexicon reads (`Forms:`,
`Plural:`, `Not:`, `This:`, `Redefines:`, a thin `Frame:` of word order and prepositions, `<x>` its slots).

An area reads its own layer, the layers of the areas its model file imports, then `shared` (`layers_of`). The
problems (`problems`): v_t18 (an entry names no element), v_t19 (it names one the model does not declare), v_t20 (two
entries of one layer name one element and neither is a form of the other) and v_t21 (`imports: [cli]` in a context
with a domain model, switched on once the plugin has the request pack `grammar/packs/request.md`).
spec_vocabulary_terms turns the entries into spec_lexicon's terms.
"""
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import domain_model
import spec_lexicon
import spec_packs
from model_parse import frontmatter

ENTRY = re.compile(r"^- \*\*(?P<term>.+?)\*\*\s*\((?P<label>[^)]*)\)\s*(?P<arrow>→|->)?\s*(?P<text>.*)$", re.DOTALL)
REF = re.compile(r"^(?P<ref>.+?)\.(?:\s+(?P<rest>.*))?$", re.DOTALL)
SHARED = "shared"
REQUEST_PACK = spec_packs.PLUGIN / "request.md"


@dataclass(frozen=True)
class Entry:
    term: str
    label: str              # its part of speech, as written
    ref: str                # the element it names, as written ("" with no `→`)
    text: str               # the gloss and the fields after the element
    where: str              # the file
    layer: str              # the area, or `shared`
    element: object = None  # domain_model.Element, or None when the model declares none

    @property
    def fields(self):
        """The spec_lexicon.Term of the entry's part of speech and fields, its category as the label reads."""
        return spec_lexicon.entry("- **%s** (%s): %s" % (self.term, self.label, self.text), self.where)

    def spellings(self):
        t = self.fields
        return {self.term} | set(t.forms) | ({t.plural} if t.plural else set())


def _bullets(body):
    out = []
    for line in body.splitlines():
        if line.startswith("- "):
            out.append(line)
        elif out and line[:1].isspace() and line.strip():
            out[-1] += " " + line.strip()
    return out


def entries(root):
    """Every entry of every vocabulary file of the context at `root`, in file order, its element resolved."""
    root = Path(root)
    model = domain_model.load(root)
    out = []
    for path in sorted((root / "spec" / "vocabulary").glob("*.md")):
        head, body = frontmatter(path.read_text(encoding="utf-8"))
        layer, where = str(head.get("area") or path.stem), path.relative_to(root).as_posix()
        for bullet in _bullets(body):
            found = ENTRY.match(" ".join(bullet.split()))
            if not found:
                continue
            ref, text = "", found.group("text").strip()
            if found.group("arrow"):
                parts = REF.match(text)
                ref, text = (parts.group("ref").strip(), (parts.group("rest") or "").strip()) if parts else (text, "")
            out.append(Entry(found.group("term").strip(), " ".join(found.group("label").split()), ref, text, where,
                             layer, model.resolve(ref) if ref else None))
    return out


def layers_of(root, area):
    """The layers a capability of `area` reads, nearest first: its own, each its model file imports, `shared`."""
    model = domain_model.load(root)
    imported = model.areas[area].imports if area in model.areas else ()
    return list(dict.fromkeys([area, *imported, SHARED]))


def _twice(found):
    by_element = defaultdict(list)
    for e in found:
        if e.element:
            by_element[(e.layer, e.element)].append(e)
    for (layer, element), group in by_element.items():
        for n, b in enumerate(group[1:], 1):
            if not any(b.term in a.spellings() or a.term in b.spellings() for a in group[:n]):
                yield ("v_t20", b.term, "%s: %s and %s both name %s %s in the layer %s" % (
                    b.where, group[0].term, b.term, element.kind, element.id, layer))


def problems(root):
    """v_t18-v_t21 of the context at `root`, as (code, term, message) sorted; none with no `spec/model/`."""
    if not domain_model.exists(root):
        return []
    found = entries(root)
    out = [("v_t18", e.term, "%s: the entry names no element of the model (write `→ <element>`)" % e.where)
           for e in found if not e.ref]
    out += [("v_t19", e.term, "%s: the entry names %s, which the model does not declare" % (e.where, e.ref))
            for e in found if e.ref and not e.element]
    out += list(_twice(found))
    if REQUEST_PACK.is_file() and "cli" in spec_packs.imports(root):
        why = "spec/index.md imports the retired pack cli; import request, and run `migrate upgrade`"
        out.append(("v_t21", "cli", why))
    return sorted(set(out))
