"""`work decision` (capability decision-tiers r7, r8): a design-decision written whole from its arguments as
`spec/decisions/<nnnn>-<slug>.md`, the next number after the highest there, the decisions index rewritten as
`model decisions` writes it, and the two committed together; its verification routes (`--verified-by`, r10) and the
ids it rests on (`--rests-on`, a universal condition among them) written beside `enforced_by`. A decision missing --summary, --decision or --tier is
refused before anything is written, every one absent named in one error (r20, r24, r25). A decision that supersedes
another (`--supersedes`, r31, r32) names it under `supersedes:`, and the one superseded, accepted until then, is set
`superseded` in the same commit; one that is not accepted, or an id that names no decision, refused, naming it."""
import datetime
import re
import sys
from pathlib import Path

import shop_files
from model_decisions import ROUTES
from model_parse import DECISIONS, decision_files

TIERS = ("check", "requirement", "judgement")
HELP = ("write a design-decision, spec/decisions/<nnnn>-<slug>.md, with its frontmatter (id, summary, date, status "
        "accepted, tier) and its ## Context, ## Decision and ## Alternatives; rewrite spec/decisions/index.md as "
        "`model decisions` does; commit both")
EPILOG = """\
The file written:

  ---
  id: design-decision/<context path>/<slug>
  summary: "<--summary>"
  date: <--date, default today>
  status: accepted
  tier: <--tier>
  enforced_by: [<--enforced-by>, ...]      (when given)
  verified_by: [<--verified-by>, ...]      (when given)
  rests_on: [<--rests-on>, ...]            (when given)
  supersedes: [<--supersedes>, ...]        (when given)
  source: [<--source>, ...]                (when given)
  by: "<--by>"                             (when given)
  ---

  # <nnnn>. <title>

  ## Context          (when --context is given)
  ## Decision
  ## Alternatives     (when --alternatives is given)

--context, --decision and --alternatives take the text, or @<file> for the text of a file. A check decision names
the tests that enforce it (--enforced-by <path>.py::<test>), a requirement decision the requirements
(--enforced-by <capability>#r<n>), a judgement decision none (design-decision/decision-tiers). A decision that
routes a universal condition rests on it (--rests-on universal-condition/u<n>) and names how it is verified
(--verified-by scenario, check, judgement or monitor). A decision that replaces one in force names it
(--supersedes <id>, its id, its path or its number): that decision's status is set to superseded and committed with
the new one; one whose status is not accepted, or an id that names no decision, is refused and nothing is written. With any of --summary,
--decision and --tier missing the command is refused, naming each one missing, and writes nothing. It prints the path
written."""


