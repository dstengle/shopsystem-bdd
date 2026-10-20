"""The work-queue of a bounded context in .shop/work/: the library behind scripts/work (capability work-queue).

Standard library only. Frontmatter is read with scripts/model's own reader, so the two never disagree on a file.
"""
import datetime
import importlib.machinery
import importlib.util
import json
import os
import re
from pathlib import Path

WORK = Path(".shop") / "work"


def _load_model():
    path = Path(__file__).resolve().with_name("model")
    loader = importlib.machinery.SourceFileLoader("shopsystem_model", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


frontmatter = _load_model().frontmatter


class Refused(Exception):
    """What work was asked cannot be done; the message says why, and nothing was changed."""


def context_path(root):
    """The <owner>/<product>/<context name> of spec/index.md's bounded-context id."""
    index = Path(root) / "spec" / "index.md"
    if not index.is_file():
        raise Refused("spec/index.md, which names the context, is missing")
    data, _ = frontmatter(read(index, root))
    ident = data.get("id")
    if not isinstance(ident, str) or "/" not in ident:
        raise Refused("spec/index.md gives no bounded-context id (bounded-context/<owner>/<product>/<context>)")
    return ident.split("/", 1)[1]


def read(path, root):
    """The text of `path`; a file that is not UTF-8 text is refused, naming it."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise Refused("%s is not UTF-8 text" % path.relative_to(root)) from None


def entry(word, what):
    """`word` as one directory entry of .shop/work/: refused when it is a path, or . or .."""
    if word in ("", ".", "..") or "/" in word or "\\" in word:
        raise Refused("the %s %s is not a %s" % (what, word, "file name" if what == "name" else "name"))


def add(root, initiative, name, part_of, under, accepts):
    """Write .shop/work/<initiative>/<name>.md as a drafted work-item (r1)."""
    entry(initiative, "initiative")
    entry(name, "name")
    for option, value in (("--part-of", part_of), ("--under", under)) + tuple(("--accepts", a) for a in accepts):
        if "\n" in value or "\r" in value:
            raise Refused("the value of %s has a newline in it; a work-item's field is one line" % option)
    path = Path(root) / WORK / initiative / (name + ".md")
    if not path.parent.is_dir():
        raise Refused("the initiative %s does not exist (no %s)" % (initiative, path.parent.relative_to(root)))
    if path.exists():
        raise Refused("%s already exists; work add leaves it as it was" % path.relative_to(root))
    text = ("---\nid: work-item/%s/%s\nkind: work-item\npart_of: %s\nstatus: drafted\nunder: %s\naccepts: [%s]\n---\n\n# %s\n"
            % (context_path(root), name, part_of, under, ", ".join(accepts), name))
    path.write_text(text)
    return path


def items(root):
    """Each work-item of every initiative under .shop/work/: (initiative, name, status), in path order (r3)."""
    for path in sorted((Path(root) / WORK).glob("*/*.md")):
        data, _ = frontmatter(read(path, root))
        if data.get("kind") == "work-item":
            yield path.parent.name, path.stem, data.get("status")


def last_logged(log, name, root):
    """The status the last move `log` gives for work-item `name` moved it to; None when no move names it.

    A line with no `after` (work run's start and end of a worker) is no move. A line that is not a JSON object is refused.
    """
    last = None
    if log.exists():
        for number, line in enumerate(read(log, root).splitlines(), 1):
            try:
                line = json.loads(line)
            except ValueError:
                line = None
            if not isinstance(line, dict):
                raise Refused("line %d of %s is not a JSON object; no move is made" % (number, log.relative_to(root)))
            if line.get("work-item") == name and "after" in line:
                last = line["after"]
    return last


def move(root, initiative, name, status, by):
    """Move a work-item to `status`, as `by`: work run's way through the lifecycle.

    The file gets the new status (r4), then log.jsonl the move's line (r5): a move and its file are written
    together, the log line last, and a log line that cannot be written puts the file back (r7). A file whose status
    is not the last one log.jsonl gives it is refused (r6), and so is a file with no status.
    """
    path = Path(root) / WORK / initiative / (name + ".md")
    before = agrees(root, initiative, name)
    text = read(path, root)
    end = text.find("\n---", 4)
    head = re.sub(r"(?m)^status:.*$", "status: " + status, text[:end], count=1)
    line = {"time": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "work-item": name,
            "before": before, "after": status, "by": by}
    log = path.parent / "log.jsonl"
    path.write_text(head + text[end:])
    try:
        append(log, (json.dumps(line) + "\n").encode())
    except OSError as error:
        path.write_text(text)
        raise Refused("%s cannot be written (%s); %s is left as it was"
                      % (log.relative_to(root), error.strerror, path.relative_to(root))) from None


def append(log, data):
    """Append `data` to `log` whole or not at all: a write that fails part-way is cut back to the size before it."""
    fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        size = os.fstat(fd).st_size
        try:
            written = 0
            while written < len(data):
                written += os.write(fd, data[written:])
        except OSError:
            os.ftruncate(fd, size)
            raise
    finally:
        os.close(fd)


def agrees(root, initiative, name):
    """The status of work-item `name`, once its file holds one and log.jsonl's last move of it agrees (r6); else refused."""
    path = Path(root) / WORK / initiative / (name + ".md")
    if not path.is_file():
        raise Refused("%s does not exist; there is no work-item %s to move" % (path.relative_to(root), name))
    data, _ = frontmatter(read(path, root))
    before = data.get("status")
    if not isinstance(before, str) or not before:
        raise Refused("%s has no status in its frontmatter; it is not moved" % path.relative_to(root))
    logged = last_logged(path.parent / "log.jsonl", name, root)
    if logged is not None and logged != before:
        raise Refused("%s gives its status as %s, but log.jsonl's last move of %s is to %s; it is not moved"
                      % (path.relative_to(root), before, name, logged))
    return before
