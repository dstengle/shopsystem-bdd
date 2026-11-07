"""A context's requirement grammar: compile and cache (design §11.3), tokenise (§9.4), parse with the guards
(§9.3), linearise, and the hint a refusal carries (§15).

The core grammars are the plugin's `grammar/*.gf`; `Lex` and `Typed` are generated from the context's lexicon
(`spec_typed`). A compiled PGF is cached under `${XDG_CACHE_HOME:-~/.cache}/shopsystem-bdd/pgf/<sha>/`, the sha
being that of every source, and is written by a rename so two processes compiling at once both get a whole one.
"""
import difflib
import hashlib
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from itertools import islice
from pathlib import Path

import spec_frames
import spec_lexicon
import spec_parse_cache
import spec_tree
import spec_typed
import spec_typed_def
import spec_typed_verbs
import tools_grammar

GRAMMARS = Path(__file__).resolve().parent.parent / "grammar"
LIMIT = 2000  # trees read from one parse before the guards; a literal slot reads any token
_loaded = {}
_contexts = {}  # (spec_lexicon.read, root) -> (state of the files, (lexicon, sources, sha))


class GrammarError(Exception):
    """The grammar could not be built: no gf, or gf refused the sources."""


@dataclass
class Parse:
    """`tree` is set when exactly one tree is left after the guards; otherwise `refusal` says why (no tree, or
    "ambiguous: n trees" with `trees` holding them). `before` counts the trees before the guards."""
    tree: tuple = None
    refusal: str = None
    trees: list = field(default_factory=list)
    before: int = 0


def gf_binary():
    """GF's binary, by `tools_grammar.gf_binary`, the one lookup: `$SHOPSYSTEM_GF`, the install path, then a `gf`
    on PATH that says it is Grammatical Framework."""
    return tools_grammar.gf_binary()


def tokenise(line):
    """A line's tokens: words, a backticked or double-quoted span whole, punctuation alone; the first word in lower
    case (the grammar writes it so)."""
    out = spec_typed.tokens(line)
    if out and out[0][:1].isupper() and (out[0][1:].islower() or len(out[0]) == 1):
        out[0] = out[0][0].lower() + out[0][1:]
    return out


def detokenise(tokens):
    text = " ".join(tokens).replace(spec_typed.PLACEHOLDER, " ")
    for mark in ",.;:":
        text = text.replace(" " + mark, mark)
    return text[:1].upper() + text[1:]


def normalise(line):
    """The line as the grammar writes it: single spaces, no space before punctuation, a capital first letter."""
    return detokenise(tokenise(line))


def _gf_text(tokens):
    return " ".join(t.replace(" ", spec_typed.PLACEHOLDER) for t in tokens)


def _cache():
    return Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "shopsystem-bdd" / "pgf"


def sources(root, lex=None):
    """{file name: text} of every GF source of the context's grammars: the core files and the generated ones. The
    lexicon is read only when `lex` is not given."""
    lex = lex or spec_lexicon.read(root)
    out = {p.name: p.read_text() for p in sorted(GRAMMARS.glob("*.gf"))}
    out.update(spec_typed.modules(lex))
    out.update(spec_typed_def.modules(lex))
    return out


def _run_gf(gf, directory, concrete):
    return subprocess.run([gf, "-make", "--output-dir=" + str(directory), concrete], cwd=directory,
                          capture_output=True, text=True)


def _compile(srcs, sha, grammar):
    gf = gf_binary()
    if not gf:
        raise GrammarError("no gf: run `python3 scripts/tools install`, or set $SHOPSYSTEM_GF")
    base = _cache()
    base.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(dir=base, prefix=".tmp-"))
    try:
        for name, text in srcs.items():
            (tmp / name).write_text(text)
        done = _run_gf(gf, tmp, "%sEng.gf" % grammar)
        if not (tmp / ("%s.pgf" % grammar)).is_file():
            raise GrammarError("gf could not compile %s:\n%s%s" % (grammar, done.stdout[-2000:], done.stderr[-2000:]))
        final = base / sha
        try:
            os.rename(tmp, final)
            tmp = None
        except OSError:
            if not (final / ("%s.pgf" % grammar)).is_file():
                os.replace(tmp / ("%s.pgf" % grammar), final / ("%s.pgf" % grammar))
    finally:
        if tmp is not None:
            shutil.rmtree(tmp, ignore_errors=True)


