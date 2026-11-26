"""The files the upgrade step "the domain contract" scaffolds (the domain contract design, §9.6), read off a 0.37
context's old lexicon (spec_lexicon over the glossary, `## Terms` and `## Relations`) and its lines: `Scaffold`'s
`model` (`spec/model/<context>.md`), `vocabulary` (the context's layer and `shared.md`) and `contract`
(`spec/adapters/cli.toml`), with what it could not place (`skipped`, `unmapped`) for the report."""
import re
from collections import defaultdict

import spec_frames
import spec_lexicon

RUNS = re.compile(r"\bruns `([^`]+)`")
OPTION = re.compile(r"`(--[A-Za-z0-9][\w-]*)`")
ON = re.compile(r"\bruns `[^`]+`[^,]*?\bon (?:a|an|the|every) ([\w-]+(?: [\w-]+)?)")
OUTCOMES = """[outcomes]
done = { exit = 0 }
returned = { exit = 0, content = "stdout" }
passed = { exit = 0, content = "stdout" }
refused = { exit = 1, errors = "stderr" }
failed = { exit = 1, content = "stdout", errors = "stderr" }
broken = { exit = 1, errors = "stderr" }
"""


def bare(word):
    return word.strip().strip("`")


def sentence(text):
    text = " ".join(text.split()).rstrip(".")
    return text[:1].upper() + text[1:] + "." if text else ""


def key(name):
    return name if re.fullmatch(r"[A-Za-z0-9_-]+", name) else '"%s"' % name


