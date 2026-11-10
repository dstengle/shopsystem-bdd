"""`work line --recodify universal` and `work line --universal --retires universal#U<n>` (capability readiness, b220):
spec/universal.md switched to the new language on an item, and a new universal condition that replaces a live one
(design-decision/requirements-retired-never-edited), each written into the item's `### universal` block
(backlog_section): its `language: codified-2` line, and the old U id under its `retired:` line.

Laid over a spec (`lay`), spec/universal.md's frontmatter says `language: codified-2`, and each retired condition is
taken out of its `## Behaviour` and its id put into its `retired:`; taken out again (`unlay`), the marker says
`codified-1` again and each retired condition is put back (by number), its text read off the file as git last held it
with the condition in it."""
import re
import subprocess
from pathlib import Path

import backlog_recodify
import backlog_retires
import spec_read
from backlog_items import Refused, label
from backlog_section import SECTION, UNIVERSAL, read, render, takes

REL = "spec/universal.md"
IDENT = re.compile(r"^universal#(U[1-9]\d*)$")


def _line(uid):
    """A universal condition `- [U<n>] ...` with its continuation lines, and the line break after it."""
    return r"(?m)^- \[%s\] .*(?:\n  .*)*(?:\n|\Z)" % re.escape(uid)


def check_recodify(root, item):
    """Refused unless the item takes lines, spec/universal.md is there in the old language, and the item does not
    switch it already."""
    takes(item)
    path = Path(root) / REL
    if not path.is_file():
        raise Refused("work line: there is no %s to recodify" % REL)
    if not spec_read.codified(path, (backlog_recodify.OLD,)):
        raise Refused("work line: %s does not say `language: %s`" % (REL, backlog_recodify.OLD))
    if read(item, "the item %s" % item.name).universal_language:
        raise Refused("work line: %s recodifies %s already" % (label(item), UNIVERSAL))


def with_language(item):
    """The item's universal block given the marker; nothing is committed."""
    blocks = read(item, "the item %s" % item.name)
    blocks.universal_language = backlog_recodify.MARKER
    item.sections[SECTION] = render(blocks)


def check_retires(root, item, ident):
    """The U<n> of `universal#U<n>`, the live universal condition the item's new one retires; refused, naming it, when
    spec/universal.md holds no live condition of that id, or the item retires it already."""
    takes(item)
    found = IDENT.match(ident or "")
    if not found:
        raise Refused("work line: --retires with --universal takes `universal#U<n>`, not %s" % ident)
    uid = found.group(1)
    held = spec_read.read_universal(root)
    if uid not in {u.id for u in held.conditions}:
        raise Refused("work line: %s is nonexistent: %s holds no live universal condition %s" % (ident, REL, uid))
    if uid in read(item, "the item %s" % item.name).universal_retired:
        raise Refused("work line: %s retires %s already" % (label(item), ident))
    return uid


def lay(into, blocks, files):
    """The universal block's marker and retired conditions laid onto `into/spec/universal.md`; its path added to
    `files` when it changed."""
    path = Path(into) / REL
    if not (blocks.universal_language or blocks.universal_retired) or not path.is_file():
        return
    text = was = path.read_text()
    for uid in blocks.universal_retired:
        found = re.search(_line(uid), text)
        if found is None:
            raise Refused("universal#%s is nonexistent: %s holds no live universal condition %s" % (uid, REL, uid))
        text = text[:found.start()] + text[found.end():]
    text = backlog_retires._listed(text, blocks.universal_retired)
    text = backlog_recodify.lay(text) if blocks.universal_language else text
    _write(path, text, was, files)


def _held(path, uid):
    """The line of the condition `uid` as git last held it in `path`; refused when it never did."""
    def git(*args):
        return subprocess.run(["git", "-C", str(path.parent), *args], capture_output=True, text=True)
    rel = git("ls-files", "--full-name", "--error-unmatch", path.name)
    log = git("log", "--format=%H", "--", path.name) if rel.returncode == 0 else rel
    for sha in log.stdout.split() if log.returncode == 0 else ():
        shown = git("show", "%s:%s" % (sha, rel.stdout.strip()))
        found = re.search(_line(uid), shown.stdout) if shown.returncode == 0 else None
        if found is not None:
            return found.group(0) if found.group(0).endswith("\n") else found.group(0) + "\n"
    raise Refused("the retired universal condition %s is in no version git holds of %s" % (uid, path))


def unlay(into, blocks, files):
    """The reverse of `lay`: each retired condition put back before the first condition numbered above it (else after
    the last), its id out of `retired:`, and the marker `codified-1` again."""
    path = Path(into) / REL
    if not (blocks.universal_language or blocks.universal_retired) or not path.is_file():
        return
    text = was = path.read_text()
    back = []
    for uid in blocks.universal_retired:
        if re.search(_line(uid), text) is not None:
            continue
        line, back = _held(path, uid), back + [uid]
        conditions = list(re.finditer(r"(?m)^- \[U([1-9]\d*)\] .*(?:\n  .*)*\n?", text))
        later = [m for m in conditions if int(m.group(1)) > int(uid[1:])]
        if later:
            at = later[0].start()
        elif conditions:
            at = conditions[-1].end()
            line = line if text[:at].endswith("\n") else "\n" + line
        else:
            text = text.rstrip("\n") + "\n\n"
            at = len(text)
        text = text[:at] + line + text[at:]
    text = backlog_retires._listed(text, back, drop=True)
    text = backlog_recodify.unlay(text) if blocks.universal_language else text
    _write(path, text.rstrip("\n") + "\n", was, files)


def _write(path, text, was, files):
    if text != was:
        path.write_text(text)
        if REL not in files:
            files.append(REL)
