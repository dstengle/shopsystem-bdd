"""A context's codified spec read once (design-r3 §3, §6): its lexicon's vocabulary, its codified capabilities (a drafted
file in `extra` replacing the capability of its name), every requirement and universal condition parsed and
translated into facts (`spec_facts`), the requirements that do not parse with their refusals, and the lexicon's
domain facts.

`load(root, extra=())` is cached in the process by the state of the files it reads: `spec/**/*.md` under `root`, the
files of `extra` and the plugin's `grammar/*.gf` (each path with its mtime_ns and size).
"""
import contextlib
from collections import namedtuple
from pathlib import Path

import spec_facts
import spec_grammar
import spec_lexicon
import spec_logic_vocab
import spec_read

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


def _caps(root, extra):
    caps = {}
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")) + [Path(p) for p in extra]:
        if spec_read.codified(path):
            cap = spec_read.capability(path)
            caps[cap.name] = cap
    return caps


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


def _translate(root, extra):
    lex = spec_lexicon.read(root)
    vocab = spec_logic_vocab.Vocab(lex)
    _define(root, lex, vocab)
    caps = _caps(root, extra)
    statements, refused = [], {}
    lines = [(name, "%s#%s" % (name, g.id), "%s#%s" % (name, r.id), r.text)
             for name, cap in sorted(caps.items()) for g in cap.groups for r in g.requirements]
    lines += [(None, None, u.id, u.text) for u in spec_read.universal(root)]
    for cap, group, ident, text in lines:
        parsed = spec_grammar.parse(root, text)
        if parsed.tree:
            statements.append(Statement(ident, cap, group, parsed.tree))
        else:
            refused[ident] = parsed.refusal
    facts = {s.id: spec_facts.translate(vocab, s.id, s.tree) for s in statements}
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
