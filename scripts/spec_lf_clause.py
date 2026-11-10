"""The clauses of grammar 4 in the logical form (the CNL 4 design, call 8; I11a): the rule (Where, While, the trigger,
the responses), each condition, trigger and act a clause over a verb phrase, one translation per template.

A frame's verb phrase is an `event` atom for an action verb and a `state` atom for a state verb, its roles the
subject and each kind of the frame by the words before it (`object` when there are none), the frame's fixed words at
its end a role of their own ("successfully"), its sense the entry's place among the entries of its word; a row's
"has" and "holds" are `rel` atoms; a verb phrase with a gap is the same atom with the gap's referent in its role. A
negated clause puts all but its subject under `not`.

The form's modality (I17) is the line's: `shall` for an obligation, `may` for a permission (a doer's `May`), and
`always` or `never` for a necessity, a line of no trigger whose one clause (`Nec`) is its part `holds`, read as a
While clause is (any K). A line that says both "shall" and "may", or "may not", is noted for spec_lf_read to refuse.
"""
import spec_lf_core as core
import spec_lf_exist
import spec_lf_np as nps
import spec_lf_number
import spec_lf_order
import spec_lf_read
import spec_lf_set
import spec_lf_time
import spec_lf_values
from spec_lf_core import Atom, Box, NPList

ORIGIN = {"where": "while", "while": "while", "when": "trigger", "if": "trigger", "response": "response",
          "holds": "while"}
MODALITY = {"Shall": "shall", "May": "may", "MAlways": "always", "MNever": "never"}


def sense(st, n):
    """The place of verb n's entry among the entries of its word."""
    v = st.names.verbs[n]
    return sum(1 for m, w in st.names.verbs.items() if m <= n and w.term.term == v.term.term)


def frame_atom(st, n, m, slots):
    """The atom of frame m of verb n, `slots` the referent of each kind of the frame in order."""
    v = st.names.verbs[n]
    roles, it = [("subject", slots[0])], iter(slots[1:])
    for words, kind in v.frames[m - 1][1]:
        roles.append((" ".join(words) or "object", next(it)) if kind is not None else (" ".join(words),))
    if v.aspect == "action":
        return Atom("event", (st.event(), v.term.term, sense(st, n), tuple(roles)))
    return Atom("state", (v.term.term, sense(st, n), tuple(roles)))


def numbers(name, count):
    return [int(x) for x in name.rsplit("_", count)[1:]]


def vp(st, tree):
    """(the verb phrase's noun phrases, build(subject, their referents) -> its atom)."""
    name, a = nps.fun(tree), nps.args(tree)
    row, suffix = st.names.row(name)
    if suffix in ("Has", "Holds"):
        return [nps.np(st, a[0])], lambda s, r: Atom("rel", (row[1], r[0], s))
    if name.startswith("e_"):
        n, m = numbers(name, 2)
        return [nps.np(st, x) for x in a], lambda s, r: frame_atom(st, n, m, [s] + list(r))
    return spec_lf_exist.vp(name) or spec_lf_set.vp(st, tree, nps.owner) or _unknown(tree)


def _unknown(tree):
    raise nps.unknown(tree)


def gap(st, tree):
    """(the noun phrases of a verb phrase with a gap, build(subject, the gap's referent, their referents))."""
    name, a = nps.fun(tree), nps.args(tree)
    row, suffix = st.names.row(name)
    if suffix == "Gap":
        return [], lambda s, g, r: Atom("rel", (row[1], g, s))
    if not name.startswith("g_"):
        raise nps.unknown(tree)
    n, m, k = numbers(name, 3)
    pieces = st.names.verbs[n].frames[m - 1][1]
    slots = [i for i, (_, kind) in enumerate(pieces) if kind is not None]
    gaps = ([0] if slots[0] == 0 else []) + ([slots[-1]] if 0 < slots[-1] == len(pieces) - 1 else [])
    at = slots.index(gaps[k - 1])

    def build(s, g, r):
        r = list(r)
        return frame_atom(st, n, m, [s] + r[:at] + [g] + r[at:])
    return [nps.np(st, x) for x in a], build


def subject_of(np):
    return np.members[0].ref if isinstance(np, NPList) else np.ref


def clause(st, subject, vptree, neg):
    """(referents, conditions) of a clause: its subject's noun phrase (translated) and its verb phrase's tree."""
    saved, st.subject = st.subject, subject_of(subject)
    args, build = vp(st, vptree)
    st.subject = saved
    if neg:
        spec_lf_read.negated(st, subject_of(subject), args, vptree)     # R4
    return st.apply([subject] + args, lambda r: build(r[0], r[1:]), 1 if neg else None)


