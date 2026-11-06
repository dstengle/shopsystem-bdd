"""The requests of a context, kept as .shop/requests/<id>.md: the library behind `work request`, `turn` and
`resolve`, `ask` and `reply` (capability requests). Every change is committed on the current branch (r12). A request
is a conversation on one GitHub issue on its upstream's repository; the step a command takes is posted there
(request_post), and this file is this side's record of it.

A request's `## Lines`, `## Questions`, `## Answers`, `## Outcomes` and `## Resolution` hold one entry a line,
`<n>. <text>`; the resolution's text is the requirement id and the version. A question's text is `line <l>: <words>`;
answer n answers question n. The text helpers and the turn rule are request_text's (plan 4, D24, D25).
"""
import re
from pathlib import Path

import request_form
import request_gh
import request_post
import request_side
import shop_files
from backlog_items import one_line
from request_text import (  # noqa: F401  (SETTLED: imported from here)
    REQUESTS,
    SETTLED,
    entries,
    field,
    next_number,
    numbered,
    requests,
    turned,
    with_entries,
    with_field,
)
from shop_files import Refused

ABOUT = ("A request between bounded contexts, kept by shopsystem-bdd's `work`: each step is a comment `work` posts, "
         "and only its block of fields is read.")


def path_of(root, ident):
    path = Path(root) / REQUESTS / (ident + ".md")
    if "/" in ident or not path.is_file():
        raise Refused("there is no request %s under %s" % (ident, REQUESTS))
    return path


def sections(root, ident):
    """Request `ident`'s Lines, Outcomes, Questions, Answers and Resolution, each as {number: text}."""
    text = shop_files.read(path_of(root, ident), root)
    return {name: dict(e.split(". ", 1) for e in entries(text, name) if ". " in e)
            for name in ("Lines", "Outcomes", "Questions", "Answers", "Resolution")}


def accepted_lines(root, ident):
    """(number, text) of each line of request `ident` whose line outcome is accepted."""
    text = shop_files.read(path_of(root, ident), root)
    outcomes = dict(e.split(". ", 1) for e in entries(text, "Outcomes") if ". " in e)
    lines = dict(e.split(". ", 1) for e in entries(text, "Lines") if ". " in e)
    return [(int(n), lines[n]) for n in sorted(lines, key=int) if outcomes.get(n) == "accepted"]


def asked_here(root):
    """(name, open questions) of each request whose asker is this context and whose status is awaiting-asker (supervision
    r101): a question is open when no answer of the same number is under `## Answers`."""
    try:
        mine = ("internal", "bounded-context/" + shop_files.context_path(root))
    except Refused:
        mine = ("internal",)
    found = []
    for name, status, _, _ in requests(root):
        text = shop_files.read(path_of(root, name), root)
        if status == "awaiting-asker" and field(text, "asker") in mine:
            answered = {e.split(". ", 1)[0] for e in entries(text, "Answers") if ". " in e}
            found.append((name, [e.split(". ", 1)[1] for e in entries(text, "Questions")
                                 if ". " in e and e.split(". ", 1)[0] not in answered]))
    return found


def _change(root, ident, message, edit, posting=None):
    """Rewrite request `ident` as `edit` makes it from its text, and commit it, and only it, then post on its issue
    what `posting` makes of the text before and after (request_post.committed); an edit that changes nothing (an
    upstream's turn that waits for `work accept`, on a request with no issue) commits nothing."""
    path = path_of(root, ident)
    text = shop_files.read(path, root)
    after = edit(text)
    request_post.committed(root, path, "work %s: %s" % (message, ident), after,
                           posting(text, after) if posting else None)


def upstreams(root):
    """The ids (without `bounded-context/`) of the bullets of spec/index.md's `## Upstreams`: the contexts this one asks."""
    index = Path(root) / "spec" / "index.md"
    section = re.search(r"(?ms)^## Upstreams\s*$(.*?)(?=^## |\Z)", index.read_text() if index.is_file() else "")
    found = [re.match(r"^- bounded-context/([^\s:]+):", line) for line in section.group(1).splitlines()] if section else []
    return [m.group(1).rsplit("/", 1)[-1] for m in found if m]


