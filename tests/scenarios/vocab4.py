"""The steps of a codified-2 feature in pytest-bdd (the CNL 4 design, I21-I27; b240 phase 13, from batch-33's b153 and
b154): a step of a feature whose capability file says `language: codified-2` read through the step grammar 4
(`features_vocab4`), as `features generate` wrote it; a step grammar 4 has no reading of is read as vocab.py reads
every other step. One step definition for each keyword matches a text grammar 4 reads, beside vocab.py's own
(`register`); the step function of every definition, and of work_queue_world's `bind_all`, reads the step again
(`step`), so whichever matches runs it alike."""
from functools import cache
from pathlib import Path

import features_vocab4
import spec_language


@cache
def _reading(root, keyword, text):
    try:
        return features_vocab4.step(root, keyword, text)
    except features_vocab4.StepError:
        return None


@cache
def _any(root):
    import spec_read
    return any(spec_read.codified(path, (spec_read.MARKER4,))
               for path in (Path(root) / "spec" / "capabilities").glob("*.md"))


def reads(root, keyword, text):
    """True when the step grammar 4 reads the text under its keyword, and a capability is codified-2 (no step is
    parsed in grammar 4 while none is); once a process for each text."""
    return _any(str(root)) and _reading(str(root), keyword, text) is not None


@cache
def _four(root, feature):
    return spec_language.four(root, Path(feature).stem)


def four(root, request):
    """True when the scenario of `request` is of a feature whose capability is codified-2."""
    node = request.node
    scenario = getattr(getattr(node, "obj", None) or getattr(node, "function", None), "__scenario__", None)
    return scenario is not None and _four(str(root), scenario.feature.filename)


def step(root, keyword, text, request):
    """The step's Call in grammar 4 when its scenario's feature is of a codified-2 capability and grammar 4 reads it,
    else None; a fresh Call each time, since a handler may set its fields."""
    if not four(root, request) or not reads(root, keyword, text):
        return None
    return features_vocab4.step(str(root), keyword, text)


class Parser:
    """A pytest-bdd step parser for any text of one keyword that grammar 4 reads."""

    def __init__(self, root, keyword):
        self.root, self.keyword, self.name = str(root), keyword, "vocab4 %s" % keyword

    def is_matching(self, name):
        return reads(self.root, self.keyword, name)

    def parse_arguments(self, name):
        return {"text": name}


def register(namespace, root, step_function, marker):
    """One step definition for each keyword, named apart from vocab.py's."""
    import pytest
    from pytest_bdd.steps import StepFunctionContext
    for keyword in ("given", "when", "then"):
        context = StepFunctionContext(type=keyword, step_func=step_function(root, keyword),
                                      parser=Parser(root, keyword))
        name = "pytestbdd_stepdef_%s_vocab4" % keyword
        namespace[name] = pytest.fixture(name=name)(marker(context))
