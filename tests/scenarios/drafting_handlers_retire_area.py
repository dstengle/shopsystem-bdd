"""drafting's area retired in an item (drafting r114-r118, b898), in a context with a domain model
(tests/scripts/fixtures/domain-model/'s spec). Each a `local` handler that takes a step of those scenarios (`mine`)
and returns False on any other: the area a1 `shelving`, an empty model file of kind port and an empty layer beside the
fixture's notes (none, when a Given says the domain model does not hold it), its model holding the model line m1
`object shelf`, its layer the term t1 `shelf`, a capability c1 `shelves` of the area the requirement r1, each when a
Given says so; the item, written at the When, holding a line of notebook; `work line --retire-area` run on it; and the
Thens read the item back, as committed, or the refusal and what it names."""
import re
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
B = sys.modules["shop_backlog_world"]
local = W.local
TAGS = {"r114", "r115", "r116", "r117", "r118"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
BLOCK = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
         "archives the note, the notes service shall keep the note.")
AREA = "shelving"
NAMES = {"a1": AREA, "m1": "object shelf", "t1": "shelf", "r1": "shelves#r1"}
KEPT = "- area `%s`" % AREA
KINDS = ("area", "model line", "term", "capability", "requirement")
NAMED = re.compile(r"\b(?:area|model line|term|requirement) ([amtr]\d+)")
MODEL = ("---\nid: model/example.org/fixture/shelving\narea: shelving\nkind: port\nimports: []\n---\n\n# Shelving\n\n"
         "## Purpose\n\nThe shelves notes stand on.\n\n```model\n%s```\n")
LAYER = "---\nid: vocabulary/example.org/fixture/shelving\narea: shelving\n---\n\n# The words of shelving\n\n## Terms\n%s"
CAPABILITY = ("---\nid: capability/example.org/fixture/shelves\ntitle: Shelves\nnarrator: the person\ngroup: service\n"
              "area: shelving\nspecifies: service notes\nlanguage: codified-2\nretired: [%s]\nunbuilt: []\n---\n\n"
              "# Shelves\n\n## Purpose\n\nShelves.\n\n## Behaviour\n\n%s")
LINE = "### [g1] A note added is kept\n- [r1] When the person adds a note, the notes service shall keep the note.\n"


def mine(step):
    """True when the step is of drafting's scenarios of r114-r118."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    """{held: what the area holds, absent: whether the domain model does not hold it}, the fixture's spec copied once."""
    world = step.context.get("retiring area")
    if world is None:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        world = step.context["retiring area"] = {"held": set(), "absent": False}
    return world


@local("GivenK")
def given_named(step):
    """an area a1, a model line m1, a term t1, a capability c1, a requirement r1: what the area holds is a Given's."""
    if not mine(step) or step.kind not in KINDS:
        return False
    _world(step)
    return None


@local("GivenDoes")
def given_held(step):
    """the area a1 holds the model line m1 (the term t1, the capability c1), the capability c1 has the requirement r1."""
    if not mine(step) or step.term not in ("holds", "hold", "has", "have"):
        return False
    found = re.search(r"\b(?:model line|term|requirement) ([mtr]\d+)", step.text)
    if found:
        _world(step)["held"].add(found.group(1))
    return None


@local("GivenDoesNot")
def given_absent(step):
    """this domain model does not hold the area a1: no model file and no layer of it."""
    if not mine(step) or step.term not in ("holds", "hold") or "the area a1" not in step.text:
        return False
    _world(step)["absent"] = True
    return None


def _area(step, held):
    spec = step.repo / "spec"
    (spec / "model" / ("%s.md" % AREA)).write_text(MODEL % ("object shelf\n" if "m1" in held else ""))
    (spec / "vocabulary" / ("%s.md" % AREA)).write_text(
        LAYER % ("\n- **shelf** (noun) → object shelf. A board notes stand on. Plural: shelves.\n" if "t1" in held else ""))
    (spec / "capabilities" / "shelves.md").write_text(
        CAPABILITY % (("", LINE) if "r1" in held else ("g1, r1", "")))


@local("WhenRuns")
def retire(step):
    """`work line <item> --retire-area shelving` (the request re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or "--retire-area" not in options:
        return False
    world = _world(step)
    if not world["absent"]:
        _area(step, world["held"])
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped", sections={"Requirements": BLOCK})
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    B.run_work(step, "line", B.ident(item), "--retire-area", AREA)
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


@local("ThenDoes")
def kept(step):
    """the drafting service refuses this request: an error exit that is no usage error, the item unchanged; names the
    area a1 (model line m1, term t1, requirement r1): the output names it; keeps the item i2, the item i2 retires the
    area a1: the run committed the item, its `### retirements` block holding the area's line."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    if step.term == "refuse":
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        assert _item_text(step) == world["before"], _item_text(step)
        return None
    if step.term == "name":
        name = NAMES[NAMED.search(step.text).group(1)]
        assert name in done.stdout + done.stderr, (done.stdout, done.stderr)
        return None
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    text = W.git(step.repo, "show", "HEAD:%s" % rel).split("\n")
    if step.term in ("retire", "retires"):
        assert "### retirements" in text and KEPT in text, (step.text, text)
    return None
