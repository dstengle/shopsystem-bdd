"""The codified spec files read (design model v5; the GF conversion's design §8.3, §8.4, §10.2, §13.4).

`capability(path)` reads a capability file whose frontmatter has `language: codified-1` or `codified-2` (CNL 4's
I19): the groups of its `## Behaviour` (`### [g<n>] <title>`, an optional `Restates:` line, `- [r<n>] <statement>`
bullets and an optional fenced `given` block, read by spec_read_given), its `## Dropped` bullets and its `retired:`
ids. A statement kept out of a group's requirements (no id,
or an id used before) is in the group's `odd`, beside its problem. `## Terms` is not read here: spec_lexicon is the
one reader of term entries. `universal(root)` reads `spec/universal.md`, `restated(root)` reads `spec/restated.json`.
Nothing is refused: what is malformed is a problem `<line>: <what>`, with the file's own line number.
"""
import json
import re
from collections import namedtuple
from pathlib import Path

from model_parse import frontmatter
from spec_read_given import Block, GivenLines  # noqa: F401  (Block: what readers of `given` meet)

MARKER = "codified-1"
MARKER4 = "codified-2"      # a file in the new language, read through grammar 4 (CNL 4's call 15, I19)
MARKERS = (MARKER, MARKER4)

Capability = namedtuple("Capability", "path name frontmatter groups dropped retired problems")
Group = namedtuple("Group", "id title restates given requirements line_no odd")   # odd: (line, r<n> or None, text)
Requirement = namedtuple("Requirement", "id text line_no")
Universal = namedtuple("Universal", "id text line_no")
UniversalFile = namedtuple("UniversalFile", "path frontmatter conditions problems")


GROUP = re.compile(r"^### \[(g[1-9]\d*)\] (\S.*)$")
REQ = re.compile(r"^- \[(r[1-9]\d*)\] (\S.*)$")
U = re.compile(r"^- \[(U[1-9]\d*)\] (\S.*)$")
OLD = re.compile(r"^(?:(?P<cap>[a-z0-9]+(?:-[a-z0-9]+)*)#)?r(?P<n>[1-9]\d*)@0\.29$")
DROPPED = re.compile(r"^- (?:(?P<cap>[a-z0-9]+(?:-[a-z0-9]+)*)#)?r(?P<n>[1-9]\d*)@0\.29: (?P<why>\S.*)$")


def codified(path, markers=MARKERS):
    """True when the file's own frontmatter has one of `markers` as its `language:` (design §13.4): `codified-1` or
    `codified-2` unless a reader passes others."""
    path = Path(path)
    if not path.is_file():
        return False
    data, _ = frontmatter(path.read_text())
    return str(data.get("language", "")).strip() in markers


def numbered(text, title):
    """(line number, line) of the `## <title>` section of a file's text, numbered as in the file."""
    out, inside = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            inside = line[3:].strip().lower() == title.lower()
        elif inside:
            out.append((n, line))
    return out


def items(lines):
    """(line number, text) of each top-level '- ' bullet, continuation lines (indented two spaces) joined."""
    out = []
    for n, line in lines:
        if line.startswith("- "):
            out.append([n, line])
        elif out and line.startswith("  ") and line.strip() and out[-1] is not None:
            out[-1][1] += " " + line.strip()
        elif line.strip():
            out.append(None)          # a line that is no bullet ends the one before
    return [tuple(i) for i in out if i is not None]


