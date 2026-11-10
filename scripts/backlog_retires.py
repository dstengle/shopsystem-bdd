"""`work line --retires` (capability readiness, b128): a new line that replaces a live requirement of a codified
capability (design-decision/requirements-retired-never-edited). The new line takes the next id of its capability as
`work line` gives it, and the old id is written under the item's capability block's `retired:` (backlog_section).

Laid over a spec (`lay`), the old line is taken out of the capability's `## Behaviour`, with its group when it was the
group's last line, and its id (and the group's) put into the capability's `retired:`; taken out again (`unlay`), both
are put back, the text read off the file as git last held it with the line in it."""
import re
import subprocess
from pathlib import Path

import spec_read
from backlog_items import Refused, label
from backlog_section import SECTION, capability_file, read, render, takes

IDENT = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)#(r[1-9]\d*)$")
GROUP = r"(?ms)^### \[(g[1-9]\d*)\] [^\n]*\n.*?(?=^### |^## |\Z)"


def _line(rid):
    """A requirement line `- [r<n>] ...` with its continuation lines, and the line break after it."""
    return r"(?m)^- \[%s\] .*(?:\n  .*)*(?:\n|\Z)" % re.escape(rid)


def check(root, item, ident, into=None):
    """The capability and r<n> of `<cap>#r<n>`, the live requirement `work line --retires` retires on the item;
    refused when the capability holds no live requirement of that id, or the item retires it already."""
    takes(item)
    found = IDENT.match(ident or "")
    if not found:
        raise Refused("work line: --retires takes `<capability>#r<n>`, not %s" % ident)
    capability, rid = found.groups()
    if into is not None and into != capability:
        raise Refused("work line: --retires %s goes into %s, not --into %s" % (ident, capability, into))
    try:
        cap = spec_read.capability(capability_file(root, capability))
    except Refused as err:
        raise Refused("work line: %s is nonexistent: %s" % (ident, err)) from None
    if rid not in {r.id for g in cap.groups for r in g.requirements} or rid in cap.retired:
        raise Refused("work line: %s is nonexistent: %s holds no live requirement %s" % (ident, capability, rid))
    if any(b.capability == capability and rid in b.retired for b in read(item, "the item %s" % item.name)):
        raise Refused("work line: %s retires %s already" % (label(item), ident))
    return capability, rid


def with_retired(item, capability, rid):
    """The item's block for `capability` given `rid` under its `retired:`; nothing is committed."""
    blocks = read(item, "the item %s" % item.name)
    at = next(k for k, b in enumerate(blocks) if b.capability == capability)
    blocks[at] = blocks[at]._replace(retired=tuple(blocks[at].retired) + (rid,))
    item.sections[SECTION] = render(blocks)


def _listed(text, ids, drop=False):
    """A capability file's text with `ids` added to (or, `drop`, taken out of) its frontmatter's `retired: [...]`."""
    head_end = text.find("\n---", 4)
    found = re.search(r"(?m)^retired:[ \t]*\[(.*)\][ \t]*$", text[:head_end])
    had = [one.strip() for one in found.group(1).split(",") if one.strip()] if found else []
    kept = [one for one in had if one not in ids] if drop else list(dict.fromkeys(had + list(ids)))
    listed = "retired: [%s]" % ", ".join(kept)
    if found:
        return text[:found.start()] + listed + text[found.end():]
    return text if drop else text[:head_end] + "\n" + listed + text[head_end:]


def _group_of(text, rid):
    """The group chunk of `text` holding the requirement `rid`, as a match, or None."""
    return next((g for g in re.finditer(GROUP, text) if re.search(_line(rid), g.group(0))), None)


def lay(text, capability, rids):
    """The capability file's text with each of `rids` out of its Behaviour and in its `retired:`, the group too when
    the line was its last; refused when a line is not there as a live requirement."""
    gone = []
    for rid in rids:
        chunk = _group_of(text, rid)
        if chunk is None:
            raise Refused("%s#%s is nonexistent: %s holds no live requirement %s" % (capability, rid, capability, rid))
        rest = re.sub(_line(rid), "", chunk.group(0), count=1)
        if re.search(r"(?m)^- \[r[1-9]\d*\] ", rest):
            text = text[:chunk.start()] + rest + text[chunk.end():]
            gone.append(rid)
        else:
            text = text[:chunk.start()] + text[chunk.end():]
            gone += [chunk.group(1), rid]
    return _listed(text, gone)


def _held(path, rid):
    """The text of `path` as git last held it with the requirement `rid` in it; refused when it never did."""
    path = Path(path)

    def git(*args):
        return subprocess.run(["git", "-C", str(path.parent), *args], capture_output=True, text=True)
    rel = git("ls-files", "--full-name", "--error-unmatch", path.name)
    log = git("log", "--format=%H", "--", path.name) if rel.returncode == 0 else rel
    for sha in log.stdout.split() if log.returncode == 0 else ():
        shown = git("show", "%s:%s" % (sha, rel.stdout.strip()))
        if shown.returncode == 0 and _group_of(shown.stdout, rid) is not None:
            return shown.stdout
    raise Refused("the retired line %s of %s is in no version git holds of it" % (rid, path))


def unlay(path, text, rids):
    """The reverse of `lay`: each of `rids` put back into its group (by number), or its group put back whole (before
    the first group numbered above it, else at the end of `## Behaviour`), and the ids out of `retired:`."""
    back = []
    for rid in rids:
        if _group_of(text, rid) is not None:
            continue
        chunk = _group_of(_held(path, rid), rid)
        gid, line = chunk.group(1), re.search(_line(rid), chunk.group(0)).group(0)
        here = next((g for g in re.finditer(GROUP, text) if g.group(1) == gid), None)
        back.append(rid)
        if here is not None:
            after = [m for m in re.finditer(r"(?m)^- \[r([1-9]\d*)\] .*(?:\n  .*)*\n?", here.group(0))
                     if int(m.group(1)) < int(rid[1:])]
            at = here.start() + (after[-1].end() if after else here.group(0).index("\n") + 1)
            text = text[:at] + (line if line.endswith("\n") else line + "\n") + text[at:]
            continue
        back.append(gid)
        later = [g for g in re.finditer(GROUP, text) if int(g.group(1)[1:]) > int(gid[1:])]
        if later:
            at = later[0].start()
        else:
            end = re.search(r"(?ms)^## Behaviour[ \t]*\n.*?(?=^## |\Z)", text)
            at = end.end() if end else len(text)
        whole = chunk.group(0) if chunk.group(0).endswith("\n\n") else chunk.group(0).rstrip("\n") + "\n\n"
        text = text[:at] + whole + text[at:]
    return _listed(text, back, drop=True)
