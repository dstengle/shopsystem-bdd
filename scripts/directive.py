"""A directive (capability conversation, b20): a short-term direction of the person, kept in the repository and never in
a session's memory, as `.shop/directives/<n>.md`, named `directive-<n>`. It cites the quote holding the person's
words and is `live` until it is reviewed: promoted to what it became (an item `b<n>`, a design-decision or
`CLAUDE.md`), or dropped with the reason. The SessionStart hook shows each live one (`hook_text`). The file reads back
as it was written (`parse(render(d), rel) == d`). Standard library and the conversation's modules only, so the hook
runs under any `python3`."""
import datetime
import re
from dataclasses import dataclass
from pathlib import Path

import conversation_quote
from plumbing import shop_files
from plumbing.migrate_write import top_level
from plumbing.shop_files import Refused

DIRECTIVES = Path(".shop") / "directives"
STATUSES = ("live", "promoted", "dropped")
LABEL = 60
HOOK_LINE = ("The person's live directives: follow each of them, and pass them on in every brief you give an agent "
             "(an agent sees no SessionStart output).")


@dataclass
class Directive:
    name: str
    ident: str
    status: str
    date: str
    quote: str
    words: str
    promoted_to: str = None
    why: str = None


def is_directive(name):
    return re.fullmatch(r"directive-[1-9]\d*", str(name)) is not None


def number(name):
    return int(name.split("-", 1)[1])


def rel_of(name):
    return (DIRECTIVES / ("%d.md" % number(name))).as_posix()


def names(root):
    """The `directive-<n>` of each file of .shop/directives/, by number; a `.md` file named otherwise is refused."""
    found = []
    for path in (Path(root) / DIRECTIVES).glob("*.md"):
        if not re.fullmatch(r"[1-9]\d*", path.stem):
            raise Refused("%s: the file name is not <n>.md" % (DIRECTIVES / path.name).as_posix())
        found.append("directive-%s" % path.stem)
    return sorted(found, key=number)


def directives(root):
    return [find(root, name) for name in names(root)]


def find(root, name):
    """The directive `name`; refused when it has no file."""
    if not is_directive(name) or not (Path(root) / rel_of(name)).is_file():
        raise Refused("there is no directive %s in %s/" % (name, DIRECTIVES.as_posix()))
    rel = rel_of(name)
    found = parse(shop_files.read(Path(root) / rel, root), rel)
    if found.name != name:
        raise Refused("%s: id %s does not end in %s" % (rel, found.ident, name))
    return found


def label(found):
    """How `work` names a directive: `directive-<n> "<its words, cut at 60 characters>"`."""
    words = " ".join(found.words.split())
    return '%s "%s"' % (found.name, words if len(words) <= LABEL else words[:LABEL] + "…")


def render(found):
    """The file's text, byte-stable: the frontmatter, the person's words as `>` lines, and a dropped one's reason
    under `## Why dropped`."""
    head = ["id: %s" % found.ident, "kind: directive", "status: %s" % found.status, "date: %s" % found.date,
            "quote: %s" % found.quote] + (["promoted_to: %s" % found.promoted_to] if found.promoted_to else [])
    words = "\n".join("> " + line if line else ">" for line in found.words.split("\n"))
    why = "\n## Why dropped\n\n%s\n" % found.why if found.why else ""
    return "---\n%s\n---\n\n# %s\n\n%s\n%s" % ("\n".join(head), found.name, words, why)


def parse(text, rel):
    """The directive of a file's text; any other shape is refused as `<rel>: <field> ...`."""
    data, body = shop_files.frontmatter(text)
    ident = data.get("id")
    if not isinstance(ident, str) or not re.fullmatch(r"directive/.+/directive-[1-9]\d*", ident):
        raise Refused("%s: id %r is not directive/<context path>/directive-<n>" % (rel, ident))
    if data.get("kind") != "directive":
        raise Refused("%s: kind %r is not directive" % (rel, data.get("kind")))
    if data.get("status") not in STATUSES:
        raise Refused("%s: status %r is not one of %s" % (rel, data.get("status"), ", ".join(STATUSES)))
    for key in ("date", "quote"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise Refused("%s: %s is missing" % (rel, key))
    if not conversation_quote.is_quote(data["quote"]):
        raise Refused("%s: quote %r is not quote-<n>" % (rel, data["quote"]))
    name = ident.rsplit("/", 1)[1]
    lines = body.split("\n")
    if lines[:2] != ["# %s" % name, ""]:
        raise Refused("%s: title: the file does not start with # %s" % (rel, name))
    at, words = 2, []
    while at < len(lines) and lines[at].startswith(">"):
        words.append(lines[at][2:] if lines[at].startswith("> ") else lines[at][1:])
        at += 1
    rest = "\n".join(lines[at:])
    why = None
    if rest.startswith("\n## Why dropped\n\n") and rest.endswith("\n"):
        why = rest[len("\n## Why dropped\n\n"):-1]
    elif rest != "":
        raise Refused("%s: body: the words as > lines, then only ## Why dropped" % rel)
    if not words:
        raise Refused("%s: words: no > lines" % rel)
    promoted = data.get("promoted_to")
    return Directive(name, ident, data["status"], data["date"], data["quote"], "\n".join(words),
                     str(promoted) if promoted else None, why)


def _new(root, quote):
    name = "directive-%d" % (max(map(number, names(root)), default=0) + 1)
    return Directive(name, "directive/%s/%s" % (shop_files.context_path(root), name), "live",
                     datetime.datetime.now(datetime.UTC).date().isoformat(), quote.name, quote.words)


def _put(root, found):
    target = Path(root) / rel_of(found.name)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(found), encoding="utf-8")


