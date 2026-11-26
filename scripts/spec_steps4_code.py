"""A code in a generated step said so that the step reads one way (b733, scenarios r48): spec_steps4 writes a
constant or a parameter as its slot's bare code (`S_Code`, "no capability in `registry`"), which the step grammar 4
may read as a code of several kinds (a row `capability | in | K` of each); features generate keeps a step's bare codes
while the step parses to one tree under its keyword (`readings`, the trees features_vocab4 reads it by), else writes
each, one after another, before its referent's kind's noun as the line said it (`K_Named`, "no capability in the
`registry` area") until it does (`one`); a step that still parses more than one way is a TraceError naming it.
"""
import spec_rgl_steps
from spec_rgl import kid
from spec_steps4_boxes import TraceError

# the trees a step is read by under its keyword (features_vocab4's)
READ = {"given": ("SCond", "_Given", "_HoldsBlock", "_HoldsText"), "when": ("STrig",), "then": ("SCond", "_Does")}


def readings(root, keyword, text):
    """The trees of a step's text read under its keyword, example data read as such (b154)."""
    trees = [t for t in spec_rgl_steps.trees(root, text) if t[0].endswith(READ[keyword])]
    data = [t for t in trees if t[0].endswith(("_HoldsBlock", "_HoldsText"))]
    return data or trees


def kinds(forms):
    """{code: its referent's kind} of the constants and parameters of the forms, a code of two kinds left out."""
    out = {}
    for _, form in forms:
        for ref in form.fixed:
            if ref.origin in ("constant", "parameter") and ref.value:
                out[ref.value] = ref.kind if out.get(ref.value, ref.kind) == ref.kind else None
    return {v: k for v, k in out.items() if k}


def _bare(tree, found):
    """Each bare code node `(S_Code, (CodeLit, v))` of a tree, in order."""
    if isinstance(tree, tuple):
        if len(tree) == 2 and str(tree[0]).endswith("_Code") and isinstance(tree[1], tuple) \
                and tree[1][:1] == ("CodeLit",):
            found.append(tree)
        else:
            for t in tree[1:]:
                _bare(t, found)
    return found


def _named(node, kind, vocab):
    """The code of a bare node before its kind's noun, in the node's slot; None when the slot is no kind above it."""
    S, K = node[0][:-len("_Code")], kid(kind)
    if not any(kid(a) == S for a in vocab.ancestors(kind)):
        return None
    inner = (K + "_Named", node[1], (K + "_UseN", (K + "_n",)))
    return (S + "_Simple", inner) if K == S else ("%s_Up_%s" % (K, S), inner)


def _swap(tree, old, new):
    if tree is old:
        return new
    if isinstance(tree, tuple):
        return tuple(_swap(t, old, new) for t in tree)
    return tree


def one(root, vocab, gram, keyword, tree, codes):
    """The text of a step tree that reads one way: its bare codes kept while it does, else named one by one by
    `codes` ({code: kind}); TraceError naming the step when it still reads more than one way."""
    text = spec_rgl_steps.text(gram, tree)
    bare = _bare(tree, [])
    if not bare or len(readings(root, keyword, text)) <= 1:
        return text
    for node in bare:
        new = _named(node, codes[node[1][1]], vocab) if node[1][1] in codes else None
        if new is None:
            continue
        tree = _swap(tree, node, new)
        text = spec_rgl_steps.text(gram, tree)
        if len(readings(root, keyword, text)) <= 1:
            return text
    raise TraceError("the step %r reads more than one way" % text)
