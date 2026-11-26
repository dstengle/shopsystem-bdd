"""`spec coupling` (b612, checking r144-r146): the specification service's report of the coupling between the areas
of the context's domain model (`spec/model/`), each area a context the disentangling (decisions 0129-0133) will make.
A coupling is of the area depended on, by another area, and holds what couples them: each word both areas' vocabulary
layers define, of the area of the word's later entry in file order (r144, `words`); each element of the area that an
element of the other's model refers to by its word (a relation's or an object attribute's target, a `kind of`, an
operation's object or a parameter naming an object, the operation an event is raised by), named by its kind and id
(r145, `elements`); each requirement of a capability of the other area whose logical form uses a term only the area's
layer holds (r146, `requirements`). The couplings most first (`couplings`), the content of a `returned` response
printed as text (`text`) or as the envelope under `--json`; each tracked Python file of the other area that imports
one of the area's, the module groups declared in `.shop/modules.toml` (r147, b744, decision 0151: spec_coupling_imports,
`imports`, each `<importer> -> <imported>`)."""
import re
from collections import defaultdict
from pathlib import Path

from plumbing.domain_envelope import Response

KINDS = ("words", "elements", "requirements", "imports")


def _coupling(found, area, by):
    return found.setdefault((area, by), {"area": area, "by": by, **{k: set() for k in KINDS}})


def _words(root, found):
    """r144: a word two areas' layers define, of each two of them the coupling of the area of its later entry by
    the earlier's."""
    import spec_vocabulary
    earlier = defaultdict(list)
    for e in spec_vocabulary.entries(root):
        if e.layer == spec_vocabulary.SHARED or e.layer in earlier[e.term]:
            continue
        for held in earlier[e.term]:
            _coupling(found, e.layer, held)["words"].add(e.term)
        earlier[e.term].append(e.layer)


def _references(model):
    """(area referring, element referred to) of each reference of one model element to another's object or
    operation."""
    objects = model.objects
    for obj in objects.values():
        named = {t for r in obj.relations for t in r.targets} | {obj.kind_of}
        named |= {t for a in obj.attributes if a.type == "object" for t in a.targets}
        yield from ((obj.area, ("object", n)) for n in named if n in objects)
    for service in model.services.values():
        for op in service.operations:
            named = {op.object} | {t for p in op.parameters if p.type == "object" for t in p.targets}
            yield from ((service.area, ("object", n)) for n in named if n in objects)
    for event in model.events:
        found = model.services.get(event.service)
        if found and found.operation(event.operation):
            yield event.area, ("operation", "%s.%s" % (event.service, event.operation))


def _elements(root, found):
    """r145: an element of an area another area's model refers to, the coupling of the area that holds it."""
    import domain_model
    model = domain_model.load(root)
    for by, (kind, name) in _references(model):
        element = model.resolve("%s %s" % (kind, name))
        if element and element.area and by and element.area != by:
            _coupling(found, element.area, by)["elements"].add("%s %s" % (kind, name))


def _requirements(root, found):
    """r146: a requirement of an area's capability that uses a term only another area's layer holds, the coupling
    of that area by the requirement's."""
    import spec_grammar4
    import spec_language
    import spec_lexicon
    import spec_lf
    import spec_read
    import spec_vocabulary
    from model_domain import uses
    layer_of = {e.where: e.layer for e in spec_vocabulary.entries(root)}
    held = defaultdict(set)
    for t in spec_lexicon.read(root).terms:
        if layer_of.get(t.where) not in (None, spec_vocabulary.SHARED):
            held[(t.category, t.term)].add(layer_of[t.where])
    vocab = None
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")):
        cap = spec_read.capability(path, ("codified-2",))
        area = str(cap.frontmatter.get("area") or "")
        if not area or cap.problems and not cap.groups:
            continue
        for group in cap.groups:
            for req in group.requirements:
                parsed = spec_language.parse(root, req.text)
                if parsed.tree is None:
                    continue
                vocab = vocab or spec_grammar4.load(root)[0]
                for word in sorted(uses(spec_lf.form(vocab, parsed.tree))):
                    areas = held.get(word, set())
                    for other in sorted(areas - {area}) if area not in areas else ():
                        _coupling(found, other, area)["requirements"].add("%s#%s" % (cap.name, req.id))


def _imports(root, found):
    """r147: a Python file of an area that imports another area's, the coupling of the imported file's area."""
    import spec_coupling_imports
    for area, by, said in spec_coupling_imports.imports(root):
        _coupling(found, area, by)["imports"].add(said)


def _natural(name):
    """`batches#r9` before `batches#r10`."""
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", name)]


def couplings(root):
    """Every coupling between the areas of the context at `root`, most first: each with its area, the area `by` that
    depends on it, and its sorted words, elements and requirements."""
    import domain_model
    found = {}
    if domain_model.exists(root):
        _words(root, found)
        _elements(root, found)
        _requirements(root, found)
        _imports(root, found)
    out = [{**c, **{k: sorted(c[k], key=_natural) for k in KINDS}} for c in found.values()]
    return sorted(out, key=lambda c: (-sum(len(c[k]) for k in KINDS), c["area"], c["by"]))


def text(found):
    if not found:
        return "no coupling between the areas\n"
    lines = []
    for c in found:
        counts = ", ".join("%d %s" % (len(c[k]), k[:-1] if len(c[k]) == 1 else k)
                           for k in KINDS)
        lines.append("%s by %s: %s" % (c["area"], c["by"], counts))
        lines += ["  %s: %s" % (k[:-1], ", ".join(c[k])) for k in KINDS if c[k]]
    return "\n".join(lines) + "\n"


def cmd(args):
    found = {"couplings": couplings(Path(args.root))}
    if not args.json:
        print(text(found["couplings"]), end="")
    return Response("returned", found)


def add_parser(sub):
    sub.add_parser("coupling", help="print the coupling between the areas of the domain model, most first")


COMMANDS = {"coupling": cmd}