def add_parser(sub):
    import argparse
    p = sub.add_parser("decision", help=HELP, description=HELP + ".", epilog=EPILOG,
                       formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("title", help="the decision's title, its heading; the slug of its file and id comes from it")
    p.add_argument("--summary", help="one sentence, the index's summary (required)")
    p.add_argument("--tier", choices=TIERS, help="check, requirement or judgement (required)")
    p.add_argument("--decision", help="the ## Decision section: what is decided (text or @<file>) (required)")
    p.add_argument("--context", help="the ## Context section: why it came up (text or @<file>)")
    p.add_argument("--alternatives", help="the ## Alternatives section: what else was weighed (text or @<file>)")
    p.add_argument("--enforced-by", dest="enforced_by", action="append", default=[],
                   help="a test (check tier) or a requirement (requirement tier) that enforces it; repeatable")
    p.add_argument("--verified-by", dest="verified_by", action="append", default=[], choices=ROUTES,
                   help="how what it decides is verified: scenario, check, judgement or monitor; repeatable")
    p.add_argument("--rests-on", dest="rests_on", action="append", default=[],
                   help="an id the decision rests on, such as the universal condition it routes; repeatable")
    p.add_argument("--supersedes", action="append", default=[],
                   help="an accepted design-decision this one replaces (its id, path or number), set superseded; "
                        "repeatable")
    p.add_argument("--source", action="append", default=[], help="an id the decision rests on; repeatable")
    p.add_argument("--by", help="who decided, and when")
    p.add_argument("--slug", help="the file's and id's name after its number (default: from the title)")
    p.add_argument("--date", help="the decision's date, YYYY-MM-DD (default: today)")


def slug_of(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def text_of(value, root, what):
    """The text an argument gives: itself, or the file's text for @<file>."""
    if value is None or not value.startswith("@"):
        return value
    path = Path(value[1:])
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.is_file():
        raise shop_files.Refused("%s: no file %s" % (what, value[1:]))
    return shop_files.read(path, path.parent).strip()


def quoted(value, what):
    if any(ch in value for ch in shop_files.LINE_BREAKS):
        raise shop_files.Refused("the %s is one line" % what)
    if '"' not in value:
        return '"%s"' % value
    if "'" not in value:
        return "'%s'" % value
    raise shop_files.Refused("the %s holds both kinds of quote" % what)


def next_number(root):
    found = [int(m.group(1)) for p in decision_files(root) for m in [re.match(r"(\d{4})-", p.name)] if m]
    return max(found, default=0) + 1


def superseded(root, refs):
    """[(path, id)] of each decision `--supersedes` names, by its id, its path or its number; an id that names none,
    or a decision whose status is not accepted, refused naming it."""
    found = []
    for ref in refs:
        hits = []
        for path in decision_files(root):
            data, _ = shop_files.frontmatter(shop_files.read(path, root))
            rel = path.relative_to(root).as_posix()
            if ref in (data.get("id"), rel, path.name, path.stem) or path.name.startswith(ref + "-"):
                hits.append((path, rel, data))
        if len(hits) != 1:
            raise shop_files.Refused("--supersedes %s names %s design-decision" % (ref, "no" if not hits else "more than one"))
        path, rel, data = hits[0]
        if data.get("status") != "accepted":
            raise shop_files.Refused("%s (%s) is %s, not accepted: only a design-decision in force is superseded"
                                     % (rel, data.get("id"), data.get("status") or "of no status"))
        found.append((path, data.get("id")))
    return found


def marked(text):
    """A decision's text with the status in its frontmatter `superseded`, nothing else of it changed."""
    head, rest = text[4:].split("\n---\n", 1)
    head = re.sub(r"^status: .*$", "status: superseded", head, count=1, flags=re.MULTILINE)
    return "---\n%s\n---\n%s" % (head, rest)


def render(number, title, ident, args, sections, date):
    head = ["id: %s" % ident, "summary: %s" % quoted(args.summary, "summary"), "date: %s" % date,
            "status: accepted", "tier: %s" % args.tier]
    for key, values in (("enforced_by", args.enforced_by), ("verified_by", args.verified_by),
                        ("rests_on", args.rests_on), ("supersedes", args.superseding), ("source", args.source)):
        if values:
            head.append("%s: [%s]" % (key, ", ".join(values)))
    if args.by:
        head.append("by: %s" % quoted(args.by, "--by"))
    body = ["# %04d. %s" % (number, title)]
    body += ["## %s\n\n%s" % (name, text.strip()) for name, text in sections if text]
    return "---\n%s\n---\n\n%s\n" % ("\n".join(head), "\n\n".join(body))


def write(args):
    """Write the decision and the index, commit both; the decision's path, relative to the root."""
    root = Path(args.root)
    absent = [option for option, value in (("--summary", args.summary), ("--decision", args.decision),
                                           ("--tier", args.tier)) if value is None]
    if absent:
        tiers = " (--tier check, requirement or judgement)" if args.tier is None else ""
        raise shop_files.Refused("a design-decision gives %s%s" % (", ".join(absent), tiers))
    title = args.title.strip()
    if not title or any(ch in title for ch in shop_files.LINE_BREAKS):
        raise shop_files.Refused("the title is one line of text")
    slug = args.slug or slug_of(title)
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        raise shop_files.Refused("the slug %r is not lowercase words joined by hyphens" % slug)
    ident = "design-decision/%s/%s" % (shop_files.context_path(root), slug)
    for path in decision_files(root):
        data, _ = shop_files.frontmatter(shop_files.read(path, root))
        if data.get("id") == ident or path.name.split("-", 1)[-1] == slug + ".md":
            raise shop_files.Refused("%s already has the id %s: give another --slug" % (path.relative_to(root), ident))
    olds = superseded(root, getattr(args, "supersedes", None) or [])
    args.superseding = [old for _, old in olds]
    sections = [("Context", text_of(args.context, root, "--context")),
                ("Decision", text_of(args.decision, root, "--decision")),
                ("Alternatives", text_of(args.alternatives, root, "--alternatives"))]
    number, date = next_number(root), args.date or datetime.date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", date):
        raise shop_files.Refused("the date %s is not YYYY-MM-DD" % date)
    rel = (DECISIONS / ("%04d-%s.md" % (number, slug))).as_posix()
    index = (DECISIONS / "index.md").as_posix()
    text = render(number, title, ident, args, sections, date)

    from model_report import render_decisions

    def put():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
        for path, _ in olds:
            path.write_text(marked(path.read_text(encoding="utf-8")), encoding="utf-8")
        (root / index).write_text(render_decisions(root), encoding="utf-8")
    paths = [rel, index] + [path.relative_to(root).as_posix() for path, _ in olds]
    shop_files.committed(root, paths, "work decision: %04d. %s" % (number, title), put)
    return rel


def decision(args):
    try:
        rel = write(args)
    except shop_files.Refused as why:
        print("work decision: %s" % why, file=sys.stderr)
        return 1
    print(rel)
    return 0


COMMANDS = {"decision": decision}
