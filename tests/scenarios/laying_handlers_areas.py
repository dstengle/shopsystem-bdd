"""Handlers of laying's g48 (r48, b830), `work_queue_world.local`s tried before laying_handlers' own, each taking only a
step of a scenario of that group (`mine`): an item that makes two areas, `watering` and `plots`, both new capabilities
of its own beside the domain-model fixture's spec, the term `plot` of the plots layer (its model line `object plot`)
and watering's requirement saying "a plot". The Givens record nothing; the When writes the item, commits the world,
makes the workspace w1 a worktree of it and lays the item there; the Thens read the reply's changed paths and the
workspace's files: watering's capability file kept, its model file kept and importing `plots`."""
import re
import shutil
import sys
from pathlib import Path

L = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/laying_handlers.py"))   # loaded before this, by name
R, W, world = L.R, L.W, L.world
B = sys.modules["shop_backlog_world"]
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
GROUP, USING, USED = "g48", "watering", "plots"
BLOCK = """### plots

narrator: a gardener
group: service
purpose: The plots of a garden, each kept by its name.

#### [g1] A plot added is kept
- [r1] When the person adds a note, the notes service shall keep the note.

### watering

narrator: a gardener
group: service
purpose: The watering of a garden's plots.

#### [g1] A plot watered is kept
- [r1] When the person adds a plot, the notes service shall keep the plot.

### plots model

```model
object plot
  attributes: name (text)
```

- **plot** (noun) → object plot. A piece of ground a gardener tends. Plural: plots."""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (found is not None and Path(found.feature.filename).stem == "laying"
            and GROUP in getattr(found, "tags", ()))


def given(step):
    """A Given of g48: what its world builds at the When."""
    if not mine(step):
        return False
    world(step)


def _world(step):
    """The domain-model fixture's model, vocabulary, CLI contract and notebook beside the codified spec, the index
    importing the request pack."""
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary", "adapters"):
        shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
    index = spec / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))


def requests(step):
    """`the batches service lays the item i1 in the workspace w1`: the world built, the item laid; the reply kept."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    import backlog_items
    import laying
    w = world(step)
    R().codify(step)
    _world(step)
    B.write_item(step, "i1", sections={"Requirements": BLOCK})
    W.init(step.repo)
    W.git(step.repo, "add", "-A")
    W.git(step.repo, "commit", "-q", "--allow-empty", "-m", "the world")
    tree = step.request.getfixturevalue("tmp_path_factory").mktemp("laying") / "w1"
    W.git(step.repo, "worktree", "add", "-q", "-b", "workspace", str(tree))
    w["tree"], w["item"] = tree, backlog_items.find(step.repo, "b1")
    w["response"] = laying.lay(w["item"], tree)


def _kept(step, rel):
    w = world(step)
    assert w["response"].outcome == "done" and rel in w["response"].content["changed"], (step.text, rel, w["response"])
    return (w["tree"] / rel).read_text()


def _imports(text):
    found = re.search(r"(?m)^imports: \[([^\]]*)\]$", text)
    return [n.strip() for n in found.group(1).split(",") if n.strip()] if found else []


def then(step):
    """`the laying service keeps `watering``: its capability file the lay changed; `keeps the area a1`: watering's
    model file the lay changed; `the area a1 imports `plots``: that model file's imports name plots."""
    if not mine(step) or "tree" not in world(step):
        return False
    term = "keep" if step.term in L.KEEPS else step.term
    model = "spec/model/%s.md" % USING
    if term == "keep" and "`%s`" % USING in step.text:
        _kept(step, "spec/capabilities/%s.md" % USING)
    elif term == "keep":
        _kept(step, model)
    elif term in ("import", "imports"):
        assert USED in _imports(_kept(step, model)), _kept(step, model)
    else:
        raise AssertionError("laying_handlers_areas takes no Then %s %s: %s" % (step.template, step.term, step.text))


for _template in ("GivenK", "GivenK_A", "GivenCode", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)
