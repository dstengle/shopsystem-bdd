"""drafting's retirement and import taken back out of an item (drafting r79-r84, b688), in a context with a domain model
(tests/scripts/fixtures/domain-model/'s spec). Each a `local` handler that takes a step of those scenarios (`mine`)
and returns False on any other: the item, written at the When, holding a line of notebook, the import of the pack p1
(the plugin's `time`), the retirement of the model line m1 (notes' `object tag`) and of the term t1 (shared's `the
person`), each but the one a Given says it does not hold; `work line --reinstate-model`, `--reinstate-term` or
`--remove-import` run on it; and the Thens read the item back, as committed, or the refusal and what it names."""
import re
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
four = sys.modules["shop_world_four"].four
local = W.local
TAGS = {"r79", "r80", "r81", "r82", "r83", "r84"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
BLOCK = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
         "archives the note, the notes service shall keep the note.")
NAMES = {"p1": "time", "m1": "object tag", "t1": "the person"}
LINES = {"p1": "- pack `time`", "m1": "- model line `object tag` in notes",
         "t1": "- term `the person → actor the person` in shared"}
FLAGS = {"--reinstate-model": "m1", "--reinstate-term": "t1", "--remove-import": "p1"}
NAMED = re.compile(r"\b(?:pack|model line|term) ([pmt]\d+)")


def mine(step):
    """True when the step is of drafting's scenarios of r79-r84."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    """{absent: the import and retirements the item does not hold}, the fixture's spec copied once."""
    world = step.context.get("reinstating")
    if world is None:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        world = step.context["reinstating"] = {"absent": set()}
    return world


@local("GivenK")
def given_named(step):
    """a pack p1, a model line m1, a term t1: the item holds its import or retirement unless a Given says not."""
    if not mine(step) or step.kind not in ("pack", "model line", "term"):
        return False
    _world(step)
    return None


@local("GivenDoesNot")
def given_absent(step):
    """the item i1 does not retire the model line m1 (the term t1), does not import the pack p1."""
    if not mine(step) or step.term not in ("retire", "retires", "import", "imports") or not NAMED.search(step.text):
        return False
    _world(step)["absent"].add(NAMED.search(step.text).group(1))
    return None


def _requirements(absent):
    imports = [LINES["p1"]] if "p1" not in absent else []
    retired = [LINES[n] for n in ("m1", "t1") if n not in absent]
    text = BLOCK
    if imports:
        text += "\n\n### imports\n\n" + "\n".join(imports)
    if retired:
        text += "\n\n### retirements\n\n" + "\n".join(retired)
    return text


@local("WhenRuns")
def reinstate(step):
    """`work line <item> --reinstate-model <m1>`, `--reinstate-term <t1>` or `--remove-import <p1>` (the request
    re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    flag = next((f for f in FLAGS if f in options), None)
    if not mine(step) or flag is None:
        return False
    world = _world(step)
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped", sections={"Requirements": _requirements(world["absent"])})
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    B.run_work(step, "line", B.ident(item), flag, NAMES[FLAGS[flag]])
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


def _committed(step):
    """The item as committed by the run, which exited 0 and left it clean."""
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return W.git(step.repo, "show", "HEAD:%s" % rel)


@local("ThenDoes")
def done(step):
    """the drafting service refuses this request: an error exit that is no usage error, the item unchanged; names the
    pack p1 (model line m1, term t1): the output names it; keeps the item: the run committed it, the import and
    retirements it did not take out still in it."""
    if not mine(step):
        return False
    result, world = step.context["result"], _world(step)
    if step.term == "refuse":
        assert result.returncode != 0 and "usage:" not in result.stderr, (result.stdout, result.stderr)
        assert _item_text(step) == world["before"], _item_text(step)
        return None
    if step.term == "name":
        name = NAMES[NAMED.search(step.text).group(1)]
        assert name in result.stdout + result.stderr, (result.stdout, result.stderr)
        return None
    text = _committed(step).split("\n")
    assert BLOCK.split("\n")[-1] in text, text
    return None


def not_held(step):
    """the item i2 does not retire the model line m1 (the term t1), does not import the pack p1: its line out of the
    item as committed, the others kept."""
    if not mine(step) or not NAMED.search(step.text):
        return False
    name = NAMED.search(step.text).group(1)
    text = _committed(step).split("\n")
    assert LINES[name] not in text, (step.text, text)
    assert all(LINES[n] in text for n in LINES if n != name), (step.text, text)
    return None


for _verb in ("retire", "retires", "import", "imports"):     # a chain of the key, which `features vocab` finds
    four("ThenDoesNot", _verb, "drafting")(not_held)
