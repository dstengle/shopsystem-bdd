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


unread = shared("shop_scenario_unread", "scenario_unread.py").unread     # b748


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
    elif len(failed) == 2:
        R.give_lines(step, item, R.FAILING)
        says(step, check, "frobnicate")
    else:       # a counter-example's (b273): the lexicon problem of an ill term, the bar's or the spec's own
        step.context["ill"] = item
        says(step, check, R.ILL_TERM)


def _ill_term(step, item, of_the_bar):
    """The ill term (v_t12) of the item's third bar check: the item's lines bring it (a check of this bar, which
    `work ready` names), or the spec's glossary has it already (no check of the bar: the item brings no problem the
    spec without it has not)."""
    if of_the_bar:
        R.give_lines(step, item, R.FAILING, [R.ILL_TERMED])
        return
    R.codify(step)
    index = step.repo / "spec" / "index.md"
    index.write_text(index.read_text().rstrip("\n") + "\n" + R.ILL_TERMED + "\n")


@local("GivenDoesNot")
def given_does_not(step):
    """`the item i1 does not pass this readiness bar`: its one line does not parse; `the item i1 does not meet the
    bar check b1`: the item fails that check (`_bar_check`); `the item i1 does not hold the requirement r5`: the
    requirement a line of the world's other item (r50); `` `universal` does not exist``: the fixture's spec,
    which has no spec/universal.md (b203)."""
    if R.mine(step) and step.term == "has" and step.nps[0].startswith("the bar check "):
        assert step.context.get("ill"), "no bar check the item does not meet before: %s" % step.text
        _ill_term(step, step.context["ill"], of_the_bar=False)
        return None
    if R.mine(step) and step.term == "exist" and step.subject == "`universal`":     # b203: none, as in the fixture
        R.codify(step)
        (step.repo / "spec" / "universal.md").unlink(missing_ok=True)
        return None
    if R.mine(step) and step.term == "exist" and step.subject.startswith("the capability "):     # b354: a new one
        step.context["new"] = step.names[0]
        return None
    if R.mine(step) and step.term in ("hold", "holds") and step.nps[0].startswith("the requirement "):      # r50
        step.context.setdefault("owner", {})[step.names[-1]] = ("not", step.names[0])
        R.give_faults(step)
        return None
    if not R.mine(step) or step.term not in ("pass", "meet"):
        return False
    item = step.names[0]
    if step.term == "pass":
        R.give_lines(step, item, R.FAILING)
    else:
        _bar_check(step, item, step.names[1])


def _owned(step):
    """b14's Givens: the item i1 holds the requirement r1 (a line of the item), the capability c1 has the requirement r1
    (a live requirement of a capability), the requirement r1 has the requirement id r2; kept for the When of
    `work line --reword` and `--remove`, which writes each."""
    if len(step.nps) != 1 or not step.nps[0].startswith(("the requirement ", "the requirement id ")):
        return False
    if step.term == "holds" and step.subject.startswith("the item ") and "requirement id" in step.nps[0]:
        step.context.setdefault("held_ids", {})[step.names[-1]] = step.names[0]       # b323: an id under retired:
    elif step.term == "holds" and step.subject.startswith("the item "):
        step.context.setdefault("owner", {})[step.names[-1]] = ("item", step.names[0])
    elif step.term == "has" and step.subject.startswith("the capability "):
        step.context.setdefault("owner", {})[step.names[-1]] = ("capability", step.names[0])
    elif step.term == "has" and step.subject.startswith("the requirement ") and "requirement id" in step.nps[0]:
        step.context.setdefault("id_of", {})[step.names[-1]] = step.names[0]
    else:
        return False
    return True


