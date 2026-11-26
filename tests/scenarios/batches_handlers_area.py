"""A capability new on an item laid in the area the item names (batches r129, b645): over batches_handlers4's new
capability `shelf` (its block with readiness_world's passing line), the area a1 `tracking`, which the block's `area:`
line names when the item holds it; the Thens read off the batch's branch after `work batch start`: the capability file
saying `area: tracking` and spec/index.md's `## Composition` naming the capability in the row of that area, both in
the lay's commit."""
import re
import sys

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
AREA = "tracking"


def mine(step):
    """True when the step is of batches' scenario of r129."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and "r129" in found.tags


@four("GivenK", "area", *BOTH)
def given_area(step):
    """an area a1: `tracking`, which no capability of the world's spec is in."""
    if not mine(step):
        return False
    step.context.setdefault("areas", {})[step.names[0]] = AREA


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the area a1 holds the capability c1: what the item's block will say; the item i1 holds the area a1: the new
    capability's block given its `area:` line after its purpose."""
    (k1, n1), (k2, _) = parts(step)
    if not mine(step) or (k1, k2) not in (("area", "capability"), ("item", "area")):
        return False
    if k1 == "item":
        rel = B.item_rel(step.context, n1)
        path = step.repo / rel
        text = path.read_text()
        purpose = re.search(r"(?m)^purpose: .*$", text)
        assert purpose, text
        path.write_text(text[:purpose.end()] + "\narea: %s" % AREA + text[purpose.end():])


def _branch(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    return T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()[0]


def _laid(step, name):
    """The capability file on the batch's branch, in the lay's commit there."""
    branch, rel = _branch(step), "spec/capabilities/%s.md" % step.context["new_capability"][name]
    assert rel in T.git(step, "log", "--format=", "--name-only", "-1", branch, "--", rel), rel
    return T.git(step, "show", "%s:%s" % (branch, rel))


@four("ThenDoes", "holds", *BOTH)
def holds_then(step):
    """the area a1 holds the capability c1: the capability file says `area: tracking` and the Composition row of
    `tracking` names the capability."""
    (k1, _), (k2, n2) = parts(step)
    if not mine(step) or (k1, k2) != ("area", "capability"):
        return False
    text = _laid(step, n2)
    assert re.search(r"(?m)^area: %s$" % AREA, text), text
    index = T.git(step, "show", "%s:spec/index.md" % _branch(step))
    rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in index.splitlines() if r.startswith("|")]
    names = [n.strip() for c in rows if c[0] == AREA for n in c[2].split(",")]
    assert step.context["new_capability"][n2] in names, index


def keeps(step):
    """the batches service keeps the capability c1: its file in the lay's commit on the batch's branch."""
    if not mine(step) or parts(step)[1][0] != "capability":
        return False
    _laid(step, parts(step)[1][1])


for _verb in ("write", "commit", "post", "keep", "make", "rewrite", "publish"):     # requested.py's, as pack's
    four("ThenDoes", _verb, *BOTH)(keeps)
