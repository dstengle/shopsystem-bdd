"""The atoms of a logical form as `grammar/check.lp`'s terms, for spec_lf_facts' walk (`Terms`, which its `Walk`
extends): a referent as its term (an actor its id, a code or an indexical a role with `named(R,X,C)`), an event atom
as its (event, doer, object), print, exit successfully and exit with an error naming as the check's own events
(`WORDS`), a relation's or a state verb's atom as an edge, an atom of the pre-state as `cond` or `crel`, and a
restriction of a response's object as `oattr`, `orel`; an attribute's value compared, spec_lf_order's `ccmp`; a time
atom refused naming it (`TIME`). The boxes, the rule and
the response are spec_lf_facts'.
"""
import spec_lf_distinct
import spec_lf_order
import spec_lf_quant
from spec_facts_np import const
from spec_lf_core import Box, Ref

WORDS = {("exit", "successfully"): "exit_ok", ("exit", "with an error naming"): "exit_error", ("print",): "print"}

# the time atoms (spec_lf_time, I16), which check.lp has no reading of: a line holding one is refused naming it
TIME = {"cmp": lambda a: "no translation of a comparison of moments",
        "history": lambda a: "no translation of the history of %s" % a.args[0]}


class Terms:
    """The terms of one walk of one form, and the facts it emits."""

    def __init__(self, ids, rid, choices=()):
        self.ids, self.rid, self.out, self.acts = ids, const(rid), [], 0
        self.choices, self.taken, self.options = list(choices), [], []

    def emit(self, pred, *args):
        fact = "%s(%s)." % (pred, ",".join((self.rid,) + tuple(str(a) for a in args)))
        if fact not in self.out:
            self.out.append(fact)

    # --- terms -------------------------------------------------------------------------------------------------
    def term(self, ref):
        if ref is None:     # the object of a state whose frame takes none (edge)
            return "none"
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

    # --- an atom of the pre-state ---------------------------------------------------------------------------------
    def literal(self, item, pos=True):
        if isinstance(item, Box):
            return self.box(item, pos)
        if item.pred == "attr":
            x, term, value = item.args
            if isinstance(value, Ref):
                return      # "the status of x": an image the pre-state says nothing of
            tid, vid = spec_lf_order.value_ids(self, x.kind, term, value)
            self.emit("cond", self.term(x), tid, vid, "pos" if pos else "neg")
        elif item.pred in ("rel", "state"):
            q, x, y = self.edge(item)
            self.emit("crel", q, self.term(x), self.term(y), "pos" if pos else "neg")
        elif item.pred == "cmp" and len(item.args) == 4:     # an attribute's value compared (b240)
            spec_lf_order.literal(self, item, pos)
        elif item.pred == spec_lf_distinct.PRED:     # two things told apart (b240): never one thing
            if not pos:
                raise ValueError("no translation of distinct in a negated condition")
            self.emit(spec_lf_distinct.PRED, *(self.term(x) for x in item.args))
        elif item.pred in TIME:
            raise ValueError(TIME[item.pred](item))
        else:
            raise ValueError("no translation of an event in a condition")

    def edge(self, atom):
        """(relation, x, y) of a `rel` atom or of a state verb's atom; y None when its frame takes no object (b219)."""
        if atom.pred == "rel":
            word, x, y = atom.args
            return self.ids.relation(word, x.kind, y.kind), x, y
        verb, _, roles = atom.args
        subject, kinds, fixed = self.slots(roles)
        if len(kinds) > 1 or fixed:
            raise ValueError("no translation of the state %s there" % verb)
        return self.ids.event(verb), subject, (kinds or [None])[0]

    # --- a restriction of an object -------------------------------------------------------------------------------
    def restrict(self, item, own, preds=("oattr", "orel")):
        """A restriction of a response's object (`own`, the referents its box introduced); of an earlier referent,
        the pre-state it presupposes."""
        if isinstance(item, Box) and item.op == "not":
            return spec_lf_quant.negated(self, item, own)
        pred = getattr(item, "pred", None)
        if pred == spec_lf_distinct.PRED:
            return self.literal(item)
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
