"""The fixed step vocabulary (design §14.1, §14.3): the generated `StepsTyped` module over `grammar/Steps.gf`, a step
parsed and read back into its template, kind, term and arguments, and the (template, kind) patterns. The handlers
those keys find are registered in tests/scenarios/vocab.py.

`StepsTyped` gives each kind its instance mention (`<kind>_Inst`, "the initiative i1") and Given templates
(`<kind>_Given` "a stage s1", `<attribute>_Given` "an initiative i1 that is `started`", `<relation>_Given`,
`<kind>_HoldsText`/`_HoldsBlock` "the file `x` holds:"). A step's keyword picks between texts that are both a Given
and a Then, or a When and a Then.
"""
import hashlib
import re
from collections import namedtuple
from itertools import islice
from pathlib import Path

import spec_grammar
import spec_lexicon
import spec_tree
import spec_typed
import spec_typed_verbs
from features_vocab_gf import attributes, modules, verb_rows

GRAMMAR = "StepsTyped"
NAME = re.compile(r"^(?:[a-z][a-z-]*[1-9]\d*|`[^`\s]+`)$")
HOLE_N, HOLE_X, META = "\x01", "\x02", object()
_loaded, _by_print = {}, {}
ALLOWED = {"given": ("SAtom", "SFeat", "_Given", "_HoldsText", "_HoldsBlock"), "when": ("STrig",),
           "then": ("SAtom", "SDoes", "SDoesNot", "SDoesTo", "SDoesI", "SDoesINot", "SPrints", "SPrintsNot", "SExitsOk", "SExitsErr",
                    "SChangesNothing")}
THEN = {"SDoes": "ThenDoes", "SDoesNot": "ThenDoesNot", "SDoesTo": "ThenDoesTo", "SDoesI": "ThenDoes",
        "SDoesINot": "ThenDoesNot", "SPrints": "ThenPrints",
        "SPrintsNot": "ThenPrintsNot", "SExitsOk": "ThenExitsOk", "SExitsErr": "ThenExitsErr",
        "SChangesNothing": "ThenChangesNothing"}
TRIG = {"Runs": "WhenRuns", "RunsOn": "WhenRuns", "IsRun": "WhenRuns", "Happens": "WhenHappens",
        "HappensI": "WhenHappens", "_Becomes": "WhenBecomes"}
BY_EVENT = {"WhenHappens", "ThenDoes", "ThenDoesNot", "ThenDoesTo", "GivenDoes", "GivenDoesNot"}
VERB_ATOMS = ("Does", "DoesNot")     # a condition of a verb, "the session s1 does not write the file f1"
BY_KIND = {"ThenK_A", "ThenK_C", "ThenHolds", "ThenFree"}


class StepError(Exception):
    """A step that does not parse in the Steps grammar, or reads as more than one step."""


class Vocab:
    """A context's compiled step grammar, with what each lexicon id names: (category, term, kind, attribute)."""

    def __init__(self, root, gram, lex):
        self.root, self.gram, self.lex = Path(root), gram, lex
        self.concr = gram.languages[GRAMMAR + "Eng"]
        self.ids, self.words, self.owner = lex.ids(), lex.words(), {}
        for (cat, term, kinds), ident in self.ids.items():
            if cat == "value":
                self.owner[ident] = ("value", term, kinds[0], kinds[1])
            elif cat in ("actor", "event", "resource", "kind"):
                self.owner[ident] = (cat, term, term if cat == "kind" else None, None)
            elif cat == "condition":
                for k in kinds:
                    self.owner["%s_%s" % (ident, self.ids[("kind", k, ())]) if len(kinds) > 1 else ident] = (
                        cat, term, k, None)
        for t, kind, tid in attributes(lex, self.ids):
            self.owner[tid] = ("attribute", t.term, kind, t.term)
        self.kind_id = {t.term: self.ids[t.key] for t in lex.of("kind")}
        self.frames = spec_typed_verbs.frames(lex)
        self.relations = {}
        for k1, word, k2, _ in lex.relations():
            if k1 in self.kind_id and k2 in self.kind_id:
                fun = spec_typed.relation_fun(self.kind_id[k1], word, self.kind_id[k2])
                self.owner[fun] = ("relation", word, k1, None)
                self.relations[fun] = (k1, k2)

    def of(self, fun):
        """(info, suffix) of a fun named after a lexicon id (`t_status_3_Is` -> its attribute, "_Is")."""
        for i in range(len(fun), 0, -1):
            if (i == len(fun) or fun[i] == "_") and fun[:i] in self.owner:
                return self.owner[fun[:i]], fun[i:]
        return None, fun

    def text(self, tree):
        """A tree or subtree written out, as it reads in a step; META is a hole ("?")."""
        import pgf

        def expr(t):
            return pgf.readExpr("?") if t is META else pgf.Expr(t[0], [expr(a) for a in t[1:]]) if isinstance(
                t, tuple) else spec_grammar._expr(t)
        return spec_typed_verbs.unframed(tree, self.frames, self.text) or detokenise(
            self.concr.linearize(expr(spec_typed_verbs.typed(tree, self.frames, META))))


