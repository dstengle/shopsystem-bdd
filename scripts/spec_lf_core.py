"""The logical form's types (the CNL 4 design, call 8, section 7.1-7.2; I11a): referents, atoms and boxes, the state
of one tree's translation, and `apply`, which places a clause's noun phrases around its atom by their determiners.

A referent (`Ref`) has a kind and an origin: `while` (a Where or While clause), `trigger`, `response`, `indexical`
(the run's own thing of a kind whose entry has `This:`, call 6), `parameter` (a code that names no word of the
context, call 7) or `constant` (an actor, a code that is a word of the context). An atom (`Atom`) is `event` (an
action verb's frame, with its event), `state` (a state verb's frame), `rel` (a relation row: has, holds, of, in) or
`attr` (an attribute's value). A box (`Box`) is a part of the rule (`while`, `where`, `when`, `if`, `response`) or
`not`, `every`, `only` (each with its referents, its body and, for every and only, its scope) or `or` of `case`s.
"""
from dataclasses import dataclass, field, replace

ORIGINS = ("while", "trigger", "response", "indexical", "parameter", "constant")


@dataclass(frozen=True)
class Ref:
    name: str               # x1, x2 ... in order of first mention
    kind: str
    origin: str
    value: str = None       # an actor's or a code's words, an indexical's `This:`
    definite: bool = False  # said "the" and bound to no earlier referent (the reading rules, I11b, resolve it)


@dataclass(frozen=True)
class Atom:
    pred: str               # event, state, rel, attr
    args: tuple


@dataclass(frozen=True)
class Box:
    op: str
    refs: tuple = ()
    body: tuple = ()
    scope: object = None    # every, only: the Box of what holds of each referent


@dataclass(frozen=True)
class Form:
    """A requirement's logical form: its modality, the referents no part introduces (constants, parameters,
    indexicals), and its parts in order (Where, While, the trigger, the response), each a Box."""
    modality: str
    fixed: tuple
    parts: tuple


@dataclass
class NP:
    """A noun phrase translated: its referent, its determiner's reading (`a`, `every`, `no`, `only`, `fixed` for a
    referent placed elsewhere), what restricts it and the referents that introduces, and the noun phrases nested in
    it ("the status of every stage"), placed around it first."""
    ref: Ref
    quant: str
    restr: list = field(default_factory=list)
    inner: list = field(default_factory=list)
    deps: list = field(default_factory=list)
    new: bool = True
    said: str = None        # the determiner and noun as said ("a stage", "stages"), for a reading rule's refusal


@dataclass
class NPList:
    op: str                 # and, or
    members: list


class State:
    """One tree's translation: the vocabulary, the referents made so far, the origin of the part being read, the
    subject of the clause being read ("its"), the functional images made ("the status of x" once a line)."""

    def __init__(self, vocab, names):
        self.vocab, self.names = vocab, names
        self.refs, self.fixed, self.images = [], {}, {}
        self.origin, self.subject, self.events = "trigger", None, 0
        self.clauses = None     # spec_lf_clause, which the relative clauses of spec_lf_np are read by
        self.notes = []         # the reading rules' refusals met while translating (spec_lf_read), in order

    def ref(self, kind, origin=None, value=None, definite=False):
        r = Ref("x%d" % (len(self.refs) + 1), kind, origin or self.origin, value, definite)
        self.refs.append(r)
        return r

    def constant(self, kind, value, origin):
        """The one referent of a constant, parameter or indexical, made on its first mention."""
        key = (origin, value)
        if key not in self.fixed:
            self.fixed[key] = self.ref(kind, origin, value)
        return self.fixed[key]

    def image(self, key, kind):
        """(the referent of a functional image, made now)."""
        if key in self.images:
            return self.images[key], False
        self.images[key] = self.ref(kind)
        return self.images[key], True

    def bound(self, kind):
        """The latest referent of `kind` or a kind under it that a part introduced, or None."""
        return next((r for r in reversed(self.refs) if r.origin in ORIGINS[:3]
                     and kind in self.vocab.ancestors(r.kind)), None)

    def event(self):
        self.events += 1
        return "e%d" % self.events


def fixed(ref):
    return NP(ref, "fixed", new=False)


def apply(args, build, neg_at=None):
    """(referents, conditions) of a clause: `args` its noun phrases in order (the subject first), `build(refs)` its
    atom over their referents; a list with "and" gives an atom for each member, one with "or" an `or` box; "every",
    "no" and "only" box the rest of the clause; from the argument `neg_at` on, the clause is under `not`."""
    return _go([(a, True) for a in args], build, [], neg_at, 0)


def _go(items, build, chosen, neg_at, i):
    if neg_at == i:
        refs, conds = _go(items, build, chosen, None, i)
        return [], [Box("not", _uniq(refs), _uniq(conds))]
    if not items:
        return [], [build(chosen)]
    (a, main), rest = items[0], items[1:]
    if isinstance(a, NPList):
        parts = [_go([(m, main)] + rest, build, chosen, neg_at, i) for m in a.members]
        if a.op == "and":
            return [r for p in parts for r in p[0]], [c for p in parts for c in p[1]]
        return [], [Box("or", (), tuple(Box("case", _uniq(r), _uniq(c)) for r, c in parts))]
    if a.deps:
        return _go([(d, False) for d in a.deps] + [(replace(a, deps=[]), main)] + rest, build, chosen, neg_at, i)
    refs, conds = _go(rest, build, chosen + [a.ref] if main else chosen, neg_at, i + 1 if main else i)
    own = ([a.ref] if a.new else []) + a.inner
    if a.quant in ("every", "only"):
        return [], [Box(a.quant, _uniq(own), _uniq(a.restr), Box("scope", _uniq(refs), _uniq(conds)))]
    if a.quant == "no":
        return [], [Box("not", _uniq(own + refs), _uniq(a.restr + conds))]
    return own + refs, a.restr + conds


def _uniq(items):
    return tuple(dict.fromkeys(items))


def part(op, refs, conds):
    return Box(op, _uniq(refs), _uniq(conds))
