"""The lexicon of a bounded context: the one reader of term entries (design §10.1), each a bullet of `spec/index.md`'s
`## Glossary` or a capability's `## Terms`, `- **status** (attribute of item): Values: `idea`, `shaped`.`, whose
parentheses name its part of speech, read by PARTS into its category, the slot it fills (actor, kind, attribute,
relation, event, resource, condition); plugin 0.31's categories name none (v_t4). Values belong to one attribute of one
kind, declared adjectives or nouns or neither (spec_value_kinds, b257). `ident` names a term in GF (§9.6); `problems`
gives v_t4–v_t10. The gloss is the text after the `:` and before the first field, one sentence (v_t7); `Kind of:`
names the kind a kind or an actor is one of (spec_frames). A relation entry (v_t8) and a `Means:` field (v_t9) are
read only to be problems; relations are spec_relations' rows.
"""
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import spec_frames
import spec_relations
import spec_value_kinds

CATEGORIES = ("actor", "kind", "attribute", "value", "relation", "event", "resource", "condition")
LETTER = {"actor": "a", "kind": "k", "attribute": "t", "value": "v", "relation": "r", "event": "e",
          "resource": "s", "condition": "c"}
# verbs the core grammar spells itself; an event with one of these names would make two trees of one line
CORE_VERBS = {"run", "print", "hold", "exit", "become", "set", "be"}

ENTRY = re.compile(r"^- \*\*(?P<term>.+?)\*\*\s*(?:\((?P<cat>[^)]*)\))?\s*:\s*(?P<text>.*)$", re.DOTALL)
FIELDS = ("Values", "Values (adjective)", "Values (noun)", "Transitions", "Means", "Forms", "Frame", "Plural", "Not", "Kind of", "This", "Redefines", "Schema",
          "Field of", "Order")
ASPECTS = ("state", "action")
NAMES = "|".join(map(re.escape, FIELDS))
FIELD = re.compile(r"(?:^|\s)(?:%s):" % NAMES)
PATTERNS = {f: re.compile(r"(?:^|\s)%s:\s*(.+?)\.(?=\s+(?:%s):|\s*$)" % (re.escape(f), NAMES), re.DOTALL) for f in FIELDS}


@dataclass(frozen=True)
class Term:
    term: str
    category: str
    kinds: tuple = ()
    text: str = ""
    where: str = ""
    values: tuple = ()
    transitions: tuple = ()
    forms: tuple = ()
    plural: str = ""
    nots: tuple = ()
    resource: str = ""
    supertype: str = ""
    frame: str = ""       # its first `Frame:`, the one the codified-1 grammar reads
    label: str = ""       # the text in the entry's parentheses, as written
    aspect: str = ""      # a verb's: state or action (`(verb, state)`), "" when it says neither (v_t14)
    frames: tuple = ()    # a verb's every `Frame:`: one meaning, one predicate
    this: str = ""        # a kind's `This:`, the run's own thing of that kind
    schema: tuple = ()    # an artifact's `Schema:` as (schema type, file), stored, checked by nothing yet (b241)
    field_of: str = ""    # an attribute's `Field of:`, the artifact it is a field of, stored (b241)
    order: str = ""       # an attribute's `Order:`, how its values are ordered (spec_lf_order, b240)
    value_kinds: tuple = ()     # (value, adjective or noun) of each declared value (spec_value_kinds, b257)

    @property
    def key(self):
        return (self.category, self.term, self.kinds)


def _fields(text, name):
    """Every value of the field `name` (one of FIELDS, its pattern compiled once) in an entry's text, in order."""
    return tuple(" ".join(m.group(1).split()) for m in PATTERNS[name].finditer(text))


def _field(text, name):
    return (_fields(text, name) or ("",))[0]


def _list(text):
    return tuple(w.strip() for w in text.split(",") if w.strip())


# The part of speech an entry names, and the grammar slot (category) it fills: the one table of both, which the
# reader and an upgrade's relabelling of plugin 0.31's categories (`relabel`) share.
PARTS = (("proper noun", "actor"), ("noun", "kind"), ("adjective", "condition"), ("attribute", "attribute"),
         ("verb", "event"))
SPEECH = {cat: part for part, cat in PARTS} | {"resource": "noun"}


def relabel(raw):
    """Plugin 0.31's category written as its part of speech: `kind` -> `noun`, `condition of stage` -> `adjective of
    stage`, `resource, exclusive` -> `noun, exclusive`; None when `raw` is no such category (a relation's among
    them, which is no term)."""
    raw = " ".join(raw.split())
    cat, sep, rest = raw.partition(" ")
    if cat.rstrip(",") not in SPEECH or cat == "attribute" and not rest.startswith("of "):
        return None
    return SPEECH[cat.rstrip(",")] + (cat[len(cat.rstrip(",")):] + sep + rest if rest else "")


