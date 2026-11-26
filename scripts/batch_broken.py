"""The task a batch's refused submit is to be fixed by (b696, batches r149).

`work batch review` keeps the ids of the tests its failed whole-suite run named, as batch_rerun keeps a task's, under
the batch's own name (`<git common dir>/shopsystem-bdd/rerun/batch-<n>`), never committed; a passing run forgets
them. While they are kept, they are the scenarios that break in the batch's workspace, and the batch poll gives the
step `fix task` with the task of the item whose change broke them (`task_of`): the first task one of whose item's
scenarios (a scenario of `features/<capability>.feature` on the batch's branch tagged with one of its requirement
ids) a failed id names, else the first whose reached tests (batch_reach) hold a failed id's file, else none: the
poll then says `look at failure` with the failed tests and no task (b703, batches r154).

A fix (b713, batches r161-r163) is a commit on a task's branch newer than the refused submit: `work batch review`
keeps each task branch's head as it submits (`submitted`, beside the failed ids, `rerun/batch-<n>.heads`), and while
the failed ids are kept, a task branch that holds a commit its kept head does not is fixed (`fixed`); the poll then
says `submit batch`, not `fix task` nor `look at failure`, whose run tests the fix."""
import re

import backlog_items
import batch_reach
import batch_rerun
import batch_tasks
from batch_git import git
from plumbing.shop_files import Refused


def failed(root, batch):
    """The ids the batch's last whole-suite run named failed, kept until a run passes."""
    return batch_rerun.kept(root, batch.name)


def _heads_key(batch):
    return "%s.heads" % batch.name


def submitted(root, batch, tasks):
    """Each task's branch head kept as the batch is submitted, so that a later commit on it reads as a fix."""
    heads = []
    for task in tasks:
        try:
            heads.append("%s %s" % (task.branch, git(root, "rev-parse", task.branch).stdout.strip()))
        except Refused:
            continue
    batch_rerun.keep(root, _heads_key(batch), heads)


def fixed(root, batch, tasks):
    """Whether a fix exists: the batch's failed run is kept and a task's branch holds a commit newer than its head
    at that submit."""
    if not failed(root, batch):
        return False
    heads = dict(line.split(" ", 1) for line in batch_rerun.kept(root, _heads_key(batch)) if " " in line)
    for task in tasks:
        head = heads.get(task.branch)
        if not head:
            continue
        try:
            if git(root, "rev-list", "--count", "%s..%s" % (head, task.branch)).stdout.strip() != "0":
                return True
        except Refused:
            continue
    return False


def test_name(title):
    """The test function pytest-bdd makes of a scenario titled `title`."""
    return "test_" + re.sub(r"^\d+_*", "", re.sub(r"\W", "", title.replace(" ", "_"))).lower()


def scenarios(feature, rid):
    """The titles of the scenarios of the feature text `feature` tagged `@<rid>`."""
    found, tags = [], set()
    for line in feature.splitlines():
        text = line.strip()
        if text.startswith("@"):
            tags = set(text.split())
        elif text.startswith(("Scenario:", "Scenario Outline:")):
            if "@" + rid in tags:
                found.append(text.split(":", 1)[1].strip())
            tags = set()
    return found


def _ids(root, task):
    try:
        return batch_tasks.item_ids(root, backlog_items.find(root, task.item))
    except Refused:
        return []


def _scenario_tests(root, batch, ids):
    """(test file, test function) of each scenario of the requirement ids `ids` on the batch's branch."""
    found = set()
    for rid in ids:
        cap, _, number = rid.partition("#")
        try:
            feature = git(root, "show", "%s:features/%s.feature" % (batch.branch, cap)).stdout
        except Refused:
            continue
        test = "tests/scenarios/test_%s.py" % cap.replace("-", "_")
        found |= {(test, test_name(title)) for title in scenarios(feature, number)}
    return found


def _reached(root, batch, task, ids, path):
    """Whether the test file `path` is one the task's change reaches."""
    if path in {"tests/scenarios/test_%s.py" % i.split("#")[0].replace("-", "_") for i in ids}:
        return True
    try:
        since = batch_tasks.lines_commit(root, batch)
        return path not in batch_reach.unreached(git, root, since, task.branch, ids)
    except Refused:
        return False


def task_of(root, batch, tasks):
    """The task of `tasks` to fix for the batch's kept failed run, or None when none is kept or none's item broke it."""
    kept = [(i.partition("::")[0], i.partition("::")[2].split("[")[0]) for i in failed(root, batch)]
    if not kept or not tasks:
        return None
    ids = {t.task: _ids(root, t) for t in tasks}
    for task in tasks:
        if set(kept) & _scenario_tests(root, batch, ids[task.task]):
            return task
    for task in tasks:
        if any(_reached(root, batch, task, ids[task.task], path) for path, _ in kept):
            return task
    return None
