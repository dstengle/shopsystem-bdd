"""What may follow where grammar 4 stopped in a refused line (the CNL 4 design, I10): GF's completion of the tokens
before it, each candidate kept only when the line's prefix with it still parses with the code literals read as
spec_grammar4 reads them, and written as the terms of the vocabulary it is a form of (a kind's noun in either
number, a verb's form, an actor, an attribute). Words that are no term (a determiner, a comma) are left out; when
only such words may follow, the terms that may follow each word among them are given."""
import spec_frames
import spec_rgl


def spellings(vocab):
    """{token: term} of every form a term is spelled with in grammar 4, a multi-word term as one token."""
    out = {}

    def add(text, term):
        out.setdefault(text.replace(" ", spec_rgl.TOKEN), term)
    for kind, (singular, plural) in vocab.nouns.items():
        add(singular, kind)
        add(plural, kind)
    for v in vocab.verbs:
        add(spec_frames.s3(v.term), v.term.term)
        add(v.term.term, v.term.term)
    for term, _ in vocab.actors:
        add(term, term)
    for t, _ in vocab.attributes:
        add(t.term, t.term)
    return out


def _next(concrete, prefix, trees):
    """The tokens GF's completion offers after the token list `prefix` that keep it a prefix of a line."""
    import pgf
    import spec_gf
    try:
        found = concrete.complete(spec_gf.gf_text(prefix) + " ")
        candidates = sorted({token for _, token, _, _ in found})
    except pgf.ParseError:
        return []
    kept = []
    for token in candidates:
        parsed, stop = trees(prefix + [token])
        if parsed or stop == len(prefix) + 1:
            kept.append(token)
    return kept


def terms(concrete, vocab, tokens, at, trees):
    """The terms that may follow tokens[:at], in order of their spelling; when only words that are no term may (a
    preposition, "to"), the terms that may follow each of them. `trees(tokens)` is spec_grammar4's parse of a token
    list, ([], len(tokens)) for one that stops at its end."""
    names = spellings(vocab)
    first = _next(concrete, tokens[:at], trees)
    found = [names[t] for t in first if t in names]
    if not found:
        found = [names[t] for word in first if word.isalpha()
                 for t in _next(concrete, tokens[:at] + [word], trees) if t in names]
    return list(dict.fromkeys(found))
