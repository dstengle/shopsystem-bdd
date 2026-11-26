"""A plugin pack an item imports (b672, drafting r73, r74, batches r132).

The item keeps its imports in an `### imports` block of its `## Requirements` (backlog_section reads and writes it,
after the moves block), one bullet a pack: `- pack `<name>``. `work line <item> --import <name>` keeps the import of
the plugin's pack `grammar/packs/<name>.md` in the item, refused naming the pack when the plugin has no pack of that
name, and when spec/index.md or the item imports it already. `lay` adds each name to `spec/index.md`'s `imports:`;
`unlay` takes out each one the index did not import at the batch's base (else in the latest version git holds of
it)."""
import re

import spec_packs
from backlog_items import Refused, commit, find, label, one_line

HEAD = "### imports"
LINE = re.compile(r"^- pack `([a-z0-9]+(?:-[a-z0-9]+)*)`$")
FLAGS = ("import_pack",)
INDEX = "spec/index.md"


def add_arguments(p):
    """`work line`'s option that imports a plugin pack."""
    p.add_argument("--import", dest="import_pack", metavar="PACK", help="a pack of the plugin (grammar/packs/<pack>.md) "
                   "the item adds to spec/index.md's imports: once it is laid")


def given(args):
    """True when the run is this module's."""
    return getattr(args, "import_pack", None) is not None


class Lines:
    """The lines of the item's `### imports` block, read one at a time by backlog_section's reader."""

    def __init__(self, imports, refuse):
        self.imports, self.refuse = imports, refuse

    def line(self, line):
        if line == HEAD or not line.strip():
            return
        found = LINE.match(line.strip())
        if not found:
            self.refuse("a line of the imports block that is no `- pack `<name>``: %s" % line)
        if found.group(1) in self.imports:
            self.refuse("the import of the pack %s is there twice" % found.group(1))
        self.imports.append(found.group(1))


def render(imports):
    return HEAD + "\n\n" + "\n".join("- pack `%s`" % name for name in imports) if imports else ""


def write(root, name, pack):
    """`--import`: the import of the plugin's pack `pack` kept in the item and committed."""
    from backlog_section import SECTION, read, takes
    from backlog_section import render as rendered
    item = find(root, name)
    takes(item)
    blocks = read(item, "the item %s" % item.name)
    pack = one_line(pack, "pack")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", pack) or not (spec_packs.PLUGIN / ("%s.md" % pack)).is_file():
        raise Refused("work line: the plugin has no pack %s" % pack, reason="no such pack", names=["pack:%s" % pack])
    if pack in spec_packs.imports(root):
        raise Refused("work line: spec/index.md imports the pack %s already" % pack)
    if pack in blocks.imports:
        raise Refused("work line: %s imports the pack %s already" % (label(item), pack))
    blocks.imports.append(pack)
    item.sections[SECTION] = rendered(blocks)
    commit(root, item, "work line: %s imports the pack %s" % (label(item), pack))
    return item, pack


def cmd(args):
    """`work line` with `--import`, alone; what was done, printed."""
    from backlog_cli import PIECES
    others = [k for k in PIECES + ("retires", "reword", "remove", "group", "in_group", "into")
              if getattr(args, k, None) is not None]
    if others:
        raise Refused("work line: --import takes no other piece and no --into")
    item, pack = write(args.root, args.name, args.import_pack)
    print("%s: imports the pack %s" % (label(item), pack))
    return 0


def lay(into, blocks, files):
    """Each pack the item imports added to `into`'s spec/index.md `imports:`, its path added to `files`."""
    from backlog_pack import _index
    for pack in getattr(blocks, "imports", ()):
        _index(into, pack, True, files)


def unlay(into, blocks, files, base=None):
    """The reverse of `lay`: each import out of spec/index.md that the index did not hold at `base` (else in the
    latest version git holds of it)."""
    from backlog_area_move_unlay import held
    from backlog_pack import _index
    imports = list(getattr(blocks, "imports", ()))
    if not imports:
        return
    was = held(spec_packs.Path(into) / INDEX, base)
    found = spec_packs.IMPORTS.search(spec_packs._frontmatter(was)) if was is not None else None
    before = [n.strip() for n in found.group("names").split(",")] if found else []
    for pack in imports:
        if pack not in before:
            _index(into, pack, False, files)
