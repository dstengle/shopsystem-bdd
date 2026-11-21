"""An item's operation tables and withheld operations (b355, drafting r31-r34, batches r79-r80): how an adapter
requests an operation, drafted in the item and laid into the adapter contract `spec/adapters/<port>.toml` by `work
batch start`.

The item keeps them in a `### <port> adapter` block of its `## Requirements` (backlog_section reads and writes it, after
the model blocks): an optional `withheld: [<service>.<operation>, ...]` line, the operations no command of the adapter
requests, then a ` ```toml ` fence of operation tables in the contract's own syntax. `work line <item> --expose
"<tables>"` keeps one operation's tables (`[operations."<service>.<operation>"]` with its command and its
parameters) in place of that operation's own, refused when the domain model, with the item's model lines laid, has no
such operation; `work line <item> --withhold <service>.<operation>` keeps the operation withheld, its table out.
`lay` puts each table into the contract in place of the operation's own and out of `[unexposed]`, and each withheld
operation into `[unexposed]` with its table out (the contract made when missing); `unlay` puts back what the contract
held at the batch's base (b479), as git last held it otherwise when no base is given."""
import re
import shutil
import subprocess
import tempfile
from collections import namedtuple
from pathlib import Path

import adapter_tables
from backlog_items import Refused, commit, find, label

HEAD = re.compile(r"^### ([a-z0-9]+) adapter$")
WITHHELD = re.compile(r"^withheld: \[([^\]]*)\]$")
FENCE, CLOSE = "```toml", "```"
PORT = "cli"
AdapterBlock = namedtuple("AdapterBlock", "port tables withheld", defaults=((), ()))


def add_arguments(p):
    """`work line`'s options of the adapter contract."""
    p.add_argument("--expose", metavar="TABLES", help='the tables of one operation for the CLI adapter contract, '
                   '`[operations."<service>.<operation>"]` with its command and parameters, kept in place of its own')
    p.add_argument("--withhold", metavar="SERVICE.OPERATION", help="an operation no command of the CLI adapter "
                   "requests, kept under the contract's [unexposed] with its table out")


class Lines:
    """The lines of the item's `### <port> adapter` blocks, read one at a time by backlog_section's reader."""

    def __init__(self, blocks, refuse):
        self.blocks, self.refuse, self.fence = blocks, refuse, None

    def head(self, port):
        if any(b.port == port for b in self.blocks):
            self.refuse("the %s adapter block is there twice" % port)
        self.blocks.append(AdapterBlock(port))

    def line(self, line):
        block = self.blocks[-1]
        if self.fence is not None:
            if line.strip() == CLOSE:
                text = "\n".join(self.fence)
                tables = tuple((i, adapter_tables.table(text, i)) for i in adapter_tables.operations(text))
                self.blocks[-1], self.fence = block._replace(tables=tables), None
            else:
                self.fence.append(line.rstrip())
        elif not line.strip():
            return
        elif (m := WITHHELD.match(line)) and not block.withheld and not block.tables:
            self.blocks[-1] = block._replace(withheld=tuple(w.strip() for w in m.group(1).split(",") if w.strip()))
        elif line.strip() == FENCE and not block.tables:
            self.fence = []
        else:
            self.refuse("a line of an adapter block that is no `withheld:` line or ```toml fence: %s" % line)


def render(block):
    parts = ["### %s adapter" % block.port]
    parts += ["withheld: [%s]" % ", ".join(block.withheld)] if block.withheld else []
    parts += ["%s\n%s\n%s" % (FENCE, "\n\n".join(t for _, t in block.tables), CLOSE)] if block.tables else []
    return "\n\n".join(parts)


def _at(blocks, port):
    found = next((n for n, b in enumerate(blocks.adapters) if b.port == port), None)
    if found is None:
        blocks.adapters.append(AdapterBlock(port))
        found = len(blocks.adapters) - 1
    return found


def operations(root, blocks):
    """The operations `<service>.<operation>` of the domain model, with the item's model lines laid on a copy."""
    import backlog_model
    import domain_model
    if not getattr(blocks, "models", ()):
        model = domain_model.read(root) if (Path(root) / "spec" / "model").is_dir() else domain_model.Model()
    else:
        copy = Path(tempfile.mkdtemp(prefix="expose-"))
        try:
            shutil.copytree(Path(root) / "spec", copy / "spec")
            backlog_model.lay(copy, blocks, [])
            model = domain_model.read(copy)
        finally:
            shutil.rmtree(copy, ignore_errors=True)
    return {"%s.%s" % (o.service, o.name) for o in model.operations()}


