"""A provider's words in an adapter spec (b550, checking r106-r109; decisions 0117, 0120, 0135): the terms of each
contract the adapter spec holds for a provider of its `providers:` (model_adapter's provider check: kept where
`spec obtain` keeps it, contract_obtain's `place`), read as entries of its lexicon after the packs and before its
own glossary (`terms`, which spec_lexicon's `read` gives a context of `kind: adapter`). The contract writes each term
as its vocabulary does, `<word> (<part of speech>): <text>`; read here in the glossary's entry form: a frame's
`<actor>` and `<agent>` the kind `agent`, `<from>` and `<to>` the object and the target of the contract's relation
the verb spells, any other `<x>` the kind x; an attribute of O its values (adjectives) or its type off the contract's
`[objects."O"]` (`bullet`). The provider's words are never edited (decision 0117): the adapter spec gives a word of
them another word with `renames: [<word> → <new word>]` in its spec/index.md (`renames`), the term then read under
the new word in every place the contract names it, its plural the new word's. A provider's term spelled as another
term the adapter spec reads (an imported pack's, its own, an earlier contract's) and not renamed clashes: it is left
out of the lexicon and a file problem names it (`clashes`, `problems`). An assumed description, a capability of the
adapter spec whose frontmatter says `assumed: true`, is evidence only when its scenarios run (decision 0120): each of
its requirement ids that no scenario of its feature refers to (`@r<n>`) is a file problem naming the id
(`unscenarioed`)."""
import re
import tomllib
from pathlib import Path

from model_parse import as_list, frontmatter

TERM = re.compile(r"^(?P<word>.+?) \((?P<pos>[^)]*)\)(?::\s*(?P<text>.*))?$")
RENAME = re.compile(r"^(?P<old>.+?)\s*(?:→|->)\s*(?P<new>.+)$")
SLOT = re.compile(r"<([^>]+)>")


def _index(root):
    path = Path(root) / "spec" / "index.md"
    return frontmatter(path.read_text())[0] if path.is_file() else {}


def adapter(root):
    import model_adapter
    return str(_index(root).get("kind", "")).strip() == model_adapter.KIND


def renames(root):
    """{word: new word} of `renames:` of the adapter spec's spec/index.md."""
    found = (RENAME.match(str(r).strip()) for r in as_list(_index(root).get("renames")))
    return {m.group("old").strip(): m.group("new").strip() for m in found if m}


def contracts(root):
    """(where, provider id, contract) of each provider's contract the adapter spec holds, in `providers:` order."""
    import contract_obtain
    import model_adapter
    root, out = Path(root), []
    for given in as_list(_index(root).get("providers")):
        m = model_adapter.PROVIDER.match(str(given).strip())
        kept = sorted(root.glob(contract_obtain.place(m.group("id"), m.group("version") or "*").as_posix())) if m else []
        if kept:
            out.append((kept[-1].relative_to(root).as_posix(), m.group("id"), tomllib.loads(kept[-1].read_text())))
    return out


def _plural(old, new, plural):
    return new[:len(new) - len(old)] + plural if plural and new.endswith(old) else ""


def bullet(line, objects, renamed):
    """A contract's term line as a glossary entry, its words renamed, or None when it does not read."""
    m = TERM.match(line.strip())
    if not m:
        return None
    word, pos, text = m.group("word"), m.group("pos"), m.group("text") or ""
    name = lambda w: renamed.get(w, w)
    if pos.startswith("attribute of "):
        owner = pos[len("attribute of "):].strip()
        for a in objects.get(owner, {}).get("attributes", []):
            values = re.match(r"^%s:\s*(.+)$" % re.escape(word), a)
            typed = re.match(r"^%s \((number|time|text)\)$" % re.escape(word), a)
            if values:
                text += " Values (adjective): %s." % ", ".join("`%s`" % v.strip() for v in re.split(r"[|<]", values.group(1)))
            elif typed:
                text += " Type: %s." % typed.group(1)
        pos = "attribute of " + name(owner)
    text = re.sub(r"Frame:\s*(.+?)\.(?=\s|$)", lambda f: "Frame: %s." % _frame(f.group(1), objects, name), text)
    plural = re.search(r"Plural:\s*(.+?)\.", text)
    if word in renamed and plural:
        new = _plural(word, renamed[word], plural.group(1))
        text = text.replace(plural.group(0), "Plural: %s." % new if new else "")
    return ("- **%s** (%s): %s" % (name(word), pos, " ".join(text.split()))).rstrip()


def _frame(frame, objects, name):
    verb = SLOT.sub("", frame).split()[0] if SLOT.sub("", frame).split() else ""
    rel = next(((o, r) for o, d in objects.items() for r in d.get("relations", []) if r.split(" → ")[0] == verb),
               None)

    def kind(slot):
        slot = slot.group(1)
        if slot in ("actor", "agent"):
            return "agent"
        if slot in ("from", "to") and rel:
            target = rel[1].split(" → ")[1].split(" (")[0].split(" | ")[0].strip()
            return name(rel[0] if slot == "from" else target)
        return name(slot)
    return SLOT.sub(kind, frame)


def _others(root):
    """(word, where) of each term the adapter spec reads besides its providers': the imported packs' and its own."""
    import spec_lexicon
    import spec_packs
    out = []
    for name in spec_packs.imports(root):
        path = spec_packs.path_of(root, name)
        out += [(t.term, "the pack %s" % name) for t in (spec_packs.terms(path, name) if path else [])]
    return out + [(t.term, t.where) for t in spec_lexicon.own(Path(root))]


def _read(root):
    """(terms, clashes): the providers' terms as entries, and (word, provider, where) of each that clashes."""
    import spec_lexicon
    if not adapter(root):
        return [], []
    renamed, taken = renames(root), dict(_others(root))
    terms, clashes = [], []
    for where, provider, contract in contracts(root):
        objects = contract.get("objects", {})
        for line in contract.get("terms", []):
            found = bullet(line, objects, renamed)
            t = spec_lexicon.entry(found, where) if found else None
            if t is None:
                continue
            if t.term in taken:
                clashes.append((t.term, provider, taken[t.term]))
                continue
            taken[t.term] = "the contract of %s" % provider
            terms.append(t)
    return terms, clashes


def terms(root):
    return _read(root)[0]


def problems(root):
    """A file problem for each clash of a provider's term and each assumed description's id with no scenario."""
    out = ["spec/index.md: the term %s of the provider %s clashes with the term %s of %s; rename it under renames:"
           % (word, provider, word, where) for word, provider, where in _read(root)[1]]
    return out + unscenarioed(root)


def unscenarioed(root):
    """A problem for each requirement id of an assumed description that no scenario of its feature refers to."""
    import spec_read
    root, out = Path(root), []
    for path in sorted((root / "spec" / "capabilities").glob("*.md")):
        if str(frontmatter(path.read_text())[0].get("assumed", "")).strip().lower() != "true":
            continue
        feature = root / "features" / ("%s.feature" % path.stem)
        tags = set(re.findall(r"@(r\d+)\b", feature.read_text())) if feature.is_file() else set()
        out += ["spec/capabilities/%s: the assumed description holds the requirement id %s#%s, which no scenario "
                "refers to" % (path.name, path.stem, q.id) for g in spec_read.capability(path).groups
                for q in g.requirements if q.id not in tags]
    return out
