"""Handlers of features/batches.feature for a parked item (b47): a park takes the item's lines out of `batch-<n>`
(g17), and `work batch done` on another task is not held up by a parked item's failing scenario (g18), nor by another
in-batch item's unbuilt scenario that passes (g19), over the world batches_handlers.py loads; see there."""
import sys

import backlog_items
import backlog_lines
from vocab import handler

W, B, T = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world"))
local = W.local


@handler("GivenR", "proposes")
def item_proposes(step):
    """The requirement is one of the item's lines: the world gives the item its lines when it builds the batch."""
    item, requirement = step.names
    step.context.setdefault("proposed", {})[requirement] = item


@local("ThenDoes", "requirement")
def removes_requirement(step):
    """The run exited 0, and the ids of the item that proposes the requirement are out of the batch branch's spec and
    its `unbuilt:`, where the lines commit laid them."""
    if step.term != "remove":
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    item = step.context["proposed"][step.names[0]]
    found = backlog_items.find(step.repo, B.ident(item))
    ids = [i.split("#")[1] for i in backlog_lines.ids(backlog_lines.read(found, found.name))]
    assert ids, (step.text, "the item has no lines")
    batch = T.batch_name(step, next(iter(step.context["given"]["batch"])))
    spec = T.git(step, "show", "%s:%s" % (batch, T.CAP))
    unbuilt = next(line for line in spec.splitlines() if line.startswith("unbuilt:"))
    for rid in ids:
        assert "[%s]" % rid not in spec and rid not in unbuilt.replace("[", " ").replace(",", " ").split(), (
            step.text, rid, spec)


def scenario_of(step):
    scenario, item = step.names
    step.context.setdefault("scenario_of", {})[scenario] = item


B.OF_GIVENS["scenario"] = scenario_of


@local("GivenK_C", "scenario")
def scenario_not_passing(step):
    """The batch's tests fail while the feature holds the scenario of the item (its group, titled as the item is)."""
    if step.text.split(" is ", 1)[1] != "not passing":
        return False
    step.context["failing"] = step.context["scenario_of"][step.names[0]]


@local("GivenK_C", "scenario")
def scenario_passing(step):
    """The item's unbuilt scenario passes in the batch's tests: a pytest run of the feature with `-p work_items`."""
    if step.text.split(" is ", 1)[1] != "passing":
        return False
    step.context["passing"] = step.context["scenario_of"][step.names[0]]


def passing_tests(step, task):
    """`[batch] tests` that run, in the task's worktree, the passing item's scenario of `features/work-queue.feature`
    under the plugin's pytest plugin, every step bound to a step that passes; the task is the world's own in-batch
    item's, so the passing scenario is another item's."""
    B.write_item(step, T.OWN_IN, title="an item the world builds", status="in-batch")
    T.given(step, "item", T.OWN_IN)
    T.given(step, "task", task).setdefault("item", T.OWN_IN)
    found = step.context["given"]["task"][task]
    tree = step.repo / ".shop" / "worktrees" / ("%s-%s" % (T.batch_name(step, found["batch"]), T.task_id(step, task)))
    title = step.context["item_fields"][step.context["passing"]]["title"]
    test = T.outside(step) / "passing" / "test_passing.py"
    test.parent.mkdir(exist_ok=True)
    test.write_text("from pytest_bdd import given, parsers, scenario, then, when\n\n\n@scenario(%r, %r)\n"
                    "def test_passing():\n    pass\n\n\n@given(parsers.re('.*'))\ndef _given():\n    pass\n\n\n"
                    "@when(parsers.re('.*'))\ndef _when():\n    pass\n\n\n@then(parsers.re('.*'))\ndef _then():\n"
                    "    pass\n" % (str(tree / "features" / "work-queue.feature"), title))
    return "[batch]\ntests = 'python3 -m pytest -q -p work_items -p no:cacheprovider %s'\n" % test


def failing_tests(step):
    """`[batch] tests` that exit 1 while `features/work-queue.feature` holds the failing item's scenario."""
    title = step.context["item_fields"][step.context["failing"]]["title"]
    check = "import pathlib, sys; sys.exit(%r in pathlib.Path('features/work-queue.feature').read_text())" % (
        "Scenario: %s\n" % title)
    return "[batch]\ntests = '''python3 -c \"%s\"'''\n" % check


@handler("WhenRuns", "`work batch done`")
def batch_done(step):
    """`work batch done` on the task, each running task given its worktree on its branch first."""
    if step.context.get("failing"):
        step.context["delivery"] = failing_tests(step)
    if step.context.get("passing"):
        step.context["delivery"] = passing_tests(step, step.names[-1])
    T.prepare(step)
    T.ensure_batch(step)
    task = step.names[-1]
    for name, found in step.context["given"]["task"].items():
        if found["status"] == "running":
            batch = T.batch_name(step, found["batch"])
            tree = step.repo / ".shop" / "worktrees" / ("%s-%s" % (batch, T.task_id(step, name)))
            T.git(step, "worktree", "add", "-q", str(tree), "%s-%s" % (batch, B.ident(found["item"])))
    batch = T.batch_name(step, step.context["given"]["task"][task]["batch"])
    T.run_batch(step, "done", batch, T.task_id(step, task))


@handler("ThenK_A", "task")
def task_is(step):
    status, _ = T.task_row(step, step.names[0])
    wanted = B.bare(step.values[0])
    assert (status != wanted) if " is not " in step.text else (status == wanted), (step.text, status,
                                                                                  step.context["result"].stderr)
