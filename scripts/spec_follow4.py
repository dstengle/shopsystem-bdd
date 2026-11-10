"""What may follow where grammar 4 stopped in a refused line (the CNL 4 design, I10): GF's completion of the tokens
before it, each candidate kept only when the line's prefix with it still parses with the code literals read as
spec_grammar4 reads them, and written as the terms of the vocabulary it is a form of (a kind's noun in either
number, a verb's form, an actor, an attribute). Words that are no term (a determiner, a comma) are left out."""
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


def terms(concrete, vocab, tokens, at, trees):
    """The terms that may follow tokens[:at], in order of their spelling; `trees(tokens)` is spec_grammar4's parse
    of a token list, ([], len(tokens)) for one that stops at its end."""
    import pgf
    import spec_grammar
    try:
        found = concrete.complete(spec_grammar._gf_text(tokens[:at]) + " ")
        candidates = sorted({token for _, token, _, _ in found})
    except pgf.ParseError:
        return []
    names = spellings(vocab)
    out = []
    for token in candidates:
        if token not in names or names[token] in out:
            continue
        parsed, stop = trees(tokens[:at] + [token])
        if parsed or stop == at + 1:
            out.append(names[token])
    return out
