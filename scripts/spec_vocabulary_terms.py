"""A context's lexicon read from its domain model and vocabulary (the domain contract design, §4.2): each entry of
spec_vocabulary turned into the spec_lexicon.Term the grammars read, its kinds, attributes, values and transitions
from the model (domain_model), not from `Values:`, `Transitions:` or `Kind of:`, and the model's relations as
spec_relations' rows.

- A noun naming an object is a kind, its key the noun; a noun that names two elements in two areas is two kinds, each
  keyed `<noun>_<area>` and spelled the noun (`word`), so that grammar 4 generates one function each.
- A proper noun naming an actor, a service or an object is an actor, of the actor's `kind of` (else `agent`); a
  service's of the request pack's kind `service` in a context importing it.
- An attribute naming `<object>.<attribute>` is an attribute of the object's kind, its values the model's (backticked
  codes, as lines write them), each value an adjective or a noun as the entry that names it says (a value no entry
  names a noun beside named ones; with none named, of no declared kind), its lifecycle's transitions, its type.
- A verb naming a relation or an operation is a verb of its aspect, its thin `Frame:` written with kinds: `<from>`
  the relation's object, `<to>` each of its targets, `<actor>` or `<agent>` the kind `agent`, `<x>` the kind of the
  object or of the parameter `x`; with no frame, `<from> <verb> <to>` or `<actor> <verb> <object>`; a verb naming an
  operation keeps it (`operation`), which grammar 4 generates the request with its parameters from (spec_rgl_ops).
- A relation `has → K` (K an object's kind, or a kind of a pack the index imports, b609) is the row `K | of | O`, `holds → K` the row `K | in | O`, and one whose phrase is a single
  preposition the row `O | <phrase> | K` (session's call); any other phrase is a state verb's, named in the vocabulary.
"""
import re
from collections import defaultdict

import domain_model
import spec_frames
import spec_lexicon
import spec_packs
import spec_relations
import spec_vocabulary

PREPOSITIONS = ("of", "in", "on", "for", "with", "from", "to", "by", "under", "at")
SLOT = re.compile(r"<([^>]+)>")


def qualified(element):
    """The id the check names a model element by (the domain contract design, §5.3): qualified by its area
    (`notes.note`, `notes.note.status`), an operation by its service (`notes.add`)."""
    return element.id if element.kind == "operation" else "%s.%s" % (element.area, element.id)


def _kinds(found, model):
    """{object name: kind key} of every noun naming an object, and the kind terms, each of the kind its object is a
    kind of (`object session kind of agent`)."""
    elements = defaultdict(set)
    for e in found:
        if e.label == "noun" and e.element and e.element.kind == "object":
            elements[e.term].add((e.layer, e.element.id))
    keys, terms = {}, []
    nouns = [e for e in found if e.label == "noun" and e.element and e.element.kind == "object"]
    for e in nouns:
        two = len({layer for layer, _ in elements[e.term]}) > 1 and len({i for _, i in elements[e.term]}) > 1
        keys.setdefault(e.element.id, "%s_%s" % (e.term, re.sub(r"[^a-z0-9]+", "_", e.layer.lower())) if two else e.term)
    done = set()
    for e in nouns:
        if e.element.id in done:
            continue
        done.add(e.element.id)
        key, t = keys[e.element.id], e.fields
        up = model.objects[e.element.id].kind_of
        terms.append(spec_lexicon.Term(term=key, category="kind", text=e.text, where=e.where, label="noun",
                                       plural=t.plural, nots=t.nots, this=t.this, word=e.term if key != e.term else "",
                                       element=qualified(e.element), supertype=keys.get(up, up)))
    return keys, terms


def _actors(model, found, kinds, services=()):
    out = []
    for e in found:
        if e.label != "proper noun" or not e.element or e.element.kind not in ("actor", "service", "object"):
            continue
        kind_of = model.actors[e.element.id].kind_of if e.element.kind == "actor" else ""
        if e.element.kind == "service" and "service" in services:     # the request pack's kind of agent
            kind_of = "service"
        if e.element.kind == "object":     # of its object's kind, or, with no noun naming it, the kind it is of
            kind_of = kinds.get(e.element.id) or model.objects[e.element.id].kind_of
        out.append(spec_lexicon.Term(term=e.term, category="actor", text=e.text, where=e.where, label=e.label,
                                     supertype=kinds.get(kind_of, kind_of) or "agent", nots=e.fields.nots,
                                     element=qualified(e.element)))
    return out


def _order(attr):
    """An attribute's value order (spec_lf_order): of one whose values the model writes `a < b < c`, those values in
    that order, or by number when each is a code of numbers joined by dots (session's call, §4.1); else none."""
    if not attr.values or not attr.ordered:
        return ""
    return "by number" if all(re.fullmatch(r"\d+(\.\d+)*", v) for v in attr.values) else "as listed"


