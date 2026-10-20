"""features/design-model-check.feature, bound to scripts/model: every scenario of the file, by `scenarios()`.

A Given builds the repository in `world` (see conftest); the When runs `model` once; the Then steps read what it
printed. The checks that read the findings as data (`check --json`) run it a second time, on demand.
"""
import os
import re
import subprocess
import sys

from pytest_bdd import given, parsers, scenarios, then, when

from .conftest import CONTEXT, INDEX, I1, OBS1, P1, PATH, SCRIPTS, THING, cap, feature, full

scenarios("design-model-check.feature")

# HIDE_CLINGO on PYTHONPATH hides clingo from an interpreter, as the fixture harness does.
HIDE_CLINGO = 'raise ImportError("clingo is hidden for this test")\n'


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


@given(parsers.parse("a repository with a work directory .shop/work/i1 in which {case}"))
def malformed_work(world, case):
    def part(**changes):
        fm = {"id": full("work-item", "p1"), "kind": "work-item", "part_of": "initiative/i1", "status": "drafted",
              "under": "thing", "check": "true"}
        fm.update(changes)
        world.write(".shop/work/i1/p1.md", "---\n" + "".join("%s: %s\n" % (k, v) for k, v in fm.items() if v is not None) + "---\n")
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


@given("a work-item in .shop/work/i1/w1.md that accepts thing#r2")
def work_item_accepting(world, context):
    world.observation()
    world.initiative()
    world.work_item(accepts="[thing#r2]")
    context["mentions"] = THING + "#r2"


@given(parsers.parse("a repository in which {case}"))
def malformed_record(world, context, case):
    x = full("design-decision", "x")
    decision = "---\nid: {}\nsummary: {}\ndate: 2026-01-01\nstatus: accepted\n---\n\n## Decision\nWe do it.\n"
    world.good()
    if case == "a decision under spec/decisions/ has no id":
        world.write("spec/decisions/0001-x.md", "---\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n\n## Decision\nWe do it.\n")
    elif case == "a decision under spec/decisions/ has no ## Decision section":
        world.write("spec/decisions/0001-x.md", "---\nid: %s\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n\nNo section.\n" % x)
    elif case == "a record under .shop/records/ with an id has the kind banana":
        world.write(".shop/records/note.md", "---\nid: %s\nkind: banana\n---\n" % full("review-finding", "n1"))
    elif case == "a frontmatter value is written as a folded block, with >":
        world.write("spec/decisions/0001-x.md", decision.format(x, ">-\n  folded"))
    elif case == "a frontmatter value is written as a literal block, with |":
        world.write("spec/decisions/0001-x.md", decision.format(x, "|\n  literal"))
    else:
        assert case == "a decision and an observation have the same id", case
        world.write("spec/decisions/0001-x.md", decision.format(x, "S"))
        world.write(".shop/records/observations.md", "# Observations\n\n## %s\nabout: %s\n" % (x, CONTEXT))
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


@then(parsers.re(r"the output names (?P<code>v15[abc])"))
def output_names_code(world, context, code):
    assert code in context["result"].stdout, context["result"].stdout
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
    elif "written" in context:  # r43, r24
        _written_unresolved(world, context, subject)
    elif "term" in context:  # r66
        assert subject == "term/" + context["term"]
        assert _term_unresolved(world, context), found(world, context)
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


def _term_unresolved(world, context):
    """The unresolved entries naming the term the Given's proposal lists."""
    return [d for d in found(world, context)["unresolved"] if context["term"] in d and "p1.md" in d]


@then(parsers.re(r"(?P<subject>term/\w+) is not reported as unresolved"))
def term_not_reported_unresolved(world, context, subject):
    assert subject == "term/" + context["term"]
    assert not _term_unresolved(world, context), found(world, context)


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


def _problems_naming(data, named):
    """The file problems that begin with the path `named` as a whole word (`.shop/work/i1:`, not `.shop/work/i1/p1.md:`)."""
    return [p for p in data["problems"] if re.match(re.escape(named) + r"[: ]", p)]


