#!/usr/bin/env python3
"""Coupling between the areas of shopsystem-bdd, read-only.

Run from anywhere:  python3 coupling.py /home/vscode/shopsystem-bdd  > coupling.md
Sections:
  0  inventory: each area's model kind, imports, objects, services, operations, vocabulary entries, capabilities, lines
  a  words shared across vocabulary layers; vocabulary entries naming another area's element; model imports
  b  model relations, attributes, kind-of and operation parameters whose target object is another area's
  c  capability lines whose logical form (spec_language.parse + spec_lf.form, model_domain.uses) names another
     area's words: each word placed in the layers of the lexicon terms of its category (as v_m1 places it)
  d  Python imports between module groups (groups.py's GROUPS)
Only the standard library is imported by this file; sections 0, a, b, c import the repository's own readers
(domain_model, spec_vocabulary, spec_read, and for c the grammar, which needs pgf). Nothing is written.
"""
import ast
import collections
import os
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "scripts"))
os.chdir(ROOT / "scripts")
sys.path.insert(0, str(Path(__file__).parent))
import groups  # noqa: E402

import domain_model  # noqa: E402
import spec_read  # noqa: E402
import spec_vocabulary  # noqa: E402
from model_parse import frontmatter  # noqa: E402

OUT = []


def p(*a):
    OUT.append(" ".join(str(x) for x in a))


def table(head, rows):
    p("| " + " | ".join(head) + " |")
    p("|" + "---|" * len(head))
    for r in rows:
        p("| " + " | ".join(str(x) for x in r) + " |")
    p("")


model = domain_model.load(ROOT)
areas = sorted(model.areas)
obj_area = {n: o.area for n, o in model.objects.items()}
entries = spec_vocabulary.entries(ROOT)

caps = {}
for path in sorted((ROOT / "spec/capabilities").glob("*.md")):
    fm = frontmatter(path.read_text())[0]
    if fm.get("area"):
        caps[path.stem] = (str(fm["area"]), path)

# ---- 0 inventory
p("## 0. Inventory\n")
rows = []
for a in areas:
    ar = model.areas[a]
    objs = [o for o in model.objects.values() if o.area == a]
    svcs = [s for s in model.services.values() if s.area == a]
    ops = sum(len(s.operations) for s in svcs)
    evs = [e for e in model.events if getattr(e, "area", None) == a]
    acts = [x for x in model.actors.values() if x.area == a]
    voc = [e for e in entries if e.layer == a]
    cs = sorted(c for c, (ca, _) in caps.items() if ca == a)
    lines = 0
    for c in cs:
        cap = spec_read.capability(caps[c][1])
        lines += sum(len(g.requirements) for g in cap.groups)
    rows.append((a, ar.kind, ", ".join(ar.imports) or "-", len(objs), len(svcs), ops, len(evs), len(acts),
                 len(voc), len(cs), lines, ", ".join(cs)))
rows.append(("shared (layer)", "-", "-", "", "", "", "", "", len([e for e in entries if e.layer == "shared"]), "", "", ""))
table(["area", "kind", "imports", "objects", "services", "operations", "events", "actors", "vocab entries",
       "capabilities", "live lines", "capability names"], rows)
p("Services and operations per area:\n")
table(["area", "service", "operations"],
      [(s.area, s.name, ", ".join(o.name for o in s.operations)) for s in sorted(model.services.values(), key=lambda s: (s.area, s.name))])

# ---- a
p("## a. Shared words and imports\n")
p("Model imports (area -> areas it imports):\n")
table(["area", "imports", "imported by"],
      [(a, ", ".join(model.areas[a].imports) or "-",
        ", ".join(b for b in areas if a in model.areas[b].imports) or "-") for a in areas])
by_word = collections.defaultdict(set)
for e in entries:
    by_word[e.term.lower()].add(e.layer)
