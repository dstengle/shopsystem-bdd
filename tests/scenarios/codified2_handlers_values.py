"""The codified-2 world's handlers of an attribute's value (b240 phase 5): "the file f1 is `3.0.1`" and "the stage s1
is `high`", the Givens features_generate4 writes of an ordered comparison ("the version of a file is after `3.0.0`").
Each records under the scenario's `values`, (the instance, the attribute) -> the value; a world that builds the
instance reads it there."""
from vocab import handler


def value(step):
    step.context.setdefault("values", {})[(step.names[0], step.attribute)] = step.values[0]


for _kind in ("file", "stage"):     # the fixture's kinds with an ordered attribute
    handler("GivenK_A", _kind)(value)
