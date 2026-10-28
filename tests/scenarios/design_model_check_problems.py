"""design-model-check's file problems (r25, r27-r30) and what the check prints and refuses (r2-r11, r33-r35)."""
import re

from pytest_bdd import given, parsers, then

from .conftest import CONTEXT, I1, P1, THING, cap, feature, full
from .design_model_check_then import found

# --- Given: file problems (r25, r27-r30) -----------------------------------------------------------------------

@given(parsers.parse("a feature file {path} in which {titles}"))
def feature_file_with(world, context, path, titles):
    world.good()
    one = feature("thing", ("@r1", "one"))
    if titles.startswith("every scenario"):
        text = one
    elif titles.startswith("two scenarios are titled"):
        second = "@deprecated" if "@deprecated" in titles else "@r1"
        text = feature("thing", ("@r1", "Apply a code"), (second, "Apply a code"))
    elif titles == "a scenario is tagged @deprecated and @holding":
        text = feature("thing", ("@r1", "one"), ("@deprecated @holding", "another"))
    else:
        assert titles == "a scenario with its own title is tagged @holding", titles
        text = feature("thing", ("@r1", "one"), ("@holding", "another"))
    world.write("features/thing.feature", one)
    world.write(path, text)


@given(parsers.parse("a decision whose source is {source} and whose by is {by}"))
def decision_source(world, context, source, by):
    world.good()
    world.observation()
    if not source.startswith("["):
        source = '"%s"' % source
    world.write("spec/decisions/0001-x.md",
                "---\nid: %s\nsummary: S\ndate: 2026-01-01\nstatus: accepted\nsource: %s\nby: \"%s\"\n---\n\n## Decision\nWe do it.\n"
                % (full("design-decision", "x"), source, by))


@given(parsers.parse("a bounded context with id bounded-context/acme.com/shop/cart in which {case}"))
def malformed_index_or_capability(world, case):
    def capfile(ident="capability/acme.com/shop/cart/thing", behaviour=True, retired="[]"):
        text = cap("thing", ["- [r1] One."], group="guarantees", retired=retired).replace("id: " + THING, "id: " + ident)
        return text if behaviour else text.replace("## Behaviour", "## Requirements")
    world.write("spec/index.md", "---\nid: bounded-context/acme.com/shop/cart\n---\n")
    if case == "spec/index.md is missing":
        (world.root / "spec/index.md").unlink()
    elif case == "spec/index.md has no id":
        world.write("spec/index.md", "---\ntitle: x\n---\n")
    elif case == "spec/capabilities/thing.md has the id capability/acme.com/shop/cart/other":
        world.write("spec/capabilities/thing.md", capfile("capability/acme.com/shop/cart/other"))
    elif case == "spec/capabilities/thing.md has no ## Behaviour section":
        world.write("spec/capabilities/thing.md", capfile(behaviour=False))
    elif case == "spec/capabilities/thing.md lists retired: [three]":
        world.write("spec/capabilities/thing.md", capfile(retired="[three]"))
    else:
        assert case == "spec/capabilities/thing.md has formulated_as: features/thing.feature", case
        world.write("spec/capabilities/thing.md",
                    capfile().replace("retired: []\n", "retired: []\nformulated_as: features/thing.feature\n"))


@given(parsers.parse("a bounded context the grammar accepts, with {path} at its root"))
def old_layout_path(world, path):
    world.good()
    if path.endswith("/"):
        world.write(path + "README.md", "# old\n")
    else:
        world.write(path, "# Decisions\n")


def _initiative_with(world, old, new):
    p = world.root / ".shop/work/i1/initiative.md"
    p.write_text(p.read_text().replace(old, new))


@given("a repository with two capabilities that each have no ## Behaviour section")
def two_capabilities_without_behaviour(world):
    for name in ("thing", "other"):
        world.write("spec/capabilities/%s.md" % name,
                    cap(name, ["- [r1] One."], group="guarantees").replace("## Behaviour", "## Requirements"))


def _problems_naming(data, named):
    """The file problems that begin with the path `named` as a whole word (`.shop/work/i1:`, not `.shop/work/i1/p1.md:`)."""
    return [p for p in data["problems"] if re.match(re.escape(named) + r"[: ]", p)]


