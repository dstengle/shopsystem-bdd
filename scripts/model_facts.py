"""The facts of scripts/model: Model reads a repository into the facts model.lp solves, with the references that name
nothing and the file problems."""

import datetime
import re
from pathlib import Path

from model_parse import (
    RID,
    as_list,
    behaviour_items,
    bullets,
    ears,
    frontmatter,
    glossary_entry,
    mention,
    scenarios,
    section,
)
from model_work import WorkReading

REF = re.compile(r"^(?P<cap>[\w.-]+(?:/[\w.-]+)*)#r(?P<n>\d+)$")
KINDS = {"bounded-context", "capability", "design-decision", "acceptance-scenario", "term", "initiative",
         "capability-proposal", "job-proposal", "map-proposal", "vision-proposal", "job-thread",
         "cross-context-request", "map-escalation", "work-item", "observation", "measurement", "review-finding",
         "decision-argument", "initiative-archive", "job", "context-seam", "product-vision"}
NAME = r"[a-z0-9]+(?:-[a-z0-9]+)*"
CONTEXT_PATH = rf"{NAME}(?:\.{NAME})*/{NAME}/{NAME}"     # <owner>/<product>/<context name>; the owner may be a domain
NOT_PROSE = re.compile(r'`[^`]*`|"[^"]*"|(?<!\w)@[\w-]+')
OLD_LAYOUT = ("spec/decisions.md", "decisions/", "work/", "records/")    # what scripts/migrate moves (r61)