def own_askers(root):
    """The spellings of this repository's own asker: its context path, its last part and its bounded-context id (r32)."""
    path = shop_files.context_path(root)
    return {path, path.rsplit("/", 1)[-1], "bounded-context/" + path}


def gate(root, asker, sources, thread, raised_for):
    """Refuse, before anything is written, a request this repository may not raise: one given another asker than the
    repository's own (r32), and, where the repository asks an upstream, one with an origin (r30) or with neither a
    request it is raised for nor a job-thread (r31)."""
    if asker != "internal" and asker not in own_askers(root):
        raise Refused("this repository raises requests only as itself; it does not raise one for the asker %s" % asker)
    if upstreams(root):
        if sources and (thread is not None or raised_for is not None):
            raise Refused("an origin (--source) belongs to an internal request; a request to an upstream names none")
        if not sources and thread is None and raised_for is None:
            raise Refused("the request names neither a request it is raised for (--raised-for) nor a job-thread (--thread)")


def refuse_upstream_part(root, text, ident, part):
    """r34: refuse, naming the upstream, a write of `part` of a request to an upstream from this repository. A record
    names its `upstream`; one kept from before does not, and is to an upstream when its asker is this repository's own
    id, the repository lists upstreams and the request names no origin; an internal request (asker the upstream itself)
    is written by this repository as either side (r44, r15, r25)."""
    upstream = field(text, "upstream")
    if upstream is not None:
        if upstream != "bounded-context/" + shop_files.context_path(root):
            raise Refused("%s is a request to the upstream %s; the upstream writes %s" % (ident, upstream, part))
        return
    asked = upstreams(root)
    if asked and field(text, "asker") in own_askers(root) and field(text, "source") is None:
        raise Refused("%s is a request to the upstream %s; the upstream writes %s" % (ident, asked[0], part))


def upstream_of(root, sources, to):
    """The bounded-context id of the context a new request asks: `to` (an upstream under `## Upstreams`, by its id or
    its last part), else the one upstream of a request that names no origin, else this context itself (an internal
    request, its issue on this context's own repository)."""
    own = "bounded-context/" + shop_files.context_path(root)
    listed = list(request_gh.bullets(root))
    if to is not None:
        found = [c for c in listed + [own] if to in (c, c[len("bounded-context/"):], c.rsplit("/", 1)[-1])]
        if not found:
            raise Refused("work request: %s is no upstream under ## Upstreams in spec/index.md" % to)
        return found[0]
    if listed and not sources:
        if len(listed) > 1:
            raise Refused("work request: this context has the upstreams %s: name one with --to" % ", ".join(listed))
        return listed[0]
    return own


