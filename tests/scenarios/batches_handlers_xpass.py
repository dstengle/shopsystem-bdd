"""A ready item whose new line's scenario passes on the lay (b488, batches r97): "the scenario s1 succeeds in the
workspace w1" of the item's scenario (batches_handlers4's `passes_given`) makes `[batch] tests` of `work batch start`
run that scenario of the batch's worktree `batch-1` (its lines laid, titled as the item is) with every step bound to
one that passes; "the batches service names the scenario s1" reads its title in what the run printed."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


def parked():
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/batches_handlers_parked.py"))


def passing_on_lay(step):
    """Under `work batch start`, the passing item's scenario run in the worktree the start lays the lines in."""
    item = step.context.get("passing")
    if not item:
        return
    tree = step.repo / ".shop" / "worktrees" / "batch-1"
    step.context["delivery"] = parked().bound_tests(step, tree / "features" / "work-queue.feature",
                                                    step.context["item_fields"][item]["title"])


T.BEFORE_START.append(passing_on_lay)


@four("GivenDoes", "has", *BOTH)
def has_id(step):
    """`the requirement r1 has the requirement id r2`, of the item whose scenario passes: the id the lay gives its
    line, which its scenario is tagged with."""
    if [k for k, _ in parts(step)] != ["requirement", "requirement id"] or "scenario_of" not in step.context:
        return False


@four("ThenDoes", "name", *BOTH)
def names_scenario(step):
    (_, _), (k, name) = parts(step)
    if k != "scenario" or name not in step.context.get("scenario_of", {}):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    title = step.context["item_fields"][step.context["scenario_of"][name]]["title"]
    assert title in done.stdout, (step.text, title, done.stdout)