def _state(root):
    files = sorted((root / "spec").glob("**/*.md")) + sorted(GRAMMARS.glob("*.gf"))
    return tuple((str(p), st.st_mtime_ns, st.st_size) for p, st in ((p, p.stat()) for p in files))


def _context(root):
    """(lexicon, GF sources, their sha) of the context, read again when a file under `spec/` or a grammar source
    changes, or when `spec_lexicon.read` is replaced (a stub, or `spec_context`'s memo): a whole spec's parses read
    the lexicon once, not three times a line. The sha names the compiled PGFs and the cached parses."""
    root = Path(root).resolve()
    key, state = (spec_lexicon.read, str(root)), _state(root)
    hit = _contexts.get(key)
    if hit is None or hit[0] != state:
        lex = spec_lexicon.read(root)
        srcs = sources(root, lex)
        sha = hashlib.sha256("".join("%s\0%s\0" % kv for kv in sorted(srcs.items())).encode()).hexdigest()[:32]
        if len(_contexts) >= 16:
            _contexts.clear()
        hit = _contexts[key] = (state, (lex, srcs, sha))
    return hit[1]


def load(root, grammar="Req"):
    """The context's compiled grammar (`"Req"`, `"Steps"` or `"Def"`) as a `pgf.PGF`, compiled once per set of sources."""
    import pgf
    _, srcs, sha = _context(root)
    if "%sEng.gf" % grammar not in srcs:
        raise GrammarError("no grammar %s under %s" % (grammar, GRAMMARS))
    if (sha, grammar) not in _loaded:
        target = _cache() / sha / ("%s.pgf" % grammar)
        if not target.is_file():
            _compile(srcs, sha, grammar)
        _loaded[(sha, grammar)] = pgf.readPGF(str(target))
    return _loaded[(sha, grammar)]


def _tree(expr, gram):
    """A pgf expression as nested tuples. An argument the English leaves unsaid (the noun phrase of "its status")
    is a metavariable; in a kind's noun-phrase slot it can only be that kind's "it"."""
    unpacked = expr.unpack()
    if not isinstance(unpacked, tuple):
        return unpacked.replace(spec_typed.PLACEHOLDER, " ") if isinstance(unpacked, str) else unpacked
    fun, args = unpacked
    if fun is None:
        return None
    out = [fun]
    for (_, _, typ), arg in zip(gram.functionType(fun).hypos, args):
        sub = _tree(arg, gram)
        if sub is None:
            cat = str(typ)
            sub = (cat[:-3] + "_It",) if cat.startswith("k_") and cat.endswith("_NP") else ("?",)
        out.append(sub)
    return tuple(out)


def _expr(tree):
    import pgf
    if isinstance(tree, tuple):
        return pgf.Expr(tree[0], [_expr(a) for a in tree[1:]])
    return pgf.Expr(tree.replace(" ", spec_typed.PLACEHOLDER) if isinstance(tree, str) else tree)


def _position(tokens, offset):
    """The index of the token at a character offset of the text given to GF."""
    start = 0
    for i, t in enumerate(tokens):
        start += len(t) + 1
        if offset < start:
            return i
    return len(tokens)


def _literal(words, text):
    """GF's String callback: a literal slot reads one token, but not a lexicon word, which the guard would refuse
    there anyway, nor a mark of punctuation, which ends a clause; so a line of many backticked words is not read 3^n ways past LIMIT."""
    import pgf

    def read(_, start):  # offsets count characters
        while start < len(text) and text[start] == " ":
            start += 1
        end = text.find(" ", start)
        end = len(text) if end < 0 else end
        token = text[start:end]
        return None if not token or token in words or token in ",.;:" else (pgf.Expr(token), 0.0, end)
    return read


