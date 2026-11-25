"""The logical form as `grammar/check.lp`'s facts (the CNL 4 design, section 7.4, I12a): what a codified-2 requirement
means, read from its form (spec_lf), never from its tree, in the facts of design-r3 §3. A referent a part introduces is a role `role(R,X,K)` under its own name (x1, x2 ...); an actor is its
id, a code that names a command run its text, any other code or an indexical a role with `named(R,X,C)`. A While or
Where part, and what the trigger says of its referents, is the pre-state (`cond`, `crel`, a state verb's atom
`crel(R,E,S,O,Pol)`, O `none` for a frame with no object, `none`, `rnone` for a `not` box with referents of its own);
the trigger's event is `trig(R,P,E,D,X)`, a run `trig(R,ran,Cmd,D,On)`; each act of the response a
`resp(R,I,Pol,E,D,X)`, with its object's restrictions `oattr`, `orel`. "print", "exit successfully", "exit with an
error naming", "change nothing" are the check's `print`, `exit_ok`, `exit_error`, `change_nothing`; setting an
attribute is spec_lf_set's. Two boxes keep their meaning (b114, b116): an `every` object is `each(R,X)`, an
obligation on each thing of its restrictor, so what another line says of that thing need only agree with it; "X shall
V only Ks that P" obliges no V: it is `only(R,I,E,D,X)` with its restrictor `rattr(R,X,T,V)`, `rrel(R,Q,X,Y)`, which
clashes only with a V of a thing known to fall outside it. A count ("print at least two stages", call 4, I15) is
`count(R,I,E,D,X,B,N)` of each act on its counted object X, with its bound B (`least`, `most`, `exactly`, `more`,
`fewer`) and number N, and a `resp` only when it admits no fewer than one X. Each line is marked `cnl4(R)`, so the
check reads its pairs as codified-2 lines (the If tag, a universal condition paired with each line). A "may" line and
a necessity are spec_lf_modal's; every and a count in a condition and a negated restriction spec_lf_quant's. The words are spec_lf_ids', the atoms' terms
spec_lf_facts_atoms'. An `or` box splits it (`R#n`,
`disj`); no translation, a ValueError.
"""
import spec_lf_distinct
import spec_lf_exist
import spec_lf_facts_request
import spec_lf_member
import spec_lf_modal
import spec_lf_none
import spec_lf_number
import spec_lf_option
import spec_lf_ordered
import spec_lf_quant
import spec_lf_set
from spec_lf_core import Atom, Box, const, least, next_choice
from spec_lf_facts_atoms import TIME, Terms

FORMS = {("response",): "ubiq", ("when", "response"): "when", ("while", "response"): "while",
         ("where", "response"): "where", ("if", "response"): "if", ("while", "when", "response"): "while_when",
         ("where", "when", "response"): "where_when", ("where", "while", "response"): "where_while",
         ("while", "if", "response"): "while_if", ("where", "if", "response"): "where_if"}


