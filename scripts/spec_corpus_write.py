"""The spec corpus written by `work batch start` (batches r46, r47; b333): in a bounded context that keeps a corpus
(`grammar/corpus/spec/`, grammar/corpus/spec/README.md), a block for each line the batch lays, under its id in id
order, its trace `From: b<k> r<n>.` (with `Retires: r<m>.` before it when the item's `retires:` pairs say so), the line
and its logical form as `model parse --form` prints it on the laid tree; and the block of each id an item retires
taken out. A codified-1 capability keeps no corpus file. The form is the parser's: the task that builds the line reads
it against the line and corrects it where its item changes the grammar."""
import re
from pathlib import Path

import backlog_items
import backlog_lines
import spec_read

CORPUS = "grammar/corpus/spec"
BLOCK = re.compile(r"(?ms)^## ([rU][1-9]\d*)[ \t]*\n.*?(?=^## |\Z)")


def kept(tree):
    """Whether the bounded context keeps a corpus."""
    return (Path(tree) / CORPUS).is_dir()


def form(tree, text):
    """The logical form of a line as `model parse --form` prints it, or its refusal when grammar 4 refuses it."""
    import spec_grammar4
    import spec_language
    import spec_lf
    parsed = spec_language.parse(tree, text)
    if parsed.tree is None:
        return "refused: %s" % parsed.refusal
    vocab, _ = spec_grammar4.load(tree)
    return spec_lf.show(spec_lf.form(vocab, parsed.tree))


def block(ident, trace, line, reading):
    return "## %s\n%s\n\n```reading\n%s\n%s\n```\n\n" % (ident, trace, line, reading)


def _number(ident):
    return int(ident[1:])


def with_block(text, ident, chunk):
    """`text` with `chunk` as the block of `ident`: in place of the one there, else before the first block of a
    higher id, else at the end; the file ending in one newline, with no blank line after its last block (b740)."""
    for found in BLOCK.finditer(text):
        if found.group(1) == ident:
            rest = text[found.end():]
            return text[:found.start()] + chunk + rest if rest.strip() else (
                text[:found.start()] + chunk).rstrip("\n") + "\n"
        if _number(found.group(1)) > _number(ident):
            return text[:found.start()] + chunk + text[found.start():]
    return text.rstrip("\n") + "\n\n" + chunk.rstrip("\n") + "\n"


def without_block(text, ident):
    """`text` less the block of `ident`."""
    for found in BLOCK.finditer(text):
        if found.group(1) == ident:
            return (text[:found.start()] + text[found.end():]).rstrip("\n") + "\n"
    return text


def codified(tree, name):
    """Whether the file `name` of the corpus (a capability's, or `universal`) is read in grammar 4."""
    if name == "universal":
        return str(spec_read.read_universal(tree).frontmatter.get("language", "")).strip() == "codified-2"
    path = backlog_lines.capability_file(tree, name)
    return path.is_file() and str(spec_read.capability(path).frontmatter.get("language", "")).strip() == "codified-2"


def _edits(item):
    """{file name: ([(id, trace, line)], [retired id])} of one item's blocks."""
    blocks = backlog_lines.read(item, backlog_items.rel_of(item.name))
    out = {}
    for b in blocks:
        retiring = {line: old for line, old in b.retires}
        laid = [(rid, "%sFrom: %s %s." % ("Retires: %s. " % retiring[rid] if rid in retiring else "", item.name, rid),
                 text) for g in b.groups for rid, text in g.requirements]
        found = out.setdefault(b.capability, ([], []))
        found[0].extend(laid)
        found[1].extend(b.retired)
    if blocks.universal or blocks.universal_retired:
        found = out.setdefault("universal", ([], []))
        found[0].extend((uid, "From: %s %s." % (item.name, uid), text) for uid, text in blocks.universal)
        found[1].extend(blocks.universal_retired)
    return out


def write(tree, items):
    """Each item's laid lines written into the tree's corpus and its retired ids taken out of it, when the tree keeps
    a corpus; the paths changed."""
    if not kept(tree):
        return []
    changed = []
    for item in items:
        for name, (laid, retired) in _edits(item).items():
            if not codified(tree, name):
                continue
            path = Path(tree) / CORPUS / ("%s.md" % name)
            text = was = path.read_text() if path.is_file() else (
                "# %s: every live line with its intended reading\n" % name)
            for ident in retired:
                text = without_block(text, ident)
            for ident, trace, line in laid:
                text = with_block(text, ident, block(ident, trace, line, form(tree, line)))
            if text != was or not path.is_file():
                path.write_text(text)
                changed.append(path.relative_to(tree).as_posix())
    return list(dict.fromkeys(changed))
