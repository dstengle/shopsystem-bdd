"""Handlers of applying's g24 (r24, b830, from laying's g48, b872), `work_queue_world.local`s tried before
applying_handlers' own, each taking only a step of a scenario of that group (`mine`): an item that makes two areas,
`watering` and `plots`, both new capabilities of its own beside the domain-model fixture's spec, the term `plot` of
the plots layer (its model line `object plot`) and watering's requirement saying "a plot". The Givens record
nothing; the When is applying_handlers' `applied`; the Thens read the reply's changed paths and the specification's
files: watering's capability file kept, its model file kept and importing `plots`."""
import re
import sys

A = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/applying_handlers.py"))   # loaded before this, by name
W, world = A.W, A.world
GROUP, USING, USED = "g24", "watering", "plots"
BLOCK = """### plots

narrator: a gardener
group: service
purpose: The plots of a garden, each kept by its name.

#### [g1] A plot added is kept
- [r1] When the person adds a note, the notes service shall keep the note.

### watering

narrator: a gardener
group: service
purpose: The watering of a garden's plots.

#### [g1] A plot watered is kept
- [r1] When the person adds a note, the notes service shall keep a plot.

### plots model

```model
object plot
  attributes: name (text)
```

- **plot** (noun) → object plot. A piece of ground a gardener tends. Plural: plots."""


def mine(step):
    return A.group(step, (GROUP,)) is not None


def given(step):
    """A Given of g24: what its world builds at the When."""
    if not mine(step):
        return False
    world(step)


def requests(step):
    """`the batches service applies the item i1 to the specification s1`: the world built, the item applied."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    A.applied(step, lambda s: A.fixture(s) or BLOCK)


def _imports(text):
    found = re.search(r"(?m)^imports: \[([^\]]*)\]$", text)
    return [n.strip() for n in found.group(1).split(",") if n.strip()] if found else []


def then(step):
    """`the specification service keeps `watering``: its capability file the apply changed; `keeps the area a1`:
    watering's model file the apply changed; `the area a1 imports `plots``: that model file's imports name plots."""
    if not mine(step) or "tree" not in world(step):
        return False
    term = "keep" if step.term in A.KEEPS else step.term
    model = "spec/model/%s.md" % USING
    if term == "keep" and "`%s`" % USING in step.text:
        A.kept(step, "spec/capabilities/%s.md" % USING)
    elif term == "keep":
        A.kept(step, model)
    elif term in ("import", "imports"):
        assert USED in _imports(A.kept(step, model)), A.kept(step, model)
    else:
        raise AssertionError("applying_handlers_areas takes no Then %s %s: %s" % (step.template, step.term, step.text))


for _template in ("GivenK", "GivenK_A", "GivenCode", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)
sys.modules["vocab"].handler("GivenCode", "item")(A.untaken)   # the key `features vocab --check` reads
