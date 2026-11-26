"""A plugin pack imported and a model element or a term retired, laid by `work batch start` (batches r132-r134, b672).
r132: the item, ready and passing the bar with readiness_world's passing line, imports the plugin's pack p1 `time`
in its `### imports` block; the Thens read `spec/index.md`'s `imports:` off the batch's branch. r133, r134: over
batches_handlers_restate's world (the domain-model fixture's model, vocabulary and notebook beside readiness_world's
codified spec), the item's line of notebook beside its `### retirements` block, which retires notes' `event a note is
added` (the model line m1, which no line says) or the term t1 `low` of notes' layer; the area a1 is notes, and the
Thens read its model and vocabulary files off the batch's branch."""
import re
import shutil
import sys
from pathlib import Path

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's
PACK = "time"
LINE = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
        "archives the note, the notes service shall keep the note.\n\n### retirements\n\n%s")
RETIRES = {"model line": "- model line `event a note is added: raised by notes.add` in notes", "term": "- term `low → value note.priority "
           "low` in notes"}
GONE = {"model line": ("spec/model/notes.md", "event a note is added: raised by notes.add"),
        "term": ("spec/vocabulary/notes.md", "- **low** (adjective) → value note.priority low.")}


def mine(step):
    """True when the step is of batches' scenarios of r132-r134."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and bool({"r132", "r133", "r134"} & set(found.tags))


def _world(step, kind):
    """The pack's world (readiness_world's codified spec), or the domain-model fixture beside it, as
    batches_handlers_restate lays it."""
    world = step.context.setdefault("retiring", {})
    if world.get("kind") is None:
        sys.modules["shop_readiness_world"].codify(step)
        if kind != "pack":
            spec = step.repo / "spec"
            for folder in ("model", "vocabulary"):
                shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
            shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
            index = spec / "index.md"
            index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))
        world["kind"] = kind
    return world


@four("GivenK", "pack", *BOTH)
@four("GivenK", "term", *BOTH)
@four("GivenK", "model line", *BOTH)
def given_named(step):
    """a pack p1, a term t1, a model line m1: the world laid."""
    if not mine(step):
        return False
    _world(step, step.kind)


@four("GivenDoes", "imports", *BOTH)
@four("GivenDoes", "import", *BOTH)
@four("GivenDoes", "retires", *BOTH)
@four("GivenDoes", "retire", *BOTH)
def given_retires(step):
    """the item i1 imports the pack p1: its block of readiness_world's passing line, then its `### imports` block; the
    item i1 retires the model line m1 (the term t1): notebook's line, then its `### retirements` block."""
    (k1, n1), (k2, _) = parts(step)
    if not mine(step) or k1 != "item":
        return False
    _world(step, k2)
    if k2 == "pack":
        R = sys.modules["shop_readiness_world"]
        title = step.context.get("item_fields", {}).get(n1, {}).get("title", "Title of %s" % n1)
        text = R.block(title, R.PASSING) + "\n\n### imports\n\n- pack `%s`" % PACK
    else:
        text = LINE % RETIRES[k2]
    B.write_item(step, n1, sections={"Requirements": text})


def _show(step, rel):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return T.git(step, "show", "%s:%s" % (branches[0], rel))


def _imported(step):
    found = re.search(r"(?m)^imports: \[([^\]]*)\]$", _show(step, "spec/index.md"))
    assert found and PACK in [n.strip() for n in found.group(1).split(",")], found


@four("ThenDoes", "imports", *BOTH)
@four("ThenDoes", "import", *BOTH)
def imports(step):
    """this bounded context imports the pack p1: the batch's spec/index.md names it under `imports:`."""
    if (step.context.get("retiring") or {}).get("kind") != "pack":
        return False
    _imported(step)


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
    """the batches service keeps the pack p1 (the area a1): the index imports it (the area's file is on the batch's
    branch, without what the item retires)."""
    kind = (step.context.get("retiring") or {}).get("kind")
    if kind is None or parts(step)[1][0] not in ("pack", "area"):
        return False
    _imported(step) if kind == "pack" else _gone(step)


for _verb in KEEPS:       # each key requested.py tries in turn of "keeps", so no other one passes
    four("ThenDoes", _verb, *BOTH)(keeps)
