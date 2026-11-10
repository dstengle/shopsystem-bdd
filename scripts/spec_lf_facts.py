"""The logical form as `grammar/check.lp`'s facts (the CNL 4 design, section 7.4, I12a): what a codified-2
requirement means, read from its form (spec_lf), never from its tree, in the facts spec_facts gives a codified-1 one,
so both feed one check.

A referent a part introduces is a role `role(R,X,K)` under its own name (x1, x2 ...); an actor is its id, a code that
names a command run its text, any other code or an indexical a role with `named(R,X,C)`. A While or Where part, and
what the trigger says of its referents, is the pre-state (`cond`, `crel`, a state verb's atom `crel(R,E,S,O,Pol)`,
and `none`, `rnone` for a `not` box with referents of its own); the trigger's event is `trig(R,P,E,D,X)`, a run
`trig(R,ran,Cmd,D,On)`; each act of the response a `resp(R,I,Pol,E,D,X)`, with its object's restrictions `oattr`,
`orel`. "print", "exit successfully", "exit with an error naming", "change nothing" are the check's `print`,
`exit_ok`, `exit_error`, `change_nothing`.

Two boxes keep their meaning (b114, b116): an `every` object is `each(R,X)`, an obligation on each thing of its
restrictor, so what another line says of that thing need only agree with it; "X shall V only Ks that P" obliges no V:
it is `only(R,I,E,D,X)` with its restrictor `rattr(R,X,T,V)`, `rrel(R,Q,X,Y)`, which clashes only with a V of a
thing known to fall outside it. Each line is marked `cnl4(R)`, so the check reads its pairs as
codified-2 lines (the If tag, a universal condition paired with each line). The words are named by spec_lf_ids. An `or` box splits the requirement as spec_facts does (`R#n`, `disj`). A construct
with no translation raises ValueError naming it.
"""
import spec_facts
from spec_facts_np import const
from spec_lf_core import Atom, Box, Ref

WORDS = {("exit", "successfully"): "exit_ok", ("exit", "with an error naming"): "exit_error", ("print",): "print"}
FORMS = {("response",): "ubiq", ("when", "response"): "when", ("while", "response"): "while",
         ("where", "response"): "where", ("if", "response"): "if", ("while", "when", "response"): "while_when",
         ("where", "when", "response"): "where_when", ("where", "while", "response"): "where_while",
         ("while", "if", "response"): "while_if", ("where", "if", "response"): "where_if"}


