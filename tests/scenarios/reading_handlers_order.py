"""reading's Thens of an order after a collection (r62, b334): read off the logical form `spec parse --form` printed of
the `order-by` example (design_model_check_worlds_order's HELD), the order is a member's: an every box over the Ks the
collection holds, restricted by `in(_, the collection)`, holds the `ordered` atom in its scope, and no `ordered` atom
names the collection (decision 0093: an order is said with its key, an attribute of the members)."""
import importlib.util
import re
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


W = _sibling("work_queue_world.py", "shop_work_queue_world")

CAPABILITIES = ("reading", "parsing")
EVERY = re.compile(r"every \[(x\d+): ([a-z ]+)\]")
ORDERED = re.compile(r"ordered\((x\d+), ([a-z ]+), (ascending|descending)\)")


def ours(step):
    return sys.modules["vocab"].origin(step.request.node) in CAPABILITIES


def _boxes(form):
    """[(member referent, its kind, the collection referent or None, [the ordered atoms of its scope])] of each every
    box of the printed form: its restriction's `in(m, c)` and the `ordered` atoms below its `scope` line."""
    lines, out = form.splitlines(), []
    for i, line in enumerate(lines):
        found = EVERY.search(line)
        if not found:
            continue
        depth, m, coll, scoped, atoms = len(line) - len(line.lstrip()), found.group(1), None, False, []
        for below in lines[i + 1:]:
            if len(below) - len(below.lstrip()) <= depth:
                break
            text = below.strip()
            scoped = scoped or text == "scope"
            held = re.fullmatch(r"in\(%s, (x\d+)\)" % m, text)
            if held and not scoped:
                coll = held.group(1)
            atoms += [a.groups() for a in ORDERED.finditer(text)] if scoped else []
        out.append((m, found.group(2), coll, atoms))
    return out


def _held(step):
    """(member, collection, its ordered atoms) of the every box over a collection's members, else an AssertionError."""
    form = step.context["result"].stdout
    held = [(m, c, atoms) for m, _, c, atoms in _boxes(form) if c is not None]
    assert held, ("no every box over the members of a collection", form)
    return held[0]


@W.local("ThenPrints")
def returned(step):
    """The language service returns the logical form l1 (the CLI adapter's `spec` prints it): a form, read whole."""
    if not ours(step) or not step.nps or not step.nps[0].startswith("the logical form"):
        return False
    done = step.context["result"]
    assert done.returncode == 0 and re.match(r"(\S+: )?shall ", done.stdout.lstrip()), (done.stdout, done.stderr)
    return None


@W.local("ThenDoes")
def then(step):
    """The collection c1 has the member m1; the member m1 has the order o1; the language service returns the logical
    form l1; the logical form l1 uses the order o1."""
    if not ours(step) or step.event not in ("has", "return", "use"):
        return False
    if step.event == "has" and not step.nps[0].startswith(("the member", "the order")):     # another's has (b420)
        return False
    done = step.context["result"]
    names = step.context.setdefault("order_names", {})
    if step.event == "return":
        return returned(step)
    member, collection, atoms = _held(step)
    if step.event == "has" and step.nps[0].startswith("the member"):
        assert re.search(r"(print|give|hand)\(e\d+, subject: x\d+, object: %s\)" % collection, done.stdout), \
            ("the collection is not what the response acts on", done.stdout)
        names.update({step.names[0]: collection, step.names[1]: member})
    elif step.event == "has":
        assert atoms and all(x == member for x, _, _ in atoms), ("the member has no order", done.stdout)
        names[step.names[1]] = atoms[0]
    else:
        orders = [a.groups() for a in ORDERED.finditer(done.stdout)]
        assert orders and all(x != collection for x, _, _ in orders), ("an order names the collection", done.stdout)
        assert names.get(step.names[1]) in orders, (step.text, names, done.stdout)
    return None
