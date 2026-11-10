"""A command's options in the trigger (b240, construct #12; the CNL 4 design, section 7.2's `run(e, agent, command,
options)`), one translation of the CLI pack's run with its options in each place a line is read.

The grammar (spec_rgl and the pack's frames of run): "runs C with the `--x` option", "with the `--x` and `--y`
options" (`K_NamedAnd`, codes before a plural noun), "with the `--x` option on a K", "with the `--x` option set to v"
(`k_option_SetTo`, v a code or a thing) and "without the `--x` option" (the option not given).

- the form: an "and" list in a run's `with` or `without` slot is one run with each member (`together`, a role for
  each), never a run for each as "and" gives of any other argument; an option's argument the atom
  `argument(option, v)` (`np`, `show`);
- the check: the command a run runs is its code with each option given and its argument when that is a code; an
  option not given is left out, so the line pairs with every line on the command alone; a thing an option is set to
  is what the run is on (`command`);
- the steps: a slot of several options one argument ("the `--x` and `--y` options" of codes, else a list with
  and: `arg`), an option with its argument said with it (`said`), the thing it is set to brought in by a Given
  (`given`), and a When step's options read back for its handler (`read`: `options`, each option given with its
  argument or None, and `without`, each option not given).
"""
import spec_rgl
from spec_lf_core import NP, Atom, NPList

PRED = "argument"
ROLES = ("with", "without")
OPTION = spec_rgl.OPTION


# --- the form ------------------------------------------------------------------------------------------------------
def codes(tree):
    """The CodeLit trees of a `Codes` tree: `a` and `b`, `a`, `b` and `c`."""
    if tree[0] == "CodeTwo":
        return [tree[1], tree[2]]
    return [tree[1]] + codes(tree[2])


def np(st, kind, rest, a):
    """The noun phrase of `K_NamedAnd` (an "and" list of the codes' referents) or of `k_option_SetTo` (the option's
    referent, its argument read first and said of it by `argument`); None of any other fun."""
    import spec_lf_np as nps  # here: spec_lf_np reads this module's funs
    if rest == "NamedAnd":
        return NPList("and", [nps.code(st, kind, c) for c in codes(a[0])])
    if rest != "SetTo":
        return None
    option, value = nps.code(st, kind, a[0]), nps.np(st, a[2])
    if hasattr(value, "members"):     # an NPList
        raise ValueError("the logical form has no translation of an option set to a list")
    return NP(option.ref, "fixed", [Atom(PRED, (option.ref, value.ref))], deps=[value], new=False)


def together(st, n, m, found):
    """The noun phrases of frame m of verb n with an "and" list in a run's with or without slot made one argument."""
    v = st.names.verbs[n]
    if v.term.term != "run":
        return found
    labels = [" ".join(words) for words, kind in v.frames[m - 1][1] if kind is not None]
    return [NPList("together", x.members) if label in ROLES and isinstance(x, NPList) and x.op == "and" else x
            for label, x in zip(labels, found)]


def show(atom, term):
    return "%s(%s, %s)" % (PRED, term(atom.args[0]), term(atom.args[1]))


# --- the check -----------------------------------------------------------------------------------------------------
def arguments(body):
    """{option: its argument} of a trigger's `argument` atoms."""
    return {a.args[0]: a.args[1] for a in body if isinstance(a, Atom) and a.pred == PRED}


def command(roles, args):
    """(the command's text with each option given and its code argument, the referents the run is on)."""
    words, on = [roles[1][1].value], []
    for r in roles[2:]:
        if len(r) != 2 or r[0] == "without":
            continue
        if r[0] != "with":
            on.append(r[1])
            continue
        if r[1].value is None:
            raise ValueError("no translation of an option with no code")
        words.append(r[1].value)
        value = args.get(r[1])
        if value is not None and value.origin in ("constant", "parameter"):
            words.append(value.value)
        elif value is not None:
            on.append(value)
    return " ".join(words), on


# --- the steps -----------------------------------------------------------------------------------------------------
def labels(roles):
    """The labels of an atom's roles after its subject, a label repeated in a row said once (one slot)."""
    out = []
    for r in roles[1:]:
        if not out or r[0] != out[-1] or len(r) != 2:
            out.append(r[0])
    return out


