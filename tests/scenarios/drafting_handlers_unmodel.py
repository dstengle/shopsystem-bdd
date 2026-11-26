"""drafting's model lines and terms taken back out of an item or reworded (drafting r43-r48, r50, b367; r95, b800;
r105, b829: a reworded term returned), in a context with a domain model (tests/scripts/fixtures/domain-model/'s spec, the area notes). Each a `local` handler that takes a step
of those scenarios (`mine`) and returns False on any other: the item, written at the When, holds a `### notes model`
block of two elements (`object folder`, the model line m1, and `object shelf`) and their two entries (folder's the
term t1), unless a Given says it does not hold m1 or t1; `work line --remove-model`, `--reword-model`,
`--remove-term` or `--reword-term` run on it; and the Thens read the item back, as committed, or the refusal and
what it names."""
import importlib.util
import re
import shutil
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
TAGS = {"r43", "r44", "r45", "r46", "r47", "r48", "r105", "r50", "r95"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
M1, OTHER = "object folder\n  attributes: name (text)", "object shelf\n  attributes: label (text)"
M2 = "object folder\n  attributes: title (text)"
T1 = "- **folder** (noun) → object folder. A place notes are kept in."
OTHER_TERM = "- **shelf** (noun) → object shelf. A place folders stand on."
T2 = "- **folder** (noun) → object folder. A box notes are kept in."
TEXTS = {"m1": M1, "m2": M2, "t1": T1, "t2": T2}
OPTIONS = ("--remove-model", "--reword-model", "--remove-term", "--reword-term")


def mine(step):
    """True when the step is of drafting's scenarios of r43-r50 (r49 reworded as r105) and r95."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    """{absent: the model line or term the item does not hold}, the fixture's spec copied once."""
    world = step.context.get("unmodel")
    if world is None:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        world = step.context["unmodel"] = {"absent": set()}
    return world


def _block(world):
    lines = [x for x in (M1, OTHER) if not ("m1" in world["absent"] and x == M1)]
    terms = [x for x in (T1, OTHER_TERM) if not ("t1" in world["absent"] and x == T1)]
    return "### notes model\n\n```model\n%s\n```\n\n%s" % ("\n\n".join(lines), "\n".join(terms))


@local("GivenK")
def given_named(step):
    """a model line m1, m2; a term t1, t2: the texts above; an item: the backlog's."""
    if not mine(step) or step.kind not in ("model line", "term"):
        return False
    _world(step)
    return None


@local("GivenDoesNot")
def given_absent(step):
    """the item i1 does not hold the model line m1 (the term t1): its block written without it."""
    if not mine(step) or step.term not in ("holds", "hold"):
        return False
    _world(step)["absent"].add(step.names[1])
    return None


@local("WhenRuns")
def change(step):
    """`work line <item> --remove-model <m1>`, `--reword-model <m1's header> <m2>`, `--remove-term folder` or
    `--reword-term folder <t2>` (an entry opening with "- ", no `--` before it, b800), with `--into notebook` when the
    request names the capability (the request re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    flag = next((f for f in OPTIONS if f in options), None)
    if not mine(step) or flag is None:
        return False
    world = _world(step)
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped", sections={"Requirements": _block(world)})
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    args = {"--remove-model": [M1.split("\n")[0]], "--reword-model": [M1.split("\n")[0], M2],
            "--remove-term": ["folder"], "--reword-term": ["folder", T2]}[flag]
    into = ["--into", "notebook"] if "--into" in options else []
    B.run_work(step, "line", B.ident(item), flag, *args, *into)
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return W.git(step.repo, "show", "HEAD:%s" % rel)


def _held(text, name):
    """Whether the item's text holds the model line or term `name`: its whole text, the other element and entry
    kept beside it."""
    assert OTHER in text and OTHER_TERM in text, text
    return TEXTS[name] in text


@local("ThenDoes")
def kept(step):
    """the drafting service refuses this request: an error exit that is no usage error, the item unchanged; names the model line m1 (the
    term t1): the output names its header (its word); the item i1 holds m2 (t2), the drafting service keeps it:
    committed, the old text gone."""
    if not mine(step):
        return False
    if step.term == "write":        # returns, re-keyed (requested's `trying`)
        return returns(step)
    done, world = step.context["result"], _world(step)
    if step.term == "refuse":
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        assert _item_text(step) == world["before"], _item_text(step)
        return None
    name = re.search(r"\b(?:model line|term) ([mt]\d+)", step.text).group(1)
    if step.term == "name":
        said = M1.split("\n")[0] if name == "m1" else "folder"
        assert said in done.stdout + done.stderr, (done.stdout, done.stderr)
        return None
    text = _done(step) if step.term not in ("holds", "hold") else _item_text(step)
    old = {"m2": "m1", "t2": "t1"}[name]
    assert _held(text, name) and (name == "m2" or not _held(text, old)), (step.text, text)
    assert name != "m2" or text.count("object folder\n") == 1, text
    return None


@local("ThenPrints")
def returns(step):
    """the drafting service returns the term t2 (r105): its entry printed whole, the run completed."""
    if not mine(step):
        return False
    done = step.context["result"]
    name = re.search(r"\bterm (t\d+)", step.text).group(1)
    assert done.returncode == 0 and TEXTS[name] in done.stdout, (done.stdout, done.stderr)
    return None


@local("ThenDoesNot")
def not_kept(step):
    """the item i1 does not hold the model line m1 (the term t1); the drafting service does not keep it: committed
    without it, the other element and entry kept."""
    if not mine(step):
        return False
    name = re.search(r"\b(?:model line|term) ([mt]\d+)", step.text).group(1)
    text = _done(step) if step.term not in ("holds", "hold") else _item_text(step)
    assert not _held(text, name), (step.text, text)
    assert name != "m1" or "object folder\n" not in text, text
    return None
