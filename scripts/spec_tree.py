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


def _chain(tree, one, more):
    """The members of a right-recursive list (`One x` / `More x rest`)."""
    out = []
    while isinstance(tree, tuple) and tree[0].endswith(more):
        out.append(tree[1])
        tree = tree[2]
    if isinstance(tree, tuple) and tree[0].endswith(one):
        out.append(tree[1])
    return out


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


def _second_object(tree):
    for node in nodes(tree):
        if node[0] == "DoTo":
            obj = node[3][1] if node[3][0] == "Only" else node[3]
            if obj[0] in ("CodeNP", "QuotedNP"):
                return "a code after a noun phrase names it (the second object of %s is a code)" % node[1][0]
    return None


def _repeats(tree):
    for node in nodes(tree):
        members = []
        if node[0] == "MoreNP":
            members = _chain(node, "OneNP", "MoreNP")
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
    "it" only after a noun phrase of its kind (§9.3), and a code after a noun phrase is its name, not a second
    object. `words` are the lexicon's spellings."""
    return _literals(tree, words) or _repeats(tree) or _anaphora(tree) or _second_object(tree)


def _rebuild(members, one, more):
    tree = (one, members[-1])
    for m in reversed(members[:-1]):
        tree = (more, m, tree)
    return tree


def normal(tree):
    """The tree with its value lists and condition conjunctions in sorted order, so two statements that say the
    same thing in another order compare equal (v15k)."""
    if not isinstance(tree, tuple):
        return tree
    fun = tree[0]
    if fun == "CondAnd" or (fun.startswith("t_") and fun.endswith("_More")):
        one, more = ("CondOne", "CondAnd") if fun == "CondAnd" else (fun[:-5] + "_One", fun)
        members = sorted((normal(m) for m in _chain(tree, one, more)), key=show)
        return _rebuild(members, one, more)
    return (fun,) + tuple(normal(a) for a in tree[1:])


def parts(tree):
    """A requirement's clauses: {"feat", "cond", "trig", "resp"}, None for a clause the form has not."""
    out = dict.fromkeys(("feat", "cond", "trig", "resp"))
    out.update(zip(FORMS.get(tree[0], ()), tree[1:]))
    return out


def logic_only(trees):
    """True when every statement of a group is ubiquitous and holds a resource: the group has no scenario."""
    if not trees:
        return False
    for tree in trees:
        resp = parts(tree)["resp"]
        if tree[0] != "Ubiq" or not resp or resp[2][0] not in RESOURCE_VPS:
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