def gapped(st, ref, subject, gaptree, neg):
    """(referents, conditions) of an object relative clause on `ref`: "a stage that sessions follow"."""
    saved, st.subject = st.subject, subject_of(subject)
    args, build = gap(st, gaptree)
    st.subject = saved
    if neg:
        spec_lf_read.negated(st, subject_of(subject), args, gaptree)    # R4
    return st.apply([subject] + args, lambda r: build(r[0], ref, r[1:]), 1 if neg else None)


def cond(st, tree):
    name, a = nps.fun(tree), nps.args(tree)
    if name in ("OneCond", "AndCond", "OrCond"):
        first = cond(st, a[0])
        if name == "OneCond":
            return first
        if name == "AndCond":
            rest = cond(st, a[1])
            return first[0] + rest[0], first[1] + rest[1]
        cases = [core.part("case", *first)]
        st.close(cases)                 # R2: the first case gives nothing to the second
        cases.append(core.part("case", *cond(st, a[1])))
        st.close(cases)
        return [], [Box("or", (), tuple(cases))]
    rest = st.names.kind(name)[1]
    if rest == "Holds":
        return clause(st, nps.np(st, a[1]), a[2], a[0] == "PNeg")
    t, rest = st.names.attr(name)
    if t is not None and (rest == "IsOf" or rest.endswith("_Is")):
        x = nps.owner(st, a[1]) if rest == "IsOf" else nps.np(st, a[1])
        value = st.names.value(nps.fun(a[2]))
        return st.apply([x], lambda r: Atom("attr", (r[0], t.term, value)), 1 if a[0] == "PNeg" else None)
    valued = spec_lf_values.cond(st, t, rest, a) if t is not None else None     # one of, none of, has no (b240)
    if valued is not None:
        return valued
    ordered = spec_lf_order.cond(st, t, rest, a) if t is not None else None     # after, before (b240)
    if ordered is not None:
        return ordered
    counted = spec_lf_number.cond(st, tree)     # the number of Ks is more than n (b240)
    if counted is not None:
        return counted
    timed = spec_lf_time.cond(st, tree)     # after, before, within the last, the perfect (I16)
    if timed is not None:
        return timed
    raise nps.unknown(tree)


def response(st, tree):
    name, a = nps.fun(tree), nps.args(tree)
    if name in ("OneResp", "AndResp"):
        first = response(st, a[0])
        rest = response(st, a[1]) if name == "AndResp" else ([], [])
        return first[0] + rest[0], first[1] + rest[1]
    said = st.names.kind(name)[1]
    if said not in ("Shall", "May"):
        raise nps.unknown(tree)
    modal(st, MODALITY[said])
    doer, refs, conds, acts = nps.np(st, a[0]), [], [], a[1]
    while True:
        act_name, act = nps.fun(acts), nps.args(acts)
        one = act[0]
        if said == "May" and nps.args(one)[0] == "PNeg":
            spec_lf_read.note(st, 'the line says "may not", which reads as "is not allowed to" and as "is allowed not '
                                  'to": say "shall not", or say what it may do')
        r, c = clause(st, doer, nps.args(one)[1], nps.args(one)[0] == "PNeg")
        refs, conds = refs + r, conds + c
        if act_name.endswith("_OneAct"):
            return refs, conds
        acts = act[1]


def modal(st, modality):
    """The line's modality, noted when a response says another than an earlier one."""
    if st.modality not in (None, modality):
        spec_lf_read.note(st, 'the line says both "%s" and "%s": say each in a line of its own' % (st.modality, modality))
    st.modality = st.modality or modality


def necessity(st, tree):
    """(referents, conditions) of a necessity's one clause: "a session always follows a stage"."""
    a = nps.args(tree)
    if st.names.kind(nps.fun(tree))[1] != "Nec":
        raise nps.unknown(tree)
    modal(st, MODALITY[a[0]])
    return clause(st, nps.np(st, a[1]), a[2], False)


def rule(st, tree):
    """The Form of a requirement's tree."""
    name, a = nps.fun(tree), nps.args(tree)
    parts = []

    def read(op, fn, sub):
        st.origin = ORIGIN[op]
        parts.append(core.part(op, *fn(st, sub)))
    pre = a[0]
    if nps.fun(pre) in ("While", "Where"):
        read(nps.fun(pre).lower(), cond, nps.args(pre)[0])
    elif nps.fun(pre) == "WhereWhile":
        read("where", cond, nps.args(pre)[0])
        read("while", cond, nps.args(pre)[1])
    if name in ("When", "If"):
        trig = a[1]
        if not st.names.kind(nps.fun(trig))[1] == "Event":
            raise nps.unknown(trig)
        read(name.lower(), lambda s, t: clause(s, nps.np(s, nps.args(t)[0]), nps.args(t)[1], False), trig)
    read("holds" if name == "Necessary" else "response", necessity if name == "Necessary" else response, a[-1])
    fixed = tuple(r for r in st.refs if r.origin not in core.ORIGINS[:3])
    return core.Form(st.modality, fixed, tuple(parts))
