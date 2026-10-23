"""The work-queue of a bounded context in .shop/work/: the library behind scripts/work (capability work-queue).

Standard library only. Frontmatter is read with scripts/model's own reader, so the two never disagree on a file.
"""
import datetime
import importlib.machinery
import importlib.util
import json
import os
import re
import subprocess
from pathlib import Path

WORK = Path(".shop") / "work"
# The statuses of the work-item lifecycle (design-decision/work-item-lifecycle-as-run); a move to any other is refused.
STATUSES = ("drafted", "researched", "planned", "ready", "claimed", "done", "green", "awaiting-answer", "withdrawn",
            "failed")


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
        raise Refused("the %s %s is not a name" % (what, word))


def highest(root):
    """The highest <n> of any work-item under .shop/work/, by its id's w<n> and its file's; 0 when there is none (r12)."""
    numbers = []
    for path in sorted((Path(root) / WORK).glob("*/*.md")):
        data, _ = frontmatter(read(path, root))
        if data.get("kind") == "work-item":
            for word in (path.stem, str(data.get("id", "")).rsplit("/", 1)[-1]):
                if re.fullmatch(r"w\d+", word):
                    numbers.append(int(word[1:]))
    return max(numbers, default=0)


def add(root, initiative, title, part_of, under, accepts):
    """Write .shop/work/<initiative>/w<n>.md as a drafted work-item titled `title`, <n> one above the highest; return w<n> (r1, r12)."""
    entry(initiative, "initiative")
    if title == "":
        raise Refused("the title is empty; a work-item needs a title for its heading")
    if "\n" in title or "\r" in title:
        raise Refused("the title has a newline in it; a work-item's heading is one line")
    for option, value in (("--part-of", part_of), ("--under", under)) + tuple(("--accepts", a) for a in accepts):
        if "\n" in value or "\r" in value:
            raise Refused("the value of %s has a newline in it; a work-item's field is one line" % option)
    directory = Path(root) / WORK / initiative
    if not directory.is_dir():
        raise Refused("the initiative %s does not exist (no %s)" % (initiative, directory.relative_to(root)))
    context = context_path(root)
    name = "w%d" % (highest(root) + 1)
    path = directory / (name + ".md")
    if path.exists():
        raise Refused("%s is a file that is not a work-item, and work add would number the new work-item %s; "
                      "work add leaves it as it was" % (path.relative_to(root), name))
    text = ("---\nid: work-item/%s/%s\nkind: work-item\npart_of: %s\nstatus: drafted\nunder: %s\naccepts: [%s]\n---\n\n# %s\n"
            % (context, name, part_of, under, ", ".join(accepts), title))
    rel = str(path.relative_to(root))
    committed(root, [rel], "work add: %s/%s drafted" % (initiative, name), lambda: path.write_text(text))
    return name


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
    if status not in STATUSES:
        raise Refused("%s is no status of the work-item lifecycle; %s is not moved" % (status, name))
    before = agrees(root, initiative, name)
    text = read(path, root)
    end = text.find("\n---", 4)
    head = re.sub(r"(?m)^status:.*$", "status: " + status, text[:end], count=1)
    line = {"time": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds"), "work-item": name,
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
        raise Refused("%s gives its status as %s, but log.jsonl's last transition of %s is to %s; it is not moved"
                      % (path.relative_to(root), before, name, logged))
    return before


def retry(root, name):
    """Move the failed work-item `name` back to the status log.jsonl gives before its last transition into failed (r8)."""
    found = [find(root, name)]
    initiative = found[0].parent.name
    if agrees(root, initiative, name) != "failed":
        raise Refused("%s is not failed; work retry returns only a failed work-item" % name)
    moves = [line for line in logged(found[0].parent / "log.jsonl", root) if line.get("work-item") == name and "after" in line]
    at = max((i for i, line in enumerate(moves) if line["after"] == "failed"), default=None)
    if at is None:
        raise Refused("log.jsonl gives no transition of %s to failed; work retry has no status to return it to" % name)
    before = moves[at]["before"]
    committed(root, rels_of(root, found[0]), "work retry: %s failed -> %s" % (name, before),
              lambda: move(root, initiative, name, before, by="work retry"))
    return before


def rels_of(root, path):
    """The work-item file `path` and its initiative's log.jsonl, relative to `root`."""
    return [str(p.relative_to(root)) for p in (path, path.parent / "log.jsonl")]


def find(root, name):
    """The one file of work-item `name` under .shop/work/; else refused."""
    found = sorted((Path(root) / WORK).glob("*/%s.md" % name)) if "/" not in name else []
    if len(found) != 1:
        raise Refused("there is %s work-item %s under %s" % ("no" if not found else "more than one", name, WORK))
    return found[0]


def withdraw(root, name):
    """Move the work-item `name`, when it is neither claimed nor green, to withdrawn (r10)."""
    path = find(root, name)
    status = agrees(root, path.parent.name, name)
    if status == "withdrawn":
        raise Refused("%s is already withdrawn; there is nothing to transition" % name)
    if status in ("claimed", "green"):
        raise Refused("%s is %s; work withdraw leaves a claimed or green work-item as it is" % (name, status))
    committed(root, rels_of(root, path), "work withdraw: %s %s -> withdrawn" % (name, status),
              lambda: move(root, path.parent.name, name, "withdrawn", by="work withdraw"))
    return "withdrawn"


def git(root, *args):
    """Run git in `root`; a git that fails is refused, with git's first line of complaint."""
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        said = (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise Refused("git %s failed: %s" % (args[0], said))
    return done.stdout


def committed(root, rels, message, write):
    """Make the change `write` makes to the files `rels` (relative to `root`), then commit them, and only them, on the
    current branch (r9). A repository git cannot commit in is refused before anything is written, and a commit that
    fails puts the files back as they were (r7)."""
    git(root, "rev-parse", "--is-inside-work-tree")
    paths = [Path(root) / rel for rel in rels]
    before = [p.read_bytes() if p.exists() else None for p in paths]
    write()
    try:
        git(root, "add", "--", *rels)
        git(root, "commit", "-q", "-m", message, "--", *rels)
    except Refused:
        for path, data in zip(paths, before):
            path.unlink(missing_ok=True) if data is None else path.write_bytes(data)
        subprocess.run(["git", "reset", "-q", "--", *rels], cwd=root, capture_output=True)
        raise


def logged(log, root):
    """The lines of `log` that are JSON objects."""
    lines = []
    for line in read(log, root).splitlines() if log.exists() else []:
        try:
            lines.append(json.loads(line))
        except ValueError:
            continue
    return [line for line in lines if isinstance(line, dict)]
