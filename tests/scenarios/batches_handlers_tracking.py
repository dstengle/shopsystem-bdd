"""batches' requests of tracking's operations (b578, decision 0133; r100, r101, r105-r112): the Thens "the batches
service allocates (delivers, restores, suspends, reopens) the item i1" and their negations read off the item's file
after the run, as the status the operation moves it to (items r56-r59, r31) or, negated, any other; a suspended
item's question the park's under its `## Question`; "resolves the context request c1" batches_handlers_request's
`resolved`. Each is in world_four's chain of the batches' scenarios and returns False for a step of
another thing."""
import sys

W, B, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_world_four"))
four, parts = F.four, F.parts

# the status each operation moves an item to
POST = {"allocate": "in-batch", "deliver": "delivered", "restore": "ready", "suspend": "needs-input",
        "reopen": "shaped"}


def _module(stem):
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)


def _item(step):
    return next((name for k, name in parts(step) if k == "item"), None)


def _requested(step, negated):
    item = _item(step)
    if item is None:
        return False
    _done(step)
    got = W.field(B.item_file(step, item), "status")
    assert (got == POST[step.term]) != negated, (step.text, got)
    if step.term == "suspend" and not negated:
        text = B.item_file(step, item).read_text()
        assert "\n## Question\n\n%s\n" % _module("batches_handlers_more").QUESTION in text, (step.text, text)


for _verb in POST:
    four("ThenDoes", _verb, "batches")(lambda step: _requested(step, False))
    four("ThenDoesNot", _verb, "batches")(lambda step: _requested(step, True))


@four("ThenDoes", "resolve", "batches")
def resolves(step):
    """The context request the item was taken in from, resolved (batches_handlers_request's `resolved`)."""
    (k, name), = [p for p in parts(step) if p[1]]
    if not k.endswith("request"):
        return False
    _module("batches_handlers_request").resolved(step, name)
