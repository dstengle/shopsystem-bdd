"""A request acts on one thing (b420, design-decision 0111), and the frames of a verb a reading uses: a tree of grammar
4 in which a request, a verb naming an operation of the domain model in a trigger, takes a plural object (a noun
phrase in the plural, or with "every", a count or a number word, or a list joined by "and") in a slot its frame names
a kind of, is no reading of its line (`plural`); spec_grammar4 drops it, and refuses a line with no other reading naming the object and the verb
(`refusal`). Of a line that reads two ways, the frames of one verb its two readings differ by (`frames`), which the
refusal names beside the words.

A tree is spec_meaning's nested lists; a verb's frame is its fun `e_<verb>_<aspect>_<n>_<m>` (spec_rgl) or, with its
parameters, `q_<verb>_<n>_<m>` (spec_rgl_ops), n the verb's entry and m its frame there.
"""
import re

FRAME = re.compile(r"^(?:e_\w+_(?:action|state)|q_\w+)_(\d+)_(\d+)$")
PLURAL_DETS = {"DetPl", "DetThePl", "DetEvery", "DetCount", "DetTwo"}


def _fun(tree):
    return tree if isinstance(tree, str) else tree[0]


def _numbers(name):
    found = FRAME.match(name)
    return (int(found.group(1)), int(found.group(2))) if found else None


def several(arg):
    """True of a slot's argument (`K_Arg`) or noun phrase that is more than one thing."""
    name = _fun(arg)
    if isinstance(arg, str):
        return False
    if name.endswith(("_And", "_NamedAnd", "_Every")):
        return True
    if name.endswith("_Det"):
        return _fun(arg[1]) in PLURAL_DETS
    if name.endswith(("_Or", "_Two", "_More")):
        return any(several(a) for a in arg[1:])
    if re.search(r"_(One|Only|Simple|Up_k_\w+)$", name) or "_By_" in name:
        return several(arg[1])
    return False


def plural(vocab, tree, trigger=False):
    """(the verb's word, the argument's tree) of the first plural object of a request in `tree`, a verb naming an
    operation in a trigger (`<S>_Event`, `<S>_Request`), else None. A response's act of such a verb is no request
    (spec_lf_request) and keeps its plurals: "the toolchain service shall install every analysis tool"."""
    if isinstance(tree, str):
        return None
    trigger = trigger or tree[0].endswith(("_Event", "_Request"))
    numbers = _numbers(tree[0]) if trigger else None
    if numbers and vocab.verbs[numbers[0] - 1].term.operation:
        v = vocab.verbs[numbers[0] - 1]
        slots = [k for _, k in v.frames[numbers[1] - 1][1] if k]
        for arg in tree[1:1 + len(slots)]:
            if several(arg):
                return v.term.term, arg
    for arg in tree[1:]:
        found = plural(vocab, arg, trigger)
        if found:
            return found
    return None


def used(vocab, tree, out=None):
    """The (verb's word, frame text) of each frame `tree` uses, in order."""
    out = [] if out is None else out
    if isinstance(tree, str) or not tree:
        name, args = tree, ()
    else:
        name, args = tree[0], tree[1:]
    numbers = _numbers(name) if isinstance(name, str) else None
    if numbers:
        v = vocab.verbs[numbers[0] - 1]
        texts = v.texts or v.term.frames
        text = texts[numbers[1] - 1] if numbers[1] <= len(texts) else v.term.term
        op = v.term.operation
        out.append((v.term.term, '"%s"%s' % (text, " (%s)" % op if op else "")))
    for a in args:
        used(vocab, a, out)
    return out


def frames(vocab, a, b):
    """The frames of a verb that the two readings `a` and `b` (trees) of the same words differ by, each read in one
    of them: [] when they use the same frames, or no verb of both."""
    one, two = used(vocab, a), used(vocab, b)
    if set(one) == set(two):
        return []
    both = list(dict.fromkeys(one + two))
    words = {w for w, _ in set(one) ^ set(two)}
    return [text for w, text in both if w in words and (w, text) not in set(one) & set(two)]


def refusal(found, linearise):
    """The refusal of a line whose only readings give a request a plural object, `found` the first's (verb, argument)."""
    verb, arg = found
    return ('refused: a request acts on one thing: "%s" is a plural object of %s; say one thing, or the collection '
            "by its frame's own words" % (linearise(arg), verb))
