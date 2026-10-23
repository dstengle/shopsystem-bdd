"""design-model-check's Given steps for bounded contexts, capabilities, proposals and frontmatter references
(r24), and table rows and EARS lines (r3, r103, r104)."""

from pytest_bdd import given, parsers

from .conftest import CONTEXT, INDEX, cap, feature, full

# --- Given: bounded contexts and capabilities ------------------------------------------------------------------

@given("a bounded context with one capability whose requirement r1 has a scenario tagged @r1")
def context_with_good_capability(world):
    world.good()


@given("a bounded context with one capability")
def context_with_a_capability(world):
    world.good()


@given("a scenario tagged @r7 in a capability with no r7, and a capability resting on a decision that does not exist")
def dangling_references(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], rests_on="[nope]"))
    world.write("features/thing.feature", feature("thing", ("@r1", "one"), ("@r7", "seven")))


@given("an initiative citing an observation, with a capability-proposal that adds r1")
def initiative_with_proposal(world, context):
    world.good()
    world.observation()
    world.initiative()
    world.proposal(status="merged", adds="[thing#r1]")
    context["ref"] = "thing#r1"


@given("a requirement no capability-proposal adds or changes")
def requirement_without_proposal(world, context):
    world.good()
    context["ref"] = "capability/thing#r1"


@given(parsers.parse("a bounded context with id {ident} and a capability thing with requirement r2"))
def context_with_id_and_capability(world, ident):
    assert ident == CONTEXT
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two."]))


@given("a capability thing with requirements r1 to r3")
def capability_r1_to_r3(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two.", "- [r3] Three."], group="guarantees"))


@given("a capability thing with requirement r1 that lists r4 as retired")
def capability_with_retired(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", retired="[r4]"))


@given("a capability thing with requirement r2 that no scenario names")
def capability_unnamed_r2(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))


@given(parsers.re(r"a capability-proposal that (?P<change>adds|removes|changes) thing#(?P<rid>r\d+(?:-r\d+)?)"))
def proposal_naming(world, context, change, rid):
    if not (world.root / "spec/capabilities/thing.md").exists():  # r18: the capability is the proposal's to imply
        world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two.", "- [r3] Three."]))
    world.observation()
    world.initiative()
    world.proposal(**{change: "[thing#%s]" % rid})
    context["changed"] = rid


@given("a merged capability-proposal that adds thing#r4")
def merged_proposal_adding_retired(world, context):
    world.observation()
    world.initiative()
    world.proposal(status="merged", adds="[thing#r4]")
    context["changed"] = "r4"


@given("a merged capability-proposal that adds thing#r4 and removes thing#r4")
def merged_proposal_on_retired(world, context):
    world.observation()
    world.initiative()
    world.proposal(status="merged", adds="[thing#r4]", removes="[thing#r4]")
    context["changed"] = "r4"


@given(parsers.parse("a capability-proposal whose list names {reference}"))
def proposal_listing(world, context, reference):
    world.observation()
    world.initiative()
    world.proposal(adds="[%s]" % reference)
    context["listed"] = reference


@given("a glossary with the term store")
def glossary_with_store(world):
    world.good()
    world.write("spec/index.md", INDEX + "\n## Glossary\n- **store**: a place.\n")


@given(parsers.re(r"a (?P<status>\w+) capability-proposal whose (?P<field>adds|changes|removes) names term/(?P<term>\w+)"))
def proposal_naming_term(world, context, status, field, term):
    world.observation()
    world.initiative()
    world.proposal(status=status, **{field: "[term/%s]" % term})
    context["term"] = term


# --- Given: frontmatter references (r24) -----------------------------------------------------------------------

DECISION = "---\nid: %s\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n%s---\n\n## Decision\nWe do it.\n"


@given(parsers.parse("a file whose {field} names {target}"))
def file_naming(world, context, field, target):
    world.good()
    world.observation()
    world.initiative()
    if target == "a decision, where a capability is needed":
        world.write("spec/decisions/0001-x.md", DECISION % (full("design-decision", "ghost"), ""))
        world.work_item(under="design-decision/ghost")
    else:
        assert target == "an id nothing in the repository has"
        if field == "supersedes":
            world.write("spec/decisions/0001-x.md", DECISION % (full("design-decision", "x"), "supersedes: ghost\n"))
        elif field == "source":
            world.initiative(source="[observation/ghost]")
        elif field == "part_of":
            world.work_item(part_of="initiative/ghost")
        elif field == "argues":
            world.proposal(argues="[ghost]")
        elif field == "under":
            world.work_item(under="ghost")
        elif field == "for":
            world.work_item(**{"for": "work-item/ghost"})
        elif field == "blocked_by":
            world.work_item(blocked_by="work-item/ghost")
        else:
            assert field == "depends_on"
            world.work_item(depends_on="ghost")


# --- Given: table rows and EARS lines (r3, r103, r104) --------------------------------------------------------------

@given("a capability whose Behaviour has a ### heading, a lead sentence, and a table with a header row, a separator "
       "and rows marked [r1] and [r2]")
def capability_with_table(world):
    world.write("spec/capabilities/thing.md", cap("thing", [
        "### Reports", "",
        "**If** `thing` finds a case of a row below, then `thing` shall report it.", "",
        "| id | what is reported |", "|---|---|", "| [r1] | one |", "| [r2] | two |"]))


@given(parsers.parse("a scenario tagged @r2"))
def scenario_tagged_r2(world):
    world.write("features/thing.feature", feature("thing", ("@r2", "two")))


@given("a capability that lists r1 as retired and has a requirement [r1]")
def capability_reusing_retired(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], retired="[r1]"))


