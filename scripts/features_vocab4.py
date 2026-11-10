"""A step of a codified-2 context read back through the step grammar 4 (the CNL 4 design, section 9; I14a): its one
reading under its keyword and the Call features_vocab gives a step of grammar 3, keyed by the same templates, so a
handler finds a codified-2 step as it finds a codified-1 one.

The templates: a Given that brings in an instance `GivenK`; example data `GivenCodeText` (a block under the step)
and `GivenCode` (one value, in `quoted`); a value `GivenK_A`, `ThenK_A`; the number of Ks compared `GivenCount`
(its noun phrase the subject, the comparison its one noun phrase, b240); a state `GivenDoes`, `GivenDoesNot`,
`ThenDoes`, `ThenDoesNot` ("x exists" of the verb exist, b240); a run `WhenRuns`, any other trigger `WhenHappens`;
an act `ThenPrints`, `ThenPrintsNot`, `ThenExitsOk`, `ThenExitsErr`, `ThenChangesNothing`, else `ThenDoes`,
`ThenDoesNot`. A step of more than one reading under its keyword (the same text read with a code of two kinds is
one) is refused.
"""
import re

import spec_lf_np
import spec_rgl_np
import spec_rgl_steps
from features_vocab import Call, StepError

ROW = re.compile(r"^r\d+_(\w+?)_(Has|Holds|Is)$")
ALLOWED = {"given": ("SCond", "_Given", "_HoldsBlock", "_HoldsText"), "when": ("STrig",), "then": ("SCond", "_Does")}


def _fun(tree):
    return tree if isinstance(tree, str) else tree[0]


def _verb(names, vp):
    """The term of a verb phrase's fun (`e_exit_action_3_2`); "set" of an attribute's `<t>_Set` (b216); a row's
    word of its frame (`r1_of_Has` "has", `r2_in_Holds` "holds") or of its condition (`r3_on_Is`, b197)."""
    if names.attr(_fun(vp))[1] == "Set":
        return "set"
    if _fun(vp) == spec_rgl_np.EXISTS:      # "x exists" (b240)
        return "exist"
    row = ROW.match(_fun(vp))
    if row:
        return {"Has": "has", "Holds": "holds"}.get(row.group(2), row.group(1).replace("_", " "))
    n = int(_fun(vp).rsplit("_", 2)[1])
    return names.verbs[n].term.term


def template(names, keyword, tree):
    """(template, kind, attribute, term) of a step tree."""
    fun, args = tree[0], tree[1:]
    if fun.endswith("_Given"):
        kind = names.kind(fun)[0]
        return "GivenK", kind, None, kind
    if fun.endswith(("_HoldsBlock", "_HoldsText")):
        kind = names.kind(fun)[0]
        return ("GivenCodeText" if fun.endswith("_HoldsBlock") else "GivenCode"), kind, None, kind
    if fun == "STrig":
        event = args[0]
        verb = _verb(names, event[2])
        return ("WhenRuns" if verb == "run" else "WhenHappens"), None, None, verb
    if fun == "SCond" and args[0][0] == "Count_Cmp":     # the number of Ks compared (b240)
        return keyword.capitalize() + "Count", None, None, None
    if fun == "SCond":
        cond = args[0]
        t, rest = names.attr(cond[0])
        neg = cond[1] == ("PNeg",)
        if t is not None:
            kind = names.kind(rest)[0]
            return keyword.capitalize() + "K_A", kind, t.term, kind
        verb = _verb(names, cond[0] if ROW.match(cond[0]) else cond[3])
        return keyword.capitalize() + ("DoesNot" if neg else "Does"), None, None, verb
    neg, verb, vp = args[0] == ("PNeg",), _verb(names, args[2]), args[2]
    if verb == "print":
        return ("ThenPrintsNot" if neg else "ThenPrints"), None, None, None
    if verb == "exit":
        return ("ThenExitsErr" if len(vp) > 1 else "ThenExitsOk"), None, None, None
    if verb == "change" and vp[1:] == (("k_thing_One", ("k_thing_Nothing",)),):
        return "ThenChangesNothing", None, None, None
    return ("ThenDoesNot" if neg else "ThenDoes"), None, None, verb


def step(root, keyword, text):
    """A step's Call, read in the step grammar 4 under its keyword; StepError when it has not one reading."""
    vocab, gram = spec_rgl_steps.load(root)
    try:
        found = spec_rgl_steps.trees(root, text)
    except spec_rgl_steps.StepError as err:
        raise StepError(str(err))
    trees = [t for t in found if t[0].endswith(ALLOWED[keyword])]
    names = spec_lf_np.Names(vocab)
    read = {template(names, keyword, t) for t in trees}
    if len(read) != 1:
        raise StepError("%r does not read as one %s step (%d readings)" % (text, keyword, len(read)))
    tree = trees[0]
    name, kind, attribute, term = read.pop()
    call = Call(keyword, name, text, tree)
    call.kind, call.attribute = kind, attribute
    for node in nodes(tree):
        if node[0] in ("NameLit", "QuotedLit"):
            (call.names if node[0] == "NameLit" else call.quoted).append(node[1])
        elif node[0] == "CodeLit" and name == "WhenRuns" and call.command is None:
            call.command = node[1]
        elif node[0] == "CodeLit" and name.endswith("K_A"):     # a value no entry lists (b240)
            call.values.append(node[1])
        elif names.attr(node[0])[0] is not None and "_v_" in node[0]:
            call.values.append(names.value(node[0]))
    row = tree[0] == "SCond" and ROW.match(tree[1][0])
    if name.endswith("Count"):
        call.subject = spec_rgl_steps.text(gram, tree[1][1])
        call.nps = [" ".join(spec_rgl_steps.text(gram, a) for a in tree[1][2:]).strip()]
    elif tree[0].endswith("_Does") or tree[0] == "SCond" and (row or not tree[1][0].endswith(("_Is", "_IsCode", "_HasNo"))):
        clause = tree[1] if tree[0] == "SCond" else tree
        call.subject = spec_rgl_steps.text(gram, clause[2])
        call.nps = [spec_rgl_steps.text(gram, a) for a in (clause[3:] if row else clause[3][1:])]
        call.event = _verb(names, clause[0] if row else clause[3])
    if name == "WhenHappens":
        call.subject, call.event = spec_rgl_steps.text(gram, tree[1][1]), term
    call.term = (call.command if name == "WhenRuns" else call.subject if name.startswith("Then") and term is None
                 else term)
    return call


def nodes(tree):
    """Every node of a tree (nested tuples), in preorder."""
    if isinstance(tree, tuple):
        yield tree
        for a in tree[1:]:
            yield from nodes(a)