def load(root):
    """The context's step vocabulary, read once per state of the spec and grammar files (`_by_print`), its grammar
    compiled and loaded once per set of sources (`_loaded`)."""
    import pgf
    key = _fingerprint(root)
    if key in _by_print:
        return _by_print[key]
    lex = spec_lexicon.read(root)
    srcs = spec_grammar.sources(root, lex)
    srcs.update(modules(lex))
    sha = hashlib.sha256(("steps\0%s" % sorted(srcs.items())).encode()).hexdigest()[:32]
    if sha not in _loaded:
        target = spec_grammar._cache() / sha / (GRAMMAR + ".pgf")
        if not target.is_file():
            spec_grammar._compile(srcs, sha, GRAMMAR)
        _loaded[sha] = pgf.readPGF(str(target))
    _by_print[key] = Vocab(root, _loaded[sha], lex)
    return _by_print[key]


def _fingerprint(root):
    """The state of a context's files: its resolved root, then (path, mtime, size) of every file under `spec/` and of
    every grammar source."""
    root = Path(root).resolve()
    files = [(p, p.relative_to(root)) for p in sorted((root / "spec").rglob("*")) if p.is_file()]
    files += [(p, p.name) for p in sorted(spec_grammar.GRAMMARS.glob("*.gf"))]
    out = [str(root)]
    for path, name in files:
        st = path.stat()
        out.append((str(name), st.st_mtime_ns, st.st_size))
    return tuple(out)


def detokenise(text):
    text = " ".join(text.split()).replace(spec_typed.PLACEHOLDER, " ")
    for mark in ",.;:":
        text = text.replace(" " + mark, mark)
    return text


def _guard(vocab, tree):
    if tree[0] == "SFeat" and tree[1][0] == "FeatAtom":
        return "a feature that is an atom is the atom's step"
    for node in spec_tree.nodes(tree):
        if node[0].endswith("_Named"):
            return "a named code is no instance"
        if node[0] == "NameLit" and (not NAME.match(node[1]) or node[1] in vocab.words):
            return "%s is no instance name" % node[1]
    return spec_tree.guard(tree, vocab.words)


def parse(vocab, keyword, text):
    """The one tree of a step under its keyword (given, when, then); StepError otherwise."""
    import pgf
    tokens = spec_typed.tokens(text.strip())
    try:
        found = vocab.concr.parse(" ".join(t.replace(" ", spec_typed.PLACEHOLDER) for t in tokens))
        trees = [spec_typed_verbs.normal(spec_grammar._tree(e, vocab.gram))
                 for _, e in islice(found, spec_grammar.LIMIT)]
    except pgf.ParseError as err:
        at = len(tokens) if err.incomplete else spec_grammar._position(tokens, err.offset)
        where = "(it ends too soon)" if at >= len(tokens) else "at %s (token %d)" % (tokens[at], at + 1)
        raise StepError("%r does not parse in Steps %s" % (text, where))
    kept = {t: None for t in trees if t[0].endswith(ALLOWED[keyword]) and not _guard(vocab, t)
            and not (keyword == "then" and t[0] == "SAtom" and t[1][0] in VERB_ATOMS)}     # a verb's Then is SDoes
    if len(kept) != 1:
        raise StepError("%r does not parse as one %s step (%d trees)" % (text, keyword, len(kept)))
    return next(iter(kept))


