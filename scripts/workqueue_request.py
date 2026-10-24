"""The requests of a context, kept as .shop/work/requests/<id>.md: the library behind `work outcome`, `turn` and
`resolve` (capability requests). Every change is committed on the current branch (r12).

A request's `## Lines`, `## Outcomes` and `## Resolution` hold one entry a line, `<n>. <text>`; the resolution's text is
the requirement id and the version.
"""
import re
from pathlib import Path

import model_parse
import workqueue
from workqueue import Refused

SETTLED = ("accepted", "refused", "withdrawn")


def _path(root, ident):
    path = Path(root) / workqueue.WORK / "requests" / (ident + ".md")
    if "/" in ident or not path.is_file():
        raise Refused("there is no request %s under %s" % (ident, workqueue.WORK / "requests"))
    return path


def _entries(text, name):
    found = re.search(r"(?ms)^## %s\n(.*?)(?=^## |\Z)" % name, text)
    return [line for line in found.group(1).splitlines() if line.strip()] if found else []


def _with_entries(text, name, entries):
    body = "## %s\n%s\n" % (name, "".join(entry + "\n" for entry in entries))
    if re.search(r"(?m)^## %s\n" % name, text):
        return re.sub(r"(?ms)^## %s\n.*?(?=^## |\Z)" % name, lambda _: body, text, count=1)
    return text.rstrip("\n") + "\n\n" + body


def _with_field(text, field, value):
    end = text.find("\n---", 4)
    return re.sub(r"(?m)^%s:.*$" % field, lambda _: "%s: %s" % (field, value), text[:end], count=1) + text[end:]


def _field(text, field):
    found = re.search(r"(?m)^%s: *(.*)$" % field, text[:text.find("\n---", 4)])
    return found.group(1).strip() if found else None


def _change(root, ident, message, edit):
    """Rewrite request `ident` as `edit` makes it from its text, and commit it, and only it."""
    path = _path(root, ident)
    text = workqueue.read(path, root)
    after = edit(text)
    workqueue.committed(root, [str(path.relative_to(root))], "work %s: %s" % (message, ident), lambda: path.write_text(after))


def _numbered(entries, number, text):
    kept = [e for e in entries if not e.startswith("%d. " % number)] + ["%d. %s" % (number, text)]
    return sorted(kept, key=lambda e: int(e.split(".", 1)[0]))


def request(root, title, asker, lines_file, sources, thread):
    """Write a new open request in the upstream's turn, `q<n>` one above the highest kept; return q<n> (r1).

    A request that names neither an origin nor a job-thread is refused (r3), and so is one with a line not in the strict
    form `model check` holds (r2); a refusal writes nothing.
    """
    if not sources and thread is None:
        raise Refused("the request names neither an origin (--source) nor a job-thread (--thread)")
    lines = [line.strip() for line in workqueue.read(Path(lines_file), Path(lines_file).parent).splitlines() if line.strip()]
    for number, line in enumerate(lines, 1):
        if not all(model_parse.ears(line)):
            raise Refused("line %d is not in the strict form model check holds: %s" % (number, line))
    directory = Path(root) / workqueue.WORK / "requests"
    taken = [int(m.group(1)) for p in directory.glob("q*.md") if (m := re.fullmatch(r"q(\d+)\.md", p.name))]
    name = "q%d" % (max(taken, default=0) + 1)
    origin = "part_of: %s" % thread if thread is not None else "source: [%s]" % ", ".join(sources)
    text = ("---\nid: request/%s/%s\nkind: request\nasker: %s\n%s\nstatus: open\nturn: upstream\n---\n\n# %s\n\n## Lines\n%s\n"
            "## Outcomes\n\n## Resolution\n"
            % (workqueue.context_path(root), name, asker, origin, title, "".join("%d. %s\n" % e for e in enumerate(lines, 1))))
    path = directory / (name + ".md")

    def write():
        directory.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    workqueue.committed(root, [str(path.relative_to(root))], "work request: %s" % name, write)
    return name


def outcome(root, ident, number, word):
    """Write line `number`'s outcome `word` (r12)."""
    _change(root, ident, "outcome", lambda t: _with_entries(t, "Outcomes", _numbered(_entries(t, "Outcomes"), number, word)))


def turn(root, ident):
    """Pass the turn to the other side; the upstream ending its turn with every line settled sets the status (r8, r9)."""
    def edit(text):
        if _field(text, "turn") == "asker":
            return _with_field(text, "turn", "upstream")
        words = [e.split(". ", 1)[1] for e in _entries(text, "Outcomes") if ". " in e]
        if len(words) == len(_entries(text, "Lines")) and all(w in SETTLED for w in words):
            text = _with_field(text, "status", "accepted" if "accepted" in words else "refused")
        return _with_field(text, "turn", "asker")
    _change(root, ident, "turn", edit)


def resolve(root, ident, lines):
    """Write each accepted line's requirement and version, `lines` being (number, requirement, version), and set the
    status to delivered (r10, r11); a request that is not accepted is refused."""
    def edit(text):
        if _field(text, "status") != "accepted":
            raise Refused("%s is %s, not accepted; work resolve resolves only an accepted request" % (ident, _field(text, "status")))
        entries = []
        for number, requirement, version in lines:
            entries = _numbered(entries, number, "%s %s" % (requirement, version))
        return _with_field(_with_entries(text, "Resolution", entries), "status", "delivered")
    _change(root, ident, "resolve", edit)
