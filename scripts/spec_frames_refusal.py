"""The refusal of a line GF stopped in, by the frame of the verb of its clause (b82, b85, b106; spec_frames reads
the frames): `refusal` names the verb and the role the line breaks, or the preposition it leaves out; `passive` names
the verb of a passive with no agent, whose frame has a subject the line leaves out."""
import re

from spec_frames import below, frame, names, s3

# the words a noun phrase may start with before its noun: a refusal at the noun after them is the verb's
DETS = {"a", "an", "the", "every", "no", "its", "only", "one", "at", "most", "to"}
# where a clause starts: a verb before one of these is not the verb of the clause GF stopped in
BOUNDARY = {",", ".", "shall", "when", "while", "if", "then", "where", "and", "or", "not"}
ENDS = {".", ",", "and", "or"}


def _forms(lexicon):
    """[(tokens of a verb form, its entry)] of every verb, the longest first."""
    import spec_typed
    out = []
    for t in lexicon.of("event"):
        for form in set(spec_typed.event_forms(t)):
            out.append((spec_typed.tokens(form), t))
    return sorted(out, key=lambda x: -len(x[0]))


def _verb_at(tokens, at, lexicon):
    """(start, end, entry) of the verb of the clause GF stopped in at token `at`, or None."""
    forms = _forms(lexicon)
    for j in range(at, -1, -1):
        noun = j and tokens[j - 1] in DETS - {"to"}       # "every commit": the kind, not the verb
        for form, t in forms if not noun else ():
            if tokens[j:j + len(form)] == form and (j == at or j + len(form) <= at):
                return j, j + len(form), t
        if j < at and tokens[j] in BOUNDARY:
            return None
    return None


def _head(tokens, i, lexicon):
    """The kind whose word (or plural) comes first in tokens[i:], before the clause ends; None when none does."""
    import spec_typed
    words = sorted(((spec_typed.tokens(w), t.term) for t in lexicon.of("kind")
                    for w in {t.term, t.plural or spec_typed.plural(t.term)}), key=lambda x: -len(x[0]))
    for j in range(i, len(tokens)):
        if tokens[j] in BOUNDARY:
            return None
        for form, kind in words:
            if tokens[j:j + len(form)] == form:
                return kind
    return None


def _role(found, tokens, start, end, at, lexicon):
    """The role of the verb at tokens[start:end] a refusal at token `at` breaks, or None when it is not the verb's."""
    under, here = below(lexicon), tokens[at]
    if at == start:
        return "subject"
    if at == end and here in ENDS:
        return "object?" if found.object else None
    if not found.object:
        return "none" if at == end else None
    to = [j for j in range(end, at + 1) if tokens[j] == found.oblique] if found.recipient else []
    if to:
        head = _head(tokens, to[-1] + 1, lexicon)
        return "recipient" if head and head not in under.get(found.recipient, ()) else None
    head = _head(tokens, end, lexicon)
    if head and head not in under.get(found.object, ()):
        return "object"
    return "recipient?" if found.recipient and here in ENDS else None


def refusal(tokens, at, lexicon):
    """Why GF stopped at token `at` of a line (the end of the line when it ran out), naming the verb of the clause
    it stopped in, or None when no verb's frame explains it."""
    at = min(at, len(tokens) - 1)
    hit = _verb_at(tokens, at, lexicon)
    if hit is None:
        return passive(tokens, at, lexicon)
    start, end, term = hit
    found = frame(term, names(lexicon))
    verb = term.term
    if found is None:
        return "the verb %s has no frame in the glossary (Frame: <subject> %s <object>.)" % (verb, s3(term))
    said = " ".join(term.frame.split())
    if found.prep and at == end and tokens[at] != found.prep:
        return "the verb %s takes its object after %s: %s" % (verb, found.prep, said)
    role = _role(found, tokens, start, end, at, lexicon)
    if role == "object?":
        return "the verb %s takes an object: %s" % (verb, said)
    if role == "recipient?":
        return "the verb %s takes a recipient: %s" % (verb, said)
    if role == "none":
        return "the verb %s takes no object: %s" % (verb, said)
    if role:
        return "the verb %s takes as its %s %s or a kind of it: %s" % (verb, role, getattr(found, role), said)
    return passive(tokens, at, lexicon)


def participle(term):
    """The past participle of a verb's term: its second `Forms:`, else its first word with -ed."""
    if len(term.forms) == 2:
        return term.forms[1]
    head, _, rest = term.term.partition(" ")
    head = head + "d" if head.endswith("e") else head[:-1] + "ied" if re.search(r"[^aeiou]y$", head) else head + "ed"
    return (head + " " + rest).strip()


def passive(tokens, at, lexicon):
    """Why the clause GF stopped in at token `at` is refused when it is a passive with no agent ("a file is not
    written", b85): the verb's frame names a subject the passive leaves out. None when the clause has none."""
    import spec_typed
    start = max([j for j in range(at) if tokens[j] in BOUNDARY - {"not"}], default=-1) + 1
    end = next((j for j in range(at, len(tokens)) if tokens[j] in BOUNDARY - {"not"}), len(tokens))
    conditions = {t.term for t in lexicon.of("condition")}
    for j in range(start, end - 1):
        k = j + 2 if tokens[j + 1] == "not" else j + 1
        for t in lexicon.of("event") if tokens[j] in ("is", "are") else ():
            form = spec_typed.tokens(participle(t))
            if tokens[k:k + len(form)] == form and " ".join(form) not in conditions:
                return "the verb %s takes a subject, which a passive leaves out: %s" % (
                    t.term, " ".join(t.frame.split()))
    return None