def _changed(root, name, change):
    from backlog_section import SECTION, read, takes
    from backlog_section import render as rendered
    item = find(root, name)
    takes(item)
    blocks = read(item, "the item %s" % item.name)
    at = _at(blocks, PORT)
    said = change(blocks, at)
    item.sections[SECTION] = rendered(blocks)
    commit(root, item, "work line: %s %s" % (label(item), said))
    return item, said


def expose(root, name, text):
    """`work line <item> --expose <tables>`: one operation's tables kept in the item in place of its own."""
    ident, tables = adapter_tables.one(text)

    def change(blocks, at):
        if ident not in operations(root, blocks):
            raise Refused("work line: the operation table %s names no operation of the domain model" % ident)
        block = blocks.adapters[at]
        blocks.adapters[at] = block._replace(
            tables=tuple(t for t in block.tables if t[0] != ident) + ((ident, tables),),
            withheld=tuple(w for w in block.withheld if w != ident))
        return "the operation table of %s" % ident
    return _changed(root, name, change)


def withhold(root, name, ident):
    """`work line <item> --withhold <service>.<operation>`: the operation kept withheld in the item, its table out."""
    ident = ident.strip()
    if not adapter_tables.IDENT.match(ident):
        raise Refused("work line: --withhold takes an operation `<service>.<operation>`, not %s" % ident)

    def change(blocks, at):
        block = blocks.adapters[at]
        blocks.adapters[at] = block._replace(tables=tuple(t for t in block.tables if t[0] != ident),
                                             withheld=tuple(w for w in block.withheld if w != ident) + (ident,))
        return "the operation %s withheld" % ident
    return _changed(root, name, change)


def cmd(args):
    """`work line --expose` and `--withhold`: one of them, and no other piece."""
    from backlog_cli import PIECES
    if (args.expose is None) == (args.withhold is None) or args.into or args.retires or args.retirement_list \
            or any(getattr(args, k) is not None for k in PIECES):
        raise Refused("work line: give one of --expose and --withhold, with no --into, line or other piece")
    if args.expose is not None:
        item, said = expose(args.root, args.name, args.expose)
    else:
        item, said = withhold(args.root, args.name, args.withhold)
    print("%s: %s" % (label(item), said))
    return 0


def contract_path(into, port):
    return Path(into) / "spec" / "adapters" / ("%s.toml" % port)


def lay(into, blocks, files):
    """The item's adapter blocks laid into `into`'s contracts, each path changed added to `files`."""
    for block in getattr(blocks, "adapters", ()):
        path = contract_path(into, block.port)
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for ident, tables in block.tables:
            text = adapter_tables.listed(adapter_tables.with_table(text, tables), ident, False)
        for ident in block.withheld:
            text = adapter_tables.listed(adapter_tables.without(text, ident), ident, True)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        files.append(path.relative_to(into).as_posix())


def _state(text, ident):
    return adapter_tables.table(text, ident), ident in adapter_tables.unexposed(text)


def _versions(path):
    """The texts git holds of `path`, newest first."""
    def git(*args):
        return subprocess.run(["git", "-C", str(path.parent), *args], capture_output=True, text=True)
    rel = git("ls-files", "--full-name", "--error-unmatch", path.name)
    if rel.returncode != 0:
        return []
    shas = git("log", "--format=%H", "--", path.name).stdout.split()
    shown = (git("show", "%s:%s" % (sha, rel.stdout.strip())) for sha in shas)
    return [s.stdout for s in shown if s.returncode == 0]


def _at_base(path, base):
    """The text of `path` at the commit `base`, empty when that commit holds no such file."""
    def git(*args):
        return subprocess.run(["git", "-C", str(path.parent), *args], capture_output=True, text=True)
    prefix = git("rev-parse", "--show-prefix").stdout.strip()
    shown = git("show", "%s:%s%s" % (base, prefix, path.name))
    return shown.stdout if shown.returncode == 0 else ""


def unlay(into, blocks, files, base=None):
    """The reverse of `lay`: each operation the block names put back as the contract at the commit `base` (the batch's
    base, b479) held it, no table and not unexposed when it held none, nothing else of the contract changed; with no
    `base`, as the newest version git holds that held it otherwise. A contract left with nothing removed."""
    for block in getattr(blocks, "adapters", ()):
        path = contract_path(into, block.port)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        versions = None if base else _versions(path)
        held = _at_base(path, base) if base else None
        for ident in [i for i, _ in block.tables] + list(block.withheld):
            if base:
                tables, listed = _state(held, ident)
            else:
                now = _state(text, ident)
                tables, listed = next((s for s in (_state(v, ident) for v in versions) if s != now), (None, False))
            text = adapter_tables.without(text, ident)
            text = adapter_tables.listed(adapter_tables.with_table(text, tables) if tables else text, ident, listed)
        if not text.strip():
            path.unlink()
        else:
            path.write_text(text, encoding="utf-8")
        files.append(path.relative_to(into).as_posix())
