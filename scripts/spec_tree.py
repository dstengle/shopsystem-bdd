"""Requirement trees: the post-parse guards (design §9.3, §9.4), normalised trees and `logic_only` (§14.2).

A tree is a nested tuple `(fun, *args)`; a literal (a `CodeLit` or `QuotedLit` string, a `CountNum` integer) is a
plain value in its fun's argument. Typed funs are named by the generated grammar (`spec_typed`): `<kind>_<det>`
for a noun phrase of a kind, `<attribute>_One`/`_More` for a value list. Every core and typed lin keeps its
arguments in their spoken order, so a tree's preorder is the order of the words.
"""
DETS = {"An", "Every", "The", "No", "AtMostOne", "One", "Pl", "Its", "Named"}
FORMS = {"Ubiq": ("resp",), "When": ("trig", "resp"), "While": ("cond", "resp"), "Where": ("feat", "resp"),
         "IfThen": ("trig", "resp"), "WhileWhen": ("cond", "trig", "resp"), "WhereWhen": ("feat", "trig", "resp"),
         "WhereWhile": ("feat", "cond", "resp"), "WhileIf": ("cond", "trig", "resp"),
         "WhereIf": ("feat", "trig", "resp")}
RESOURCE_VPS = {"Hold", "HoldA", "HoldAtMost"}
REPEATABLE = {"MoreNP": ("OneNP", "MoreNP"), "AndVP": ("OneVP", "AndVP"), "OrVP": ("OneVPor", "OrVP"),
              "AndResp": ("OneResp", "AndResp")}
LISTS = {"CondAnd": ("CondOne", "CondAnd"), "CondOr": ("CondOne", "CondOr")}


def nodes(tree):
    """Every application node of the tree, in preorder."""
    if not isinstance(tree, tuple):
        return
    yield tree
    for arg in tree[1:]:
        yield from nodes(arg)


def _kind_det(fun):
    kind, _, det = fun.rpartition("_")
    return (kind, det) if fun.startswith("k_") and kind else (None, None)


def _split(tree, one, more):
    """(members, tail) of a right-recursive list (`One x` / `More x rest`); `tail` is the node that ends it when that
    is not a `One` (CondAnd A (CondOr B C) ends in a CondOr), else None."""
    out = []
    while isinstance(tree, tuple) and tree[0].endswith(more):
        out.append(tree[1])
        tree = tree[2]
    if isinstance(tree, tuple) and tree[0].endswith(one):
        out.append(tree[1])
        return out, None
    return out, tree


def _chain(tree, one, more):
    """The members of a right-recursive list (`One x` / `More x rest`)."""
    return _split(tree, one, more)[0]


def _literals(tree, words):
    for node in nodes(tree):
        if node[0] == "?":
            return "the tree has a gap"
        if node[0] == "CodeLit":
            token = node[1]
            if not (len(token) > 1 and token[0] == token[-1] == "`"):
                return "the code %s has no backticks" % token
            if token in words:
                return "the code %s is a lexicon word" % token
        if node[0] == "QuotedLit" and not (len(node[1]) > 1 and node[1][0] == node[1][-1] == '"'):
            return "the text %s has no double quotes" % node[1]
    return None


def _repeats(tree):
    for node in nodes(tree):
        members = []
        if node[0] in REPEATABLE:
            members = _chain(node, *REPEATABLE[node[0]])
        elif node[0].startswith("t_") and node[0].endswith("_More"):
            members = _chain(node, "_One", "_More")
        for i, m in enumerate(members):
            if m in members[:i]:
                return "the list repeats %s" % show(m)
    return None


def _anaphora(tree):
    seen, any_np = set(), False
    for node in nodes(tree):
        kind, det = _kind_det(node[0])
        if det == "It":
            if kind not in seen:
                return "\"it\" (%s) has no %s before it" % (kind, kind)
        elif det == "Its" and not any_np:
            return "\"its\" has no noun phrase before it"
        if det in DETS:
            seen.add(kind)
            any_np = True
    return None


def guard(tree, words):
    """Why the tree is dropped (a reason), or None when it passes: literals (§9.4), no repeated list member, and
    "it" only after a noun phrase of its kind (§9.3). `words` are the lexicon's spellings."""
    return _literals(tree, words) or _repeats(tree) or _anaphora(tree)


def _rebuild(members, one, more):
    tree = (one, members[-1])
    for m in reversed(members[:-1]):
        tree = (more, m, tree)
    return tree


def normal(tree):
    """The tree with its value lists and condition conjunctions (or disjunctions) in sorted order, so two statements
    that say the same thing in another order compare equal (v15k). A list mixing `and` and `or` keeps its order."""
    if not isinstance(tree, tuple):
        return tree
    fun = tree[0]
    if fun in LISTS or (fun.startswith("t_") and fun.endswith("_More")):
        one, more = LISTS.get(fun) or (fun[:-5] + "_One", fun)
        members, tail = _split(tree, one, more)
        if tail is None:
            return _rebuild(sorted((normal(m) for m in members), key=show), one, more)
    return (fun,) + tuple(normal(a) for a in tree[1:])


def responses(resps):
    """The conjuncts of a `Resps`, in their spoken order, as (polarity, subject, VP) with polarity "Shall" or
    "ShallNot": `shall A and B` gives two "Shall" conjuncts, `shall not A or B` two "ShallNot" ones (neither)."""
    out = []
    for polarity, subject, vps in _chain(resps, "OneResp", "AndResp"):
        one, more = ("OneVP", "AndVP") if polarity == "Shall" else ("OneVPor", "OrVP")
        out += [(polarity, subject, vp) for vp in _chain(vps, one, more)]
    return out


def parts(tree):
    """A requirement's clauses: {"feat", "cond", "trig", "resp"}, None for a clause the form has not. "resp" is
    the list of the response's conjuncts (`responses`)."""
    out = dict.fromkeys(("feat", "cond", "trig", "resp"))
    out.update(zip(FORMS.get(tree[0], ()), tree[1:]))
    if out["resp"] is not None:
        out["resp"] = responses(out["resp"])
    return out


def logic_only(trees):
    """True when every statement of a group is ubiquitous and holds a resource: the group has no scenario."""
    if not trees:
        return False
    for tree in trees:
        resp = parts(tree)["resp"]
        if tree[0] != "Ubiq" or not resp or any(p != "Shall" or vp[0] not in RESOURCE_VPS for p, _, vp in resp):
            return False
    return True


def _quote(value):
    if isinstance(value, str):
        return '"%s"' % value.replace("\\", "\\\\").replace('"', '\\"')
    return str(value)


def show(tree):
    """The tree written as GF writes an expression."""
    if not isinstance(tree, tuple):
        return _quote(tree)
    if len(tree) == 1:
        return tree[0]
    return " ".join([tree[0]] + [show(a) if not isinstance(a, tuple) or len(a) == 1 else "(%s)" % show(a)
                                 for a in tree[1:]])
