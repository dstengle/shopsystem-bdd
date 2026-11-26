"""The decision a laid retirement leaves unenforced, superseded by the lay (b741, batches r173, r174; b750, r177, r178).

When a batch lays items whose blocks retire requirements (`retired:`, and the `retires:` pairs of their lines) that an
accepted design-decision names under `enforced_by`, the lay writes the decision's one successor into the worktree, in
the lay's commit (`lay`): decision_write's render of the old decision's title, under the slug `<old slug>-<first
item>`, its summary, tier, `verified_by` and `rests_on` kept, `enforced_by` with each retired id replaced by the lines
of whichever item retires it, `supersedes` the old decision, `source` each such item and `by` "the lay of <their
ids>", its `## Context` one paragraph a retired id, naming it and the item that retires it with its lines (`entries`
reads them back), and its `## Decision` the old one's; the old decision set `superseded` and the decisions index
written again. A decision already superseded by a successor of this batch's lay (none of its items `delivered`) that
a later lay retires ids of, as amend's relay does, has that successor written again with every item's retirements. An unlay (a park, review's parked items, amend's relay)
writes each successor of the lay again with the retirements of its items left (the old decision kept superseded),
and takes it out and sets the old decision `accepted` again only once no item of it is left (`unlay`). A decision
number taken on the base meanwhile is a merge's concern, as for one written by hand."""
import datetime
import re
from pathlib import Path

import backlog_items
import backlog_lines
import decision_write
from model_parse import DECISIONS, as_list, decision_files, frontmatter
from plumbing import shop_files

LAY = "the lay of "
PARAGRAPH = re.compile(r"^(?P<gone>\S+), which this decision's predecessor \S+ named under enforced_by, is retired by "
                       r"(?P<label>.*) \((?P<item>item/[^)\s]+)\) with (?P<lines>.*)\.$")


def by(idents):
    return LAY + ", ".join(idents)


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


def entries(body):
    """{item id: (its label, {retired id: [its lines]})} a successor's `## Context` names, in its order."""
    found = {}
    for paragraph in (_section(body, "Context") or "").split("\n\n"):
        match = PARAGRAPH.match(paragraph.strip())
        if match:
            lines = [] if match["lines"] == "no line" else match["lines"].split(", ")
            found.setdefault(match["item"], (match["label"], {}))[1][match["gone"]] = lines
    return found


def _successor(tree, path, data, body, retired, number=None, slug=None):
    """(its path relative to the tree, its text) of the successor of the decision at `path`; `retired` {item id:
    (label, {retired id: lines})}, a successor written again keeping its `number` and `slug`."""
    old = path.name.split("-", 1)[1][:-len(".md")]
    slug = slug or "%s-%s" % (old, next(iter(retired)).rsplit("/", 1)[-1])
    title = next((line.split(". ", 1)[-1] for line in body.splitlines() if line.startswith("# ")), old)
    listed, enforcers, context = as_list(data.get("enforced_by")), [], []
    for ident in listed:
        lines = [(item, label, got[ident]) for item, (label, got) in retired.items() if ident in got]
        enforcers += [i for _, _, ls in lines for i in ls] if lines else [ident]
        context += ["%s, which this decision's predecessor %s named under enforced_by, is retired by %s (%s) with %s."
                    % (ident, data["id"], label, item, ", ".join(ls) or "no line") for item, label, ls in lines]
    fields = {"summary": str(data.get("summary") or title), "tier": data.get("tier"),
              "enforced by": list(dict.fromkeys(enforcers)), "routes": as_list(data.get("verified_by")),
              "rests on": as_list(data.get("rests_on")), "supersedes": [data["id"]], "source": list(retired),
              "author": by(retired)}
    number = number or decision_write.next_number(tree)
    ident = "design-decision/%s/%s" % (shop_files.context_path(tree), slug)
    text = decision_write.render(number, title, ident, fields,
                                 [("Context", "\n\n".join(context)), ("Decision", _section(body, "Decision") or "")],
                                 datetime.date.today().isoformat())
    return (DECISIONS / ("%04d-%s.md" % (number, slug))).as_posix(), text


def _index(tree):
    from model_report import render_decisions
    index = Path(tree) / DECISIONS / "index.md"
    index.write_text(render_decisions(tree), encoding="utf-8")
    return index.relative_to(tree).as_posix()


