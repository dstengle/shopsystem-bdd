"""An item's terms of a context's own pack (b472, drafting r51, r52, batches r95): term entries drafted in the item and
laid into `spec/packs/<name>.md` by `work batch start`, the pack imported.

The item keeps them in a `### <name> pack` block of its `## Requirements` (backlog_section reads and writes it, after
the adapter blocks): term bullets in the glossary's entry form. `work line <item> --pack <name> --term "<bullet>"`
keeps each term in the block, refused when the pack (the context's file, or the item's block) has an entry of the
term's word already, naming the term, and on a name of the plugin's own packs (grammar/packs/), which a context pack
of that name would shadow whole (spec_packs' `path_of`). `lay` appends each entry to the pack's `## Glossary`, the
pack made when missing, and adds its name to `spec/index.md`'s `imports:`; `unlay` takes the entries out again, and a
pack the lay made, left with none, out with its import."""
import re
from collections import namedtuple
from pathlib import Path

import spec_packs
from backlog_items import Refused, commit, find, label

HEAD = re.compile(r"^### ([a-z0-9]+(?:-[a-z0-9]+)*) pack$")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
WORD = re.compile(r"^- \*\*([^*]+)\*\*")
MADE = "# %s\n\nThe terms of this bounded context's own pack %s.\n\n## Glossary\n\n"
PackBlock = namedtuple("PackBlock", "name terms", defaults=((),))


def add_arguments(p):
    """`work line`'s option of a context's own pack."""
    p.add_argument("--pack", metavar="NAME", help="with --term: the context's own pack spec/packs/<name>.md the term "
                   "entry goes into, the pack imported by spec/index.md once the item is laid")


class Lines:
    """The lines of the item's `### <name> pack` blocks, read one at a time by backlog_section's reader."""

    def __init__(self, blocks, refuse):
        self.blocks, self.refuse = blocks, refuse

    def head(self, name):
        if any(b.name == name for b in self.blocks):
            self.refuse("the %s pack block is there twice" % name)
        self.blocks.append(PackBlock(name))

    def line(self, line):
        if not line.strip():
            return
        if not WORD.match(line):
            self.refuse("a line of a pack block that is no term entry: %s" % line)
        self.blocks[-1] = self.blocks[-1]._replace(terms=self.blocks[-1].terms + (line.strip(),))


def render(block):
    return "### %s pack" % block.name + ("\n\n" + "\n".join(block.terms) if block.terms else "")


def path_of(into, name):
    return Path(into) / "spec" / "packs" / ("%s.md" % name)


def _words(text):
    return {m.group(1) for m in (WORD.match(x) for x in text.split("\n")) if m}


def write(root, name, pack, terms):
    """`work line <item> --pack <pack> --term <bullet>...`: each term kept in the item's block of the pack."""
    from backlog_section import SECTION, read, takes
    from backlog_section import render as rendered
    if not NAME.match(pack) or (spec_packs.PLUGIN / ("%s.md" % pack)).is_file():
        raise Refused("work line: --pack %s names %s; a context's own pack has a name of its own" % (
            pack, "the plugin's own pack" if NAME.match(pack) else "no pack name"))
    for term in terms:
        if not WORD.match(term.strip()):
            raise Refused("work line: a term entry opens with `- **<word>**`, not %s" % term)
    item = find(root, name)
    takes(item)
    blocks = read(item, "the item %s" % item.name)
    at = next((n for n, b in enumerate(blocks.packs) if b.name == pack), None)
    if at is None:
        blocks.packs.append(PackBlock(pack))
        at = len(blocks.packs) - 1
    file = path_of(root, pack)
    held = _words(file.read_text(encoding="utf-8")) if file.is_file() else set()
    held |= _words("\n".join(blocks.packs[at].terms))
    for term in terms:
        word = WORD.match(term.strip()).group(1)
        if word in held:
            raise Refused("work line: the pack %s has the term %s already" % (pack, word))
        held.add(word)
    blocks.packs[at] = blocks.packs[at]._replace(terms=blocks.packs[at].terms + tuple(t.strip() for t in terms))
    item.sections[SECTION] = rendered(blocks)
    said = "%s of the pack %s" % ("a term" if len(terms) == 1 else "%d terms" % len(terms), pack)
    commit(root, item, "work line: %s %s" % (label(item), said))
    return item, said


def cmd(args):
    """`work line --pack`: with --term, and no --into, line or other piece."""
    from backlog_cli import PIECES
    if not args.term or args.into or args.retires or any(getattr(args, k) is not None for k in PIECES if k != "term"):
        raise Refused("work line: --pack takes --term, with no --into, line or other piece")
    item, said = write(args.root, args.name, args.pack, args.term)
    print("%s: %s" % (label(item), said))
    return 0


def _imports(text, name, wanted):
    """spec/index.md's text with `name` in its frontmatter's `imports:` (or out of it)."""
    head = re.match(r"---\n.*?\n---\n", text, re.DOTALL)
    if head is None:
        return text
    front = head.group(0)
    found = spec_packs.IMPORTS.search(front)
    names = [n.strip() for n in found.group("names").split(",") if n.strip()] if found else []
    if (name in names) == wanted:
        return text
    names = names + [name] if wanted else [n for n in names if n != name]
    line = "imports: [%s]" % ", ".join(names)
    front = front[:found.start()] + line + front[found.end():] if found else front[:-4] + line + "\n---\n"
    return front + text[head.end():]


def _index(into, name, wanted, files):
    path = Path(into) / "spec" / "index.md"
    if path.is_file() and (text := _imports(path.read_text(), name, wanted)) != path.read_text():
        path.write_text(text)
        files.append("spec/index.md")


def _glossed(text, terms):
    """`text` with `terms` after the last line of its `## Glossary` (made at the end when it has none)."""
    found = re.search(r"(?ms)^## Glossary[ \t]*\n(.*?)(?=^## |\Z)", text)
    if found is None:
        return text.rstrip("\n") + "\n\n## Glossary\n\n" + "\n".join(terms) + "\n"
    inside = found.group(1).rstrip("\n")
    body = (inside + "\n" if inside.strip() else "\n") + "\n".join(terms) + "\n"
    rest = text[found.end(1):]
    return text[:found.start(1)] + body + ("\n" + rest if rest else "")


def lay(into, blocks, files):
    """Each pack block's entries appended to its pack's `## Glossary` (the pack made when missing), the pack imported;
    each path changed added to `files`."""
    for block in getattr(blocks, "packs", ()):
        path = path_of(into, block.name)
        text = path.read_text(encoding="utf-8") if path.is_file() else MADE % (block.name, block.name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_glossed(text, block.terms), encoding="utf-8")
        files.append(path.relative_to(into).as_posix())
        _index(into, block.name, True, files)


def unlay(into, blocks, files):
    """The reverse of `lay`: each entry out of its pack; a pack left as the lay makes it, with no entry, removed and
    its import out."""
    for block in getattr(blocks, "packs", ()):
        path = path_of(into, block.name)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for term in block.terms:
            text = re.sub(r"(?m)^%s\n?" % re.escape(term), "", text, count=1)
        files.append(path.relative_to(into).as_posix())
        if text.strip() == (MADE % (block.name, block.name)).strip():
            path.unlink()
            _index(into, block.name, False, files)
        else:
            path.write_text(text, encoding="utf-8")
