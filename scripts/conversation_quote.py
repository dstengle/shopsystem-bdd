"""A quote (capability conversation; workflow simplification plan 8, D3-D6): the person's words, cited from one
message of a session's transcript with the two messages before it and the two after it, kept as `.shop/quotes/<n>.md`
and named `quote-<n>`, committed alone on the current branch. The file reads back as it was written whatever its text
holds (`parse(render(q), rel) == q`): each message is in a fence longer than any backtick run in it. Standard library
only."""
import datetime
import re
from dataclasses import dataclass, field
from pathlib import Path

import conversation_prompt
import conversation_read as C
import workqueue
from measure_read import Refused as ReadRefused
from measure_read import json_rows, moment, store_dir
from workqueue import Refused

QUOTES = Path(".shop") / "quotes"
LIMIT = 2000
LABEL = 60
WHO = {"person": "the person", "session": "the session"}
HEADING = re.compile(r"### (the person|the session), (\S+), (.+?)(, cited)?")


@dataclass
class Quote:
    name: str
    ident: str
    session: str
    message: str
    date: str
    words: str
    messages: list = field(default_factory=list)


def is_quote(name):
    return re.fullmatch(r"quote-[1-9]\d*", str(name)) is not None


def number(name):
    return int(name.split("-", 1)[1])


def rel_of(name):
    return (QUOTES / ("%d.md" % number(name))).as_posix()


def names(root):
    """The `quote-<n>` of each file of .shop/quotes/, by number; a `.md` file named otherwise is refused."""
    found = []
    for path in (Path(root) / QUOTES).glob("*.md"):
        if not re.fullmatch(r"[1-9]\d*", path.stem):
            raise Refused("%s: the file name is not <n>.md" % (QUOTES / path.name).as_posix())
        found.append("quote-%s" % path.stem)
    return sorted(found, key=number)


def next_name(root):
    return "quote-%d" % (max(map(number, names(root)), default=0) + 1)


def find(root, name):
    """The quote `name`; refused when it has no file."""
    if not is_quote(name) or not (Path(root) / rel_of(name)).is_file():
        raise Refused("there is no quote %s in %s/" % (name, QUOTES.as_posix()))
    rel = rel_of(name)
    quote = parse(workqueue.read(Path(root) / rel, root), rel)
    if quote.name != name:
        raise Refused("%s: id %s does not end in %s" % (rel, quote.ident, name))
    return quote


def label(quote):
    """How `work` names a quote: `quote-<n> "<its words, cut at 60 characters>"` (design goal 10)."""
    words = C.normal(quote.words)
    return '%s "%s"' % (quote.name, words if len(words) <= LABEL else words[:LABEL] + "…")


def fence(text):
    """Backticks one more than the longest run in `text`, at least three."""
    return "`" * max(3, 1 + max((len(run) for run in re.findall(r"`+", text)), default=0))


def render(quote):
    """The file's text, byte-stable (D3)."""
    head = ["id: %s" % quote.ident, "kind: quote", "session: %s" % quote.session, "message: %s" % quote.message,
            "date: %s" % quote.date]
    words = "\n".join("> " + line if line else ">" for line in quote.words.split("\n"))
    out = "---\n%s\n---\n\n# %s\n\n%s\n\n## Messages\n" % ("\n".join(head), quote.name, words)
    for m in quote.messages:
        mark = fence(m.text)
        cited = ", cited" if m.ident == quote.message else ""
        out += "\n### %s, %s, %s%s\n\n%stext\n%s\n%s\n" % (WHO[m.who], m.at.isoformat(), m.ident, cited, mark,
                                                          m.text, mark)
    return out


