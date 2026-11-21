"""`work observe` (records r9, b475): an observation filed as an entry of `.shop/records/observations.md`, its heading
the id `observation/<context path>/<date>-<slug>` and under it `about:`, `by:` and `date:` over its text, appended
whole and committed; the file made with its heading when it is missing. An id the file holds already is refused, since
a committed observation is never edited, and so is an `--about` that denotes nothing (record_write's `attributed`)."""
import datetime
import re
from pathlib import Path

import record_write
import shop_files

PATH = record_write.RECORDS / "observations.md"
HEAD = "# Observations\n\nDated, never edited. An observation is an origin: an initiative may cite it as its `source`.\n"
HELP = ("file an observation: an entry of .shop/records/observations.md, its heading the id "
        "observation/<context path>/<date>-<slug>, with about, by and date over its text; commit it")


def add_parser(sub):
    p = sub.add_parser("observe", help=HELP, description=HELP + ".")
    p.add_argument("summary", metavar="text", help="the observation's text, one paragraph")
    p.add_argument("--about", help="the id of the node, item or batch it is about (default: the bounded context)")
    p.add_argument("--by", default="a session", help="who saw it (default: a session)")
    p.add_argument("--slug", help="its id's name after the date (default: from the first words of the text)")
    p.add_argument("--date", help="its date, YYYY-MM-DD (default: today)")


def write(root, summary, *, about=None, by="a session", slug=None, date=None):
    """The operation records.file observation: the entry appended to observations.md and committed; its id."""
    root = Path(root)
    text = record_write.one_line(summary, "text")
    by = record_write.one_line(by, "by")
    date = date or datetime.date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", date):
        raise shop_files.Refused("the date %s is not YYYY-MM-DD" % date, reason="not a date", names=["parameter:date"])
    slug = record_write.slugged(slug, " ".join(text.split()[:6]))
    ident = "observation/%s/%s-%s" % (shop_files.context_path(root), date, slug)
    current = shop_files.read(root / PATH, root) if (root / PATH).is_file() else HEAD
    if re.search(r"^## %s$" % re.escape(ident), current, re.MULTILINE):
        raise shop_files.Refused("%s holds %s, and a committed observation is never edited: give another {names}"
                                 % (PATH.as_posix(), ident), reason="observation exists", names=["parameter:slug"])
    about = record_write.attributed(about, root) if about is not None else "bounded-context/%s" % \
        shop_files.context_path(root)
    entry = "\n## %s\nabout: %s\nby: %s\ndate: %s\n\n%s\n" % (ident, about, by, date, text)

    def put():
        (root / PATH).parent.mkdir(parents=True, exist_ok=True)
        (root / PATH).write_text(current.rstrip("\n") + "\n" + entry, encoding="utf-8")
    shop_files.committed(root, [PATH.as_posix()], "work observe: %s-%s" % (date, slug), put)
    return ident


def observe(args):
    """`work observe`: the request records.file observation, its text the summary."""
    from domain_envelope import Response
    ident = write(args.root, args.summary, about=args.about, by=args.by, slug=args.slug, date=args.date)
    print(ident)
    return Response("done", {"id": ident, "path": PATH.as_posix()})


COMMANDS = {"observe": observe}