multi = sorted((w, ls) for w, ls in by_word.items() if len(ls) > 1)
p("Words with entries in more than one layer: %d\n" % len(multi))
table(["word", "layers"], [(w, ", ".join(sorted(ls))) for w, ls in multi])
cross = collections.Counter()
crossw = collections.defaultdict(list)
for e in entries:
    el = e.element
    if el is None or not getattr(el, "area", None):
        continue
    if el.area != e.layer:
        cross[(e.layer, el.area)] += 1
        crossw[(e.layer, el.area)].append(e.term)
p("Vocabulary entries whose element is declared in another area's model (layer -> element's area): %d\n"
  % sum(cross.values()))
table(["layer", "element's area", "entries", "words"],
      [(k[0], k[1], n, ", ".join(crossw[k][:12]) + (" ..." if len(crossw[k]) > 12 else ""))
       for k, n in cross.most_common()])

# ---- b
p("## b. Model references to another area's objects\n")
refs = []
for o in model.objects.values():
    for r in o.relations:
        for t in r.targets:
            if obj_area.get(t) and obj_area[t] != o.area:
                refs.append((o.area, obj_area[t], "relation", "%s %s -> %s" % (o.name, r.phrase, t)))
    for at in o.attributes:
        for t in at.targets:
            if obj_area.get(t) and obj_area[t] != o.area:
                refs.append((o.area, obj_area[t], "attribute", "%s.%s -> %s" % (o.name, at.name, t)))
    if o.kind_of and obj_area.get(o.kind_of) and obj_area[o.kind_of] != o.area:
        refs.append((o.area, obj_area[o.kind_of], "kind of", "%s kind of %s" % (o.name, o.kind_of)))
for s in model.services.values():
    for op in s.operations:
        for prm in op.parameters:
            for t in prm.targets:
                if obj_area.get(t) and obj_area[t] != s.area:
                    refs.append((s.area, obj_area[t], "parameter", "%s.%s(%s)" % (s.name, op.name, prm.name)))
        if op.object and obj_area.get(op.object) and obj_area[op.object] != s.area:
            refs.append((s.area, obj_area[op.object], "operation object", "%s.%s on %s" % (s.name, op.name, op.object)))
pairs = collections.Counter((a, b) for a, b, _, _ in refs)
p("Total: %d\n" % len(refs))
table(["from area", "to area", "count"], [(a, b, n) for (a, b), n in pairs.most_common()])
objc = collections.Counter(x[3].split(" -> ")[-1] for x in refs if " -> " in x[3])
p("Most referenced foreign objects (relations, attributes):\n")
table(["object", "its area", "references"], [(o, obj_area[o], n) for o, n in objc.most_common(15)])
p("All references:\n")
table(["from", "to", "what", "reference"], sorted(refs))

