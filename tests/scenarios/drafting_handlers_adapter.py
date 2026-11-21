"""drafting's operation tables and withheld operations in an item (drafting r31-r34, b355), in a context with a
domain model (tests/scripts/fixtures/domain-model/'s spec: the service notes). Each a `local` handler that takes a step
of those scenarios (`mine`) and returns False on any other: an operation an operation of notes (`notes.frobnicate`
when it does not exist), an operation table one of its operation's tables told apart by its parameter's example, the
item written at the When with what it holds as its `### cli adapter` block, `work line --expose` or `--withhold` run,
and the Thens read the item's block and the commit that kept it."""
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
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
TAGS = {"r31", "r32", "r33", "r34"}


def mine(step):
    """True when the step is of drafting's scenarios of r31-r34."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None \
        and bool(TAGS & set(found.tags))


def _world(step):
    """{operations: {name: id}, tables: {name: operation name}, held: [(kind, name)]}, the context's spec once."""
    world = step.context.get("adapter")
    if world is None:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        world = step.context["adapter"] = {"operations": {}, "tables": {}, "held": [], "others": set()}
    return world


def _operation(world, table):
    """The id of the operation a table is of: its operation's, `notes.label` for a table of another operation."""
    if table in world["others"]:
        return "notes.label"
    return world["operations"].get(world["tables"].get(table), "notes.archive")


def text(world, table):
    """The tables of the operation table `table`: its operation's command and a parameter whose example is its name."""
    op = _operation(world, table)
    return ('[operations."%s"]\ncommand = "notes %s"\n[operations."%s".parameters]\nnote = { positional = 1, '
            'example = "%s" }' % (op, op.split(".")[1], op, table))


@local("GivenK")
def given_named(step):
    """an operation o1 (notes.archive), an operation table o1 (of notes.archive until a Given says whose)."""
    if not mine(step) or step.kind not in ("operation", "operation table"):
        return False
    world = _world(step)
    if step.kind == "operation":
        world["operations"][step.names[0]] = "notes.archive"
    else:
        world["tables"].setdefault(step.names[0], None)
    return None


@local("GivenDoesNot")
def given_absent(step):
    """the operation o1 does not exist: `notes.frobnicate`, which the model does not declare; the operation o2 does not
    have the operation table o4: a table of another operation."""
    if not mine(step) or step.term not in ("exist", "has", "have"):
        return False
    world = _world(step)
    if step.term == "exist":
        world["operations"][step.names[0]] = "notes.frobnicate"
    else:
        world["others"].add(step.names[1])
    return None


@local("GivenDoes")
def given_holds(step):
    """the operation o1 has the operation table o2; the item i1 holds the operation table o1 (or the operation o1,
    withheld): written into the item at the When."""
    if not mine(step) or step.term not in ("holds", "has"):
        return False
    world = _world(step)
    if step.term == "has":
        world["tables"][step.names[1]] = step.names[0]
    else:
        kind = "operation table" if "operation table" in step.nps[0] else "operation"
        world["held"].append((kind, step.names[1]))
        step.context["declared"] = step.names[0]
    return None


def _block(world):
    held = world["held"]
    withheld = [world["operations"][n] for k, n in held if k == "operation"]
    tables = [text(world, n) for k, n in held if k == "operation table"]
    return "### cli adapter" + ("\n\nwithheld: [%s]" % ", ".join(withheld) if withheld else "") + \
        ("\n\n```toml\n%s\n```" % "\n\n".join(tables) if tables else "")


@local("WhenRuns")
def run(step):
    """`work line <item> --expose <tables>` or `--withhold <operation>` (the request re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or not options & {"--expose", "--withhold"}:
        return False
    world = _world(step)
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    if world["held"]:
        B.write_item(step, item, status="shaped", sections={"Requirements": _block(world)})
    else:
        B.write_item(step, item, status="shaped")
    if "--expose" in options:
        name = re.search(r"\bthe operation table (o\d+)", step.text).group(1)
        step.context["exposed"] = name
        B.run_work(step, "line", B.ident(item), "--expose", text(world, name))
    else:
        name = re.search(r"\bthe operation (o\d+)", step.text).group(1)
        B.run_work(step, "line", B.ident(item), "--withhold", world["operations"][name])
    return None


def _item_text(step):
    return (step.repo / step.context["items"][step.context["declared"]]).read_text()


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    rel = step.context["items"][step.context["declared"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return W.git(step.repo, "show", "HEAD:%s" % rel)


def _held(world, item, kind, name):
    """Whether the item's text holds the operation table `name` (its tables, of one operation), or the operation
    withheld."""
    if kind == "operation table":
        return text(world, name) in item
    found = re.search(r"(?m)^withheld: \[(.*)\]$", item)
    return bool(found) and world["operations"][name] in [w.strip() for w in found.group(1).split(",")]


@local("ThenDoes")
def kept(step):
    """the item i1 holds the operation table o1 (or the operation o1); the drafting service keeps it: `work` exited 0
    and committed the item holding it; refuses this request: an error exit, the item not changed; names the operation
    table o2: the output names its operation."""
    if not mine(step):
        return False
    world, done = _world(step), step.context["result"]
    if step.term == "refuse":
        assert done.returncode != 0, (done.stdout, done.stderr)
        assert "--expose" not in _item_text(step) and "frobnicate" not in _item_text(step), _item_text(step)
        return None
    if step.term == "name":
        name = re.search(r"\bthe operation table (o\d+)", step.text).group(1)
        assert _operation(world, name) in done.stdout + done.stderr, (done.stdout, done.stderr)
        return None
    kind = "operation table" if "operation table" in step.text else "operation"
    name = re.search(r"\bthe %s (o\d+)" % kind, step.text).group(1)
    item = _done(step) if step.term not in ("holds", "hold") else _item_text(step)
    assert _held(world, item, kind, name), (step.text, item)
    return None


@local("ThenDoesNot")
def not_kept(step):
    """the drafting service does not keep the operation table o4: the item holds none of its tables, and of the
    operation exposed only the new operation table (the one it held before taken out, its withholding too)."""
    if not mine(step) or "operation table" not in step.text:
        return False
    world, item = _world(step), _done(step)
    name = re.search(r"\bthe operation table (o\d+)", step.text).group(1)
    assert not _held(world, item, "operation table", name), (step.text, item)
    op = _operation(world, step.context["exposed"])
    assert item.count('[operations."%s"]' % op) == 1 and _held(world, item, "operation table",
                                                                step.context["exposed"]), item
    assert not re.search(r"(?m)^withheld: .*%s" % re.escape(op), item), item
    return None
