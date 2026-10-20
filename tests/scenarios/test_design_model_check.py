"""features/design-model-check.feature, bound to scripts/model: the scenarios of requirements r1, r9, r12, r13,
r16-r18, r21-r25 and r27-r32. (The rest are bound by the work-items that follow.)

A Given builds the repository in `world` (see conftest); the When runs `model` once; the Then steps read what it
printed. The checks that read the findings as data (`check --json`) run it a second time, on demand.
"""
import os
import re
import sys

from pytest_bdd import given, parsers, scenario, then, when

from .conftest import CONTEXT, INDEX, I1, P1, THING, cap, feature, full

FEATURE = "design-model-check.feature"
BOUND = (
    'a repository the grammar accepts passes',
    'references that name nothing are reported',
    'without clingo the check says how to install it',
    "facts are printed in clingo's syntax",
    "why traces a requirement to its initiative's sources",
    'why with no proposal says so',
    'a range of ids stands for each id in it',
    "a reference written name#r<n> is that capability's requirement",
    'a reference in neither requirement form, or a reversed range, is unresolved',
    'a proposal adding or removing a requirement no capability has is unresolved, unless it adds a retired id',
    'a frontmatter reference to nothing, or to the wrong kind, is unresolved',
    'a malformed index or capability file is a file problem',
    'a malformed work directory or work file is a file problem',
    'a work-item accepting a requirement no scenario names is a file problem',
    'a malformed decision, record or frontmatter is a file problem',
    'file problems are each printed and fail the check',
    'the check ends with the four counts',
    'rows of a violated relation are limited, saying how many more there are',
    "a scenario names a requirement by its tag in its capability's feature file",
    'a held scenario names no requirement',
    'a scenario tagged with several requirements names each of them',
    'a mention is a whole word in any case, plural allowed',
    'a code span, a double-quoted string and a tag are no mention',
    "a Behaviour line in none of EARS's patterns is v_e1",
    'a table row is checked by its lead sentence',
    'a Behaviour line with two shalls or two sentences is v_e2',
    'a table row whose id lost its brackets is a line with no id',
    'a table is led only by the sentence just before it',
    'a retired id used again is refused',
    'a merged capability-proposal may add or remove an id its capability lists as retired',
    'a table row with an id is a requirement, and its header, separator and lead sentence are not',
)

# HIDE_CLINGO on PYTHONPATH hides clingo from an interpreter, as the fixture harness does.
HIDE_CLINGO = 'raise ImportError("clingo is hidden for this test")\n'


def _test_name(title):
    """The test's name, from its scenario's title (a scenario may name several requirements, so not from a tag)."""
    return "test_" + re.sub(r"\W+", "_", title).strip("_").lower()


def _bind(title):
    def test():
        pass
    test.__name__ = _test_name(title)
    return scenario(FEATURE, title)(test)


for _title in BOUND:
    globals()[_test_name(_title)] = _bind(_title)


def found(world, context):
    """`check --json` of the repository, run once."""
    if "found" not in context:
        context["found"], _ = world.check_json()
    return context["found"]


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


@given("an interpreter without the clingo package")
def no_clingo(world, repo, context):
    world.good()
    world.write("hidden/clingo.py", HIDE_CLINGO)
    env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_MODEL_PYTHON", "SHOPSYSTEM_MODEL_REEXEC")}
    env.update(PYTHONPATH=str(repo / "hidden"), PATH=str(repo / "empty"))
    context["env"] = env


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


# --- Given: frontmatter references (r24) -----------------------------------------------------------------------

DECISION = "---\nid: %s\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n%s---\n"


@given(parsers.parse("a file whose {field} names {target}"))
def file_naming(world, context, field, target):
    world.good()
    world.observation()
    world.initiative()
    if target == "a decision, where a capability is needed":
        world.write("decisions/0001-x.md", DECISION % (full("design-decision", "ghost"), ""))
        world.work_item(under="design-decision/ghost")
    else:
        assert target == "an id nothing in the repository has"
        if field == "supersedes":
            world.write("decisions/0001-x.md", DECISION % (full("design-decision", "x"), "supersedes: ghost\n"))
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


