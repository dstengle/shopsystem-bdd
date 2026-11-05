"""`measure defect <item> --says TEXT` (capability telemetry r3; workflow simplification plan 7, D11): a fault found
after the merge, written `.shop/batches/<n>/defect-<k>.md` against its delivered item and its merged batch and
committed alone on the current branch, and a batch's defects read back. `parse(render(d), rel) == d`; any other shape
is refused as `<rel>: <field> ...`. Standard library only."""
import datetime
import re
from dataclasses import dataclass
from pathlib import Path

import backlog_items
import batch_git
import batch_plan
import shop_files
from transcripts import Refused

COMMAND = "measure defect"


@dataclass
class Defect:
    name: str
    ident: str
    batch: str
    item: str
    date: str
    says: str


def rel_of(batch_name, k):
    return (batch_plan.BATCHES / str(batch_plan.number(batch_name)) / ("defect-%d.md" % k)).as_posix()


def render(defect):
    return ("---\nid: %s\nkind: defect\nbatch: %s\nitem: %s\ndate: %s\n---\n\n# %s %s\n\n%s\n" % (
        defect.ident, defect.batch, defect.item, defect.date, defect.batch, defect.name, defect.says))


def parse(text, rel):
    try:
        data, body = shop_files.frontmatter(text)
    except shop_files.Refused as why:
        raise Refused("%s: %s" % (rel, why)) from None
    ident = data.get("id")
    m = re.fullmatch(r"defect/.+/(batch-[1-9]\d*)/(d[1-9]\d*)", ident) if isinstance(ident, str) else None
    if not m:
        raise Refused("%s: id %r is not defect/<context path>/batch-<n>/d<k>" % (rel, ident))
    if data.get("kind") != "defect":
        raise Refused("%s: kind %r is not defect" % (rel, data.get("kind")))
    if data.get("batch") != m.group(1):
        raise Refused("%s: batch %r is not %s" % (rel, data.get("batch"), m.group(1)))
    if rel != rel_of(m.group(1), int(m.group(2)[1:])):
        raise Refused("%s: id: %s is not the defect of this file" % (rel, ident))
    if not backlog_items.is_item(data.get("item")):
        raise Refused("%s: item %r is not b<n>" % (rel, data.get("item")))
    date = str(data.get("date"))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise Refused("%s: date %r is not YYYY-MM-DD" % (rel, data.get("date")))
    title, _, says = body.strip("\n").partition("\n")
    if title.strip() != "# %s %s" % m.groups():
        raise Refused("%s: title: the body does not start with %r" % (rel, "# %s %s" % m.groups()))
    if not says.strip():
        raise Refused("%s: says: the defect has no text" % rel)
    return Defect(m.group(2), ident, m.group(1), data["item"], date, says.strip("\n"))


def defects(root, batch_name):
    """The batch's defects, by k; a `defect-*.md` not named `defect-<k>.md` is refused."""
    folder = Path(root) / batch_plan.BATCHES / str(batch_plan.number(batch_name))
    found = []
    for path in folder.glob("defect-*.md"):
        rel = path.relative_to(root).as_posix()
        if not re.fullmatch(r"defect-[1-9]\d*\.md", path.name):
            raise Refused("%s: id: the file name is not defect-<k>.md" % rel)
        found.append(parse(shop_files.read(path, root), rel))
    return sorted(found, key=lambda d: int(d.name[1:]))


def record(root, item_name, says):
    """D11: the defect of a delivered item of a merged batch written and committed; its rel path. Refused, changing
    nothing, for empty `says`, an item in no batch, or an item not delivered or of a batch not merged."""
    try:
        return _record(root, item_name, says)
    except shop_files.Refused as why:
        raise Refused(str(why)) from None


def _record(root, item_name, says):
    if not says.strip():
        raise Refused("--says is empty; say the fault and how to reproduce it")
    item = backlog_items.find(root, item_name)
    with batch_git.locked(root):
        batch = batch_plan.of_item(root, item.name)
        if batch is None:
            raise Refused("%s is in no batch; a defect is of a delivered item of a merged batch" %
                          backlog_items.label(item))
        if item.status != "delivered" or batch.status != "merged":
            raise Refused("%s is %s in %s, which is %s; a defect is of a delivered item of a merged batch" % (
                backlog_items.label(item), item.status, batch.name, batch.status))
        k = max((int(d.name[1:]) for d in defects(root, batch.name)), default=0) + 1
        context = shop_files.context_path(root)
        defect = Defect("d%d" % k, "defect/%s/%s/d%d" % (context, batch.name, k), batch.name, item.name,
                        datetime.date.today().isoformat(), says.strip())
        rel = rel_of(batch.name, k)

        def write():
            path = Path(root) / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render(defect), encoding="utf-8")
        shop_files.committed(root, [rel], "%s: %s %s of %s" % (COMMAND, batch.name, defect.name,
                                                             backlog_items.label(item)), write)
    return rel
