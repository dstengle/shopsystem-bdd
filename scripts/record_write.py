"""`work record` (capability design-model-check r56): a record written whole as `.shop/records/<date>-<slug>.md`, its
frontmatter (id, kind, about, date) and `# <title>` over the body a file gives, its row appended to the table of
`.shop/records/README.md`, and the two committed together. A path that exists already is refused, since a committed
record is never edited, and so is an `--about` that is not one line or not the id of a kind of node `model` knows
(r57), or that denotes no node, item or batch the repository holds (records r3, r5, r6, b49). With `--design` or
`--plan` the request is records.file design or records.file plan, written by record_design (b475)."""
import datetime
import re
from pathlib import Path

import shop_files

RECORDS = Path(".shop") / "records"
# The record kinds `model` reads under .shop/records/ (model_work.RECORD_KINDS) that a record file holds: an
# observation is a heading of observations.md, and initiative-archive is plugin 0.30's.
KINDS = ("analysis", "design", "measurement", "review-finding", "decision-argument")
HISTORY = {"design": "record", "analysis": "record"}     # their ids are record/<path>/<name>
README_HEAD = ("# Records\n\nDated, never edited. Paths are under `.shop/records/`.\n\n| path | record | kind |\n"
               "|---|---|---|\n")
HELP = ("write a record (or with --design a design's folder, with --plan a plan in it), .shop/records/<date>-<slug>.md, with its frontmatter (id, kind, about, date) and # <title> "
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
never edited, so give another --slug. It prints the path written.

work record "<title>" --design --summary "<row>" --body <file> files a design: the folder
.shop/records/<date>-<slug>/ with its design.md (the frontmatter above, kind design) and the row
`| `<date>-<slug>/design.md` | <--summary> | design |`, committed together.

work record "<title>" --plan --design <design> --body <file> files a plan in the folder of the design
(its folder's name <date>-<topic>, its path or its id record/<context path>/<date>-<topic>): plan-<k>.md,
k the next number of the folder's plans, `# <title>` over the body, committed. A design that does not
exist is refused."""


def add_parser(sub):
    import argparse
    p = sub.add_parser("record", help=HELP, description=HELP + ".", epilog=EPILOG,
                       formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("title", help="the record's title, its heading; the slug of its file and id comes from it")
    p.add_argument("--kind", choices=KINDS, help="the record's kind (a record but a design or a plan gives it)")
    p.add_argument("--summary", help="the text of its row in .shop/records/README.md, one line (a record and a design "
                   "give it)")
    p.add_argument("--design", nargs="?", const=True, metavar="DESIGN",
                   help="alone: file a design, the folder .shop/records/<date>-<slug>/ with its design.md; with --plan: "
                   "the design the plan goes in (its folder's name <date>-<topic>, its path or its id)")
    p.add_argument("--plan", action="store_true", help="file a plan, plan-<k>.md in the folder of the --design given")
    p.add_argument("--body", required=True, help="a file whose text is the record's body, under its title")
    p.add_argument("--about", help="the id of the node, item or batch the record is about, <kind>/<...> on one line, one this "
                   "repository holds (default: the bounded context)")
    p.add_argument("--slug", help="the file's name after its date (default: from the title)")
    p.add_argument("--date", help="the record's date, YYYY-MM-DD (default: today)")


def one_line(text, what):
    text = text.strip()
    if not text or any(ch in text for ch in shop_files.LINE_BREAKS):
        raise shop_files.Refused("the %s is one line of text" % what)
    return text


def slugged(slug, title):
    """The file's name after its date: `slug`, else lowercase words of the title joined by hyphens."""
    slug = slug or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        raise shop_files.Refused("the slug %r is not lowercase words joined by hyphens" % slug, reason="not a slug",
                                 names=["parameter:slug"])
    return slug


def attributed(about, root="."):
    """An `--about` as the frontmatter holds it: one line, `<kind>/<...>` of a kind of node `model` knows (a design or
    an analysis is `record/...`), an item or a batch, that denotes a node, an item or a batch this repository holds
    (b49): its id, or `<kind>/<name>` in this context."""
    import shop_ids
    from model_facts import KINDS as NODE_KINDS
    kinds = NODE_KINDS | set(HISTORY.values()) | set(shop_ids.KINDS)
    kind, _, rest = about.strip().partition("/")
    if (any(ch in about for ch in shop_files.LINE_BREAKS) or not rest or not re.fullmatch(r"\S+", rest)
            or kind not in kinds):
        raise shop_files.Refused("{names} %r is not one line naming a node: <kind>/<...>, the kind one of %s"
                                 % (about, ", ".join(sorted(kinds))), reason="names no node", names=["parameter:about"])
    if not denotes(Path(root), about.strip()):
        raise shop_files.Refused("{names} %r denotes no node, item or batch this repository holds" % about.strip(),
                                 reason="denotes nothing", names=["parameter:about"])
    return about.strip()


def denotes(root, about):
    """True when `about` is the id of an item or a batch the root holds, or of a node `model` reads there."""
    import shop_ids
    if about.partition("/")[0] in shop_ids.KINDS:
        return shop_ids.held(root, about, shop_files.context_path(root))
    from model_facts import Model
    model = Model(root)
    model.read()
    return model.qualify(about) in model.nodes


def with_row(readme, row):
    """The README with `row` after the last row of its table (or a new table when it has none)."""
    lines = readme.splitlines(keepends=True)
    last = max((n for n, line in enumerate(lines) if line.startswith("|")), default=None)
    if last is None:
        return readme.rstrip("\n") + "\n\n| path | record | kind |\n|---|---|---|\n" + row
    return "".join(lines[:last + 1]) + ("" if lines[last].endswith("\n") else "\n") + row + "".join(lines[last + 1:])


def write(root, title, summary, kind, body, *, about=None, slug=None, date=None):
    """The operation records.keep: write the record and its row, commit both; the record's path, relative to the
    root. Each parameter by its business name (`body` the path of the file of its text)."""
    root = Path(root)
    title, summary = one_line(title, "title"), one_line(summary, "summary").replace("|", "\\|")
    date = date or datetime.date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", date):
        raise shop_files.Refused("the date %s is not YYYY-MM-DD" % date, reason="not a date", names=["parameter:date"])
    slug = slugged(slug, title)
    body_path = Path(body)
    if not body_path.is_file():
        raise shop_files.Refused("{names}: no file %s" % body, reason="no such file", names=["parameter:body"])
    text_of_body = shop_files.read(body_path, body_path.parent).strip()
    path = shop_files.context_path(root)
    name = "%s-%s" % (date, slug)
    rel, readme = (RECORDS / ("%s.md" % name)).as_posix(), (RECORDS / "README.md").as_posix()
    if (root / rel).exists():
        raise shop_files.Refused("%s exists, and a committed record is never edited: give another {names}" % rel,
                                 reason="record exists", names=["parameter:slug"])
    about = attributed(about, root) if about is not None else "bounded-context/%s" % path
    text = ("---\nid: %s/%s/%s\nkind: %s\nabout: %s\ndate: %s\n---\n\n# %s\n\n%s\n"
            % (HISTORY.get(kind, kind), path, name, kind, about, date, title, text_of_body))
    row = "| `%s.md` | %s | %s |\n" % (name, summary, kind)
    current = shop_files.read(root / readme, root) if (root / readme).is_file() else README_HEAD

    def put():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
        (root / readme).write_text(with_row(current, row), encoding="utf-8")
    shop_files.committed(root, [rel, readme], "work record: %s" % name, put)
    return rel


def record(args):
    """`work record`: the request records.keep, its parameters read off the command line by business name."""
    from domain_envelope import Response
    import record_design
    if args.plan:
        if not isinstance(args.design, str):
            raise shop_files.Refused("a plan gives {names}, the design it goes in", reason="missing parameters",
                                     names=["parameter:design"])
        rel = record_design.plan(args.root, args.title, args.design, args.body)
    elif args.design is not None:
        if args.design is not True:
            raise shop_files.Refused("{names} names a design only with --plan; alone it files one",
                                     reason="design without plan", names=["parameter:design"])
        required(args, "summary")
        rel = record_design.design(args.root, args.title, args.summary, args.body, about=args.about, slug=args.slug,
                                   date=args.date)
    else:
        required(args, "kind", "summary")
        rel = write(args.root, args.title, args.summary, args.kind, args.body, about=args.about, slug=args.slug,
                    date=args.date)
    print(rel)
    return Response("done", {"path": rel})


def required(args, *names):
    """Refused naming each of `names` the command line does not give."""
    missing = [name for name in names if getattr(args, name) is None]
    if missing:
        raise shop_files.Refused("{names} must be given", reason="missing parameters",
                                 names=["parameter:%s" % name for name in missing])


COMMANDS = {"record": record}
