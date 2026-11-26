"""A fix of a batch's refused submit (batches r161-r163, b713): "the fix f1 exists" is a commit on the first task's
branch, citing its item, made after `work batch review`'s whole-suite run was refused (batches_handlers_next's
`refused_submit`, which runs batches_world's `AFTER_SUBMIT`); "no fix exists" makes none, so no task's branch moves after the
submit."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


@four("GivenK", "fix", *BOTH)
def given_fix(step):
    """`a fix f1`: made only once a Given says it exists."""
    T.given(step, "fix", step.names[0])


@four("GivenDoes", "exist", *BOTH)
@four("GivenDoesNot", "exist", *BOTH)
def fix_exists(step):
    """`the fix f1 exists` (a commit after the refused submit); `no fix exists` (none)."""
    k, _ = parts(step)[0]
    if k != "fix":
        return False
    step.context["fixed"] = step.template == "GivenDoes" and not (step.subject or "").startswith("no ")


def fix(step, batch):
    """The fix made, when a Given says it exists: a commit citing the first task's item on its branch."""
    if not step.context.get("fixed"):
        return
    task = next(t for t, f in step.context["given"]["task"].items() if f["batch"] == batch)
    _, branch = T.task_row(step, task)
    item = branch.rsplit("-", 1)[1]
    tree = T.outside(step) / ("fix-%s" % branch)
    T.git(step, "worktree", "add", "-q", str(tree), branch)
    (tree / "src").mkdir(exist_ok=True)
    (tree / "src" / ("%s-fix.txt" % item)).write_text("fixed %s\n" % item)
    T.git(step, "add", "-A", cwd=tree)
    T.git(step, "commit", "-q", "-m", "fix %s\n\nItem: %s" % (item, item), cwd=tree)
    T.git(step, "worktree", "remove", "--force", str(tree))


T.AFTER_SUBMIT.append(fix)
