"""What a stage's result must give for `work run` to take its work as done (supervision r131, r132, design-decision
0038): the stage's output, and the question that says it is missing. The one word a result's status gives decides no
transition (r133). Standard library only."""
import re


def given(data, field):
    """Whether the result `data` gives `field`: a list with something in it, or a text that is not blank."""
    value = data.get(field)
    return bool(value) and (not isinstance(value, str) or bool(value.strip()))


def missing(role, data):
    """What the stage of `role` (researcher, planner, reviewer) was to deliver and its result `data` does not give, as
    words (the researcher's file set), else None. The implementer's output is commits the tests pass on; the merge says
    if they are missing."""
    if role == "researcher" and not isinstance(data.get("fileset"), list) and not given(data, "fileset"):     # [] says no file changes
        return "the researcher's file set"
    if role == "planner":
        if not given(data, "plan"):
            return "the planner's plan"
        if not given(data, "fileset"):
            return "the planner's file set"
    if role == "reviewer" and not given(data, "findings"):
        return "the reviewer's findings"
    return None


def says(data, field):
    """Whether the result `data` gives `field` as a sentence and gives no question."""
    said = data.get(field) if isinstance(data, dict) else None
    return isinstance(said, str) and bool(said.strip()) and not data.get("questions")


def gives_nothing(data):
    """Whether an apply round's result gives that it applied nothing, because the proposal's answers give what its drafts
    do not hold: its `nothing_applied` field, with no question and no change list (r147)."""
    return says(data, "nothing_applied") and data.get("changes") in (None, [])


def formulated_nothing(data):
    """Whether a formulate round's result gives that it formulated nothing, because the proposal's answers change lines not
    in spec/: its `nothing_formulated` field, with no question (r149, r153)."""
    return says(data, "nothing_formulated")


def sent_back(kind, data):
    """Whether the result `data` of a round of `kind` sends the proposal back to integration: an apply round that gives
    an answer its drafts do not hold, as `unheld_answers` or as `nothing_applied` (r150), or a formulate round that
    formulated nothing (r149)."""
    if kind == "formulate":
        return formulated_nothing(data)
    if kind == "apply":
        unheld = data.get("unheld_answers") if isinstance(data, dict) else None
        return gives_nothing(data) or (isinstance(unheld, list) and bool(unheld))
    return False


def scenario_ids(text):
    """The requirement ids (`r4`) the non-deprecated scenarios of the feature file `text` are tagged with."""
    found, tags = set(), []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("@"):
            tags += line.split()
        elif line.startswith(("Scenario:", "Scenario Outline:")):
            if "@deprecated" not in tags:
                found.update(t[1:] for t in tags)
            tags = []
        elif line and not line.startswith("#"):
            tags = []
    return found


def is_guarantees(root, capability):
    """Whether spec/capabilities/<capability>.md under `root` has `group: guarantees` in its frontmatter."""
    path = root / "spec" / "capabilities" / (capability + ".md")
    head = path.read_text().split("---\n")[1:2] if path.is_file() else []
    return bool(head) and re.search(r"(?m)^group: guarantees$", head[0]) is not None


def unformulated(root, ids):
    """The ids (`thing#r4`) of `ids` with no non-deprecated scenario in features/<capability>.feature under `root`: a
    formulate round's output is a scenario for each requirement its proposal adds or changes (r132), except those of a
    guarantees capability, which has no scenarios (design-decision 0065)."""
    lacking, read = [], {}
    for each in ids:
        if "#r" not in each:     # a term/<term> id is no requirement
            continue
        capability, _, number = each.partition("#")
        if is_guarantees(root, capability):
            continue
        if capability not in read:
            path = root / "features" / (capability + ".feature")
            read[capability] = scenario_ids(path.read_text()) if path.is_file() else set()
        if number not in read[capability]:
            lacking.append(each)
    return lacking


def question(role, what):
    """The question that names `what` as missing from the result of the stage of `role`, which gave no question."""
    return "%s is missing: the %s's result gave no question and does not give it" % (what, role)