class Reader(GivenLines):
    """One capability file's Behaviour read line by line into groups."""

    def __init__(self, name, retired):
        self.name, self.retired = name, set(retired)
        self.groups, self.problems, self.seen = [], [], set()
        self.group = self.fence = self.data_under = None

    def problem(self, n, what):
        self.problems.append((n, f"{n}: {what}"))

    def fresh(self, ident, n):
        if ident in self.seen:
            self.problem(n, f"{ident} appears a second time")
            return False
        self.seen.add(ident)
        if ident in self.retired:
            self.problem(n, f"{ident} is retired")
        return True

    def close_group(self):
        if self.group is not None and not self.group.requirements and any(g is self.group for g in self.groups):
            self.problem(self.group.line_no, f"{self.group.id} has no requirement")
        self.group = None

    def read(self, lines):
        for n, line in lines:
            if self.fence is not None:
                self.given_line(n, line)
            elif line.startswith("### "):
                self.heading(n, line)
            elif line.startswith("Restates:"):
                self.restates(n, line)
            elif line.strip() == "```given":
                self.fence = n
            elif line.startswith("- "):
                self.requirement(n, line)
            elif line.startswith("  ") and line.strip() and self.group and self.group.requirements:
                last = self.group.requirements[-1]
                self.group.requirements[-1] = last._replace(text=last.text + " " + line.strip())
        if self.fence is not None:
            self.problem(self.fence, "a given block is not closed")
        self.close_group()

    def heading(self, n, line):
        self.close_group()
        m = GROUP.match(line)
        if not m:
            self.problem(n, "a group heading is not '### [g<n>] <title>'")
        else:
            self.group = Group(m.group(1), m.group(2).strip(), [], [], [], n, [])
            if self.fresh(m.group(1), n):           # a second g<n> is read for its problems, and kept out
                self.groups.append(self.group)

    def restates(self, n, line):
        if self.group is None:
            self.problem(n, "a Restates: line outside a group")
            return
        for token in (t.strip() for t in line[len("Restates:"):].strip().rstrip(".").split(",")):
            m = OLD.match(token)
            if m:
                self.group.restates.append((m.group("cap") or self.name, int(m.group("n"))))
            else:
                self.problem(n, f"Restates: {token!r} is not r<n>@0.29 or <capability>#r<n>@0.29")

    def requirement(self, n, line):
        m = REQ.match(line)
        if self.group is None:
            self.problem(n, "a requirement outside a group")
        elif not m:
            self.problem(n, "a requirement is not '- [r<n>] <statement>'")
            self.group.odd.append((n, None, line[2:].strip()))      # a statement with no id (v15a)
        elif self.fresh(m.group(1), n):
            self.group.requirements.append(Requirement(m.group(1), m.group(2).strip(), n))
        else:
            self.group.odd.append((n, m.group(1), m.group(2).strip()))     # an id used a second time (v15b)


def dropped(name, lines):
    out, problems = [], []
    for n, text in items(lines):
        m = DROPPED.match(text)
        if m:
            out.append((m.group("cap") or name, int(m.group("n")), m.group("why").strip()))
        else:
            problems.append((n, f"{n}: a dropped line is not '- r<n>@0.29: <reason>'"))
    return out, problems


def capability(path, markers=MARKERS):
    """The groups, dropped ids and retired ids of a codified capability file, and its problems; a file whose marker
    is none of `markers` is read as not codified."""
    path = Path(path)
    text = path.read_text()
    data, _ = frontmatter(text)
    retired = [str(r) for r in data.get("retired") or []] if isinstance(data.get("retired") or [], list) else []
    name = path.stem
    if str(data.get("language", "")).strip() not in markers:
        return Capability(path, name, data, [], [], retired, [f"{path.name} is not codified (no language: {' or '.join(markers)})"])
    reader = Reader(name, retired)
    reader.read(numbered(text, "Behaviour"))
    gone, problems = dropped(name, numbered(text, "Dropped"))
    found = sorted(reader.problems + problems, key=lambda p: p[0])
    return Capability(path, name, data, reader.groups, gone, retired, [p for _, p in found])


def read_universal(root):
    """spec/universal.md: its frontmatter, its `- [U<n>] <statement>` conditions and its problems (a U<n> of its
    `retired:` used again among them)."""
    path = Path(root) / "spec" / "universal.md"
    if not path.is_file():
        return UniversalFile(path, {}, [], [])
    text = path.read_text()
    data, _ = frontmatter(text)
    problems, found, seen = [], [], set()
    retired = {str(r) for r in data.get("retired") or []} if isinstance(data.get("retired") or [], list) else set()
    if str(data.get("language", "")).strip() not in MARKERS:
        problems.append(f"universal.md is not codified (no language: {' or '.join(MARKERS)})")
    for n, item in items(numbered(text, "Behaviour")):
        m = U.match(item)
        if not m:
            problems.append(f"{n}: a universal condition is not '- [U<n>] <statement>'")
        elif m.group(1) in seen:
            problems.append(f"{n}: {m.group(1)} appears a second time")
        elif m.group(1) in retired:
            problems.append(f"{n}: {m.group(1)} is retired")
        else:
            seen.add(m.group(1))
            found.append(Universal(m.group(1), m.group(2).strip(), n))
    return UniversalFile(path, data, found, problems)


def universal(root):
    """The universal conditions U<n> of spec/universal.md, checked on every trace (design §8.4)."""
    return read_universal(root).conditions


def restated(root):
    """spec/restated.json: each 0.29 id `<capability>#r<n>` with its `text` and `line`, frozen from 96818f71."""
    path = Path(root) / "spec" / "restated.json"
    return json.loads(path.read_text()) if path.is_file() else {}


def is_guarantees(root, capability):
    """Whether spec/capabilities/<capability>.md under `root` has `group: guarantees` in its frontmatter."""
    path = Path(root) / "spec" / "capabilities" / (capability + ".md")
    head = path.read_text().split("---\n")[1:2] if path.is_file() else []
    return bool(head) and re.search(r"(?m)^group: guarantees$", head[0]) is not None