# --- Given: file problems (r25, r27-r30) -----------------------------------------------------------------------

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
    else:
        assert case == "spec/capabilities/thing.md lists retired: [three]", case
        world.write("spec/capabilities/thing.md", capfile(retired="[three]"))


def _initiative_with(world, old, new):
    p = world.root / "work/i1/initiative.md"
    p.write_text(p.read_text().replace(old, new))


@given(parsers.parse("a repository with a work directory work/i1 in which {case}"))
def malformed_work(world, case):
    def part(**changes):
        fm = {"id": full("work-item", "p1"), "kind": "work-item", "part_of": "initiative/i1", "status": "drafted",
              "under": "thing", "check": "true"}
        fm.update(changes)
        world.write("work/i1/p1.md", "---\n" + "".join("%s: %s\n" % (k, v) for k, v in fm.items() if v is not None) + "---\n")
    world.good()
    if case == "there is no initiative.md":
        part()
        return
    world.initiative()
    if case == "initiative.md has no id":
        _initiative_with(world, "id: %s\n" % I1, "")
    elif case == "the part p1.md has no id":
        part(id=None)
    elif case == "the part p1.md has the kind banana":
        part(kind="banana")
    elif case == "the part p1.md has no status":
        part(status=None)
    elif case == "the part p1.md has a status not in its kind's lifecycle":
        part(status="loved")
    elif case == "initiative.md has the priority high":
        _initiative_with(world, "priority: 1", "priority: high")
    else:
        assert case == "initiative.md has a date written 16/10/2026", case
        _initiative_with(world, "date: 2026-10-15", "date: 16/10/2026")


@given("a work-item in work/i1/w1.md that accepts thing#r2")
def work_item_accepting(world, context):
    world.observation()
    world.initiative()
    world.work_item(accepts="[thing#r2]")
    context["mentions"] = THING + "#r2"


@given(parsers.parse("a repository in which {case}"))
def malformed_record(world, context, case):
    x = full("design-decision", "x")
    decision = "---\nid: {}\nsummary: {}\ndate: 2026-01-01\nstatus: accepted\n---\n"
    world.good()
    if case == "a decision under decisions/ has no id":
        world.write("decisions/0001-x.md", "---\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n")
    elif case == "a record under records/ with an id has the kind banana":
        world.write("records/note.md", "---\nid: %s\nkind: banana\n---\n" % full("review-finding", "n1"))
    elif case == "a frontmatter value is written as a folded block, with >":
        world.write("decisions/0001-x.md", decision.format(x, ">-\n  folded"))
    elif case == "a frontmatter value is written as a literal block, with |":
        world.write("decisions/0001-x.md", decision.format(x, "|\n  literal"))
    else:
        assert case == "a decision and an observation have the same id", case
        world.write("decisions/0001-x.md", decision.format(x, "S"))
        world.write("records/observations.md", "# Observations\n\n## %s\nabout: %s\n" % (x, CONTEXT))
        context["same_id"] = x


@given("a repository with two capabilities that each have no ## Behaviour section")
def two_capabilities_without_behaviour(world):
    for name in ("thing", "other"):
        world.write("spec/capabilities/%s.md" % name,
                    cap(name, ["- [r1] One."], group="guarantees").replace("## Behaviour", "## Requirements"))


# --- Given: the counts and the row limit (r31, r32) -------------------------------------------------------------

@given("a repository with one violation, one warning, one unresolved reference and one file problem")
def one_of_each(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."], rests_on="[nope]"))
    world.write("features/stray.feature", "Feature: stray\n")


@given(parsers.parse("a repository with {rows:d} requirements no scenario names"))
def unscenarioed(world, context, rows):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r%d] Req %d." % (n, n) for n in range(1, rows + 1)]))
    context["rows"] = rows


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


