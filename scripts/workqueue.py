"""The work-queue of a bounded context in .shop/work/: the library behind scripts/work (capability work-queue).

Standard library only. Frontmatter is read with scripts/model's own reader, so the two never disagree on a file.
"""
import datetime
import importlib.machinery
import importlib.util
import json
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
    data, _ = frontmatter(index.read_text())
    return data["id"].split("/", 1)[1]


def add(root, initiative, name, part_of, under, accepts):
    """Write .shop/work/<initiative>/<name>.md as a drafted work-item (r1)."""
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
        data, _ = frontmatter(path.read_text())
        if data.get("kind") == "work-item":
            yield path.parent.name, path.stem, data.get("status")


def last_logged(log, name):
    """The status the last line of `log` for work-item `name` moved it to; None when no line names it."""
    last = None
    if log.exists():
        for line in log.read_text().splitlines():
            entry = json.loads(line)
            if entry.get("work-item") == name:
                last = entry.get("after")
    return last


def move(root, initiative, name, status, by):
    """Move a work-item to `status`, as `by`: work run's way through the lifecycle.

    The file gets the new status (r4), then log.jsonl the move's line (r5): a move and its file are written
    together, the log line last. A file whose status is not the last one log.jsonl gives it is refused (r6).
    """
    path = Path(root) / WORK / initiative / (name + ".md")
    if not path.is_file():
        raise Refused("%s does not exist; there is no work-item %s to move" % (path.relative_to(root), name))
    text = path.read_text()
    before = frontmatter(text)[0].get("status")
    logged = last_logged(path.parent / "log.jsonl", name)
    if logged is not None and logged != before:
        raise Refused("%s gives its status as %s, but log.jsonl's last move of %s is to %s; it is not moved"
                      % (path.relative_to(root), before, name, logged))
    end = text.find("\n---", 4)
    head = re.sub(r"(?m)^status:.*$", "status: " + status, text[:end], count=1)
    path.write_text(head + text[end:])
    line = {"time": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "work-item": name,
            "before": before, "after": status, "by": by}
    with open(path.parent / "log.jsonl", "a") as log:
        log.write(json.dumps(line) + "\n")
