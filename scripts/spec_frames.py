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
condition). `s3` is a verb's third person singular, which grammar 4 reads its forms by.
"""
import difflib
import re
from collections import namedtuple

# prep: the verb's preposition before its object; oblique: the one before its recipient ("records thing in file");
# fixed: the fixed phrase before the object of a verb naming an operation ("lists the characters of note", b796)
Frame = namedtuple("Frame", "subject object recipient prep oblique fixed", defaults=(None, "to", None))
# what fixed words after the verb may be, said when a frame of them does not read (b796)
FIXED = ("words of no kind after the verb read as a fixed phrase before the object, or as the whole object, on a verb "
         "naming an operation")
# what a frame of a context with a domain model names its noun phrases by (b811)
SLOTS = "a frame names its slots in angle brackets, each a kind, an actor or a parameter of its operation"
# where a frame stands in its entry (b840): what follows it would be read into it
ENDS = "a Frame: is the last thing of its entry, after its gloss, with no text but another Frame: after it"
# the words that, right after a verb in its frame, are the verb's preposition before its object
PREPOSITIONS = {"to", "for", "from", "on", "onto", "in", "into", "at", "with", "about", "of", "by", "over", "under",
                "through", "after", "before", "against", "upon", "without"}


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
    (`Frame: viewer subscribes to channel.`): the object comes after it; a recipient follows the object behind any
    preposition (`Frame: agent records thing in file.`); a verb naming an operation may take a fixed phrase of no kind
    in place of its object (`Frame: <actor> lists the notes.`, the domain contract design §4.2) or before it
    (`Frame: <actor> lists the characters of <note>.`, as grammar 4 reads it, b796). `said` reads another of its
    frames."""
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
    split = _recipient(rest, names)
    if split:
        return Frame(subject, split[0], split[2], prep, split[1]), None
    obj, to, rec = rest.rpartition(" to ")
    if _noun(rest, names):
        return Frame(subject, _noun(rest, names), None, prep), None
    if term.operation and not any(_noun(w, names) for w in rest.split()):     # a fixed object: "lists the notes"
        return Frame(subject, None, None), None
    fixed = _fixed(rest, names) if term.operation else None
    if fixed:
        return Frame(subject, fixed[1], None, None, "to", " ".join(filter(None, (prep, fixed[0])))), None
    if to and _noun(obj, names):
        return None, (rec, "recipient")
    return None, (obj if to and _noun(rec, names) else rest, "object")


def _fixed(rest, names):
    """(fixed phrase, object) of the words after a verb that are words of no kind, then a kind: "the characters of
    note"; None when they are not."""
    words = rest.split()
    for j in range(1, len(words)):
        obj = _noun(" ".join(words[j:]), names)
        if obj:
            return None if any(_noun(w, names) for w in words[:j]) else (" ".join(words[:j]), obj)
    return None


def _recipient(rest, names):
    """(object, preposition, recipient) of the words after a verb (and its own preposition) that are an object and
    a recipient behind any preposition, the last that splits them into two kinds; None when none does."""
    words = rest.split()
    for j in range(len(words) - 2, 0, -1):
        obj, rec = _noun(" ".join(words[:j]), names), _noun(" ".join(words[j + 1:]), names)
        if words[j] in PREPOSITIONS and obj and rec:
            return obj, words[j], rec
    return None


def frame(term, names):
    """The Frame of an event entry, or None when it has none or it does not read: its subject, object and recipient
    each one of `names` (the lexicon's kinds and actors), and the preposition the verb takes before its object."""
    return read(term, names)[0]


def frames(term, names):
    """Every `Frame:` of a verb's entry that reads, in order: the several frames of one meaning."""
    return [f for f in (read(term, names, said)[0] for said in term.frames) if f]


