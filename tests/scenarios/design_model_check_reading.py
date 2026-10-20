"""design-model-check's reading: the forms of an id and a reference (r24, r43, r46), which files model reads (r19),
the check as JSON (r33), and one part directly and one capability argued (r34, r35)."""
import re
import subprocess
import sys

from pytest_bdd import given, parsers, then, when

from .conftest import CONTEXT, I1, OBS1, P1, PATH, SCRIPTS, THING, cap, feature, full
from .design_model_check_given import DECISION
from .design_model_check_problems import _initiative_with
from .design_model_check_then import found


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
