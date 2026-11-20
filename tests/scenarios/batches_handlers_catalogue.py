"""The construct catalogue a batch opened does not keep (batches r75, b390): no item whose status is `ready` among the
scenario's items, no construct catalogue in the repository, and the Then read off the run: `grammar/constructs.md` on
no branch of the repository."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four = F.four
CATALOGUE = "grammar/constructs.md"
# The line of the world's own ready item (batches_world's D21 item, the one `work batch start` picks): a backticked
# value that spells a construct's code (`done`), cited by no "uses", so its line uses no construct.
VALUED = "While an initiative is `done`, when the person runs `work abandon` on the initiative, `work` shall exit successfully."


@four("GivenK_A", "item", "batches")
def no_ready_item(step):
    """No item whose status is `ready` exists, said of the line "no requirement of an item whose status is `ready`
    uses a construct": no item the scenario names is `ready`, and the one ready item, the world's own that `work batch
    start` picks, has a line that uses no construct but holds a value that spells one's code."""
    if not step.text.startswith("no item whose status is ") or step.names:
        return False
    for name in list(step.context.get("items", {})):
        assert B.fields_of(step, name).get("status") != step.values[0].strip("`"), step.text
    step.context["own_line"] = VALUED


@four("GivenDoes", "exist", "batches")
def no_catalogue(step):
    """No construct catalogue exists: the repository holds no `grammar/constructs.md`."""
    if step.subject != "no construct catalogue":
        return False
    (step.repo / CATALOGUE).unlink(missing_ok=True)
    step.context["no_catalogue"] = True


def _keeps_no_catalogue(step):
    """The batches service does not keep a construct catalogue: the batch opened (so the lay ran), and no branch of the
    repository, the base's or the batch's, holds `grammar/constructs.md`."""
    if step.nps != ["a construct catalogue"]:
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    assert step.context.get("no_catalogue"), (step.text, "a construct catalogue existed")
    for branch in T.git(step, "branch", "--format=%(refname:short)").split():
        held = T.git(step, "ls-tree", "--name-only", "-r", branch, "--", CATALOGUE).split()
        assert CATALOGUE not in held, (step.text, branch, done.stdout, done.stderr)
    assert not (step.repo / CATALOGUE).exists(), step.text


# A negated keep is tried as each of the CLI's spellings of keeping in turn (requested.NEGATED), the first that passes
# taken: the check is each one's, so no looser handler of another spelling passes it.
for _term in sys.modules["vocab"].vocab4.requested.KEEPS:
    four("ThenDoesNot", _term, "batches")(_keeps_no_catalogue)
