"""Verb frames (b82, `.shop/records/2026-11-07-verb-frames/design.md`): what a verb takes, read from its glossary
entry, and the lines and entries that do not keep to it.

A verb (a `(verb)` entry, an event) names its frame on a `Frame:` field, a clause in the order it is read, the kinds (or
actors) as glossary terms:

    - **return** (verb): Frame: `feed` returns video to caller.      subject, object, recipient
    - **request** (verb): Frame: caller requests video.               subject, object
    - **end** (verb): Frame: session ends.                            no object

`frame(term, names)` reads one; `problems(lexicon)` gives v_t11 (a verb with no frame that reads) and v_t12 (a
condition whose definition names with "the" a kind other than its own: a relation between two kinds written as a
condition). A noun fills a role when its kind (or the actor) is the frame's or a kind of it (`below`: `Kind of:` of
kinds and actors). The grammar types a verb's object, recipient and trigger subject (spec_typed_verbs), so a line
that breaks a frame stops GF: `refusal` names the verb where it stopped and the role it breaks; `guard` checks the
subject of a `shall` against the frames of its verbs; `passive` names the verb of a passive with no agent, whose
frame has a subject the line leaves out (b85).
"""
import re
from collections import namedtuple

Frame = namedtuple("Frame", "subject object recipient")
# the words a noun phrase may start with before its noun: a refusal at the noun after them is the verb's
DETS = {"a", "an", "the", "every", "no", "its", "only", "one", "at", "most", "to"}
# where a clause starts: a verb before one of these is not the verb of the clause GF stopped in
BOUNDARY = {",", ".", "shall", "when", "while", "if", "then", "where", "and", "or", "not"}
ENDS = {".", ",", "and", "or"}
_frames = {}


def s3(term):
    """The third person singular of a verb's term: its `Forms:` first, else its first word inflected."""
    if term.forms:
        return term.forms[0]
    head, _, rest = term.term.partition(" ")
    if re.search(r"(s|sh|ch|x|z|o)$", head):
        head += "es"
    elif re.search(r"[^aeiou]y$", head):
        head = head[:-1] + "ies"
    else:
        head += "s"
    return (head + " " + rest).strip()


def _noun(text, names):
    text = " ".join(text.split())
    if text in names:
        return text
    bare = re.sub(r"^(?:a|an|the)\s+", "", text)
    return bare if bare in names else None


def frame(term, names):
    """The Frame of an event entry, or None when it has none or it does not read: its subject, object and recipient
    each one of `names` (the lexicon's kinds and actors)."""
    text = " ".join(term.frame.split())
    if not text:
        return None
    verb = s3(term)
    at = (" %s " % text).find(" %s " % verb)
    if at < 1:
        return None
    subject, rest = _noun(text[:at - 1], names), text[at - 1 + len(verb) + 1:].strip()
    if subject is None:
        return None
    if not rest:
        return Frame(subject, None, None)
    obj, to, rec = rest.rpartition(" to ")
    if to and _noun(obj, names) and _noun(rec, names):
        return Frame(subject, _noun(obj, names), _noun(rec, names))
    return Frame(subject, _noun(rest, names), None) if _noun(rest, names) else None


def names(lexicon):
    return lexicon.kind_names() | {t.term for t in lexicon.of("actor")}


def _blank(text):
    return re.sub(r"`[^`]*`|\"[^\"]*\"", "x", text)


def relational(term, kinds):
    """The other kind a condition's definition names with "the", or None: at each "the", the longest kind the words
    after it begin with ("the request line" names a request line, not a request)."""
    import spec_lexicon
    text = _blank(spec_lexicon.gloss(term.text))
    longest = sorted(kinds, key=len, reverse=True)
    for found in re.finditer(r"\bthe ", text, re.IGNORECASE):
        rest = text[found.end():]
        kind = next((k for k in longest if re.match(r"%s(?![\w-])" % re.escape(k), rest)), None)
        if kind and kind not in term.kinds:
            return kind
    return None