@then(parsers.parse("it reports a file problem naming {named}"))
def file_problem_named(world, context, named):
    data = found(world, context)
    if named.endswith(" and scripts/migrate"):  # r61: an old layout's path, named with the script that moves it
        path = named[: -len(" and scripts/migrate")]
        assert _problems_naming(data, path) == ["%s: the layout has no %s; run scripts/migrate" % (path, path)], data
        return
    named, _, absent = named.partition(", and not ")
    count = len(_problems_naming(data, named))
    if "mentions" in context:  # r28: and the requirement the work-item accepts
        count = len([p for p in _problems_naming(data, named) if context["mentions"] in p])
    assert count == 1, data
    if absent:
        assert not any(absent in p for p in data["problems"]), data


@then(parsers.parse("it does not report a file problem naming {named}"))
def no_file_problem_named(world, context, named):
    data = found(world, context)
    assert not _problems_naming(data, named), data


@then(parsers.re(r"the decision's source is (?P<reported>not reported|reported) as unresolved"))
def decisions_source_unresolved(world, context, reported):
    data = found(world, context)
    mine = [d for d in data["unresolved"] if d.startswith("spec/decisions/0001-x.md")]
    assert bool(mine) == (reported == "reported"), data
    assert not any("ghost" in d for d in data["unresolved"]) or reported == "reported", data


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
    m = re.search(r"^v_s3  a requirement has no scenario  \(%d\)\n((?:    .*\n)+)" % context["rows"], out, re.M)
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


# === decisions index and why (r14, r16, r17, r105) =====================================================================

def _decisions(world):
    """spec/decisions/ with an old decision and a new one superseding it."""
    world.write("spec/decisions/0001-old.md", '---\nid: %s\nsummary: "Do it the old way."\ndate: 2026-01-01\nstatus: superseded\n---\n# 1\n'
                % full("design-decision", "old"))
    world.write("spec/decisions/0002-new.md", '---\nid: %s\nsummary: "Do it | the new way."\ndate: 2026-02-01\nstatus: accepted\n'
                'supersedes: design-decision/old\nrevisit_when: "it hurts"\nrevisit_signal: requests\n---\n# 2\n'
                % full("design-decision", "new"))


@given("two decisions under spec/decisions/, one superseding the other")
def two_decisions(world):
    _decisions(world)


@given("two decisions under spec/decisions/, one of them with no id")
def two_decisions_one_anonymous(world):
    _decisions(world)
    world.write("spec/decisions/0003-anon.md", "---\nsummary: Nameless.\nstatus: accepted\n---\n")


@when("model decisions is run")
def model_decisions(run, context):
    context["result"] = run("model", "--root", ".", "decisions")  # from the repository's directory, as the index names its file


def _index_text(repo):
    return (repo / "spec" / "decisions" / "index.md").read_text()


@then("spec/decisions/index.md has a row for each with its summary, status and what it supersedes, linked to its file")
def decisions_rows(repo, context):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    text = _index_text(repo)
    old, new = full("design-decision", "old"), full("design-decision", "new")
    assert "| [%s](0001-old.md) | Do it the old way. | superseded |  |  |" % old in text, text
    assert "| [%s](0002-new.md) | Do it \\| the new way. | accepted | %s | it hurts |" % (new, old) in text, text


@then("it prints spec/decisions/index.md as the file it wrote")
def decisions_file_named(context):
    result = context["result"]
    assert result.stdout.strip() == "wrote spec/decisions/index.md", result.stdout + result.stderr


@then("spec/decisions/index.md lists the decision with an id and not the one without")
def decisions_only_with_id(repo):
    text = _index_text(repo)
    assert "[%s]" % full("design-decision", "new") in text, text
    assert "Nameless." not in text, text


@given("a capability thing")
def capability_thing(world):
    world.good()


@then("it is refused because thing is not a requirement reference")
def why_refused(context):
    assert "'thing' is not a requirement reference" in context["result"].stdout, context["result"].stdout


@given("a capability thing with no requirement r9")
def capability_without_r9(world):
    world.good()


@then(parsers.parse("it says no capability has {ref} where the requirement's text would be"))
def why_no_capability(context, ref):
    lines = context["result"].stdout.splitlines()
    assert lines[0] == "%s#%s: no capability has this requirement now" % (THING, ref.split("#")[1]), lines