def _attributes(model, found, kinds):
    out = []
    named = {e.element.id: ("adjective" if e.label.startswith("adjective") else "noun")
             for e in found if e.element and e.element.kind == "value"}
    for e in (e for e in found if e.label.startswith("attribute") and e.element and e.element.kind == "attribute"):
        owner, _, name = e.element.id.partition(".")
        obj = model.objects[owner]
        attr = obj.attribute(name)
        values = tuple("`%s`" % v for v in attr.values)
        declared = {v: named.get("%s.%s %s" % (owner, name, v)) for v in attr.values}
        value_kinds = tuple(("`%s`" % v, k or "noun") for v, k in declared.items()) if any(declared.values()) else ()
        transitions = tuple(("`%s`" % a, "`%s`" % b, "") for lc in obj.lifecycles if lc.attribute == name
                            for a, b in lc.transitions)
        kind = kinds.get(owner)
        out.append(spec_lexicon.Term(
            term=e.term, category="attribute", kinds=(kind,) if kind else (), text=e.text, where=e.where,
            label="attribute of %s" % (kind or owner), values=values, value_kinds=value_kinds, order=_order(attr),
            transitions=transitions, type=attr.type if attr.type in ("number", "time", "text") else
            ("" if values else "text"), element=qualified(e.element)))
    return out


def _slot(model, e, name, kinds, strict=False):
    if name in ("actor", "agent"):
        return ["agent"]
    if e.element.kind == "relation":
        owner, _, phrase = e.element.id.partition(".")
        rel = model.objects[owner].relation(phrase)
        if name == "from":
            return [kinds.get(owner, owner)]
        if name == "to":
            return [kinds.get(t, t) for t in rel.targets]
    if name in kinds:
        return [kinds[name]]
    if e.element.kind == "operation":
        service, _, op = e.element.id.rpartition(".")
        param = next((p for p in model.services[service].operation(op).parameters if p.name == name), None)
        if param:     # a parameter of no object a slot of `thing`
            return [kinds.get(t, t) for t in param.targets] or ["thing"]
    return None if strict else ["thing"]


def _slotless(model, e, frame, kinds):
    """Whether a written `Frame:` takes no noun phrase: no slot in angle brackets, or none naming a kind, an actor or
    a parameter of its operation (b811); such a frame is a v_t13 (spec_frames), never read as of `thing`; of a frame
    that takes one, each other slot that names none of them, nor `thing`, a pack's kind or an object of the model,
    is `unslotted`, a v_t13 naming the slot (b840)."""
    return not any(name == "thing" or _slot(model, e, name, kinds, strict=True)
                   for name in re.findall(r"<([^>]+)>", frame))


def _frames(model, e, kinds, verb, known=frozenset()):
    thin = e.fields.frames
    if not thin:
        if e.element.kind == "relation":
            thin = ("<from> %s <to>" % verb,)
        else:
            service, _, op = e.element.id.rpartition(".")
            thin = ("<actor> %s <%s>" % (verb, model.services[service].operation(op).object or "thing"),)
    out = {}
    for frame in thin:
        texts = [""]
        for piece in re.split(r"(<[^>]+>)", frame):
            slot = SLOT.fullmatch(piece)
            options = _slot(model, e, slot.group(1), kinds) if slot else [piece]
            texts = [t + o for t in texts for o in options]
        for t in texts:
            out.setdefault(" ".join(t.split()), frame)
    slotless = tuple(f for f in e.fields.frames if _slotless(model, e, f, kinds))
    unslotted = tuple((f, name) for f in e.fields.frames if f not in slotless for name in SLOT.findall(f)
                      if name not in known and not _slot(model, e, name, kinds, strict=True))
    return tuple(out), tuple(out.values()), slotless, unslotted


def _verbs(model, found, kinds, known=frozenset()):
    out = []
    for e in found:
        if not e.label.startswith("verb") or not e.element or e.element.kind not in ("relation", "operation"):
            continue
        t = e.fields
        frames, written, slotless, unslotted = _frames(model, e, kinds, spec_frames.s3(t), known)
        out.append(spec_lexicon.Term(term=e.term, category="event", text=e.text, where=e.where, label=e.label,
                                     aspect=t.aspect, forms=t.forms, frames=frames, frame=frames[0], nots=t.nots,
                                     written=written, slotless=slotless, unended=t.unended, unslotted=unslotted,
                                     operation=e.element.id if e.element.kind == "operation" else "",
                                     element=qualified(e.element)))
    return out


def rows(model, kinds):
    """The model's relations as spec_relations rows between kinds."""
    out = []
    for obj in model.objects.values():
        for rel in obj.relations:
            for target in rel.targets:
                o, k = kinds.get(obj.name), kinds.get(target)
                if not o or not k:
                    continue
                where = obj.where.rpartition(":")[0]
                if rel.phrase == "has":
                    out.append(spec_relations.Row(k, "of", o, "one", where))
                elif rel.phrase == "holds":
                    out.append(spec_relations.Row(k, "in", o, "", where))
                elif rel.phrase in PREPOSITIONS:
                    out.append(spec_relations.Row(o, rel.phrase, k, "one" if rel.card.startswith("one") else "",
                                                  where))
    return out


def lexicon(root):
    """The spec_lexicon.Lexicon of a context with a domain model."""
    model, found = domain_model.load(root), spec_vocabulary.entries(root)
    kinds, terms = _kinds(found, model)
    packed = spec_packs.kinds(root)
    kinds.update({n: n for n in model.objects if n in packed and n not in kinds})   # a pack's noun its kind (b688)
    keys = dict(kinds)
    keys.update({name: name for name in model.actors})
    services = ("service",) if "request" in spec_packs.imports(root) else ()
    terms += _actors(model, found, kinds, services) + _attributes(model, found, kinds) + _verbs(
        model, found, keys, {"thing", *packed, *model.objects})     # a slot of a pack's kind or an object reads
    held = {k: k for k in packed}     # a relation to an imported pack's kind a row too (b609)
    held.update(kinds)
    return spec_lexicon.Lexicon(terms, rows(model, held))