def _category(raw):
    """The part of speech of an entry as (category, kinds, resource): `noun` -> ("kind", (), ""), `attribute of
    initiative` -> ("attribute", ("initiative",), ""), `noun, exclusive` -> ("resource", (), "exclusive"); a relation
    entry (a problem, v_t8) as a relation; anything else, plugin 0.31's categories among them, as no category ("")."""
    raw = " ".join(raw.split())
    if raw == "artifact":   # one part of speech: "the comment form" a proper noun, "layout" a noun, under artifact
        return "artifact", (), ""
    if raw.startswith("relation"):
        parts = re.split(r"\s*(?:→|->)\s*", raw[len("relation"):].strip())
        return "relation", tuple(p.strip() for p in parts if p.strip()), ""
    for part, cat in PARTS:
        if raw == part or part == "verb" and raw in ("verb, " + a for a in ASPECTS):
            return cat, (), ""
        if raw.startswith(part + " of ") and cat in ("attribute", "condition"):
            return cat, _list(raw[len(part) + 4:]), ""
        if raw.startswith(part + ", ") and part == "noun":
            return "resource", (), raw[len(part) + 2:].strip()
    return "", (), ""


def entry(bullet, where):
    """One term entry, or None when the bullet is not one. A missing category reads as ""."""
    found = ENTRY.match(" ".join(bullet.split()))
    if not found:
        return None
    label = " ".join((found.group("cat") or "").split())
    category, kinds, resource = _category(label)
    text, term = found.group("text").strip(), found.group("term").strip()
    if category == "artifact":
        category = "actor" if term.startswith(("the ", "`")) else "kind"
    schema = re.match(r"(.+?),?\s*`([^`]+)`$", _field(text, "Schema"))
    aspect = label.partition(", ")[2] if category == "event" else ""
    transitions = []
    for row in _field(text, "Transitions").split(";"):
        step = re.match(r"\s*(.+?)\s*(?:→|->)\s*(.+?):\s*(.+?)\s*$", row)
        if step:
            transitions.append(step.groups())
    kinds_of = tuple((v, k) for k in sorted(spec_value_kinds.KINDS, key=lambda k: text.find("Values (%s)" % k))
                     for v in _list(_field(text, "Values (%s)" % k)))     # in the entry's order
    return Term(term=term, category=category, kinds=kinds, text=text, where=where, value_kinds=kinds_of,
                values=_list(_field(text, "Values")) + tuple(v for v, _ in kinds_of), transitions=tuple(transitions),
                forms=_list(_field(text, "Forms")), plural=_field(text, "Plural"), nots=_list(_field(text, "Not")),
                resource=resource, supertype=_field(text, "Kind of") or ("artifact" if label == "artifact" else ""), frame=_field(text, "Frame"), label=label,
                aspect=aspect, frames=_fields(text, "Frame"), this=_field(text, "This"),
                schema=schema.groups() if schema else (), field_of=_field(text, "Field of"),
                order=_field(text, "Order"))


def gloss(text):
    """An entry's text up to its first field."""
    found = FIELD.search(text)
    return (text[:found.start()] if found else text).strip()


def one_sentence(text):
    """design-r2 §8's rule: code spans, quoted strings and e.g., i.e., etc., vs. are blanked; `.!?` before a space or
    the end, and `;`, end a sentence; `:` does not. An empty gloss passes."""
    text = re.sub(r"`[^`]*`|\"[^\"]*\"|“[^”]*”", "x", text)
    text = re.sub(r"\b(?:e\.g|i\.e|etc|vs)\.", "x", text).strip()
    body = text[:-1] if text[-1:] in ".!?" else text
    return ";" not in text and not re.search(r"[.!?](?:\s|$)", body)


def _bullets(text, heading):
    """The bullets of one `## <heading>` section, each with its indented continuation lines joined."""
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip() == heading
            continue
        if not inside:
            continue
        if line.startswith("- "):
            out.append(line)
        elif out and line[:1].isspace() and line.strip():
            out[-1] += " " + line.strip()
    return out


@dataclass
class Lexicon:
    terms: list = field(default_factory=list)
    rows: list = field(default_factory=list)       # spec_relations.Row of the `## Relations` tables

    def of(self, category):
        return [t for t in self.terms if t.category == category]

    def kind_names(self):
        return {t.term for t in self.of("kind")}

    def values(self):
        """Every value as (value, kind, attribute term, attribute entry)."""
        return [(v, k, t.term, t) for t in self.of("attribute") for k in t.kinds for v in t.values]

    def keys(self):
        keys = [t.key for t in self.terms if t.category in LETTER and t.category != "value"]
        return keys + [("value", v, (k, a)) for v, k, a, _ in self.values()]

    def ids(self):
        """A GF identifier for every key; colliding identifiers are numbered in sorted key order."""
        by_base = defaultdict(list)
        for key in set(self.keys()):
            by_base[ident(key[1], key[0])].append(key)
        out = {}
        for base, keys in by_base.items():
            for n, key in enumerate(sorted(keys)):
                out[key] = base if n == 0 else "%s_%d" % (base, n + 1)
        return out

    def words(self):
        """Every spelling a line may use: terms, values, and the forms of events."""
        out = {t.term for t in self.terms if t.category in LETTER}
        out |= {v for v, _, _, _ in self.values()}
        out |= {f for t in self.of("event") for f in t.forms} | {t.plural for t in self.terms if t.plural}
        return out | {r.word for r in self.rows}

    def relations(self):
        """The expanded relation rows (k1, word, k2, rid), the supertype's own included (spec_relations)."""
        return spec_relations.expand(self)

    def definition(self, term):
        """The gloss sentence of a condition (its entry, or by name the first so named), which a `Def` parse reads;
        "" when none."""
        found = [t for t in self.of("condition") if t == term or t.term == term]
        return gloss(found[0].text) if found else ""


