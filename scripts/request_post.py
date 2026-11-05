"""A step of a request posted on its issue, and recorded (capability requests, r29-r41, intake r7): the comment's
block of fields read off the local record (request_form), posted through request_gh, and its URL written under the
record's `## Comments` as `<k>. <URL> <step>`, so that `work sync` never records it again (r32).

Each side posts its own part: the asker its lines and answers, the upstream its line outcomes, questions,
counter-proposals (with the lines they are), reasons, the capability each accepted line goes into and the resolution;
every comment carries the request's status and turn after the step. Which side this repository is comes from the
record: its `upstream` names the context that answers it, and its `asker` the one that asks. A record with no
`issue` (one kept from before requests went through issues) posts nothing."""
import request_form
import request_gh
import shop_files
from request_text import COUNTERS, entries, field, with_entries

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


def post(root, text, step, sections, command, fields=None, free="", close=False):
    """`text` with the comment of `step` posted on its issue and recorded; the issue closed after it when `close`."""
    url = field(text, "issue")
    if not url:
        return text
    posted = request_gh.comment(root, url, body(root, text, step, sections, fields, free), command)
    if close:
        request_gh.close(root, url, command)
    return with_comment(text, posted, step)


def posted_turn(root, before, after, command):
    """`after`, the record once a turn passed, with the turn posted by the side whose turn it was in `before`: its
    part, and the issue closed when the turn refused the request (r37)."""
    side = "asker" if field(before, "turn") == "asker" else "upstream"
    return post(root, after, "turn", part(after, side), command, close=field(after, "status") == "refused")