@then("it lists the proposal")
def why_lists_proposal(context):
    lines = context["result"].stdout.splitlines()
    assert "  changes by capability-proposal %s (drafted, 2026-10-15)" % P1 in lines, lines


@given(parsers.re(r"(?:only )?a capability-proposal (?P<first>p\d) dated (?P<date>[\d-]+) that (?P<verb>adds|changes|removes) thing#r2"
                  r"(?: and a capability-proposal (?P<second>p\d) dated (?P<date2>[\d-]+) that (?P<verb2>adds|changes|removes) thing#r2)?"))
def dated_proposals(world, first, date, verb, second, date2, verb2):
    world.observation()
    world.initiative()
    for ident, d, v in [(first, date, verb)] + ([(second, date2, verb2)] if second else []):
        world.proposal(ident=ident, date=d, **{v: "[thing#r2]"})


@then(parsers.parse("it lists {listed}, in that order, each with its status and date"))
def why_lists_in_order(context, listed):
    out = context["result"].stdout
    seen = re.findall(r"^  [\w/]+ by capability-proposal " + re.escape(full("capability-proposal", "")) +
                      r"(p\d) \((\w+), (\d{4}-\d\d-\d\d)\)$", out, re.M)
    assert [p for p, _, _ in seen] == listed.split(" then "), out
    assert all(status == "drafted" for _, status, _ in seen)
    assert [d for _, _, d in seen] == sorted(d for _, _, d in seen)


# === forms of an id and a reference (r24, r43, r46) ===============================================================

def _id_form_files(world):
    """A guarantees capability thing, the observation obs-1 and the initiative i1."""
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
    world.observation()
    world.initiative()


@given(parsers.parse("a bounded context with id {ident}, a capability thing and an initiative i1"))
def context_with_thing_and_initiative(world, ident):
    assert ident == CONTEXT
    _id_form_files(world)


@given(parsers.parse("a bounded context whose context path is {path}"))
def context_path(world, path):
    assert path == PATH
    _id_form_files(world)


@given(parsers.parse("a bounded context with id {ident}, a capability thing with requirement r1, a decision x and an observation x"))
def context_with_decision_and_observation(world, context, ident):
    assert ident == CONTEXT
    _id_form_files(world)
    world.write("spec/decisions/0001-x.md", DECISION % (full("design-decision", "x"), ""))
    world.write(".shop/records/observations.md", "# Observations\n\n## %s\nabout: %s\n\n## %s\nabout: %s\n"
                % (OBS1, CONTEXT, full("observation", "x"), CONTEXT))
    context["refused"] = True


@given(parsers.re(r"(?P<file>a capability-proposal|a capability|an initiative) whose (?P<field>\w+) is written (?P<written>\S+)"))
def file_whose_field_is_written(world, context, file, field, written):
    if file == "a capability-proposal":
        world.proposal(**({field: "[%s]" % written} if field != "part_of" else {}))
        if field == "part_of":
            p = world.root / ".shop/work/i1/p1.md"
            p.write_text(p.read_text().replace("part_of: initiative/i1", "part_of: " + written))
    elif file == "a capability":
        assert field == "rests_on"
        world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees", rests_on="[%s]" % written))
    else:
        assert field == "source"
        world.initiative(source="[%s]" % written)
    context["written"], context["field"] = written, field


def _written_unresolved(world, context, subject):
    """`<subject> is reported as unresolved`, for r24's refused forms and r43's bare part_of."""
    data = found(world, context)
    assert subject == context["written"]
    if context.get("refused"):  # r24: once, and no file problem
        assert len([d for d in data["unresolved"] if subject in d]) == 1, data
        assert data["problems"] == [], data
    else:  # r43
        assert [d for d in data["unresolved"] if " %s " % subject in d] == [".shop/work/i1/p1.md: %s names nothing in this repository" % subject], data


@then(parsers.re(r"(?P<written>\S+) is read as (?P<read>\S+) and not reported as unresolved"))
def written_read_as(world, context, written, read):
    data = found(world, context)
    assert written == context["written"]
    assert data["unresolved"] == [], data
    facts = world.model("facts").stdout
    assert '%s("%s", "%s").' % (context["field"], P1, read) in facts, facts


