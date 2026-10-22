"""The 0.24.0 upgrade step "work-items named by ids" (migration-tools r25, r26): every work-item under .shop/work/ is
renamed `w<n>`, numbered from 1 by its initiative's number and then its file name; the file, its `runs/<name>/`, its
id, its heading, its initiative's log lines and its initiative's `blocked_by` and `depends_on` follow. Free text is
left as it is. `plan` computes every change and writes none."""
import json
import re

WORK = ".shop/work"


class Changes:
    """What a step will do: directories and files to rename with git (old, new), and files to write (path, text)."""

    def __init__(self):
        self.moves = []
        self.texts = {}


def context_path(root):
    match = re.search(r"^id:\s*bounded-context/(\S+)\s*$", (root / "spec/index.md").read_text(), re.M)
    return match.group(1)


def front_kind(text):
    head = text.split("\n---", 1)[0] if text.startswith("---\n") else ""
    match = re.search(r"^kind:\s*(\S+)\s*$", head, re.M)
    return match.group(1) if match else None


def initiatives(root):
    """The initiative directories, in the order of their number `i<n>`."""
    found = [(int(m.group(1)), d) for d in (root / WORK).iterdir() if d.is_dir() and (m := re.match(r"i(\d+)", d.name))]
    return [d for _, d in sorted(found, key=lambda pair: pair[0])]


def work_items(directory):
    return [p for p in sorted(directory.glob("*.md")) if front_kind(p.read_text()) == "work-item"]


def rewrite_item(text, old, new, ctx, names):
    """The item's text with its id `new`, a heading, and the work-item names its blocked_by and depends_on hold renamed."""
    text = re.sub(r"^id:.*$", "id: work-item/%s/%s" % (ctx, new), text, count=1, flags=re.M)
    head, sep, body = text[4:].partition("\n---\n")
    if not re.search(r"^# ", body, re.M):
        body = "\n# %s\n%s" % (old, body)
    pattern = re.compile(r"(?<![\w/-])(work-item/(?:%s/)?)?(%s)(?![\w-])" % (re.escape(ctx), "|".join(map(re.escape, sorted(names, key=len, reverse=True)))))

    def rename(match):
        return (match.group(1) or "") + names[match.group(2)]

    lines = [pattern.sub(rename, l) if re.match(r"(blocked_by|depends_on):", l) else l for l in head.splitlines(True)]
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


def plan(root):
    ctx, changes, number = context_path(root), Changes(), 0
    for directory in initiatives(root):
        items, names = work_items(directory), {}
        for path in items:
            number += 1
            names[path.stem] = "w%d" % number
        if not names:
            continue
        rel = directory.relative_to(root).as_posix()
        for path in items:
            new = names[path.stem]
            text = rewrite_item(path.read_text(), path.stem, new, ctx, names)
            if new != path.stem:
                changes.moves.append(("%s/%s.md" % (rel, path.stem), "%s/%s.md" % (rel, new)))
            changes.texts["%s/%s.md" % (rel, new)] = text
            if (directory / "runs" / path.stem).is_dir() and new != path.stem:
                changes.moves.append(("%s/runs/%s" % (rel, path.stem), "%s/runs/%s" % (rel, new)))
        log = directory / "log.jsonl"
        if log.is_file():
            changes.texts[rel + "/log.jsonl"] = rewrite_log(log.read_text(), names)
    return changes