def _lays(found):
    """{old id: (path, data, body)} of each successor a lay wrote among `found`."""
    return {as_list(data.get("supersedes"))[0]: (path, data, body) for path, (data, body) in found
            if str(data.get("by") or "").strip("\"'").startswith(LAY) and len(as_list(data.get("supersedes"))) == 1}


def _pending(tree, lays):
    """{old id: (path, data, body)} of the lays' successors none of whose items is `delivered` in the worktree: this
    batch's, which a later lay writes again; a delivered one is a decision like any other, superseded in its turn."""
    def delivered(ident):
        path = tree / backlog_items.rel_of(ident.rsplit("/", 1)[-1])
        return path.exists() and frontmatter(path.read_text(encoding="utf-8"))[0].get("status") == "delivered"
    return {old: found for old, found in lays.items() if not any(map(delivered, as_list(found[1].get("source"))))}


def _again(tree, path, old, retired):
    """The successor at `path` written again from the decision `old` with `retired`; its path."""
    number, slug = path.name.split("-", 1)
    rel, text = _successor(tree, old[0], old[1][0], old[1][1], retired, int(number), slug[:-len(".md")])
    (tree / rel).write_text(text, encoding="utf-8")
    return rel


def lay(tree, items, written=None):
    """Each decision of the worktree the items' retirements leave unenforced, accepted or superseded by an earlier
    lay's successor, superseded by one successor of every item retiring its ids, `(item, successor's path, old id)`
    added to `written`; the paths changed."""
    tree, changed = Path(tree), []
    retirements = [(item, retiring(item)) for item in items]
    found = _decisions(tree)
    pending = _pending(tree, _lays(found))
    for path, (data, body) in found:
        if any(path == p for p, _, _ in pending.values()):
            continue
        ident, enforced = data.get("id"), set(as_list(data.get("enforced_by")))
        new = {item.ident: (backlog_items.label(item), {r: ls for r, ls in got.items() if r in enforced})
               for item, got in retirements if enforced & set(got)}
        earlier = pending.get(ident) if data.get("status") == "superseded" else None
        if not ident or not new or (data.get("status") != "accepted" and not earlier):
            continue
        if earlier:
            retired = {k: v for k, v in entries(earlier[2]).items() if k not in new}
            rel = _again(tree, earlier[0], (path, (data, body)), dict(retired, **new))
        else:
            rel, text = _successor(tree, path, data, body, new)
            (tree / rel).write_text(text, encoding="utf-8")
            path.write_text(decision_write.marked(path.read_text(encoding="utf-8")), encoding="utf-8")
            changed.append(path.relative_to(tree).as_posix())
        changed.append(rel)
        if written is not None:
            written += [(item, rel, ident) for item, _ in retirements if item.ident in new]
    return list(dict.fromkeys(changed)) + [_index(tree)] if changed else []


def unlay(tree, items):
    """Each successor a lay of the items wrote written again with the retirements of the items of it left, or, with
    none left, taken out of the worktree and the decision it supersedes `accepted` again; the paths changed."""
    tree, changed, gone = Path(tree), [], {item.ident for item in items}
    found = _decisions(tree)
    olds = {data.get("id"): (path, (data, body)) for path, (data, body) in found}
    for old_id, (path, data, body) in _lays(found).items():
        if not gone & set(as_list(data.get("source"))):
            continue
        left = {k: v for k, v in entries(body).items() if k not in gone and k in as_list(data.get("source"))}
        old = olds.get(old_id)
        if left and old:
            changed.append(_again(tree, path, old, left))
            continue
        path.unlink()
        changed.append(path.relative_to(tree).as_posix())
        if old and old[0].exists() and old[1][0].get("status") == "superseded":
            old[0].write_text(re.sub(r"(?m)^status: superseded$", "status: accepted",
                                     old[0].read_text(encoding="utf-8"), count=1), encoding="utf-8")
            changed.append(old[0].relative_to(tree).as_posix())
    return changed + [_index(tree)] if changed else []


def said(written):
    """The lines `work batch start` prints and the batch brief holds: `<item>: <path> supersedes <old id>`."""
    return ["%s: %s supersedes %s" % (backlog_items.label(item), rel, old) for item, rel, old in written]
