"""The catalogues as specification artifacts (b370): a part of Model (model_facts) that reads the rule catalogue
(`grammar/rules.md`) and the construct catalogue (`grammar/constructs.md`) a context keeps, one `## <code>` heading an
entry, each entry named `<catalogue>#<code>`.

Facts: `node(E, "catalogue-entry")`, `purpose(E)` of an entry with a `- Purpose:` line, `entry_item(E, I)` of each
item its `- Since:` and `- Changed:` lines name (`b<n>`, an item of the context the catalogue's header names, else of
this one), `item_status(I, S)` of each item of `.shop/backlog/`, `rule_catalogue(P)` and `catalogued_rule(C)` of the
rule catalogue's codes, and `cites_rule(Q, C)` of each rule code a live requirement names in backticks or quotes:
model.lp's v_c1 (a requirement names a rule the rule catalogue has no entry of), v_c2 (an entry with no purpose), v_c3
(an entry that mentions no item) and v_c4 (an entry that mentions an item that is not delivered). A context that keeps
no catalogue has no fact of it."""
import re

from model_parse import frontmatter

CATALOGUES = ("grammar/rules.md", "grammar/constructs.md")
RULES = CATALOGUES[0]
CODE = re.compile(r"v\d+[a-z]?|v_[a-z]\w*|w_[a-z]\w*")      # a rule's code, as model.lp's labels give them
CITED = re.compile(r"`([^`]+)`|\"([^\"]+)\"")
HEADING = re.compile(r"^## (\S+)[ \t]*$", re.MULTILINE)
OWNER = re.compile(r"name items of `([^`]+)`")
ITEMS = re.compile(r"^- (?:Since|Changed): (.*)$", re.MULTILINE)


def entries(text):
    """[(code, the entry's text)] of a catalogue, in its order."""
    found = list(HEADING.finditer(text))
    return [(m.group(1), text[m.end():found[i + 1].start() if i + 1 < len(found) else len(text)])
            for i, m in enumerate(found)]


def items(body):
    """The item numbers an entry's Since: and Changed: lines name, in order."""
    return [int(n) for line in ITEMS.findall(body) for n in re.findall(r"\bb([1-9]\d*)\b", line)]


def cited(text):
    """The rule codes a line names in backticks or quotes, each once."""
    return list(dict.fromkeys(c for pair in CITED.findall(text) for c in pair if c and CODE.fullmatch(c)))


class CatalogueReading:
    """The part of Model that reads the catalogues and the items their entries mention."""

    def read_catalogues(self):
        kept = [rel for rel in CATALOGUES if (self.root / rel).is_file()]
        if not kept:
            return
        for path in sorted((self.root / ".shop" / "backlog").glob("b*.md")):
            data, _ = frontmatter(path.read_text())
            if data.get("id") and data.get("status"):
                self.fact("item_status", str(data["id"]), str(data["status"]))
        for rel in kept:
            text = (self.root / rel).read_text()
            owner = OWNER.search(text.split("\n## ", 1)[0])
            owner = owner.group(1) if owner else self.path
            if rel == RULES:
                self.fact("rule_catalogue", rel)
            for code, body in entries(text):
                ident = "%s#%s" % (rel, code)
                self.node(ident, "catalogue-entry")
                if rel == RULES:
                    self.fact("catalogued_rule", code)
                if re.search(r"^- Purpose: \S", body, re.MULTILINE):
                    self.fact("purpose", ident)
                for n in dict.fromkeys(items(body)):
                    self.fact("entry_item", ident, "item/%s/b%d" % (owner, n))
        if RULES in kept:
            for qid, text in sorted(self.req_text.items()):
                for code in cited(text):
                    self.fact("cites_rule", qid, code)