@given(parsers.parse("{file} gives {node} the id {ident}"))
def file_gives_id(world, file, node, ident):
    if file == "spec/index.md":
        world.write(file, "---\nid: %s\n---\n" % ident)
    elif file == "spec/capabilities/thing.md":
        world.write(file, cap("thing", ["- [r1] One."], group="guarantees").replace("id: " + THING, "id: " + ident))
    elif file == "spec/decisions/0001-x.md":
        world.write(file, "---\nid: %s\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n\n## Decision\nWe do it.\n" % ident)
    elif file == ".shop/work/i1/initiative.md":
        _initiative_with(world, "id: %s" % I1, "id: " + ident)
    elif file == ".shop/work/i1/p1.md":
        world.work_item("p1", id=ident)
    elif file == ".shop/records/observations.md":
        world.write(file, "# Observations\n\n## %s\nabout: %s\n" % (ident, CONTEXT))
    else:
        assert file == ".shop/records/f1.md", file
        world.write(file, "---\nid: %s\nkind: review-finding\n---\n" % ident)


# === an initiative done or abandoned (r36) ===========================================================================

@given(parsers.parse("a capability-change initiative with status {status}"))
def initiative_with_status(world, status):
    world.good()
    world.observation()
    world.initiative(status=status)


@given("under it a capability-proposal with status formulated, whose requirements scenarios name")
def formulated_proposal(world):
    world.proposal(status="formulated", adds="[thing#r1]")


@given(parsers.parse("under it a capability-proposal with status withdrawn, and under that a work-item with status {status}"))
def withdrawn_proposal_with_item(world, status):
    world.proposal(status="withdrawn", adds="[thing#r1]")
    world.work_item(status=status, part_of="capability-proposal/p1")


@then("no violation names the initiative")
def no_violation_names_initiative(world, context):
    data = found(world, context)
    assert [v for v in data["violations"] if I1 in v[1]] == [], data


# === the glossary (r48, r49) ======================================================================================

def _glossary(world, *bullets):
    """spec/index.md with a ## Glossary section with these bullets."""
    world.write("spec/index.md", INDEX + "\n## Glossary\n\n" + "\n".join(bullets) + "\n\n## Where things live\n\n- Here.\n")


def _term(name):
    return full("term", name)


@given(parsers.parse("a bounded context whose glossary has the bullet {bullet}"))
def glossary_with_bullet(world, context, bullet):
    if bullet.startswith('"') and bullet.endswith('"'):  # r48 quotes its bullet; r49's examples do not
        _glossary(world, bullet[1:-1])
    else:
        _glossary(world, "- **slice**: a unit of work.", bullet)


@given("a bounded context whose glossary defines batch, avoiding sprint and lot, and slice, avoiding nothing")
def glossary_batch_and_slice(world):
    _glossary(world, "- **batch**: the slices one session plans. Not: sprint, lot.",
              "- **slice**: a unit of work with an observable done.")


def _fact_lines(context):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    return result.stdout.splitlines()


@then("it prints the term term/ex.com/prod/ctx/suite-record")
def prints_term(context):
    assert 'node("%s", "term").' % _term("suite-record") in _fact_lines(context)


@then('its avoided words are "test record" and "run", and nothing else')
def avoided_words(context):
    lines = _fact_lines(context)
    assert 'avoid("%s", "test record").' % _term("suite-record") in lines
    assert 'avoid("%s", "run").' % _term("suite-record") in lines
    assert [l for l in lines if l.startswith("avoid(")] == [
        'avoid("%s", "test record").' % _term("suite-record"), 'avoid("%s", "run").' % _term("suite-record")]


@then("it reports one file problem naming spec/index.md")
def one_file_problem_in_index(world, context):
    data = found(world, context)
    assert len(data["problems"]) == 1, data
    assert data["problems"][0].startswith("spec/index.md"), data


@then("each term has a node fact of kind term and a term_of fact naming the bounded context")
def terms_have_kind_and_context(context):
    lines = _fact_lines(context)
    for t in ("batch", "slice"):
        assert 'node("%s", "term").' % _term(t) in lines
        assert 'term_of("%s", "%s").' % (_term(t), CONTEXT) in lines


