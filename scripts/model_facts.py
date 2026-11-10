"""The facts of scripts/model: Model reads a repository into the facts model.lp solves, with the references that name
nothing and the file problems."""

import datetime
import re
from pathlib import Path

import spec_read
from model_parse import as_list, frontmatter, mention, scenarios
from model_requests import RequestReading
from model_spec import SpecReading
from model_work import FROZEN_KINDS, WorkReading

REF = re.compile(r"^(?P<cap>[\w.-]+(?:/[\w.-]+)*)#r(?P<n>\d+)(?P<old>@0\.29)?$")
KINDS = {"bounded-context", "capability", "design-decision", "requirement", "requirement-group", "scenario", "term",
         "universal-condition", "job-thread", "observation", "measurement", "review-finding", "decision-argument",
         "initiative-archive", "job", "context-seam", "product-vision", "request"} | FROZEN_KINDS
NAME = r"[a-z0-9]+(?:-[a-z0-9]+)*"
CONTEXT_PATH =rf"{NAME}(?:\.{NAME})*/{NAME}/{NAME}"     # <owner>/<product>/<context name>; the owner may be a domain
NOT_PROSE = re.compile(r'`[^`]*`|"[^"]*"|(?<!\w)@[\w-]+')
OLD_LAYOUT = ("spec/decisions.md", "decisions/", "work/", "records/")    # what scripts/migrate moves (r61)


class Model(SpecReading, WorkReading, RequestReading):
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
        self.req_text = {}
        self.sc_text = {}       # scenario id -> its title and steps
        self.retired = set()    # (capability id, n)
        self.words = set()      # each term and avoided word, lowercased
        self.unmentioned = set()    # the codified statements and scenarios: a parsed line uses lexicon words (C27)
        self.groups = {}        # group id -> spec_read.Group
        self.group_of = {}      # requirement id -> its group id
        self.restated = {}      # <cap>#r<n> -> {"text", "line"}, spec/restated.json
        self.restated_by = {}   # <cap>#r<n>@0.29 -> [group ids that restate it]
        self._grammar = None

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
            self.foreign(ref)
            return ref      # another context's full id, or malformed: want() or resolve_req() reports it
        if kind and re.fullmatch(NAME, ref):
            return f"{kind}/{self.path}/{ref}"
        return ref

    def foreign(self, ref):
        """r117: a request id with another context's path is a `foreign` fact (the frozen kinds are history: D5)."""
        head, _, rest = ref.partition("/")
        if head == "request" and re.fullmatch(rf"{CONTEXT_PATH}/{NAME}", rest) and not rest.startswith(self.path + "/"):
            self.fact("foreign", ref)

    def check_id(self, ident, kind, where):
        """A node's id is <kind>/<context path>/<name>, with its own kind."""
        if self.path:
            self.foreign(str(ident))
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
        q = f"{cap}#r{m.group('n')}"
        if not m.group("old"):
            return q
        q += "@0.29"     # a 0.29 id is history (§13.4): `why` reads it in spec/restated.json, which lacks those retired before
        self.nodes.setdefault(q, "0.29 id")       # looked up, never a node: no fact is written for it
        self.fact("old_ref", q)
        return q

    def term(self, word, n, avoided):
        """A glossary entry: the term node term/<path>/<word, spaces as hyphens>, its entry number and its Not: words."""
        word = " ".join(word.lower().split())
        t = self.term_id(word)
        self.check_id(t, "term", "spec/index.md")
        self.node(t, "term")
        self.fact("term_of", t, self.context)
        self.fact("glossary_entry", t, n, word)
        self.words.add(word)
        for w in avoided:
            self.fact("avoid", t, w)
            self.words.add(w)
        return t

    def term_id(self, word):
        """A term's id: its words joined by "-", what no id may hold (the `@` of a tag, an apostrophe) left out."""
        return f"term/{self.path}/{'-'.join(re.sub(r'[^a-z0-9 -]', '', word.lower()).split())}"

    def read(self):
        self.read_layout()
        self.read_index()
        self.read_restated()
        self.read_universal()
        self.read_capabilities()
        self.read_features()
        self.read_decisions()
        self.read_records()
        self.read_work()
        self.read_requests()
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
        data, _ = frontmatter(path.read_text())
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
        if spec_read.codified(path):
            self.read_lexicon()         # the typed glossary (§10.1)
        else:
            self.fact("uncodified", "spec/index.md")    # v_p0: run `migrate upgrade`

    def read_mentions(self):
        """mentions(X, W) for each requirement and scenario X and each term or avoided word W it contains."""
        found = [(w, mention(w)) for w in sorted(self.words)]
        for x, text in list(self.req_text.items()) + list(self.sc_text.items()):
            if x in self.unmentioned:
                continue
            text = NOT_PROSE.sub(" ", text)        # code spans, double-quoted strings and @ tags are no mentions (r51)
            for w, pattern in found:
                if pattern.search(text):
                    self.fact("mentions", x, w)

    def read_capabilities(self):
        for path in sorted((self.root / "spec" / "capabilities").glob("*.md")):
            data, body = frontmatter(path.read_text())
            name = path.stem
            codified = spec_read.codified(path)      # read as groups (§13.4); else v_p0
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
            self.unread(data, path)
            if "formulated_as" in data:
                self.problems.append(f"{self.rel(path)}: formulated_as is not read; the feature file is "
                                     f"features/{name}.feature")
            if not any(l.startswith("## ") and l[3:].strip().lower() == "behaviour" for l in body.splitlines()):
                self.problems.append(f"{self.rel(path)}: no '## Behaviour' section")
            entry = {"name": name, "reqs": {}, "group": data.get("group"), "path": path,
                     "feature": f"features/{name}.feature", "codified": False}
            if codified:
                self.read_codified(cap, path, entry)
            else:
                self.fact("uncodified", self.rel(path))
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
                self.node(s, "scenario")
                self.sc_text[s] = "\n".join([title] + steps)
                if cap is not None and self.caps[cap]["codified"]:
                    self.codified_scenario(cap, key, title, tags, s)

    def want(self, ident, kind, where):
        self._wanted = getattr(self, "_wanted", [])
        self._wanted.append((ident, kind, where))

    def frozen_request(self, ident):
        """Whether `ident` is a request of this context kept only in the frozen .shop/work/requests/."""
        head, _, rest = str(ident).partition("/")
        if head != "request" or not self.path or not rest.startswith(self.path + "/") or ident in self.nodes:
            return False
        return (self.root / ".shop" / "work" / "requests" / (rest.rsplit("/", 1)[-1] + ".md")).is_file()

    def check_refs(self):
        for ident, kind, where in getattr(self, "_wanted", []):
            if str(ident).partition("/")[0] in FROZEN_KINDS:
                continue        # a reference into the frozen .shop/work/ is history, never resolved (D5)
            if self.frozen_request(ident):
                continue        # a request of the frozen queue is history too (D7): its file is still there
            if str(ident).endswith("@0.29") and kind is None:
                self.resolve_req(ident, where)      # a 0.29 id is history, looked up by its form alone
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
