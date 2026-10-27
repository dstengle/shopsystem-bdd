"""The requests of a context, kept as .shop/work/requests/<id>.md: the library behind `work outcome`, `turn` and
`resolve`, `ask` and `reply` (capability requests). Every change is committed on the current branch (r12).

A request's `## Lines`, `## Questions`, `## Answers`, `## Outcomes` and `## Resolution` hold one entry a line,
`<n>. <text>`; the resolution's text is the requirement id and the version. A question's text is `line <l>: <words>`;
answer n answers question n.
"""
import json
import re
from pathlib import Path

import model_parse
import workqueue
import workqueue_done
from workqueue import Refused

SETTLED = ("accepted", "refused", "withdrawn")


def path_of(root, ident):
    path = Path(root) / workqueue.WORK / "requests" / (ident + ".md")
    if "/" in ident or not path.is_file():
        raise Refused("there is no request %s under %s" % (ident, workqueue.WORK / "requests"))
    return path


def _entries(text, name):
    found = re.search(r"(?ms)^## %s\n(.*?)(?=^## |\Z)" % name, text)
    return [line for line in found.group(1).splitlines() if line.strip()] if found else []


def accepted_lines(root, ident):
    """(number, text) of each line of request `ident` whose line outcome is accepted."""
    text = workqueue.read(path_of(root, ident), root)
    outcomes = dict(e.split(". ", 1) for e in _entries(text, "Outcomes") if ". " in e)
    lines = dict(e.split(". ", 1) for e in _entries(text, "Lines") if ". " in e)
    return [(int(n), lines[n]) for n in sorted(lines, key=int) if outcomes.get(n) == "accepted"]


def asked_here(root):
    """(name, open questions) of each request whose asker is this context and whose status is awaiting-asker (supervision
    r101): a question is open when no answer of the same number is under `## Answers`."""
    try:
        mine = ("internal", "bounded-context/" + workqueue.context_path(root))
    except Refused:
        mine = ("internal",)
    found = []
    for name, status, _, _ in workqueue.requests(root):
        text = workqueue.read(path_of(root, name), root)
        if status == "awaiting-asker" and field(text, "asker") in mine:
            answered = {e.split(". ", 1)[0] for e in _entries(text, "Answers") if ". " in e}
            found.append((name, [e.split(". ", 1)[1] for e in _entries(text, "Questions")
                                 if ". " in e and e.split(". ", 1)[0] not in answered]))
    return found


def _with_entries(text, name, entries):
    body = "## %s\n%s\n" % (name, "".join(entry + "\n" for entry in entries))
    if re.search(r"(?m)^## %s\n" % name, text):
        return re.sub(r"(?ms)^## %s\n.*?(?=^## |\Z)" % name, lambda _: body, text, count=1)
    return text.rstrip("\n") + "\n\n" + body


def _with_field(text, field, value):
    end = text.find("\n---", 4)
    return re.sub(r"(?m)^%s:.*$" % field, lambda _: "%s: %s" % (field, value), text[:end], count=1) + text[end:]


def field(text, field):
    found = re.search(r"(?m)^%s: *(.*)$" % field, text[:text.find("\n---", 4)])
    return found.group(1).strip() if found else None


def _change(root, ident, message, edit):
    """Rewrite request `ident` as `edit` makes it from its text, and commit it, and only it."""
    path = path_of(root, ident)
    text = workqueue.read(path, root)
    after = edit(text)
    workqueue.committed(root, [str(path.relative_to(root))], "work %s: %s" % (message, ident), lambda: path.write_text(after))


def _numbered(entries, number, text):
    kept = [e for e in entries if not e.startswith("%d. " % number)] + ["%d. %s" % (number, text)]
    return sorted(kept, key=lambda e: int(e.split(".", 1)[0]))


def upstreams(root):
    """The ids (without `bounded-context/`) of the bullets of spec/index.md's `## Upstreams`: the contexts this one asks."""
    index = Path(root) / "spec" / "index.md"
    section = re.search(r"(?ms)^## Upstreams\s*$(.*?)(?=^## |\Z)", index.read_text() if index.is_file() else "")
    found = [re.match(r"^- bounded-context/([^\s:]+):", line) for line in section.group(1).splitlines()] if section else []
    return [m.group(1).rsplit("/", 1)[-1] for m in found if m]


def own_askers(root):
    """The spellings of this repository's own asker: its context path, its last part and its bounded-context id (r32)."""
    path = workqueue.context_path(root)
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


def _refuse_upstream_part(root, text, ident, part):
    """r34: refuse, naming the upstream, a write of `part` of a request to an upstream from this repository. A request is
    to an upstream when its asker is this repository's own id, the repository lists upstreams and the request names no
    origin; an internal request (asker the upstream itself) is written by this repository as either side (r44, r15, r25)."""
    asked = upstreams(root)
    if asked and field(text, "asker") in own_askers(root) and field(text, "source") is None:
        raise Refused("%s is a request to the upstream %s; the upstream writes %s" % (ident, asked[0], part))


