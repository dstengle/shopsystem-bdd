"""The requests of a context, kept as .shop/requests/<id>.md: the library behind `work outcome`, `turn` and
`resolve`, `ask` and `reply` (capability requests). Every change is committed on the current branch (r12).

A request's `## Lines`, `## Questions`, `## Answers`, `## Outcomes` and `## Resolution` hold one entry a line,
`<n>. <text>`; the resolution's text is the requirement id and the version. A question's text is `line <l>: <words>`;
answer n answers question n. The text helpers and the turn rule are request_text's (plan 4, D24, D25).
"""
import re
from pathlib import Path

import request_lines
import shop_files
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


def _change(root, ident, message, edit):
    """Rewrite request `ident` as `edit` makes it from its text, and commit it, and only it."""
    path = path_of(root, ident)
    text = shop_files.read(path, root)
    after = edit(text)
    shop_files.committed(root, [str(path.relative_to(root))], "work %s: %s" % (message, ident), lambda: path.write_text(after))


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
    """r34: refuse, naming the upstream, a write of `part` of a request to an upstream from this repository. A request is
    to an upstream when its asker is this repository's own id, the repository lists upstreams and the request names no
    origin; an internal request (asker the upstream itself) is written by this repository as either side (r44, r15, r25)."""
    asked = upstreams(root)
    if asked and field(text, "asker") in own_askers(root) and field(text, "source") is None:
        raise Refused("%s is a request to the upstream %s; the upstream writes %s" % (ident, asked[0], part))


def request(root, title, asker, lines_file, sources, thread, raised_for=None):
    """Write a new open request in the upstream's turn, `q<n>` one above the highest kept; return q<n> (r1).

    A request that names neither an origin nor a job-thread is refused (r3), and so is one with a line the upstream
    would not read (r2): one that does not parse in its requirement grammar, or, where its index is not codified, one
    not in the strict form `model check` holds (request_lines); a refusal writes nothing.
    """
    if not sources and thread is None and raised_for is None:
        raise Refused("the request names neither an origin (--source) nor a job-thread (--thread)")
    if not Path(lines_file).is_file():
        raise Refused("the file %s does not exist" % lines_file)
    lines = [line.strip() for line in shop_files.read(Path(lines_file), Path(lines_file).parent).splitlines() if line.strip()]
    request_lines.check(root, lines)
    directory = Path(root) / REQUESTS
    name = "q%d" % next_number(root)
    origin = ["part_of: %s" % thread] if thread is not None else ["source: [%s]" % ", ".join(sources)] if sources else []
    if raised_for is not None and re.fullmatch(r"q\d+", raised_for):     # a bare q<n> names a request of this context
        raised_for = "request/%s/%s" % (shop_files.context_path(root), raised_for)
    origin = "\n".join(origin + (["raised_for: %s" % raised_for] if raised_for is not None else []))
    text = ("---\nid: request/%s/%s\nkind: request\nasker: %s\n%s\nstatus: open\nturn: upstream\n---\n\n# %s\n\n## Lines\n%s\n"
            "## Questions\n\n## Answers\n\n## Outcomes\n\n## Resolution\n"
            % (shop_files.context_path(root), name, asker, origin, title,"".join("%d. %s\n" % e for e in enumerate(lines, 1))))
    path = directory / (name + ".md")

    def write():
        directory.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    shop_files.committed(root, [str(path.relative_to(root))], "work request: %s" % name, write)
    return name


def outcome(root, ident, number, word):
    """Write line `number`'s outcome `word` (r12, r15); in the asker's turn it is refused, writing nothing (r16)."""
    def edit(text):
        refuse_upstream_part(root, text, ident, "the line outcomes")
        if field(text, "turn") == "asker":
            raise Refused("%s is in the asker's turn; the upstream writes a line outcome only in its own turn" % ident)
        return with_entries(text, "Outcomes", numbered(entries(text, "Outcomes"), number, word))
    _change(root, ident, "outcome", edit)


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
        if field(text, "turn") == "upstream":
            raise Refused("%s is in the upstream's turn; the asker answers a question only in its own turn" % ident)
        return with_entries(text, "Answers", numbered(entries(text, "Answers"), number, answer))
    _change(root, ident, "reply", edit)


def turn(root, ident):
    """Pass the turn to the other side (r7, r8, r9, r17, r18, r23): `request_text.turned`."""
    _change(root, ident, "turn", turned)


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
    path = path_of(root, ident)
    after = edit(shop_files.read(path, root))
    shop_files.committed(root, [str(path.relative_to(root))], "work resolve: %s" % ident, lambda: path.write_text(after))