def misread(term, names, shown=False):
    """Why a verb's `Frame:` (the first of its frames that does not read) does not read, naming the word it could not
    read and what it expected there, and, `shown`, the frame as its entry writes it (b796), each up to the end of its
    sentence (b826); None when each reads or
    the entry gives no `Frame:` (v_t11). A word the frame could not read that is no one word is given no nearest
    names, and what fixed words after the verb may be in their place. A frame that takes no noun phrase (no slot in
    angle brackets naming a kind, an actor or a parameter, spec_vocabulary_terms' `slotless`, b811) does not read,
    nor one that does not end its entry (spec_lexicon's `unended`) or names a slot that refers to none of them
    (`unslotted`, b840), each named."""
    if term.unended:
        return 'the Frame: "%s." does not end its entry, "%s." follows it: %s' % (*term.unended[0], ENDS)
    if term.slotless:
        return 'the Frame: "%s." takes no noun phrase: %s' % (_sentence(term.slotless[0]), SLOTS)
    if term.unslotted:
        return 'the Frame: "%s." names the slot <%s>, which refers to no kind, no actor and no parameter: %s' % (
            _sentence(term.unslotted[0][0]), term.unslotted[0][1], SLOTS)
    said = term.frames or (term.frame,)
    at, why = next(((i, w) for i, w in enumerate(read(term, names, f)[1] for f in said) if w), (None, None))
    if why is None:
        return None
    word, role = _sentence(why[0]), why[1]
    head = 'the Frame: "%s." ' % _sentence((term.written or said)[at]) if shown else "the Frame: "
    if role.startswith("verb"):
        return '%sdoes not read at "%s": it expects its subject, then the %s' % (head, word, role)
    if " " in word:
        return '%sdoes not read at "%s": the verb\'s %s is a kind or an actor of the glossary; %s' % (
            head, word, role, FIXED)
    near = difflib.get_close_matches(word, sorted(names), 3)
    return '%sdoes not read at "%s": the verb\'s %s is a kind or an actor of the glossary%s' % (
        head, word, role, " (nearest: %s)" % ", ".join(near) if near else "")


def _sentence(text):
    """A frame's text up to the end of its first sentence: the gloss after a `Frame:` is no part of it (b826)."""
    return re.split(r"\.\s", text, maxsplit=1)[0]


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
    senses = {}
    for t in lexicon.of("event"):
        senses.setdefault(t.term, []).append(frames(t, known))
    for verb, entries in senses.items():
        for i, mine in enumerate(entries):
            for theirs in entries[i + 1:]:
                if overlap(mine, theirs, under):
                    out.add(verb)
    return out


def overlap(mine, theirs, under, top=()):
    """Whether two senses' frames take, in some frame of each, the same kind or one under the other in every slot
    (`under`: `below`'s), a kind of `top` above every kind (the base kind `thing`, b847)."""
    near = lambda a, b: a == b or a in top or b in top or a in under.get(b, ()) or b in under.get(a, ())
    return any(f.fixed == g.fixed and all(near(a, b) if a and b else a == b for a, b in zip(f[:3], g[:3]))
               for f in mine for g in theirs)


def problems(lexicon, outer=frozenset()):
    """v_t11, v_t12, v_t13 (a `Frame:` that does not read), v_t14 (a verb with no aspect) and v_t15 (two senses
    that overlap) as (code, term, message), and v_t4 for an actor whose `Kind of:` names no kind."""
    known, kinds, out = names(lexicon, outer), lexicon.kind_names() | outer, []
    out += [("v_t14", t.term, "%s: the verb's entry says neither state nor action: write (verb, state) or (verb, "
             "action)" % t.where) for t in lexicon.of("event") if not t.aspect]
    out += [("v_t15", v, "two entries of the verb %s take, in every slot, the same kind or one kind under the "
             "other: their kinds do not tell the senses apart" % v) for v in sorted(overlapping(lexicon))]
    out += [("v_t4", t.term, "%s: Kind of: %s is not a kind" % (t.where, t.supertype)) for t in lexicon.of("actor")
            if t.supertype and t.supertype not in kinds and t.label != "artifact"]     # artifact: the CLI pack's
    for t in lexicon.of("event"):
        why = misread(t, known, shown=True)
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
