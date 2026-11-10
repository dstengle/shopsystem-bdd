"""The vocabulary grammar 4 is generated from (the CNL 4 design, I7a): a context's terms over every layer, its kinds
in one tree, its actors, attributes and values, and each verb's frames read into pieces.

The layers are spec_packs' (each imported pack, the glossary of `spec/index.md`, each capability's `## Terms`); a word
a higher layer defines takes the place of a lower layer's entries of it (`Redefines:`, v_t16). The base grammar's own
kinds are `thing`, the root, and `agent`, a kind of thing (the CLI pack's frames name both); a kind or an actor with
no `Kind of:` is a kind of thing.

A verb's `Frame:` is read as its subject (a kind or an actor's kind), the verb's third person form, then pieces: each
a run of fixed words and the kind after them, or fixed words alone at the end: `agent runs command with option` is
[((), command), (("with",), option)]; `tool exits with an error naming thing` is [(("with", "an", "error",
"naming"), thing)]. A frame that does not read so is left out (v_t13 names it).
"""
import re
from dataclasses import dataclass, field

import spec_frames
import spec_lexicon
import spec_packs
import spec_relations

BASE_KINDS = {"thing": None, "agent": "thing"}


@dataclass(frozen=True)
class Verb:
    term: object                # the spec_lexicon.Term of its entry
    aspect: str                 # state or action
    frames: tuple               # (subject kind, pieces) of each frame that reads


@dataclass
class Vocab:
    kinds: dict = field(default_factory=dict)       # kind -> its parent kind (None for thing)
    nouns: dict = field(default_factory=dict)       # kind -> (singular, plural) spelling
    actors: list = field(default_factory=list)      # (term, kind)
    attributes: list = field(default_factory=list)  # (term entry, its kinds that are kinds here)
    verbs: list = field(default_factory=list)       # Verb
    words: set = field(default_factory=set)         # every spelling a code literal may not be

    def ancestors(self, kind):
        """The kind itself and every kind above it, nearest first."""
        out = []
        while kind is not None and kind not in out:
            out.append(kind)
            kind = self.kinds.get(kind)
        return out


def lexicon(root):
    """The context's terms over every layer, a lower layer's entries of a word a higher layer defines left out."""
    layered = spec_packs.layers(root)
    order = {layer: n for n, layer in enumerate(dict.fromkeys(layer for layer, _ in layered))}
    top = {}
    for layer, t in layered:
        top[t.term] = max(top.get(t.term, -1), order[layer])
    terms = [t for layer, t in layered if order[layer] == top[t.term]]
    return spec_lexicon.Lexicon(terms, spec_relations.read(root))


def regular_plural(word):
    head, _, last = word.rpartition(" ")
    if re.search(r"(s|sh|ch|x|z)$", last):
        last += "es"
    elif re.search(r"[^aeiou]y$", last):
        last = last[:-1] + "ies"
    else:
        last += "s"
    return (head + " " + last).strip()


def pieces(words, kinds):
    """The pieces of a frame's words after its verb, or None when a kind follows a kind with no word between."""
    out, fixed, i = [], [], 0
    while i < len(words):
        found = next((j for j in range(len(words), i, -1) if " ".join(words[i:j]) in kinds), None)
        if found is None:
            fixed.append(words[i])
            i += 1
            continue
        if out and not fixed:
            return None
        out.append((tuple(fixed), " ".join(words[i:found])))
        fixed, i = [], found
    return out + ([(tuple(fixed), None)] if fixed else [])


def frame(term, text, kinds, actors):
    """(subject kind, pieces) of one `Frame:` of a verb's entry, or None when it does not read."""
    words, verb = text.split(), spec_frames.s3(term).split()
    for n in range(len(words) - len(verb), 0, -1):
        subject = " ".join(words[:n])
        if words[n:n + len(verb)] == verb and (subject in kinds or subject in actors):
            rest = pieces(words[n + len(verb):], kinds)
            return None if rest is None else (actors.get(subject, subject), tuple(rest))
    return None


def read(root):
    """The Vocab of the context at `root`."""
    lex, vocab = lexicon(root), Vocab()
    vocab.kinds = dict(BASE_KINDS)
    for t in lex.of("kind") + lex.of("resource"):
        vocab.kinds[t.term] = t.supertype if t.supertype and t.supertype != t.term else "thing"
    for kind, parent in list(vocab.kinds.items()):
        if parent is not None and parent not in vocab.kinds:
            vocab.kinds[kind] = "thing"
    plural = {t.term: t.plural for t in lex.terms if t.plural}
    vocab.nouns = {k: (k, plural.get(k) or regular_plural(k)) for k in vocab.kinds}
    vocab.actors = [(t.term, t.supertype if t.supertype in vocab.kinds else "thing") for t in lex.of("actor")]
    vocab.attributes = [(t, tuple(k for k in t.kinds if k in vocab.kinds)) for t in lex.of("attribute")]
    actors = dict(vocab.actors)
    for t in lex.of("event"):
        read_frames = tuple(f for f in (frame(t, text, vocab.kinds, actors) for text in t.frames) if f)
        if t.aspect in spec_lexicon.ASPECTS and read_frames:
            vocab.verbs.append(Verb(t, t.aspect, read_frames))
    vocab.words = lex.words() | {sg for sg, _ in vocab.nouns.values()} | {pl for _, pl in vocab.nouns.values()}
    vocab.words |= {spec_frames.s3(v.term) for v in vocab.verbs}
    return vocab