def _raw(root, tokens, grammar):
    """(trees in their normal form, error index or None) of the parse before the guards; GF's own trees are kept in
    `spec_parse_cache`."""
    lex, _, sha = _context(root)
    text, words = _gf_text(tokens), {w.replace(" ", spec_typed.PLACEHOLDER) for w in lex.words()}
    digest = spec_parse_cache.key(sha, grammar, text, words, LIMIT)
    hit = spec_parse_cache.get(sha, grammar, digest)
    if hit is None:
        hit = _gf_parse(root, tokens, grammar, text, words)
        spec_parse_cache.put(sha, grammar, digest, *hit)
    return [spec_typed_verbs.normal(t) for t in hit[0]], hit[1]


def _gf_parse(root, tokens, grammar, text, words):
    import pgf
    gram = load(root, grammar)
    try:
        parses = islice(gram.languages["%sEng" % grammar].parse(text, callbacks=[("String", _literal(words, text))]),
                        LIMIT)
        return [_tree(e, gram) for _, e in parses], None
    except pgf.ParseError as err:
        return [], (len(tokens) if err.incomplete else _position(tokens, err.offset))


def parse(root, line, grammar="Req"):
    """One line parsed in the context's grammar (`"Req"`, `"Steps"` or `"Def"`), the guards applied. A definition
    (`"Def"`) whose tree says "it" is refused: it names its subject as "the <kind>" (design-r2 §4.3)."""
    tokens = tokenise(line)
    trees, at = _raw(root, tokens, grammar)
    if at is not None:
        why = grammar != "Def" and spec_frames.refusal(tokens, at, _context(root)[0])
        if why:
            return Parse(refusal="refused: %s" % why)
        if at >= len(tokens):
            return Parse(refusal="the line ends before its sentence does (after %d tokens)" % len(tokens))
        return Parse(refusal="does not parse at %s (token %d of %d)" % (tokens[at], at + 1, len(tokens)))
    lex = _context(root)[0]
    words = lex.words()
    kept, reasons = [], []
    for tree in trees:
        reason = ((grammar == "Def" and spec_typed_def.refusal(tree, lex)) or spec_tree.guard(tree, words)
                  or (grammar == "Req" and spec_frames.guard(tree, lex)))
        if reason:
            reasons.append(reason)
        elif tree not in kept:
            kept.append(tree)
    if len(kept) == 1:
        return Parse(tree=kept[0], trees=kept, before=len(trees))
    if not kept:
        # a reason about a literal is the least telling: every token may be read as one
        reasons.sort(key=lambda r: r.startswith(("the code", "the text")))
        return Parse(refusal="refused: %s" % (reasons[0] if reasons else "no tree"), before=len(trees))
    return Parse(refusal="ambiguous: %d trees" % len(kept), trees=kept, before=len(trees))


def linearise(root, tree, grammar="Req"):
    """A tree (in its normal form, spec_typed_verbs) written back as a sentence of the context's grammar."""
    concr = load(root, grammar).languages["%sEng" % grammar]
    tree = spec_typed_verbs.typed(tree, spec_typed_verbs.frames(_context(root)[0]))
    return detokenise(concr.linearize(_expr(tree)).split(" "))


def hint(root, line, grammar="Req"):
    """For a refused line: the longest prefix that parsed, the token after it, and the lexicon words nearest it."""
    tokens = tokenise(line)
    _, at = _raw(root, tokens, grammar)
    if at is None or at >= len(tokens):
        return {"prefix": normalise(line), "token": None, "near": []}
    words = sorted(spec_lexicon.read(root).words())
    prefix = detokenise(tokens[:at]) if at else ""
    if prefix and line.lstrip()[:1].isupper():
        prefix = prefix[0].upper() + prefix[1:]
    return {"prefix": prefix, "token": tokens[at], "near": difflib.get_close_matches(tokens[at], words, n=5)}
