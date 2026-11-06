"""`work sync` (capability requests, r32, r33): what the other side of each request posted on its issue, recorded in
this side's record, and every request printed with its status and, unless it is closed, whose turn it is. Run on either side, it is how a person nudges
a conversation along ("check your requests").

A request this context answers that has no record yet is an open issue on this context's own GitHub repository whose
body is an `ask` form (request_form); it is written as a new `q<n>`. For each record with an issue, closed or not,
each comment it does not yet hold (`## Comments`, request_post) is read as its block of fields and recorded: only
the part of the side that posted its step is applied (r52), its entries written into their sections, by number, its
status and turn set, an offer kept under `## Offer`. The poster is the asker of an `ask` or a `fits`, the upstream of
an `offer`, an `accept` or a `resolve`, and of a `turn` the side whose turn the request was; an entry of the other
side's part (`own`) is recorded with its comment and never applied. A closed request's status and turn are never
set by a comment (r53), so a late comment reopens no request. A comment whose block does not parse, or that
holds none, is printed and never recorded, so it is printed again on the next sync. A comment recorded already is
passed over: sync is safe to run again. A record with no issue whose issue was opened but its URL never committed
(b36, f6) is given it, before the asks are read, so that it is not taken as a new request. The changed records are
one commit."""
from pathlib import Path

import intake_moves
import request_form
import request_gh
import request_moves
import request_post
import request_steps
import shop_files
from request_text import (
    REQUESTS,
    entries,
    field,
    next_number,
    numbered,
    with_entries,
    with_field,
)

CLOSED = ("delivered", "refused", "withdrawn")
COMMAND = "work sync"


ASKER_STEPS, UPSTREAM_STEPS = ("ask", "fits"), ("offer", "accept", "resolve")


def poster(text, step):
    """The side that posted `step` on the record `text`: 'asker' or 'upstream'; a turn is the side's whose turn the
    request was."""
    if step in ASKER_STEPS or step in UPSTREAM_STEPS:
        return "asker" if step in ASKER_STEPS else "upstream"
    return "asker" if field(text, "turn") == "asker" else "upstream"


def own(text, form, section, number):
    """Whether entry `number` of `section` in the comment `form` is of the part of the side that posted it, not a
    foreign entry: the asker's part is its lines and answers, and the resolution of a `fits`; the upstream's is the
    rest, and the lines its counter-proposals are."""
    if poster(text, form.step) == "asker":
        return section in request_post.ASKER_PART or (section == "Resolution" and form.step == "fits")
    if section == "Lines":
        counters = set(request_post.numbered(text, request_post.COUNTERS).values())
        return number in counters | set(form.sections.get(request_post.COUNTERS, {}).values())
    return section not in request_post.ASKER_PART


def applied(text, form, url):
    """The record `text` with the readable comment `form`, posted at `url`, recorded, and the poster's part of it
    written into it: a foreign entry is passed over, and a closed request keeps its status and turn."""
    before = text
    for section, given in form.sections.items():
        held = entries(text, section)
        for number in sorted((n for n in given if own(before, form, section, n)), key=int):
            held = numbered(held, int(number), given[number].replace("\n", " "))
        if held != entries(text, section):
            text = with_entries(text, section, held)
    for name in ("status", "turn"):
        if form.fields.get(name):
            text = with_field(text, name, form.fields[name].strip())
    if form.fields.get("offer") and poster(before, form.step) == "upstream":
        text = request_steps.with_offer(text, form.fields["offer"])
    return request_post.with_comment(text, url, form.step)


def taken(root, url, title, form, name):
    """The record of a request of another context (or of this one) this context answers, from its issue's ask."""
    fields = form.fields
    ident = "request/%s/%s" % (shop_files.context_path(root), name)
    text = ("---\nid: %s\nkind: request\nasker: %s\nupstream: %s\nissue: %s\nasked_as: %s\nstatus: open\n"
            "turn: upstream\n---\n\n# %s\n\n## Ask\n%s\n\n## Lines\n\n## Questions\n\n## Answers\n\n## Outcomes\n\n"
            "## Resolution\n\n## Comments\n1. %s ask\n"
            % (ident, fields.get("asker") or "unknown", request_post.own_id(root), url, fields.get("request") or url,
               (fields.get("title") or title).replace("\n", " "), request_post.quoted(fields.get("ask") or title), url))
    return text


