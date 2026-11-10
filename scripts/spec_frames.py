"""Verb frames (b82, `.shop/records/2026-11-07-verb-frames/design.md`): what a verb takes, read from its glossary
entry, and the lines and entries that do not keep to it.

A verb (a `(verb)` entry, an event) names its frame on a `Frame:` field, a clause in the order it is read, the kinds (or
actors) as glossary terms:

    - **return** (verb): Frame: `feed` returns video to caller.      subject, object, recipient
    - **request** (verb): Frame: caller requests video.               subject, object
    - **end** (verb): Frame: session ends.                            no object

A preposition right after the verb is the verb's, its object after it (b106, design call 1):

    - **subscribe** (verb): Frame: viewer subscribes to channel.       subject, preposition, object

`frame(term, names)` reads one, `misread` says why one does not read; `problems(lexicon)` gives v_t11 (a verb with no
`Frame:`), v_t13 (a `Frame:` that does not read, naming the word it could not read) and v_t12 (a
condition whose definition names with "the" a kind other than its own: a relation between two kinds written as a
condition). A noun fills a role when its kind (or the actor) is the frame's or a kind of it (`below`: `Kind of:` of
kinds and actors). The grammar types a verb's object, recipient and trigger subject (spec_typed_verbs), so a line
that breaks a frame stops GF: spec_frames_refusal names the verb where it stopped; `guard` checks the subject of a
`shall` against the frames of its verbs.
"""
import difflib
import re
from collections import namedtuple

Frame = namedtuple("Frame", "subject object recipient prep", defaults=(None,))
# the words that, right after a verb in its frame, are the verb's preposition before its object
PREPOSITIONS = {"to", "for", "from", "on", "onto", "in", "into", "at", "with", "about", "of", "by", "over", "under",
                "through", "after", "before", "against", "upon", "without"}
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


def read(term, names, said=None):
    """(Frame, None) of an event entry whose (first) `Frame:` reads, else (None, (the word it could not read, the role
    it reads it as)); (None, None) when the entry gives no `Frame:`. A preposition after the verb is the verb's
    (`Frame: viewer subscribes to channel.`): the object comes after it. `said` reads another of its frames."""
    text = " ".join((term.frame if said is None else said).split())
    if not text:
        return None, None
    verb = s3(term)
    at = (" %s " % text).find(" %s " % verb)
    if at < 1:
        return None, (text, "verb %s after its subject" % verb)
    subject, rest = _noun(text[:at - 1], names), text[at - 1 + len(verb) + 1:].strip()
    if subject is None:
        return None, (text[:at - 1], "subject")
    if not rest:
        return Frame(subject, None, None), None
    first, _, after = rest.partition(" ")
    prep = first if first in PREPOSITIONS and after else None
    rest = after if prep else rest
    obj, to, rec = rest.rpartition(" to ")
    if to and _noun(obj, names) and _noun(rec, names):
        return Frame(subject, _noun(obj, names), _noun(rec, names), prep), None
    if _noun(rest, names):
        return Frame(subject, _noun(rest, names), None, prep), None
    if to and _noun(obj, names):
        return None, (rec, "recipient")
    return None, (obj if to and _noun(rec, names) else rest, "object")


def frame(term, names):
    """The Frame of an event entry, or None when it has none or it does not read: its subject, object and recipient
    each one of `names` (the lexicon's kinds and actors), and the preposition the verb takes before its object."""
    return read(term, names)[0]


def frames(term, names):
    """Every `Frame:` of a verb's entry that reads, in order: the several frames of one meaning."""
    return [f for f in (read(term, names, said)[0] for said in term.frames) if f]


def misread(term, names):
    """Why a verb's `Frame:` (the first of its frames that does not read) does not read, naming the word it could not
    read and what it expected there; None when each reads or the entry gives no `Frame:` (v_t11)."""
    why = next((w for w in (read(term, names, said)[1] for said in term.frames or (term.frame,)) if w), None)
    if why is None:
        return None
    word, role = why
    if role.startswith("verb"):
        return 'the Frame: does not read at "%s": it expects its subject, then the %s' % (word, role)
    near = difflib.get_close_matches(word, sorted(names), 3)
    return 'the Frame: does not read at "%s": the verb\'s %s is a kind or an actor of the glossary%s' % (
        word, role, " (nearest: %s)" % ", ".join(near) if near else "")


def names(lexicon, outer=frozenset()):
    """The kinds and actors a frame may name: the lexicon's, and `outer` (spec_rgl_vocab.outer, b199)."""
    return lexicon.kind_names() | {t.term for t in lexicon.of("actor")} | outer


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


def overlapping(lexicon):
    """The verbs with two entries (two senses) whose frames take, in every slot, the same kind or one kind under the
    other (v_t15): no line's kinds would tell the senses apart. Frames that fill different slots do not overlap."""
    known, under, out = names(lexicon), below(lexicon), set()
    near = lambda a, b: a == b or a in under.get(b, ()) or b in under.get(a, ())
    senses = {}
    for t in lexicon.of("event"):
        senses.setdefault(t.term, []).append(frames(t, known))
    for verb, entries in senses.items():
        for i, mine in enumerate(entries):
            for theirs in entries[i + 1:]:
                if any(all(near(a, b) if a and b else a == b for a, b in zip(f[:3], g[:3]))
                       for f in mine for g in theirs):
                    out.add(verb)
    return out


def problems(lexicon, outer=frozenset()):
    """v_t11, v_t12, v_t13 (a `Frame:` that does not read), v_t14 (a verb with no aspect) and v_t15 (two senses
    that overlap) as (code, term, message), and v_t4 for an actor whose `Kind of:` names no kind."""
    known, kinds, out = names(lexicon, outer), lexicon.kind_names() | outer, []
    out += [("v_t14", t.term, "%s: the verb's entry says neither state nor action: write (verb, state) or (verb, "
             "action)" % t.where) for t in lexicon.of("event") if not t.aspect]
    out += [("v_t15", v, "two entries of the verb %s take, in every slot, the same kind or one kind under the "
             "other: their kinds do not tell the senses apart" % v) for v in sorted(overlapping(lexicon))]
    out += [("v_t4", t.term, "%s: Kind of: %s is not a kind" % (t.where, t.supertype)) for t in lexicon.of("actor")
            if t.supertype and t.supertype not in kinds]
    for t in lexicon.of("event"):
        why = misread(t, known)
        if why:
            out.append(("v_t13", t.term, "%s: %s" % (t.where, why)))
        elif frame(t, known) is None:
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
    for n in list(out):
        seen, at = {n}, up.get(n)
        while at and at not in seen:
            out.setdefault(at, {at}).add(n)
            seen.add(at)
            at = up.get(at)
    return out


def _of(lexicon):
    """{event id: (term, Frame or None)} and {kind or actor id: its name}, kept while the lexicon is."""
    hit = _frames.get(id(lexicon))
    if hit is None or hit[0] is not lexicon:
        ids, known = lexicon.ids(), names(lexicon)
        named = {ids[t.key]: t.term for t in lexicon.terms if t.category in ("kind", "actor")}
        verbs = {}
        for t in lexicon.of("event"):     # a verb's first sense, the one the codified-1 grammar reads
            verbs.setdefault(ids[t.key], (t, frame(t, known)))
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
