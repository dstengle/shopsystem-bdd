"""Handlers of features/batches.feature's chore steps (r41-r43, b316), each in world_four's chain beside the
backlog's: an item that holds a chore (its `## Chore`, written again as later Givens change it: a check that fails in
the task's worktree, a file the chore does not hold, which the commit of the item's branch the world makes touches,
`src/b<j>.txt`), and the Thens that the batch brief holds the chore and that a refusal names the chore or the
file."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")

PASSING = "true"
FAILING = "test -f src/never-built.txt"


def _write(step, chore):
    """The item's `## Chore` written from what the Givens said of the chore `chore`; what `work` names it by."""
    found = step.context["chores"][chore]
    fields = step.context.get("item_fields", {}).get(found["item"], {})
    sections = dict(fields.get("sections", {"Notes": B.NOTE}),
                    Chore="Files:\n%s\n\nCheck: `%s`" % ("\n".join("- %s" % f for f in found["files"]), found["check"]))
    B.write_item(step, found["item"], sections=sections)
    step.context.setdefault("says", {})[chore] = found["check"]


@four("GivenDoes", "holds", *BOTH)
def item_holds_chore(step):
    """The item holds the chore: its `## Chore` names the files the world's commit touches (`src/`), its check
    passing."""
    (k1, item), (k2, chore) = parts(step)
    if (k1, k2) != ("item", "chore"):
        return False
    step.context.setdefault("chores", {})[chore] = {"item": item, "files": ["src/"], "check": PASSING}
    _write(step, chore)


@four("GivenDoes", "fail", *BOTH)
def chore_fails(step):
    """The chore fails in the worktree of the task: its check looks for a file no commit adds."""
    (k1, chore), _ = parts(step)
    if k1 != "chore":
        return False
    step.context["chores"][chore]["check"] = FAILING
    _write(step, chore)


@four("GivenDoesNot", "holds", *BOTH)
def chore_holds_not(step):
    """The chore does not hold the file: it names only `docs/`, and the file is one the world's commit adds."""
    (k1, chore), (k2, file) = parts(step)
    if (k1, k2) != ("chore", "file"):
        return False
    found = step.context["chores"][chore]
    found["files"] = ["docs/"]
    _write(step, chore)
    step.context.setdefault("says", {})[file] = "src/%s.txt" % B.ident(found["item"])


@four("GivenDoes", "touch", *BOTH)
def commit_touches(step):
    """The commit touches the file: the world's commit of the item's branch adds `src/b<j>.txt`, the file's name."""
    (k1, _), (k2, file) = parts(step)
    if (k1, k2) != ("commit", "file"):
        return False
    assert file in step.context.get("says", {}), (step.text, "no Given named the file's path")


@four("GivenK", "file", *BOTH)
def given_file(step):
    """A file: what a later Given says of it names its path."""


@four("ThenDoes", "name", *BOTH)
def names_chore(step):
    """The run was refused (exit 1) naming the chore (its check) or the file (its path)."""
    k, name = parts(step)[1]
    if k not in ("chore", "file"):
        return False
    done = step.context["result"]
    assert done.returncode == 1, (step.text, done.returncode, done.stdout, done.stderr)
    said = step.context["says"][name]
    assert said in done.stderr, (step.text, said, done.stderr)


@four("ThenDoes", "holds", *BOTH)
def brief_holds_chore(step):
    """The batch brief the run wrote holds the chore's files and check under its item's task, in place of ids."""
    (k1, brief), (k2, chore) = parts(step)
    if (k1, k2) != ("batch brief", "chore"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    rel = W.node_rel(step.context, brief)
    assert rel, (step.text, "no batch brief was written")
    text = (step.repo / rel).read_text()
    found = step.context["chores"][chore]
    task = text.split("### ", 1)[1:] and [t for t in text.split("\n### ") if B.ident(found["item"]) + ' "' in t]
    assert task, (step.text, text)
    assert "Chore check: `%s`" % found["check"] in task[0], (step.text, task[0])
    assert ", ".join(found["files"]) in task[0] and "Requirement ids" not in task[0], (step.text, task[0])
