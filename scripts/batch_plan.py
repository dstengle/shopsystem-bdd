"""The batch and its plan, one file `.shop/batches/<n>/plan.md` (capability batches; workflow simplification plan 4,
D3, D4, D9, D18): its frontmatter (status, base branch, the commit it forked from, its branch, its pull request), a
`## Tasks` table of one task for each item, and a `## Plan` kept byte for byte (the batch session's notes).

`parse(render(batch), rel) == batch`; any other shape is refused as `<rel>: <field> ...`, never skipped. The file is
committed on the base branch only, with the items it moves."""
import re
from dataclasses import dataclass, field
from pathlib import Path

import backlog_items
import shop_files
from batch_git import current_branch
from shop_files import Refused

BATCHES = Path(".shop") / "batches"
STATUSES = ("building", "in-review", "awaiting-merge", "merged", "abandoned")
OPEN = STATUSES[:3]
TASK_STATUSES = ("pending", "running", "done", "failed")
PLAN = ("One task for each item: each builds its item's requirement lines, whose generated scenarios are its "
        "acceptance tests.")
HEAD = "| task | item | status | branch |\n|---|---|---|---|"


@dataclass
class Task:
    task: str
    item: str
    status: str
    branch: str


@dataclass
class Batch:
    name: str
    ident: str
    status: str
    base: str
    forked_from: str
    branch: str
    pull_request: str | None
    tasks: list = field(default_factory=list)
    plan: str = PLAN


def is_batch(name):
    return bool(re.fullmatch(r"batch-[1-9]\d*", name or ""))


def number(name):
    return int(name.split("-", 1)[1])


def rel_of(name):
    return (BATCHES / str(number(name)) / "plan.md").as_posix()


def _sections(body, rel):
    lines = body.strip("\n").split("\n")
    if not lines or not lines[0].startswith("# ") or not lines[0][2:].strip():
        raise Refused("%s: title: the file has no `# ` heading first in its body" % rel)
    found, heading = {}, None
    for line in lines[1:]:
        if line.startswith("## "):
            heading = line[3:].strip()
            found[heading] = []
        elif heading is not None:
            found[heading].append(line)
        elif line.strip():
            raise Refused("%s: title: text between the `# ` heading and the first `## ` section" % rel)
    return lines[0][2:].strip(), {h: "\n".join(b).strip("\n") for h, b in found.items()}


def _tasks(text, rel):
    rows = [line for line in text.split("\n") if line.strip()]
    if rows[:2] != HEAD.split("\n"):
        raise Refused("%s: tasks: the table has no header `%s`" % (rel, HEAD.split("\n")[0]))
    tasks = []
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if not row.strip().startswith("|") or len(cells) != 4:
            raise Refused("%s: tasks: the row %s does not have 4 cells" % (rel, row))
        tid, item, status, branch = cells
        if not re.fullmatch(r"t[1-9]\d*", tid) or not backlog_items.is_item(item) or not branch:
            raise Refused("%s: tasks: the row %s is not `| t<k> | b<j> | <status> | <branch> |`" % (rel, row))
        if status not in TASK_STATUSES:
            raise Refused("%s: tasks: the status %r of %s is not one of %s" % (rel, status, tid, ", ".join(TASK_STATUSES)))
        if any(t.task == tid for t in tasks):
            raise Refused("%s: tasks: the task %s is there twice" % (rel, tid))
        tasks.append(Task(tid, item, status, branch))
    return tasks


