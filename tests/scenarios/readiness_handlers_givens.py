"""The Givens of features/readiness.feature in grammar 4 (b240 phase 20): each a `local` handler of its template
that takes a step of readiness's scenarios (`mine`) and returns False on any other, which then goes on to the
registry. What a Given says is kept in the scenario's context for the When (readiness_handlers_line.py) and the
Thens (readiness_handlers_thens.py) to read: the item's lines, the ids `work line` retires, and under `says` what a
refusal names each instance by."""
import importlib.util
import sys
from pathlib import Path


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
R = shared("shop_readiness_world", "readiness_world.py")
local = W.local

NAMED = ("relation row", "universal condition", "upstream entry", "given block", "bar check", "step",
         "rule", "requirement id", "universal condition id")


def says(step, name, text):
    step.context.setdefault("says", {})[name] = text


@local("GivenK")
def given_named(step):
    """`a relation row r1`, `a bar check b1`, ...: a thing the When or another Given makes of its name; nothing yet."""
    if not R.mine(step) or step.kind not in NAMED:
        return False


def _bar_check(step, item, check):
    """The item fails the bar check `check`: the first a request line of it not settled, the next a line of it that
    does not parse; what `work ready` names each by."""
    failed = step.context.setdefault("failed", [])
    failed.append(check)
    if len(failed) == 1:
        R.write_request(step)
        B.write_item(step, item, request=R.REQUEST)
        says(step, check, "line 1 of request %s" % R.REQUEST)
    else:
        R.give_lines(step, item, R.FAILING)
        says(step, check, "frobnicate")


@local("GivenDoesNot")
def given_does_not(step):
    """`the item i1 does not pass this readiness bar`: its one line does not parse; `the item i1 does not meet the
    bar check b1`: the item fails that check (`_bar_check`)."""
    if not R.mine(step) or step.term not in ("pass", "meet"):
        return False
    item = step.names[0]
    if step.term == "pass":
        R.give_lines(step, item, R.FAILING)
    else:
        _bar_check(step, item, step.names[1])


@local("GivenDoes")
def given_does(step):
    """pass: the item's one line passes the bar; has: "no requirement has the requirement id r1" (and of a universal
    condition id) makes the id one that `work line --retires` is refused, any other has (a bar check of the bar, a
    scenario of the item, a step of the scenario) nothing; holds: a term the item holds one that violates `v_t12`; violate: the
    rule the term violates, named by its code."""
    if not R.mine(step) or step.term not in ("pass", "has", "holds", "violate"):
        return False
    if step.term == "pass":
        R.give_lines(step, step.names[0], R.PASSING)
    elif step.term == "has" and step.subject.startswith("no "):
        wrong = R.NONEXISTENT_U if "universal condition" in step.subject else R.NONEXISTENT
        step.context.setdefault("retires", {})[step.names[-1]] = wrong
        says(step, step.names[-1], wrong)
    elif step.term == "holds" and step.nps[0].startswith("the term "):
        R.give_lines(step, step.names[0], R.PASSING, [R.ILL_TERMED])
        says(step, step.names[1], R.ILL_TERM)
    elif step.term == "violate":
        says(step, step.names[1], "v_t12")


@local("GivenK_A", "item")
def given_item_shaped(step):
    """`the item i1 is `shaped``: the backlog's, the item kept as the one a step's lines go onto."""
    if R.mine(step):
        step.context["item"] = step.names[0]
    return False
