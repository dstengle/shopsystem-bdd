"""drafting's capability block taken out of an item and the capability another item holds (drafting r35-r37, b450), in
a fresh context as drafting_handlers_model founds it: spec/index.md in the new language and no capability file. Each a
`local` handler that takes a step of those scenarios (`mine`) and returns False on any other: the item holding the new
capability's block (and, of r35, its model block), a batch's plan naming the item it holds, `work line --remove
<capability>` (r35), `--capability <capability>` (r36) or `--into <capability> <line>` (r37) run on another item, and
the Thens that read the item back or what the refusal names. "another item that holds the capability" (i3) is the
item the Givens wrote it into."""
import importlib.util
import sys
from pathlib import Path


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
local = W.local
TAGS = {"r35", "r36", "r37"}
NAME = "checklists"
DECLARED = ("### checklists\n\nnarrator: a person keeping checklists\ngroup: service\n"
            "purpose: Checklists of things to do, each ticked off in turn.")
MODEL = "object checklist kind of file"
LINE = "When the person ticks a checklist, the checklists service shall keep the checklist."
INDEX = ("---\nid: bounded-context/ex.com/prod/ctx\ntitle: ctx\nlanguage: codified-2\nimports: [request]\n---\n\n"
         "# ctx\n")
PLAN = ("---\nid: batch/ex.com/prod/ctx/batch-1\nkind: batch\nstatus: building\nbase: main\nforked_from: 0000000\n"
        "branch: batch-1\npull_request:\n---\n\n# batch-1\n\n## Tasks\n\n| task | item | status | branch |\n"
        "|---|---|---|---|\n| t1 | %s | running | batch-1-%s |\n")


def mine(step):
    """True when the step is of drafting's scenarios of r35-r37."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    """{holder: the item that holds the capability, model: whether it holds a model line}, the fresh context once."""
    world = step.context.get("retract")
    if world is None:
        spec = step.repo / "spec"
        for folder in ("model", "vocabulary", "capabilities"):
            (spec / folder).mkdir(parents=True, exist_ok=True)
            (spec / folder / ".gitkeep").write_text("")
        (spec / "index.md").write_text(INDEX)
        world = step.context["retract"] = {"holder": None, "model": False, "batch": None}
    return world


def _write(step, world):
    """The holder written: shaped, or in-batch when a batch holds it, with the block and, of r35, its model block."""
    text = DECLARED + ("\n\n### %s model\n\n```model\n%s\n```" % (NAME, MODEL) if world["model"] else "")
    B.write_item(step, world["holder"], status="in-batch" if world["batch"] else "shaped",
                 sections={"Requirements": text})


@local("GivenK")
def given_named(step):
    """a capability, a model line, a requirement: what the item's block holds; a batch: its plan, once it holds an
    item; an item: the backlog's."""
    if not mine(step) or step.kind not in ("capability", "model line", "requirement", "batch"):
        return False
    _world(step)
    return None


@local("GivenDoesNot")
def given_absent(step):
    """the capability c1 does not exist: no spec/capabilities/<name>.md, as in a fresh context."""
    return None if mine(step) and step.term == "exist" else False


@local("GivenDoes")
def given_holds(step):
    """the item i1 holds the capability c1 or the model line m1; the batch b1 holds the item i1 (its plan naming the
    item's task, the item in-batch); the capability c1 has the requirement r1 (nothing more: r1 is what the When
    drafts)."""
    if not mine(step) or step.term not in ("holds", "has"):
        return False
    world = _world(step)
    if step.term == "has":
        return None
    if step.text.startswith("the batch "):
        world["batch"] = step.names[0]
        world["holder"] = step.names[1]
        path = step.repo / ".shop" / "batches" / "1" / "plan.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        b = B.ident(step.names[1])
        path.write_text(PLAN % (b, b))
        step.context.setdefault("says", {})[step.names[0]] = "batch-1"
    else:
        world["holder"] = step.names[0]
        world["model"] = world["model"] or "model line" in step.text
    _write(step, world)
    return None


def _options(step):
    return {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}


@local("WhenRuns")
def drafts(step):
    """r35: `work line <holder> --remove checklists`; r36: `work line i2 --capability checklists ...`; r37: `work line
    i2 --into checklists <line>`, the other item written shaped and empty first."""
    if not mine(step):
        return False
    world = _world(step)
    if "--remove" in _options(step):
        B.run_work(step, "line", B.ident(world["holder"]), "--remove", NAME)
        return None
    other = next(n for n in step.names if n.startswith("i") and n != world["holder"])
    B.write_item(step, other, status="shaped")
    if "--capability" in _options(step):
        B.run_work(step, "line", B.ident(other), "--capability", NAME, "--narrator", "a person", "Checklists.")
    else:
        B.run_work(step, "line", B.ident(other), "--into", NAME, LINE)
    return None


def _holder_text(step):
    return (step.repo / step.context["items"][step.context["retract"]["holder"]]).read_text()


@local("ThenDoes")
def done(step):
    """refuses: `work` exited non-zero; names the item i3 or the batch b1: the holder's label or `batch-1` in what it
    printed; the item i3 holds the capability c1: the holder's block is as the Givens wrote it."""
    if not mine(step):
        return False
    world, result = step.context["retract"], step.context["result"]
    said = result.stdout + result.stderr
    if step.term == "refuse":
        assert result.returncode != 0, said
    elif step.term == "name":
        name = step.names[-1]
        expected = "batch-1" if name == world["batch"] else step.context["says"][world["holder"]]
        assert expected in said, (expected, said)
    else:
        assert DECLARED in _holder_text(step), _holder_text(step)
    return None


@local("ThenDoesNot")
def taken(step):
    """the item i1 does not hold the capability c1 or the model line m1: neither block is in the item; the drafting
    service does not keep it: `work` exited 0 and committed the item so."""
    if not mine(step):
        return False
    result = step.context["result"]
    assert result.returncode == 0, (result.stdout, result.stderr)
    text = _holder_text(step)
    assert "### %s" % NAME not in text and MODEL not in text, text
    rel = step.context["items"][step.context["retract"]["holder"]]
    assert "### %s" % NAME not in W.git(step.repo, "show", "HEAD:%s" % rel), step.text
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return None
