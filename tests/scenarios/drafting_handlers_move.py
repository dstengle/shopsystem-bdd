"""drafting's model element and term moved to another area on an item (drafting r66-r69, b607), in a context with a
domain model (tests/scripts/fixtures/domain-model/'s spec, the area notes). Each a `local` handler that takes a step
of those scenarios (`mine`) and returns False on any other: the model line m1 notes' `object tag` (`object folder`,
which no area declares, when a Given says the domain model does not hold it), the term t1 shared's `the person`
(`shelf`, which no layer holds, when a Given says no area holds it); the item, written at the When, holding a new
capability `labelling` whose area the moved element goes to; `work line --into labelling --move-model` or
`--move-term` run on it; and the Thens read the item back, as committed, or the refusal and what it names."""
import re
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
local = W.local
TAGS = {"r66", "r67", "r68", "r69"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
BLOCK = "### labelling\n\nnarrator: a person keeping notes\ngroup: service\npurpose: The tags a note carries."
HELD = {"m1": "object tag", "t1": "the person"}
ABSENT = {"m1": "object folder", "t1": "shelf"}
KEPT = {"m1": "- model line `object tag` from notes to labelling", "t1": "- term `the person → actor the person` "
        "from shared to notes"}


def mine(step):
    """True when the step is of drafting's scenarios of r66-r69."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    """{absent: the model lines and terms no area holds}, the fixture's spec copied once."""
    world = step.context.get("moving")
    if world is None:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        world = step.context["moving"] = {"absent": set()}
    return world


@local("GivenK")
def given_named(step):
    """a model line m1, a term t1: the fixture's (HELD) unless a Given says no area holds it."""
    if not mine(step) or step.kind not in ("model line", "term"):
        return False
    _world(step)
    return None


@local("GivenDoesNot")
@local("GivenDoes")
def given_absent(step):
    """this domain model does not hold the model line m1, no area holds the term t1: ABSENT's in its place."""
    if not mine(step) or step.term not in ("holds", "hold"):
        return False
    _world(step)["absent"].add(re.search(r"\b(?:model line|term) ([mt]\d+)", step.text).group(1))
    return None


def _named(world, name):
    return (ABSENT if name in world["absent"] else HELD)[name]


@local("WhenRuns")
def move(step):
    """`work line <item> --into labelling --move-model <m1>` or `--move-term <t1>` (the request re-keyed by the CLI
    contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    flag = next((f for f in ("--move-model", "--move-term") if f in options), None)
    if not mine(step) or flag is None:
        return False
    world = _world(step)
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    name = re.search(r"\b(?:model line|term) ([mt]\d+)", step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped", sections={"Requirements": BLOCK})
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    into = ["--into", "labelling"] if flag == "--move-model" else []
    B.run_work(step, "line", B.ident(item), *into, flag, _named(world, name))
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


@local("ThenDoes")
def kept(step):
    """the drafting service refuses this request: an error exit that is no usage error, the item unchanged; names the
    model line m1 (the term t1): the output names it; the item i1 holds it, the drafting service keeps it: its move
    in the item's `### moves` block, committed."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    if step.term == "refuse":
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        assert _item_text(step) == world["before"], _item_text(step)
        return None
    name = re.search(r"\b(?:model line|term) ([mt]\d+)", step.text).group(1)
    if step.term == "name":
        assert _named(world, name) in done.stdout + done.stderr, (done.stdout, done.stderr)
        return None
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    text = _item_text(step) if step.term in ("holds", "hold") else W.git(step.repo, "show", "HEAD:%s" % rel)
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    assert "### moves" in text and KEPT[name] in text.split("\n"), (step.text, text)
    return None
