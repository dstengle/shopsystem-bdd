"""The lexicon's problems (split out of spec_lexicon, which re-exports `problems` and `unlabelled`): v_t4 (a term
names its part of speech, its kinds are kinds, an attribute gives values), v_t5, v_t6, v_t7 (a gloss of one sentence,
`one_sentence`) and v_t9, beside spec_relations' and spec_frames' problems; and the refusal of a lexicon with a term
that names no part of speech (`unlabelled`).
"""
import re
from collections import defaultdict

import spec_frames
import spec_relations
import spec_value_kinds
from spec_lexicon import LETTER, gloss, relabel


def one_sentence(text):
    """design-r2 §8's rule: code spans, quoted strings and e.g., i.e., etc., vs. are blanked; `.!?` before a space or
    the end, and `;`, end a sentence; `:` does not. An empty gloss passes."""
    text = re.sub(r"`[^`]*`|\"[^\"]*\"|“[^”]*”", "x", text)
    text = re.sub(r"\b(?:e\.g|i\.e|etc|vs)\.", "x", text).strip()
    body = text[:-1] if text[-1:] in ".!?" else text
    return ";" not in text and not re.search(r"[.!?](?:\s|$)", body)


def _unnamed(t):
    return t.category not in LETTER or t.category == "value"


def _relabelled(t):
    hint = relabel(t.label)
    return "(%s) is written (%s)" % (t.label, hint) if hint else ""


def unlabelled(lexicon):
    """The refusal of a lexicon with a term that names no part of speech (v_t4), each such term named with the
    label it is to carry, or None: the grammars are built from the parts of speech, and such a term fills no slot."""
    found = []
    for t in lexicon.terms:
        if _unnamed(t):
            fix = _relabelled(t) or ("(%s) is no part of speech" % t.label if t.label else "names no part of speech")
            found.append("%s: %s %s" % (t.where, t.term, fix))
    if not found:
        return None
    return ("terms that do not name their part of speech (write each as (noun), (proper noun), (artifact), (verb), "
            "(adjective of <kind>), (attribute of <kind>) or (noun, <resource>)): " + "; ".join(found))


def problems(lexicon, outer=frozenset()):
    """v_t4 (a term has a category, and its kinds are kinds), v_t5 (a value names one attribute of one kind),
    v_t6 (no two terms linearise the same), v_t7 (a gloss of more than one sentence), v_t9 (a `Means:` field),
    spec_relations' v_t4, v_t8 and v_t10, and spec_frames' v_t11, v_t12 and v_t13 (its frames may name `outer`, b199), as (code, term, message) sorted."""
    out = []
    kinds = lexicon.kind_names()
    for t in lexicon.terms:
        if _unnamed(t):
            hint = _relabelled(t)
            out.append(("v_t4", t.term, "%s: the term does not name its part of speech%s" % (
                t.where, "; " + hint if hint else "")))
        elif t.category in ("attribute", "condition", "relation") and not t.kinds:
            out.append(("v_t4", t.term, "%s: the %s names no kind" % (t.where, t.category)))
        elif any(k not in kinds for k in t.kinds):
            missing = ", ".join(k for k in t.kinds if k not in kinds)
            out.append(("v_t4", t.term, "%s: %s is not a kind" % (t.where, missing)))
        elif t.category == "attribute" and (not t.values and not t.type or spec_value_kinds.mixed(t)):
            out.append(("v_t4", t.term, "%s: the attribute gives %s" % (t.where, spec_value_kinds.mixed(t) or "no Values")))
        if t.category == "event" and t.term in lexicon.core_verbs():
            out.append(("v_t6", t.term, "%s: the grammar spells `%s` itself" % (t.where, t.term)))
    seen = defaultdict(list)
    for v, k, a, _ in lexicon.values():
        seen[(k, v)].append(a)
    out += [("v_t5", v, "the value %s of %s is in more than one attribute (%s)" % (v, k, ", ".join(a)))
            for (k, v), a in seen.items() if len(a) > 1]
    counts = defaultdict(int)
    for t in lexicon.terms:     # a verb's two entries are two senses (spec_frames' v_t15)
        counts[t.key] += t.category != "event"
    out += [("v_t6", key[1], "the %s %s is given %d times" % (key[0], key[1], n)) for key, n in counts.items()
            if n > 1]
    for t in lexicon.of("actor"):
        words = t.term.split(" ", 1)
        if len(words) == 2 and words[0] in ("a", "an", "the") and words[1] in kinds:
            out.append(("v_t6", t.term, "the actor %s reads as the kind %s" % (t.term, words[1])))
    out += [("v_t7", t.term, "%s: the entry's gloss is more than one sentence" % t.where)
            for t in lexicon.terms if not one_sentence(gloss(t.text))]
    out += [("v_t9", t.term, "%s: the meaning is a Means: field; write one Def sentence, or a gloss" % t.where)
            for t in lexicon.terms if re.search(r"(?:^|\s)Means:", t.text)]
    return sorted(set(out + spec_relations.problems(lexicon, outer) + spec_frames.problems(lexicon, outer)))
