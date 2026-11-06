"""`work batch resume`, `done` and `park` (capability batches r5, r6; workflow simplification plan 4, D10, D12,
D15-D18): one task for each item, built on its branch `batch-<n>-b<j>` in the worktree `batch-<n>-t<k>`.

`resume` gives each pending task of an `in-batch` item its worktree and sets it `running`, and gives a running task
whose worktree is gone its worktree back on its branch, with the commits made so far; it reads no input. `done`
checks the task's worktree and branch and runs the tests there before it sets the task `done`. `park` sets an item
`needs-input` with its question and its task back to `pending`, its branch kept and its worktree removed; a worktree
with uncommitted changes is refused unless `--discard` (plan 4 review, S2). A path is used as a worktree only when it
is that worktree on its branch (`batch_git.is_tree`, S1). Each
change is one commit of the batch file (and the item) on the base branch, made under the lock. The checks shared with
`work batch review` are here: the lines commit, uncited commits, commits that change `.shop/`, the tests."""
import re
import shlex
import subprocess

import backlog_items
import backlog_lines
import backlog_moves
import batch_fix
import batch_parked
import batch_plan
import spec_unbuilt
from batch_git import (
    delivery,
    git,
    is_tree,
    locked,
    remove_tree,
    scripts_env,
    tree_for,
    trees_dir,
    uncommitted,
)
from shop_files import Refused

TESTS = "python3 -m pytest -q -p work_items"
SHOP = (".shop/backlog", ".shop/batches")


def lines_commit(root, batch):
    """The batch branch's first commit after `forked_from`: the commit that laid the lines."""
    found = git(root, "rev-list", "--reverse", "--first-parent", "%s..%s" % (batch.forked_from, batch.branch)).stdout
    if not found.split():
        raise Refused("work batch: %s has no commit after %s" % (batch.branch, batch.forked_from[:7]))
    return found.split()[0]


def uncited(root, since, branch, names):
    """`<short sha> "<subject>"` of each commit on `branch` after `since` with no `Item: <item>` line for one of the
    item names `names` (D10)."""
    out = git(root, "log", "--format=%h%x00%s%x00%(trailers:key=Item,valueonly,separator=%x2c)%x00%B%x1e",
              "%s..%s" % (since, branch)).stdout
    found = []
    for entry in filter(str.strip, out.split("\x1e")):
        sha, subject, cited, body = entry.strip("\n").split("\x00")
        if not set(names) & {c.strip() for c in cited.split(",")}:
            unread = re.search(r"(?m)^Item: ", body) and not cited.strip()
            found.append('%s "%s"%s' % (sha, subject, " (its Item: line is not in the message's last paragraph, "
                                        "and git reads trailers from the last paragraph only)" if unread else ""))
    return found


def under_shop(root, since, branch):
    """The paths under `.shop/backlog/` or `.shop/batches/` a commit on `branch` after `since` changes (D4)."""
    out = git(root, "log", "--format=", "--name-only", "%s..%s" % (since, branch), "--", *SHOP).stdout
    return sorted(set(filter(None, out.splitlines())))


def run_tests(root, tree):
    """`[batch] tests` of `.shop/delivery.toml` (default `python3 -m pytest -q -p work_items`) run in `tree`, the
    plugin's scripts on PYTHONPATH (D12)."""
    command = delivery(root).get("batch", {}).get("tests", TESTS)
    return command, subprocess.run(shlex.split(command), cwd=tree, capture_output=True, text=True, env=scripts_env())


def tests_pass(root, tree, command_name):
    command, done = run_tests(root, tree)
    if done.returncode != 0:
        tail = "\n".join((done.stdout + done.stderr).splitlines()[-20:])
        raise Refused("%s: the tests `%s` failed in %s (exit %d):\n%s" % (command_name, command, tree,
                                                                       done.returncode, tail))


def item_ids(root, item):
    return backlog_lines.ids(backlog_lines.read(item, backlog_items.rel_of(item.name)))


def tree_of(root, batch, task):
    return trees_dir(root) / ("%s-%s" % (batch.name, task.task))


def citable(root, batch, task):
    """The items a commit on the task's branch may cite (plan 4 rulings, Q2): its own, and each `in-batch` item of a
    task before it in plan order, so that a later branch may merge an earlier one's; never a parked item."""
    earlier = batch.tasks[:batch.tasks.index(task)]
    return [task.item] + [t.item for t in earlier if backlog_items.find(root, t.item).status == "in-batch"]


def task_label(root, task):
    return "%s %s" % (task.task, backlog_items.label(backlog_items.find(root, task.item)))


def building(root, name, command):
    """The batch `name`, refused unless it is `building` and `root` is on its base."""
    batch = batch_plan.find(root, name)
    batch_plan.on_base(root, batch)
    if batch.status != "building":
        raise Refused("%s: %s is %s; %s takes a batch that is building" % (command, batch.name, batch.status, command))
    return batch


def resume(root, name):
    """(the batch, [(task, its worktree or None)]) of `work batch resume` (D16)."""
    with locked(root):
        batch = building(root, name, "work batch resume")
        lines, moved, out = None, [], []
        for task in batch.tasks:
            item = backlog_items.find(root, task.item)
            tree = tree_of(root, batch, task)
            if item.status != "in-batch" or task.status not in ("pending", "running"):
                out.append((task, None))
                continue
            if not is_tree(tree, task.branch):
                lines = lines or lines_commit(root, batch)
                tree_for(root, tree, task.branch, "work batch resume", lines)
            if task.status == "pending":
                task.status = "running"
                moved.append(task.task)
            out.append((task, tree))
        if moved:
            batch_plan.commit(root, batch, [], "work batch resume: %s %s running" % (batch.name, ", ".join(moved)))
        batch_fix.trees(root, batch)    # each open finding's worktree, its task left done (plan 5, D14)
        return batch, out


