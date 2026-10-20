"""design-model-check's decisions index and why (r14-r17, r105), an initiative done or abandoned (r36), and the
rules (r37, r65)."""
import re

from pytest_bdd import given, parsers, then, when

from .conftest import I1, P1, SCRIPTS, THING, full
from .design_model_check_then import found


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