def parse(text, rel):
    data, body = shop_files.frontmatter(text)
    ident = data.get("id")
    if not isinstance(ident, str) or not ident.startswith("batch/") or not is_batch(ident.rsplit("/", 1)[-1]):
        raise Refused("%s: id %r is not batch/<context path>/batch-<n>" % (rel, ident))
    if data.get("kind") != "batch":
        raise Refused("%s: kind %r is not batch" % (rel, data.get("kind")))
    if data.get("status") not in STATUSES:
        raise Refused("%s: status %r is not one of %s" % (rel, data.get("status"), ", ".join(STATUSES)))
    for key in ("base", "forked_from", "branch"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise Refused("%s: %s is not given" % (rel, key))
    title, sections = _sections(body, rel)
    name = ident.rsplit("/", 1)[-1]
    if title != name:
        raise Refused("%s: title %r is not the batch's name %s" % (rel, title, name))
    return Batch(name=name, ident=ident, status=data["status"], base=data["base"], forked_from=data["forked_from"],
                 branch=data["branch"], pull_request=data.get("pull_request") or None,
                 tasks=_tasks(sections.get("Tasks", ""), rel), plan=sections.get("Plan", ""))


def render(batch):
    head = ["id: %s" % batch.ident, "kind: batch", "status: %s" % batch.status, "base: %s" % batch.base,
            "forked_from: %s" % batch.forked_from, "branch: %s" % batch.branch,
            "pull_request:%s" % (" %s" % batch.pull_request if batch.pull_request else "")]
    rows = "".join("\n| %s | %s | %s | %s |" % (t.task, t.item, t.status, t.branch) for t in batch.tasks)
    return "---\n%s\n---\n\n# %s\n\n## Tasks\n\n%s%s\n\n## Plan\n\n%s\n" % (
        "\n".join(head), batch.name, HEAD, rows, batch.plan)


def names(root):
    """The `batch-<n>` of each `.shop/batches/<n>/plan.md`, by number; one not named by a number is refused."""
    found = []
    for path in (Path(root) / BATCHES).glob("*/plan.md"):
        if not re.fullmatch(r"[1-9]\d*", path.parent.name):
            raise Refused("%s: id: the directory name is not a number" % path.relative_to(root).as_posix())
        found.append("batch-%s" % path.parent.name)
    return sorted(found, key=number)


def load(root, name):
    rel = rel_of(name)
    batch = parse(shop_files.read(Path(root) / rel, root), rel)
    if batch.name != name:
        raise Refused("%s: id %s does not end in %s" % (rel, batch.ident, name))
    return batch


def batches(root):
    return [load(root, name) for name in names(root)]


def find(root, name):
    if not is_batch(name) or not (Path(root) / rel_of(name)).is_file():
        raise Refused("there is no batch %s in %s/" % (name, BATCHES.as_posix()))
    return load(root, name)


def open_batch(root):
    """The batch that is `building`, `in-review` or `awaiting-merge`, or None (D9)."""
    return next((b for b in batches(root) if b.status in OPEN), None)


def next_name(root):
    return "batch-%d" % (max(map(number, names(root)), default=0) + 1)


def task(batch, tid, command="work batch"):
    found = next((t for t in batch.tasks if t.task == tid), None)
    if found is None:
        raise Refused("%s: %s has no task %s" % (command, batch.name, tid))
    return found


def of_item(root, item_name):
    """The highest-numbered batch whose tasks name the item, or None."""
    return next((b for b in reversed(batches(root)) if any(t.item == item_name for t in b.tasks)), None)


def on_base(root, batch):
    """Refused unless `root` is on the batch's base branch (D18)."""
    branch = current_branch(root)
    if branch != batch.base:
        raise Refused("work batch: %s is built from %s; run it on %s, not %s" % (
            batch.name, batch.base, batch.base, branch or "a detached HEAD"))


def commit(root, batch, items, message, files=None):
    """`plan.md`, each item's file and each of `files` ({rel: text}) written and committed together on the current
    branch; the caller holds `batch_git.locked`."""
    files = files or {}
    rels = [rel_of(batch.name)] + [backlog_items.rel_of(i.name) for i in items] + list(files)

    def write():
        path = Path(root) / rels[0]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(batch), encoding="utf-8")
        for item in items:
            (Path(root) / backlog_items.rel_of(item.name)).write_text(backlog_items.render(item), encoding="utf-8")
        for rel, text in files.items():
            (Path(root) / rel).parent.mkdir(parents=True, exist_ok=True)
            (Path(root) / rel).write_text(text, encoding="utf-8")
    shop_files.committed(root, rels, message, write)
