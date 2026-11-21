"""items' merge into a successor (r43-r45, b484): a successor, the item another item is merged into, written as an
item of the backlog under its own number (backlog_world's `ident`: `s1` is `b81`), its status as a Given says, and
what a refusal names it by, its label."""
import sys

F = sys.modules["shop_world_four"]
four, parts = F.four, F.parts
B = sys.modules["shop_backlog_world"]

BOTH = ("backlog", "batches")


@four("GivenK", "successor", *BOTH)
def given_successor(step):
    if not B.item_rel(step.context, step.names[0]):
        B.write_item(step, step.names[0])


@four("GivenDoes", "exist", *BOTH)
def successor_exists(step):
    k, _ = parts(step)[0]
    if k != "successor":
        return False
    given_successor(step)


@four("GivenK_A", "successor", *BOTH)
def successor_is(step):
    """The status of the successor s1 is `delivered`: its file says so."""
    B.write_item(step, step.names[0], **{step.attribute: B.bare(step.values[0])})


@four("ThenDoes", "name", *BOTH)
def names_successor(step):
    """`work` names the successor s1: its label, `b81 "Title of s1"`."""
    k, name = parts(step)[1]
    if k != "successor":
        return False
    done = step.context["result"]
    assert step.context["says"][name] in done.stdout + done.stderr, (step.text, done.stdout, done.stderr)
