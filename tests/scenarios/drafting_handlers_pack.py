"""drafting's term written into a pack for an item (drafting r51, r52, b472), in a context with a domain model
(tests/scripts/fixtures/domain-model/'s spec). Each a `local` handler that takes a step of those scenarios (`mine`) and
returns False on any other: the pack p1 the context's own `household`, which `spec/packs/household.md` holds with the
term t1 when a Given says it has it; the item, written at the When, `shaped` with no requirement lines; `work line
<item> --pack household --term <t1>` run on it; and the Thens read the item back, as committed, or the refusal, the
item unchanged, and what it names."""
import re
import shutil
import sys
from pathlib import Path

W, B = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world"))
local = W.local
TAGS = {"r51", "r52"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
PACK, WORD = "household", "pantry"
T1 = "- **pantry** (noun): a cupboard food is kept in."
HELD = "# household\n\nThe household's own words.\n\n## Glossary\n\n- **pantry** (noun): a room food is kept in.\n"


def mine(step):
    """True when the step is of drafting's scenarios of r51 and r52."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    """{}, the fixture's spec copied once."""
    world = step.context.get("packed")
    if world is None:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        world = step.context["packed"] = {}
    return world


@local("GivenK")
def given_named(step):
    """a term t1, a pack p1: the texts above; an item: the backlog's."""
    if not mine(step) or step.kind not in ("term", "pack"):
        return False
    _world(step)
    return None


@local("GivenDoes")
def given_has(step):
    """the pack p1 has the term t1: spec/packs/household.md holds an entry of its word."""
    if not mine(step) or step.term not in ("has", "have"):
        return False
    _world(step)
    path = step.repo / "spec" / "packs" / ("%s.md" % PACK)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HELD)
    return None


@local("WhenRuns")
def write(step):
    """`work line <item> --pack household --term <t1>` (the request re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or "--pack" not in options:
        return False
    world = _world(step)
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped")
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    B.run_work(step, "line", B.ident(item), "--pack", PACK, "--term", T1)
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


@local("ThenDoes")
def kept(step):
    """the drafting service refuses this request: an error exit that is no usage error, the item unchanged; names the
    term t1: the output names its word; the item i1 holds the term t1, the drafting service keeps it: committed under
    the item's `### household pack` block."""
    if not mine(step):
        return False
    done, world = step.context["result"], _world(step)
    if step.term == "refuse":
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        assert _item_text(step) == world["before"], _item_text(step)
        return None
    if step.term == "name":
        assert WORD in done.stdout + done.stderr, (done.stdout, done.stderr)
        return None
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    text = W.git(step.repo, "show", "HEAD:%s" % rel)
    assert "### %s pack\n\n%s" % (PACK, T1) in text, text
    return None
