"""The refusal of a line grammar 4 stopped in, by the frames of the verb of its clause (the CNL 4 design, I10;
spec_frames_refusal's twin on spec_rgl_vocab's frames): a verb short of the object or the recipient its frames take,
a noun of a kind no frame of it takes in its subject, object or recipient slot, and a passive, which grammar 4 does not
have, naming the verb whose subject it leaves out.

A frame's object is its first piece with no fixed words before its kind; its recipient a piece after "to"."""
from spec_frames import s3
from spec_frames_refusal import participle

# the words a noun phrase may start with before its noun: a verb's form after one of them is a noun
DETS = {"a", "an", "the", "every", "no", "its", "only"}
# where a clause starts: a verb before one of these is not the verb of the clause grammar 4 stopped in
BOUNDARY = {",", ".", "shall", "when", "while", "if", "then", "where", "and", "or", "not"}
ENDS = {".", ",", "and", "or"}


def _forms(vocab):
    """[(tokens of a verb form, its Verb)], the longest first."""
    out = [(form.split(), v) for v in vocab.verbs for form in {s3(v.term), v.term.term}]
    return sorted(out, key=lambda x: -len(x[0]))


def _verb_at(vocab, tokens, at):
    """(start, end, Verb) of the verb of the clause grammar 4 stopped in at token `at`, or None."""
    forms = _forms(vocab)
    for j in range(at, -1, -1):
        for form, v in forms if not (j and tokens[j - 1] in DETS) else ():
            if tokens[j:j + len(form)] == form and (j == at or j + len(form) <= at):
                return j, j + len(form), v
        if j < at and tokens[j] in BOUNDARY:
            return None
    return None


def _head(vocab, tokens, i):
    """The kind of the first noun (or actor) in tokens[i:] before the clause ends, or None."""
    words = sorted([(w.split(), k) for k, spellings in vocab.nouns.items() for w in spellings] +
                   [(a.split(), k) for a, k in vocab.actors], key=lambda x: -len(x[0]))
    for j in range(i, len(tokens)):
        if tokens[j] in BOUNDARY:
            return None
        for form, kind in words:
            if tokens[j:j + len(form)] == form:
                return kind
    return None


def _slot(frame, fixed):
    """The kind of a frame's piece after the fixed words `fixed` (() for its object), or None."""
    return next((kind for words, kind in frame[1] if words == fixed and kind), None)


def _said(v):
    return "; ".join(" ".join(text.split()) for text in v.term.frames)


def refusal(vocab, tokens, at):
    """Why grammar 4 stopped at token `at` (the end of the line when it ran out), naming the verb of the clause it
    stopped in, or None when no verb's frame explains it."""
    at = min(at, len(tokens) - 1)
    within = lambda slot, kind: kind is None or any(s in vocab.ancestors(kind) for s in slot)
    after = _verb_at(vocab, tokens, at + 1) if at + 1 < len(tokens) else None
    if after and after[0] == at + 1:        # stopped at the subject's noun, the verb right after it
        subjects = [f[0] for f in after[2].frames]
        if not within(subjects, _head(vocab, tokens, at)):
            return "refused: the verb %s takes as its subject %s or a kind of it: %s" % (
                after[2].term.term, " or ".join(subjects), _said(after[2]))
    hit = _verb_at(vocab, tokens, at)
    if hit is None:
        return passive(vocab, tokens, at)
    start, end, v = hit
    takes = "refused: the verb %s takes %%s: %s" % (v.term.term, _said(v))
    objects = [k for k in (_slot(f, ()) for f in v.frames) if k]
    recipients = [k for k in (_slot(f, ("to",)) for f in v.frames) if k]
    if at == end and tokens[at] in ENDS:
        return takes % "an object" if objects and all(_slot(f, ()) for f in v.frames) else None
    to = [j for j in range(end, at + 1) if tokens[j] == "to"] if recipients else []
    if to:
        head = _head(vocab, tokens, to[-1] + 1)
        return None if within(recipients, head) else takes % (
            "as its recipient %s or a kind of it" % " or ".join(recipients))
    head = _head(vocab, tokens, end)
    if objects and not within(objects, head):
        return takes % ("as its object %s or a kind of it" % " or ".join(objects))
    if tokens[at] in ENDS and recipients and all(_slot(f, ("to",)) for f in v.frames):
        return takes % "a recipient"
    return passive(vocab, tokens, at)


def passive(vocab, tokens, at):
    """The refusal of the clause at token `at` when it is a passive ("a file is not written"): grammar 4 has none,
    and the verb's frame names a subject the passive leaves out. None when the clause is no passive."""
    start = max([j for j in range(at) if tokens[j] in BOUNDARY - {"not"}], default=-1) + 1
    end = next((j for j in range(at, len(tokens)) if tokens[j] in BOUNDARY - {"not"}), len(tokens))
    for j in range(start, end - 1):
        k = j + 2 if tokens[j + 1] == "not" else j + 1
        for v in vocab.verbs if tokens[j] in ("is", "are") else ():
            form = participle(v.term).split()
            if tokens[k:k + len(form)] == form:
                return "refused: the verb %s takes a subject, which a passive leaves out: %s" % (v.term.term, _said(v))
    return None
