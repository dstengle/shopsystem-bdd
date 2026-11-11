"""`work record` (capability design-model-check r56): a record written whole as `.shop/records/<date>-<slug>.md`, its
frontmatter (id, kind, about, date) and `# <title>` over the body a file gives, its row appended to the table of
`.shop/records/README.md`, and the two committed together. A path that exists already is refused, since a committed
record is never edited, and so is an `--about` that is not one line or not the id of a kind of node `model` knows
(r57)."""
import datetime
import re
import sys
from pathlib import Path

import shop_files
from model_facts import KINDS as NODE_KINDS

RECORDS = Path(".shop") / "records"
# The record kinds `model` reads under .shop/records/ (model_work.RECORD_KINDS) that a record file holds: an
# observation is a heading of observations.md, and initiative-archive is plugin 0.30's.
KINDS = ("analysis", "design", "measurement", "review-finding", "decision-argument")
HISTORY = {"design": "record", "analysis": "record"}     # their ids are record/<path>/<name>
README_HEAD = ("# Records\n\nDated, never edited. Paths are under `.shop/records/`.\n\n| path | record | kind |\n"
               "|---|---|---|\n")
HELP = ("write a record, .shop/records/<date>-<slug>.md, with its frontmatter (id, kind, about, date) and # <title> "
        "over the body of --body; append its row to .shop/records/README.md; commit both")
EPILOG = """\
The file written:

  ---
  id: <record, or the kind for measurement, review-finding, decision-argument>/<context path>/<date>-<slug>
  kind: <--kind>
  about: <--about, default the bounded context>
  date: <--date, default today>
  ---

  # <title>

  <the text of the --body file>

and the row `| `<date>-<slug>.md` | <--summary> | <--kind> |` at the end of the table of .shop/records/README.md
(the file made with its table when it is missing). A record that exists already is refused: a committed record is
never edited, so give another --slug. It prints the path written."""


def add_parser(sub):
    import argparse
    p = sub.add_parser("record", help=HELP, description=HELP + ".", epilog=EPILOG,
                       formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("title", help="the record's title, its heading; the slug of its file and id comes from it")
    p.add_argument("--kind", required=True, choices=KINDS, help="the record's kind")
    p.add_argument("--summary", required=True, help="the text of its row in .shop/records/README.md, one line")
    p.add_argument("--body", required=True, help="a file whose text is the record's body, under its title")
    p.add_argument("--about", help="the id of the node the record is about, <kind>/<...> on one line (default: the bounded context)")
    p.add_argument("--slug", help="the file's name after its date (default: from the title)")
    p.add_argument("--date", help="the record's date, YYYY-MM-DD (default: today)")


def one_line(text, what):
    text = text.strip()
    if not text or any(ch in text for ch in shop_files.LINE_BREAKS):
        raise shop_files.Refused("the %s is one line of text" % what)
    return text


def attributed(about):
    """An `--about` as the frontmatter holds it: one line, `<kind>/<...>` of a kind of node `model` knows (a design or
    an analysis is `record/...`)."""
    kind, _, rest = about.strip().partition("/")
    if (any(ch in about for ch in shop_files.LINE_BREAKS) or not rest or not re.fullmatch(r"\S+", rest)
            or kind not in NODE_KINDS | set(HISTORY.values())):
        raise shop_files.Refused("--about %r is not one line naming a node: <kind>/<...>, the kind one of %s"
                                 % (about, ", ".join(sorted(NODE_KINDS | set(HISTORY.values())))))
    return about.strip()


def with_row(readme, row):
    """The README with `row` after the last row of its table (or a new table when it has none)."""
    lines = readme.splitlines(keepends=True)
    last = max((n for n, line in enumerate(lines) if line.startswith("|")), default=None)
    if last is None:
        return readme.rstrip("\n") + "\n\n| path | record | kind |\n|---|---|---|\n" + row
    return "".join(lines[:last + 1]) + ("" if lines[last].endswith("\n") else "\n") + row + "".join(lines[last + 1:])


def write(args):
    """Write the record and its row, commit both; the record's path, relative to the root."""
    root = Path(args.root)
    title, summary = one_line(args.title, "title"), one_line(args.summary, "summary").replace("|", "\\|")
    date = args.date or datetime.date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", date):
        raise shop_files.Refused("the date %s is not YYYY-MM-DD" % date)
    slug = args.slug or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        raise shop_files.Refused("the slug %r is not lowercase words joined by hyphens" % slug)
    body_path = Path(args.body)
    if not body_path.is_file():
        raise shop_files.Refused("--body: no file %s" % args.body)
    body = shop_files.read(body_path, body_path.parent).strip()
    path = shop_files.context_path(root)
    name = "%s-%s" % (date, slug)
    rel, readme = (RECORDS / ("%s.md" % name)).as_posix(), (RECORDS / "README.md").as_posix()
    if (root / rel).exists():
        raise shop_files.Refused("%s exists, and a committed record is never edited: give another --slug" % rel)
    about = attributed(args.about) if args.about is not None else "bounded-context/%s" % path
    text = ("---\nid: %s/%s/%s\nkind: %s\nabout: %s\ndate: %s\n---\n\n# %s\n\n%s\n"
            % (HISTORY.get(args.kind, args.kind), path, name, args.kind, about, date, title, body))
    row = "| `%s.md` | %s | %s |\n" % (name, summary, args.kind)
    current = shop_files.read(root / readme, root) if (root / readme).is_file() else README_HEAD

    def put():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
        (root / readme).write_text(with_row(current, row), encoding="utf-8")
    shop_files.committed(root, [rel, readme], "work record: %s" % name, put)
    return rel


def record(args):
    try:
        rel = write(args)
    except shop_files.Refused as why:
        print("work record: %s" % why, file=sys.stderr)
        return 1
    print(rel)
    return 0


COMMANDS = {"record": record}
