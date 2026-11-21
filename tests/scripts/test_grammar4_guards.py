"""Guards on grammar 4's size and parse time (b441), so that a generator that multiplies is caught before a release.

Grammar 4's Context is generated from a context's vocabulary (spec_rgl), and a generator that writes a fun per pair
of things (b437's `K_Obj_S_O`, a fun per gap and kind, made 44.5% of the compiled grammar's productions) grows it with
the square of the kinds, and GF's parse time with it. The guards read the generated Context.gf of this repository and
of the construct catalogue's contexts, with no compile:

- the funs taking a VPSlash, ClSlash or RS (a gap, a slashed clause, a relative clause) at most `SLASH_PER_KIND` a
  kind;
- the whole grammar's funs at most `FUNS_PER_KIND` a kind;
- spec_rgl_np.senses' funs, 2A(A-1) for A attribute entries sharing a word (79,600 at A = 200), at most `SENSES`;

and, compiled, the parse of a fixed set of lines within `BUDGET` seconds, parsed once more before it fails.

The line set parses in 1.6 s alone. `LOADED` is the slowest parse measured under load (b442, 2026-11-21, 32 CPUs):
the whole suite under `python3 -m pytest -n 32` took 6.1 s (load average 20), and seven such suites at once in one
worktree, as `work batch done` runs seven tasks' suites, took 5.3 s to 18.1 s over two rounds of seven (load average
220 to 254). Twice `LOADED` reaches the 28.6 s of the grammar before b437, so `BUDGET` is not doubled: it sits between
`LOADED` and 28.6 s, and a parse over it is retried once, so a passing load does not fail the guard while a grammar
that multiplies, slower than 28.6 s under any load, fails both.

The grammar before b437's factoring had, in this repository, 1480 funs taking a slash category for 218 kinds (6.8 a
kind) and 8929 funs (41.0 a kind), and parsed the line set in 28.6 s; after it, 820 (3.8 a kind), 7824 (35.9 a kind)
and 1.5 s. A construct that adds funs a kind may raise a bound, as a change of its own, never to let a multiplying
generator through.
"""
import json
import pathlib
import re
import sys
import time
from types import SimpleNamespace

import spec_gf
import spec_grammar4
import spec_rgl
import spec_rgl_np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
CONSTRUCTS = REPO / "grammar" / "corpus" / "constructs"
ROOTS = {"repository": REPO, "constructs": CONSTRUCTS, "constructs/request": CONSTRUCTS / "request"}
# the lines b437 kept with their logical forms: every tenth of this repository's, in id order, is the line set
FORMS = REPO / "tests" / "scripts" / "fixtures" / "grammar4-factored" / "forms.json"

SLASHED = ("VPSlash", "ClSlash", "RS")
SLASH_PER_KIND = 5
FUNS_PER_KIND = 40
SENSES = 400
LOADED = 18.1
BUDGET = 25.0
SENSE = re.compile(r"^t_\w+_\d+_(CmpT|SameAs)_t_\w+_\d+$")


def signatures(srcs):
    """[(fun, [its argument categories' lincats])] of the generated Context."""
    head = srcs["ContextEng.gf"].split("\n  lin\n")[0]
    lincats = dict(re.findall(r"^\s+(\w+) = (.+?) ;$", head, re.MULTILINE))
    body = srcs["Context.gf"].split("\n  fun\n", 1)[1]
    return [(name, [lincats.get(cat.strip(), cat.strip()) for cat in typ.split("->")[:-1]])
            for name, typ in re.findall(r"^\s+(\w+) : (.+?) ;$", body, re.MULTILINE)]


def oversized(vocab, srcs):
    """The guards a grammar's sources break, each said with its count and bound; [] when none."""
    kinds, funs = len(vocab.kinds), signatures(srcs)
    slashed = [name for name, args in funs if set(args) & set(SLASHED)]
    senses = [name for name, _ in funs if SENSE.match(name)]
    return [said for said, count, bound in (
        ("funs taking %s" % "/".join(SLASHED), len(slashed), SLASH_PER_KIND * kinds),
        ("funs", len(funs), FUNS_PER_KIND * kinds),
        ("senses' funs", len(senses), SENSES)) if count > bound
        for said in ["%d %s for %d kinds, over %d" % (count, said, kinds, bound)]]


