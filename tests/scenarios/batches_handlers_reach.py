"""A scenario a task's change does not reach (b456, batches r78): "the scenario s1 breaks in the workspace w1" of a
scenario that has a capability, not an item, is a failing test of that capability, `tests/scenarios/test_review.py`
of the fixture's `review`, which holds no requirement id of the task's item (whose lines are in `work-queue`, beside
a passing `tests/scenarios/test_work_queue.py`); no kept change of the task touches `features/review.feature`.
`.shop/delivery.toml` runs pytest over `tests/`, so `work batch done` passes only when it leaves the test of a
capability the change does not reach out."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
CAPABILITY = "review"          # a capability of the fixture's spec other than the items' work-queue
TESTS = "[batch]\ntests = 'python3 -m pytest -q -p work_items -p no:cacheprovider tests'\n"


@four("GivenDoes", "fail", *BOTH)
def breaks(step):
    """The scenario breaks: a scenario of no item, its capability given by a later step."""
    k, name = parts(step)[0]
    if k != "scenario" or name in step.context.get("scenario_of", {}):
        return False
    step.context.setdefault("unreached", {})[name] = None
    step.context["delivery"] = TESTS
    make_tests(step)


@four("GivenDoes", "has", *BOTH)
def has_capability(step):
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) != ("scenario", "capability") or n1 not in step.context.get("unreached", {}):
        return False
    step.context["unreached"][n1] = CAPABILITY


@four("GivenDoes", "holds", *BOTH)
def holds_none(step):
    """The capability holds no requirement id of the item (`review` holds none of work-queue's); the workspace holds no
    kept change that touches the capability's feature (the world's commit of the task adds `src/b<j>.txt`)."""
    if "unreached" not in step.context or not step.nps or not step.nps[-1].startswith("no "):
        return False


@four("GivenK", "capability", *BOTH)
def given_capability(step):
    """The capability, the fixture's `review`, once a scenario has it."""
    if "unreached" not in step.context:
        return False


def make_tests(step):
    """The tests of the two capabilities, written before the world commits main and makes the batch."""
    tests = step.repo / "tests" / "scenarios"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / ("test_%s.py" % CAPABILITY)).write_text("def test_breaks():\n    assert False\n")
    (tests / "test_work_queue.py").write_text("def test_passes():\n    pass\n")
