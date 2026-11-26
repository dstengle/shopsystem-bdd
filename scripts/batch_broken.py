"""The task a batch's refused submit is to be fixed by (b696, batches r149).

`work batch review` keeps the ids of the tests its failed whole-suite run named, as batch_rerun keeps a task's, under
the batch's own name (`<git common dir>/shopsystem-bdd/rerun/batch-<n>`), never committed; a passing run forgets
them. While they are kept, they are the scenarios that break in the batch's workspace, and the batch poll gives the
step `fix task` with the task of the item whose change broke them (`task_of`): the first task one of whose item's
scenarios (a scenario of `features/<capability>.feature` on the batch's branch tagged with one of its requirement
ids) a failed id names, else the first whose reached tests (batch_reach) hold a failed id's file, else the first
task."""
import re

import backlog_items
import batch_reach
import batch_rerun
import batch_tasks
from batch_git import git
from shop_files import Refused


def failed(root, batch):
    """The ids the batch's last whole-suite run named failed, kept until a run passes."""
    return batch_rerun.kept(root, batch.name)


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
    """The task of `tasks` to fix for the batch's kept failed run, or None when none is kept."""
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
    return tasks[0]
