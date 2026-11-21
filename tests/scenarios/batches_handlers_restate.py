"""A model line that restates an operation, laid by `work batch start` and taken out by `work batch park` (batches
r87, r88, b463): the domain-model fixture's spec as the world's (its operation `archive(note)`), the item's line of
notebook and its `### notes model` block holding notes' `archive` with a parameter added, and the Thens read `spec/model/notes.md` off the batch's branch after the command."""
import shutil
import sys
from pathlib import Path

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
MODEL = "spec/model/notes.md"
OLD = "  operation archive(note)  outcomes: done"
LINE = "  operation archive(note, reason)  outcomes: done"
BLOCK = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
         "archives the note, the notes service shall keep the note.\n\n### notes model\n\n```model\nservice notes\n%s\n```" % LINE)
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's


@four("GivenK", "model line", *BOTH)
def given_line(step):
    """a model line m1: notes' archive restated; beside readiness_world's codified spec (whose work-queue the world's
    batches build), the fixture's model, vocabulary and notebook, the index importing the request pack."""
    sys.modules["shop_readiness_world"].codify(step)
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary"):
        shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
    index = spec / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))
    step.context["restating"] = True


@four("GivenDoes", "restates", *BOTH)
@four("GivenDoes", "restate", *BOTH)
def given_restates(step):
    """the model line m1 restates the operation o1: so LINE says it, of the fixture's `archive(note)`."""
    if parts(step)[0][0] != "model line":
        return False


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the model line m1: its `### notes model` block; this domain model holds the model line m1:
    the batch's lay put it there (batches_world's make_batch)."""
    (k1, n1), (k2, _) = parts(step)
    if k2 != "model line":
        return False
    if k1 == "item":
        B.write_item(step, n1, sections={"Requirements": BLOCK})


def _model(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    branch = branches[0]
    return T.git(step, "show", "%s:%s" % (branch, MODEL)).split("\n")


@four("ThenDoes", "holds", *BOTH)
def model_holds(step):
    """this domain model holds the model line m1: the batch's notes model declares `archive` once, as the line
    says it."""
    (k1, _), (k2, _) = parts(step)
    if k1 not in ("domain model", "model") or k2 != "model line":     # "this domain model" is ("model", None)
        return False
    lines = _model(step)
    assert [x for x in lines if x.startswith("  operation archive(")] == [LINE], lines


@four("ThenDoesNot", "holds", *BOTH)
@four("ThenDoesNot", "hold", *BOTH)
def model_holds_not(step):
    """the domain model d1 does not hold the operation o1 (the line it was, laid over) or the model line m1 (taken
    out by the park, the operation's own line put back)."""
    (k1, _), (k2, _) = parts(step)
    if k1 != "domain model" or k2 not in ("operation", "model line"):
        return False
    lines = _model(step)
    gone, kept = (OLD, LINE) if k2 == "operation" else (LINE, OLD)
    assert gone not in lines and lines.count(kept) == 1, (step.text, lines)


def keeps(step):
    """the batches service keeps the model line m1 or the domain model d1: spec/model/notes.md on the batch's
    branch."""
    if parts(step)[1][0] not in ("model line", "domain model") or not step.context.get("restating"):
        return False
    lines = _model(step)
    if parts(step)[1][0] == "model line":
        assert LINE in lines, lines


for _verb in KEEPS:       # each key requested.py tries in turn of "keeps", so no other one passes
    four("ThenDoes", _verb, *BOTH)(keeps)
