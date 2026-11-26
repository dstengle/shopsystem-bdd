"""An operation an item's model line adds, with no operation table on the item (batches r92, b489): over
batches_handlers_restate's world (the domain-model fixture's model, vocabulary and notebook), the fixture's adapter
contract too, the item's `### notes model` block adding notes' `pin`, and the Thens read `spec/adapters/cli.toml` off
the batch's branch after `work batch start`: the table written from the model's operation."""
import shutil
import sys
from pathlib import Path

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
CONTRACT = "spec/adapters/cli.toml"
OPERATION = "notes.pin"
BLOCK = ("### notebook\n\n#### [g10] An active note pinned is kept\n- [r10] While a note is `active`, when the person "
         "pins the note, the notes service shall keep the note.\n\n### notes model\n\n```model\nservice notes\n"
         "  operation pin(note)  outcomes: done\n```\n\n- **pin** (verb, action) \u2192 operation notes.pin. Forms: "
         "pins, pinned. Frame: <actor> pins <note>.")


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the model line m1: noted, the item written by batches_handlers_restate (and again below)."""
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) == ("item", "model line"):
        step.context["model_item"] = n1
    return False


@four("GivenDoes", "specifies", *BOTH)
@four("GivenDoes", "specify", *BOTH)
def specifies(step):
    """the model line m1 specifies the operation o1: the item's model block adds notes' `pin`, beside the fixture's
    adapter contract, which holds no table of it."""
    if [k for k, _ in parts(step)] != ["model line", "operation"]:
        return False
    shutil.copytree(FIXTURE / "adapters", step.repo / "spec" / "adapters", dirs_exist_ok=True)
    B.write_item(step, step.context["model_item"], sections={"Requirements": BLOCK})
    step.context["specified"] = True


def _contract(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return T.git(step, "show", "%s:%s" % (branches[0], CONTRACT))


@four("ThenDoes", "has", *BOTH)
@four("ThenDoes", "holds", *BOTH)
def has_table(step):
    """the operation o1 has the operation table o2, the adapter contract a1 holds it: one table of notes.pin in the
    batch's contract, its command after the operation and its parameter an option."""
    kinds = [k for k, _ in parts(step)]
    if not step.context.get("specified") or kinds not in (["operation", "operation table"],
                                                           ["adapter contract", "operation table"]):
        return False
    text = _contract(step)
    assert text.count('[operations."%s"]' % OPERATION) == 1, text
    assert 'command = "notes pin"' in text and '[operations."%s".parameters]' % OPERATION in text, text


@four("GivenDoesNot", "holds", *BOTH)
@four("GivenDoesNot", "hold", *BOTH)
@four("GivenDoesNot", "has", *BOTH)
@four("GivenDoes", "has", *BOTH)
@four("GivenDoes", "holds", *BOTH)
def lacks(step):
    """this domain model does not hold the operation o1, the operation o1 has no operation table, the item i1 holds no
    operation table of the operation o1 (b716): the fixture's model and contract hold no `pin`, nor does the item."""
    kinds = [k for k, _ in parts(step)]
    if kinds[0] == "item" and " holds no operation table of " in step.text and step.context.get("specified"):
        return None
    if kinds not in (["model", "operation"], ["domain model", "operation"], ["operation", "operation table"]) \
            or not step.context.get("specified"):
        return False
    if kinds[0] == "operation" and step.template == "GivenDoes" and "has no" not in step.text:
        return False
