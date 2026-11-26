"""A model element and the term that means it both retired by one item, laid by `work batch start` (batches r142,
b688). Over batches_handlers_retire's world (the domain-model fixture's model, vocabulary and notebook beside
readiness_world's codified spec), notes given an `object folder` that no line says and the term `folder` of notes'
layer that means it; the item's line of notebook beside its `### retirements` block, which retires the model line m1
(`object folder`, restating the element e1) and the term t1 (`folder`, meaning it); the area a1 is notes, and the
Thens read its vocabulary file off the batch's branch."""
import shutil
import sys
from pathlib import Path

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's
LINE = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
        "archives the note, the notes service shall keep the note.\n\n### retirements\n\n%s")
RETIRES = {"model line": "- model line `object folder` in notes", "term": "- term `folder → object folder` in notes"}
ENTRY = "- **folder** (noun) → object folder. A place a person keeps notes in."
VOCABULARY = "spec/vocabulary/notes.md"


def mine(step):
    """True when the step is of batches' scenario of r142."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and "r142" in found.tags


def _world(step):
    """batches_handlers_retire's world of a model line (as batches_handlers_restate lays it), notes given the object folder and its term; the retirements
    the item holds so far."""
    world = step.context.get("retiring_both")
    if world is None:
        sys.modules["shop_readiness_world"].codify(step)
        spec = step.repo / "spec"
        for folder in ("model", "vocabulary"):
            shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
        shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
        index = spec / "index.md"
        index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))
        model = spec / "model" / "notes.md"
        text = model.read_text()
        at = text.rindex("```")
        model.write_text(text[:at] + "\nobject folder\n  attributes: name (text)\n" + text[at:])
        vocabulary = step.repo / VOCABULARY
        vocabulary.write_text(vocabulary.read_text().rstrip("\n") + "\n" + ENTRY + "\n")
        world = step.context["retiring_both"] = {"retires": []}
    return world


@four("GivenK", "element", *BOTH)
@four("GivenK", "term", *BOTH)
@four("GivenK", "model line", *BOTH)
def given_named(step):
    """a model line m1, an element e1, a term t1: the world laid."""
    if not mine(step):
        return False
    _world(step)


@four("GivenDoes", "restates", *BOTH)
@four("GivenDoes", "restate", *BOTH)
@four("GivenDoes", "means", *BOTH)
@four("GivenDoes", "mean", *BOTH)
def given_element(step):
    """the model line m1 restates the element e1, the term t1 means the element e1: so the world says."""
    if not mine(step):
        return False
    _world(step)


@four("GivenDoes", "retires", *BOTH)
@four("GivenDoes", "retire", *BOTH)
def given_retires(step):
    """the item i1 retires the model line m1 (the term t1): notebook's line, then its `### retirements` block of
    each retirement so far."""
    (k1, n1), (k2, _) = parts(step)
    if not mine(step) or k1 != "item":
        return False
    world = _world(step)
    world["retires"].append(RETIRES[k2])
    B.write_item(step, n1, sections={"Requirements": LINE % "\n".join(world["retires"])})


def _gone(step):
    """notes' layer on the batch's branch does not hold the term, and the lay changed it."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    assert ENTRY not in T.git(step, "show", "%s:%s" % (branches[0], VOCABULARY)).split("\n"), step.text
    assert VOCABULARY in T.git(step, "log", "--format=", "--name-only", "-1", branches[0], "--", VOCABULARY)


@four("ThenDoesNot", "holds", *BOTH)
@four("ThenDoesNot", "hold", *BOTH)
def area_holds_not(step):
    """the area a1 does not hold the term t1: on the batch's branch."""
    if "retiring_both" not in step.context or parts(step)[0][0] != "area":
        return False
    _gone(step)


def keeps(step):
    """the batches service keeps the area a1: its layer is on the batch's branch, without the term."""
    if "retiring_both" not in step.context or parts(step)[1][0] != "area":
        return False
    _gone(step)


for _verb in KEEPS:       # each key requested.py tries in turn of "keeps", so no other one passes
    four("ThenDoes", _verb, *BOTH)(keeps)
