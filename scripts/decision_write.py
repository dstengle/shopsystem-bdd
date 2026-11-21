"""`work decision` (capability decision-tiers r7, r8): a design-decision written whole from its arguments as
`spec/decisions/<nnnn>-<slug>.md`, the next number after the highest there, the decisions index rewritten as
`model decisions` writes it, and the two committed together; its verification routes (`--verified-by`, r10) and the
ids it rests on (`--rests-on`, a universal condition among them) written beside `enforced_by`. A decision missing --summary, --decision or --tier is
refused before anything is written, every one absent named in one error (r20, r24, r25). A decision that supersedes
another (`--supersedes`, r31, r32) names it under `supersedes:`, and the one superseded, accepted until then, is set
`superseded` in the same commit; one that is not accepted, or an id that names no decision, refused, naming it."""
import datetime
import re
from pathlib import Path

import decision_amend
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
written.

work decision --amend <decision> [--enforced-by <id>]... [--rests-on <id>]... adds to an accepted decision (its id,
path or number) each enforcer under enforced_by and each foundation under rests_on it does not name yet, nothing else
of it changed, rewrites the index and commits both; when it names every one already, it completes and changes no
file; a decision whose status is not accepted is refused, naming it,
and nothing is written. It prints the path amended."""


def add_parser(sub):
    import argparse
    p = sub.add_parser("decision", help=HELP, description=HELP + ".", epilog=EPILOG,
                       formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("title", nargs="?",
                   help="the decision's title, its heading; the slug of its file and id comes from it (required "
                        "but with --amend)")
    p.add_argument("--amend", metavar="DECISION",
                   help="amend this accepted design-decision (its id, path or number) in place of writing one: add "
                        "each --enforced-by to its enforced_by and each --rests-on to its rests_on")
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
    """[(path, id)] of each decision `supersedes` names, by its id, its path or its number; an id that names none,
    or a decision whose status is not accepted, refused naming it."""
    found = []
    for ref in refs:
        path, rel, data = decision_amend.found(root, ref, "supersedes")
        decision_amend.in_force(rel, data, "superseded")
        found.append((path, data.get("id")))
    return found


def marked(text):
    """A decision's text with the status in its frontmatter `superseded`, nothing else of it changed."""
    head, rest = text[4:].split("\n---\n", 1)
    head = re.sub(r"^status: .*$", "status: superseded", head, count=1, flags=re.MULTILINE)
    return "---\n%s\n---\n%s" % (head, rest)


def render(number, title, ident, fields, sections, date):
    """The decision's text; `fields` its frontmatter's values by business name."""
    head = ["id: %s" % ident, "summary: %s" % quoted(fields["summary"], "summary"), "date: %s" % date,
            "status: accepted", "tier: %s" % fields["tier"]]
    for key, name in (("enforced_by", "enforced by"), ("verified_by", "routes"), ("rests_on", "rests on"),
                      ("supersedes", "supersedes"), ("source", "source")):
        if fields.get(name):
            head.append("%s: [%s]" % (key, ", ".join(fields[name])))
    if fields.get("author"):
        head.append("by: %s" % quoted(fields["author"], "author"))
    body = ["# %04d. %s" % (number, title)]
    body += ["## %s\n\n%s" % (name, text.strip()) for name, text in sections if text]
    return "---\n%s\n---\n\n%s\n" % ("\n".join(head), "\n\n".join(body))


def write(root, title, summary=None, tier=None, wording=None, *, context=None, alternatives=None, enforced_by=(),
          routes=(), rests_on=(), supersedes=(), source=(), author=None, slug=None, date=None):
    """The operation decisions.enter: write the decision and the index, commit both; the decision's path, relative to
    the root. Each parameter by its business name; a refusal names its parameters as `parameter:<name>`."""
    root = Path(root)
    absent = ["parameter:" + name for name, value in (("summary", summary), ("wording", wording), ("tier", tier))
              if value is None]
    if absent:
        raise shop_files.Refused("a design-decision gives {names}%s" % (" (a tier: check, requirement or judgement)"
                                                                        if tier is None else ""),
                                 reason="missing parameters", names=absent)
    if tier not in TIERS:
        raise shop_files.Refused("the tier %s is not check, requirement or judgement" % tier, reason="no such tier",
                                 names=["parameter:tier"])
    title = title.strip()
    if not title or any(ch in title for ch in shop_files.LINE_BREAKS):
        raise shop_files.Refused("the title is one line of text", reason="not one line", names=["parameter:title"])
    slug = slug or slug_of(title)
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        raise shop_files.Refused("the slug %r is not lowercase words joined by hyphens" % slug, reason="not a slug",
                                 names=["parameter:slug"])
    ident = "design-decision/%s/%s" % (shop_files.context_path(root), slug)
    for path in decision_files(root):
        data, _ = shop_files.frontmatter(shop_files.read(path, root))
        if data.get("id") == ident or path.name.split("-", 1)[-1] == slug + ".md":
            raise shop_files.Refused("%s already has the id %s: give another {names}" % (path.relative_to(root), ident),
                                     reason="id taken", names=["parameter:slug"])
    olds = superseded(root, supersedes or [])
    sections = [("Context", text_of(context, root, "the context")),
                ("Decision", text_of(wording, root, "the wording")),
                ("Alternatives", text_of(alternatives, root, "the alternatives"))]
    number, date = next_number(root), date or datetime.date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", date):
        raise shop_files.Refused("the date %s is not YYYY-MM-DD" % date, reason="not a date", names=["parameter:date"])
    rel = (DECISIONS / ("%04d-%s.md" % (number, slug))).as_posix()
    index = (DECISIONS / "index.md").as_posix()
    fields = {"summary": summary, "tier": tier, "enforced by": list(enforced_by), "routes": list(routes),
              "rests on": list(rests_on), "supersedes": [old for _, old in olds], "source": list(source),
              "author": author}
    text = render(number, title, ident, fields, sections, date)

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


# the CLI adapter's requests of decisions.enter and decisions.amend: each business parameter's argparse dest where the two differ
PARAMETERS = {"wording": "decision", "routes": "verified_by", "author": "by", "enforcer": "enforced_by",
              "foundation": "rests_on"}


def decision(args):
    """`work decision`: the request decisions.enter, its parameters read off the command line by business name."""
    from domain_envelope import Response
    if args.amend is not None:
        return amend(args)
    if args.title is None:
        raise shop_files.Refused("a design-decision gives {names}", reason="missing parameters",
                                 names=["parameter:title"])
    rel = write(args.root, args.title, args.summary, args.tier, args.decision, context=args.context,
                alternatives=args.alternatives, enforced_by=args.enforced_by, routes=args.verified_by,
                rests_on=args.rests_on, supersedes=args.supersedes, source=args.source, author=args.by,
                slug=args.slug, date=args.date)
    print(rel)
    return Response("done", {"path": rel})


def amend(args):
    """`work decision --amend`: the request decisions.amend, its enforcers and foundations off the command line."""
    from domain_envelope import Response
    rel = decision_amend.amend(args.root, args.amend, args.enforced_by, args.rests_on)
    print(rel)
    return Response("done", {"path": rel})


decision.parameters = PARAMETERS
COMMANDS = {"decision": decision}
