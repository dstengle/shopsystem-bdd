"""Handlers of features/backlog.feature in grammar 4 (b240, b158): its steps keyed by the verb or the command alone
(`ThenDoes set`, `GivenDoes has`, `WhenRuns `work withdraw``), each in world_four's chain of the backlog's and the
batches' handlers, over the items backlog_world.py writes. A handler here returns False for a step of another kind
than the backlog's, which the batches' handlers (batches_handlers4.py) or the registry then take."""
import json
import re
import shlex
import sys

W, B, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_world_four"))
four, kind, parts = F.four, F.kind, F.parts
BOTH = ("backlog", "batches")
TEXT = {"refuse": ("out of scope",), "answer": ("the first reading",)}


def done_ok(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    return done.stdout


def ensure(step, name):
    if not B.item_rel(step.context, name):
        B.write_item(step, name)


@four("WhenRuns", "`work withdraw`", *BOTH)
@four("WhenRuns", "`work answer`", *BOTH)
@four("WhenRuns", "`work show`", *BOTH)
@four("WhenRuns", "`work refuse`", *BOTH)
@four("WhenRuns", "`work shape`", *BOTH)
def run_on_item(step):
    verb = B.bare(step.term).split()[1]
    B.run_work(step, verb, B.ident(step.names[-1]), *TEXT.get(verb, ()))


@four("WhenRuns", "`work rate --value high-value --urgency low-urgency --size small`", *BOTH)
def work_rate(step):
    B.run_work(step, *shlex.split(B.bare(step.term))[1:2], B.ident(step.names[-1]), *shlex.split(B.bare(step.term))[2:])


@four("WhenRuns", "`work backlog`", *BOTH)
def work_backlog(step):
    B.run_work(step, "backlog", *[B.bare(o) for o, _ in (getattr(step, "options", None) or [])])


@four("ThenK_A", "item", *BOTH)
def item_is(step):
    """The item's attribute is the value; an item no Given wrote is the one the run wrote."""
    if not B.item_rel(step.context, step.names[0]):
        B.bind_written(step, step.names[0])
    got = W.field(B.item_file(step, step.names[0]), step.attribute)
    assert got == B.bare(step.values[0]), (step.text, got)


@four("ThenDoes", "set", *BOTH)
def sets(step):
    """`work` sets the T of the item i1 to `v`: the item's file says it; the batches' kinds are theirs."""
    found = re.match(r"^`work` sets the (\w+) of the item (i\d+) to `([^`]+)`$", step.text)
    if not found:
        return False
    attribute, name, value = found.groups()
    done_ok(step)
    assert W.field(B.item_file(step, name), attribute) == value, (step.text, W.field(B.item_file(step, name),
                                                                                       attribute))


@four("ThenDoes", "write", *BOTH)
@four("ThenDoes", "commit", *BOTH)
def writes_item(step):
    (k, name), = parts(step)[1:]
    if k == "item":
        rel = B.bind_written(step, name) if step.term == "write" else B.item_rel(step.context, name)
        if step.term == "commit":
            B.in_commits(step, rel)
    elif k == "dependency" and step.term == "write":
        assert name in step.context.get("deps", {}), (step.text, "no item gained the dependency")
    else:
        return False


@four("ThenDoes", "has", *BOTH)
def has_then(step):
    """The item i1 has the dependency d1 (its file gained one), the title t1 (the title its file has)."""
    (k1, item), (k2, name) = parts(step)
    if k1 != "item" or k2 not in ("dependency", "title"):
        return False
    if k2 == "title":
        step.context.setdefault("titles", {})[name] = item
        return
    done_ok(step)
    gained = [d for d in B.depends_on(B.item_file(step, item))
              if d not in step.context.get("item_fields", {}).get(item, {}).get("depends_on", [])]
    assert gained, (step.text, B.changed(step))
    step.context.setdefault("deps", {})[name] = {"of": item, "on": gained[0]}


@four("GivenDoes", "has", *BOTH)
@four("GivenDoes", "on", *BOTH)
def has_given(step):
    """A dependency of an item (has) or on one (on), a question on an item; the repository's and the command's own
    things are the world's (has with no name)."""
    (k1, n1), (k2, n2) = parts(step)
    if n1 is None:
        return
    if (k1, k2) == ("item", "dependency") or (k1, k2) == ("dependency", "item"):
        dep, item = (n2, n1) if k1 == "item" else (n1, n2)
        found = step.context.setdefault("deps", {}).setdefault(dep, {})
        found["of" if k1 == "item" else "on"] = item
        B.add_dependency(step, found)
    elif (k1, k2) == ("question", "item"):
        step.context.setdefault("questions", {})[n1] = [n2]
    else:
        return False


@four("GivenDoes", "exist", *BOTH)
def exists(step):
    k, name = parts(step)[0]
    if k == "item":
        ensure(step, name)
    elif k != "dependency":
        return False


@four("GivenK", "JSON object", *BOTH)
@four("GivenK", "push", *BOTH)
@four("GivenK", "branch name", *BOTH)
@four("GivenK", "upstream branch", *BOTH)
@four("GivenK", "question", *BOTH)
def given_noted(step):
    """A thing the world makes itself, as the steps about it say."""


@four("ThenDoes", "refuse", *BOTH)
def refuses(step):
    done = step.context["result"]
    assert done.returncode == 1, (step.text, done.returncode, done.stdout, done.stderr)


@four("ThenDoes", "name", *BOTH)
def names_item(step):
    """`work` names the status of the item i1: its label and its status as it was; the task: its batch's task."""
    done = step.context["result"]
    said = done.stdout + done.stderr
    k, name = parts(step)[1]
    if step.nps[0].startswith("the status of the item "):
        assert '%s "%s"' % (B.ident(name), B.title_of(step, name)) in said, (step.text, said)
        assert step.context["item_fields"][name]["status"] in said, (step.text, said)
    elif k == "task" and step.context.get("git_branches"):
        assert "task %s of batch-1" % name in said and "batch-1-b1" in said, (step.text, said)
    else:
        return False


def row_of(step, name):
    line = B.row(done_ok(step), name)
    assert line is not None, (step.text, step.context["result"].stdout)
    return line


@four("ThenPrints", "`work`", *BOTH)
def prints(step):
    """What `work backlog` or `work show` printed: an item's row and its fields, a title, a dependency, a question,
    the JSON object."""
    if W.runs(step)[-1]["args"][1:2] == ["batch"]:
        return False
    np = step.nps[0]
    k, name = kind(np)
    stdout = done_ok(step)
    if k == "JSON object":
        assert isinstance(json.loads(stdout), dict), stdout
    elif k == "title":
        item = step.context["titles"][name]
        assert B.title_of(step, item) in stdout, (step.text, stdout)
        line = B.row(stdout, item)
        assert line is None or B.title_of(step, item) in B.cells(line), (step.text, line)
    elif k == "dependency":
        dep = step.context["deps"][name]
        assert "blocked by %s" % B.ident(dep["on"]) in row_of(step, dep["of"]), (step.text, stdout)
    elif k == "question":
        assert "question: %s" % B.QUESTION in row_of(step, step.context["questions"][name][0]), (step.text, stdout)
    elif k == "remote":
        assert "not pushed: %s: " % name in stdout + step.context["result"].stderr, (step.text, stdout)
    elif " of the item " in np:
        attribute, item = np[4:].split(" of the item ")
        line, wanted = row_of(step, item), W.field(B.item_file(step, item), attribute)
        if attribute == "status":
            assert B.heading_of(stdout, line) == wanted, (step.text, line)
        else:
            assert wanted in B.cells(line), (step.text, wanted, line)
    elif k == "item":
        row_of(step, name)
    else:
        return False