@then("batch has an avoid fact for sprint and one for lot")
def batch_avoids(context):
    lines = _fact_lines(context)
    assert 'avoid("%s", "sprint").' % _term("batch") in lines
    assert 'avoid("%s", "lot").' % _term("batch") in lines


@then("slice has no avoid fact")
def slice_avoids_nothing(context):
    assert not [l for l in _fact_lines(context) if l.startswith('avoid("%s"' % _term("slice"))]


# === the search for an interpreter with clingo (r12, r55) =========================================================

PROBE = "-c import clingo"
TRIED_ALWAYS = ["/usr/local/bin/python3", "/usr/bin/python3"]


def _fake_python(world, dirname, behaviour="find"):
    """A python3 in <dirname> that logs each call. find: runs the real interpreter without the hiding PYTHONPATH;
    probe-only: says yes to the probe but runs the real interpreter with clingo still hidden; lack: has no clingo."""
    real = sys.executable
    body = {"find": 'exec /usr/bin/env -u PYTHONPATH "%s" "$@"' % real,
            "probe-only": 'if [ "$1" = "-c" ]; then exit 0; fi\nexec "%s" "$@"' % real,
            "lack": "exit 1"}[behaviour]
    p = world.write("%s/python3" % dirname, '#!/bin/sh\necho "%s: $*" >> "%s"\n%s\n' % (dirname, world.root / "calls.log", body))
    p.chmod(0o755)
    return p


def _search_env(world, path_dirs, **extra):
    """The environment of the interpreter without clingo: clingo hidden, PATH as given."""
    env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_MODEL_PYTHON", "VIRTUAL_ENV", "SHOPSYSTEM_MODEL_REEXEC")}
    env["PYTHONPATH"] = str(world.root / "hidden")
    env["PATH"] = os.pathsep.join(str(world.root / d) for d in path_dirs)
    env.update(extra)
    return env


def _calls(world):
    log = world.root / "calls.log"
    return log.read_text().splitlines() if log.exists() else []


def _check_calls(world):
    return [c for c in _calls(world) if str(SCRIPTS / "model") in c]


@given("an interpreter that cannot import clingo")
def interpreter_without_clingo(world, context):
    world.good()
    world.write("hidden/clingo.py", HIDE_CLINGO)
    context["env"] = _search_env(world, ["empty"])


@given("on PATH, in order, a virtualenv's python3 that has clingo, a python3 without it and two python3s with it")
def path_of_four(world, context):
    for d, behaviour in (("venv/bin", "find"), ("lacks", "lack"), ("bin", "find"), ("later", "find")):
        _fake_python(world, d, behaviour)
    context["env"] = _search_env(world, ["venv/bin", "lacks", "bin", "later"], VIRTUAL_ENV=str(world.root / "venv"))


@given("a python3 on PATH that says it has clingo but runs the check without it")
def path_of_liar(world, context):
    _fake_python(world, "bin", "probe-only")
    context["env"] = _search_env(world, ["bin"])


@given("no python3 that can, whether PATH has none or $SHOPSYSTEM_MODEL_PYTHON and PATH name ones without it")
def no_python_with_clingo(world, context):
    _fake_python(world, "lacks", "lack")
    nowhere = world.root / "nowhere/python3"
    # the case run by the When has no interpreter on PATH; the other is run by the Then steps (see _tried_cases)
    context["cases"] = [("no interpreter on PATH", [], context["env"]),
                        ("interpreters that lack it", [str(nowhere), str(world.root / "lacks/python3")],
                         _search_env(world, ["lacks"], SHOPSYSTEM_MODEL_PYTHON=str(nowhere)))]


@then("it asks the one without clingo, then the first with it, and runs again under that one")
def asks_in_order(world, context):
    out = context["result"].stdout
    assert "0 violations" in out, out
    assert _calls(world) == ["lacks: " + PROBE, "bin: " + PROBE, "bin: %s --root %s check" % (SCRIPTS / "model", world.root)], _calls(world)


@then("it never asks the virtualenv's python3 or the second with clingo")
def never_asks(world):
    assert not [c for c in _calls(world) if c.startswith(("venv/bin:", "later:"))], _calls(world)


