"""The batch's specification rebuilt from its base at submit (reviews r17-r20, b874): every in-batch item applied, in
task order, by the specification service (spec_apply's `apply`) to a detached worktree of the commit the batch forks
from, and the paths the apply writes (batch_merge's `OWNED`, and every other path this apply changed) then taken into
the batch's worktree as the rebuild holds them, in one commit citing each item (`rebuild`), none when they are so
already. A parked item is applied nowhere, so its requirements and the design-decisions its retirements would supersede
are not in the batch's workspace (r17, r18), while a decision an in-batch item's retirement leaves unenforced is
superseded once, by the rebuild (r19). The task branches are merged after it keeping those paths, with
what each task changed there after its last apply merged onto them (batch_merge)."""
import backlog_items
import batch_merge
import spec_apply
from batch_git import git, remove_tree, trees_dir
from plumbing.shop_files import Refused


def rebuilt(root, batch, items, command):
    """(the commit of the rebuild, the paths its apply changed): `items` applied in order to a detached worktree of
    the batch's base commit, committed there; the worktree removed, the commit kept by git."""
    tree = trees_dir(root) / ("%s-rebuild" % batch.name)
    remove_tree(root, tree)
    git(root, "worktree", "add", "-q", "--detach", str(tree), batch.forked_from)
    try:
        reply = spec_apply.apply(tree, items, command)
        if reply.outcome != "done":
            raise Refused("%s: the specification service answered %s: %s" % (
                command, reply.outcome, "; ".join(e["reason"] for e in reply.errors)))
        changed = list(dict.fromkeys(reply.content["changed"]))
        git(tree, "add", "-A")
        git(tree, "commit", "-q", "--allow-empty", "-m", "%s: rebuilt" % batch.name)
        return git(tree, "rev-parse", "HEAD").stdout.strip(), changed
    finally:
        remove_tree(root, tree)


def taken(tree, commit, owned):
    """The paths the apply writes in the worktree as `commit` holds them, a file `commit` does not hold taken out."""
    held = set(git(tree, "ls-tree", "-r", "--name-only", commit).stdout.splitlines())
    here = set(git(tree, "ls-files").stdout.splitlines())
    mine = sorted(p for p in held if batch_merge.is_owned(p, owned))
    for k in range(0, len(mine), 200):
        git(tree, "checkout", commit, "--", *mine[k:k + 200])
    gone = sorted(p for p in here - held if batch_merge.is_owned(p, owned))
    if gone:
        git(tree, "rm", "-q", "-f", "--", *gone)


def rebuild(root, tree, batch, items, built, command):
    """The batch's worktree given the specification rebuilt from its base with `items` applied, each id a task branch
    built out of `unbuilt:` (`built`: (branch, its item's ids) of each), committed citing each item when it changed;
    the paths the rebuild's apply changed, which the merges after it keep."""
    commit, changed = rebuilt(root, batch, items, command)
    taken(tree, commit, changed)
    for branch, ids in built:
        batch_merge.built_on(tree, branch, ids)
    if git(tree, "status", "--porcelain").stdout.strip():
        git(tree, "commit", "-q", "-m", "%s: the specification rebuilt from its base with %s\n\n%s" % (
            batch.name, ", ".join(backlog_items.label(i) for i in items),
            "\n".join("Item: %s" % i.name for i in items)))
    return changed
