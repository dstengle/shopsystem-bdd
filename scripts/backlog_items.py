"""One item of the backlog (capability backlog): its file `.shop/backlog/b<n>.md` read and written, its label, and its
commit (workflow simplification plan 2, D2-D4, D16).

The file holds its fields in frontmatter, its title as its one `# ` heading (never quoted in YAML) and optional `## `
sections. An unrated field is written empty and reads as None. A file that is not an item's is refused, naming the
file and the field, by every command that reads it; it is never skipped."""
import re
from dataclasses import dataclass, field
from pathlib import Path

import workqueue
from workqueue import Refused
from workqueue_answer import LINE_BREAKS

BACKLOG = Path(".shop") / "backlog"
STATUSES = ("idea", "shaped", "ready", "in-batch", "delivered", "needs-input", "refused", "withdrawn")
PROVENANCES = ("own", "peer", "product")
RATINGS = {"value": ("low-value", "medium-value", "high-value"),
           "urgency": ("low-urgency", "medium-urgency", "high-urgency"),
           "size": ("small", "medium", "large")}


@dataclass
class Item:
    name: str
    ident: str
    title: str
    status: str
    provenance: str
    value: str | None = None
    urgency: str | None = None
    size: str | None = None
    depends_on: tuple = ()
    sections: dict = field(default_factory=dict)

    @property
    def question(self):
        return self.sections.get("Question")


def is_item(name):
    """Whether `name` has an item's id form, `b<n>`."""
    return bool(re.fullmatch(r"b[1-9]\d*", name or ""))


def number(name):
    return int(name[1:])


def one_line(text, what):
    """`text`, stripped, when it is one non-empty line; else refused, naming `what`."""
    if any(c in text for c in LINE_BREAKS):
        raise Refused("the %s has a line break in it; %s is one line" % (what, what))
    if not text.strip():
        raise Refused("the %s is empty" % what)
    return text.strip()


def _choice(data, rel, name, allowed, optional=False):
    value = data.get(name)
    if optional and value is None:
        return None
    if value not in allowed:
        raise Refused("%s: %s %r is not one of %s" % (rel, name, value, ", ".join(allowed)))
    return value


def _body(text, rel):
    """(title, sections) of the body: its one `# ` heading, then each `## ` heading's text."""
    lines = text.strip("\n").split("\n")
    if not lines or not lines[0].startswith("# ") or not lines[0][2:].strip():
        raise Refused("%s: title: the file has no `# ` heading first in its body" % rel)
    title, sections, heading = lines[0][2:].strip(), {}, None
    for line in lines[1:]:
        if line.startswith("# "):
            raise Refused("%s: title: the file has more than one `# ` heading" % rel)
        if line.startswith("## "):
            heading = line[3:].strip()
            sections[heading] = []
        elif heading is not None:
            sections[heading].append(line)
        elif line.strip():
            raise Refused("%s: title: text between the `# ` heading and the first `## ` section" % rel)
    return title, {h: "\n".join(body).strip("\n") for h, body in sections.items()}


def parse(text, rel):
    """The item of a file's text; a malformed file is refused as `<rel>: <field> ...` (D16)."""
    data, body = workqueue.frontmatter(text)
    ident = data.get("id")
    if not isinstance(ident, str) or not ident.startswith("item/"):
        raise Refused("%s: id %r is not item/<context path>/b<n>" % (rel, ident))
    if data.get("kind") != "item":
        raise Refused("%s: kind %r is not item" % (rel, data.get("kind")))
    depends = data.get("depends_on", [])
    if not isinstance(depends, list) or not all(isinstance(d, str) and is_item(d) for d in depends):
        raise Refused("%s: depends_on %r is not a list of b<n>" % (rel, depends))
    title, sections = _body(body, rel)
    return Item(name=ident.rsplit("/", 1)[-1], ident=ident, title=title, status=_choice(data, rel, "status", STATUSES),
                provenance=_choice(data, rel, "provenance", PROVENANCES),
                **{k: _choice(data, rel, k, allowed, optional=True) for k, allowed in RATINGS.items()},
                depends_on=tuple(depends), sections=sections)


def render(item):
    """The file's text, byte-stable: `parse(render(item), rel) == item`."""
    def line(key, value):
        return "%s:%s" % (key, " %s" % value if value else "")
    head = [line("id", item.ident), "kind: item", line("status", item.status), line("provenance", item.provenance)]
    head += [line(k, getattr(item, k)) for k in RATINGS] + ["depends_on: [%s]" % ", ".join(item.depends_on)]
    body = "".join("\n## %s\n\n%s\n" % (h, t) if t else "\n## %s\n" % h for h, t in item.sections.items())
    return "---\n%s\n---\n\n# %s\n%s" % ("\n".join(head), item.title, body)


def rel_of(name):
    return (BACKLOG / ("%s.md" % name)).as_posix()


def names(root):
    """The `b<n>` of each file of .shop/backlog/, by number; a `.md` file named otherwise is refused, never skipped."""
    found = []
    for path in (Path(root) / BACKLOG).glob("*.md"):
        if not is_item(path.stem):
            raise Refused("%s: id: the file name is not b<n>" % (BACKLOG / path.name).as_posix())
        found.append(path.stem)
    return sorted(found, key=number)


def items(root):
    """Every item of the backlog, by number; a malformed file is refused."""
    return [load(root, name) for name in names(root)]


def load(root, name):
    rel = rel_of(name)
    item = parse(workqueue.read(Path(root) / rel, root), rel)
    if item.name != name:
        raise Refused("%s: id %s does not end in %s" % (rel, item.ident, name))
    return item


def find(root, name):
    """The item `name`; refused when it has no file."""
    if not is_item(name) or not (Path(root) / rel_of(name)).is_file():
        raise Refused("there is no item %s in %s/" % (name, BACKLOG.as_posix()))
    return load(root, name)


def next_name(root):
    """`b<highest + 1>` over the files of .shop/backlog/ (D4)."""
    return "b%d" % (max(map(number, names(root)), default=0) + 1)


def label(item):
    """How `work` names an item: its id and its title, `b3 "Fix the parser"` (design goal 10)."""
    return '%s "%s"' % (item.name, item.title)


def as_dict(item):
    """The item's own fields, as `work show --json` and `work backlog --json` give them."""
    return {"id": item.name, "title": item.title, "status": item.status, "provenance": item.provenance,
            "value": item.value, "urgency": item.urgency, "size": item.size, "depends_on": list(item.depends_on),
            "question": item.question}


def commit(root, item, message):
    """Write the item's file and commit that one path (D3: git history is the item's log)."""
    rel = rel_of(item.name)

    def write():
        path = Path(root) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(item), encoding="utf-8")
    workqueue.committed(root, [rel], message, write)
