"""A context's codified spec read once (design-r3 §3, §6): its lexicon's vocabulary, its codified capabilities (a drafted
file in `extra` replacing the capability of its name), every requirement and universal condition parsed and
translated into facts, the requirements that do not parse with their refusals, and the lexicon's domain facts.

Only a capability file that says `language: codified-2` is read, through grammar 4 (CNL 4's call 15, I12a): each line
parsed (spec_grammar4), its logical form (spec_lf) translated into facts (spec_lf_facts), a line a reading rule
refuses or the translation has no facts of among the refused. A file that says codified-1 is no capability of the
context here (`model check` refuses it, naming `migrate upgrade`: v_p0); the universal conditions are read when
`spec/universal.md` says codified-2. The vocabulary is the layered lexicon's, packs included, with grammar 4's kinds.

`load(root, extra=())` is cached in the process by the state of the files it reads: `spec/**/*.md` under `root`, the
files of `extra` and the plugin's `grammar/*.gf` (each path with its mtime_ns and size).
"""
from collections import namedtuple
from pathlib import Path

import spec_grammar4
import spec_language
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


def _caps(root, extra):
    """{name: capability} of the capabilities that say `language: codified-2`, a drafted file replacing its name's."""
    caps = {}
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")) + [Path(p) for p in extra]:
        if spec_read.codified(path, (spec_grammar4.MARKER,)):
            cap = spec_read.capability(path, (spec_grammar4.MARKER,))
            caps[cap.name] = cap
    return caps


class Four:
    """Grammar 4's side of one read: its vocabulary, compiled once, and the check's names of its words; also the
    spec corpus's translation of one line (tests/scripts/test_corpus_spec.py, check 2)."""

    def __init__(self, root):
        self.root, self.rgl, self.ids = root, None, None
        self.lex, kinds = spec_rgl_vocab.lexicon(root), spec_grammar4.sources(root)[0].kinds
        self.vocab = spec_logic_vocab.Vocab(self.lex, kinds)

    def facts(self, ident, text):
        """(the tree and facts of a codified-2 line, None) or (None, its refusal)."""
        if self.rgl is None:
            self.rgl = spec_grammar4.load(self.root)[0]
            self.ids = spec_lf_ids.Ids(self.vocab, self.lex, self.rgl.kinds)
        parsed = spec_grammar4.parse(self.root, text)
        why = parsed.refusal or spec_lf_read.refusal(self.rgl, parsed.tree)
        if why:
            return None, why
        try:
            return (parsed.tree, spec_lf_facts.translate(self.ids, ident, spec_lf.form(self.rgl, parsed.tree))), None
        except ValueError as err:
            return None, "refused: %s" % err


def _read(root, extra):
    four = Four(root)
    caps = _caps(root, extra)
    statements, refused, facts = [], {}, {}
    lines = [(name, "%s#%s" % (name, g.id), "%s#%s" % (name, r.id), r.text)
             for name, cap in sorted(caps.items()) for g in cap.groups for r in g.requirements]
    if spec_language.four(root, universal=True):
        lines += [(None, None, u.id, u.text) for u in spec_read.universal(root)]
    for cap, group, ident, text in lines:
        found, why = four.facts(ident, text)
        if found:
            statements.append(Statement(ident, cap, group, found[0]))
            facts[ident] = found[1]
        else:
            refused[ident] = why
    return Context(four.vocab, caps, statements, facts, refused, spec_logic_vocab.domain(four.vocab))


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
