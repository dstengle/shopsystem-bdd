"""The codified-2 world's handlers of an attribute's value (b240 phases 5 and 6): "the file f1 is `3.0.1`" and "the
stage s1 is `high`", the Givens features_generate4 writes of an ordered comparison ("the version of a file is after
`3.0.0`") and of a value set ("the outcome of a line is one of ..."); "the line l1 is not `refused`", which records
nothing; and "the line l1 has no outcome", which records None. Each records under the scenario's `values`, (the
instance, the attribute) -> the value; a world that builds the instance reads it there."""
from vocab import handler


def value(step):
    if " is not " in step.text:
        return
    step.context.setdefault("values", {})[(step.names[0], step.attribute)] = (step.values or [None])[0]


for _kind in ("file", "stage", "line"):     # the fixture's kinds with an ordered attribute or a value set's Given
    handler("GivenK_A", _kind)(value)
