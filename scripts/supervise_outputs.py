"""What a stage's result must give for `work run` to take its work as done (supervision r131, r132, design-decision
0038): the stage's output, and the question that says it is missing. The one word a result's status gives decides no
transition (r133). Standard library only."""


def given(data, field):
    """Whether the result `data` gives `field`: a list with something in it, or a text that is not blank."""
    value = data.get(field)
    return bool(value) and (not isinstance(value, str) or bool(value.strip()))


def missing(role, data):
    """What the stage of `role` (researcher, planner, reviewer) was to deliver and its result `data` does not give, as
    words (the researcher's file set), else None. The implementer's output is commits the tests pass on; the merge says
    if they are missing."""
    if role == "researcher" and not given(data, "fileset"):
        return "the researcher's file set"
    if role == "planner":
        if not given(data, "plan"):
            return "the planner's plan"
        if not given(data, "fileset"):
            return "the planner's file set"
    if role == "reviewer" and not given(data, "findings"):
        return "the reviewer's findings"
    return None


def question(role, what):
    """The question that names `what` as missing from the result of the stage of `role`, which gave no question."""
    return "%s is missing: the %s's result gave no question and does not give it" % (what, role)
