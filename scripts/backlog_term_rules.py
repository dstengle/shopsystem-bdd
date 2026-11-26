"""The lexicon rules a term written or reworded into an item breaks (b810, b826, drafting r101, r102): the item, as it is to be
committed, laid onto a temporary copy of `spec/` (backlog_lines' `lay_onto`), and each problem of the lexicon
(spec_lexicon's, spec_vocabulary's) the lay brings that names a word of the terms; in a context with a domain model,
whose lexicon is read off the model, each vocabulary entry's own part of speech (v_t4) and gloss of one sentence (v_t7)
checked too, as a capability term's are. When one of `RULES` is among them, the write is refused naming the term and
every rule it breaks, each once with its first message (`refuse`), nothing committed; another rule, as v_t6, leaves the write to go on (backlog_lines'
`warn_terms`). A lay or a read of the copy that is refused or fails on a file refuses nothing: the readiness bar
checks it whole."""
import re
import shutil
import tempfile
from pathlib import Path

from backlog_items import Refused

RULES = ("v_t4", "v_t7", "v_t11", "v_t13", "v_t14", "v_t19")
WORD = re.compile(r"\s*-\s*\*\*(.+?)\*\*")


def _problems(root):
    import spec_lexicon
    import spec_rgl_vocab
    import spec_vocabulary
    lexicon = spec_lexicon.read(root)
    return set(spec_lexicon.problems(lexicon, spec_rgl_vocab.outer(root))) | set(spec_vocabulary.problems(root))


def _entry_problems(bullet):
    """v_t4 and v_t7 of a vocabulary entry `- **w** (<part of speech>) → <element>. <gloss>`, read as a term entry;
    none of a bullet that is no vocabulary entry."""
    import spec_lexicon
    import spec_lexicon_problems
    import spec_vocabulary
    found = spec_vocabulary.ENTRY.match(bullet.strip())
    if not found or not found.group("arrow"):
        return set()
    ref = spec_vocabulary.REF.match(found.group("text") or "")
    rest = (ref.group("rest") or "") if ref else ""
    word, label = found.group("term"), found.group("label")
    term = spec_lexicon.entry("- **%s** (%s): %s" % (word, label, rest), "the entry")
    out = set()
    if term is None or spec_lexicon_problems._unnamed(term):
        out.add(("v_t4", word, "the entry's (%s) is no part of speech" % label))
    if not spec_lexicon_problems.one_sentence(spec_lexicon.gloss(rest)):
        out.add(("v_t7", word, "the entry's gloss is more than one sentence"))
    return out


def violations(root, item, bullets):
    """{word: [(code, message)]} of each term of `bullets` the lay of `item` onto a copy of `root`'s spec makes
    break a lexicon rule, sorted; a problem the spec had before the lay left out."""
    words = {m.group(1).strip() for m in (WORD.match(b) for b in bullets) if m}
    import backlog_lines
    import domain_model
    import spec_held
    copy, found = Path(tempfile.mkdtemp(prefix="term-rules-")), set()
    try:
        shutil.copytree(Path(root) / "spec", copy / "spec")
        with spec_held.held(copy):
            before = _problems(copy)
            backlog_lines.lay_onto(copy, item)
            found = _problems(copy) - before
        if domain_model.exists(root):
            for bullet in bullets:
                found |= _entry_problems(bullet)
    except (Refused, OSError):  # a lay or a read that fails refuses nothing: the readiness bar checks it whole
        found = set()
    finally:
        shutil.rmtree(copy, ignore_errors=True)
    out = {}
    for code, word, message in sorted(f for f in found if f[1] in words):
        if code not in {c for c, _ in out.get(word, ())}:      # a rule named once, as two readers may each find it
            out.setdefault(word, []).append((code, message))
    return out


def refuse(root, item, bullets):
    """Refused, naming each term and every rule it breaks, when a term of `bullets` breaks one of `RULES`."""
    broken = {w: v for w, v in violations(root, item, bullets).items() if any(c in RULES for c, _ in v)}
    if not broken:
        return
    said = "; ".join("%s breaks %s (%s)" % (w, ", ".join(sorted({c for c, _ in v})), "; ".join(m for _, m in v))
                     for w, v in broken.items())
    names = ["term:%s" % w for w in broken] + ["rule:%s" % c for c in sorted({c for v in broken.values() for c, _ in v})]
    raise Refused("work line: the term %s" % said, reason="term violating a rule", names=names)
