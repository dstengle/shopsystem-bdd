"""The decision a laid retirement leaves unenforced, superseded by the lay (b741, batches r173, r174).

When a batch lays an item whose block retires a requirement (`retired:`, and the `retires:` pairs of its lines) that an
accepted design-decision names under `enforced_by`, the lay writes the decision's successor into the worktree, in the
lay's commit (`lay`): decision_write's render of the old decision's title, under the slug `<old slug>-<item>`, its
summary, tier, `verified_by` and `rests_on` kept, `enforced_by` with each retired id replaced by the item's ids that
retire it, `supersedes` the old decision, `source` the item and `by` "the lay of <item id>", its `## Context` naming the
retired ids and the item and its `## Decision` the old one's; the old decision set `superseded` and the decisions index
written again. An unlay (a park, review's parked items, amend's relay) takes each successor of the item's lay out again
(`source` the item and `by` its lay's) and sets each decision it supersedes `accepted` again (`unlay`). A decision
number taken on the base meanwhile is a merge's concern, as for one written by hand."""
import datetime
import re
from pathlib import Path

import backlog_items
import backlog_lines
import decision_write
import shop_files
from model_parse import DECISIONS, as_list, decision_files, frontmatter


def by(item):
    return "the lay of %s" % item.ident


def retiring(item):
    """{retired `<cap>#r<n>`: [the item's `<cap>#r<m>` that retire it]} of the item's blocks."""
    found = {}
    for block in backlog_lines.read(item, backlog_items.rel_of(item.name)):
        for rid in block.retired:
            found.setdefault("%s#%s" % (block.capability, rid), [])
        for line, rid in block.retires:
            found.setdefault("%s#%s" % (block.capability, rid), []).append("%s#%s" % (block.capability, line))
    return found


def _decisions(tree):
    return [(path, frontmatter(path.read_text(encoding="utf-8"))) for path in decision_files(tree)]


def _section(body, name):
    found = re.search(r"(?ms)^## %s\n(.*?)(?=^## |\Z)" % re.escape(name), body)
    return found.group(1).strip() if found else None


def _successor(tree, path, data, body, item, retired):
    """(its path relative to the tree, its text) of the successor of the decision at `path`."""
    old = path.name.split("-", 1)[1][:-len(".md")]
    slug = "%s-%s" % (old, item.name)
    title = next((line.split(". ", 1)[-1] for line in body.splitlines() if line.startswith("# ")), old)
    enforcers = []
    for ident in as_list(data.get("enforced_by")):
        enforcers += retired.get(ident, [ident])
    gone = [i for i in as_list(data.get("enforced_by")) if i in retired]
    fields = {"summary": str(data.get("summary") or title), "tier": data.get("tier"),
              "enforced by": list(dict.fromkeys(enforcers)), "routes": as_list(data.get("verified_by")),
              "rests on": as_list(data.get("rests_on")), "supersedes": [data["id"]], "source": [item.ident],
              "author": by(item)}
    context = "%s, which this decision's predecessor %s named under enforced_by, %s retired by %s %s." % (
        ", ".join(gone), data["id"], "is" if len(gone) == 1 else "are", backlog_items.label(item),
        "with " + ", ".join(i for g in gone for i in retired[g]) if any(retired[g] for g in gone) else "with no line")
    number = decision_write.next_number(tree)
    ident = "design-decision/%s/%s" % (shop_files.context_path(tree), slug)
    text = decision_write.render(number, title, ident, fields,
                                 [("Context", context), ("Decision", _section(body, "Decision") or "")],
                                 datetime.date.today().isoformat())
    return (DECISIONS / ("%04d-%s.md" % (number, slug))).as_posix(), text


def _index(tree):
    from model_report import render_decisions
    index = Path(tree) / DECISIONS / "index.md"
    index.write_text(render_decisions(tree), encoding="utf-8")
    return index.relative_to(tree).as_posix()


def lay(tree, items, written=None):
    """Each accepted decision of the worktree an item's retirement leaves unenforced superseded by a successor
    written beside it, `(item, successor's path, old id)` added to `written`; the paths changed."""
    tree, changed = Path(tree), []
    for item in items:
        retired = retiring(item)
        if not retired:
            continue
        for path, (data, body) in _decisions(tree):
            if data.get("status") != "accepted" or not data.get("id") or \
                    not set(as_list(data.get("enforced_by"))) & set(retired):
                continue
            rel, text = _successor(tree, path, data, body, item, retired)
            (tree / rel).write_text(text, encoding="utf-8")
            path.write_text(decision_write.marked(path.read_text(encoding="utf-8")), encoding="utf-8")
            changed += [rel, path.relative_to(tree).as_posix()]
            if written is not None:
                written.append((item, rel, data["id"]))
    return changed + [_index(tree)] if changed else []


def unlay(tree, items):
    """Each successor an item's lay wrote taken out of the worktree, each decision it supersedes `accepted` again;
    the paths changed."""
    tree, changed = Path(tree), []
    for item in items:
        found = _decisions(tree)
        for path, (data, _) in found:
            if item.ident not in as_list(data.get("source")) or str(data.get("by") or "").strip("\"'") != by(item):
                continue
            path.unlink()
            changed.append(path.relative_to(tree).as_posix())
            olds = set(as_list(data.get("supersedes")))
            for other, (old, _) in found:
                if old.get("id") in olds and other.exists() and old.get("status") == "superseded":
                    other.write_text(re.sub(r"(?m)^status: superseded$", "status: accepted",
                                            other.read_text(encoding="utf-8"), count=1), encoding="utf-8")
                    changed.append(other.relative_to(tree).as_posix())
    return changed + [_index(tree)] if changed else []


def said(written):
    """The lines `work batch start` prints and the batch brief holds: `<item>: <path> supersedes <old id>`."""
    return ["%s: %s supersedes %s" % (backlog_items.label(item), rel, old) for item, rel, old in written]
