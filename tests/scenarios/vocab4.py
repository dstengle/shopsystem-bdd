"""The steps of a codified-2 feature in pytest-bdd (the CNL 4 design, I21-I27): a step of a feature whose capability
file says `language: codified-2` read through the step grammar 4 (`features_vocab4`), as `features generate` wrote
it; a step grammar 4 has no reading of (a codified-2 file that still holds lines of the old grammar) is read as
vocab.py reads every other step. One step definition for each keyword matches a text grammar 4 reads, beside
vocab.py's own; the step function of every definition reads the step again, so whichever matches runs it alike."""
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
def _four(root, feature):
    return spec_language.four(root, Path(feature).stem)


def step(root, keyword, text, request):
    """The step's Call in grammar 4 when its scenario's feature is of a codified-2 capability and grammar 4 reads it,
    else None; a fresh Call each time, since a handler may set its fields."""
    scenario = getattr(getattr(request.node, "obj", None), "__scenario__", None)
    if scenario is None or not _four(str(root), scenario.feature.filename) or not _reading(str(root), keyword, text):
        return None
    return features_vocab4.step(str(root), keyword, text)


class Parser:
    """A pytest-bdd step parser for any text of one keyword that grammar 4 reads."""

    def __init__(self, root, keyword):
        self.root, self.keyword, self.name = str(root), keyword, "vocab4 %s" % keyword

    def is_matching(self, name):
        return _reading(self.root, self.keyword, name) is not None

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
