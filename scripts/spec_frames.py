"""Verb frames (b82, `.shop/records/2026-11-07-verb-frames/design.md`): what a verb takes, read from its glossary
entry, and the lines and entries that do not keep to it.

A verb (an `event` entry) names its frame on a `Frame:` field, a clause in the order it is read, the kinds (or
actors) as glossary terms:

    - **return** (event): Frame: `feed` returns video to caller.      subject, object, recipient
    - **request** (event): Frame: caller requests video.               subject, object
    - **end** (event): Frame: session ends.                            no object

`frame(term, names)` reads one; `problems(lexicon)` gives v_t11 (a verb with no frame that reads) and v_t12 (a
condition whose definition names with "the" a kind other than its own: a relation between two kinds written as a
condition), and `guard(tree, lexicon)` the reason a parsed line uses a verb without a noun its frame takes, or with
one it does not take, naming the verb's term.
"""
import re
from collections import namedtuple

Frame = namedtuple("Frame", "subject object recipient")
# the verb funs of `grammar/Req.gf`: (index of the event argument, objects given, recipient given)
USES = {"Do": (1, True, False), "DoI": (1, False, False), "DoTo": (1, True, True), "Happens": (2, True, False),
        "HappensI": (2, False, False)}
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
    """v_t11 and v_t12 as (code, term, message)."""
    known, kinds, out = names(lexicon), lexicon.kind_names(), []
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


def _of(lexicon):
    """{event id: (term, Frame or None)} of a lexicon, kept while the lexicon is."""
    hit = _frames.get(id(lexicon))
    if hit is None or hit[0] is not lexicon:
        ids, known = lexicon.ids(), names(lexicon)
        hit = _frames[id(lexicon)] = (lexicon, {ids[t.key]: (t, frame(t, known)) for t in lexicon.of("event")})
        if len(_frames) > 16:
            _frames.clear()
            _frames[id(lexicon)] = hit
    return hit[1]


def guard(tree, lexicon):
    """Why a tree's verb does not keep to its frame, naming the verb; None when every verb does."""
    import spec_tree
    by_id = _of(lexicon)
    for node in spec_tree.nodes(tree):
        if node[0] not in USES:
            continue
        at, has_object, has_recipient = USES[node[0]]
        term, found = by_id.get(node[at][0], (None, None))
        if term is None:
            continue
        verb = term.term
        if found is None:
            return "the verb %s has no frame in the glossary (Frame: <subject> %s <object>.)" % (verb, s3(term))
        if found.object and not has_object:
            return "the verb %s takes an object: %s %s %s" % (verb, found.subject, s3(term), found.object)
        if not found.object and has_object:
            return "the verb %s takes no object: %s %s" % (verb, found.subject, s3(term))
        if found.recipient and not has_recipient:
            return "the verb %s takes a recipient: %s %s %s to %s" % (verb, found.subject, s3(term), found.object,
                                                                      found.recipient)
        if has_recipient and not found.recipient:
            return "the verb %s takes no recipient: %s %s %s" % (verb, found.subject, s3(term), found.object)
    return None
