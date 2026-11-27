"""The in-process adapter of the laying service (b611, b758; decision 0125), the one wired in: the lay, prepare,
lift and check of an item in a workspace (a worktree of the batch, or of its task), each answered as laying's Response,
over the specification service's apply (spec_apply, spec_apply_check, b871).

`lay`: spec_apply's `lay` (the item's lines into the workspace's `spec/`, their ids into `unbuilt:`), the bound
check's violations of a clean workspace's committed state kept first (spec_apply_check's `keep`). `prepare`, once the
items of a batch are laid, once for all of them: spec_apply's `prepare`, an unresponsive feature generator refused as
the command's (b749). `lift`: the reverse (`unlay_lines`). `check`: spec_apply_check's `violating`, past the
workspace's committed state before the lay (`before`, b725)."""
import backlog_items
import backlog_lines
import batch_generator
import decision_successor
import laying
import spec_apply
import spec_apply_check
import spec_composition
import spec_unbuilt
from plumbing.shop_files import Refused

violating = spec_apply_check.violating


def lay(item, workspace, command):
    spec_apply_check.keep(workspace)
    return laying.done(lay_item(workspace, item))


def prepare(workspace, _batch, items, command):
    unwritten, superseded = [], []
    changed = prepared(workspace, items, unwritten, command, superseded)
    return laying.done(changed, unwritten=unwritten, superseded=superseded)


def lift(item, workspace, command, base=None):
    return laying.done(unlay_lines(workspace, [item], command, base))


def check(item, workspace):
    found = violating(workspace, [item], spec_apply_check.before(workspace))
    return laying.failed(found[0][1]) if found else laying.done([])


def lay_item(tree, item):
    """The item's lines laid into the worktree's `spec/` and their ids into `unbuilt:`; the paths changed."""
    return spec_apply.lay(tree, item)


def prepared(tree, items, unwritten=None, command="work batch start", superseded=None):
    """The worktree, its `items` laid, made whole for their batch (spec_apply's `prepare`); a generator's refusal,
    an unresponsive one among them, said as `command`'s (b486, b749); the paths changed."""
    try:
        return spec_apply.prepare(tree, items, unwritten, command, superseded)
    except batch_generator.Unresponsive as err:
        raise Refused("%s: features generate failed: %s" % (command, err)) from None


def lay_lines(tree, picked, unwritten=None, command="work batch start", superseded=None):
    """Every picked item laid (`lay_item`) and the worktree prepared for them (`prepared`), as `work batch start`
    leaves its workspace; the paths changed."""
    files = [p for item in picked for p in lay_item(tree, item)]
    return list(dict.fromkeys(prepared(tree, picked, unwritten, command, superseded) + files))


def _generated(tree, capability, command):
    try:
        return spec_apply.generated(tree, capability, command)
    except batch_generator.Unresponsive as err:
        raise Refused("%s: features generate of %s failed: %s" % (command, capability, err)) from None


def unlay_lines(tree, items, command, base=None):
    """Every item's lines taken out of the worktree's `spec/` and their ids out of `unbuilt:`, and the feature of each
    service capability changed written again (plan 4 review, B1), spec/index.md's Composition again, the operation
    tables as the commit `base` (the batch's base, b479) held them, each decision the items' lay superseded accepted
    again and its successor out (b741); the paths changed."""
    changed = []
    for item in items:
        ids = backlog_lines.ids(backlog_lines.read(item, backlog_items.rel_of(item.name)))
        for capability in backlog_lines.unlay(tree, item, changed, base):
            path = backlog_lines.capability_file(tree, capability)
            path.write_text(spec_unbuilt.without_unbuilt(
                path.read_text(), [i.split("#")[1] for i in ids if i.split("#")[0] == capability]))
            changed += _generated(tree, capability, command)
    changed += decision_successor.unlay(tree, items)
    changed += spec_composition.write(tree)
    return list(dict.fromkeys(changed))