class Scaffold:
    def __init__(self, lexicon, said, area):
        self.lexicon, self.said, self.area = lexicon, said, area
        self.tools = {t.term: bare(t.term) for t in lexicon.of("actor") if t.supertype == "tool"}
        self.agents = [t for t in lexicon.of("actor") if t.supertype != "tool"]
        self.objects = {t.term: t for t in lexicon.terms if t.category in ("kind", "resource")}
        self.requests = []                                  # (file, id, service, operation, parameters, command)
        self.operations = defaultdict(dict)                 # service -> operation -> {parameter: option or None}
        self.outcomes = defaultdict(set)
        self._read_lines()
        self.relations, self.skipped = self._relations()
        self.verbs = self._verbs()

    def _read_lines(self):
        for rel, ident, text in self.said:
            for code in RUNS.findall(text):
                tool, _, rest = code.partition(" ")
                if tool not in self.tools.values():
                    continue
                op = rest.strip() or "run"
                params = self.operations[tool].setdefault(op, {})
                given = []
                for option in OPTION.findall(text):
                    name = option[2:].replace("-", " ")
                    params.setdefault(name, option)
                    given.append(name)
                for noun in ON.findall(text):
                    noun = next((n for n in (noun, noun.split()[0]) if n in self.objects), None)
                    if noun:
                        params.setdefault(noun, None)
                        given.append(noun)
                self.requests.append((rel, ident, tool, op, tuple(dict.fromkeys(given)), code))
                ends = self.outcomes[(tool, op)]
                ends.add("done")
                if re.search(r"\bprints?\b", text):
                    ends.add("returned")
                if re.search(r"\brefuse|\bexits? with an error", text):
                    ends.add("refused")

    def _relations(self):
        """{object: [(phrase, target, card)]} of the rows and the state verbs between objects, and the rows skipped."""
        out, skipped = defaultdict(list), []
        for row in self.lexicon.rows:
            card = "one" if row.cardinality.strip() == "one" else "many"
            owner, phrase, target = ((row.k2, "has", row.k1) if row.word == "of" else
                                     (row.k2, "holds", row.k1) if row.word == "in" else (row.k1, row.word, row.k2))
            if owner in self.objects and target in self.objects:
                out[owner].append((phrase, target, card))
            else:
                skipped.append(row)
        for verb in self.lexicon.of("event"):
            ends = self._ends(verb)
            if verb.aspect == "state" and ends:
                out[ends[0]].append((ends[1], ends[2], "many"))
        return out, skipped

    def _ends(self, verb):
        """(subject object, the words between, object) of a verb's first frame when both ends are objects."""
        words = verb.frame.split()
        for i in range(len(words) - 1, 0, -1):
            subject = " ".join(words[:i])
            if subject not in self.objects:
                continue
            for j in range(i + 1, len(words)):
                if " ".join(words[j:]) in self.objects:
                    return subject, " ".join(words[i:j]), " ".join(words[j:])
        return None

    def _verbs(self):
        """{verb term: (element, frame)} of each verb the scaffold names an element of."""
        out, ops = {}, {op: svc for svc, found in self.operations.items() for op in found}
        for verb in self.lexicon.of("event"):
            ends, s3 = self._ends(verb), spec_frames.s3(verb)
            if verb.aspect == "state" and ends:
                out[verb.term] = ("relation %s.%s" % (ends[0], ends[1]), "<from> %s <to>" % ends[1])
            elif verb.term in ops:
                target = next((w for w in reversed(verb.frame.split()) if w in self.objects), "")
                out[verb.term] = ("operation %s.%s" % (ops[verb.term], verb.term),
                                  "<actor> %s <%s>" % (s3, target) if target else "")
        return out

    def unmapped(self):
        """The verbs and conditions the scaffold names no element of."""
        return [t for t in self.lexicon.terms if t.category in ("event", "condition") and t.term not in self.verbs]

    def model(self, path, root):
        title = re.search(r"^title:\s*(.+)$", (root / "spec/index.md").read_text(), re.MULTILINE)
        blocks = [self._object(name, t) for name, t in self.objects.items()]
        for svc, found in self.operations.items():
            ops = ["  operation %s(%s)  outcomes: %s" % (op, ", ".join(params), " | ".join(
                o for o in ("done", "returned", "refused") if o in self.outcomes[(svc, op)])) for op, params in found.items()]
            blocks.append("\n".join(["service %s" % svc] + ops))
        blocks += ["service %s" % name for name in self.tools.values() if name not in self.operations]
        blocks += ["\n".join("actor %s kind of %s" % (bare(t.term), t.supertype or "agent") for t in self.agents)]
        return ("---\nid: model/%s/%s\narea: %s\nkind: core\nimports: []\n---\n\n# %s\n\n## Purpose\n\nScaffolded by "
                "`migrate upgrade` (0.38.0, the domain contract) from the glossary, the `## Terms` and the `## "
                "Relations` of 0.37: check each object, attribute, relation and operation.\n\n```model\n%s\n```\n"
                % (path, self.area, self.area, title.group(1).strip() if title else self.area,
                   "\n\n".join(b for b in blocks if b)))

    def _object(self, name, term):
        head = "object %s" % name + (" kind of %s" % term.supertype if term.supertype else "")
        attrs, cycles = [], []
        for t in self.lexicon.of("attribute"):
            if name not in t.kinds:
                continue
            values = [bare(v) for v in t.values]
            if values:
                attrs.append("%s: %s" % (t.term, (" < " if t.order else " | ").join(values)))
            else:
                attrs.append("%s (%s)" % (t.term, t.type if t.type in ("number", "time") else "text"))
            if t.transitions:
                cycles.append("  lifecycle %s: %s" % (t.term, "; ".join(
                    "%s → %s" % (bare(a), bare(b)) for a, b, _ in t.transitions)))
        lines = [head] + (["  attributes: " + "; ".join(attrs)] if attrs else []) + cycles
        rels = ["%s → %s (%s)" % r for r in self.relations.get(name, [])]
        return "\n".join(lines + (["  relations: " + "; ".join(rels)] if rels else []))

    def _entry(self, t, element, frame=""):
        fields = [sentence(spec_lexicon.gloss(t.text))]
        fields += ["Forms: %s." % ", ".join(t.forms)] if t.forms else []
        fields += ["Plural: %s." % t.plural] if t.plural else []
        fields += ["Not: %s." % ", ".join(t.nots)] if t.nots else []
        fields += ["This: %s." % t.this] if t.this else []
        fields += ["Frame: %s." % frame] if frame else []
        redefines = re.search(r"Redefines:\s*([^.]+)\.", t.text)
        kept = [p.strip() for p in redefines.group(1).split(",") if p.strip() != "cli"] if redefines else []
        fields += ["Redefines: %s." % ", ".join(kept)] if kept else []
        label = "verb, %s" % t.aspect if t.category == "event" and t.aspect else t.label
        return "- **%s** (%s)%s %s" % (t.term, label, " → %s." % element if element else ":", " ".join(f for f in fields if f))

    def entries(self, own):
        out = []
        for t in self.lexicon.terms:
            if t.category == "actor":
                if t.term in self.tools and own:
                    out.append("- **the %s service** (proper noun) → service %s. %s" % (
                        self.tools[t.term], self.tools[t.term], sentence(spec_lexicon.gloss(t.text))))
                elif t.term not in self.tools and not own:
                    out.append(self._entry(t, "actor %s" % bare(t.term)))
                continue
            if not own:
                continue
            if t.category in ("kind", "resource"):
                out.append(self._entry(t, "object %s" % t.term))
            elif t.category == "attribute":
                out += [self._entry(t, "attribute %s.%s" % (k, t.term)) for k in t.kinds if k in self.objects]
                kinds = dict(t.value_kinds)
                out += ["- **%s** (%s) → value %s.%s %s." % (bare(v), kinds.get(v, "adjective"), k, t.term, bare(v))
                        for k in t.kinds if k in self.objects for v in t.values]
            elif t.category in ("event", "condition"):
                element, frame = self.verbs.get(t.term, ("", ""))
                out.append(self._entry(t, element, frame))
        named = set(self.verbs) | {t.term for t in self.lexicon.of("event")}
        for svc, found in self.operations.items():
            for op in found:
                if own and " " not in op and op not in named:
                    s3 = spec_frames.s3(spec_lexicon.Term(term=op, category="event"))
                    out.append("- **%s** (verb, action) → operation %s.%s. Forms: %s." % (op, svc, op, s3))
                    named.add(op)
        return out

    def vocabulary(self, path, own):
        layer = self.area if own else "shared"
        head = ("---\nid: vocabulary/%s/%s\narea: %s\n---\n\n# The words of %s\n\n" % (path, layer, layer, layer) if own
                else "---\nid: vocabulary/%s/shared\n---\n\n# Shared words\n\n" % path)
        return head + "## Terms\n\n" + "".join(e + "\n" for e in self.entries(own))

    def contract(self):
        out = ['# The CLI adapter\'s contract of this bounded context, scaffolded by `migrate upgrade` (0.38.0) from the',
               "# commands its lines ran: name each tool's program under [programs], its path from the context's root.",
               'adapter = "cli"', 'json = "--json"', "", "[programs]"]
        out += ['# %s = "<the path of its program>"' % name for name in self.tools.values()]
        out += ["", OUTCOMES.rstrip("\n"), "", "[cli-only]", 'options = ["--json"]']
        for svc, found in self.operations.items():
            for op, params in found.items():
                ident = '"%s.%s"' % (svc, op)
                out += ["", "[operations.%s]" % ident, 'command = "%s %s"' % (svc, op) if op != "run" else
                        'command = "%s"' % svc]
                if params:
                    out.append("[operations.%s.parameters]" % ident)
                    positional = 0
                    for name, option in params.items():
                        if option:
                            out.append('%s = { option = "%s" }' % (key(name), option))
                        else:
                            positional += 1
                            out.append("%s = { positional = %d }" % (key(name), positional))
        return "\n".join(out) + "\n"
