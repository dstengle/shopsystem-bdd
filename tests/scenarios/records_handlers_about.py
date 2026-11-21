"""Records' `--about` of an item, a batch or nothing (r3, r5, r6, b49): the item `.shop/backlog/b<n>.md` and the batch
`.shop/batches/<n>/plan.md` a Given brings in, each written with its id; a text that denotes one of them, or nothing,
given to `work record` as its `--about` by design_model_check_handlers_forms' When; and the Then of the record's
`about:`, the id of what it concerns. Each Given a `local` taken only in records' scenarios."""
import importlib.util
import re
import sys
from pathlib import Path

from vocab import handler


def shared(name, file):
    """A module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
H = shared("shop_design_model_check_handlers", "design_model_check_handlers.py")
local = W.local
# what a Given brings in: its kind, the file that holds it and its id, by the number of its name (`i1`, `b1`)
THINGS = {"item": (".shop/backlog/b%s.md", "item/%s/b%s", "item"),
          "batch": (".shop/batches/%s/plan.md", "batch/%s/batch-%s", "batch")}


def mine(step):
    """True for a step of features/records.feature's own groups."""
    return sys.modules["vocab"].origin(step.request.node) == "records"


def ident(kind, name):
    return THINGS[kind][1] % (H.PATH, re.sub(r"\D", "", name))


@local("GivenK", "item")
@local("GivenK", "batch")
def given_thing(step):
    """`an item i1`, `a batch b1`: its file, the frontmatter its id and kind."""
    if not mine(step):
        return False
    rel, _, kind = THINGS[step.kind]
    H.write(step.repo, rel % re.sub(r"\D", "", step.names[0]),
            "---\nid: %s\nkind: %s\n---\n\n# %s\n" % (ident(step.kind, step.names[0]), kind, step.names[0]))


@local("GivenDoes")
@local("GivenDoesNot")
def given_denotes(step):
    """`the text t1 denotes the item i1`: the item's id the record's `--about`; `... denotes no node` (and no item,
    no batch): an id of a kind each of them has, of nothing this repository holds."""
    if not mine(step) or step.term != "denote":
        return False
    found = [(kind, name) for kind in THINGS for name in step.names if any(np.startswith("the %s " % kind)
                                                                            for np in step.nps)]
    about = ident(*found[0]) if found and len(step.names) > 1 else H.full("capability", "nowhere")
    step.context["record_about"] = ["--about", about]
    for name in step.names:
        H.says(step, name, about)


@handler("ThenDoes", "concern")
def concerns(step):
    """`the record r1 concerns the item i1`: the record `work record` wrote is about the item's id; the registry's
    handler of its key, which `features vocab --check` finds (no other feature says concern)."""
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    text = (step.repo / done.stdout.strip().splitlines()[-1]).read_text()
    kind = next(kind for kind in THINGS if step.nps[-1].startswith("the %s " % kind))
    assert "\nabout: %s\n" % ident(kind, step.names[-1]) in text, text


@local("ThenDoes")
def names_text(step):
    """`the records service names the text t1`: the refusal names the `--about` the record was filed with. r5's
    scenario says "names the record r1", as its When files the record r1 "with the record r1": grammar 4 reads "with
    the text" in r5 as the parameter `text` given the record (its form's `param(e1, text, x6)`), so the thing named is
    what the When gave as the text, whichever instance the step calls it."""
    if not mine(step) or step.term != "name" or "record_about" not in step.context:
        return False
    done, about = step.context["result"], step.context["record_about"][-1]
    assert about in done.stdout + done.stderr and "--about" in done.stderr, (about, done.stdout, done.stderr)
