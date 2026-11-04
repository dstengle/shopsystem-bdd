"""Handlers of features/backlog.feature (plan 2): `work`'s backlog commands run on the items backlog_world.py
writes, and what they wrote, committed and printed read back.

A step whose registry key another capability claims (`ThenPrints` with `` `work` ``, `ThenDoes` with `write`,
`WhenRuns` with `` `work show` ``) is taken through work_queue_world's `local` table by its kind, so it reaches these
handlers only in test_backlog.py, which binds with `bind_all`; each returns False for a step that is not about the
backlog, which then goes on to the registry."""
import importlib.util
import sys
from pathlib import Path

import backlog_items
from vocab import handler


def shared(name, file):
    """A world module loaded once by path, the one work_queue_handlers.shared() loads when it is the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
local, bare = W.local, B.bare


@handler("WhenRuns", "`work idea`")
def work_idea(step):
    B.run_work(step, "idea", "A new idea")


@handler("GivenK", "item")
def given_item(step):
    if not B.item_rel(step.context, step.names[0]):
        B.write_item(step, step.names[0])


@handler("GivenK_A", "item")
def given_item_is(step):
    """`an item i1 that is v`, `the item i1 is v`; `the item i1 is not v` keeps the item's value when it is another,
    else takes the first of the attribute's values that is not v."""
    name, value, attribute = step.names[0], bare(step.values[0]), step.attribute
    if " is not " in step.text:
        had = B.fields_of(step, name)
        if had and had[attribute] != value:
            return
        allowed = backlog_items.STATUSES if attribute == "status" else backlog_items.RATINGS[attribute]
        value = next(v for v in allowed if v != value)
    B.write_item(step, name, **{attribute: value})


@handler("ThenK_A", "item")
def item_is(step):
    got = W.field(B.item_file(step, step.names[0]), step.attribute)
    wanted = bare(step.values[0])
    assert (got != wanted) if " is not " in step.text else (got == wanted), (step.text, got)


@local("WhenRuns", "item")
def run_on_item(step):
    if step.term not in ("`work show`",):
        return False
    B.run_work(step, bare(step.term).split()[1], B.ident(step.names[0]))


@local("ThenDoes", "item")
def does_to_item(step):
    rel = B.bind_written(step, step.names[0]) if step.term == "write" else B.item_rel(step.context, step.names[0])
    if step.term == "commit":
        B.in_commits(step, rel)
    elif step.term != "write":
        return False


@local("ThenPrints", "title")
def prints_title(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    hits = [n for n in step.context.get("items", {}) if B.title_of(step, n) in done.stdout]
    assert hits, (step.text, done.stdout)
    step.context.setdefault("titles", {})[step.names[0]] = hits


@local("ThenR", "title")
def title_of(step):
    title, item = step.names
    assert item in step.context.get("titles", {}).get(title, ()), (step.text, step.context.get("titles"))
    assert B.title_of(step, item) in step.context["result"].stdout


@local("ThenExitsErr", "item")
def item_refused(step):
    """The run exited non-zero, naming the label of each item the step names, and for `the status of the item i<n>`
    that item's status as it was before the run."""
    done = step.context["result"]
    assert done.returncode != 0, done.stdout
    said = done.stdout + done.stderr
    for name in step.names:
        assert '%s "%s"' % (B.ident(name), B.title_of(step, name)) in said, (step.text, said)
        if any(np.startswith("the status of the item %s" % name) for np in step.nps):
            status = step.context["item_fields"][name]["status"]
            assert status in said, (step.text, status, said)
