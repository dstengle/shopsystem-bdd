"""`work line <item> --retirement-list <file>` (b461): a retirement list applied to an item in one request. The file
holds one pair a line, a live requirement id `<capability>#r<n>` and the requirement line that retires it
(`<cap>#r<n> <line>`, a `:` after the id allowed); blank lines and lines opening with `#` are skipped. Each pair is
written as `work line --retires` writes it (backlog_lines, backlog_retires), and the item committed once; a list that
holds a requirement id no requirement has, or that does not read, is refused whole, naming it, the item unchanged."""
import re
from pathlib import Path

import backlog_lines
import backlog_retires
from backlog_items import Refused, commit, find, label

PAIR = re.compile(r"^(\S+?#r\d+):?\s+(\S.*)$")


def pairs(path):
    """The (id, line) pairs of the retirement list at `path`, in its order; refused naming a line that does not
    read, an id given twice, or a list of none."""
    try:
        text = Path(path).read_text()
    except OSError as err:
        raise Refused("work line: the retirement list %s cannot be read: %s" % (path, err.strerror)) from None
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        found = PAIR.match(line)
        if not found:
            raise Refused("work line: the retirement list %s, line %d, is not `<capability>#r<n> <line>`: %s"
                          % (path, n, line))
        if any(found.group(1) == ident for ident, _ in out):
            raise Refused("work line: the retirement list %s names %s twice" % (path, found.group(1)))
        out.append(found.groups())
    if not out:
        raise Refused("work line: the retirement list %s holds no pair" % path)
    return out


def apply(root, name, path):
    """Every pair of the list written into the item `name`: its line the next id of its capability, the old id
    under the block's `retired:` and the pair under its `retires:`; one commit. Each id checked before anything is
    written. The item and the pairs of new and old ids."""
    item = find(root, name)
    listed = pairs(path)
    for ident, _ in listed:
        backlog_retires.check(root, item, ident)
    done = []
    for ident, text in listed:
        capability, rid = backlog_retires.check(root, item, ident)
        new = backlog_lines.add_line_to(root, item, capability, text)
        backlog_retires.with_retired(item, capability, rid, new.split("#")[1])
        done.append((new, ident))
    commit(root, item, "work line: %s retirement list: %s" % (
        label(item), ", ".join("%s retires %s" % pair for pair in done)))
    return item, done


def cmd(args):
    """`work line <item> --retirement-list <file>`, with no other piece."""
    others = [k for k in ("text", "term", "relation", "given", "universal", "upstream", "recodify", "model", "into",
                          "retires", "reword", "remove", "group", "in_group", "capability") if getattr(args, k, None)]
    if others or args.no_line:
        raise Refused("work line: --retirement-list takes no requirement line or other option")
    item, done = apply(args.root, args.name, args.retirement_list)
    for new, old in done:
        print("%s: %s retires %s" % (label(item), new, old))
    return 0
