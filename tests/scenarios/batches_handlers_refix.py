"""A fix after a review of a scenario its item's change broke (reviews r14, b703), over batches_world's batch and
batches_handlers_finding's review, recorded with no finding: the scenario of the item that succeeds in the batch's
workspace is one the batch's last whole-suite run broke, so once the batch is made (T.AFTER_BATCH) that run's failure
is kept under the batch's name as `work batch review` keeps it (batch_rerun), naming the item's scenario test; the
world's commit on the item's task branch, citing the item, is the fix the review accepts, and `[batch] tests` pass."""
import sys

import batch_broken
import batch_rerun

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))


def broken_before(step, name):
    """The batch's kept failed run, when it has a review with no finding and a scenario of its item succeeds."""
    given = step.context.get("given", {})
    reviews = [r for r, f in given.get("review", {}).items() if f.get("batch") == name]
    item = step.context.get("passing")
    if not reviews or given.get("review finding") or not item:
        return
    test = "tests/scenarios/test_work_queue.py::%s" % batch_broken.test_name(step.context["item_fields"][item]["title"])
    batch_rerun.keep(step.repo, T.batch_name(step, name), [test])


T.AFTER_BATCH.append(broken_before)