class Call:
    """A step read back: its template, the kind and attribute it is typed by, the term its handler is keyed by, and
    its arguments (names, values, subject, command, event, resource, noun phrases, quoted texts, and a docstring or
    data table). `fixtures(name)` gives the scenario's pytest fixtures when it runs, so a handler reads `step.repo`,
    `step.context`, `step.run` and `step.request`."""

    def __init__(self, keyword, template, text, tree):
        self.keyword, self.template, self.text, self.tree = keyword, template, text, tree
        self.kind = self.attribute = self.term = self.subject = self.command = self.event = self.resource = None
        self.docstring = self.datatable = self.fixtures = None
        self.names, self.values, self.nps, self.quoted = [], [], [], []

    def __repr__(self):
        return "Call(%s)" % ", ".join("%s=%r" % kv for kv in self.__dict__.items() if kv[0] != "tree")

    def __getattr__(self, name):
        if name in ("repo", "context", "run", "request") and self.fixtures is not None:
            return self.fixtures(name)
        raise AttributeError(name)


def _template(vocab, keyword, tree):
    fun = tree[0]
    info, suffix = vocab.of(fun)
    if suffix == "_Given":
        return {"attribute": "GivenK_A", "kind": "GivenK", "relation": "GivenR"}[info[0]], info
    if suffix in ("_HoldsText", "_HoldsBlock"):
        return ("GivenCode" if suffix == "_HoldsText" else "GivenCodeText"), info
    if fun == "SFeat":
        return "GivenFeat", None
    if fun == "SAtom":
        atom = tree[1][0]
        if atom in VERB_ATOMS:     # a verb between two kinds (b85)
            return "Given" + atom, None
        if atom in ("Holds", "HoldsA", "IsFree"):
            return keyword.capitalize() + ("Free" if atom == "IsFree" else "Holds"), None
        i_info, _ = vocab.of(atom)
        cat = i_info[0] if i_info else None
        return keyword.capitalize() + {"attribute": "K_A", "relation": "R"}.get(cat, "K_C"), i_info
    if fun == "STrig":
        i_info, i_suffix = vocab.of(tree[1][0])
        return TRIG.get(tree[1][0]) or TRIG.get(i_suffix, "WhenK"), i_info
    return THEN[fun], None


def step(vocab, keyword, text):
    """A step's Call: parsed under its keyword and read back."""
    tree = parse(vocab, keyword, text)
    template, info = _template(vocab, keyword, tree)
    call = Call(keyword, template, text, tree)
    for node in spec_tree.nodes(tree):
        n_info, suffix = vocab.of(node[0])
        if node[0] in ("NameLit", "QuotedLit"):
            (call.names if node[0] == "NameLit" else call.quoted).append(node[1])
        elif n_info and n_info[0] == "value":
            call.values.append(n_info[1])
            call.attribute = call.attribute or n_info[3]
        elif n_info and n_info[0] in ("kind", "attribute", "relation") and call.kind is None:
            call.kind = n_info[2]
        elif n_info and n_info[0] in ("event", "resource") and not suffix:
            setattr(call, n_info[0], getattr(call, n_info[0]) or n_info[1])
        elif node[0] in ("ActorSubj", "NPSubj") and call.subject is None:
            call.subject = vocab.text(node)
        elif node[0] in ("CmdCode", "CmdActor") and call.command is None:
            call.command = vocab.text(node)
        elif node[0] in ("OneNP", "MoreNP"):
            call.nps.append(vocab.text(node[1]))
    for i in {"SDoes": (3,), "SDoesNot": (3,), "SDoesTo": (3, 4), "SExitsErr": (2,)}.get(tree[0], ()):
        call.nps.append(vocab.text(tree[i]))
    if template in ("GivenDoes", "GivenDoesNot"):
        call.nps.append(vocab.text(tree[1][3]))
    if info and info[0] == "attribute":
        call.attribute = info[3]
    t = template
    call.term = (info[1] if t in ("GivenR", "ThenR") else call.command if t == "WhenRuns" else call.event if t in BY_EVENT
                 else text.split(" is given")[0] if t == "GivenFeat"
                 else call.subject if t.startswith("Then") and t not in BY_KIND else call.kind)
    return call