@then("when $SHOPSYSTEM_MODEL_PYTHON names a python3 with clingo, it runs again under that one")
def explicit_python(world, context):
    _fake_python(world, "chosen")
    (world.root / "calls.log").unlink(missing_ok=True)
    env = _search_env(world, ["bin"], SHOPSYSTEM_MODEL_PYTHON=str(world.root / "chosen/python3"))
    result = world.model("check", env=env, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 violations" in result.stdout
    assert _calls(world) == ["chosen: " + PROBE, "chosen: %s --root %s check" % (SCRIPTS / "model", world.root)], _calls(world)


@then("the check runs again under that python3 once")
def runs_again_once(world, context):
    assert "clingo" in context["result"].stdout
    assert len(_check_calls(world)) == 1, _calls(world)


def _each_case(world, context):
    """The When's result and the other case's, run here: (name, result, interpreters tried) for each."""
    if "second" not in context:
        context["second"] = world.model("check", env=context["cases"][1][2], timeout=60)
    return [(context["cases"][0][0], context["result"], context["cases"][0][1]),
            (context["cases"][1][0], context["second"], context["cases"][1][1])]


@then("it names clingo and pip install clingo")
def names_pip_install(world, context):
    for name, result, _ in _each_case(world, context):
        assert "clingo" in result.stdout, name
        assert "pip install clingo" in result.stdout, name


@then("it names each interpreter it tried, /usr/local/bin/python3 and /usr/bin/python3 among them")
def names_interpreters_tried(world, context):
    for name, result, tried in _each_case(world, context):
        assert result.returncode == 2, (name, result.stdout + result.stderr)
        named = result.stdout.split("it tried has it:", 1)[1].split("\n", 1)[0]
        assert [p.strip() for p in named.rstrip(".").split(",")] == tried + TRIED_ALWAYS, (name, named)
    assert _check_calls(world) == [], _calls(world)


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


# === the decisions index checked and written, and the rules (r15, r37, r65) ========================================

HAND_WRITTEN = "# Decisions\n\nhand-written\n"


@given("a spec/decisions/index.md that differs from what model decisions writes")
def stale_index(world):
    _decisions(world)
    world.write("spec/decisions/index.md", HAND_WRITTEN)


@given("a spec/decisions/index.md that is what model decisions writes")
def current_index(world):
    _decisions(world)
    written = world.model("decisions")
    assert written.returncode == 0, written.stdout + written.stderr


@when("model decisions --check is run")
def model_decisions_check(world, context):
    context["result"] = world.model("decisions", "--check")


@then("it says the file is not current, exits 1, and the file is unchanged")
def index_not_current(repo, context):
    result = context["result"]
    assert result.returncode == 1, result.stdout + result.stderr
    assert "not what `model decisions` writes" in result.stdout, result.stdout
    assert _index_text(repo) == HAND_WRITTEN


@then("it says the file is current")
def index_current(context):
    assert "spec/decisions/index.md is current" in context["result"].stdout, context["result"].stdout


@given("a repository with no spec/decisions/")
def no_decisions_directory(repo):
    assert not (repo / "spec" / "decisions").exists()


@then("the index has its header and no row")
def index_header_only(repo):
    text = _index_text(repo)
    assert text.startswith("# "), text
    assert "](" not in text, text


@given("any repository")
def any_repository(world):
    pass  # the World's spec/index.md is enough: the rules are model.lp's, not the repository's


@when("model rules is run")
def model_rules(world, context):
    context["result"] = world.model("rules")


def _lp_labels():
    """The codes model.lp labels, in its order."""
    return re.findall(r'^label\("([^"]+)",', (SCRIPTS / "model.lp").read_text(), re.M)


@then("it prints each rule's code and plain label, one a line, the violations first and then the warnings")
def rules_printed(context):
    out = context["result"].stdout
    rows = [line.split("  ", 1) for line in out.splitlines()]
    assert all(len(row) == 2 and row[1] for row in rows), out
    codes = [c for c, _ in rows]
    assert codes == _lp_labels(), out
    assert ["v_s3", "a requirement has no scenario"] in rows
    firstw = min(i for i, c in enumerate(codes) if c.startswith("w_"))
    assert all(c.startswith("w_") for c in codes[firstw:]), codes
    assert all(c.startswith("v") for c in codes[:firstw]), codes


# === which files model reads (r19) ===============================================================================

def _files_read():
    """For each file of r19's Examples: the path written, its text, and a line of the facts that shows it was read."""
    decision = "---\nid: %s\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n---\n" % full("design-decision", "one")
    one = 'node("%s", "design-decision").' % full("design-decision", "one")
    initiative, i1 = "---\nid: %s\nstatus: started\n---\n" % I1, 'node("%s", "initiative").' % I1
    observations, obs = "# Observations\n\n## %s\nabout: %s\n" % (OBS1, CONTEXT), 'node("%s", "observation").' % OBS1
    capability = (cap("thing", ["- [r1] One."]), 'node("%s", "capability").' % THING)
    return {
        "spec/index.md": ("---\nid: bounded-context/row.com/prod/rowctx\n---\n",
                          'node("bounded-context/row.com/prod/rowctx", "bounded-context").'),
        "spec/capabilities/thing.md": capability,
        "features/sub/thing.feature": (feature("thing", ("@r1", "it answers")), "features/sub/thing.feature:it answers"),
        "spec/decisions/0001-one.md": (decision, one),
        "spec/decisions/index.md": (decision, one),
        ".shop/work/i1/initiative.md": (initiative, i1),
        ".shop/records/observations.md": (observations, obs),
        ".shop/records/review/f1.md with an id": ("---\nid: %s\nkind: review-finding\n---\n" % full("review-finding", "f1"),
                                                  'node("%s", "review-finding").' % full("review-finding", "f1")),
        ".shop/records/review/f2.md with no id": ("---\nkind: review-finding\nabout: capability/zzmark\n---\n", "zzmark"),
        "decisions/0001-one.md": (decision, one),
        "work/i1/initiative.md": (initiative, i1),
        "records/observations.md": (observations, obs),
    }


@given(parsers.parse("a repository in a directory that has {file}"))
def repository_with_file(world, context, file):
    text, marker = _files_read()[file]
    world.write(file.split(" ", 1)[0], text)
    context["marker"] = marker


@when(parsers.re(r"model facts is run (?P<how>with --root naming that directory|from that directory with no --root)"))
def model_facts_how(world, repo, context, how):
    if how.startswith("with --root"):
        context["result"] = world.model("facts")
    else:
        context["result"] = subprocess.run([sys.executable, str(SCRIPTS / "model"), "facts"], capture_output=True, text=True, cwd=repo)


@then(parsers.re(r"the facts printed (?P<outcome>include|do not include) what (?P<file>.+) contains"))
def facts_include(context, outcome, file):
    facts = context["result"].stdout
    assert (context["marker"] in facts) == (outcome == "include"), facts


# === the check as JSON (r33) =====================================================================================

@given("a repository the grammar accepts")
def repository_accepted(world, context):
    world.good()
    context["violating"] = False


@given("a repository with a requirement no scenario names")
def repository_unscenarioed(world, context):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] Req 1."]))
    context["violating"] = True


