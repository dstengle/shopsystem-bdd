"""Handlers of features/decision-tiers.feature in grammar 4 (b240 phase 15): the verbs enforce, supersede and verify,
a test's outcome, a route of a decision and its kind, and the Thens "`model` runs `pytest` on the test" and "the
design-decision d1 has the route r1", over decision_tiers_handlers.py's decision files. "no K enforces (verifies)
..." is what a decision written with no `enforced_by` (no `rests_on`) already says."""
import re
import sys

from vocab import handler

D = sys.modules.get("shop_decision_tiers_handlers")
W = sys.modules["shop_work_queue_world"]
local = W.local
OUTSIDE = "sampling"      # a route outside the four


def tiers():
    """decision_tiers_handlers.py, loaded once under its shared name."""
    global D
    if D is None:
        import importlib.util
        from pathlib import Path
        spec = importlib.util.spec_from_file_location("shop_decision_tiers_handlers",
                                                      Path(__file__).with_name("decision_tiers_handlers.py"))
        D = sys.modules["shop_decision_tiers_handlers"] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(D)
    return D


def listed(step, name, key):
    return [x.strip() for x in tiers().fields(step, name).get(key, "").strip("[]").split(",") if x.strip()]


@handler("GivenDoes", "enforce")
def given_enforces(step):
    """`the test t1 enforces the design-decision d1`: the test's id in the decision's `enforced_by`."""
    if step.subject.startswith("no "):
        return
    by, name = (tiers().bare(n) for n in step.names)
    D.field(step, name, "enforced_by", "[%s]" % ", ".join(listed(step, name, "enforced_by")
                                                          + [step.context["says"][by]]))


@handler("GivenDoes", "supersede")
def given_supersedes(step):
    new, old = (tiers().bare(n) for n in step.names)
    D.field(step, new, "supersedes", "[%s]" % ", ".join(listed(step, new, "supersedes") + ["design-decision/%s" % old]))


@handler("GivenDoes", "verify")
def given_verifies(step):
    """Only "no design-decision verifies the universal condition u1": no decision rests on it."""
    assert step.subject.startswith("no "), step.text


@handler("GivenK_A", "test")
def given_outcome(step):
    """`the test t1 is `failed``: its test asserts False; `passed`, it passes."""
    name = tiers().bare(step.names[0])
    failing = tiers().bare(step.values[0]) == "failed" and " is not " not in step.text
    D.write(step, "tests/test_%s.py" % name, D.source(step, name, failing=failing))


@handler("GivenK", "route")
def given_route(step):
    step.context.setdefault("routes", {})[step.names[0]] = OUTSIDE


@handler("GivenK_A", "route")
def given_route_kind(step):
    """The route's kind is the word under `verified_by`: "is v" that word, "is not v" a word outside the four when
    it was v."""
    route, value = step.names[0], tiers().bare(step.values[0])
    routes = step.context.setdefault("routes", {})
    if " is not " not in step.text:
        routes[route] = value
    elif routes.get(route) == value:
        routes[route] = OUTSIDE
    for name, has in step.context.get("routed", {}).items():
        if has == route:
            D.field(step, name, "verified_by", "[%s]" % routes[route])


@local("GivenDoes")
def given_has_route(step):
    """`the design-decision d1 has the route r1`: the decision written again as a judgement decision, clean in every
    other way, whose `verified_by` names the route; the error names it by its id."""
    if step.term != "has" or step.names[-1] not in step.context.get("routes", {}):
        return False
    name, route = tiers().bare(step.names[0]), step.names[1]
    D.decision(step, name, tier="judgement")
    D.field(step, name, "verified_by", "[%s]" % step.context["routes"][route])
    step.context.setdefault("routed", {})[name] = route
    D.says(step, name, "design-decision/%s/%s" % (D.PATH, name))


@local("ThenDoes")
def has_route(step):
    """After `work decision --verified-by`: the decision the run wrote names the route under `verified_by`."""
    if step.term != "has" or not re.search(r"\bthe route \S+$", step.text):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    path = step.repo / done.stdout.strip().splitlines()[-1].split()[-1]
    assert re.search(r"^verified_by: \[check\]$", path.read_text(), re.MULTILINE), path.read_text()


@local("ThenDoes")
def runs_pytest(step):
    """`model` runs `pytest` on the test: its id is on a `holds` or `failing` line, and the test ran."""
    if step.term != "run" or not step.context.get("decisions_run"):
        return False
    done, name = step.context["result"], tiers().bare(step.names[0])
    said = step.context["says"][name]
    assert any(line.startswith(("holds ", "failing ")) and said in line for line in done.stdout.splitlines()), \
        (said, done.stdout)
    assert name in (D.outside(step) / "ran").read_text().split(), done.stdout