@given(parsers.parse("a scenario in {path} with the tag @r2 {placed}"))
def scenario_placed(world, path, placed):
    text = feature("thing", ("@r2", "two"))
    if placed == "on its feature":
        text = text.replace("Feature: thing", "@r2\nFeature: thing").replace("  @r2\n  Scenario", "  Scenario")
    world.write(path, text)


@given("a capability thing with requirement r2")
def capability_r2(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))


@given("its only scenario tagged @r2 is also tagged @deprecated")
def scenario_deprecated(world):
    world.write("features/thing.feature", feature("thing", ("@r2 @deprecated", "two")))


@given("a capability thing with requirements r1 and r2")
def capability_r1_r2(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two."]))


@given("a glossary term store that avoids shelf")
def glossary_store(world):
    world.write("spec/index.md", INDEX + "\n## Glossary\n- **store**: a place. Not: shelf.\n")


@given('requirements that say "the Store", "the stores", "restore" and "a shelf and a store-front"')
def requirements_saying(world):
    lines = ["the Store", "the stores", "restore", "a shelf and a store-front"]
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r%d] %s." % (n, t) for n, t in enumerate(lines, 1)]))


@given('a scenario whose steps say "a shelf" and another whose title says "the store"')
def scenarios_saying(world):
    world.write("features/thing.feature", "Feature: thing\n\n  Scenario: first\n    Given a shelf\n\n"
                "  Scenario: the store\n    Given a thing\n")


@given("a capability whose Behaviour has a table whose row is marked r1 without brackets")
def capability_with_unbracketed_row(world):
    world.write("spec/capabilities/thing.md", cap("thing", [
        "**When** asked, `thing` shall answer as the rows say:", "", "| id | what |", "|---|---|", "| r1 | one |"]))


@given("a capability whose Behaviour has a table led by a good sentence, a ### heading, and a second table with a row "
       "marked [r2] and no lead")
def capability_with_two_tables(world):
    world.write("spec/capabilities/thing.md", cap("thing", [
        "**When** asked, `thing` shall answer as the rows say:", "", "| id | what |", "|---|---|", "| [r1] | one |", "",
        "### More", "", "| id | what |", "|---|---|", "| [r2] | two |"]))


@given("a capability whose Behaviour has these lines")
def capability_with_lines(world, datatable):
    rows = datatable[1:]
    world.write("spec/capabilities/thing.md", cap("thing", ["- [%s] %s" % (r[0], r[1]) for r in rows]))


@given("a capability whose Behaviour has a table with rows marked [r1] and [r2], led by a sentence that names no system")
def capability_with_unled_table(world):
    world.write("spec/capabilities/thing.md", cap("thing", [
        "Each row below is reported.", "", "| id | what |", "|---|---|", "| [r1] | one |", "| [r2] | two |"]))