class Walk:
    """One walk of one form: its facts and the choices it took at each `or` box."""

    def __init__(self, ids, rid, choices=()):
        self.ids, self.rid, self.out = ids, const(rid), []
        self.choices, self.taken, self.options = list(choices), [], []
        self.acts = 0

    def emit(self, pred, *args):
        fact = "%s(%s)." % (pred, ",".join((self.rid,) + tuple(str(a) for a in args)))
        if fact not in self.out:
            self.out.append(fact)

    def pick(self, n):
        i = len(self.taken)
        c = self.choices[i] if i < len(self.choices) else 0
        self.taken.append(c)
        self.options.append(n)
        return c

    # --- terms -------------------------------------------------------------------------------------------------
    def term(self, ref):
        if ref.origin == "constant" and ref.value in self.ids.actors:
            return self.ids.actors[ref.value]
        if ref.origin in ("constant", "parameter", "indexical"):
            self.emit("role", ref.name, self.ids.kind(ref.kind))
            self.emit("named", ref.name, const(ref.value))
        return ref.name

    def roles(self, refs):
        for r in refs:
            self.emit("role", r.name, self.ids.kind(r.kind))

    @staticmethod
    def slots(roles):
        """(the subject, the referents of the frame's kinds after it, the fixed words of the frame's end)."""
        subject = roles[0][1]
        kinds = [r[1] for r in roles[1:] if len(r) == 2]
        fixed = tuple(r[0] for r in roles[1:] if len(r) == 1) + tuple(r[0] for r in roles[1:] if len(r) == 2
                                                                         and r[0] == "with an error naming")
        return subject, kinds, fixed

    def obj(self, refs):
        terms = [self.term(r) for r in refs]
        return "none" if not terms else terms[0] if len(terms) == 1 else "pair(%s,%s)" % tuple(terms[:2])

    def event(self, atom):
        """(event, doer, object) of an event atom."""
        _, verb, _, roles = atom.args
        subject, kinds, fixed = self.slots(roles)
        return WORDS.get((verb,) + fixed[:1]) or self.ids.event(verb), self.term(subject), self.obj(kinds)

    # --- the pre-state -----------------------------------------------------------------------------------------
    def literal(self, item, pos=True):
        if isinstance(item, Box):
            return self.box(item, pos)
        if item.pred == "attr":
            x, term, value = item.args
            if isinstance(value, Ref):
                return      # "the status of x": an image the pre-state says nothing of
            tid, vid = self.ids.attr(x.kind, term, value)
            self.emit("cond", self.term(x), tid, vid, "pos" if pos else "neg")
        elif item.pred in ("rel", "state"):
            q, x, y = self.edge(item)
            self.emit("crel", q, self.term(x), self.term(y), "pos" if pos else "neg")
        else:
            raise ValueError("no translation of an event in a condition")

    def edge(self, atom):
        """(relation, x, y) of a `rel` atom or of a state verb's atom between two kinds."""
        if atom.pred == "rel":
            word, x, y = atom.args
            return self.ids.relation(word, x.kind, y.kind), x, y
        verb, _, roles = atom.args
        subject, kinds, fixed = self.slots(roles)
        if len(kinds) != 1 or fixed:
            raise ValueError("no translation of the state %s there" % verb)
        return self.ids.event(verb), subject, kinds[0]

    def box(self, box, pos):
        if box.op == "or":
            case = box.body[self.pick(len(box.body))]
            self.roles(case.refs)
            for item in case.body:
                self.literal(item, pos)
        elif box.op == "not" and not box.refs:
            for item in box.body:
                self.literal(item, not pos)
        elif box.op == "not" and pos:
            self.none(set(box.refs), box.body)
        else:
            raise ValueError("no translation of %s in a condition" % box.op)

    def none(self, own, body):
        """"no K that ...": over the whole pre-state, its own referents named by their kind."""
        def side(r):
            return "kind(%s)" % self.ids.kind(r.kind) if r in own else self.term(r)
        for item in body:
            if isinstance(item, Atom) and item.pred == "attr" and item.args[0] in own:
                x, term, value = item.args
                self.emit("none", self.ids.kind(x.kind), *self.ids.attr(x.kind, term, value))
            elif isinstance(item, Atom) and item.pred in ("rel", "state"):
                q, x, y = self.edge(item)
                self.emit("rnone", q, side(x), side(y))
            else:
                raise ValueError("no translation of no there")

    # --- the rule ----------------------------------------------------------------------------------------------
    def run(self, form):
        ops = tuple(p.op for p in form.parts)
        if form.modality != "shall" or ops not in FORMS:
            raise ValueError("no translation of the rule %s %s" % (form.modality, " ".join(ops)))
        self.emit("form", FORMS[ops])
        self.out.append("cnl4(%s)." % self.rid)
        for p in form.parts:
            self.roles(p.refs)
            if p.op in ("when", "if"):
                self.trigger(p)
            elif p.op == "response":
                self.response(p.body, set(p.refs))
            else:
                for item in p.body:
                    self.literal(item)
        return self.out

    def trigger(self, part):
        events = [a for a in part.body if isinstance(a, Atom) and a.pred == "event"]
        if len(events) != 1:
            raise ValueError("no translation of a trigger with %d events" % len(events))
        _, verb, _, roles = events[0].args
        subject, kinds, _ = self.slots(roles)
        if verb == "run" and kinds and kinds[0].origin in ("constant", "parameter"):
            on = [r[1] for r in roles[1:] if len(r) == 2 and r[0] not in ("object", "with")]
            options = [r[1].value for r in roles[1:] if len(r) == 2 and r[0] == "with"]
            cmd = " ".join([kinds[0].value] + options)
            self.emit("trig", "ran", const(cmd), self.term(subject), self.obj(on))
        else:
            e, d, x = self.event(events[0])
            self.emit("trig", "does", e, d, x)
        for item in part.body:
            if item is not events[0]:
                self.literal(item)

    # --- the response ------------------------------------------------------------------------------------------
    def response(self, body, own, pos=True):
        for item in body:
            if isinstance(item, Atom) and item.pred == "event":
                self.act(item, pos)
            elif isinstance(item, Atom):
                self.restrict(item, own)
            elif item.op == "not" and self.nothing(item):
                self.acts += 1
                self.emit("resp", self.acts, "pos" if pos else "neg", "change_nothing", self.term(
                    item.body[0].args[3][0][1]), "none")
            elif item.op == "not":
                self.roles(item.refs)
                self.response(item.body, own | set(item.refs), not pos)
            elif item.op == "every" and pos:
                self.roles(item.refs)
                for r in item.refs:
                    self.emit("each", r.name)
                for c in item.body:
                    self.restrict(c, own | set(item.refs))
                self.response(item.scope.body, own | set(item.refs) | set(item.scope.refs))
            elif item.op == "only" and pos:
                self.only(item)
            else:
                raise ValueError("no translation of %s in a response" % item.op)

    @staticmethod
    def nothing(box):
        """True for "change nothing": `not` over a thing changed, and nothing else."""
        return (len(box.refs) == 1 and box.refs[0].kind == "thing" and len(box.body) == 1
                and isinstance(box.body[0], Atom) and box.body[0].pred == "event" and box.body[0].args[1] == "change")

    def act(self, atom, pos):
        e, d, x = self.event(atom)
        self.acts += 1
        self.emit("resp", self.acts, "pos" if pos else "neg", e, d, x)

    def restrict(self, item, own, preds=("oattr", "orel")):
        """A restriction of a response's object (`own`, the referents its box introduced); of an earlier referent,
        the pre-state it presupposes."""
        pred = getattr(item, "pred", None)
        if pred not in ("attr", "rel", "state"):
            raise ValueError("no translation of %s on an object" % (pred or item.op))
        first = {"attr": lambda a: a[0], "rel": lambda a: a[1], "state": lambda a: a[2][0][1]}[pred](item.args)
        if first not in own:
            return self.literal(item)
        if item.pred == "attr":
            x, term, value = item.args
            if not isinstance(value, Ref):
                self.emit(preds[0], self.term(x), *self.ids.attr(x.kind, term, value))
        else:
            q, x, y = self.edge(item)
            self.emit(preds[1], q, self.term(x), self.term(y))

    def only(self, box):
        """"D shall V only Ks that P": no act; `only` and the restrictor P of its K (`rattr`, `rrel`)."""
        self.roles(box.refs)
        own = set(box.refs)
        for c in box.body:
            self.restrict(c, own, ("rattr", "rrel"))
        for item in box.scope.body:
            if not (isinstance(item, Atom) and item.pred == "event"):
                raise ValueError("no translation of only over that")
            e, d, x = self.event(item)
            self.acts += 1
            self.emit("only", self.acts, e, d, x)


def translate(ids, ident, form):
    """The facts of one codified-2 requirement's Form (of each of its splits, in order)."""
    first = Walk(ids, ident)
    out = first.run(form)
    if not first.options:
        return out
    out, seq, k = [], [], 0
    while seq is not None:
        k += 1
        sid = "%s#%d" % (ident, k)
        w = Walk(ids, sid, seq)
        out += ["disj(%s,%s)." % (const(sid), const(ident))] + w.run(form)
        seq = spec_facts._next(w.taken, w.options)
    return out
