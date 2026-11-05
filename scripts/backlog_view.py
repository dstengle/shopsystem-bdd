"""`work backlog` (capability backlog r6-r8, r17): every item of the backlog in one table a state, in rank order,
with what each item waits on, and the same as one JSON object (workflow simplification plan 2, D7-D9).

The score is (value + urgency) / size, low = small = 1, medium = 2, high = large = 3 (D7). Within a state items go by
score from high to low, ties to the item added first; an item missing a rating has no score and ranks after the
rated. An item is blocked by each dependency on an item that is not `delivered`, a missing one included (D9). Reading
only direct dependencies, the view never walks a cycle written by hand."""
import backlog_items
import batch_plan

WEIGHT = {"low-value": 1, "medium-value": 2, "high-value": 3, "low-urgency": 1, "medium-urgency": 2,
          "high-urgency": 3, "small": 1, "medium": 2, "large": 3}
STATE_ORDER = ("in-batch", "needs-input", "ready", "shaped", "idea", "delivered", "refused", "withdrawn")
COLUMNS = ("rank", "item", "title", "provenance", "value", "urgency", "size", "score", "waiting on")


def score(item):
    if None in (item.value, item.urgency, item.size):
        return None
    return (WEIGHT[item.value] + WEIGHT[item.urgency]) / WEIGHT[item.size]


def blockers(item, by_name):
    """(name, status or `missing`) of each item `item` depends on that is not `delivered`."""
    out = []
    for name in item.depends_on:
        status = by_name[name].status if name in by_name else "missing"
        if status != "delivered":
            out.append((name, status))
    return out


def ordered(items):
    """[(state, items in rank order)] in STATE_ORDER, a state with no items left out (D7, D8)."""
    def rank_key(item):
        found = score(item)
        return (found is None, -(found or 0), backlog_items.number(item.name))
    return [(state, sorted(its, key=rank_key)) for state in STATE_ORDER
            for its in [[i for i in items if i.status == state]] if its]


def first_line(item):
    question = item.question if item.status == "needs-input" else None
    return question.strip().splitlines()[0] if question and question.strip() else None


def progress(root, item):
    """{"name", "status", "tasks_done", "tasks"} of the batch an `in-batch` item is in, or None (plan 4, D26)."""
    batch = batch_plan.of_item(root, item.name) if item.status == "in-batch" else None
    if batch is None:
        return None
    return {"name": batch.name, "status": batch.status, "tasks_done": sum(t.status == "done" for t in batch.tasks),
            "tasks": len(batch.tasks)}


def waiting_on(item, by_name, root=None):
    said = ["blocked by %s (%s)" % (backlog_items.label(by_name[n]) if n in by_name else n, s)
            for n, s in blockers(item, by_name)]
    question = first_line(item)
    found = progress(root, item) if root is not None else None
    said += ["in %(name)s (%(status)s): %(tasks_done)d of %(tasks)d tasks done" % found] if found else []
    return said + (["question: %s" % question] if question else [])


def row_json(item, by_name, rank, root=None):
    out = backlog_items.as_dict(item)
    out.update(score=score(item), rank=rank,
               blocked_by=[{"id": n, "status": s} for n, s in blockers(item, by_name)])
    found = progress(root, item) if root is not None else None
    out.update({"batch": found} if found else {})
    return out


def rank_of(item, items):
    """The item's rank in its state's table."""
    return next(n for state, its in ordered(items) if state == item.status
                for n, i in enumerate(its, 1) if i.name == item.name)


def cell(text):
    return (text or "-").replace("|", "\\|")


def tables(root):
    items = backlog_items.items(root)
    if not items:
        return "the backlog is empty\n"
    by_name = {i.name: i for i in items}
    out = []
    for state, its in ordered(items):
        lines = ["## %s (%d)" % (state, len(its)), "", "| %s |" % " | ".join(COLUMNS),
                 "|" + "---|" * len(COLUMNS)]
        for n, item in enumerate(its, 1):
            found = score(item)
            cells = [str(n), item.name, item.title, item.provenance, item.value, item.urgency, item.size,
                     "%.2f" % found if found is not None else None, "; ".join(waiting_on(item, by_name, root))]
            lines.append("| %s |" % " | ".join(map(cell, cells)))
        out.append("\n".join(lines) + "\n")
    return "\n".join(out)


def as_json(root):
    items = backlog_items.items(root)
    by_name = {i.name: i for i in items}
    return {"items": [row_json(item, by_name, n, root) for _, its in ordered(items) for n, item in enumerate(its, 1)]}
