"""A context's codified spec read once (design-r3 §3, §6): its lexicon's vocabulary, its codified capabilities (a drafted
file in `extra` replacing the capability of its name), every requirement and universal condition parsed and
translated into facts (`spec_facts`), the requirements that do not parse with their refusals, and the lexicon's
domain facts.

A capability file that says `language: codified-2` is read through grammar 4 (CNL 4's call 15, I12a): each line
parsed (spec_grammar4), its logical form (spec_lf) translated into the same facts (spec_lf_facts), a line a reading
rule refuses or the translation has no facts of among the refused; both kinds of file feed one check. A context whose
`spec/index.md` says `language: codified-2` takes its vocabulary from its layered lexicon, packs included, and reads
its universal conditions in grammar 4 too.

`load(root, extra=())` is cached in the process by the state of the files it reads: `spec/**/*.md` under `root`, the
files of `extra` and the plugin's `grammar/*.gf` (each path with its mtime_ns and size).
"""
import contextlib
from collections import namedtuple
from pathlib import Path

import spec_facts
import spec_grammar
import spec_grammar4
import spec_lexicon
import spec_lf
import spec_lf_facts
import spec_lf_ids
import spec_lf_read
import spec_logic_vocab
import spec_read
import spec_rgl_vocab

GRAMMAR = Path(__file__).resolve().parent.parent / "grammar"
Statement = namedtuple("Statement", "id capability group tree")
Context = namedtuple("Context", "vocab caps statements facts refused domain")
_CACHE = {}


def _stamp(paths):
    out = []
    for p in paths:
        try:
            st = p.stat()
        except OSError:
            out.append((str(p), None, None))
            continue
        out.append((str(p), st.st_mtime_ns, st.st_size))
    return tuple(out)


def fingerprint(root, extra=()):
    root = Path(root).resolve()
    spec = sorted((root / "spec").glob("**/*.md"))
    return (str(root), _stamp(spec), _stamp([Path(p).resolve() for p in extra]),
            _stamp(sorted(GRAMMAR.glob("*.gf"))))


MARKERS = (spec_read.MARKER, spec_grammar4.MARKER)


def _caps(root, extra):
    """{name: capability} of the codified capabilities, and the names of those that say `language: codified-2`."""
    caps, four = {}, set()
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")) + [Path(p) for p in extra]:
        if spec_read.codified(path, MARKERS):
            cap = spec_read.capability(path, MARKERS)
            caps[cap.name] = cap
            if spec_read.codified(path, (spec_grammar4.MARKER,)):
                four.add(cap.name)
            else:
                four.discard(cap.name)
    return caps, four


def _define(root, lex, vocab):
    """`spec_facts.define` for each condition whose sentence parses as a `Def`."""
    for term in lex.of("condition"):
        text = lex.definition(term)
        try:
            tree = spec_grammar.parse(root, text, grammar="Def").tree if text else None
        except spec_grammar.GrammarError:
            return
        if tree and tree[0] in vocab.def_funs:
            spec_facts.define(vocab, tree)


def _memo(fn):
    """`fn(root)` once per resolved root; a call with more arguments goes through."""
    seen = {}

    def call(root, *args, **kwargs):
        if args or kwargs:
            return fn(root, *args, **kwargs)
        key = Path(root).resolve()
        if key not in seen:
            seen[key] = fn(root)
        return seen[key]
    return call


@contextlib.contextmanager
def _once():
    """`spec_lexicon.read` and `spec_grammar.sources` memoised by root while one context is read: `spec_grammar.parse`
    reads the lexicon three times a line and writes the generated GF sources again, which on a whole spec is most
    of the read. The files do not change under one read; both are restored after it."""
    saved = spec_lexicon.read, spec_grammar.sources
    spec_lexicon.read, spec_grammar.sources = _memo(saved[0]), _memo(saved[1])
    try:
        yield
    finally:
        spec_lexicon.read, spec_grammar.sources = saved


def _read(root, extra):
    with _once():
        return _translate(root, extra)


class _Four:
    """Grammar 4's side of one read: its vocabulary, compiled once, and the check's names of its words."""

    def __init__(self, root, marked):
        self.root, self.marked, self.rgl, self.ids = root, marked, None, None

    def facts(self, ident, text):
        """(the tree and facts of a codified-2 line, None) or (None, its refusal)."""
        if self.rgl is None:
            self.rgl = spec_grammar4.load(self.root)[0]
            lex = spec_rgl_vocab.lexicon(self.root)
            self.ids = spec_lf_ids.Ids(spec_logic_vocab.Vocab(lex, self.rgl.kinds), lex, self.rgl.kinds)
        parsed = spec_grammar4.parse(self.root, text)
        why = parsed.refusal or spec_lf_read.refusal(self.rgl, parsed.tree)
        if why:
            return None, why
        try:
            return (parsed.tree, spec_lf_facts.translate(self.ids, ident, spec_lf.form(self.rgl, parsed.tree))), None
        except ValueError as err:
            return None, "refused: %s" % err


def _vocab(root, four):
    """The logic's Vocab: of the layered lexicon and grammar 4's kinds when `spec/index.md` says codified-2."""
    if not four.marked:
        lex = spec_lexicon.read(root)
        vocab = spec_logic_vocab.Vocab(lex)
        _define(root, lex, vocab)
        return vocab
    lex = spec_rgl_vocab.lexicon(root)
    return spec_logic_vocab.Vocab(lex, spec_rgl_vocab.read(root).kinds)


def _translate(root, extra):
    four = _Four(root, spec_grammar4.marked(root))
    vocab = _vocab(root, four)
    caps, fours = _caps(root, extra)
    statements, refused, facts = [], {}, {}
    lines = [(name, "%s#%s" % (name, g.id), "%s#%s" % (name, r.id), r.text)
             for name, cap in sorted(caps.items()) for g in cap.groups for r in g.requirements]
    lines += [(None, None, u.id, u.text) for u in spec_read.universal(root)]
    for cap, group, ident, text in lines:
        if cap in fours or (cap is None and four.marked):
            found, why = four.facts(ident, text)
            if found:
                statements.append(Statement(ident, cap, group, found[0]))
                facts[ident] = found[1]
            else:
                refused[ident] = why
            continue
        parsed = spec_grammar.parse(root, text)
        if parsed.tree:
            statements.append(Statement(ident, cap, group, parsed.tree))
            facts[ident] = spec_facts.translate(vocab, ident, parsed.tree)
        else:
            refused[ident] = parsed.refusal
    domain = spec_logic_vocab.domain(vocab) + spec_facts.def_facts(vocab)
    return Context(vocab, caps, statements, facts, refused, domain)


def load(root, extra=()):
    """The Context of the spec at `root`, with the drafted files of `extra` laid over it."""
    extra = tuple(str(p) for p in extra or ())
    key = (str(Path(root).resolve()), extra)
    stamp = fingerprint(root, extra)
    hit = _CACHE.get(key)
    if hit and hit[0] == stamp:
        return hit[1]
    ctx = _read(root, extra)
    _CACHE[key] = (stamp, ctx)
    return ctx
