"""An item picked whose ids collide with its capability's keeps what it holds beside its lines once `work batch
start`'s pick renumbers them (batches r190-r192, b764), `work_queue_world.local`s each taking only a step of a scenario
of one of their groups (`mine`). A scenario's world is its group's (`WORLDS`), written before `work batch start`
(batches_world's BEFORE_START), so the Givens record nothing: the item i1 `ready`, its group and requirement ids `g1`
and `r1`, which its capability holds already (laying_handlers_model's `colliding`), beside a term of the context's own
pack `household` (g190, laying_handlers_pieces' block, readiness_world's passing line in work-queue), a table of
`notes.archive` (g191, the same line, the contract holding another table of it before, as no model declares it on the
codified spec, which the request pack would not read the line in) or the term `the person` moved from shared to notes
(g192, notebook's line). The Thens read the batch's branch: the item's line laid under an id the pick gave it, in place
of `r1`, which the capability keeps, and what the item holds beside it (the pack's term under its `## Glossary`, the
contract's one table of `notes.archive`, notes' layer holding the term and shared's not)."""
import re
import sys
from pathlib import Path

W, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_batches_world", "shop_world_four"))
parts = F.parts
requested = sys.modules["vocab"].vocab4.requested     # KEEPS: the spellings of keep
CONTRACT, PACK = "spec/adapters/cli.toml", "spec/packs/household.md"
NOTES, SHARED = "spec/vocabulary/notes.md", "spec/vocabulary/shared.md"
MOVED = "### moves\n\n- term `the person → actor the person` from shared to notes"
GROUPS = ("g190", "g191", "g192")


def _module(name):
    """A laying handler module, loaded after this one by the conftest's glob."""
    return next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith("/" + name))


def _model():
    return _module("laying_handlers_model.py")


def group(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    if found is None or Path(found.feature.filename).stem != "batches":
        return None
    return next((t for t in found.tags if t in GROUPS), None)


def _passing():
    R = sys.modules["shop_readiness_world"]
    return R.block("Title of i1", R.PASSING)


def _block(step, tag):
    """The item's `## Requirements`, under colliding ids; g191's contract holding table `o2` of the operation, and
    the domain-model fixture beside the spec of g192."""
    M = _model()
    if tag == "g190":
        pieces = _module("laying_handlers_pieces.py")
        return M.colliding(_passing() + "\n\n### %s pack\n\n%s" % (pieces.PACK, pieces.TERM))
    if tag == "g191":
        contract = step.repo / CONTRACT
        contract.parent.mkdir(parents=True, exist_ok=True)
        contract.write_text('[programs]\nnotes = "notes.py"\n\n%s\n' % M.table("o2"))
        return M.colliding(_passing() + "\n\n### cli adapter\n\n```toml\n%s\n```" % M.table("o1"))
    M._fixture(step)
    return M.colliding(M.NOTEBOOK % MOVED)


def build(step):
    """Before `work batch start`: the group's item i1, `ready`, written over the codified spec."""
    tag = group(step)
    if tag is None:
        return
    sys.modules["shop_readiness_world"].codify(step)
    sys.modules["shop_backlog_world"].write_item(step, "i1", status="ready",
                                                 sections={"Requirements": _block(step, tag)})


T.BEFORE_START.append(build)


# Each Given of these groups that reaches `given` (a Given a handler keyed by its kind takes first, "the item i1 meets
# this readiness bar", never does), by its template, its verb or attribute and the kinds of its things, as
# features/batches.feature says it: `build` writes what they describe, so each is only checked.
_SHARED = {("GivenK", "item", ()), ("GivenK_A", "status", ("item",)), ("GivenK", "capability", ()),
           ("GivenK", "batch", ()), ("GivenDoes", "holds", ("item", "requirement id")),
           ("GivenDoes", "holds", ("capability", "requirement id"))}
GIVENS = {"g190": _SHARED | {("GivenK", "term", ()), ("GivenK", "pack", ()), ("GivenDoes", "has", ("pack", "term")),
                             ("GivenDoes", "holds", ("item", "term"))},
          "g191": _SHARED | {("GivenK", "operation table", ()), ("GivenDoes", "holds", ("item", "operation table"))},
          "g192": _SHARED | {("GivenK", "term", ()), ("GivenK", "element", ()), ("GivenK", "area", ()),
                             ("GivenDoes", "mean", ("term", "element")), ("GivenDoes", "move", ("item", "term")),
                             ("GivenDoes", "holds", ("area", "element"))}}


def given(step):
    """A Given of these groups: what `build` writes before the When; one its group's entry of `GIVENS` does not hold
    refused, naming the step."""
    tag = group(step)
    if tag is None:
        return False
    key = (step.template, step.attribute or step.term, tuple(k for k, _ in parts(step)))
    if key not in GIVENS[tag]:
        raise AssertionError("batches_handlers_renumbered takes no Given %s of %s: %s" % (key, tag, step.text))


def _branch(step, rel):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return T.git(step, "show", "%s:%s" % (branches[0], rel))


def renumbered(step, tag):
    """The item's line laid once on the batch's branch under an id other than `r1`, which the capability keeps."""
    R = sys.modules["shop_readiness_world"]
    capability, line = (("notebook", _model().NOTEBOOK.split("- [r10] ")[1].split("\n")[0]) if tag == "g192"
                        else (R.CAPABILITY, R.PASSING))
    text = _branch(step, "spec/capabilities/%s.md" % capability)
    ids = re.findall(r"(?m)^- \[(r\d+)\] %s$" % re.escape(line), text)
    assert len(ids) == 1 and ids != ["r1"] and re.search(r"(?m)^- \[r1\] ", text), (ids, text)


def _pack(step):
    pieces = _module("laying_handlers_pieces.py")
    text = _branch(step, PACK)
    assert "## Glossary" in text and text.index("## Glossary") < text.index(pieces.TERM), text


def _contract(step):
    M = _model()
    text = _branch(step, CONTRACT)
    assert M.table("o1") in text and text.count('[operations."%s"]' % M.OPERATION) == 1, text


def _area(step):
    target, source = _branch(step, NOTES).split("\n"), _branch(step, SHARED).split("\n")
    person = _model().PERSON
    assert target.count(person) == 1 and person not in source, (target, source)


# Each Then of these groups by its verb and the kinds of its things: what it reads.
THENS = {("keep", "pack"): _pack,
         ("has", ("pack", "term")): _pack,
         ("keep", "adapter contract"): _contract,
         ("holds", ("adapter contract", "operation table")): _contract,
         ("keep", "area"): _area,
         ("holds", ("area", "term")): _area}


def then(step):
    """The Thens of these groups: the item's line renumbered, and the Then's own check (`THENS`); a Then of no entry
    refused."""
    tag = group(step)
    if tag is None or "result" not in step.context:
        return False
    verb = "keep" if step.term in requested.KEEPS else {"have": "has", "hold": "holds"}.get(step.term, step.term)
    kinds = tuple(k for k, _ in parts(step))
    key = (verb, kinds[-1]) if verb == "keep" else (verb, kinds)     # a keep's subject re-keyed to its program
    if step.template != "ThenDoes" or key not in THENS:
        raise AssertionError("batches_handlers_renumbered takes no Then %s %s: %s" % (step.template, key, step.text))
    renumbered(step, tag)
    THENS[key](step)


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)
