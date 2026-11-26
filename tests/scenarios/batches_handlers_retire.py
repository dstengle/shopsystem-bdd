"""A model element or a term retired, laid by `work batch start` (batches r133, r134, b672): over
batches_handlers_restate's world (the domain-model fixture's model, vocabulary and notebook beside readiness_world's
codified spec), the item's line of notebook beside its `### retirements` block, which retires notes' `event a note is
added` (the model line m1, which no line says) or the term t1 `low` of notes' layer; the area a1 is notes, and the
Thens read its model and vocabulary files off the batch's branch."""
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
RETIRES = {"model line": "- model line `event a note is added: raised by notes.add` in notes", "term": "- term `low → value note.priority "
           "low` in notes"}
GONE = {"model line": ("spec/model/notes.md", "event a note is added: raised by notes.add"),
        "term": ("spec/vocabulary/notes.md", "- **low** (adjective) → value note.priority low.")}


def mine(step):
    """True when the step is of batches' scenarios of r133 and r134."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and bool({"r133", "r134"} & set(found.tags))


def _world(step, kind):
    """The domain-model fixture beside readiness_world's codified spec, as batches_handlers_restate lays it."""
    world = step.context.setdefault("retiring", {})
    if world.get("kind") is None:
        sys.modules["shop_readiness_world"].codify(step)
        spec = step.repo / "spec"
        for folder in ("model", "vocabulary"):
            shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
        shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
        index = spec / "index.md"
        index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))
        world["kind"] = kind
    return world


@four("GivenK", "term", *BOTH)
@four("GivenK", "model line", *BOTH)
def given_named(step):
    """a term t1, a model line m1: the world laid."""
    if not mine(step):
        return False
    _world(step, step.kind)


@four("GivenDoes", "retires", *BOTH)
@four("GivenDoes", "retire", *BOTH)
def given_retires(step):
    """the item i1 retires the model line m1 (the term t1): notebook's line, then its `### retirements` block."""
    (k1, n1), (k2, _) = parts(step)
    if not mine(step) or k1 != "item":
        return False
    _world(step, k2)
    B.write_item(step, n1, sections={"Requirements": LINE % RETIRES[k2]})


def _show(step, rel):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return T.git(step, "show", "%s:%s" % (branches[0], rel))


def _gone(step):
    """The area's file on the batch's branch does not hold what the item retires, and the lay changed it."""
    rel, line = GONE[step.context["retiring"]["kind"]]
    assert line not in _show(step, rel).split("\n"), (step.text, rel)
    branch = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()[0]
    assert rel in T.git(step, "log", "--format=", "--name-only", "-1", branch, "--", rel), rel


@four("ThenDoesNot", "holds", *BOTH)
@four("ThenDoesNot", "hold", *BOTH)
def area_holds_not(step):
    """the area a1 does not hold the model line m1 (the term t1): on the batch's branch."""
    if parts(step)[0][0] != "area" or (step.context.get("retiring") or {}).get("kind") not in GONE:
        return False
    _gone(step)


def keeps(step):
    """the batches service keeps the area a1: the area's file is on the batch's branch, without what the item
    retires."""
    kind = (step.context.get("retiring") or {}).get("kind")
    if kind is None or parts(step)[1][0] != "area":
        return False
    _gone(step)


for _verb in KEEPS:       # each key requested.py tries in turn of "keeps", so no other one passes
    four("ThenDoes", _verb, *BOTH)(keeps)