@when("model check is run with --json")
def model_check_json(world, context):
    context["found"], context["result"] = world.check_json()


@then("it prints one JSON object with the violations, warnings, unresolved references and file problems")
def one_json_object(context):
    data = context["found"]
    assert sorted(data) == ["labels", "problems", "unresolved", "violations", "warnings"], data
    assert bool(data["violations"]) == context["violating"], data


@then("the object maps each code it prints to its plain label")
def json_labels(context):
    data = context["found"]
    codes = {name for name, _ in data["violations"] + data["warnings"]}
    assert set(data["labels"]) == codes, data
    assert all(isinstance(v, str) and v for v in data["labels"].values()), data


# === one part directly, and one capability argued (r34, r35) =======================================================

def _two_capabilities(world):
    for name in ("other", "thing"):
        world.write("spec/capabilities/%s.md" % name, cap(name, ["- [r1] One."], group="guarantees"))
    world.observation()


@given("an initiative that is not a capability-change with two parts directly under it")
def defect_with_two_parts(world):
    _two_capabilities(world)
    world.initiative(kind="defect")
    for w in ("w1", "w2"):
        world.work_item(w)


@given("a capability-change initiative with two capability-proposals directly under it")
def change_with_two_proposals(world):
    _two_capabilities(world)
    world.initiative()
    world.proposal("p1", adds="[thing#r1]")
    world.proposal("p2", adds="[other#r1]", argues="[other]")


