"""spec/index.md's `## Composition` written from the capability files (b606, batches r113-r115), as `work batch start`
writes it on every lay and the unlay of a parked item writes it again: the index form, one table `| area | kind |
capabilities |`, each area's row naming the capabilities of that area that hold a requirement (a `- [r<n>]` line of
their `## Behaviour`). A capability with no live requirement (retired, or every line moved) is named nowhere in the
index: its file, with `retired:` and `## Moved`, and spec/moves.json stay its record. The section's prose before its
first table or heading is kept; its subsections (the old tables and the Retired lists) are not. An area is a
capability's `area:`, else its name; its kind spec/model/<area>.md's `kind`, else the kind the section gave it (a row
of the table, or an old `### <area> (<kind>)` heading), else core. The areas and capabilities the section named keep
their order, the others follow in name order; the section is made at the end of the index when it has none and some
capability holds a requirement."""
import re
from pathlib import Path

import spec_read

HEADER = "| area | kind | capabilities |\n|---|---|---|"
SECTION = re.compile(r"(?ms)^## Composition[ \t]*\n(.*?)(?=^## |\Z)")
ROW = re.compile(r"(?m)^\|(.*)\|[ \t]*$")
HEADING = re.compile(r"(?m)^### (\S+) \(([^()\s]+)\)[ \t]*$")
NAMED = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`")


def _field(text, name):
    head = re.match(r"(?s)---\n(.*?)\n---", text)
    found = re.search(r"(?m)^%s:[ \t]*(\S.*?)[ \t]*$" % name, head.group(1)) if head else None
    return found.group(1) if found else None


def held(root):
    """(capability, area) of each capability file of `root` that holds a requirement, in name order."""
    found = []
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")):
        text = path.read_text()
        if any(spec_read.REQ.match(line) for _, line in spec_read.numbered(text, "Behaviour")):
            found.append((path.stem, _field(text, "area") or path.stem))
    return found


def _given(body):
    """The order of the areas and capabilities the section's `body` names, and the kinds it gives its areas."""
    order, kinds = [], {}
    for heading in HEADING.finditer(body):
        kinds.setdefault(heading.group(1), heading.group(2))
    for row in ROW.finditer(body):
        cells = [c.strip() for c in row.group(1).split("|")]
        if len(cells) == 3 and cells[0] not in ("area", "") and not set(cells[0]) <= set("-:"):
            kinds.setdefault(cells[0], cells[1])
            order += [cells[0]] + [n.strip().strip("`") for n in cells[2].split(",")]
        order += NAMED.findall(row.group(1))
    return order, kinds


def table(root, body=""):
    """The one table of the index form over `root`'s capability files, ordered and kinded as `body` gives."""
    order, kinds = _given(body)
    rank = {n: k for k, n in reversed(list(enumerate(order)))}

    def key(name):
        return (rank.get(name, len(rank)), name)
    areas = {}
    for name, area in held(root):
        areas.setdefault(area, []).append(name)
    model = Path(root) / "spec" / "model"
    rows = []
    for area in sorted(areas, key=lambda a: min([key(a)] + [key(n) for n in areas[a]])):
        path = model / ("%s.md" % area)
        kind = (_field(path.read_text(), "kind") if path.exists() else None) or kinds.get(area, "core")
        rows.append("| %s | %s | %s |" % (area, kind, ", ".join(sorted(areas[area], key=key))))
    return "%s\n%s\n" % (HEADER, "\n".join(rows)) if rows else ""


def composed(root, text):
    """spec/index.md's `text` with its `## Composition` in the index form over `root`'s capability files."""
    found = SECTION.search(text)
    if not found:
        rows = table(root)
        return text.rstrip("\n") + "\n\n## Composition\n\n" + rows if rows else text
    body = found.group(1)
    lead = re.split(r"(?m)^(?:###|\|)", body, maxsplit=1)[0].strip("\n")
    rows = table(root, body)
    now = ("\n" + lead + "\n" if lead.strip() else "") + ("\n" + rows if rows else "")
    if found.end() < len(text):
        now += "\n"
    return text[:found.start(1)] + now + text[found.end():]


def write(root):
    """spec/index.md of `root` written with its Composition in the index form; ["spec/index.md"] when it changed."""
    index = Path(root) / "spec" / "index.md"
    if not index.exists():
        return []
    was = index.read_text()
    now = composed(root, was)
    if now == was:
        return []
    index.write_text(now)
    return ["spec/index.md"]
