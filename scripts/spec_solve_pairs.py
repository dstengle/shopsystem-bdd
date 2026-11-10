"""The findings of `model logic` that a pair of requirements gives (design-r3 §6), read off the shown atoms of
`grammar/check.lp`: the L1 of each pair that clashes and of each requirement that contradicts itself, the L6 of each
pair whose clash depends on a prose condition, each pair's witness (its merged pre-state) from one normal solve of the
part `witness` for all of them, and the pairs set aside: a pair that shares a code no unification keeps one thing
(`coded(A,B)` never `fit(A,B)`), checked no further while every other pair's findings are kept (b120)."""
import re
from collections import defaultdict, namedtuple

import clingo
import spec_facts

Finding = namedtuple("Finding", "code ids text")


def order(ident):
    """The sort key of a requirement id: a capability's lines before the universal conditions, then by number."""
    cap, _, local = ident.rpartition("#")
    return (local.startswith("U"), cap, local[:1], int(re.sub(r"\D", "", local) or 0))


def pairs(found):
    """{(id, id) of a pair of requirements, a split's read as one, or (id,) of one: its atoms' (a, b, why, ...)}."""
    by_pair = defaultdict(list)
    for a, b, why, *rest in found:
        pair = tuple(sorted({spec_facts.split(a), spec_facts.split(b)}, key=order))
        by_pair[pair].append((a, b, "self" if len(pair) == 1 else why, *rest))
    return sorted(by_pair.items(), key=lambda kv: [order(i) for i in kv[0]])


def clashes(ctl, solve, words, clashed, maybes=()):
    """The L1 of each pair of requirements, and of each requirement that contradicts itself; the L6 of each pair with
    a `maybe` and no `clash`. Each pair's witness (its merged pre-state) comes from one normal solve for all of them,
    `solve(ctl)` giving its shown atoms."""
    out, firm, chosen = [], set(), []
    for code, fact, found in (("L1", "focus", clashed), ("L6", "focusm", maybes)):
        for pair, hits in pairs(found):
            if len(pair) == 1:
                out.append(Finding("L1", list(pair), "%s contradicts itself" % pair[0]))
                continue
            if pair in firm:
                continue
            firm.add(pair)
            chosen.append((code, fact, pair, hits, min(hits)[:2]))
    found = witnesses(ctl, solve, [(fact, ab) for _, fact, _, _, ab in chosen])
    for code, _, pair, hits, (a, b) in chosen:
        x, y = (a, b) if spec_facts.split(a) == pair[0] else (b, a)
        text = words.clash(x, y, sorted({h[2] for h in hits}), words.pre(a, b, found[(a, b)]))
        if code == "L6":
            text = words.maybe(sorted({h[3] for h in hits}), text)
        out.append(Finding(code, list(pair), text))
    return out


def witnesses(ctl, solve, focused):
    """{pair: the pre/prec atoms of its witness}: the pairs as facts focus(A,B) (an L1) or focusm(A,B) (an L6) of
    check.lp's part `witness`, ground on the check's own grounding, and one normal solve. Pairs share no atom, so the
    one model holds a witness of each, the same one a solve focused on that pair alone finds."""
    by = defaultdict(list)
    if not focused:
        return by
    ctl.add("witness", [], "\n".join("%s." % clingo.Function(e, [clingo.String(a), clingo.String(b)])
                                     for e, (a, b) in focused))
    ctl.ground([("witness", [])])
    for atom in solve(ctl):
        sym = clingo.parse_term(atom)
        if sym.name in ("pre", "prec"):
            by[(sym.arguments[0].string, sym.arguments[1].string)].append(atom)
    return by


def aside(coded, fit):
    """An `aside` of each pair that shares a code (`coded`) no unification keeps one thing (never `fit`): that pair is
    set aside, and only it."""
    kept = {tuple(p) for p in fit}
    out = []
    for pair, _ in pairs([(a, b, "aside") for a, b in coded if (a, b) not in kept]):
        if len(pair) == 2:
            same = pair[0].rpartition("#")[0] == pair[1].rpartition("#")[0]
            other = "#" + pair[1].rpartition("#")[2] if same else pair[1]
            out.append(Finding("aside", list(pair), "%s and %s name one code of two things that cannot be one: the "
                               "pair is set aside, not checked against each other" % (pair[0], other)))
    return out