def ident(term, category):
    """`work-item`, kind -> k_work_item; `` `work run` ``, actor -> a_work_run."""
    return "%s_%s" % (LETTER[category], re.sub(r"[^a-z0-9]+", "_", term.lower()).strip("_") or "x")


def read(root):
    """The lexicon of the context at `root`: the glossary of `spec/index.md` and every capability's `## Terms`."""
    root = Path(root)
    sources = [(root / "spec" / "index.md", "Glossary")]
    sources += [(p, "Terms") for p in sorted((root / "spec" / "capabilities").glob("*.md"))]
    terms = []
    for path, heading in sources:
        if path.is_file():
            where = path.relative_to(root).as_posix()
            terms += [t for t in (entry(b, where) for b in _bullets(path.read_text(), heading)) if t]
    return Lexicon(terms, spec_relations.read(root))


def _unnamed(t):
    return t.category not in LETTER or t.category == "value"


def _relabelled(t):
    hint = relabel(t.label)
    return "(%s) is written (%s)" % (t.label, hint) if hint else ""


def unlabelled(lexicon):
    """The refusal of a lexicon with a term that names no part of speech (v_t4), each such term named with the
    label it is to carry, or None: the grammars are built from the parts of speech, and such a term fills no slot."""
    found = []
    for t in lexicon.terms:
        if _unnamed(t):
            fix = _relabelled(t) or ("(%s) is no part of speech" % t.label if t.label else "names no part of speech")
            found.append("%s: %s %s" % (t.where, t.term, fix))
    if not found:
        return None
    return ("terms that do not name their part of speech (write each as (noun), (proper noun), (artifact), (verb), "
            "(adjective of <kind>), (attribute of <kind>) or (noun, <resource>)): " + "; ".join(found))


def problems(lexicon, outer=frozenset()):
    """v_t4 (a term has a category, and its kinds are kinds), v_t5 (a value names one attribute of one kind),
    v_t6 (no two terms linearise the same), v_t7 (a gloss of more than one sentence), v_t9 (a `Means:` field),
    spec_relations' v_t4, v_t8 and v_t10, and spec_frames' v_t11, v_t12 and v_t13 (its frames may name `outer`, b199), as (code, term, message) sorted."""
    out = []
    kinds = lexicon.kind_names()
    for t in lexicon.terms:
        if _unnamed(t):
            hint = _relabelled(t)
            out.append(("v_t4", t.term, "%s: the term does not name its part of speech%s" % (
                t.where, "; " + hint if hint else "")))
        elif t.category in ("attribute", "condition", "relation") and not t.kinds:
            out.append(("v_t4", t.term, "%s: the %s names no kind" % (t.where, t.category)))
        elif any(k not in kinds for k in t.kinds):
            missing = ", ".join(k for k in t.kinds if k not in kinds)
            out.append(("v_t4", t.term, "%s: %s is not a kind" % (t.where, missing)))
        elif t.category == "attribute" and (not t.values or spec_value_kinds.mixed(t)):
            out.append(("v_t4", t.term, "%s: the attribute gives %s" % (t.where, spec_value_kinds.mixed(t) or "no Values")))
        if t.category == "event" and t.term in CORE_VERBS:
            out.append(("v_t6", t.term, "%s: the grammar spells `%s` itself" % (t.where, t.term)))
    seen = defaultdict(list)
    for v, k, a, _ in lexicon.values():
        seen[(k, v)].append(a)
    out += [("v_t5", v, "the value %s of %s is in more than one attribute (%s)" % (v, k, ", ".join(a)))
            for (k, v), a in seen.items() if len(a) > 1]
    counts = defaultdict(int)
    for t in lexicon.terms:     # a verb's two entries are two senses (spec_frames' v_t15)
        counts[t.key] += t.category != "event"
    out += [("v_t6", key[1], "the %s %s is given %d times" % (key[0], key[1], n)) for key, n in counts.items()
            if n > 1]
    for t in lexicon.of("actor"):
        words = t.term.split(" ", 1)
        if len(words) == 2 and words[0] in ("a", "an", "the") and words[1] in kinds:
            out.append(("v_t6", t.term, "the actor %s reads as the kind %s" % (t.term, words[1])))
    out += [("v_t7", t.term, "%s: the entry's gloss is more than one sentence" % t.where)
            for t in lexicon.terms if not one_sentence(gloss(t.text))]
    out += [("v_t9", t.term, "%s: the meaning is a Means: field; write one Def sentence, or a gloss" % t.where)
            for t in lexicon.terms if re.search(r"(?:^|\s)Means:", t.text)]
    return sorted(set(out + spec_relations.problems(lexicon, outer) + spec_frames.problems(lexicon, outer)))
