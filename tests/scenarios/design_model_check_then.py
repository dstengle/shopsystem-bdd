"""design-model-check's Then steps on what `model check`, `facts` and `why` printed, and `found`, the
findings of `check --json` read once."""
import re

from pytest_bdd import parsers, then

from .conftest import I1, P1, THING, full


def found(world, context):
    """`check --json` of the repository, run once."""
    if "found" not in context:
        context["found"], _ = world.check_json()
    return context["found"]


# --- Then ------------------------------------------------------------------------------------------------------

@then(parsers.parse("it exits {code:d}"))
def exits(context, code):
    result = context["result"]
    assert result.returncode == code, result.stdout + result.stderr
    assert "Traceback" not in result.stderr


@then("it prints 0 violations, 0 unresolved references and 0 file problems")
def reports_nothing(context):
    out = context["result"].stdout
    assert "0 violations" in out
    assert "0 unresolved references, 0 file problems" in out


@then(parsers.re(r"the output names (?P<code>v15[abc])"))
def output_names_code(world, context, code):
    assert code in context["result"].stdout, context["result"].stdout
    assert code in [name for name, _ in found(world, context)["violations"]], found(world, context)


@then("thing#r4 is printed neither under v15c nor as unresolved")
def r4_not_reported(world, context):
    data = found(world, context)
    assert [d for d in data["unresolved"] if "thing#r4" in d] == [], data
    assert [a for name, a in data["violations"] if name in ("v15c", "v15d") and "thing#r4" in a[0]] == [], data


@then(parsers.re(r"the requirement thing#r2 is (?P<reported>not|still|printed) (?:printed )?under v_s3"))
def r2_under_v_s3(world, context, reported):
    rows = [a[0] for name, a in found(world, context)["violations"] if name == "v_s3"]
    assert (THING + "#r2" in rows) == (reported != "not"), found(world, context)


@then("neither thing#r1 nor thing#r2 is printed under v_s3")
def neither_under_v_s3(world, context):
    rows = [a[0] for name, a in found(world, context)["violations"] if name == "v_s3"]
    assert rows == [], found(world, context)


@then("it prints no file problem")
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


@then("it prints no file problem and no v_s2")
def no_file_problem_and_no_v_s2(world, context):
    data = found(world, context)
    assert data["problems"] == [], data
    assert [a for name, a in data["violations"] if name == "v_s2"] == [], data


@then("it prints no file problem and no v15a")
def no_file_problem_and_no_v15a(world, context):
    data = found(world, context)
    assert data["problems"] == [], data
    assert [a for name, a in data["violations"] if name == "v15a"] == [], data


@then("thing#r1 is printed under v_s3 and thing#r2 is not")
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


@then(parsers.re(r"(?P<subject>.+?) is printed as unresolved"))
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


@then(parsers.re(r"(?P<subject>term/\w+) is not printed as unresolved"))
def term_not_reported_unresolved(world, context, subject):
    assert subject == "term/" + context["term"]
    assert not _term_unresolved(world, context), found(world, context)


@then(parsers.re(r"(?P<subject>.+?) is printed under v15c and not as unresolved"))
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


def _written_unresolved(world, context, subject):
    """`<subject> is printed as unresolved`, for r24's refused forms and r43's bare part_of."""
    data = found(world, context)
    assert subject == context["written"]
    if context.get("refused"):  # r24: once, and no file problem
        assert len([d for d in data["unresolved"] if subject in d]) == 1, data
        assert data["problems"] == [], data
    else:  # r43
        assert [d for d in data["unresolved"] if " %s " % subject in d] == [".shop/work/i1/p1.md: %s names nothing in this repository" % subject], data