def resume_said(root, batch, out):
    said = ["%s %s: plan %s" % (batch.name, batch.status, batch_plan.rel_of(batch.name))]
    for task, tree in out:
        item = backlog_items.find(root, task.item)
        label = "%s %s" % (task.task, backlog_items.label(item))
        if tree is not None:
            said.append("%s: running in %s on %s: build %s; then work batch done %s %s, or work batch park %s %s "
                        "--question <text>" % (label, tree, task.branch, ", ".join(item_ids(root, item)), batch.name,
                                               task.task, batch.name, item.name))
        elif item.status != "in-batch":
            said.append("%s: parked (%s)" % (label, item.status))
        else:
            said.append("%s: %s" % (label, task.status))
    return "\n".join(said + batch_fix.said(root, batch, batch_fix.trees(root, batch)))


def checked(root, batch, task):
    """The head of the task's branch once its worktree, its commits and its ids are as `done` wants (D10, D12)."""
    command = "work batch done"
    label = task_label(root, task)
    if task.status != "running":
        raise Refused("%s: %s is %s; %s takes a task that is running" % (command, label, task.status, command))
    tree = tree_of(root, batch, task)
    if not is_tree(tree, task.branch):
        raise Refused("%s: %s has no worktree at %s; run work batch resume %s" % (command, label, tree, batch.name))
    loose = uncommitted(tree)
    if loose:
        raise Refused("%s: %s has uncommitted changes in %s: %s" % (command, label, tree, ", ".join(loose)))
    since = lines_commit(root, batch)
    shop = under_shop(root, since, task.branch)
    if shop:
        raise Refused("%s: %s: a commit on %s changes %s, which only the base branch's batch commands change" % (
            command, label, task.branch, ", ".join(shop)))
    bare = uncited(root, since, task.branch, citable(root, batch, task))
    if bare:
        raise Refused("%s: %s: a commit on %s cites no item (an `Item: %s` line): %s" % (
            command, label, task.branch, task.item, "; ".join(bare)))
    left = spec_unbuilt.unbuilt(tree)
    unbuilt = [i for i in item_ids(root, backlog_items.find(root, task.item))
               if i.split("#")[1] in left.get(i.split("#")[0], ())]
    if unbuilt:
        raise Refused("%s: %s: still in unbuilt: %s" % (command, label, ", ".join(unbuilt)))
    head = git(tree, "rev-parse", "HEAD").stdout.strip()
    tests_pass(root, tree, "%s: %s" % (command, label))
    return head


def done(root, name, tid):
    """The task `done` (D16's `done`): checked and tested outside the lock, then, under it, committed if the task is
    still running at the head that was tested."""
    command = "work batch done"
    batch = building(root, name, command)
    head = checked(root, batch, batch_plan.task(batch, tid, command))
    with locked(root):
        batch = building(root, name, command)
        task = batch_plan.task(batch, tid, command)
        tree = tree_of(root, batch, task)
        if task.status != "running" or git(root, "rev-parse", task.branch).stdout.strip() != head or (
                not is_tree(tree, task.branch) or uncommitted(tree)):
            raise Refused("work batch done: %s changed while its tests ran; run it again" % task_label(root, task))
        task.status = "done"
        batch_plan.commit(root, batch, [], "work batch done: %s %s" % (batch.name, task_label(root, task)))
        return task


def refuse_loose(root, batch, tasks, command):
    """Refused while a worktree of `tasks` has uncommitted changes, naming the files and the worktree (S2)."""
    said = []
    for task in tasks:
        tree = tree_of(root, batch, task)
        loose = uncommitted(tree) if is_tree(tree) else []
        if loose:
            said.append("%s: %s has uncommitted changes in %s: %s; commit them on %s with `Item: %s`, or pass "
                        "--discard" % (command, task_label(root, task), tree, ", ".join(loose), task.branch, task.item))
    if said:
        raise Refused("\n".join(said))


def park(root, name, item_name, question, discard=False):
    """`in-batch` -> `needs-input` (D15): the question under `## Question`, a note naming the branch; its task back to
    `pending`, its worktree removed and its branch kept. Refused while the worktree has uncommitted changes, unless
    `discard`."""
    question = backlog_moves.text_line(question, "question")
    with locked(root):
        batch = building(root, name, "work batch park")
        item = backlog_items.find(root, item_name)
        task = next((t for t in batch.tasks if t.item == item.name), None)
        if task is None:
            raise Refused("work batch park: %s is not in %s" % (backlog_items.label(item), batch.name))
        if item.status != "in-batch":
            raise Refused("work batch park: %s is %s; work batch park takes an item that is in-batch" % (
                backlog_items.label(item), item.status))
        if not discard:
            refuse_loose(root, batch, [task], "work batch park")
        item.status = "needs-input"
        item.sections["Question"] = question
        backlog_moves.add_note(item, "parked from %s; its work is on branch %s" % (batch.name, task.branch))
        task.status = "pending"
        remove_tree(root, tree_of(root, batch, task))
        before = batch_parked.take_out(root, batch, [item], "work batch park")     # at once (r17)
        try:
            batch_plan.commit(root, batch, [item], "work batch park: %s %s -> needs-input" % (
                batch.name, backlog_items.label(item)))
        except BaseException:
            batch_parked.put_back(root, batch, before)
            raise
        return item
