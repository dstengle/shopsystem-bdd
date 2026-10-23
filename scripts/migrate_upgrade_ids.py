"""The 0.24.0 upgrade step "work-items named by ids" (migration-tools r25, r26): every work-item under .shop/work/ is
renamed `w<n>`, numbered from 1 by its initiative's number and then its file name; the file, its `runs/<name>/`, its
id, its heading, its initiative's log lines, and every work-item's `blocked_by`, `depends_on` and `for` that names it
(in any initiative) follow. Free text, comments and `#r<n>` qualified names are left as they are. `plan` computes every change and writes none."""
import json
import re

WORK = ".shop/work"


class Changes:
    """What a step will do: directories and files to rename with git (old, new), and files to write (path, text)."""

    def __init__(self):
        self.moves = []
        self.texts = {}
        self.failures = []


def context_path(root):
    index = root / "spec/index.md"
    match = re.search(r"^id:\s*bounded-context/(\S+)\s*$", index.read_text() if index.is_file() else "", re.M)
    return match.group(1) if match else None


def front_kind(text):
    head = text.split("\n---", 1)[0] if text.startswith("---\n") else ""
    match = re.search(r"^kind:\s*(\S+)\s*$", head, re.M)
    return match.group(1) if match else None


def initiatives(root):
    """The initiative directories, in the order of their number `i<n>`."""
    if not (root / WORK).is_dir():
        return []
    found = [(int(m.group(1)), d) for d in (root / WORK).iterdir() if d.is_dir() and (m := re.match(r"i(\d+)", d.name))]
    return [d for _, d in sorted(found, key=lambda pair: (pair[0], pair[1].name))]


def work_items(directory):
    return [p for p in sorted(directory.glob("*.md")) if front_kind(p.read_text()) == "work-item"]


def rewrite_item(text, old, new, ctx, resolve, where):
    """The item's text with its id `new`, a heading, and the work-item names its blocked_by, depends_on and for hold
    renamed; `resolve(name, where, field)` gives the id a name now has, or None to leave it."""
    text = re.sub(r"^id:.*$", "id: work-item/%s/%s" % (ctx, new), text, count=1, flags=re.M)
    head, sep, body = text[4:].partition("\n---\n")
    if not re.search(r"^# ", body, re.M):
        body = "\n# %s\n%s" % (old, body)
    pattern = re.compile(r"(?<![\w/-])(work-item/(?:%s/)?)?([\w-]+)(?![\w#-])" % re.escape(ctx))

    def names_in(text, field):
        def rename(match):
            found = resolve(match.group(2), where, field)
            return match.group(0) if found is None else (match.group(1) or "") + found
        comment = re.search(r"\s#", text)
        cut = comment.start() if comment else len(text)
        return pattern.sub(rename, text[:cut]) + text[cut:]

    fields = r"(blocked_by|depends_on|for):"
    lines, listing = [], None
    for l in head.splitlines(True):
        key = re.match(fields + r"\s*$", l)
        listing = key.group(1) if key else (listing if listing and re.match(r"\s*-\s", l) else None)
        if re.match(fields, l):
            key, rest = l.split(":", 1)
            l = key + ":" + names_in(rest, key)
        elif listing:
            l = names_in(l, listing)
        lines.append(l)
    return "---\n" + "".join(lines) + sep + body


def rewrite_log(text, names):
    """The log with the `work-item` field of each line naming a renamed work-item renamed; other lines as they were."""
    out = []
    for line in text.splitlines(True):
        entry = json.loads(line) if line.strip() else None
        if entry and entry.get("work-item") in names:
            entry["work-item"] = names[entry["work-item"]]
            line = json.dumps(entry) + ("\n" if line.endswith("\n") else "")
        out.append(line)
    return "".join(out)


def resolver(held, own, failures):
    """A name's new id: the referring initiative's own, else the one initiative holding it; one several hold is refused."""
    def resolve(name, where, field):
        if name in own:
            return own[name]
        elsewhere = held.get(name, {})
        if len(elsewhere) > 1:
            failures.append("could not rename %s of %s: %s lists a work-item that initiatives %s all hold"
                            % (name, where, field, " and ".join(sorted(elsewhere))))
        return next(iter(elsewhere.values())) if len(elsewhere) == 1 else None
    return resolve


def plan(root):
    ctx, changes, number = context_path(root), Changes(), 0
    numbered, held = [], {}
    if ctx is None and any(work_items(d) for d in initiatives(root)):
        changes.failures.append("could not give the work-items their ids: spec/index.md has no bounded-context id")
        return changes
    for directory in initiatives(root):
        items, names = work_items(directory), {}
        for path in items:
            number += 1
            names[path.stem] = "w%d" % number
            held.setdefault(path.stem, {})[directory.name] = names[path.stem]
        if names:
            numbered.append((directory, items, names))
    for directory, items, names in numbered:
        rel = directory.relative_to(root).as_posix()
        for path in items:
            new = names[path.stem]
            resolve = resolver(held, names, changes.failures)
            text = rewrite_item(path.read_text(), path.stem, new, ctx, resolve, "%s/%s.md" % (rel, path.stem))
            if new != path.stem:
                changes.moves.append(("%s/%s.md" % (rel, path.stem), "%s/%s.md" % (rel, new)))
            changes.texts["%s/%s.md" % (rel, new)] = text
            if (directory / "runs" / path.stem).is_dir() and new != path.stem:
                changes.moves.append(("%s/runs/%s" % (rel, path.stem), "%s/runs/%s" % (rel, new)))
        log = directory / "log.jsonl"
        if log.is_file():
            changes.texts[rel + "/log.jsonl"] = rewrite_log(log.read_text(), names)
    return changes
