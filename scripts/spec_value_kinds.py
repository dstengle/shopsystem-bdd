"""The kind of an attribute's values (b257): an attribute entry gives its values as `Values (adjective):` (they read
after "is" as an adjective or a participle: `shaped`, `in-batch`) and `Values (noun):` (any other: a noun, a verb
phrase, a code), or as a plain `Values:` of no declared kind. The short form "x is `v`" (grammar 4's `<t>_<K>_Is`,
`_IsOneOf`, `_IsNoneOf` and `_IsCode`) is good English of an adjective value only, so a line that says it of a noun
value is refused, naming the full form "the T of x is `v`" or "a K whose T is `v`" (`refusal`); a value of no
declared kind keeps 4.0's reading, which `model check` warns of (`w_value_kind`, `undeclared`)."""
import re

KINDS = ("adjective", "noun")
SHORT = re.compile(r"^(t_[a-z0-9_]+?_\d+)_(k_\w+?)_(Is|IsOneOf|IsNoneOf|IsCode)$")
SAID = {"Is": "is %s", "IsCode": "is %s", "IsOneOf": "is one of %s", "IsNoneOf": "is not %s"}


def kind(term, value):
    """`adjective`, `noun`, or "" (no declared kind) of a value of the attribute entry `term`; a code no entry lists
    is a noun of an attribute that declares its values' kinds."""
    declared = dict(term.value_kinds)
    if value in declared:
        return declared[value]
    return "noun" if declared and value not in term.values else ""


def undeclared(term):
    """True of an attribute entry whose values are given with a plain `Values:` and no declared kind."""
    return bool(term.values) and not term.value_kinds


def mixed(term):
    """The problem of an attribute entry that gives a plain `Values:` beside a declared one, or ""."""
    plain = len(term.values) > len(term.value_kinds)
    return "both Values: and Values (adjective|noun):" if plain and term.value_kinds else ""


def _article(word):
    return "an" if word[:1] in "aeiou" else "a"


def values_of(tree, attribute, prefix):
    """The values a short form's tree names: the value funs under it, a code literal's text."""
    fun = tree if isinstance(tree, str) else tree[0]
    if fun.startswith(prefix + "_v_"):
        slug = fun[len(prefix) + 3:]
        return [v for v in attribute.values if re.sub(r"[^a-z0-9]+", "_", v.lower()).strip("_") == slug][:1]
    if isinstance(tree, str):
        return []
    if tree[0] == "CodeLit":
        return [tree[1].strip('"')]
    return [v for a in tree[1:] for v in values_of(a, attribute, prefix)]


def short_forms(tree):
    """Every (fun, polarity, its value subtree) of a short form in a tree (nested lists)."""
    if isinstance(tree, str):
        return []
    found = []
    if SHORT.match(tree[0]):
        neg = len(tree) > 3 and tree[1] == "PNeg"
        found.append((tree[0], neg, tree[-1]))
    return found + [f for a in tree[1:] for f in short_forms(a)]


def refusal(vocab, text):
    """The refusal of a tree's text that says a noun value in the short form, or None."""
    import spec_meaning
    tree = spec_meaning.read(text)
    attributes = {"t_%s_%d" % (re.sub(r"[^a-z0-9]+", "_", t.term.lower()).strip("_") or "x", n): t
                  for n, (t, _) in enumerate(vocab.attributes, 1)}
    kinds = {"k_" + (re.sub(r"[^a-z0-9]+", "_", k.lower()).strip("_") or "x"): k for k in vocab.kinds}
    for fun, neg, values in short_forms(tree):
        T, K, form = SHORT.match(fun).groups()
        t = attributes.get(T)
        named = values_of(values, t, T) if t else []
        nouns = [v for v in named if kind(t, v) == "noun"]
        if nouns:
            return full(t.term, kinds.get(K, K), nouns[0], form, neg, named)
    return None


def full(term, k, value, form, neg=False, named=()):
    """The refusal of the short form of `value`, a noun of the attribute `term` of the kind `k`; `named` the values
    a set names."""
    named = list(named) or [value]
    listed = ", ".join(named[:-1]) + " or " + named[-1] if len(named) > 1 else named[0]
    said = SAID[form] % (listed if form in ("IsOneOf", "IsNoneOf") else value)
    said = said.replace("is ", "is not ", 1) if neg else said
    out = 'refused: %s is a noun, a value of the %s of %s %s: "%s %s %s" does not read; write "the %s of the %s %s"' % (
        value, term, _article(k), k, _article(k), k, said, term, k, said)
    if form in ("IsOneOf", "IsNoneOf"):     # "whose" takes one value
        return out
    return out + ' or "%s %s whose %s %s"' % (_article(k), k, term, said)
