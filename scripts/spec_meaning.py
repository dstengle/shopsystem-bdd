"""One meaning, or refused (the CNL 4 design, call 2; I9): a grammar 4 line whose trees all mean one thing keeps the
first of them in a fixed order; a line whose trees mean different things is refused, naming the words that have two
readings.

A tree's meaning is its logical form (spec_lf, I11a) over the context's vocabulary. Without a vocabulary, and to find
the words of a line that read two ways, it is the normalised tree: the tree with the funs that only carry a noun
phrase to its slot left out (`<K>_Simple`, `<K>_One`, `<K>_Up_<A>`), since two trees that differ only there say the
same of the same things.
"""
import re

TOKEN = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+')
CARRIERS = re.compile(r"^k_\w+?_(Simple|One|Up_k_\w+)$")


def read(text):
    """A tree's text as nested lists [fun, arg ...]; a string literal or a bare fun stays a string."""
    stack = [[]]
    for tok in TOKEN.findall(text):
        if tok == "(":
            stack.append([])
        elif tok == ")":
            done = stack.pop()
            stack[-1].append(done if len(done) > 1 else done[0])
        else:
            stack[-1].append(tok)
    out = stack[0]
    return out if len(out) > 1 else out[0]


def write(tree):
    """Nested lists written back as a tree's text."""
    if isinstance(tree, str):
        return tree
    return " ".join([tree[0]] + [w if isinstance(a, str) else "(%s)" % w for a in tree[1:] for w in [write(a)]])


def meaning(tree, vocab=None):
    """The meaning of a tree (its text), as a hashable value: its logical form over `vocab`, or with none the
    normalised tree."""
    if vocab is not None:
        import spec_lf  # imported here: spec_lf reads trees with this module's `read`
        return spec_lf.form(vocab, tree)

    def norm(t):
        if isinstance(t, str):
            return t
        if CARRIERS.match(t[0]) and len(t) == 2:
            return norm(t[1])
        return (t[0],) + tuple(norm(a) for a in t[1:])
    return norm(read(tree))


def fun(tree):
    return tree if isinstance(tree, str) else tree[0]


def split(a, b):
    """The subtree of `a` (nested lists) whose words read two ways: below the last node `a` and `b` share, the one
    argument whose meaning differs, or that node itself when more than one does."""
    while not isinstance(a, str) and not isinstance(b, str) and fun(a) == fun(b) and len(a) == len(b):
        differ = [i for i in range(1, len(a)) if meaning(write(a[i])) != meaning(write(b[i]))]
        if len(differ) != 1:
            return a
        i = differ[0]
        if fun(a[i]) != fun(b[i]):
            return a[i]
        a, b = a[i], b[i]
    return a


def one(trees, vocab=None):
    """(the tree kept, None) when every tree means one thing, else (None, (the subtree's text of the first tree whose
    words read two ways, the number of meanings)). The trees are taken shortest first, then by their text; their
    meanings are logical forms over `vocab` when it is given."""
    ordered = sorted(trees, key=lambda t: (len(t), t))
    of = {t: meaning(t, vocab) for t in ordered}
    meanings = list(dict.fromkeys(of.values()))
    if len(meanings) == 1:
        return ordered[0], None
    first = next(t for t in ordered if of[t] == meanings[0])
    second = next(t for t in ordered if of[t] == meanings[1])
    return None, (write(split(read(first), read(second))), len(meanings))