def parse(text, rel):
    """The quote of a file's text; any other shape is refused as `<rel>: <field> ...` (D3)."""
    data, body = workqueue.frontmatter(text)
    ident = data.get("id")
    if not isinstance(ident, str) or not re.fullmatch(r"quote/.+/quote-[1-9]\d*", ident):
        raise Refused("%s: id %r is not quote/<context path>/quote-<n>" % (rel, ident))
    if data.get("kind") != "quote":
        raise Refused("%s: kind %r is not quote" % (rel, data.get("kind")))
    for key in ("session", "message", "date"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise Refused("%s: %s is missing" % (rel, key))
    name = ident.rsplit("/", 1)[1]
    lines = body.split("\n")
    if lines[:2] != ["# %s" % name, ""]:
        raise Refused("%s: title: the file does not start with # %s" % (rel, name))
    at = 2
    words = []
    while at < len(lines) and lines[at].startswith(">"):
        words.append(lines[at][2:] if lines[at].startswith("> ") else lines[at][1:])
        at += 1
    if not words or lines[at:at + 3] != ["", "## Messages", ""]:
        raise Refused("%s: words: no > lines followed by ## Messages" % rel)
    messages = _messages(lines, at + 2, rel, data["message"])
    return Quote(name, ident, data["session"], data["message"], data["date"], "\n".join(words), messages)


def _messages(lines, at, rel, cited_ident):
    """The messages from `lines[at]` on: each a blank line, its heading, a blank line and its fence of text."""
    messages = []
    while lines[at:] != [""]:
        head = HEADING.fullmatch(lines[at + 1]) if lines[at:at + 1] == [""] and at + 1 < len(lines) else None
        opening = lines[at + 3] if at + 3 < len(lines) else ""
        if head is None or lines[at + 2:at + 3] != [""] or not re.fullmatch(r"`{3,}text", opening):
            raise Refused("%s: messages: not ### <who>, <time>, <ident> and a fence of text" % rel)
        mark, start = opening[:-len("text")], at + 4
        if mark not in lines[start:]:
            raise Refused("%s: messages: a fence is not closed" % rel)
        end = lines.index(mark, start)
        who, when, ident, cited = head.groups()
        if bool(cited) != (ident == cited_ident):
            raise Refused("%s: message: %s is the cited message, and only it is marked cited" % (rel, cited_ident))
        try:
            when = moment(when, rel)
        except ReadRefused as why:
            raise Refused(str(why)) from None
        messages.append(C.Message(ident, "person" if who == "the person" else "session", when,
                                  "\n".join(lines[start:end])))
        at = end + 1
    if not any(m.ident == cited_ident for m in messages):
        raise Refused("%s: message: %s is none of the messages" % (rel, cited_ident))
    return messages


def transcript_of(root, session, transcript):
    """(session id, transcript path) by D5's order: --transcript, then --session in any project of the store, then the
    pointer the UserPromptSubmit hook kept."""
    if transcript:
        path = Path(transcript)
        if not path.is_file():
            raise Refused("the transcript %s is not a file" % path)
        if not session:
            session = next((r["sessionId"] for r in _rows(path) if isinstance(r.get("sessionId"), str)), None)
            if not session:
                raise Refused("the transcript %s names no session; give --session <id>" % path)
        return session, path
    if session:
        found = sorted((store_dir() / "projects").glob("*/%s.jsonl" % session))
        if not found:
            raise Refused("there is no transcript of the session %s under %s" % (session, store_dir() / "projects"))
        return session, found[0]
    pointer = conversation_prompt.kept(root)
    if pointer is not None:
        if not Path(pointer[1]).is_file():
            raise Refused("the transcript %s the UserPromptSubmit hook kept for the session %s is not a file; give "
                          "--session <id>" % (pointer[1], pointer[0]))
        return pointer[0], Path(pointer[1])
    raise Refused("no session is known: the UserPromptSubmit hook keeps it (work quote --hook), or give --session <id>")


def _rows(path):
    try:
        return json_rows(path)
    except ReadRefused as why:
        raise Refused(str(why)) from None


def _cut(message, cited):
    if message is cited or len(message.text) <= LIMIT:
        return message
    return C.Message(message.ident, message.who, message.at, message.text[:LIMIT] + " […]")


def write(root, words, session=None, transcript=None):
    """The quote of `words` (D4), written as the next `.shop/quotes/<n>.md` and committed alone (D6)."""
    if not C.normal(words or ""):
        raise Refused("the words are empty")
    session, path = transcript_of(root, session, transcript)
    try:
        found = C.messages(path)
    except ReadRefused as why:
        raise Refused(str(why)) from None
    index = C.cited(found, words)
    if index is None:
        raise Refused('the person wrote no message with "%s" in the session %s; quote their words as they wrote them,'
                      ' or give --session <id>' % (C.normal(words)[:40], session))
    near = [_cut(m, found[index]) for m in C.around(found, index)]
    name = next_name(root)
    date = found[index].at.astimezone(datetime.UTC).date().isoformat()
    quote = Quote(name, "quote/%s/%s" % (workqueue.context_path(root), name), session, found[index].ident, date,
                  words.strip(), near)
    rel = rel_of(name)

    def put():
        target = Path(root) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(quote), encoding="utf-8")
    workqueue.committed(root, [rel], "quote: %s from the session %s" % (name, session[:8]), put)
    return quote