# One entry of the vocabulary: a (template, kind) pattern, the fun that gives it, and its regex.
Row = namedtuple("Row", "keyword template kind attribute fun pattern regex")


def _row(vocab, keyword, template, kind, attribute, tree):
    text, pattern, regex, counts = vocab.text(tree), [], [], {"n": 0, "x": 0}
    for token in re.split(r"(\x01|\x02|\?)", text):
        if token in (HOLE_N, HOLE_X, "?"):
            hole = "n" if token == HOLE_N else "x"
            counts[hole] += 1
            pattern.append("{%s%d}" % (hole, counts[hole]))
            regex.append(r"\S+" if hole == "n" else ".+?")
        else:
            pattern.append(token)
            regex.append(re.escape(token))
    return Row(keyword, template, kind, attribute, tree[0], "".join(pattern), "".join(regex))


def rows(vocab):
    """The vocabulary: one Row for each (keyword, template, kind[, attribute]) pattern of the context."""
    N, NP, M = ("NameLit", HOLE_N), ("CodeNP", ("CodeLit", HOLE_X)), META
    out = [("given", "GivenFeat", None, None, ("SFeat", M)),
           ("when", "WhenRuns", None, None, ("STrig", ("Runs", M, M))),
           ("when", "WhenRuns", None, None, ("STrig", ("IsRun", M)))]
    for f, template in THEN.items():
        if f.startswith("SDoes"):
            continue
        args = {"SPrints": (M, ("OneNP", NP)), "SPrintsNot": (M, ("OneNP", NP)), "SExitsErr": (M, NP)}.get(f, (M,))
        out.append(("then", template, None, None, (f,) + args))
    out += verb_rows(vocab, NP, N, META, THEN)
    for kind, kid in sorted(vocab.kind_id.items()):
        inst = (kid + "_toNP", (kid + "_Inst", N))
        out += [("given", "GivenK", kind, None, (kid + "_Given", N)),
                ("given", "GivenCode", kind, None, (kid + "_HoldsText", N, M)),
                ("given", "GivenCodeText", kind, None, (kid + "_HoldsBlock", N)),
                ("when", "WhenRuns", kind, None, ("STrig", ("RunsOn", M, M, inst)))]
        out += [(k, k.capitalize() + "Holds", kind, None, ("SAtom", (h, inst, M))) for k in ("given", "then")
                for h in ("Holds", "HoldsA")]
    for t, kind, tid in attributes(vocab.lex, vocab.ids):
        inst = (vocab.kind_id[kind] + "_Inst", N)
        out += [("given", "GivenK_A", kind, t.term, (tid + "_Given", N, M)),
                ("when", "WhenBecomes", kind, t.term, ("STrig", (tid + "_Becomes", inst, M)))]
        out += [(k, k.capitalize() + "K_A", kind, t.term, ("SAtom", (tid + s, inst, M))) for k in ("given", "then")
                for s in ("_Is", "_IsNot")]
    for fun, (k1, k2) in sorted(vocab.relations.items()):
        atom = ("SAtom", (fun + "_Atom", (vocab.kind_id[k1] + "_Inst", N), (vocab.kind_id[k2] + "_Inst", N)))
        out += [(k, k.capitalize() + "R", k1, None, atom) for k in ("given", "then")]
    return [_row(vocab, *entry) for entry in out]