@then(parsers.parse("it prints a file problem naming {named}"))
def file_problem_named(world, context, named):
    data = found(world, context)
    if named.endswith(" and scripts/migrate"):  # r61: an old layout's path, named with the script that moves it
        path = named[: -len(" and scripts/migrate")]
        assert _problems_naming(data, path) == ["%s: the layout has no %s; run scripts/migrate" % (path, path)], data
        return
    named, _, absent = named.partition(", and not ")
    # r110's problems (a work-item's file name, a held id) answer another line, not counted here, unless the file is a w<n>.md
    r110 = not re.search(r"/w\d+\.md$", named)
    mine = [p for p in _problems_naming(data, named)
            if not (r110 and ("a work-item's file is named w<n>.md" in p or "is already held by" in p))]
    count = len(mine)
    if "mentions" in context:  # r28: and the requirement the work-item accepts
        count = len([p for p in mine if context["mentions"] in p])
    assert count == 1, data
    if absent:
        assert not any(absent in p for p in data["problems"]), data


@then(parsers.parse("it prints no file problem naming {named}"))
@then(parsers.parse("it does not print a file problem naming {named}"))
def no_file_problem_named(world, context, named):
    data = found(world, context)
    assert not _problems_naming(data, named), data


@then(parsers.re(r"the decision's source is (?P<reported>not printed|printed) as unresolved"))
def decisions_source_unresolved(world, context, reported):
    data = found(world, context)
    mine = [d for d in data["unresolved"] if d.startswith("spec/decisions/0001-x.md")]
    assert bool(mine) == (reported == "printed"), data
    assert not any("ghost" in d for d in data["unresolved"]) or reported == "printed", data


@then("it prints a file problem")
def file_problem(world, context):
    data = found(world, context)
    if "same_id" in context:  # a type-first id names its kind, so the observation's heading is also not an observation id (r46)
        assert len([p for p in data["problems"] if "%s is both" % context["same_id"] in p]) == 1, data
    else:
        assert len(data["problems"]) == 1, data


@then("it prints a file problem for each of the two capabilities")
def file_problems_printed(context):
    out = context["result"].stdout
    pattern = r"^file: spec/capabilities/(thing|other)\.md: no '## Behaviour' section$"
    assert len(re.findall(pattern, out, re.MULTILINE)) == 2, out


# === what the check prints, and the refusals (r2-r11, r33-r35) ======================================================

@given("a bounded context with a requirement no scenario names")
def requirement_no_scenario_names(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))


@then("the output names v_s3 with its plain label and the requirement's id")
def output_names_v_s3(context):
    out = context["result"].stdout
    assert re.search(r"v_s3  a requirement has no scenario  \(1\)\n\s+" + re.escape(THING + "#r1"), out), out


@given("a capability whose Behaviour has a bullet with no [r<n>]")
def bullet_without_id(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- **When** asked, `thing` shall answer."], group="guarantees"))


@given("a capability whose Behaviour has two bullets marked [r1]")
def two_bullets_r1(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r1] Two."], group="guarantees"))


@given("a capability-proposal that changes r9 of a capability with no r9")
def proposal_changing_r9(world):
    world.good()
    world.observation()
    world.initiative()
    world.proposal(changes="[thing#r9]")


@then("the output names v15e with the proposal and the requirement")
def output_names_v15e(context):
    out = context["result"].stdout
    assert re.search(r"v15e  a proposal changes a requirement no capability has  \(1\)\n\s+" + re.escape("%s, %s#r9" % (P1, THING)), out), out


@given("a capability-proposal with status formulated that adds a requirement no scenario names")
def formulated_proposal_unscenarioed(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."]))
    world.observation()
    world.initiative()
    world.proposal(status="formulated", adds="[thing#r1]")


@then("the output names v15f with the proposal")
def output_names_v15f(context):
    out = context["result"].stdout
    assert re.search(r"v15f  a formulated proposal leaves a requirement without a scenario  \(1\)\n\s+" + re.escape(P1), out), out


@given("a capability in the guarantees group whose requirements no scenario names")
def guarantees_unscenarioed(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] `thing` shall be fast."], group="guarantees"))


@then("the output does not name v_s3")
def output_without_v_s3(context):
    assert "v_s3" not in context["result"].stdout, context["result"].stdout


@given("a work-item whose part_of names nothing")
def work_item_reaching_nothing(world):
    world.good()
    world.observation()
    world.initiative()
    world.work_item(part_of="initiative/nowhere")


@then("the output names v9c with the work-item")
def output_names_v9c(context):
    out = context["result"].stdout
    assert re.search(r"v9c  a part reaches no initiative  \(1\)\n\s+" + re.escape(full("work-item", "w1")), out), out


@given("a bounded context the grammar accepts, with an observation no initiative cites")
def uncited_observation(world):
    world.good()
    world.observation()


@then("the output gives w_uncited_obs with its plain label and its count")
def output_gives_warning(context):
    out = context["result"].stdout
    assert "warning w_uncited_obs  an observation no initiative cites  (1)" in out, out
