"""A step of a request posted on its issue, and recorded (capability requests, r29-r41, intake r7): the record is
committed first and the step posted after (b36, r45-r47: a commit git refuses posts nothing; a post GitHub refuses
puts the record back); the comment's block of fields read off the local record (request_form), posted through
request_gh, and its URL written under the record's `## Comments` as `<k>. <URL> <step>` in a second commit, so that
`work sync` never records it again (r32).

Each side posts its own part: the asker its lines and answers, the upstream its line outcomes, questions,
counter-proposals (with the lines they are), reasons, the capability each accepted line goes into and the resolution;
every comment carries the request's status and turn after the step. Which side this repository is comes from the
record: its `upstream` names the context that answers it, and its `asker` the one that asks. A record with no
`issue` (one kept from before requests went through issues) posts nothing."""
from pathlib import Path
from typing import NamedTuple

import request_form
import request_gh
import shop_files
from request_text import COUNTERS, entries, field, with_entries
from shop_files import Refused

ASKER_PART = ("Lines", "Answers")
UPSTREAM_PART = ("Outcomes", "Questions", COUNTERS, "Reasons", "Into", "Resolution")
COMMENTS = "Comments"


def quoted(text):
    """`text` with each line quoted (`> `), so that no line of it reads as a section of the record."""
    return "".join("> %s\n" % line if line else ">\n" for line in text.rstrip("\n").split("\n"))


def own_id(root):
    return "bounded-context/" + shop_files.context_path(root)


def numbered(text, section):
    """{number: text} of a numbered section."""
    return {n: t for n, t in (e.split(". ", 1) for e in entries(text, section) if ". " in e)}


def is_upstream(root, text):
    """Whether this repository answers the request: its `upstream` is this context (a record with no `upstream` is
    answered here, as before)."""
    upstream = field(text, "upstream")
    return upstream is None or upstream == own_id(root)


def is_asker(root, text):
    """Whether this repository asked the request: its `upstream` is another context, or its asker is this one (a
    record with no `upstream` is written here as either side, as before)."""
    import request_moves
    if field(text, "upstream") is None or not is_upstream(root, text):
        return True
    return field(text, "asker") in request_moves.own_askers(root) | {"internal"}


def part(text, side):
    """The sections of `side`'s part ('asker' or 'upstream') of the record, as {section: {number: text}}; the
    upstream's part also holds the lines its counter-proposals are."""
    if side == "asker":
        return {s: numbered(text, s) for s in ASKER_PART if numbered(text, s)}
    found = {s: numbered(text, s) for s in UPSTREAM_PART if numbered(text, s)}
    counters = set(numbered(text, COUNTERS).values())
    lines = {n: t for n, t in numbered(text, "Lines").items() if n in counters}
    if lines:
        found["Lines"] = lines
    return found


def recorded(text):
    """The URLs of the comments the record holds."""
    return {e.split(". ", 1)[1].split(" ", 1)[0] for e in entries(text, COMMENTS) if ". " in e}


def with_comment(text, url, step):
    held = entries(text, COMMENTS)
    return with_entries(text, COMMENTS, held + ["%d. %s %s" % (len(held) + 1, url, step)])


def body(root, text, step, sections, fields=None, free=""):
    """The comment of `step` on the record `text`: its block with the request's id, status and turn."""
    given = {"step": step, "request": field(text, "id"), "status": field(text, "status"), "turn": field(text, "turn")}
    return request_form.render(dict(given, **(fields or {})), sections, free)


class Posting(NamedTuple):
    """A step to post on a record's issue once the record is committed."""
    step: str
    sections: object
    command: str
    fields: object = None
    free: str = ""
    close: bool = False


def posting(text, step, sections, command, fields=None, free="", close=False):
    """The comment of `step` to post on the issue of the record `text` once it is committed, the issue closed after
    it when `close`; None for a record with no `issue`."""
    return Posting(step, sections, command, fields, free, close) if field(text, "issue") else None


def turn_posting(before, after, command):
    """The turn to post once `after`, the record with the turn passed, is committed: the part of the side whose turn
    it was in `before`, and the issue closed when the turn refused the request (r37)."""
    side = "asker" if field(before, "turn") == "asker" else "upstream"
    return posting(after, "turn", part(after, side), command, close=field(after, "status") == "refused")


def committed(root, path, message, after, posted=None, others=(), write=None):
    """Commit the record `after` at `path`, with the files `others` that `write` writes, and only then post `posted`
    on the record's issue and commit the comment's URL under `## Comments` (b36, r45-r47): a commit git refuses posts
    nothing; a record `after` leaves unchanged is committed empty before it is posted. A comment GitHub refuses puts the files back, in a commit, and is refused. Return the record."""
    path = Path(path)
    rels = [str(path.relative_to(root))] + list(others)
    before = [(Path(root) / rel).read_bytes() if (Path(root) / rel).exists() else None for rel in rels]

    def write_all():
        if write is not None:
            write()
        path.write_text(after)
    changed = write is not None or not path.is_file() or path.read_text() != after
    if changed:
        shop_files.committed(root, rels, message, write_all)
    if posted is None:
        return after
    if not changed:  # a step that leaves the record as it was (r36) is still committed, empty, before it is posted
        shop_files.committed(root, rels[:1], message, lambda: None, empty=True)
    url = field(after, "issue")
    try:
        said = request_gh.comment(root, url, body(root, after, posted.step, posted.sections, posted.fields,
                                                  posted.free), posted.command)
    except Refused:
        if changed:
            shop_files.committed(root, rels, "%s: put back, not posted" % message, lambda: _put_back(root, rels, before))
        raise
    final = with_comment(after, said, posted.step)
    shop_files.committed(root, rels[:1], "%s: posted" % message, lambda: path.write_text(final))
    if posted.close:
        request_gh.close(root, url, posted.command)
    return final


def _put_back(root, rels, before):
    for rel, data in zip(rels, before):
        target = Path(root) / rel
        target.unlink(missing_ok=True) if data is None else target.write_bytes(data)
