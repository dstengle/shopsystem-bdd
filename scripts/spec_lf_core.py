"""The logical form's types (the CNL 4 design, call 8, section 7.1-7.2; I11a): referents, atoms and boxes, the state
of one tree's translation, and `apply`, which places a clause's noun phrases around its atom by their determiners.

A referent (`Ref`) has a kind and an origin: `while` (a Where or While clause), `trigger`, `response`, `indexical`
(the run's own thing of a kind whose entry has `This:`, call 6), `parameter` (a code that names no word of the
context, call 7) or `constant` (an actor, a code that is a word of the context). An atom (`Atom`) is `event` (an
action verb's frame, with its event), `state` (a state verb's frame), `rel` (a relation row: has, holds, of, in) or
`attr` (an attribute's value). A box (`Box`) is a part of the rule (`while`, `where`, `when`, `if`, `response`) or
`not`, `every`, `only`, `count` (each with its referents, its body and, for every, only and count, its scope; a count
its bound and number, as ("at least", 2): call 4, I15; a number a parameter's referent, b240), `number` (the Ks "the
number of Ks that P" counts, its `count` the number's referent: spec_lf_number, b240) or `or` of `case`s.
"""
from dataclasses import dataclass, field, replace

ORIGINS = ("while", "trigger", "response", "indexical", "parameter", "constant")


def const(text):
    """A clingo string."""
    return '"%s"' % str(text).replace("\\", "\\\\").replace('"', '\\"')


def split(ident):
    """The requirement a split of an `or` comes from: `s#r5#2` -> `s#r5`; any other id as it is."""
    head, sep, tail = ident.rpartition("#")
    return head if sep and tail.isdigit() else ident


def next_choice(taken, options):
    """The choices of the next walk of a form's `or` boxes after one that took `taken`, or None after the last."""
    for j in range(len(taken) - 1, -1, -1):
        if taken[j] + 1 < options[j]:
            return taken[:j] + [taken[j] + 1]
    return None


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
    scope: object = None    # every, only, count: the Box of what holds of each referent
    count: tuple = None     # count: (its bound, its number), as ("at most", 1); number: the number's Ref


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
    count: tuple = None     # a count's (bound, number): quant "count"
    image: bool = False     # a functional image ("the K of x", "its K", "the T of x") made here: under a negated
    #                         clause it stays outside the `not` (it is there whether or not the clause holds)


@dataclass
class NPList:
    op: str                 # and, or; together: one argument of every member (a run's options, spec_lf_option)
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
        self.open = []          # the referents whose noun phrases are being read: R2 passes over them
        self.boxed = {}         # each referent made inside a box already read (a no, not, every, only or count box, a
        #                         case of an or) and that box: R2 passes over it
        self.modality = None    # shall, may, always, never: the first a response or a necessity says (I17)
        self.pairs = {}         # each referent of "two Ks" and its pair (spec_lf_distinct, b240)

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

    def apply(self, args, build, neg_at=None):
        """`apply`, the referents of each box it gives kept as boxed (R2, b222)."""
        refs, conds = apply(args, build, neg_at)
        self.close(conds)
        return refs, conds

    def close(self, conds):
        """Keep the referents made inside each box of `conds` as boxed, with the box (R2)."""
        for r, b in closed(conds).items():
            self.boxed.setdefault(r, b)

    def event(self):
        self.events += 1
        return "e%d" % self.events


def fixed(ref):
    return NP(ref, "fixed", new=False)


def apply(args, build, neg_at=None):
    """(referents, conditions) of a clause: `args` its noun phrases in order (the subject first), `build(refs)` its
    atom over their referents; a list with "and" gives an atom for each member, one with "or" an `or` box; "every",
    "no", "only" and a count box the rest of the clause; from the argument `neg_at` on, the clause is under `not`."""
    return _go([(a, True) for a in args], build, [], neg_at, 0)


def _go(items, build, chosen, neg_at, i):
    if neg_at == i:
        held = [a for a, main in items if main and isinstance(a, NP) and a.image and a.new
                and not any(d.new or d.restr for d in a.deps)]
        items = [(replace(a, new=False, restr=[], inner=[], deps=[]) if any(a is h for h in held) else a, main)
                 for a, main in items]
        refs, conds = _go(items, build, chosen, None, i)
        outside = [r for a in held for r in [a.ref] + a.inner], [c for a in held for c in a.restr]
        return outside[0], outside[1] + [Box("not", _uniq(refs), _uniq(conds))]
    if not items:
        return [], [build(chosen)]
    (a, main), rest = items[0], items[1:]
    if isinstance(a, NPList) and a.op == "together":    # one argument of every member: a run's options (b240)
        deps, members = [d for m in a.members for d in m.deps], [replace(m, deps=[]) for m in a.members]
        if deps:
            return _go([(d, False) for d in deps] + [(NPList("together", members), main)] + rest, build, chosen,
                       neg_at, i)
        refs, conds = _go(rest, build, chosen + [tuple(m.ref for m in members)] if main else chosen, neg_at,
                          i + 1 if main else i)
        own = [r for m in members for r in ([m.ref] if m.new else []) + m.inner]
        return own + refs, [c for m in members for c in m.restr] + conds
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
    if a.quant == "count":
        return [], [Box("count", _uniq(own), _uniq(a.restr), Box("scope", _uniq(refs), _uniq(conds)), a.count)]
    if a.quant == "no":
        return [], [Box("not", _uniq(own + refs), _uniq(a.restr + conds))]
    return own + refs, a.restr + conds


CLOSING = ("not", "every", "only", "count", "number", "case")


def closed(conds, box=None):
    """{referent: the innermost box it is made in} of `conds`' referents inside a not, every, only, count or number
    box ("no" is a not box) or a case of an or: none is accessible outside its box. A scope's referents are its box's."""
    out = {}
    for c in conds:
        if isinstance(c, Box):
            here = c if c.op in CLOSING else box
            out.update({r: here for r in c.refs} if here is not None else {})
            out.update(closed(c.body, here))
            out.update(closed([c.scope], here) if c.scope is not None else {})
    return out


def least(count):
    """The fewest things a count (bound, number) admits: "at most" and "fewer than" admit none; of a parameter's
    number (a Ref) "more than" admits one, any other bound none."""
    bound, n = count
    if isinstance(n, Ref):
        return 1 if bound == "more than" else 0
    return {"at least": n, "exactly": n, "more than": n + 1}.get(bound, 0)


def _uniq(items):
    return tuple(dict.fromkeys(items))


def part(op, refs, conds):
    return Box(op, _uniq(refs), _uniq(conds))
