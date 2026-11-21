"""items' `work retitle` and `work split` (r48-r52, b459): an item retitled with the title the person gives
(`NEW`), and the title kept read off its file; a requirement `r<n>` an item holds written as its line `notes#r<n>` in
the item's `## Requirements` (what a refusal names it by), an item split with the requirements the step names, and the
item the split makes, which a Given brought in by name only (`an item i2`), bound to the file the run wrote."""
import re
import sys

F = sys.modules["shop_world_four"]
four, parts = F.four, F.parts
B, W = sys.modules["shop_backlog_world"], sys.modules["shop_work_queue_world"]

BOTH = ("backlog", "batches")
NEW = "A title the person gives"
CAPABILITY = "notes"
MADE = "(the item the split makes)"


def _ident(name):
    return "%s#%s" % (CAPABILITY, name)


def _section(lines):
    """An item's `## Requirements` holding the requirement lines `lines` (names `r<n>`), one group."""
    return "### %s\n\n#### [g1] What the item asks\n%s" % (CAPABILITY, "\n".join(
        "- [%s] The line of %s." % (r, r) for r in lines))


@four("WhenRuns", "`work retitle`", *BOTH)
def work_retitle(step):
    item = step.names[0]
    step.context["retitled"] = item
    B.run_work(step, "retitle", B.ident(item), NEW)


@four("ThenDoes", "write", *BOTH)
@four("ThenDoes", "commit", *BOTH)
def keeps_title(step):
    """`work` keeps the title t2: the retitled item's file holds the title the person gave, in the run's commit."""
    (k, name), = parts(step)[1:]
    if k != "title" or "retitled" not in step.context:
        return False
    item = step.context["retitled"]
    assert step.context["result"].returncode == 0, (step.text, step.context["result"].stderr)
    assert B.title_of(step, item) == NEW, (step.text, B.title_of(step, item))
    B.in_commits(step, B.item_rel(step.context, item))
    step.context.setdefault("titles", {})[name] = [item]


@four("GivenK", "requirement", *BOTH)
def given_requirement(step):
    step.context.setdefault("says", {})[step.names[0]] = _ident(step.names[0])


@four("GivenDoes", "holds", *BOTH)
def item_holds(step):
    (k1, item), (k2, req) = parts(step)
    if (k1, k2) != ("item", "requirement") or not _splitting(step):
        return False
    held = step.context.setdefault("held", {}).setdefault(item, [])
    held.append(req)
    fields = step.context.get("item_fields", {}).get(item, {})
    sections = dict(fields.get("sections", {"Notes": B.NOTE}), Requirements=_section(held))
    B.write_item(step, item, sections=sections)


def _splitting(step):
    """Whether the scenario's request splits an item (a batch's item holds its requirement otherwise)."""
    return any(" splits the item " in t for t in W.scenario_texts(step))


def _made(step, split):
    """The items the scenario names that a Given brings in by name only and the split does not act on: the item the
    split makes, its file left for the run to write."""
    texts = W.scenario_texts(step)
    when = next(i for i, t in enumerate(texts) if " splits " in t)
    before = texts[:when]
    out = []
    for name in sorted(step.context.get("items", {})):
        said = [t for t in before if re.search(r"\b%s\b" % name, t)]
        if name != split and said == ["an item %s" % name]:
            out.append(name)
    return out


@four("WhenRuns", "`work split`", *BOTH)
def work_split(step):
    split = step.names[0]
    made = _made(step, split)
    for name in made:      # the item the split makes: no file before the run
        (step.repo / step.context["items"].pop(name)).unlink()
        step.context["item_fields"].pop(name, None)
        step.context["says"].pop(name, None)
    reqs = [n for n in step.names if n in step.context.get("says", {}) and n.startswith("r")]
    before = {p.name for p in (step.repo / B.BACKLOG).glob("*.md")}
    for name in made:
        step.context.setdefault("items", {})[name] = MADE    # not written before the run
    done = B.run_work(step, "split", B.ident(split), *[a for r in reqs for a in ("--requirement", _ident(r))])
    written = sorted({p.name for p in (step.repo / B.BACKLOG).glob("*.md")} - before)
    for name, file in zip(made, written):
        rel = "%s/%s" % (B.BACKLOG, file)
        step.context["items"][name] = rel
        step.context["says"][name] = '%s "%s"' % (file[:-3], B.title_of(step, name))
    for name in made[len(written):]:
        step.context["items"].pop(name)
    return done


@four("ThenDoes", "holds", *BOTH)
def item_holds_then(step):
    """The item i2 holds the requirement r1: its file's `## Requirements` holds the line of r1."""
    (k1, item), (k2, req) = parts(step)
    if (k1, k2) != ("item", "requirement") or not _splitting(step):
        return False
    assert step.context["result"].returncode == 0, (step.text, step.context["result"].stderr)
    rel = B.item_rel(step.context, item)
    assert rel, (step.text, "no file of the item")
    text = (step.repo / rel).read_text()
    assert "### %s" % CAPABILITY in text and "- [%s] The line of %s." % (req, req) in text, (step.text, text)
