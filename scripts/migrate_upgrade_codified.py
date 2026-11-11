"""The 0.30.0 upgrade step "codified requirements" (the GF conversion's design §13.4, §15; migration-tools g29).

`plan` computes every change and writes none:
- `spec/restated.json`, when it is missing, from the live 0.29 ids of each capability without `language: codified-1`:
  `<cap>#r<n>` mapped to the line's text and line number (a table row's text is its lead sentence and its cells);
- each such capability's Behaviour turned into a scaffold: one group for each old line, `Restates:` filled, the old
  text as an HTML comment, no requirement bullets and no marker, `retired: []` and a `## Dropped` section;
  a codified capability is skipped;
- every scenario tagged `@deprecated` deleted from `features/`;
- every `<cap>#r<n>` of `.shop/work/**` that predates the conversion written `<cap>#r<n>@0.29` (a range is listed id by
  id): every tracked file when this step writes `spec/restated.json`, else the lines a file had at the commit that
  added `spec/restated.json`;
- `notes`: what is left for a session to write (the scaffolded capabilities, the glossary when it is untyped, and each
  open capability-proposal, whose 0.29 lines and ids the codified spec cannot take as they are).
"""
import json
import re
import subprocess

from migrate_upgrade_ids import Changes, context_path
from model_parse import frontmatter

RESTATED = "spec/restated.json"
CAPS = "spec/capabilities"
RID = re.compile(r"^\[r(\d+)\]\s*")
TABLE_ID = re.compile(r"^\[r\d+\]$")
MARKER = "codified-1"
CLOSED = ("merged", "formulated", "withdrawn")


def codified(text):
    return str(frontmatter(text)[0].get("language", "")).strip() == MARKER


def behaviour_items(lines):
    """(text, lead, line number, heading) of each line of a 0.29 Behaviour section (given as (number, line)): a
    top-level bullet with its continuation lines joined, or a table row whose first cell is `[r<n>]`, its other cells
    joined by ' | '; `lead` is the sentence just before the table, `heading` the `###` the line is under."""
    items, lead, open_bullet, paragraph, in_table, heading = [], None, False, False, False, None
    for n, line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            open_bullet = paragraph = False
            in_table = True
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if cells and (TABLE_ID.match(cells[0]) or re.fullmatch(r"r\d+", cells[0])):
                items.append([cells[0] + " " + " | ".join(cells[1:]), lead, n, heading])
            elif items and items[-1][1] is None and not RID.match(items[-1][0]) and items[-1][0].endswith(":"):
                lead = items.pop()[0]       # a bullet with no id that ends in ':' above a table leads it
            continue
        if in_table and stripped:
            lead, in_table = None, False
        if line.startswith(("- ", "* ")):
            items.append([stripped[2:].strip(), None, n, heading])
            lead = None if RID.match(items[-1][0]) else items[-1][0]
            open_bullet, paragraph = True, False
        elif open_bullet and line.startswith("  ") and stripped:
            items[-1][0] += " " + stripped
            lead = None if RID.match(items[-1][0]) else items[-1][0]
        elif stripped.startswith("#"):
            lead, open_bullet, paragraph = None, False, False
            heading = stripped[4:].strip() if stripped.startswith("### ") else None
        elif stripped and not line.startswith(" "):
            lead = lead + " " + stripped if paragraph else stripped
            open_bullet, paragraph = False, True
        elif not stripped:
            paragraph = False
    return [tuple(i) for i in items]


def behaviour(text):
    """(start, end) line indexes of the `## Behaviour` section's body, or None."""
    lines = text.splitlines()
    start = next((i + 1 for i, l in enumerate(lines) if l.strip().lower() == "## behaviour"), None)
    if start is None:
        return None
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


def old_lines(text):
    """(n, the line's text, line number, heading) of each 0.29 id of a capability's Behaviour, and the texts with no id."""
    span = behaviour(text)
    if span is None:
        return [], []
    lines = text.splitlines()
    numbered = [(i + 1, lines[i]) for i in range(*span)]
    found, loose = [], []
    for item, lead, n, heading in behaviour_items(numbered):
        m = RID.match(item)
        if not m:
            loose.append(item)
            continue
        said = item[m.end():]
        found.append((int(m.group(1)), lead + " | " + said if lead else said, n, heading))
    return found, loose


def comment(text):
    return "<!-- %s -->" % text.replace("--", "- -")


def scaffold(text):
    """The capability's text with its Behaviour as groups to write, `retired: []` and a `## Dropped` section."""
    found, loose = old_lines(text)
    start, end = behaviour(text)
    lines = text.splitlines()
    body = ["", comment("written by the 0.30.0 upgrade: write each group's requirements, then add `language: "
                        "codified-1` to the frontmatter")]
    body += [comment("no id: " + t) for t in loose]
    for g, (n, said, _, heading) in enumerate(found, 1):
        title = "%s (r%d@0.29)" % (heading, n) if heading else "r%d@0.29" % n
        body += ["", "### [g%d] %s" % (g, title), "Restates: r%d@0.29." % n, comment("r%d@0.29: %s" % (n, said))]
    rest = lines[end:]
    if not any(l.strip().lower() == "## dropped" for l in rest):
        while rest and not rest[-1].strip():
            rest.pop()
        rest += ([""] if rest else []) + ["## Dropped"]
    out = "\n".join(lines[:start] + body + [""] + rest) + "\n"
    return re.sub(r"(?m)\A(---\n(?:.*\n)*?)retired:.*\n", r"\1retired: []\n", out, count=1)


def capabilities(root):
    folder = root / CAPS
    return sorted(folder.glob("*.md")) if folder.is_dir() else []