@local("GivenDoes")
def given_does(step):
    """pass: the item's one line passes the bar; has: "no requirement has the requirement id r1" (and of a universal
    condition id) makes the id one that `work line --retires` is refused, any other has (a bar check of the bar, a
    scenario of the item, a step of the scenario) nothing; holds: a term the item holds one that violates `v_t12`; violate: the
    rule the term violates, named by its code, or of a requirement group the rule r2, two lines of the item's group
    whose conditions differ (v15k: b333), the group and the rule named by their ids; has no translation or no parse: the requirement a
    line of the item that holds it which `spec logic` reads no translation of (r41) or grammar 4 no parse of (r50)
    (`R.give_faults`), or the universal condition the item's one, beside a passing line
    (b203); holds a universal condition: the item's `U1`, one `spec logic` reads, beside a passing line unless it holds
    no requirement (b516); the capability
    c1 exists: the When names a capability of the spec (b317)."""
    if R.mine(step) and step.term == "exist" and step.subject.startswith("the capability "):     # b317's r56
        step.context.setdefault("exists", set()).add(step.names[0])
        return None
    if not R.mine(step) or step.term not in ("pass", "has", "holds", "violate"):
        return False
    if _owned(step):
        return None
    if step.term == "pass" and step.names[0] in step.context.get("universal_of", {}):     # b516: kept, passing
        R.give_universal(step, step.names[0], step.context["universal_of"][step.names[0]])
    elif step.term == "pass":
        R.give_lines(step, step.names[0], R.PASSING)
    elif step.term == "holds" and step.nps == ["no requirement"]:      # b516: its universal conditions its only lines
        step.context.setdefault("lineless", set()).add(step.names[0])
        if step.names[0] in step.context.get("universal_of", {}):
            R.give_universal(step, step.names[0], step.context["universal_of"][step.names[0]])
    elif step.term == "holds" and step.nps[0].startswith("the universal condition "):       # b203
        R.give_universal(step, step.names[0], R.TRANSLATED_U)
        says(step, step.names[1], "universal#%s" % R.ITEM_U)
    elif step.term == "has" and step.subject.startswith("the universal condition ") and step.nps == ["no translation"]:
        R.give_universal(step, step.context.get("item", "i1"), R.UNREAD)
    elif step.term == "has" and step.subject.startswith("the requirement ") and step.nps in (["no translation"],
                                                                                          ["no parse"]):
        step.context.setdefault("fault", {})[step.names[0]] = step.nps[0].split()[1]       # r41, r50
        R.give_faults(step)
    elif step.term == "has" and step.context.get("says", {}).get(step.names[-1]) == R.ILL_TERM:
        _ill_term(step, step.context["ill"], of_the_bar=True)     # the ill term's check one of this bar
    elif step.term == "has" and step.subject.startswith("no "):
        wrong = R.NONEXISTENT_U if "universal condition" in step.subject else R.NONEXISTENT
        step.context.setdefault("retires", {})[step.names[-1]] = wrong
        says(step, step.names[-1], wrong)
    elif step.term == "holds" and step.nps[0].startswith("the term "):
        R.give_lines(step, step.names[0], R.PASSING, [R.ILL_TERMED])
        says(step, step.names[1], R.ILL_TERM)
    elif step.term == "violate" and step.subject.startswith("the requirement group "):       # b333
        R.give_lines(step, step.context.get("item", "i1"), R.DIFFERING)
        says(step, step.names[0], R.DIFFERING_GROUP)
        says(step, step.names[-1], R.DIFFERING_RULE)
    elif step.term == "violate":
        says(step, step.names[1], "v_t12")
    elif not (step.nps and step.nps[0].startswith(WRITTEN.get(step.term, ()))):
        unread(step, "the Given %r" % step.text)     # b748: no world of readiness reads it


# What a has or holds names that the bar or the When writes, so its Given records nothing: a bar check of the bar, a
# scenario of the item, a step of the scenario; the capability whose block the When writes into the item (drafting r25).
WRITTEN = {"has": ("the bar check ", "the scenario ", "the step "), "holds": ("the capability ",)}


@local("GivenDoes")
@local("GivenDoesNot")
def given_retires(step):
    """b323: the requirement r1 retires (or does not retire) the requirement id r3 the item holds; kept for the When
    of `work line --remove`, which writes the item's history so."""
    if not R.mine(step) or step.term != "retire" or not step.nps[0].startswith("the requirement id "):
        return False
    step.context.setdefault("retires_id", {})[step.names[-1]] = step.template == "GivenDoes"
    return None


@local("GivenK_A", "item")
def given_item_shaped(step):
    """`the item i1 is `shaped``: the backlog's, the item kept as the one a step's lines go onto."""
    if R.mine(step):
        step.context["item"] = step.names[0]
    return False
