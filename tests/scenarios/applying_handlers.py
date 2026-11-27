"""Handlers of features/applying.feature (b872), each a `work_queue_world.local` that takes only a step of its
scenarios (`mine`), tried after applying_handlers_*'s, which take the steps of their own groups: an item applied to a
specification by the specification service's apply, made in process of spec_apply, on readiness_world's codified spec
(committed on `main`). The specification s1 is the spec of a worktree of the repository beside it on a branch of its
own (`workspace`), as a batch's is. The When builds the group's world (`applied`: the item i1, `b1`, holding the
`## Requirements` its group's world gives; of g1 readiness_world's PASSING line as `work-queue#r5`), applies the item
there and keeps the specification service's reply, a domain_envelope Response; the Thens read the reply and the
specification's files (`kept`, a file the apply done changed). `build` is the world of the laying port's lift and of
checking's apply refused (laying_handlers, checking_handlers_apply)."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
ID = "r5"                       # readiness_world's `block` gives the item's line this id in work-queue
CAP = "spec/capabilities/work-queue.md"
KEEPS = ("keep", "write", "commit", "make")


def scenario(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found if found is not None and Path(found.feature.filename).stem == "applying" else None


def mine(step):
    return scenario(step) is not None


def group(step, groups):
    """The tag of the scenario's group among `groups`, or None of a scenario of another feature or group."""
    found = scenario(step)
    return None if found is None else next((t for t in found.tags if t in groups), None)


def world(step):
    return step.context.setdefault("applying", {})


def R():
    return sys.modules["shop_readiness_world"]


def fixture(step):
    """The domain-model fixture's model, vocabulary, CLI contract and notebook beside the codified spec, the index
    importing the request pack."""
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary", "adapters"):
        shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
    index = spec / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))


def workspace(step, w):
    """The repository committed and the workspace a worktree of it; (the workspace, the item i1)."""
    import backlog_items
    W.init(step.repo)
    W.git(step.repo, "add", "-A")
    W.git(step.repo, "commit", "-q", "--allow-empty", "-m", "the world")
    tree = step.request.getfixturevalue("tmp_path_factory").mktemp("applying") / "w1"
    W.git(step.repo, "worktree", "add", "-q", "-b", "workspace", str(tree))
    w["tree"], w["item"] = tree, backlog_items.find(step.repo, "b1")
    return tree, w["item"]


def build(step, w=None):
    """The repository's codified spec with the item i1's line, committed, and the workspace a worktree of it."""
    R().codify(step)
    R().give_lines(step, "i1", R().PASSING)
    return workspace(step, {} if w is None else w)


def applied(step, block):
    """The codified spec, the item i1 holding what `block(step)` gives (None: written already), committed; the item,
    its ids renumbered past its capabilities' as `work batch start`'s pick renumbers them (batch_pick), applied to the
    workspace's specification, the reply kept."""
    import backlog_lines
    import spec_apply
    w = world(step)
    R().codify(step)
    text = block(step)
    if text is not None:
        sys.modules["shop_backlog_world"].write_item(step, "i1", sections={"Requirements": text})
    tree, item = workspace(step, w)
    backlog_lines.renumber(tree, item, {})
    w["response"] = spec_apply.apply(tree, [item])


def kept(step, rel):
    """The text of the specification's file `rel`, which the apply done changed."""
    w = world(step)
    assert w["response"].outcome == "done" and rel in w["response"].content["changed"], (step.text, rel, w["response"])
    return (w["tree"] / rel).read_text()


def given(step):
    """A Given of g1: what its world builds at the When."""
    if not mine(step):
        return False
    world(step)


def requests(step):
    """`the batches service applies the item i1 to the specification s1`: the item holding the PASSING line."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    applied(step, lambda s: R().give_lines(s, "i1", R().PASSING))


def then(step):
    """`the specification s1 holds the requirement r1`: its line in the capability file under its id; `the
    specification service keeps the specification s1`: the apply done."""
    if not mine(step) or "response" not in world(step):
        return False
    if step.term in KEEPS:
        assert world(step)["response"].outcome == "done", world(step)["response"]
    elif step.term == "holds":
        assert "- [%s] %s" % (ID, R().PASSING) in kept(step, CAP), kept(step, CAP)
    else:
        raise AssertionError("applying_handlers takes no Then %s %s: %s" % (step.template, step.term, step.text))


for _template in ("GivenK", "GivenK_A", "GivenCode", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)


def untaken(step):
    """A key of the applying scenarios' steps, which `features vocab --check` reads: what is left when the locals
    take no step."""
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