# ---- c
p("## c. Capability lines naming another area's words (logical form)\n")
try:
    import model_domain
    import spec_grammar4
    import spec_language
    import spec_lexicon
    import spec_lf
    vocab = spec_grammar4.load(ROOT)[0]
    terms = spec_lexicon.read(ROOT).terms
    layer_of = {e.where: e.layer for e in entries}
    lay = collections.defaultdict(set)
    for t in terms:
        lay[(t.category, t.term)].add(layer_of.get(t.where, "pack/base"))
    shared_home = collections.defaultdict(set)
    for e in entries:
        if e.layer == "shared" and e.element is not None:
            shared_home[e.term.lower()].add(e.element.area)
    person = collections.Counter()
    sharedown = collections.Counter()
    usec = collections.Counter()
    wordc = collections.defaultdict(collections.Counter)
    linec = collections.Counter()
    unparsed, total = [], 0
    detail = []
    for c, (a, path) in sorted(caps.items()):
        cap = spec_read.capability(path)
        for g in cap.groups:
            for r in g.requirements:
                total += 1
                parsed = spec_language.parse(ROOT, r.text)
                if parsed.tree is None:
                    unparsed.append("%s#%s" % (c, r.id))
                    continue
                form = spec_lf.form(vocab, parsed.tree)
                foreign = set()
                for cat, word in model_domain.uses(form):
                    ls = lay.get((cat, word), {"pack/base"})
                    if a in ls or "pack/base" in ls:
                        continue
                    others = sorted(ls - {"shared"}) or ["shared"]
                    if others == ["shared"]:
                        homes = shared_home.get(word.lower(), set())
                        if a in homes:
                            sharedown[a] += 1
                            continue
                        if (cat, word) == ("actor", "the person"):
                            person[a] += 1
                            continue
                        others = ["shared>" + ("/".join(sorted(homes)) or "?")]
                    for o in others[:1] if len(others) == 1 else ["/".join(others)]:
                        usec[(a, o)] += 1
                        wordc[(a, o)][word] += 1
                        if not o.startswith("shared>" + a):
                            foreign.add((o, word))
                if foreign:
                    linec[a] += 1
                    detail.append(("%s#%s" % (c, r.id), a, "; ".join("%s:%s" % x for x in sorted(foreign))))
    p("Lines read: %d, unparsed: %d (%s)\n" % (total, len(unparsed), ", ".join(unparsed) or "-"))
    p("A use is counted once a word a line names; a word whose terms are in the line's own layer or a pack is"
      " own; one only in `shared` is placed by the area whose model declares its element (`shared>area`; a use of a shared word whose element is the line's own area is own); any other is the area(s) whose layers hold it.\n")
    p("Uses of shared words of the line's own area, counted as own: %s\n" % dict(sharedown))
    p("Uses of the actor `the person` (declared in tracking's model, named by every area), left out below: %s\n"
      % dict(person))
    table(["line's area", "word's area", "uses", "top words"],
          [(a, b, n, ", ".join("%s (%d)" % kv for kv in wordc[(a, b)].most_common(8)))
           for (a, b), n in usec.most_common()])
    table(["area", "lines naming a word of another area (the person aside)"], sorted(linec.items()))
    p("Lines naming another area's word:\n")
    table(["line", "area", "foreign words (area:word)"], detail)
except Exception as exc:  # the grammar tools absent
    p("Not read: %r\n" % (exc,))

# ---- d
p("## d. Python imports between module groups\n")
mods = {}
for f in sorted((ROOT / "scripts").iterdir()):
    if f.is_file() and (f.suffix == ".py" or (not f.suffix and f.read_bytes()[:30].startswith(b"#!/usr/bin/env python"))):
        mods[f.stem if f.suffix else f.name] = f
gof = {m: groups.group(m) for m in mods}
edges = collections.Counter()
ex = collections.defaultdict(set)
for m, f in mods.items():
    try:
        tree = ast.parse(f.read_text())
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            names = [node.module.split(".")[0]]
        for n in names:
            if n in mods and gof[n] != gof[m]:
                edges[(gof[m], gof[n])] += 1
                ex[(gof[m], gof[n])].add("%s->%s" % (m, n))
sizes = collections.Counter(gof.values())
p("Modules per group:\n")
table(["group", "modules", "lines"], [(g, sizes[g], sum(len(mods[m].read_text().splitlines()) for m in mods if gof[m] == g))
                                     for g in sorted(sizes)])
table(["group", "members"], [(g, ", ".join(sorted(m for m in mods if gof[m] == g))) for g in sorted(sizes)])
p("Import statements from one group to another (static and inside functions): %d\n" % sum(edges.values()))
table(["from group", "to group", "imports", "examples"],
      [(a, b, n, ", ".join(sorted(ex[(a, b)])[:6]) + (" ..." if len(ex[(a, b)]) > 6 else ""))
       for (a, b), n in edges.most_common()])
fan = collections.Counter()
for (a, b), n in edges.items():
    fan[b] += n
p("Fan-in by group (imports from other groups):\n")
table(["group", "imported from other groups"], fan.most_common())

print("\n".join(OUT))