def restated(root):
    out = {}
    for path in capabilities(root):
        text = path.read_text()
        if not codified(text):
            for n, said, line, _ in old_lines(text)[0]:
                out["%s#r%d" % (path.stem, n)] = {"text": said, "line": line}
    return out


SCENARIO = re.compile(r"^\s*(Scenario|Scenario Outline|Example|Scenarios|Rule|Background):")


def without_tagged(text, tag="@deprecated"):
    """The feature's text with every scenario tagged `tag` (its tags, its lines) left out; a docstring's lines are text,
    never a scenario or a tag."""
    lines = text.splitlines(True)
    starts, quoted = [], None
    for i, line in enumerate(lines):
        fence = line.strip()[:3]
        if fence in ('"""', "```"):
            quoted = None if quoted == fence else (quoted or fence)
        elif quoted is None and SCENARIO.match(line):
            j = i
            while j > 0 and lines[j - 1].strip().startswith(("@", "#")):
                j -= 1
            starts.append((j, i))
    keep = list(lines)
    for k, (start, head) in enumerate(starts):
        tags = " ".join(l for l in lines[start:head] if l.strip().startswith("@")).split()
        if tag in tags and not lines[head].strip().startswith(("Rule:", "Background:")):
            end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
            keep[start:end] = [None] * (end - start)
    return "".join(l for l in keep if l is not None)


def ref_pattern(root, names):
    ctx = context_path(root)
    pre = r"capability/(?:%s/)?" % re.escape(ctx) if ctx else r"capability/"
    caps = "|".join(sorted((re.escape(n) for n in names), key=len, reverse=True)) or "(?!)"
    return re.compile(r"(?<![\w.#/-])(?P<pre>%s)?(?P<cap>%s)#r(?P<a>\d+)(?:\s*[-–]\s*r?(?P<b>\d+))?(?![\w@-])"
                      % (pre, caps))


def ids(m):
    a, b = int(m.group("a")), int(m.group("b") or m.group("a"))
    if b < a:
        return [m.group(0)]
    return ["%s%s#r%d@0.29" % (m.group("pre") or "", m.group("cap"), n) for n in range(a, b + 1)]


def rewrite_line(line, pattern):
    item = re.match(r"^(\s*-\s+)(\S+)(\s*)$", line)
    m = pattern.fullmatch(item.group(2)) if item else None
    if m:
        return "".join(item.group(1) + i + "\n" for i in ids(m))[:-1] + item.group(3)
    return pattern.sub(lambda m: ", ".join(ids(m)), line)


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True).stdout


def blobs(root, tree):
    out = git(root, "ls-files", "-s", "--", ".shop/work") if tree is None else \
        git(root, "ls-tree", "-r", tree, "--", ".shop/work")
    return {l.split("\t", 1)[1]: l.split()[1] if tree is None else l.split()[2] for l in out.splitlines() if "\t" in l}


def references(root, names, frozen_here, changes):
    """Write the old references of each tracked file of .shop/work that predates the conversion."""
    pattern, now = ref_pattern(root, names), blobs(root, None)
    added = None if frozen_here else git(root, "log", "--diff-filter=A", "--format=%H", "--", RESTATED).split()
    freeze = added[-1] if added else None
    then = blobs(root, freeze) if freeze else None
    for rel in sorted(now):
        if then is not None and rel not in then:
            continue
        try:
            text = (root / rel).read_text()
        except (UnicodeDecodeError, OSError):
            continue
        old = None
        if then is not None and then[rel] != now[rel]:
            old = set(git(root, "show", "%s:%s" % (freeze, rel)).splitlines())
        lines = text.splitlines(True)
        new = "".join(l if old is not None and l.rstrip("\n") not in old else
                      rewrite_line(l.rstrip("\n"), pattern) + l[len(l.rstrip("\n")):] for l in lines)
        if new != text:
            changes.texts[rel] = new


def plan(root):
    changes = Changes()
    changes.notes = []
    frozen_here = not (root / RESTATED).is_file()
    names = {p.stem for p in capabilities(root)}
    if frozen_here and (root / CAPS).is_dir():
        found = restated(root)
        changes.texts[RESTATED] = json.dumps(found, indent=1) + "\n"
        changes.notes.append("wrote %s: the text of %d 0.29 ids" % (RESTATED, len(found)))
    elif not frozen_here:
        names |= {k.split("#", 1)[0] for k in json.loads((root / RESTATED).read_text())}
    for path in capabilities(root):
        text = path.read_text()
        if codified(text):
            continue
        if behaviour(text):
            changes.texts[path.relative_to(root).as_posix()] = scaffold(text)
        changes.notes.append("left for a session to write: %s (%d groups)"
                             % (path.relative_to(root).as_posix(), len(old_lines(text)[0])))
    for path in sorted((root / "features").rglob("*.feature")) if (root / "features").is_dir() else []:
        text = path.read_text()
        if without_tagged(text) != text:
            changes.texts[path.relative_to(root).as_posix()] = without_tagged(text)
    references(root, names, frozen_here, changes)
    index = root / "spec/index.md"
    if index.is_file() and not codified(index.read_text()):
        changes.notes.append("left for a session to write: the glossary of spec/index.md, in typed entries")
    for path in sorted((root / ".shop/work").glob("*/*.md")):
        data = frontmatter(path.read_text())[0]
        if data.get("kind") == "capability-proposal" and data.get("status") not in CLOSED:
            changes.notes.append("left for a session to write: %s, a capability-proposal that is `%s`, in 0.29 lines"
                                 % (path.relative_to(root).as_posix(), data.get("status")))
    return changes
