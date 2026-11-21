"""An item's operation tables and withheld operations laid into the adapter contract (batches r79, r80, b355): the
item's `### cli adapter` block written as its Givens say (a table of `notes.archive`, told apart by its parameter's
example, or the operation withheld), a table of the operation the contract holds before the batch (`spec/adapters/
cli.toml` committed in the world's spec), and the Thens read the contract off the batch's branch after `work batch
start`."""
import re
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
OPERATION = "notes.archive"
CONTRACT = "spec/adapters/cli.toml"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's


def table(name):
    """The tables of the operation table `name`: notes.archive's, its parameter's example its name."""
    return ('[operations."%s"]\ncommand = "notes archive"\n[operations."%s".parameters]\nnote = { positional = 1, '
            'example = "%s" }' % (OPERATION, OPERATION, name))


def _world(step):
    return step.context.setdefault("adapter", {"tables": [], "withheld": []})


@four("GivenK", "operation table", *BOTH)
@four("GivenK", "operation", *BOTH)
def given_named(step):
    """an operation o1 (notes.archive), an operation table o1 (one of its tables)."""


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the operation table o1 (or the operation o1, withheld): its `### cli adapter` block."""
    (k1, n1), (k2, n2) = parts(step)
    if k1 != "item" or k2 not in ("operation table", "operation"):
        return False
    world = _world(step)
    world["tables" if k2 == "operation table" else "withheld"].append(n2)
    block = "### cli adapter" + ("\n\nwithheld: [%s]" % OPERATION if world["withheld"] else "")
    block += "\n\n```toml\n%s\n```" % "\n\n".join(table(n) for n in world["tables"]) if world["tables"] else ""
    B.write_item(step, n1, sections={"Requirements": block})
    step.context.setdefault("adapter_item", n1)


@four("GivenDoes", "has", *BOTH)
def has(step):
    """the operation o1 has the operation table o2: the contract holds it before the batch."""
    (k1, _), (k2, n2) = parts(step)
    if (k1, k2) != ("operation", "operation table"):
        return False
    path = step.repo / CONTRACT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('[programs]\nnotes = "notes.py"\n\n%s\n' % table(n2))


def _contract(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branch = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()[0]
    return T.git(step, "show", "%s:%s" % (branch, CONTRACT))


def keeps(step):
    """the batches service keeps the adapter contract a1: spec/adapters/cli.toml on the batch's branch."""
    if parts(step)[1][0] != "adapter contract":
        return False
    _contract(step)


@four("ThenDoes", "holds", *BOTH)
def contract_holds(step):
    """the adapter contract a1 holds the operation table o1: the item's table in it, in place of any of its own."""
    (k1, _), (k2, n2) = parts(step)
    if (k1, k2) != ("adapter contract", "operation table"):
        return False
    text = _contract(step)
    assert table(n2) in text and text.count('[operations."%s"]' % OPERATION) == 1, text


def keeps_not(step):
    """the batches service does not keep the operation table o2: no table of the withheld operation in the contract,
    which lists it under [unexposed]."""
    (k, n) = parts(step)[1]
    if k != "operation table":
        return False
    text = _contract(step)
    assert table(n) not in text and '[operations."%s"' % OPERATION not in text, text
    assert re.search(r'(?ms)^\[unexposed\].*"%s"' % re.escape(OPERATION), text), text


for _verb in KEEPS:       # each key requested.py tries in turn of "keeps" and "does not keep", so no other one passes
    four("ThenDoes", _verb, *BOTH)(keeps)
    four("ThenDoesNot", _verb, *BOTH)(keeps_not)
