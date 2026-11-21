"""An item's own universal conditions, upstream entries and given blocks taken back out of it or replaced (b48,
drafting r53-r64), as `--remove-model` and `--reword-model` do for its model lines (backlog_model_edit). Each commits
only the item.

`work line <item> --remove-universal U<n>` takes the item's universal condition `U<n>` (or `universal#U<n>`) out;
`--replace-universal U<n> "<statement>"` gives it a new statement under its id. `--remove-upstream
<bounded-context id>` takes the item's upstream entry of that id out; `--replace-upstream <id> "<entry>"` puts the
new entry, checked as `--upstream`'s, in its place. `--remove-given <capability>#g<n>` takes the given block of the
item's group out; `--replace-given <capability>#g<n> "<block>"` puts the new block, checked as `--given`'s, in its
place. A piece the item does not hold is refused, naming it. A universal condition taken out leaves the block's
`retired:` as it is (the block keeps no pairs of a condition and the id it retires)."""
import re
from pathlib import Path

import backlog_forms
from backlog_items import Refused, commit, find, label, one_line
from backlog_section import SECTION, read, render, takes

KINDS = ("universal", "upstream", "given")
FLAGS = tuple("%s_%s" % (verb, kind) for verb in ("remove", "replace") for kind in KINDS)
WORDS = {"universal": "universal condition", "upstream": "upstream entry", "given": "given block"}


def add_arguments(p):
    """`work line`'s options that take an item's own universal condition, upstream entry or given block out, or
    replace it."""
    for kind, metavar, named in (("universal", "U<n>", "the item's universal condition `U<n>`"),
                                 ("upstream", "ID", "the item's upstream entry of the bounded-context id"),
                                 ("given", "CAP#g<n>", "the given block of the item's group `<capability>#g<n>`")):
        p.add_argument("--remove-%s" % kind, metavar=metavar, help="%s, taken out" % named)
        p.add_argument("--replace-%s" % kind, metavar=metavar, help="%s, replaced by the %s given as the text" % (
            named, WORDS[kind]))


def given(args):
    """True when the run is one of this module's."""
    return any(getattr(args, k, None) is not None for k in FLAGS)


def _missing(kind, name):
    raise Refused("work line: the item holds no %s %s" % (WORDS[kind], name), reason="%s not in the item" % WORDS[kind],
                  names=["%s:%s" % (WORDS[kind], name)])


def _universal(blocks, name, new):
    ident = re.sub(r"^universal#", "", name)
    at = next((i for i, (u, _) in enumerate(blocks.universal) if u == ident), None)
    if at is None:
        _missing("universal", name)
    if new is None:
        del blocks.universal[at]
        return
    statement = one_line(new, "universal condition")
    if statement.startswith("#"):
        raise Refused("work line: the universal condition starts with #, which would read as a heading")
    blocks.universal[at] = (ident, statement)


def _upstream(root, blocks, name, new):
    ids = [backlog_forms.UPSTREAM.match(b).group(1) for b in blocks.upstreams]
    if name not in ids:
        _missing("upstream", name)
    at = ids.index(name)
    if new is None:
        del blocks.upstreams[at]
        return
    bullet = backlog_forms.upstream_entry(new)
    ident = backlog_forms.UPSTREAM.match(bullet).group(1)
    index = Path(root) / backlog_forms.INDEX_REL
    known = backlog_forms.upstreams(index.read_text() if index.is_file() else "") + ids[:at] + ids[at + 1:]
    if ident in known:
        raise Refused("work line: the upstream entry %s: %s is an upstream already" % (bullet, ident))
    blocks.upstreams[at] = bullet


def _given(blocks, name, new):
    capability, _, group = name.partition("#")
    block = next((b for b in blocks if b.capability == capability), None)
    at = next((i for i, g in enumerate(block.groups) if g.id == group), None) if block else None
    if at is None or not block.groups[at].given:
        _missing("given", name)
    block.groups[at] = block.groups[at]._replace(given=() if new is None else backlog_forms.given_block(new))


def change(root, name, kind, piece, new=None):
    """The item's piece of `kind` (universal, upstream, given) named `piece` taken out (`new` None) or replaced by
    `new`; committed."""
    item = find(root, name)
    takes(item)
    blocks = read(item, "the item %s" % item.name)
    piece = one_line(piece, WORDS[kind]).strip()
    if kind == "universal":
        _universal(blocks, piece, new)
    elif kind == "upstream":
        _upstream(root, blocks, piece, new)
    else:
        _given(blocks, piece, new)
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s %s the %s %s" % (label(item), "removes" if new is None else "replaces",
                                                       WORDS[kind], piece))
    return item


def cmd(args):
    """`work line` with one of this module's options: one of them, the text only of a replace; what was done,
    printed."""
    flags = [k for k in FLAGS if getattr(args, k, None) is not None]
    from backlog_cli import PIECES
    others = [k for k in PIECES[1:] + ("into", "retires", "reword", "remove", "group", "in_group")
              if getattr(args, k, None) is not None]
    if len(flags) != 1 or others:
        raise Refused("work line: --remove-universal, --replace-universal, --remove-upstream, --replace-upstream, "
                      "--remove-given and --replace-given take one of them, and the text of a replace")
    verb, kind = flags[0].split("_")
    value = getattr(args, flags[0])
    if verb == "remove" and args.text is not None:
        raise Refused("work line: --remove-%s takes no text" % kind)
    if verb == "replace" and not args.text:
        raise Refused("work line: --replace-%s %s takes the %s that replaces it" % (kind, value, WORDS[kind]))
    item = change(args.root, args.name, kind, value, args.text if verb == "replace" else None)
    print("%s: %s %s %s" % (label(item), WORDS[kind], value.strip(), "removed" if verb == "remove" else "replaced"))
    return 0