def fired(found):
    """The names of the guards `oversized` said broke, in its order, without the counts a context's size gives."""
    return [said.split(" for ")[0].split(" ", 1)[1] for said in found]


def test_each_context_s_grammar_is_within_its_bounds():
    assert {name: oversized(*spec_grammar4.sources(root)) for name, root in ROOTS.items()} == {
        name: [] for name in ROOTS}


def multiplying(per):
    """noun_phrases that also write `per(w, vocab)`'s funs, as a generator that multiplies would."""
    def write(w, vocab):
        states = spec_rgl_np.noun_phrases(w, vocab)
        per(w, vocab)
        return states
    return write


def generated(root, per):
    """(vocab, sources) of `root` with `per`'s funs written beside the generated ones."""
    vocab, srcs = spec_grammar4.sources(root)
    srcs.update(spec_rgl.modules(vocab, multiplying(per), spec_grammar4._clauses))
    return vocab, srcs


def a_gap_per_pair_of_kinds(w, vocab):
    """A fun per gap and kind, as `K_Obj_S_O` was before b437: here a gap of each kind on the noun of each kind."""
    for o in vocab.kinds:
        w.cat("%s_Gap_Guard" % spec_rgl.kid(o), "VPSlash")
        for k in vocab.kinds:
            w.fun("%s_Obj_%s_Guard" % (spec_rgl.kid(k), spec_rgl.kid(o)),
                  "%s_Gap_Guard -> %s_CN" % (spec_rgl.kid(o), spec_rgl.kid(k)), "x", "x")


def test_the_guards_catch_a_fun_per_gap_and_kind():
    found = oversized(*generated(CONSTRUCTS, a_gap_per_pair_of_kinds))
    assert fired(found) == ["funs taking VPSlash/ClSlash/RS", "funs"]


def test_the_guards_catch_a_fun_per_pair_of_values():
    """A fun per pair of the funs of a kind's values: the whole grammar's bound, with no slash category in it."""
    def per(w, vocab):
        for k in vocab.kinds:
            for n in range(60):
                w.fun("%s_Pair_Guard_%d" % (spec_rgl.kid(k), n), "%s_NP -> Cond" % spec_rgl.kid(k), "x", "x")
    found = oversized(*generated(CONSTRUCTS, per))
    assert fired(found) == ["funs"]


def test_the_senses_guard_catches_two_hundred_entries_of_one_word():
    """spec_rgl_np.senses over 200 attribute entries of the word "status": 2A(A-1) = 79,600 funs."""
    w, entry = spec_rgl.Writer(), SimpleNamespace(term="status")
    spec_rgl_np.senses(w, SimpleNamespace(attributes=[(entry, ["thing"])] * 200))
    vocab, srcs = spec_grammar4.sources(CONSTRUCTS)
    srcs["Context.gf"] = srcs["Context.gf"].replace("\n  fun\n", "\n  fun\n%s\n" % "\n".join(w.funs), 1)
    # 79,600 beside the catalogue's own; the whole grammar's bound breaks too
    assert fired(oversized(vocab, srcs)) == ["funs", "senses' funs"]


def line_set():
    """Every tenth line of this repository kept in FORMS, in id order: a fixed line set."""
    kept = json.loads(FORMS.read_text())["repository"]
    return [kept[rid]["line"] for rid in sorted(kept)[::10]]


def parse_time(root, lines):
    """Seconds GF takes to parse `lines` in `root`'s compiled grammar, its parse cache passed over."""
    vocab, gram = spec_grammar4.load(root)
    words = {w.replace(" ", spec_rgl.TOKEN) for w in vocab.words}
    start = time.perf_counter()
    for line in lines:
        spec_grammar4._gf_trees(gram, words, spec_gf.tokenise(line))
    return time.perf_counter() - start


def test_the_line_set_parses_within_its_budget():
    toolchain.require()
    lines = line_set()
    assert len(lines) == 42
    assert LOADED < BUDGET < 28.6
    # a parse over the budget is retried once: a load passes, a grammar that multiplies fails both
    assert parse_time(REPO, lines) <= BUDGET or parse_time(REPO, lines) <= BUDGET