def slots(roles):
    """The referents of an atom's slots in order, the referents of a slot said more than once a tuple."""
    out, last = [], None
    for r in roles[1:]:
        if len(r) != 2:
            last = None
            continue
        if r[0] == last and r[0] in ROLES:
            out[-1] = (out[-1] if isinstance(out[-1], tuple) else (out[-1],)) + (r[1],)
        else:
            out.append(r[1])
        last = r[0]
    return out


def arg(reader, refs, slot):
    """The `K_Arg` tree of several referents in one slot: codes before the plural noun, else a list with and."""
    K = spec_rgl.kid(slot)
    if all(r.value is not None and r.origin in ("constant", "parameter") and r not in reader.arguments for r in refs):
        tree = ("CodeTwo", ("CodeLit", refs[-2].value), ("CodeLit", refs[-1].value))
        for r in reversed(refs[:-2]):
            tree = ("CodeMore", ("CodeLit", r.value), tree)
        return (K + "_NamedAnd", tree, (K + "_UseN", (K + "_n",)))
    nps = (K + "_Two", reader.np(refs[-2], slot), reader.np(refs[-1], slot))
    for r in reversed(refs[:-2]):
        nps = (K + "_More", reader.np(r, slot), nps)
    return (K + "_And", nps)


def slot_arg(reader, ref, slot):
    """The `K_Arg` tree of a run's slot as the line says it, or None of a slot that holds no option: several options
    (`arg`), an option with its argument (`said`), an option named by its code before its noun ("the `--json`
    option")."""
    if isinstance(ref, tuple):
        return arg(reader, ref, slot)
    if ref in reader.arguments:
        return (spec_rgl.kid(slot) + "_One", said(reader, ref, slot))
    if ref.kind != OPTION or ref.value is None or ref.origin not in ("constant", "parameter"):
        return None
    K = spec_rgl.kid(OPTION)
    tree = (K + "_Named", ("CodeLit", ref.value), (K + "_UseN", (K + "_n",)))
    return (spec_rgl.kid(slot) + "_One", (K + "_Simple", tree) if slot == OPTION else
            ("%s_Up_%s" % (K, spec_rgl.kid(slot)), tree))


def said(reader, ref, slot):
    """The `K_NP` tree of an option with its argument: "the `--every` option set to `5`"."""
    K = spec_rgl.kid(OPTION)
    tree = (K + "_SetTo", ("CodeLit", ref.value), (K + "_UseN", (K + "_n",)), reader.arg(reader.arguments[ref], "thing"))
    return (K + "_Simple", tree) if slot == OPTION else ("%s_Up_%s" % (K, spec_rgl.kid(slot)), tree)


def given(reader, atom):
    """No Given of an argument but the thing it is, brought in at its first mention."""
    option, value = atom.args
    reader.arguments[option] = value
    if value.origin in ("constant", "parameter") or value in reader.known:
        return []
    reader.known.add(value)
    K = spec_rgl.kid(value.kind)
    return [(K + "_Given", (K + "_n",), ("NameLit", reader.name(value)))]


def read(names, text, vp):
    """(options, without) of a run's verb phrase in a When step: each option given as (its code, its argument's text
    or None), each option not given its code; `text` writes a tree out."""
    options, without = [], []
    fun = vp[0]
    if not fun.startswith("e_run_"):
        return options, without
    n, m = (int(x) for x in fun.rsplit("_", 2)[1:])
    pieces = [" ".join(words) for words, kind in names.verbs[n].frames[m - 1][1] if kind is not None]
    for label, a in zip(pieces, vp[1:]):
        if label in ROLES:
            for code, value in _options(a, text):
                (options.append((code, value)) if label == "with" else without.append(code))
    return options, without


def _options(tree, text):
    if not isinstance(tree, tuple):
        return []
    K = spec_rgl.kid(OPTION)
    if tree[0] == K + "_Named":
        return [(tree[1][1], None)]
    if tree[0] == K + "_SetTo":
        return [(tree[1][1], text(tree[3]))]
    if tree[0] == K + "_NamedAnd":
        return [(c[1], None) for c in codes(tree[1])]
    return [o for a in tree[1:] for o in _options(a, text)]
