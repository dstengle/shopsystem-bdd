"""A model element and a term an item moves to another area, laid by `work batch start` (batches r117, r118, b607):
over batches_handlers_restate's world (the domain-model fixture's model, vocabulary and notebook beside readiness_world's
codified spec), an area `labels` with an empty model; the item's line of notebook beside its `### moves` block, which
moves notes' `object tag` to labels (r117) or shared's term `the person` to notes, the area that declares the actor
(r118); and the Thens read the model and vocabulary files off the batch's branch after the command."""
import shutil
import sys
from pathlib import Path

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's
LABELS = "---\nid: model/example.org/fixture/labels\narea: labels\nkind: core\nimports: []\n---\n\n# Labels\n\n" \
         "## Purpose\n\nThe labels notes carry.\n\n```model\n```\n"
LINE = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
        "archives the note, the notes service shall keep the note.\n\n### moves\n\n%s")
MOVES = {"model line": "- model line `object tag` from notes to labels",
         "term": "- term `the person → actor the person` from shared to notes"}
TERM = "- **the person** (proper noun) → actor the person. The human who keeps the notes."


def mine(step):
    """True when the step is of batches' scenarios of r117 and r118."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and bool({"r117", "r118"} & set(found.tags))


def _world(step):
    """The domain-model fixture beside readiness_world's codified spec, as batches_handlers_restate lays it, and the
    area labels."""
    if step.context.get("moving") is None:
        sys.modules["shop_readiness_world"].codify(step)
        spec = step.repo / "spec"
        for folder in ("model", "vocabulary"):
            shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
        shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
        index = spec / "index.md"
        index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))
        (spec / "model" / "labels.md").write_text(LABELS)
        step.context["moving"] = {}
    return step.context["moving"]


@four("GivenK", "area", *BOTH)
@four("GivenK", "term", *BOTH)
def given_named(step):
    """an area a1, a term t1: the world laid (a model line m1 lays it through batches_handlers_restate)."""
    if not mine(step):
        return False
    _world(step)
    return False if step.kind == "area" and step.context.get("restating") else None


@four("GivenDoes", "moves", *BOTH)
@four("GivenDoes", "move", *BOTH)
def given_moves(step):
    """the model line m1 moves to the area a1: noted; the item i1 moves the term t1: its `### moves` block moving
    the person into notes."""
    (k1, n1), (k2, _) = parts(step)
    if not mine(step):
        return False
    world = _world(step)
    if (k1, k2) == ("model line", "area"):
        world["kind"] = "model line"
    elif (k1, k2) == ("item", "term"):
        world["kind"] = "term"
        B.write_item(step, n1, sections={"Requirements": LINE % MOVES["term"]})
    else:
        return False


@four("GivenDoes", "means", *BOTH)
@four("GivenDoes", "mean", *BOTH)
def given_means(step):
    """the term t1 means the element e1: the person's entry names the actor the person."""
    if not mine(step) or [k for k, _ in parts(step)] != ["term", "element"]:
        return False


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the model line m1 that moves to an area: its `### moves` block moving `object tag` to
    labels; the area a1 holds the element e1: the fixture's notes declares the actor the person."""
    (k1, n1), (k2, _) = parts(step)
    kind = (step.context.get("moving") or {}).get("kind")
    if (k1, k2) == ("item", "model line") and kind == "model line":
        B.write_item(step, n1, sections={"Requirements": LINE % MOVES["model line"]})
    elif (k1, k2) != ("area", "element") or kind != "term":
        return False


def _branch(step, rel):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return T.git(step, "show", "%s:%s" % (branches[0], rel)).split("\n")


def _held(step):
    """The area's file on the batch's branch holds what the item moves, and the file it moved from does not."""
    kind = step.context["moving"]["kind"]
    if kind == "model line":
        target, source = _branch(step, "spec/model/labels.md"), _branch(step, "spec/model/notes.md")
        assert target.count("object tag") == 1 and "  relations: of → note (one)" in target, target
        assert "object tag" not in source and "imports: [labels]" in source, source
    else:
        target, source = _branch(step, "spec/vocabulary/notes.md"), _branch(step, "spec/vocabulary/shared.md")
        assert target.count(TERM) == 1 and TERM not in source, (target, source)


@four("ThenDoes", "holds", *BOTH)
def area_holds(step):
    """the area a1 holds the model line m1 (the term t1): on the batch's branch."""
    if parts(step)[0][0] != "area" or not step.context.get("moving", {}).get("kind"):
        return False
    _held(step)


def keeps(step):
    """the batches service keeps the area a1: its file on the batch's branch, holding what the item moves."""
    if parts(step)[1][0] != "area" or not step.context.get("moving", {}).get("kind"):
        return False
    _held(step)


for _verb in KEEPS:       # each key requested.py tries in turn of "keeps", so no other one passes
    four("ThenDoes", _verb, *BOTH)(keeps)
