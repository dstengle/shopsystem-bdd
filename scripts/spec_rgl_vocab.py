"""The vocabulary grammar 4 is generated from (the CNL 4 design, I7a): a context's terms over every layer, its kinds
in one tree, its actors, attributes and values, and each verb's frames read into pieces.

The layers are spec_packs' (each imported pack, the glossary of `spec/index.md`, each capability's `## Terms`); a word
the context defines takes the place of every pack's entries of it in the same sense (`Redefines:`, v_t16), a later pack's of an earlier
one's, while the glossary's and the capabilities' entries stand side by side, as the old lexicon reads them (b151).
The base grammar's own kinds are `thing`, the root, and `agent`, a kind of thing (the CLI pack's frames name both); a
kind or an actor with no `Kind of:` is a kind of thing.

A verb's `Frame:` is read as its subject (a kind or an actor's kind), the verb's third person form, then pieces: each
a run of fixed words and the kind after them, or fixed words alone at the end: `agent runs command with option` is
[((), command), (("with",), option)]; `tool exits with an error naming thing` is [(("with", "an", "error",
"naming"), thing)]. A frame that does not read so is left out (v_t13 names it). In a context with a domain model, its
operations by their qualified id (`operations`), which a verb names (spec_rgl_ops).
"""
import dataclasses
import re
from dataclasses import dataclass, field

import domain_model
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
    texts: tuple = ()           # the `Frame:` text of each of them, in order (b420: a refusal names it)
    actors: tuple = ()          # of each of them, the actor its subject names, else "" (b847: only it is the subject)


@dataclass
class Vocab:
    kinds: dict = field(default_factory=dict)       # kind -> its parent kind (None for thing)
    nouns: dict = field(default_factory=dict)       # kind -> (singular, plural) spelling
    actors: list = field(default_factory=list)      # (term, kind)
    attributes: list = field(default_factory=list)  # (term entry, its kinds that are kinds here)
    verbs: list = field(default_factory=list)       # Verb
    rows: list = field(default_factory=list)        # (k1, word, k2) of each relation row whose kinds are kinds here
    words: set = field(default_factory=set)         # every spelling a code literal may not be
    this: dict = field(default_factory=dict)        # kind -> its entry's `This:`, the run's own thing of the kind
    operations: dict = field(default_factory=dict)  # `<service>.<name>` -> its domain_model Operation (spec_rgl_ops)
    elements: dict = field(default_factory=dict)    # an actor's term -> the model element it names (b544)

    def ancestors(self, kind):
        """The kind itself and every kind above it, nearest first."""
        out = []
        while kind is not None and kind not in out:
            out.append(kind)
            kind = self.kinds.get(kind)
        return out


def lexicon(root):
    """The context's terms over every layer: every entry of the glossary and of each capability side by side, and of
    the packs' entries of a word only the last pack's, none when the context defines the word itself in the same sense
    (spec_packs' `sense`: a verb beside a pack's noun of its spelling, b618)."""
    layered = spec_packs.layers(root)
    own = {spec_packs.sense(t) for layer, t in layered if not layer.startswith("pack ")}
    last = {spec_packs.sense(t): layer for layer, t in layered if layer.startswith("pack ")}
    beside = {spec_packs.sense(t) for layer, t in layered if not layer.startswith("pack ") and spec_lexicon.beside(t)}
    terms = [t for layer, t in layered if not layer.startswith("pack ")
             or (spec_packs.sense(t) not in own and last[spec_packs.sense(t)] == layer)
             or (layer == "pack request" and spec_packs.sense(t) in beside)]
    if domain_model.exists(root):
        terms = _kinds_of(terms, domain_model.load(root).objects)
    return spec_lexicon.Lexicon(terms, spec_relations.read(root), tuple(spec_packs.imports(root)))


def _kinds_of(terms, objects):
    """A pack's kind of no `Kind of:` under the kind its model object is a kind of (b618: `object file kind of text`
    puts the base pack's `file` under `text`), as spec_vocabulary_terms reads a noun naming an object."""
    out = []
    for t in terms:
        up = objects[t.term].kind_of if t.category == "kind" and not t.supertype and t.term in objects else ""
        out.append(dataclasses.replace(t, supertype=up) if up else t)
    return out


def outer(root):
    """The kinds outside the context's own lexicon that the old lexicon reader's frames may name (b199): in a
    codified-2 context, the base kinds and every kind and actor of each imported pack; in any other, none."""
    import spec_grammar4  # here: spec_grammar4 imports this module

    if not spec_grammar4.marked(root):
        return frozenset()
    out = set(BASE_KINDS)
    for name in spec_packs.imports(root):
        path = spec_packs.path_of(root, name)
        if path is not None:
            out |= {t.term for t in spec_packs.terms(path, name) if t.category in ("kind", "actor")}
    return frozenset(out)


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


def frame(term, text, kinds, actors, named=False):
    """(subject kind, pieces) of one `Frame:` of a verb's entry, or None when it does not read; `named`, the actor
    its subject names in place of the frame (b847), "" when it names a kind."""
    words, verb = text.split(), spec_frames.s3(term).split()
    for n in range(len(words) - len(verb), 0, -1):
        subject = " ".join(words[:n])
        if words[n:n + len(verb)] == verb and (subject in kinds or subject in actors):
            rest = pieces(words[n + len(verb):], kinds)
            if named:
                return subject if subject in actors and subject not in kinds else ""
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
    vocab.this = {t.term: t.this for t in lex.of("kind") + lex.of("resource") if t.this}
    plural = {t.term: t.plural for t in lex.terms if t.plural}
    word = {t.term: t.word for t in lex.terms if t.word}     # a word of two areas: one kind each, spelled the word
    vocab.nouns = {k: (word.get(k, k), plural.get(k) or regular_plural(word.get(k, k))) for k in vocab.kinds}
    vocab.actors = [(t.term, t.supertype if t.supertype in vocab.kinds else "thing") for t in lex.of("actor")]
    vocab.elements = {t.term: t.element for t in lex.of("actor") if t.element}
    vocab.attributes = [(t, tuple(k for k in t.kinds if k in vocab.kinds)) for t in lex.of("attribute")]
    vocab.rows = list(dict.fromkeys((r.k1, r.word, r.k2) for r in lex.rows
                                    if r.k1 in vocab.kinds and r.k2 in vocab.kinds))
    actors = dict(vocab.actors)
    for t in lex.of("event"):
        framed = [(f, text) for f, text in ((frame(t, text, vocab.kinds, actors), text) for text in t.frames) if f]
        if t.aspect in spec_lexicon.ASPECTS and framed:
            vocab.verbs.append(Verb(t, t.aspect, tuple(f for f, _ in framed), tuple(text for _, text in framed),
                                    tuple(frame(t, text, vocab.kinds, actors, named=True) for _, text in framed)))
    if domain_model.exists(root):     # the operations a verb may name (the domain contract design, §5.1)
        vocab.operations = {"%s.%s" % (op.service, op.name): op for op in domain_model.load(root).operations()}
    vocab.words = lex.words() | {sg for sg, _ in vocab.nouns.values()} | {pl for _, pl in vocab.nouns.values()}
    vocab.words |= {spec_frames.s3(v.term) for v in vocab.verbs} | {"its", "no", "only", "has", "have", "holds", "this"}
    return vocab
