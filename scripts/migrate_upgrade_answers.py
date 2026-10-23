"""The 0.25.0 upgrade step "answers, not rulings" (migration-tools r29): the status awaiting-ruling becomes awaiting-answer
in every work-item's file and in every status field of every initiative's log, and the heading `## Rulings` becomes
`## Answers` in every work-item. Free text is left as it is. `plan` computes every change and writes none."""
import json
import re

from migrate_upgrade_ids import WORK, Changes, initiatives, work_items

OLD, NEW = "awaiting-ruling", "awaiting-answer"


def rewrite_item(text):
    """The work-item's text with its frontmatter status and its `## Rulings` heading renamed."""
    head, sep, body = text.partition("\n---\n")
    head = re.sub(r"^(status:[ \t]*)%s[ \t]*$" % OLD, r"\g<1>%s" % NEW, head, flags=re.M)
    body = re.sub(r"^## Rulings[ \t]*$", "## Answers", body, flags=re.M)
    return head + sep + body


def rewrite_log(text):
    """The log with each status field (`before`, `after`) holding the old status renamed; other lines as they were."""
    out = []
    for line in text.splitlines(True):
        entry = json.loads(line) if line.strip() else None
        if entry and OLD in (entry.get("before"), entry.get("after")):
            entry.update({k: NEW for k in ("before", "after") if entry.get(k) == OLD})
            line = json.dumps(entry) + ("\n" if line.endswith("\n") else "")
        out.append(line)
    return "".join(out)


def plan(root):
    changes = Changes()
    for directory in initiatives(root):
        rel = directory.relative_to(root).as_posix()
        for path in work_items(directory):
            text = path.read_text()
            if rewrite_item(text) != text:
                changes.texts["%s/%s" % (rel, path.name)] = rewrite_item(text)
        log = directory / "log.jsonl"
        if log.is_file() and rewrite_log(log.read_text()) != log.read_text():
            changes.texts[rel + "/log.jsonl"] = rewrite_log(log.read_text())
    return changes