def request(root, title, asker, ask_text, sources, thread, raised_for=None, to=None):
    """Write the request, open in the upstream's turn, `q<n>` one above the highest kept, and commit it; then post
    its issue on its upstream's GitHub repository and commit the issue's URL into it (b36, r45: a commit git refuses
    opens no issue; an issue GitHub refuses takes the request out again); return (q<n>, the URL) (r27). An upstream that names
    no GitHub repository is refused before anything is posted (r28). The ask is the asker's own words; its lines
    come later (`work propose`), checked by the upstream."""
    if not sources and thread is None and raised_for is None:
        raise Refused("the request names neither an origin (--source) nor a job-thread (--thread)")
    title = one_line(title, "title")
    ask_text = (ask_text or title).strip()
    upstream = upstream_of(root, sources, to)
    repo = request_gh.repo_of(root, upstream, "work request")
    shop_files.git(root, "rev-parse", "--is-inside-work-tree")
    directory = Path(root) / REQUESTS
    name = "q%d" % next_number(root)
    ident = "request/%s/%s" % (shop_files.context_path(root), name)
    origin = ["part_of: %s" % thread] if thread is not None else ["source: [%s]" % ", ".join(sources)] if sources else []
    if raised_for is not None and re.fullmatch(r"q\d+", raised_for):     # a bare q<n> names a request of this context
        raised_for = "request/%s/%s" % (shop_files.context_path(root), raised_for)
    origin = "".join(o + "\n" for o in origin + (["raised_for: %s" % raised_for] if raised_for is not None else []))
    fields = {"step": "ask", "request": ident, "asker": asker, "upstream": upstream, "title": title, "ask": ask_text,
              "status": "open", "turn": "upstream"}

    def record(url=None):
        """The record, with the issue's URL once it is opened."""
        issue, comments = ("issue: %s\n" % url, "1. %s ask\n" % url) if url else ("", "")
        return ("---\nid: %s\nkind: request\nasker: %s\nupstream: %s\n%s%sstatus: open\nturn: upstream\n---\n\n"
                "# %s\n\n## Ask\n%s\n## Lines\n\n## Questions\n\n## Answers\n\n## Outcomes\n\n## Resolution\n\n"
                "## Comments\n%s" % (ident, asker, upstream, issue, origin, title, request_post.quoted(ask_text), comments))
    path = directory / (name + ".md")
    rel = str(path.relative_to(root))

    def write():
        directory.mkdir(parents=True, exist_ok=True)
        path.write_text(record())
    shop_files.committed(root, [rel], "work request: %s" % name, write)     # b36, r45: committed before it is posted
    try:
        url = request_gh.open_issue(root, repo, title, request_form.render(fields, None, ABOUT), "work request")
    except Refused:
        shop_files.committed(root, [rel], "work request: %s put back, its issue not opened" % name, path.unlink)
        raise
    shop_files.committed(root, [rel], "work request: %s posted" % name,
                         lambda: path.write_text(record(url)))
    return name, url


def ask(root, ident, number, question):
    """Write the next question, on line `number`, as `<n>. line <number>: <question>` (r20); the asker's turn refuses it."""
    def edit(text):
        refuse_upstream_part(root, text, ident, "the questions")
        if field(text, "turn") == "asker":
            raise Refused("%s is in the asker's turn; the upstream asks a question only in its own turn" % ident)
        asked = entries(text, "Questions")
        return with_entries(text, "Questions", asked + ["%d. line %d: %s" % (len(asked) + 1, number, question)])
    _change(root, ident, "ask", edit)


def reply(root, ident, number, answer):
    """Write `answer` as the answer to question `number`, under the same number (r21); the upstream's turn refuses it."""
    def edit(text):
        request_side.refuse_reply(root, text, ident)
        if field(text, "turn") == "upstream":
            raise Refused("%s is in the upstream's turn; the asker answers a question only in its own turn" % ident)
        return with_entries(text, "Answers", numbered(entries(text, "Answers"), number, answer))
    _change(root, ident, "reply", edit)


def turn(root, ident):
    """Pass the turn to the other side (r7, r8, r9, r17, r18, r23): `request_text.turned`, and post the side's part of
    the turn on the issue, closing it when the turn refused the request (r34-r37)."""
    def edit(text):
        request_side.refuse_turn(root, text, ident)
        return turned(text)
    _change(root, ident, "turn", edit, lambda text, after: request_post.turn_posting(text, after, "work turn"))


def resolve(root, ident, lines):
    """Write each accepted line's requirement and version, `lines` being (number, requirement, version), and set the
    status to delivered (r10, r11); a request that is not accepted is refused."""
    def edit(text):
        refuse_upstream_part(root, text, ident, "the resolution")
        if field(text, "status") != "accepted":
            raise Refused("%s is %s, not accepted; work resolve resolves only an accepted request" % (ident, field(text, "status")))
        held = []
        for number, requirement, version in lines:
            held = numbered(held, number, "%s %s" % (requirement, version))
        text = with_field(with_entries(text, "Resolution", held), "status", "delivered")
        return with_field(text, "turn", "asker")  # r24
    _change(root, ident, "resolve", edit, lambda _, after: request_post.posting(  # r41
        after, "resolve", {"Resolution": request_post.numbered(after, "Resolution")}, "work resolve", close=True))
