"""Handlers of features/backlog.feature (plan 2): `work`'s backlog commands run on the items backlog_world.py
writes, and what they wrote, committed and printed read back.

A step whose registry key another capability claims (`ThenPrints` with `` `work` ``, `ThenDoes` with `write`,
`WhenRuns` with `` `work show` ``) is taken through work_queue_world's `local` table by its kind, so it reaches these
handlers only in test_backlog.py, which binds with `bind_all`; each returns False for a step that is not about the
backlog, which then goes on to the registry."""
import importlib.util
import shlex
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
    """The item's attribute is (is not) the value. A negated Then says what a command did not do, so the command must
    exist: a usage error (argparse's exit 2) would make it hold whatever the command is. Its exit code is left to the
    line that builds it (plan 2 rulings, Q2)."""
    got = W.field(B.item_file(step, step.names[0]), step.attribute)
    wanted = bare(step.values[0])
    done = step.context.get("result")
    if " is not " in step.text and done is not None:
        assert done.returncode != 2, (step.text, "the command is not there", done.stderr)
    assert (got != wanted) if " is not " in step.text else (got == wanted), (step.text, got)


@handler("WhenRuns", "`work shape`")
@handler("WhenRuns", "`work refuse`")
def work_move(step):
    B.run_work(step, bare(step.term).split()[1], B.ident(step.names[0]), *TEXT.get(step.term, ()))


# The text a command on an item takes, where it takes one.
TEXT = {"`work refuse`": ("out of scope",), "`work answer`": ("the first reading",)}


@local("WhenRuns", "item")
def run_on_item(step):
    """`work show`, `work withdraw` and `work answer` on an item; on any other kind they are the work-queue's."""
    if step.term not in ("`work show`", "`work withdraw`", "`work answer`"):
        return False
    B.run_work(step, bare(step.term).split()[1], B.ident(step.names[0]), *TEXT.get(step.term, ()))


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
    stdout = step.context["result"].stdout
    assert B.title_of(step, item) in stdout
    line = B.row(stdout, item)
    assert line is None or B.title_of(step, item) in B.cells(line), (step.text, line)   # a table: in the item's row


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


@handler("WhenRuns", "`work rate`")
def work_rate(step):
    flags = [w for flag in step.context.get("flags", []) for w in shlex.split(flag)]
    B.run_work(step, "rate", B.ident(step.names[0]), *flags)


@handler("WhenRuns", "`work depend`")
def work_depend(step):
    B.write_item(step, B.OWN, title=B.OWN_TITLE)
    B.run_work(step, "depend", B.ident(step.names[0]), "--on", B.ident(B.OWN))


@local("ThenDoes", "dependency")
def writes_dependency(step):
    """The last run changed the file of an item whose depends_on gained an entry; the dependency is (that item,
    the entry)."""
    if step.term != "write":
        return False
    gained = []
    for rel in filter(B.is_item_file, B.changed(step)):
        name = B.name_of(step.context, rel)
        had = step.context.get("item_fields", {}).get(name, {}).get("depends_on", [])
        gained += [(name, d) for d in B.depends_on(step.repo / rel) if d not in had]
    assert gained, (step.text, B.changed(step))
    step.context.setdefault("deps", {})[step.names[0]] = {"of": gained[0][0], "on": gained[0][1]}


@local("ThenR", "dependency")
def dependency_of(step):
    dep, item = step.names
    if step.term != "of":
        return False
    assert step.context["deps"][dep]["of"] == item, (step.text, step.context["deps"])


@handler("WhenRuns", "`work backlog`")
def work_backlog(step):
    B.run_work(step, "backlog", *step.context.get("flags", []))


@handler("GivenK", "dependency")
def given_dependency(step):
    step.context.setdefault("deps", {}).setdefault(step.names[0], {})


def dependency_given(step, half):
    dep, item = step.names
    found = step.context.setdefault("deps", {}).setdefault(dep, {})
    found[half] = item
    B.add_dependency(step, found)


B.OF_GIVENS["dependency"] = lambda step: dependency_given(step, "of")


@handler("GivenR", "of")
def given_of(step):
    assert step.kind in B.OF_GIVENS, "no Given of a %s of another: %s" % (step.kind, step.text)
    B.OF_GIVENS[step.kind](step)


@local("GivenR", "dependency")
def given_dependency_on(step):
    if step.term != "on":
        return False
    dependency_given(step, "on")


@handler("GivenK_C", "item")
def given_blocked(step):
    word = step.text.split(" is ", 1)[1]
    assert word in ("blocked", "not blocked"), step.text
    step.context.setdefault("blocked", {})[step.names[0]] = word == "blocked"


def result_ok(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    return done.stdout


def row_of(step, name):
    line = B.row(result_ok(step), name)
    assert line is not None, (step.text, step.context["result"].stdout)
    return line


@local("ThenPrints", "item")
def prints_item(step):
    """`the item i1`: its row; `the status of the item i1`: its row under the table of its status; any other
    attribute: the item file's value is a cell of its row."""
    name = step.names[0]
    line, np = row_of(step, name), step.nps[0]
    attribute = np[4:].split(" of the item ")[0] if " of the item " in np else None
    if attribute is None:
        return
    wanted = W.field(B.item_file(step, name), attribute)
    if attribute == "status":
        assert B.heading_of(step.context["result"].stdout, line) == wanted, (step.text, line)
    else:
        assert wanted in B.cells(line), (step.text, wanted, line)


@local("ThenPrints", "dependency")
def prints_dependency(step):
    dep = step.context["deps"][step.names[0]]
    line = row_of(step, dep["of"])
    assert "blocked by %s" % B.ident(dep["on"]) in line, (step.text, line)


def about_items(step):
    """Whether the scenario keeps items: a step of another feature's kind (a question on a work-item) is not ours."""
    return bool(step.context.get("items"))


@local("ThenPrints", "question")
def prints_question(step):
    if not about_items(step):
        return False
    stdout = result_ok(step)
    hits = [n for n, f in step.context.get("item_fields", {}).items()
            if f["status"] == "needs-input" and B.QUESTION in stdout]
    assert hits, (step.text, stdout)
    step.context.setdefault("questions", {})[step.names[0]] = hits


@local("ThenR", "question")
def question_on(step):
    question, item = step.names
    if step.term != "on" or not B.item_rel(step.context, item):
        return False
    assert item in step.context.get("questions", {}).get(question, ()), step.text
    assert "question: %s" % B.QUESTION in row_of(step, item), step.text
