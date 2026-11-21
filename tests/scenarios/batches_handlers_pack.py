"""A term of a context's own pack laid by `work batch start` (batches r95, b472): the item, ready and passing the bar
with readiness_world's passing line, holds the term t1 in its `### household pack` block (the pack p1 the context's own
`household`, which no file holds before the lay); the Thens read `spec/packs/household.md` and `spec/index.md` off the
batch's branch after the command, the pack in the lay's commit."""
import sys

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
PACK = "household"
FILE = "spec/packs/%s.md" % PACK
T1 = "- **pantry** (noun): a cupboard food is kept in."
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's


def _r():
    return sys.modules["shop_readiness_world"]


def mine(step):
    """True when the step is of batches' scenario of r95."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and "r95" in found.tags


@four("GivenK", "term", *BOTH)
@four("GivenK", "pack", *BOTH)
def given_named(step):
    """a term t1, a pack p1: the texts above."""
    if not mine(step):
        return False
    step.context["packing"] = True


@four("GivenDoes", "has", *BOTH)
def given_has(step):
    """the pack p1 has the term t1: the term is of the pack the item's block names."""
    if [k for k, _ in parts(step)] != ["pack", "term"] or not mine(step):
        return False


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the term t1: its block of readiness_world's passing line, then its `### household pack`
    block."""
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) != ("item", "term") or not mine(step):
        return False
    R = _r()
    R.codify(step)
    title = step.context.get("item_fields", {}).get(n1, {}).get("title", "Title of %s" % n1)
    text = R.block(title, R.PASSING) + "\n\n### %s pack\n\n%s" % (PACK, T1)
    B.write_item(step, n1, sections={"Requirements": text})


def _show(step, rel):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return T.git(step, "show", "%s:%s" % (branches[0], rel))


@four("ThenDoes", "has", *BOTH)
def has_term(step):
    """the pack p1 has the term t1: the batch's pack holds the entry under its `## Glossary`."""
    if [k for k, _ in parts(step)] != ["pack", "term"] or not step.context.get("packing"):
        return False
    text = _show(step, FILE)
    assert "## Glossary" in text and text.index("## Glossary") < text.index(T1), text


@four("ThenDoes", "imports", *BOTH)
@four("ThenDoes", "import", *BOTH)
def imports(step):
    """this bounded context imports the pack p1: the batch's spec/index.md names it under `imports:`."""
    if not step.context.get("packing"):
        return False
    import re
    found = re.search(r"(?m)^imports: \[([^\]]*)\]$", _show(step, "spec/index.md"))
    assert found and PACK in [n.strip() for n in found.group(1).split(",")], found


def keeps(step):
    """the batches service keeps the pack p1: spec/packs/household.md in the lay's commit on the batch's branch."""
    if parts(step)[1][0] != "pack" or not step.context.get("packing"):
        return False
    _show(step, FILE)
    branch = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()[0]
    assert FILE in T.git(step, "log", "--format=", "--name-only", "-1", branch, "--", FILE), FILE


for _verb in KEEPS:       # each key requested.py tries in turn of "keeps", so no other one passes
    four("ThenDoes", _verb, *BOTH)(keeps)
