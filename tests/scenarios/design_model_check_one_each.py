"""design-model-check's steps for what each scenario and work-item must name: a scenario one requirement (r107,
v_s2) and a work-item its acceptance or check (r106, v_w4)."""

from pytest_bdd import given, parsers, then

from .conftest import feature
from .design_model_check_then import found

SCENARIO = "features/thing.feature:one"


@given(parsers.re(r"in features/thing.feature a scenario tagged (?P<tags>@r1(?: @r2)?(?: @deprecated)?)"
                  r"(?P<feature_tag>, in a feature tagged @r2)?"))
def scenario_tagged(world, tags, feature_tag):
    text = feature("thing", (tags, "one"))
    if feature_tag:
        text = text.replace("Feature: thing", "@r2\nFeature: thing")
    world.write("features/thing.feature", text)


@then(parsers.re(r"the scenario is (?P<printed>printed|not printed) under v_s2"))
def scenario_under_v_s2(world, context, printed):
    rows = [a[0] for name, a in found(world, context)["violations"] if name == "v_s2"]
    assert (SCENARIO in rows) == (printed == "printed"), found(world, context)
