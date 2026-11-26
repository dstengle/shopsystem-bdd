"""`work record --design` and `work record --plan` (records r7, r4, r8, b475): a design filed as the folder
`.shop/records/<date>-<slug>/`, its `design.md` written whole (frontmatter id, kind `design`, about, date, and
`# <title>` over the body a file gives) with its row in `.shop/records/README.md`, both committed (`design`); a plan
filed as `plan-<k>.md` in the folder of its design, `# <title>` over its body, k the next number of the folder's
plans, and committed (`plan`). A design whose folder exists is refused, since a committed record is never edited,
and so is a plan whose design does not exist, naming the design."""
import datetime
import re
from pathlib import Path

import record_write
from plumbing import shop_files

RECORDS = record_write.RECORDS


def dated(date):
    date = date or datetime.date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", date):
        raise shop_files.Refused("the date %s is not YYYY-MM-DD" % date, reason="not a date", names=["parameter:date"])
    return date


def text_of(body):
    """The text of the file `body`, refused naming the option when there is no such file."""
    path = Path(body)
    if not path.is_file():
        raise shop_files.Refused("{names}: no file %s" % body, reason="no such file", names=["parameter:body"])
    return shop_files.read(path, path.parent).strip()


def design(root, title, summary, body, *, about=None, slug=None, date=None):
    """The operation records.file design: the design's folder with its `design.md` and its row in the records index,
    committed; the path of `design.md`, relative to the root."""
    root = Path(root)
    title, summary = record_write.one_line(title, "title"), record_write.one_line(summary, "summary").replace("|", "\\|")
    date, text = dated(date), text_of(body)
    slug = record_write.slugged(slug, title)
    name, path = "%s-%s" % (date, slug), shop_files.context_path(root)
    folder = RECORDS / name
    if (root / folder).exists():
        raise shop_files.Refused("%s exists, and a committed record is never edited: give another {names}"
                                 % folder.as_posix(), reason="record exists", names=["parameter:slug"])
    about = record_write.attributed(about, root) if about is not None else "bounded-context/%s" % path
    rel, readme = (folder / "design.md").as_posix(), (RECORDS / "README.md").as_posix()
    content = ("---\nid: record/%s/%s\nkind: design\nabout: %s\ndate: %s\n---\n\n# %s\n\n%s\n"
               % (path, name, about, date, title, text))
    row = "| `%s/design.md` | %s | design |\n" % (name, summary)
    current = shop_files.read(root / readme, root) if (root / readme).is_file() else record_write.README_HEAD

    def put():
        (root / folder).mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(content, encoding="utf-8")
        (root / readme).write_text(record_write.with_row(current, row), encoding="utf-8")
    shop_files.committed(root, [rel, readme], "work record: the design %s" % name, put)
    return rel


def folder_of(root, ref):
    """The folder (relative to the root) of the design `ref` names: its folder's name `<date>-<topic>`, its path, the
    path of its `design.md` or its id `record/<path>/<date>-<topic>`; refused naming the design when it holds no
    `design.md`."""
    name = re.sub(r"/design\.md$", "", ref.strip()).rstrip("/").rpartition("/")[2]
    folder = RECORDS / name
    if not name or name in (".", "..") or not (Path(root) / folder / "design.md").is_file():
        raise shop_files.Refused("{names} %r: no design %s/design.md" % (ref, folder.as_posix()),
                                 reason="design that does not exist", names=["parameter:design"])
    return folder


def plan(root, title, design_ref, body):
    """The operation records.file plan: `plan-<k>.md` in the folder of the design, committed; its path, relative to
    the root."""
    root = Path(root)
    title = record_write.one_line(title, "title")
    folder = folder_of(root, design_ref)
    text = text_of(body)
    taken = [int(m.group(1)) for p in (root / folder).iterdir() if (m := re.match(r"plan-(\d+)\b", p.name))]
    rel = (folder / ("plan-%d.md" % (max(taken, default=0) + 1))).as_posix()

    def put():
        (root / rel).write_text("# %s\n\n%s\n" % (title, text), encoding="utf-8")
    shop_files.committed(root, [rel], "work record: %s" % rel.removeprefix(RECORDS.as_posix() + "/"), put)
    return rel
