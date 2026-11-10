"""The handlers of grammar 4's steps (a codified-2 feature, b240): a step's key, (template, term), is the verb's or
the command's alone (`GivenDoes has`, `ThenDoes set`, `WhenRuns `work backlog``), so several capabilities handle one
key. `four(template, term, *features)` adds a handler to the key's chain, tried in the order added, each returning
False for a step that is not its own; the chain is the key's handler when the registry has none (vocab.lookup).
`bind(namespace, root, *features)` makes a test module try the chains of its features' handlers first, then
work_queue_world's `bind_all`, so a key another capability's codified-1 handler claims reaches these too."""
import re
import sys

import pytest

# {(template, term): [(features, fn)]}, kept on the vocabulary's module: this module is loaded twice, by the
# handlers' glob and by a test module's import.
sys.modules.setdefault("shop_world_four", sys.modules[__name__])   # what handler modules import
CHAINS = sys.modules["vocab"].FOUR_CHAINS

NP = re.compile(r"^(?:the )?(.+?) ([a-z]+\d+)$")


def kind(np):
    """(kind, name) of a noun phrase "the item i1"; ("repository", None) of "this repository"."""
    found = NP.match(np or "")
    return (found.group(1), found.group(2)) if found else (np.split()[-1], None)


def parts(step):
    """[(kind, name)] of the subject and each noun phrase of a step, in order."""
    return [kind(np) for np in ([step.subject] if step.subject else []) + list(step.nps)]


def _chain(key, features=None):
    def run(step):
        for owners, fn in CHAINS[key]:
            if (features is None or owners & features) and fn(step) is not False:
                return True
        if features is None:
            raise AssertionError("no handler of %s %s takes the step: %s" % (key + (step.text,)))
        return False
    return run


def four(template, term, *features):
    """`@four("ThenDoes", "set", "backlog", "batches")`: fn handles the key's steps in those features' scenarios."""
    def mark(fn):
        key = (template, term)
        if key not in CHAINS:
            CHAINS[key] = []
            sys.modules["vocab"].FOUR_RUN[key] = _chain(key)
        CHAINS[key].append((frozenset(features), fn))
        return fn
    return mark


def bind(namespace, root, *features):
    """`bind_all`, with each step tried first on its key's chain of these features' handlers."""
    from pytest_bdd.steps import StepFunctionContext
    world = sys.modules["shop_work_queue_world"]
    vocab = sys.modules["vocab"]
    world.bind_all(namespace, root)
    mine = frozenset(features)
    for keyword in ("given", "when", "then"):
        context = StepFunctionContext(type=keyword, step_func=_first(root, keyword, mine),
                                      parser=world.Reads(vocab, root, keyword))
        name = "pytestbdd_stepdef_%s_reads_any" % keyword
        namespace[name] = pytest.fixture(name=name)(vocab._marker(context))


def _first(root, keyword, mine):
    """The step function of one keyword: the chain of the key's handlers of `mine`, then bind_all's."""
    world, vocab = sys.modules["shop_work_queue_world"], sys.modules["vocab"]
    rest = world._local_first(vocab, root, keyword)

    def step_function(text, request, docstring=None, datatable=None):
        call = vocab.vocab4.step(root, keyword, text, request)
        if call is not None and (call.template, call.term) in CHAINS:
            call.docstring, call.datatable, call.fixtures = docstring, datatable, request.getfixturevalue
            if _chain((call.template, call.term), mine)(call):
                return None
        return rest(text, request, docstring, datatable)
    return step_function
