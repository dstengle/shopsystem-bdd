"""Grammar 4 of a context (the CNL 4 design, I7a): the base grammar `grammar/Base.gf` with the module `Context`
spec_rgl generates from the context's vocabulary, compiled against the RGL and cached as spec_grammar caches grammar
3, a line parsed in it, linearised back, and the refusal of a line it does not parse, naming a verb that does not
agree in number with its subject or whose aspect is not the one its clause takes (a state verb in a trigger, an
action verb in a While clause; call 3).

`model parse` reads a line in grammar 4 when `spec/index.md` says `language: codified-2` (`marked`); every other
reader keeps grammar 3 until the switch (I19). A line with more than one tree is refused here; one meaning or refused
is I9's.
"""
import difflib
import hashlib
from dataclasses import dataclass, field
from itertools import islice
from pathlib import Path

import model_parse
import spec_grammar
import spec_rgl
import spec_rgl_vocab
import tools_grammar

MARKER = "codified-2"
GRAMMAR = "Context"
BASE = ("Base.gf", "BaseEng.gf")
LIMIT = 50
_loaded = {}


@dataclass
class Parse:
    """`tree` (a pgf expression's text) when the line has exactly one tree; else `refusal` says why, and `trees`
    holds the trees of an ambiguous line."""
    tree: str = None
    refusal: str = None
    trees: list = field(default_factory=list)


def marked(root):
    """True when `spec/index.md` of the context at `root` says `language: codified-2`."""
    path = Path(root) / "spec" / "index.md"
    data, _ = model_parse.frontmatter(path.read_text()) if path.is_file() else ({}, "")
    return str(data.get("language", "")).strip() == MARKER


def sources(root):
    """(vocab, {file name: text}) of grammar 4: the base grammar's files and the generated Context."""
    vocab = spec_rgl_vocab.read(root)
    out = {name: (spec_grammar.GRAMMARS / name).read_text() for name in BASE}
    out.update(spec_rgl.modules(vocab))
    return vocab, out


def load(root):
    """(vocab, the compiled grammar as a pgf.PGF), compiled once per set of sources and RGL release."""
    import pgf
    if not tools_grammar.rgl_path():
        raise spec_grammar.GrammarError("gf-rgl is missing: run `python3 scripts/tools install`")
    vocab, srcs = sources(root)
    sha = hashlib.sha256(("rgl %s\0" % tools_grammar.RGL_RELEASE + "".join(
        "%s\0%s\0" % kv for kv in sorted(srcs.items()))).encode()).hexdigest()[:32]
    if sha not in _loaded:
        target = spec_grammar._cache() / sha / ("%s.pgf" % GRAMMAR)
        if not target.is_file():
            spec_grammar._compile(srcs, sha, GRAMMAR)
        _loaded[sha] = pgf.readPGF(str(target))
    return vocab, _loaded[sha]


def _literal(words, text):
    """GF's String callback: a code is one backticked token that is no word of the vocabulary (a value's, an
    actor's), as spec_grammar reads one; a bare word is never a code."""
    read = spec_grammar._literal(words, text)

    def code(cat, start):
        found = read(cat, start)
        return found if found and text[start:].lstrip().startswith("`") else None
    return code


def _trees(gram, words, tokens):
    """(the distinct trees of a parse, or [] and the index of the token GF stopped at)."""
    import pgf
    text = spec_grammar._gf_text(tokens)
    try:
        parses = islice(gram.languages[GRAMMAR + "Eng"].parse(
            text, callbacks=[("String", _literal(words, text))]), LIMIT)
        return list(dict.fromkeys(str(e) for _, e in parses)), None
    except pgf.ParseError as err:
        return [], (len(tokens) if err.incomplete else spec_grammar._position(tokens, err.offset))


def disagreeing(gram, vocab, tokens, at):
    """The verb whose form at token `at` would parse in the other number: its term, or None."""
    words = {w.replace(" ", spec_rgl.TOKEN) for w in vocab.words}
    for v in vocab.verbs:
        singular, plural = spec_rgl.spec_frames.s3(v.term), v.term.term
        other = {singular: plural, plural: singular}.get(tokens[at] if at < len(tokens) else None)
        if other and len(other.split()) == 1 and _trees(gram, words, tokens[:at] + [other] + tokens[at + 1:])[0]:
            return v.term.term
    return None


# the aspect a clause takes, by the word that opens it (call 3): a trigger an action, a While clause a state
CLAUSES = {"when": ("action", "a trigger"), "if": ("action", "a trigger"), "while": ("state", "a While clause")}
ASPECT = {"action": "an action", "state": "a state"}


def misaspected(vocab, tokens, at):
    """The refusal of a verb at token `at` whose aspect is not the one its clause takes, or None: the clause is the
    one the nearest When, If or While before it opens."""
    if at is None or at >= len(tokens):
        return None
    clause = next((CLAUSES[w.lower()] for w in reversed(tokens[:at]) if w.lower() in CLAUSES), None)
    for v in vocab.verbs:
        forms = {spec_rgl.spec_frames.s3(v.term).split()[0], v.term.term.split()[0]}
        if clause and tokens[at] in forms and v.aspect != clause[0]:
            return "refused: the verb %s is %s, and %s takes %s" % (v.term.term, ASPECT[v.aspect], clause[1],
                                                                    ASPECT[clause[0]])
    return None


def parse(root, line):
    """One line parsed in grammar 4."""
    vocab, gram = load(root)
    tokens = spec_grammar.tokenise(line)
    words = {w.replace(" ", spec_rgl.TOKEN) for w in vocab.words}
    trees, at = _trees(gram, words, tokens)
    if len(trees) == 1:
        return Parse(tree=trees[0], trees=trees)
    if trees:
        return Parse(refusal="ambiguous: %d trees" % len(trees), trees=trees)
    term = disagreeing(gram, vocab, tokens, at)
    if term:
        return Parse(refusal="refused: the verb %s does not agree in number with its subject" % term)
    aspect = misaspected(vocab, tokens, at)
    if aspect:
        return Parse(refusal=aspect)
    if at >= len(tokens):
        return Parse(refusal="the line ends before its sentence does (after %d tokens)" % len(tokens))
    return Parse(refusal="does not parse at %s (token %d of %d)" % (tokens[at], at + 1, len(tokens)))


def linearise(root, tree):
    """A tree of grammar 4 written back as a line."""
    import pgf
    _, gram = load(root)
    text = gram.languages[GRAMMAR + "Eng"].linearize(pgf.readExpr(tree))
    return spec_grammar.detokenise(text.split(" "))


def hint(root, line):
    """For a refused line: the longest prefix that parsed and the vocabulary's words nearest the token after it."""
    vocab, gram = load(root)
    tokens = spec_grammar.tokenise(line)
    _, at = _trees(gram, {w.replace(" ", spec_rgl.TOKEN) for w in vocab.words}, tokens)
    if at is None or at >= len(tokens):
        return {"prefix": spec_grammar.normalise(line), "near": []}
    return {"prefix": spec_grammar.detokenise(tokens[:at]) if at else "",
            "near": difflib.get_close_matches(tokens[at], sorted(vocab.words), n=5)}
