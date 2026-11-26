"""A batch whose submit broke a scenario of no item (batches r154, b703): over batches_handlers_reach's scenario of the
fixture's `review` capability that breaks (a test none of the batch's items holds an id of and no task's change
reaches), "the batch b1 holds no item" is the world's own in-batch item alone, whose task is done and whose scenario
does not break; `work batch review` run before the poll so that its whole-suite run is kept failed, then `work batch
next`; and the Then that the batches service returns the scenario, its test among the step's failed tests."""
import json
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


def _module(stem):
    """A handler module of the glob, by its file's stem."""
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


def _next():
    return _module("batches_handlers_next")


@first("GivenDoes", "holds")
def holds_no_item(step):
    """`the batch b1 holds no item`: none the scenario names; the world's own in-batch item gives its task."""
    (k1, _), (k2, _) = parts(step)[:2]
    if (k1, k2) != ("batch", "item") or not step.nps[-1].startswith("no "):
        return False


@first("WhenRuns", "`work batch next`")
def polled_after_failure(step):
    """The poll after a submit refused by a scenario of no item (`unreached`, batches_handlers_reach)."""
    if not step.context.get("unreached") or step.context.get("failing"):
        return False
    T.prepare(step)
    T.ensure_batch(step)
    batch = next(n for n in step.names if n in step.context["given"]["batch"])
    _next().refused_submit(step, batch)
    done = T.run_batch(step, "next", T.batch_name(step, batch), "--json")
    step.context["polled"] = json.loads(done.stdout) if done.returncode == 0 else None


@four("ThenPrints", "`work`", *BOTH)
def returns_scenario(step):
    """`the batches service returns the scenario s1`: its capability's test among the batch step's failed tests."""
    kind, name = parts(step)[-1]
    if kind != "scenario" or "polled" not in step.context:
        return False
    content = _next()._step(step)
    capability = step.context.get("unreached", {}).get(name) or _module("batches_handlers_reach").CAPABILITY
    test = "tests/scenarios/test_%s.py::" % capability.replace("-", "_")
    assert any(t.startswith(test) for t in content.get("failed tests") or ()), (step.text, content)