class Model(WorkReading):
    def __init__(self, root, today=None):
        self.root = Path(root)
        self.today = today or datetime.date.today()
        self.facts = []
        self.nodes = {}
        self.dangling = []
        self.problems = []
        self.context = None     # bounded-context/<path>
        self.path = None        # <owner>/<product>/<context name>
        self.caps = {}          # capability id -> {"name", "reqs": {n: node id}, "group"}
        self.proposals = {}     # part id -> frontmatter
        self.parents = {}       # part id -> part_of
        self.sources = {}       # initiative id -> [record ids]
        self.req_text = {}
        self.sc_text = {}       # acceptance-scenario id -> its title and steps
        self.retired = set()    # (capability id, n)
        self.words = set()      # each term and avoided word, lowercased

    def fact(self, name, *args):
        self.facts.append((name, args))

    def node(self, ident, kind):
        if ident in self.nodes and self.nodes[ident] != kind:
            self.problems.append(f"{ident} is both a {self.nodes[ident]} and a {kind}")
        self.nodes[ident] = kind
        self.fact("node", ident, kind)

    def rel(self, path):
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)

    def qualify(self, ref, kind=None):
        """<kind>/<path>/<name> as is; <kind>/<name> in this context; <name> where the field fixes the kind."""
        ref = str(ref).strip()
        if not self.path:
            return ref
        head, slash, rest = ref.partition("/")
        if slash and head in KINDS:
            if rest.startswith(self.path + "/") or (head == "bounded-context" and rest == self.path):
                return ref
            if re.fullmatch(NAME, rest):
                return f"{head}/{self.path}/{rest}"
            return ref      # another context's full id, or malformed: want() or resolve_req() reports it
        if kind and re.fullmatch(NAME, ref):
            return f"{kind}/{self.path}/{ref}"
        return ref

    def check_id(self, ident, kind, where):
        """A node's id is <kind>/<context path>/<name>, with its own kind."""
        prefix = f"{kind}/{self.path}/"
        if self.path and not (str(ident).startswith(prefix) and re.fullmatch(NAME, str(ident)[len(prefix):])):
            self.problems.append(f"{where}: id {ident!r} is not {prefix}<name>")

    def resolve_req(self, ref, where):
        m = REF.match(str(ref).strip())
        cap = self.qualify(m.group("cap"), "capability") if m else None
        if not m or (self.path and not re.fullmatch(rf"capability/{re.escape(self.path)}/{NAME}", cap)):
            self.dangling.append(f"{where}: {ref!r} is not a requirement reference "
                                 "(<capability>#r<n>, or #r<a>-r<b> with a <= b, the capability written "
                                 "capability/<context path>/<name>, capability/<name> or <name>)")
            return None
        return f"{cap}#r{m.group('n')}"

    def read(self):
        self.read_layout()
        self.read_index()
        self.read_capabilities()
        self.read_features()
        self.read_decisions()
        self.read_records()
        self.read_work()
        self.check_refs()
        self.read_mentions()
        return self

    def read_layout(self):
        """Each path of the old layout under the root is a file problem (r61)."""
        for old in OLD_LAYOUT:
            path = self.root / old
            if path.is_dir() if old.endswith("/") else path.is_file():
                self.problems.append(f"{old}: the layout has no {old}; run scripts/migrate")

    def read_index(self):
        path = self.root / "spec" / "index.md"
        if not path.exists():
            self.problems.append("spec/index.md is missing: no bounded-context is named")
            return
        data, body = frontmatter(path.read_text())
        ident = data.get("id")
        if not ident:
            self.problems.append("spec/index.md has no frontmatter id naming the bounded-context")
            return
        m = re.fullmatch(rf"bounded-context/({CONTEXT_PATH})", str(ident))
        if not m:
            self.problems.append(f"spec/index.md: id {ident!r} is not bounded-context/<owner>/<product>/<context name>")
            return
        self.context, self.path = m.group(0), m.group(1)
        self.node(self.context, "bounded-context")
        self.read_glossary(body)

    def read_glossary(self, body):
        for n, bullet in enumerate(bullets(section(body, "Glossary")), 1):
            entry = glossary_entry(bullet)
            if entry is None:
                self.problems.append(f"spec/index.md: glossary bullet {n} is not "
                                     "'- **<term>**: <definition>. Not: <word>, <word>.' (Not: optional)")
                continue
            word, avoided = entry
            t = f"term/{self.path}/{'-'.join(word.lower().split())}"
            self.check_id(t, "term", "spec/index.md")
            self.node(t, "term")
            self.fact("term_of", t, self.context)
            self.fact("glossary_entry", t, n, " ".join(word.lower().split()))
            self.words.add(" ".join(word.lower().split()))
            for w in avoided:
                self.fact("avoid", t, w)
                self.words.add(w)

    def read_mentions(self):
        """mentions(X, W) for each requirement and scenario X and each term or avoided word W it contains."""
        found = [(w, mention(w)) for w in sorted(self.words)]
        for x, text in list(self.req_text.items()) + list(self.sc_text.items()):
            text = NOT_PROSE.sub(" ", text)        # code spans, double-quoted strings and @ tags are no mentions (r51)
            for w, pattern in found:
                if pattern.search(text):
                    self.fact("mentions", x, w)

    def read_capabilities(self):
        for path in sorted((self.root / "spec" / "capabilities").glob("*.md")):
            data, body = frontmatter(path.read_text())
            name = path.stem
            expected = f"capability/{self.path}/{name}" if self.path else None
            cap = data.get("id") or expected or name
            if expected and cap != expected:
                self.problems.append(f"{self.rel(path)}: id {cap!r} is not {expected!r}")
            elif expected:
                self.check_id(cap, "capability", self.rel(path))     # the file name must be a <name>
            self.node(cap, "capability")
            if self.context:
                self.fact("in", cap, self.context)
            if data.get("narrator"):
                self.fact("narrator", cap, data["narrator"])
            if data.get("group"):
                self.fact("group", cap, data["group"])
            for d in as_list(data.get("rests_on")):
                d = self.qualify(d, "design-decision")
                self.fact("rests_on", cap, d)
                self.want(d, "design-decision", self.rel(path))
            retired = set()
            for r in as_list(data.get("retired")):
                m = re.fullmatch(r"r?(\d+)", str(r))
                if m:
                    retired.add(int(m.group(1)))
                    self.retired.add((cap, int(m.group(1))))
                    self.fact("retired_id", cap, int(m.group(1)))
                else:
                    self.problems.append(f"{self.rel(path)}: retired {r!r} is not r<n>")
            self.unread(data, path)
            if "formulated_as" in data:
                self.problems.append(f"{self.rel(path)}: formulated_as is not read; the feature file is "
                                     f"features/{name}.feature")
            if not any(l.startswith("## ") and l[3:].strip().lower() == "behaviour" for l in body.splitlines()):
                self.problems.append(f"{self.rel(path)}: no '## Behaviour' section")
            entry = {"name": name, "reqs": {}, "group": data.get("group"), "path": path,
                     "feature": f"features/{name}.feature"}
            for i, (text, lead) in enumerate(behaviour_items(section(body, "Behaviour")), 1):
                m = RID.match(text)
                if m:
                    n = int(m.group(1))
                    q = f"{cap}#r{n}"
                    if n in entry["reqs"]:
                        q = f"{cap}#r{n}~{i}"   # a second bullet with the same id: its own node, so v15b sees both
                    self.fact("req_id", q, cap, n)
                    entry["reqs"].setdefault(n, q)
                    self.req_text[q] = text[m.end():]
                else:
                    q = f"{cap}#line{i}"
                    self.req_text[q] = text
                self.node(q, "capability-requirement")
                self.fact("has_req", cap, q)
                shaped, single = ears(lead if lead is not None else text)
                if not shaped:
                    self.fact("ears_other", q)
                if not single:
                    self.fact("ears_many", q)
            self.caps[cap] = entry

    def read_features(self):
        by_feature = {}
        for cap, entry in self.caps.items():
            by_feature[str(Path(entry["feature"]))] = cap
        for path in sorted((self.root / "features").rglob("*.feature")):
            key = self.rel(path)
            cap = by_feature.get(key)
            if cap is None:
                self.problems.append(f"{key}: not features/<name>.feature for a capability <name>")
            seen = set()
            for title, tags, steps in scenarios(path.read_text()):
                if "@holding" in tags:
                    self.problems.append(f"{key}: scenario {title!r} is tagged @holding; the tag is @deprecated")
                if "@deprecated" in tags:
                    continue        # a deprecated scenario formulates no line (design-decision/held-scenario-formulates-no-requirement)
                s = f"{key}:{title}"
                if s in seen:
                    self.problems.append(f"{key}: two scenarios are titled {title!r}")
                seen.add(s)
                self.node(s, "acceptance-scenario")
                self.sc_text[s] = "\n".join([title] + steps)
                for tag in tags:
                    m = re.fullmatch(r"@r(\d+)", tag)
                    if not m or cap is None:
                        continue
                    q = f"{cap}#r{m.group(1)}"
                    if q in self.nodes:
                        self.fact("has_sc", q, s)
                    else:
                        self.dangling.append(f"{key}: scenario {title!r} names {q}, which {cap} does not have")


    def want(self, ident, kind, where):
        self._wanted = getattr(self, "_wanted", [])
        self._wanted.append((ident, kind, where))

    def check_refs(self):
        for ident, kind, where in getattr(self, "_wanted", []):
            if kind is None and ident not in self.nodes:
                self.dangling.append(f"{where}: {ident} names nothing in this repository")
            elif kind is not None and self.nodes.get(ident) != kind:
                self.dangling.append(f"{where}: {ident} is not a {kind} in this repository")

    def unread(self, data, path):
        for key in data.get("__unread__", []):
            self.problems.append(f"{self.rel(path)}: {key} uses a folded or literal block, which is not read; write it on one line")

    def asp(self):
        def term(a):
            if isinstance(a, int):
                return str(a)
            return '"' + str(a).replace("\\", "\\\\").replace('"', '\\"') + '"'
        return "\n".join(f"{n}({', '.join(term(a) for a in args)})." for n, args in self.facts)