def request(root, title, asker, lines_file, sources, thread, delegation=None, raised_for=None):
    """Write a new open request in the upstream's turn, `q<n>` one above the highest kept; return q<n> (r1).

    A request that names neither an origin nor a job-thread is refused (r3), and so is one with a line not in the strict
    form `model check` holds (r2); a refusal writes nothing.
    """
    if delegation is not None and not delegation.strip():
        raise Refused("the delegation is empty")
    if not sources and thread is None and raised_for is None:
        raise Refused("the request names neither an origin (--source) nor a job-thread (--thread)")
    if not Path(lines_file).is_file():
        raise Refused("the file %s does not exist" % lines_file)
    lines = [line.strip() for line in workqueue.read(Path(lines_file), Path(lines_file).parent).splitlines() if line.strip()]
    for number, line in enumerate(lines, 1):
        if not all(model_parse.ears(line)):
            raise Refused("line %d is not in the strict form model check holds: %s" % (number, line))
    directory = Path(root) / workqueue.WORK / "requests"
    taken = [int(m.group(1)) for p in directory.glob("q*.md") if (m := re.fullmatch(r"q(\d+)\.md", p.name))]
    name = "q%d" % (max(taken, default=0) + 1)
    origin = ["part_of: %s" % thread] if thread is not None else ["source: [%s]" % ", ".join(sources)] if sources else []
    if raised_for is not None and re.fullmatch(r"q\d+", raised_for):     # a bare q<n> names a request of this context
        raised_for = "request/%s/%s" % (workqueue.context_path(root), raised_for)
    origin = "\n".join(origin + (["raised_for: %s" % raised_for] if raised_for is not None else []))
    given = "delegation: %s\n" % json.dumps(delegation) if delegation is not None else ""
    text = ("---\nid: request/%s/%s\nkind: request\nasker: %s\n%s\nstatus: open\nturn: upstream\n%s---\n\n# %s\n\n## Lines\n%s\n"
            "## Questions\n\n## Answers\n\n## Outcomes\n\n## Resolution\n"
            % (workqueue.context_path(root), name, asker, origin, given, title,"".join("%d. %s\n" % e for e in enumerate(lines, 1))))
    path = directory / (name + ".md")

    def write():
        directory.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    workqueue.committed(root, [str(path.relative_to(root))], "work request: %s" % name, write)
    return name


def outcome(root, ident, number, word):
    """Write line `number`'s outcome `word` (r12, r15); in the asker's turn it is refused, writing nothing (r16)."""
    def edit(text):
        _refuse_upstream_part(root, text, ident, "the line outcomes")
        if field(text, "turn") == "asker":
            raise Refused("%s is in the asker's turn; the upstream writes a line outcome only in its own turn" % ident)
        return _with_entries(text, "Outcomes", _numbered(_entries(text, "Outcomes"), number, word))
    _change(root, ident, "outcome", edit)


def ask(root, ident, number, question):
    """Write the next question, on line `number`, as `<n>. line <number>: <question>` (r20); the asker's turn refuses it."""
    def edit(text):
        _refuse_upstream_part(root, text, ident, "the questions")
        if field(text, "turn") == "asker":
            raise Refused("%s is in the asker's turn; the upstream asks a question only in its own turn" % ident)
        entries = _entries(text, "Questions")
        return _with_entries(text, "Questions", entries + ["%d. line %d: %s" % (len(entries) + 1, number, question)])
    _change(root, ident, "ask", edit)


def reply(root, ident, number, answer):
    """Write `answer` as the answer to question `number`, under the same number (r21); the upstream's turn refuses it."""
    def edit(text):
        if field(text, "turn") == "upstream":
            raise Refused("%s is in the upstream's turn; the asker answers a question only in its own turn" % ident)
        return _with_entries(text, "Answers", _numbered(_entries(text, "Answers"), number, answer))
    _change(root, ident, "reply", edit)


def turn(root, ident):
    """Pass the turn to the other side (r7); to the upstream it sets awaiting-upstream (r18). To the asker, the upstream
    ending its turn with every line settled sets the status (r8, r9), else awaiting-asker (r17)."""
    def edit(text):
        if field(text, "turn") == "asker":
            return _with_field(_with_field(text, "status", "awaiting-upstream"), "turn", "upstream")
        words = [e.split(". ", 1)[1] for e in _entries(text, "Outcomes") if ". " in e]
        if len(words) == len(_entries(text, "Lines")) and all(w in SETTLED for w in words):
            if field(text, "status") != "delivered":
                text = _with_field(text, "status", "accepted" if "accepted" in words else "refused")
                if "accepted" in words:
                    return text  # r23: the upstream's end that sets accepted keeps the turn
        else:
            text = _with_field(text, "status", "awaiting-asker")
        return _with_field(text, "turn", "asker")
    _change(root, ident, "turn", edit)


def resolve(root, ident, lines):
    """Write each accepted line's requirement and version, `lines` being (number, requirement, version), and set the
    status to delivered (r10, r11); a request that is not accepted is refused."""
    def edit(text):
        _refuse_upstream_part(root, text, ident, "the resolution")
        if field(text, "status") != "accepted":
            raise Refused("%s is %s, not accepted; work resolve resolves only an accepted request" % (ident, field(text, "status")))
        entries = []
        for number, requirement, version in lines:
            entries = _numbered(entries, number, "%s %s" % (requirement, version))
        text = _with_field(_with_entries(text, "Resolution", entries), "status", "delivered")
        return _with_field(text, "turn", "asker")  # r24
    path = path_of(root, ident)
    after =edit(workqueue.read(path, root))
    done = [d for d in workqueue_done.naming(root, ident) if workqueue_done.becomes(root, d, {ident: "delivered"})]

    def write():
        path.write_text(after)
        for directory in done:
            workqueue_done.mark(directory, root)
    rels = [str(p.relative_to(root)) for p in [path] + [d / "initiative.md" for d in done]]
    workqueue.committed(root, rels, "work resolve: %s" % ident, write)