def write(root, words, session=None, transcript=None):
    """`work directive "<words>"`: the quote of the person's words (as `work quote` finds them) and a live directive
    citing it, written and committed in one commit."""
    quote = conversation_quote.made(root, words, session, transcript)
    found = _new(root, quote)

    def put():
        conversation_quote.put(root, quote)
        _put(root, found)
    shop_files.committed(root, [conversation_quote.rel_of(quote.name), rel_of(found.name)],
                         "directive: %s citing %s" % (found.name, quote.name), put)
    return found


def from_quote(root, name):
    """`work directive --quote quote-<n>`: a live directive citing an existing quote, committed."""
    found = _new(root, conversation_quote.find(root, name))
    shop_files.committed(root, [rel_of(found.name)], "directive: %s citing %s" % (found.name, name),
                         lambda: _put(root, found))
    return found


def target_exists(root, target):
    """Whether what a directive is promoted to exists: an item `b<n>` of .shop/backlog/, `CLAUDE.md`, or a
    design-decision by its id (`design-decision/<context path>/<slug>`, or `design-decision/<slug>`)."""
    root = Path(root)
    if re.fullmatch(r"b[1-9]\d*", target):
        return (root / ".shop" / "backlog" / ("%s.md" % target)).is_file()
    if target == "CLAUDE.md":
        return (root / "CLAUDE.md").is_file()
    if target.startswith("design-decision/"):
        slug = target.rsplit("/", 1)[1]
        return bool(slug) and any((root / "spec" / "decisions").glob("[0-9][0-9][0-9][0-9]-%s.md" % slug))
    return False


def _live(root, name, command):
    found = find(root, name)
    if found.status != "live":
        raise Refused("%s is %s, not live; shop work %s reviews a live directive" % (name, found.status, command))
    return found


def promote(root, name, target):
    """`work promote directive-<n> --to <target>`: a live directive promoted to the target, which exists."""
    found = _live(root, name, "promote")
    if not target_exists(root, target):
        raise Refused("%s does not exist: --to takes an item b<n>, a design-decision's id or CLAUDE.md, written first"
                      % target)
    found.status, found.promoted_to = "promoted", target
    shop_files.committed(root, [rel_of(name)], "directive: %s promoted to %s" % (name, target),
                         lambda: _put(root, found))
    return found


def drop(root, name, why):
    """`work drop directive-<n> --why "<reason>"`: a live directive dropped with its reason."""
    if not (why or "").strip():
        raise Refused("--why is empty: give the reason the directive is dropped")
    found = _live(root, name, "drop")
    found.status, found.why = "dropped", why.strip()
    shop_files.committed(root, [rel_of(name)], "directive: %s dropped" % name, lambda: _put(root, found))
    return found


def age(found, today=None):
    today = today or datetime.datetime.now(datetime.UTC).date()
    days = (today - datetime.date.fromisoformat(found.date)).days
    return "%d day%s" % (days, "" if days == 1 else "s")


def hook_text(cwd):
    """What the SessionStart hook prints at the top level of the cwd's repository: HOOK_LINE and each live directive
    with its quote and its words; nothing when none is live or outside a repository with `.shop/`, `work directives:
    <why>` for a refusal."""
    root = top_level(cwd)
    if root is None or not (Path(root) / ".shop").is_dir():
        return ""
    try:
        live = [d for d in directives(root) if d.status == "live"]
    except Refused as why:
        return "work directives: %s" % why
    if not live:
        return ""
    out = [HOOK_LINE]
    for d in live:
        out.append("- %s (%s, %s): %s" % (d.name, d.quote, d.date, d.words.replace("\n", "\n  ")))
    return "\n".join(out)