def unreadable(out, url, where, why, body):
    out.append("unreadable comment %s on %s, not recorded (%s):" % (url, where, why))
    out.extend("    " + line for line in (body or "").strip().splitlines()[:20])


def unheld_issues(root, command=COMMAND):
    """[(URL, title, body)] of the open issues of this context's own repository whose body is a form (readable or
    not) that no record holds as its issue; none without a GitHub repository of its own."""
    try:
        repo = request_gh.own_repo(root, command)
    except shop_files.Refused:      # no GitHub repository of its own: no request can be asked of this context
        return []
    held = {field(shop_files.read(p, root), "issue") for p in (Path(root) / REQUESTS).glob("q*.md")}
    return [(url, title, body) for url, title, body in request_gh.listed(root, repo, command)
            if url not in held and request_form.is_form(body)]


def unheld_comments(root, text, command=COMMAND):
    """[(URL, body)] of the comments on the issue of the record `text` that it does not hold (`## Comments`)."""
    _, comments, _ = request_gh.view(root, field(text, "issue"), command)
    held = request_post.recorded(text)
    return [(url, body) for url, body in comments if url not in held]


def adopted(root, text):
    """The record `text`, which has no issue, with the issue opened for it whose URL was never committed (f6); `text`
    as it is when there is none, or its upstream is unhosted."""
    if not field(text, "upstream") or field(text, "status") in CLOSED:
        return text
    try:
        url = request_post.orphan_issue(root, text, COMMAND)
    except shop_files.Refused:
        return text
    if url is None:
        return text
    upstream = "\nupstream: %s\n" % field(text, "upstream")
    return request_post.with_comment(text.replace(upstream, upstream + "issue: %s\n" % url, 1), url, "ask")


def new_requests(root, writes, out):
    """The asks on this context's own repository that no record holds yet, written as new records."""
    number = next_number(root)
    taken_up = {field(t, "issue") for t in writes.values()}
    for url, title, body in unheld_issues(root):
        if url in taken_up:
            continue
        try:
            form = request_form.parse(body)
        except request_form.Unreadable as why:
            unreadable(out, url, "a new issue", why, body)
            continue
        if form.step != "ask":
            unreadable(out, url, "a new issue", "its step is %s, not ask" % form.step, body)
            continue
        name = "q%d" % number
        number += 1
        writes[Path(root) / REQUESTS / (name + ".md")] = taken(root, url, title, form, name)


def caught_up(root, name, text, out):
    """`text` with each comment of its issue it does not hold yet that is readable recorded."""
    for url, body in unheld_comments(root, text):
        try:
            form = request_form.parse(body)
            if form is None:
                raise request_form.Unreadable("it holds no block of fields")
        except request_form.Unreadable as why:
            unreadable(out, url, name, why, body)
            continue
        text = applied(text, form, url)
    return text


def waiting(root, status, text):
    """Whose move a live request waits on, in words; nothing for a closed one."""
    if status in CLOSED:
        return ""
    mine = request_post.is_upstream(root, text) if field(text, "turn") == "upstream" else request_post.is_asker(root, text)
    side = "this side" if mine else "the other side"
    return ": the %s's turn, waiting on %s" % (field(text, "turn"), side)


def sync(root):
    """Record what the other side posted, commit the records changed, and print every request."""
    writes, out = {}, []
    for name, status, _, _ in request_moves.requests(root):
        path = request_moves.path_of(root, name)
        text = shop_files.read(path, root)
        after = text if field(text, "issue") else adopted(root, text)
        if after != text:
            writes[path] = after
    new_requests(root, writes, out)
    for name, status, _, _ in request_moves.requests(root):
        path = request_moves.path_of(root, name)
        text = writes.get(path) or shop_files.read(path, root)
        if not field(text, "issue"):
            continue
        after = caught_up(root, name, text, out)
        if after != text:
            writes[path] = after
    if writes:
        rels = sorted(str(p.relative_to(root)) for p in writes)
        def write():
            for path, text in writes.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
        shop_files.committed(root, rels, "work sync: %s" % ", ".join(Path(r).stem for r in rels), write)
    for line in out:
        print(line)
    for name, status, _, _ in request_moves.requests(root):
        text = shop_files.read(request_moves.path_of(root, name), root)
        print("%s %s%s" % (intake_moves.named(name, text), status, waiting(root, status, text)))
    return 0