class Walk(Terms):
    """One walk of one form: its facts and the choices it took at each `or` box."""

    def pick(self, n):
        c = self.choices[len(self.taken)] if len(self.taken) < len(self.choices) else 0
        self.taken.append(c)
        self.options.append(n)
        return c

    # --- the boxes of the pre-state ------------------------------------------------------------------------------
    def box(self, box, pos):
        if box.op == "or":
            case = box.body[self.pick(len(box.body))]
            self.roles(case.refs)
            for item in case.body:
                self.literal(item, pos)
        elif box.op == "not" and not box.refs:
            for item in box.body:
                self.literal(item, not pos)
        elif box.op == "not" and pos and spec_lf_none.nested(box):     # a `not` inside the "no" box (b238)
            spec_lf_none.facts(self, box)
        elif box.op == "not" and pos:
            self.none(set(box.refs), box.body)
        elif box.op in ("every", "count") and pos:     # spec_lf_quant's (b197)
            spec_lf_quant.condition(self, box)
        else:
            raise ValueError("no translation of %s in a condition" % box.op)

    def none(self, own, body):
        """"no K that ...": over the whole pre-state, its own referents named by their kind."""
        def side(r):
            return "kind(%s)" % self.ids.kind(r.kind) if r in own else self.term(r)
        for item in body:
            if spec_lf_member.nothing(item, own):     # "holds nothing" (b274): no K of each row
                spec_lf_member.none(self, item)
            elif isinstance(item, Atom) and item.pred == "attr" and item.args[0] in own:
                x, term, value = item.args
                self.emit("none", self.ids.kind(x.kind), *self.ids.attr(x.kind, term, value))
            elif isinstance(item, Atom) and item.pred in ("rel", "state"):
                q, x, y = self.edge(item)
                self.emit("rnone", q, side(x), side(y))
            elif isinstance(item, Atom) and item.pred == spec_lf_exist.PRED and item.args[0] in own:
                spec_lf_exist.none(self, item.args[0].kind)     # "no K exists" (b240)
            elif isinstance(item, Atom) and item.pred in TIME:
                raise ValueError(TIME[item.pred](item))
            else:
                raise ValueError("no translation of no there")

    # --- the rule ----------------------------------------------------------------------------------------------
    def run(self, form):
        ops = tuple(p.op for p in form.parts)
        if spec_lf_modal.necessary(self, form):
            return self.out
        if ops not in FORMS:
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
        if spec_lf_facts_request.requests(part):     # a request with its parameters (the domain contract)
            return spec_lf_facts_request.trigger(self, part)
        events = [a for a in part.body if isinstance(a, Atom) and a.pred == "event"]
        if len(events) != 1 and not spec_lf_distinct.one_act(events):
            raise ValueError("no translation of a trigger with %d events" % len(events))
        for event in events:     # the acts of "two Ks" (b240): one trigger each, one verb and one doer
            self.trig(event, spec_lf_option.arguments(part.body))
        for item in part.body:
            if item not in events and getattr(item, "pred", None) != spec_lf_option.PRED:
                self.literal(item)

    def trig(self, event, args=None):
        _, verb, _, roles = event.args
        subject, kinds, _ = self.slots(roles)
        if verb == "run" and kinds and kinds[0].origin in ("constant", "parameter"):
            cmd, on = spec_lf_option.command(roles, args or {})     # with its options (b240)
            self.emit("trig", "ran", const(cmd), self.term(subject), self.obj(on))
        else:
            e, d, x = self.event(event)
            self.emit("trig", "does", e, d, x)

    # --- the response ------------------------------------------------------------------------------------------
    def response(self, body, own, pos=True):
        for item in body:
            if isinstance(item, Atom) and item.pred in ("event", spec_lf_set.PRED):
                self.act(item, pos)
            elif isinstance(item, Atom) and item.pred in spec_lf_facts_request.ASKED:     # response-request (b543)
                spec_lf_facts_request.act(self, item, body, pos)
            elif isinstance(item, Atom) and item.pred == spec_lf_ordered.PRED:     # an order of the act before it (b275)
                spec_lf_ordered.facts(self, item, self.acts)
            elif isinstance(item, Atom):
                self.restrict(item, own)
            elif spec_lf_ordered.held(item):     # an order on a collection's members (b334), of the act on it
                spec_lf_ordered.facts(self, spec_lf_ordered.held(item)[2], self.acts)
            elif item.op == "not" and not self.acting(item):
                spec_lf_quant.negated(self, item, own)
            elif item.op == "not" and self.nothing(item):
                self.acts += 1
                self.emit("resp", self.acts, "pos" if pos else "neg", "change_nothing", self.term(
                    item.body[0].args[3][0][1]), "none")
            elif item.op == "not":
                self.roles(item.refs)
                self.response(item.body, own | set(item.refs), not pos)
            elif item.op == "every" and spec_lf_member.every(self, item, own):     # holds-exactly (b274)
                continue
            elif item.op == "every" and pos:
                self.roles(item.refs)
                for r in item.refs:
                    self.emit("each", r.name)
                for c in item.body:
                    self.restrict(c, own | set(item.refs))
                self.response(item.scope.body, own | set(item.refs) | set(item.scope.refs))
            elif item.op in ("only", "count") and pos and spec_lf_quant.held(item):     # over a row (b272)
                spec_lf_quant.holding(self, item, own)
            elif item.op == "only" and pos and not self.may:
                self.only(item)
            elif item.op == "count" and pos:
                self.count(item, own | set(item.refs))
            elif item.op == "number":      # a printed number (b240), or one not printed
                spec_lf_number.facts(self, item)
            else:
                raise ValueError("no translation of %s in a response" % item.op)

    @staticmethod
    def acting(box):
        """True for a box with an event atom in it, at any depth: a negated act, not a negated restriction."""
        return any(isinstance(i, Atom) and i.pred in ("event", "request", spec_lf_set.PRED)
                   or isinstance(i, Box) and Walk.acting(i)
                   for i in list(box.body) + ([box.scope] if getattr(box, "scope", None) else []))

    @staticmethod
    def nothing(box):
        """True for "change nothing": `not` over a thing changed, and nothing else."""
        return (len(box.refs) == 1 and box.refs[0].kind == "thing" and len(box.body) == 1
                and isinstance(box.body[0], Atom) and box.body[0].pred == "event" and box.body[0].args[1] == "change")

    def act(self, atom, pos):
        if atom.pred == spec_lf_set.PRED:     # setting an attribute (b216): `set` and its `resp`
            return spec_lf_set.facts(self, atom, spec_lf_modal.polarity(self, pos))
        e, d, x = self.event(atom)
        if spec_lf_facts_request.operated(self, e):     # an operation's act with no parameters: a request (b571)
            return spec_lf_facts_request.asked(self, pos, "req(%s,())" % e, d, x, e, x)
        self.acts += 1
        self.emit("resp", self.acts, spec_lf_modal.polarity(self, pos), e, d, x)
        if e == "named" and pos:     # the request pack's name: what a response names (spec_lf_facts_request)
            self.emit("names", self.acts, x)

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
            self.emit("only", self.acts, self.keyed(e, x), d, x)

    def count(self, box, own):
        """"D shall V at least n Ks": each act on the counted K a `count`, and a `resp` when the count admits no fewer
        than one K."""
        self.roles(box.refs)
        for c in box.body:
            self.restrict(c, own)
        for item in box.scope.body:
            if not (isinstance(item, Atom) and item.pred == "event"):
                raise ValueError("no translation of a count over that")
            e, d, x = self.event(item)
            if x != box.refs[0].name:
                raise ValueError("no translation of a count of other than an object")
            self.acts += 1
            k = self.keyed(e, x)
            if least(box.count):
                self.emit("resp", self.acts, spec_lf_modal.polarity(self, True), k, d, x)
            self.emit("count", self.acts, k, d, x, spec_lf_quant.BOUNDS[box.count[0]], box.count[1])

    def keyed(self, e, x):
        """The event of act number `self.acts` on x: of a verb naming an operation the request `req(O,())` with its
        `rqo`, as `act` keys it (b571, b579), so a counted or only act clashes with a request of its operation."""
        if not spec_lf_facts_request.operated(self, e):
            return e
        self.emit("rqo", self.acts, e, x)
        return "req(%s,())" % e


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
        seq = next_choice(w.taken, w.options)
    return out
