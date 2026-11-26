"""drafting's plugin pack imported and model element and term retired on an item (drafting r73-r78, b672), in a context
with a domain model (tests/scripts/fixtures/domain-model/'s spec, the area notes). Each a `local` handler that takes a
step of those scenarios (`mine`) and returns False on any other: the pack p1 the plugin's `time` (`calendar`, which the
plugin has no pack of, when a Given says it does not exist), the model line m1 notes' `object tag` (`object folder`,
which notes does not declare, when a Given says the domain model does not hold it), the term t1 shared's `the person`
(`shelf`, which no layer holds, when a Given says no area holds it); the item, written at the When, holding a line of
notebook; `work line --import`, `--into notebook --retire-model` or `--retire-term` run on it; and the Thens read the
item back, as committed, or the refusal and what it names."""
import re
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
local = W.local
TAGS = {"r73", "r74", "r75", "r76", "r77", "r78"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
BLOCK = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
         "archives the note, the notes service shall keep the note.")
HELD = {"p1": "time", "m1": "object tag", "t1": "the person"}
ABSENT = {"p1": "calendar", "m1": "object folder", "t1": "shelf"}
KEPT = {"p1": ("### imports", "- pack `time`"), "m1": ("### retirements", "- model line `object tag` in notes"),
        "t1": ("### retirements", "- term `the person → actor the person` in shared")}
FLAGS = {"--import": [], "--retire-model": ["--into", "notebook"], "--retire-term": []}
NAMED = re.compile(r"\b(?:pack|model line|term) ([pmt]\d+)")


def mine(step):
    """True when the step is of drafting's scenarios of r73-r78."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    """{absent: the packs, model lines and terms there are none of}, the fixture's spec copied once."""
    world = step.context.get("retiring")
    if world is None:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        world = step.context["retiring"] = {"absent": set()}
    return world


@local("GivenK")
def given_named(step):
    """a pack p1, a model line m1, a term t1: HELD's unless a Given says there is none."""
    if not mine(step) or step.kind not in ("pack", "model line", "term"):
        return False
    _world(step)
    return None


@local("GivenDoesNot")
@local("GivenDoes")
def given_absent(step):
    """the pack p1 does not exist, this domain model does not hold the model line m1, no area holds the term t1:
    ABSENT's in its place."""
    if not mine(step) or step.term not in ("holds", "hold", "exist", "exists") or not NAMED.search(step.text):
        return False
    _world(step)["absent"].add(NAMED.search(step.text).group(1))
    return None


def _named(world, name):
    return (ABSENT if name in world["absent"] else HELD)[name]


@local("WhenRuns")
def retire(step):
    """`work line <item> --import <p1>`, `--into notebook --retire-model <m1>` or `--retire-term <t1>` (the request
    re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    flag = next((f for f in FLAGS if f in options), None)
    if not mine(step) or flag is None:
        return False
    world = _world(step)
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    name = NAMED.search(step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped", sections={"Requirements": BLOCK})
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    B.run_work(step, "line", B.ident(item), *FLAGS[flag], flag, _named(world, name))
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


@local("ThenDoes")
def kept(step):
    """the drafting service refuses this request: an error exit that is no usage error, the item unchanged; names the
    pack p1 (model line m1, term t1): the output names it; the item i1 imports or holds it, the drafting service keeps
    it or the item: its line in the item's `### imports` or `### retirements` block, committed."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    if step.term == "refuse":
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        assert _item_text(step) == world["before"], _item_text(step)
        return None
    found = NAMED.search(step.text)
    name = found.group(1) if found else next(n for n in KEPT if n not in world["absent"] and _held(step, n))
    if step.term == "name":
        assert _named(world, name) in done.stdout + done.stderr, (done.stdout, done.stderr)
        return None
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    text = _item_text(step) if step.term in ("holds", "hold", "imports", "import") else \
        W.git(step.repo, "show", "HEAD:%s" % rel)
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    head, line = KEPT[name]
    assert head in text.split("\n") and line in text.split("\n"), (step.text, text)
    return None


def _held(step, name):
    return KEPT[name][1] in _item_text(step).split("\n")