@given(parsers.parse("a capability thing with requirement r2, {formulated}"))
def capability_formulated_as(world, context, formulated):
    line = "formulated_as: " + formulated.split(" ", 1)[1] if formulated.startswith("formulated_as ") else None
    text = cap("thing", ["- [r2] Two."])
    text = text.replace("formulated_as: features/thing.feature\n", (line + "\n") if line else "")
    world.write("spec/capabilities/thing.md", text)


@given(parsers.parse("a scenario in {path} with the tag @r2 {placed}"))
def scenario_placed(world, path, placed):
    text = feature("thing", ("@r2", "two"))
    if placed == "on its feature":
        text = text.replace("Feature: thing", "@r2\nFeature: thing").replace("  @r2\n  Scenario", "  Scenario")
    world.write(path, text)


@given("a capability thing with requirement r2")
def capability_r2(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r2] Two."]))


@given("its only scenario tagged @r2 is also tagged @holding")
def scenario_held(world):
    world.write("features/thing.feature", feature("thing", ("@r2 @holding", "two")))


@given("a capability thing with requirements r1 and r2")
def capability_r1_r2(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One.", "- [r2] Two."]))


@given("a scenario tagged @r1 @r2")
def scenario_tagged_both(world):
    world.write("features/thing.feature", feature("thing", ("@r1 @r2", "both")))


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


# --- When ------------------------------------------------------------------------------------------------------

@when("model check is run")
def model_check(world, context):
    if "env" in context:  # r12: the interpreter that cannot import clingo, and no other on the PATH
        context["result"] = world.model("check", env=context["env"], timeout=60)
    else:
        context["result"] = world.model("check")


@when("model check is run without --json")
def model_check_plain(world, context):
    context["result"] = world.model("check")


@when(parsers.re(r"model check is run (?P<limit>with --limit \d+|with no --limit)"))
def model_check_limited(world, context, limit):
    args = [] if limit == "with no --limit" else ["--limit", limit.rsplit(" ", 1)[1]]
    context["result"] = world.model("check", *args)


@when("model facts is run")
def model_facts(world, context):
    context["result"] = world.model("facts", python=[sys.executable, "-I", "-S"])


@when(parsers.parse("model why is run for {ref}"))
def model_why(world, context, ref):
    if ref in ("that requirement", "it"):
        ref = context["ref"]
    context["result"] = world.model("why", ref)


# --- Then ------------------------------------------------------------------------------------------------------

@then(parsers.parse("it exits {code:d}"))
def exits(context, code):
    result = context["result"]
    assert result.returncode == code, result.stdout + result.stderr
    assert "Traceback" not in result.stderr


@then("it reports 0 violations, 0 unresolved references and 0 file problems")
def reports_nothing(context):
    out = context["result"].stdout
    assert "0 violations" in out
    assert "0 unresolved references, 0 file problems" in out


@then(parsers.re(r"the output names (?P<code>v15[ac])"))
def output_names_code(world, context, code):
    assert code in [name for name, _ in found(world, context)["violations"]], found(world, context)


@then("thing#r4 is reported neither under v15c nor as unresolved")
def r4_not_reported(world, context):
    data = found(world, context)
    assert [d for d in data["unresolved"] if "thing#r4" in d] == [], data
    assert [a for name, a in data["violations"] if name in ("v15c", "v15d") and "thing#r4" in a[0]] == [], data


@then(parsers.re(r"the requirement thing#r2 is (?P<reported>not|still|reported) (?:reported )?under v_s3"))
def r2_under_v_s3(world, context, reported):
    rows = [a[0] for name, a in found(world, context)["violations"] if name == "v_s3"]
    assert (THING + "#r2" in rows) == (reported != "not"), found(world, context)


@then("neither thing#r1 nor thing#r2 is reported under v_s3")
def neither_under_v_s3(world, context):
    rows = [a[0] for name, a in found(world, context)["violations"] if name == "v_s3"]
    assert rows == [], found(world, context)


@then("it reports no file problem")
def no_file_problem(world, context):
    assert found(world, context)["problems"] == []


def _mentions(context):
    facts = context["result"].stdout
    return [m.groups() for m in re.finditer(r'^mentions\("([^"]*)", "([^"]*)"\)\.$', facts, re.M)]


@then('"the Store" and "the stores" each mention store')
def stores_mentioned(context):
    mentioned = _mentions(context)
    assert (THING + "#r1", "store") in mentioned and (THING + "#r2", "store") in mentioned, mentioned


@then('"restore" and "store-front" mention nothing')
def restore_mentions_nothing(context):
    # "store-front" is in the requirement that also says "a shelf", which mentions shelf (next Then): so, nothing about store
    mentioned = _mentions(context)
    assert not [m for m in mentioned if m[0] == THING + "#r3"], mentioned
    assert (THING + "#r4", "store") not in mentioned, mentioned


@then('the requirement and the scenario saying "a shelf" each mention shelf')
def shelf_mentioned(context):
    mentioned = _mentions(context)
    assert (THING + "#r4", "shelf") in mentioned, mentioned
    assert ("features/thing.feature:first", "shelf") in mentioned, mentioned


@then("only r4 mentions shelf")
def only_r4_mentions_shelf(context):
    assert [m[0] for m in _mentions(context) if m[1] == "shelf"] == [THING + "#r4"], _mentions(context)


@then("it reports no file problem and no v_s2")
def no_file_problem_and_no_v_s2(world, context):
    data = found(world, context)
    assert data["problems"] == [], data
    assert [a for name, a in data["violations"] if name == "v_s2"] == [], data


@then("it reports no file problem and no v15a")
def no_file_problem_and_no_v15a(world, context):
    data = found(world, context)
    assert data["problems"] == [], data
    assert [a for name, a in data["violations"] if name == "v15a"] == [], data


@then("thing#r1 is reported under v_s3 and thing#r2 is not")
def r1_but_not_r2_under_v_s3(world, context):
    data = found(world, context)
    rows = [a[0] for name, a in data["violations"] if name == "v_s3"]
    assert THING + "#r1" in rows and THING + "#r2" not in rows, data


def _named(world, context, code):
    return {a[0].rsplit("#", 1)[1] for name, a in found(world, context)["violations"] if name == code}


@then(parsers.re(r"(?P<code>v_e[12]) names (?P<ids>r\d+(?:(?:, | and )r\d+)*)"))
def names_requirements(world, context, code, ids):
    assert _named(world, context, code) == set(re.findall(r"r\d+", ids)), found(world, context)


@then(parsers.re(r"(?P<code>v_e[12]) does not name (?P<ids>r\d+(?:(?:, | or )r\d+)*)"))
def does_not_name_requirements(world, context, code, ids):
    assert not _named(world, context, code) & set(re.findall(r"r\d+", ids)), found(world, context)


@then(parsers.re(r"(?P<subject>.+?) is reported as unresolved"))
def reported_unresolved(world, context, subject):
    out = context["result"].stdout
    if subject == "each":  # r9
        assert "unresolved: features/thing.feature: scenario 'seven' names %s#r7" % THING in out
        assert "unresolved: spec/capabilities/thing.md: %s is not a design-decision" % full("design-decision", "nope") in out
    elif subject.startswith("that "):  # r24: the field named in the Given's example row
        data = found(world, context)
        assert len([d for d in data["unresolved"] if "ghost" in d]) == 1, data
    elif "listed" in context:  # r22
        ref = context["listed"]
        assert subject == ref
        data = found(world, context)
        assert len([d for d in data["unresolved"] if "'%s' is not a requirement reference" % ref in d]) == 1, data
    else:  # r23
        data = found(world, context)
        rid = context["changed"]
        assert subject == "thing#" + rid
        unresolved = [d for d in data["unresolved"] if "%s#%s" % (THING, rid) in d]
        v15c = [a for name, a in data["violations"] if name == "v15c" and a == ["%s#%s" % (THING, rid)]]
        assert (len(unresolved), v15c) == (1, []), data


@then(parsers.re(r"(?P<subject>.+?) is reported under v15c and not as unresolved"))
def reported_v15c(world, context, subject):
    data = found(world, context)
    rid = context["changed"]
    assert subject == "thing#" + rid
    unresolved = [d for d in data["unresolved"] if "%s#%s" % (THING, rid) in d]
    v15c = [a for name, a in data["violations"] if name == "v15c" and a == ["%s#%s" % (THING, rid)]]
    assert (unresolved, len(v15c)) == ([], 1), data


@then(parsers.parse("it names clingo and the pip command that installs it"))
def names_clingo(context):
    out = context["result"].stdout
    assert "clingo" in out
    assert "-m pip install clingo" in out


@then("each line is one fact, such as a node fact for the capability")
def facts_are_clingo(context):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert 'node("%s", "capability").' % THING in lines
    assert 'req_id("%s#r1", "%s", 1).' % (THING, THING) in lines
    assert all(re.fullmatch(r"\w+\(.*\)\.", l) for l in lines)


@then("it prints the requirement, the proposal, the initiative and the observation")
def why_traces(context):
    result = context["result"]
    assert result.returncode == 0, result.stdout + result.stderr
    assert "%s#r1: **When** asked, `thing` shall answer." % THING in result.stdout
    assert "adds by capability-proposal %s (merged, 2026-10-15)" % P1 in result.stdout
    assert "part_of initiative %s" % I1 in result.stdout
    assert "source observation %s" % full("observation", "obs-1") in result.stdout


@then("it says no capability-proposal adds or changes it")
def why_without_proposal(context):
    assert "no capability-proposal adds or changes it" in context["result"].stdout


@then("it prints the proposal as adding it")
def why_range(context):
    result = context["result"]
    assert result.returncode == 0, result.stdout
    assert "adds by capability-proposal %s" % P1 in result.stdout


@then(parsers.parse("it prints capability/ex.com/prod/ctx/thing#r2 with its text and the proposal as adding it"))
def why_by_name(context):
    result = context["result"]
    assert result.returncode == 0, result.stdout
    assert "%s#r2: Two." % THING in result.stdout
    assert "adds by capability-proposal %s" % P1 in result.stdout


@then(parsers.parse("it reports a file problem naming {named}"))
def file_problem_named(world, context, named):
    data = found(world, context)
    named, _, absent = named.partition(", and not ")
    count = len([p for p in data["problems"] if p.startswith(named)])
    if "mentions" in context:  # r28: and the requirement the work-item accepts
        count = len([p for p in data["problems"] if p.startswith(named) and context["mentions"] in p])
    assert count == 1, data
    if absent:
        assert not any(absent in p for p in data["problems"]), data


@then("it reports a file problem")
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
    assert len(re.findall(pattern, out, re.M)) == 2, out


@then("it prints the four counts, each 1")
def four_counts(context):
    out = context["result"].stdout
    assert "1 violations, 1 warnings, 1 unresolved references, 1 file problems" in out.splitlines()[-1], out


def _v_s3_rows(context):
    out = context["result"].stdout
    m = re.search(r"^v_s3  \(%d\)\n((?:    .*\n)+)" % context["rows"], out, re.M)
    assert m, out
    return m.group(1).splitlines(), out


@then(parsers.parse("it prints {shown:d} rows under v_s3"))
def rows_shown(context, shown):
    lines, out = _v_s3_rows(context)
    assert len([l for l in lines if THING + "#r" in l]) == shown, out


@then(parsers.parse("it says there are {more:d} more"))
def rows_more(context, more):
    lines, _ = _v_s3_rows(context)
    assert "    ... and %d more" % more in lines