def problems(lexicon):
    """v_t11 and v_t12 as (code, term, message), and v_t4 for an actor whose `Kind of:` names no kind."""
    known, kinds, out = names(lexicon), lexicon.kind_names(), []
    out += [("v_t4", t.term, "%s: Kind of: %s is not a kind" % (t.where, t.supertype)) for t in lexicon.of("actor")
            if t.supertype and t.supertype not in kinds]
    for t in lexicon.of("event"):
        if frame(t, known) is None:
            out.append(("v_t11", t.term, "%s: the verb's entry gives no Frame: naming the kinds of its subject and "
                        "object, or `Frame: <subject> %s.` when it takes none" % (t.where, s3(t))))
    for t in lexicon.of("condition"):
        other = relational(t, kinds)
        if other:
            out.append(("v_t12", t.term, "%s: the condition names the %s: a relation between two kinds is a verb "
                        "between them" % (t.where, other)))
    return out


def supers(lexicon):
    """{kind or actor: the kind its `Kind of:` names}."""
    return {t.term: t.supertype for t in lexicon.terms if t.category in ("kind", "actor") and t.supertype}


def below(lexicon):
    """{kind or actor: itself and every kind and actor under it, at any depth}."""
    up = supers(lexicon)
    out = {n: {n} for n in names(lexicon)}
    for n in out:
        seen, at = {n}, up.get(n)
        while at and at not in seen:
            out.setdefault(at, {at}).add(n)
            seen.add(at)
            at = up.get(at)
    return out


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
    to = [j for j in range(end, at + 1) if tokens[j] == "to"] if found.recipient else []
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
    role, said = _role(found, tokens, start, end, at, lexicon), " ".join(term.frame.split())
    if role == "object?":
        return "the verb %s takes an object: %s" % (verb, said)
    if role == "recipient?":
        return "the verb %s takes a recipient: %s" % (verb, said)
    if role == "none":
        return "the verb %s takes no object: %s" % (verb, said)
    if role:
        return "the verb %s takes as its %s %s or a kind of it: %s" % (verb, role, getattr(found, role), said)
    return passive(tokens, at, lexicon)


def _of(lexicon):
    """{event id: (term, Frame or None)} and {kind or actor id: its name}, kept while the lexicon is."""
    hit = _frames.get(id(lexicon))
    if hit is None or hit[0] is not lexicon:
        ids, known = lexicon.ids(), names(lexicon)
        named = {ids[t.key]: t.term for t in lexicon.terms if t.category in ("kind", "actor")}
        verbs = {ids[t.key]: (t, frame(t, known)) for t in lexicon.of("event")}
        hit = _frames[id(lexicon)] = (lexicon, verbs, named, below(lexicon))
        if len(_frames) > 16:
            _frames.clear()
            _frames[id(lexicon)] = hit
    return hit[1:]


def _subject(subj, named):
    """The kind or actor a `shall`'s subject names, or None when it names none (a code)."""
    if subj[0] == "ActorSubj":
        return named.get(subj[1][0])
    np = subj[1]
    return named.get(np[0][:-len("_toNP")]) if np[0].endswith("_toNP") else None


def guard(tree, lexicon):
    """Why the subject of a `shall` is not of the kind a frame of its verbs names, naming the verb; None when every
    subject is."""
    import spec_tree
    verbs, named, under = _of(lexicon)
    for node in spec_tree.nodes(tree):
        if node[0] not in ("Shall", "ShallNot"):
            continue
        subject = _subject(node[1], named)
        for vp in spec_tree.nodes(node[2]):
            if subject is None or vp[0] not in ("Do", "DoI", "DoTo"):
                continue
            term, found = verbs.get(vp[1][0], (None, None))
            if found and subject not in under.get(found.subject, ()):
                return "the verb %s takes as its subject %s or a kind of it: %s" % (
                    term.term, found.subject, " ".join(term.frame.split()))
    return None


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