@then(parsers.re(r"the initiative is (?P<reported>reported|not reported) under v_k5"))
def initiative_under_v_k5(world, context, reported):
    data = found(world, context)
    rows = [a for name, a in data["violations"] if name == "v_k5"]
    assert rows == ([[I1]] if reported == "reported" else []), data


@given("capabilities thing and other")
def capabilities_thing_and_other(world):
    _two_capabilities(world)
    world.initiative()


@given("a capability-proposal that argues both thing and other")
def proposal_arguing_both(world):
    world.proposal(adds="[thing#r1, other#r1]", argues="[thing, other]")


@then("the output names v_k6 with the proposal")
def output_names_v_k6(context):
    out = context["result"].stdout
    assert re.search(r"v_k6  .+  \(1\)\n\s+" + re.escape(P1), out), out


# === the glossary checked (r52-r54) ================================================================================

@given("a glossary term slice that avoids chunk")
def glossary_slice_avoids_chunk(world):
    _glossary(world, "- **slice**: a unit of work. Not: chunk.")


@given('a requirement that says "chunk", a scenario titled "chunks are planned" and a deprecated scenario titled "a chunk as it was"')
def chunk_everywhere(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it plans each chunk.", "- [r2] It plans a slice."]))
    world.write("features/thing.feature", feature("thing", ("@r1", "it plans"), ("@r2", "chunks are planned"),
                                                  ("@r2 @deprecated", "a chunk as it was")))


def _v_t1(world, context):
    return [a for name, a in found(world, context)["violations"] if name == "v_t1"]


@then("v_t1 names the requirement, chunk and the term slice")
def v_t1_names_requirement(world, context):
    assert [THING + "#r1", "chunk", _term("slice")] in _v_t1(world, context), found(world, context)


@then("v_t1 names the scenario, chunk and the term slice")
def v_t1_names_scenario(world, context):
    assert ["features/thing.feature:chunks are planned", "chunk", _term("slice")] in _v_t1(world, context), found(world, context)


@then("v_t1 does not name the deprecated scenario")
def v_t1_not_deprecated(world, context):
    assert not [a for a in _v_t1(world, context) if "as it was" in a[0]], found(world, context)


@given("a glossary with an entry for slice and another for Slice")
def glossary_slice_twice(world):
    _glossary(world, "- **slice**: a unit of work.", "- **Slice**: a piece of a batch.")


@then("v_t2 names term/ex.com/prod/ctx/slice")
def v_t2_names_slice(world, context):
    assert [a for name, a in found(world, context)["violations"] if name == "v_t2"] == [[_term("slice")]], found(world, context)


@given("a glossary where slice avoids batch, batch is a term, and hand-back avoids Hand-back")
def glossary_avoiding_terms(world):
    _glossary(world, "- **slice**: a unit of work. Not: batch.", "- **batch**: the slices one session plans.",
              "- **hand-back**: an implementer's stop. Not: Hand-back, halt.")


@then("v_t3 names batch and hand-back")
def v_t3_names(world, context):
    rows = [a for name, a in found(world, context)["violations"] if name == "v_t3"]
    assert sorted(rows) == [["batch"], ["hand-back"]], found(world, context)


# === an abandoned initiative (r59) ===============================================================================

@given("an abandoned capability-change initiative")
def abandoned_initiative(world):
    world.good()
    world.observation()
    world.initiative(status="abandoned")


@then("v_d2 names the initiative")
def v_d2_names_initiative(world, context):
    assert [a for name, a in found(world, context)["violations"] if name == "v_d2"] == [[I1]], found(world, context)


@then("once the work-item is withdrawn too, no violation names the initiative")
def withdrawn_too(world):
    world.work_item(status="withdrawn", part_of="capability-proposal/p1")
    data, _ = world.check_json()
    assert [v for v in data["violations"] if I1 in v[1]] == [], data
