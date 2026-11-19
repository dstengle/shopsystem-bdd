"""The domain contract's part of scripts/spec (its design, §5.5 and §8): a part of Model (model_facts).

In a context with a domain model (`spec/model/`): `model_problem(S, Why)` of each of domain_model_check's v_m8, the
vocabulary's problems (spec_vocabulary) as `elementless(T, Why)` (v_t18), `unresolved(T, Why)` (v_t19),
`named_twice(T, Why)` (v_t20) and `retired_import(C, P)` (v_t21), and `foreign_term(Q, W, Why)` (v_m1) of each word a
parsed requirement of a capability with an `area:` uses (a kind, a verb, an attribute or an actor of its logical form)
whose entries are all in vocabulary layers its area does not read; the facts of model_domain_lines of the model and of
each parsed requirement (v_m2-v_m7); `adapter_problem(Code, S, Why)` of adapter_cli_check's v_a1-v_a4,
`contract_op(C, O)` and `op_holds(C, O, Q)` of what each operation of an adapter contract holds (adapter_annotate;
v_a5, v_a6 against `requester`). In any context: `cites_record(I, R)` of each
`record/...` or `.shop/records/` path an item's `source:` names, with `new_item(I)` for an item numbered from
RECORDS_POLICY (the records policy, v_r1; an older item's citation is history, w_r1).
"""
import re

import adapter_annotate
import adapter_cli
import adapter_cli_check
import domain_model
import domain_model_check
import model_domain_lines
import spec_vocabulary
from backlog_items import RECORDS_POLICY
from model_parse import as_list, frontmatter

FACTS = {"v_t18": "elementless", "v_t19": "unresolved", "v_t20": "named_twice"}


def uses(form):
    """(category, word) of each kind, actor, verb and attribute a logical form names."""
    from spec_lf_core import Atom, Box, Form, Ref
    out, todo = set(), [form]
    while todo:
        x = todo.pop()
        if isinstance(x, Ref):
            out.add(("kind", x.kind))
            if x.origin == "constant" and x.value:
                out.add(("actor", x.value))
        elif isinstance(x, Atom):
            if x.pred == "event":
                out.add(("event", x.args[1]))
            elif x.pred == "request":     # a request names its operation's verb (spec_lf_request)
                out.add(("event", x.args[2]))
            elif x.pred == "state":
                out.add(("event", x.args[0]))
            elif x.pred == "attr":
                out.add(("attribute", x.args[1]))
            todo += list(x.args)
        elif isinstance(x, (Box, Form)):
            todo += [getattr(x, f) for f in x.__dataclass_fields__]
        elif isinstance(x, (tuple, list)):
            todo += list(x)
    return out


class DomainReading:
    """The part of Model that reads the domain model, the vocabulary and the records policy."""

    def read_domain(self):
        if not domain_model.exists(self.root):
            return
        for code, subject, why in domain_model_check.problems(domain_model.load(self.root)):
            self.fact("model_problem", subject, why)
        for name, *args in model_domain_lines.model_facts(domain_model.load(self.root)):     # v_m2-v_m7
            self.fact(name, *args)
        for code, term, why in spec_vocabulary.problems(self.root):
            if code == "v_t21":
                self.fact("retired_import", self.context, term)
            else:
                self.fact(FACTS[code], term, why)
        # the CLI contract both ways, when spec/adapters/cli.toml exists (v_a1-v_a4)
        for code, subject, why in adapter_cli_check.problems(self.root, domain_model.load(self.root)):
            self.fact("adapter_problem", code, subject, why)
        for rel in adapter_annotate.contracts(self.root):     # what each operation holds (v_a5, v_a6)
            for ident, held in adapter_annotate.held(adapter_cli.read(self.root)).items():
                self.fact("contract_op", str(rel), ident)
                for q in held:
                    self.fact("op_holds", str(rel), ident, self.requirement_id(q))

    def requirement_id(self, short):
        """`<capability>#r<n>` as the facts name a requirement: its capability's `id:` before `#r<n>`."""
        name, _, n = short.partition("#")
        path = self.root / "spec" / "capabilities" / ("%s.md" % name)
        found = frontmatter(path.read_text())[0].get("id") if path.is_file() else None
        return "%s#%s" % (found or name, n)

    def _layer_of(self):
        if getattr(self, "_layers", None) is None:
            self._layers = {e.where: e.layer for e in spec_vocabulary.entries(self.root)}
        return self._layers

    def domain_line(self, path, ident, text):
        """foreign_term(Q, W, Why) of a parsed requirement of a capability with an `area:` (v_m1), and the facts of
        its requests, refusals and sets against the model (model_domain_lines: v_m2-v_m7)."""
        if not domain_model.exists(self.root):
            return
        import spec_grammar4
        import spec_language
        import spec_lf
        parsed = spec_language.parse(self.root, text)
        if parsed.tree is None:
            return
        vocab = spec_grammar4.load(self.root)[0]
        form = spec_lf.form(vocab, parsed.tree)
        if getattr(self, "_lines", None) is None:
            import spec_lexicon
            self._lines = model_domain_lines.Lines(domain_model.load(self.root), spec_lexicon.read(self.root))
        for name, *args in self._lines.facts(ident, form):
            self.fact(name, *args)
        area = frontmatter(path.read_text())[0].get("area")
        if not area:
            return
        readable, layer_of = set(spec_vocabulary.layers_of(self.root, str(area))), self._layer_of()
        terms = self.lexicon_terms()
        for cat, word in sorted(uses(form)):
            layers = {layer_of.get(t.where) for t in terms if t.category == cat and t.term == word}
            if layers and None not in layers and not layers & readable:
                self.fact("foreign_term", ident, word, "%s is a word of %s, which the area %s does not read" % (
                    word, ", ".join(sorted(layers)), area))

    def lexicon_terms(self):
        if getattr(self, "_terms", None) is None:
            import spec_lexicon
            self._terms = spec_lexicon.read(self.root).terms
        return self._terms

    def read_sources(self):
        """cites_record(I, R) and new_item(I) of the items of `.shop/backlog/` (the records policy)."""
        for path in sorted((self.root / ".shop" / "backlog").glob("b*.md")):
            found = re.fullmatch(r"b([1-9]\d*)", path.stem)
            if not found:
                continue
            data, _ = frontmatter(path.read_text())
            ident = data.get("id") or path.stem
            cited = [s for s in as_list(data.get("source")) if re.match(r"(?:record/|\.shop/records/)", str(s))]
            for ref in cited:
                self.fact("cites_record", ident, str(ref))
            if cited and int(found.group(1)) >= RECORDS_POLICY:
                self.fact("new_item", ident)
