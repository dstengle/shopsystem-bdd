"""features/feature-file-tools.feature, bound to scripts/features: the scenarios of requirements r1-r7, r10-r18,
r25-r29, r36-r38, r41, r42, r46, r51-r58. (The slice, deprecate, retire and plugin ones are bound by the
work-items that follow, or retired with the commands they test.)

A Given writes the feature files, test modules and trees a scenario names into `repo`; the When runs `features`
once and keeps the files as they were (`context["before"]`); the Then steps read what it printed and what it left.
"""
import re
import shlex

import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE = "feature-file-tools.feature"
BOUND = (
    'every feature file under the directory is read, and docstring text is not',
    'a feature file with a Rule block is refused',
    'an edit is refused only when it would leave a Rule: block outside a docstring',
    'counting by tag counts outline rows, inherited tags and untagged scenarios',
    "listing by tag includes the feature's and the Examples' tags",
    'listing by title finds every scenario whose title contains the text',
    'listing that matches nothing prints nothing and fails',
    'retagging a title that is not in exactly one file is refused',
    'retagging with a tag that is not a requirement tag is bad usage',
    'moving a scenario takes its block to the end of the destination',
    'moving with the Background inlined puts its steps first',
    'moving with feature tags kept adds the missing ones on a tag line of their own',
    'moving to a destination that does not exist is refused',
    'two trees alike scenario by scenario pass the move check',
    'a scenario that changed in the move is named with what changed',
    'a title that appears twice in either tree is a duplicate',
    'a binding that names no scenario is reported',
    'bindings that all name a scenario pass',
    'a test module that does not parse is refused',
    'rebinding rewrites each binding of the old title and counts them',
    'rebinding to a title no scenario has is refused',
    'moving a scenario to its own file is refused',
    'a title in only one tree is missing or added',
    'a tag is found with or without its leading @',
    'rebinding to a title several feature files have is refused',
    'rebinding a title written over several lines is refused',
    'a refusal says why on stderr and fails',
    "tagging with a requirement id adds it to the scenario's requirement tags",
    '--file works in that file only, whatever other files have the title',
    '--file naming a file that does not have the title is refused',
    '--file naming a file that has the title twice is refused',
    '--file naming a file outside --dir is refused',
    'rebind --file rewrites only the bindings whose feature names that file',
    'deprecating a scenario marks it deprecated and records what for',
    'deprecating a scenario already deprecated is refused',
    'the deprecated list shows each deprecated scenario and what will retire it',
    'the deprecated list says when nothing is deprecated',
    'retiring a deprecated scenario removes its block',
    'retiring a scenario that is not deprecated is refused',
    'deprecating a scenario prints its file and new title',
    'the deprecated list flags a deprecated scenario it cannot place',
    'a scenarios() call binds every scenario of the feature files it names',
    '--unbound reports a scenario that no call binds',
    '--unbound reports a scenario bound twice with each call',
    '--unbound looks only at the feature files it names',
)


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


# --- the files a scenario writes ----------------------------------------------------------------------------

NOTE_WITH = '    Given a note\n      """\n      %s\n      """\n'
RULE = "Feature: Rules\n\n  Rule: a rule\n\n    Scenario: Inside\n      Given a step\n"


def feature_text(*scenarios, tags="", background=""):
    head = "%sFeature: Cart\n  Narrator: a shopper\n\n" % (tags + "\n" if tags else "")
    return head + background + "\n".join(scenarios)


def scenario_text(title, tags="", body="    Given a step\n", kind="Scenario"):
    return "%s  %s: %s\n%s" % ("  %s\n" % tags if tags else "", kind, title, body)


def outline_text(title, tags, *tables):
    """A Scenario Outline whose Examples tables are (tag line, number of rows)."""
    out = "%s  Scenario Outline: %s\n    Given <n>\n" % ("  %s\n" % tags if tags else "", title)
    for tag, rows in tables:
        out += "\n%s    Examples:\n      | n |\n%s" % ("    %s\n" % tag if tag else "", "".join("      | %d |\n" % i for i in range(1, rows + 1)))
    return out


def binding(title, feature_name="cart.feature", line=12):
    """A test module whose binding call sits on line `line`."""
    pad = "".join("# filler\n" for _ in range(line - 2))
    return 'from pytest_bdd import scenario\n%s@scenario("%s", "%s")\ndef test_x():\n    pass\n' % (pad, feature_name, title)


def write(repo, name, text):
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def snapshot(repo):
    """Every file under `repo`, by path."""
    return {str(p.relative_to(repo)): p.read_text() for p in sorted(repo.rglob("*")) if p.is_file()}


def store(repo, context, path, *scenarios, tags=None, background=None):
    """Write the feature file `path` from what the scenario has told so far: scenarios add up, tags and Background replace."""
    entry = context.setdefault("files", {}).setdefault(path, {"scenarios": [], "tags": "", "background": ""})
    entry["scenarios"].extend(scenarios)
    if tags is not None:
        entry["tags"] = tags
    if background is not None:
        entry["background"] = background
    context["last"] = path
    write(repo, path, feature_text(*entry["scenarios"], tags=entry["tags"], background=entry["background"]))


def titles_in(text):
    return re.findall(r'"([^"]*)"', text)


def tag_line_of(text, title):
    """The line just above `Scenario: <title>`."""
    lines = text.splitlines()
    return lines[lines.index("  Scenario: " + title) - 1]


# --- the checks every scenario ends with --------------------------------------------------------------------

@pytest.fixture(autouse=True)
def whole_output(context):
    """After each scenario: features never crashed, and a listing had exactly the lines the scenario said it lists."""
    yield
    result = context.get("result")
    if result is not None:
        assert "Traceback" not in result.stderr
    if "listed" in context:
        assert sorted(result.stdout.splitlines()) == sorted(context["listed"])


def refused(run, repo, *args):
    """Run an edit that must be refused: exit 1, nothing on stdout, a reason on stderr, every file as it was."""
    before = snapshot(repo)
    done = run("features", *args)
    assert done.returncode == 1, done.stdout + done.stderr
    assert done.stdout == ""
    assert "Traceback" not in done.stderr
    assert snapshot(repo) == before
    return done.stderr


def rejected(context, code=1):
    result = context["result"]
    assert result.returncode == code, result.stdout + result.stderr
    assert result.stdout == ""
    assert "Traceback" not in result.stderr
    return result.stderr


# --- Given: feature files -----------------------------------------------------------------------------------

@given(parsers.re(r'a feature file (?P<path>\S+) with a scenario "(?P<title>[^"]+)"(?: tagged @(?P<tag>\S+)| not tagged @deprecated)?'))
def feature_with_scenario(repo, context, path, title, tag):
    store(repo, context, path, scenario_text(title, "@" + tag if tag else ""))


@given(parsers.parse('the scenario "{title}" has a docstring with the lines "@slice-1" and "Scenario: Phantom"'))
def scenario_with_docstring(repo, context, title):
    path = context["last"]
    entry = context["files"][path]
    entry["scenarios"] = [scenario_text(title, "@slice-1", NOTE_WITH % "@slice-1\n      Scenario: Phantom")]
    store(repo, context, path)


@given("a feature file features/rules.feature that has a Rule: block")
def feature_with_rule(repo):
    write(repo, "features/rules.feature", RULE)


@given(parsers.re(r"an edit by features that would leave features/cart.feature with (?P<result>.+)"))
def edit_leaving(repo, context, result):
    """Moving a scenario into a destination that ends inside an unclosed docstring flips which lines of the moved block
    lie inside a docstring."""
    open_dest = feature_text(scenario_text("Existing", body='    Given a note\n      """\n      still open\n'))
    doc_line = "Scenario: Apply a code" if result.startswith("two") else "Rule: not a rule"
    title = "Empty cart" if result.startswith("two") else "Apply a code"
    write(repo, "features/old.feature", feature_text(scenario_text(title, body=NOTE_WITH % doc_line)))
    if "outside" in result:
        dest = open_dest
    elif "inside" in result:
        dest = feature_text(scenario_text("Existing"))
    else:
        dest = feature_text(scenario_text("Apply a code"),
                            scenario_text("Existing", body=open_dest.split("Scenario: Existing\n")[1]))
    write(repo, "features/cart.feature", dest)
    context.update(result_wanted=result, title=title, edit=["move", title, "--to", "features/cart.feature"])


@given(parsers.re(r"a feature file (?P<path>\S+) tagged @(?P<tag>\S+)"))
def feature_tagged(repo, context, path, tag):
    store(repo, context, path, tags="@" + tag)


@given(parsers.re(r'it has a scenario "(?P<title>[^"]+)" with no tags of its own'))
def it_has_plain_scenario(repo, context, title):
    store(repo, context, context["last"], scenario_text(title))


@given(parsers.re(r'it has a scenario "(?P<title>[^"]+)" tagged @(?P<tag>\S+)'))
def it_has_tagged_scenario(repo, context, title, tag):
    store(repo, context, context["last"], scenario_text(title, "@" + tag))


@given('it has a Scenario Outline "Outlined" tagged @slice-2 with an Examples table tagged @r3 of 2 rows and an untagged Examples table of 1 row')
def it_has_outline_with_two_tables(repo, context):
    store(repo, context, context["last"], outline_text("Outlined", "@slice-2", ("@r3", 2), ("", 1)))


@given('it has a Scenario Outline "Outlined" whose one Examples table is tagged @checkout and has one row')
def it_has_outline_with_one_table(repo, context):
    store(repo, context, context["last"], outline_text("Outlined", "", ("@checkout", 1)))


@given(parsers.re(r'another feature file (?P<path>\S+) tagged @(?P<tag>\S+) has a scenario "(?P<title>[^"]+)"'))
def another_feature_file(repo, context, path, tag, title):
    store(repo, context, path, scenario_text(title), tags="@" + tag)


@given(parsers.re(r'a feature file (?P<path>\S+?)(?: with no tags)? has a scenario "(?P<title>[^"]+)"(?: with no tags)?'))
def untagged_feature_file(repo, context, path, title):
    store(repo, context, path, scenario_text(title))


@given(parsers.re(r'a feature file (?P<path>\S+) with scenarios (?P<titles>"[^"]+"(?:, "[^"]+")* and "[^"]+")'))
def feature_with_scenarios(repo, context, path, titles):
    store(repo, context, path, *[
        scenario_text(t, "@slice-1", "    Given a cart\n    When a code is applied\n") if t == "Apply a code" else scenario_text(t)
        for t in titles_in(titles)])


@given(parsers.parse('a feature file {path} whose last scenario is "{title}"'))
def feature_whose_last(repo, context, path, title):
    store(repo, context, path, scenario_text(title))
    context["destination"] = (repo / path).read_text()


@given(parsers.parse('a feature file {path} with no scenario tagged @slice-9'))
def feature_without_slice_9(repo, context, path):
    store(repo, context, path, scenario_text("Apply a code", "@slice-1"))


@given(parsers.parse('a feature file {path} whose Background has the step "{step}"'))
def feature_with_background(repo, context, path, step):
    store(repo, context, path, background="  Background:\n    %s\n\n" % step)


@given(parsers.parse('its scenario "{title}" has first step "{step}"'))
def its_scenario_has_first_step(repo, context, title, step):
    store(repo, context, context["last"], scenario_text(title, body="    %s\n" % step))


@given(parsers.re(r"a feature file (?P<path>\S+)"))
def feature_file(repo, context, path):
    store(repo, context, path)


@given(parsers.parse("a feature file {path} with the feature tags @cart and @checkout"))
def old_with_two_feature_tags(repo, context, path):
    store(repo, context, path, tags="@cart @checkout")


@given(parsers.re(r'its scenario "(?P<title>[^"]+)" has (?:the tag line "(?P<tags>[^"]+)"|(?P<none>no tag line))'))
def its_scenario_has_tag_line(repo, context, title, tags, none):
    store(repo, context, context["last"], scenario_text(title, tags or ""))


@given("a feature file features/cart.feature with the feature tag @cart")
def cart_with_feature_tag(repo, context):
    store(repo, context, "features/cart.feature", tags="@cart")


@given(parsers.parse("no file {path}"))
def no_file(repo, path):
    assert not (repo / path).exists()


@given(parsers.parse('the title "Apply a code" is in {holders}'))
def title_in_files(repo, context, holders):
    write(repo, "features/other.feature", feature_text(scenario_text("Empty cart")))
    for path in re.findall(r"features/\w+\.feature", holders):
        write(repo, path, feature_text(scenario_text("Apply a code")))
    context["exact_files"] = True


@given(parsers.parse('a feature file {path} whose only scenario "{title}" has the tag line "{tags}"'))
def only_scenario_with_tag_line(repo, context, path, title, tags):
    store(repo, context, path, scenario_text(title, tags))


@given(parsers.parse('a feature file {path} whose only scenario "{title}" has the tags @wip, @slice-2, @r1 and @r4'))
def only_scenario_with_tags(repo, context, path, title):
    store(repo, context, path, scenario_text(title, "@wip @slice-2 @r1 @r4"))


def two_files(repo, context):
    """kb's case: one title in two feature files, each file with other scenarios."""
    store(repo, context, "features/cart.feature", scenario_text("Apply a code", "@slice-1 @r1"), scenario_text("Empty cart", "@r2"))
    store(repo, context, "features/old.feature", scenario_text("Apply a code", "@slice-2 @r1"), scenario_text("Checkout", "@r3"))
    context["two_files"] = (feature_text(scenario_text("Apply a code", "@slice-1 @r1"), scenario_text("Empty cart", "@r2")),
                            feature_text(scenario_text("Apply a code", "@slice-2 @r1"), scenario_text("Checkout", "@r3")))


@given('features/cart.feature and features/old.feature both have a scenario "Apply a code"')
def both_have_apply(repo, context):
    two_files(repo, context)


@given('a feature file features/cart.feature without a scenario "Voucher"')
def cart_without_voucher(repo, context):
    two_files(repo, context)


@given('features/codes.feature has a scenario "Voucher"')
def codes_has_voucher(repo, context):
    write(repo, "features/codes.feature", feature_text(scenario_text("Voucher", "@r2")))


@given('a feature file features/cart.feature with two scenarios "Apply a code"')
def cart_with_two(repo, context):
    write(repo, "features/cart.feature", feature_text(scenario_text("Apply a code", "@r1"), scenario_text("Apply a code", "@r2")))
    write(repo, "features/old.feature", feature_text(scenario_text("Apply a code", "@r3")))


@given('a feature file elsewhere/other.feature outside the features directory with a scenario "Apply a code"')
def feature_outside(repo, context):
    two_files(repo, context)
    write(repo, "elsewhere/other.feature", feature_text(scenario_text("Apply a code", "@r9")))
    write(repo, "features/codes.feature", feature_text(scenario_text("Voucher")))


@given('a feature file with a scenario "Apply a voucher"')
def a_feature_with_voucher(repo, context):
    store(repo, context, "features/cart.feature", scenario_text("Apply a voucher"))


@given('features/cart.feature and features/codes.feature both have a scenario "Apply a voucher"')
def both_hold_voucher(repo, context):
    store(repo, context, "features/cart.feature", scenario_text("Apply a voucher"))
    store(repo, context, "features/codes.feature", scenario_text("Apply a voucher"))


@given('no feature file has a scenario "Apply a voucher"')
def no_voucher(repo, context):
    store(repo, context, "features/cart.feature", scenario_text("Empty cart"))


# --- Given: trees ---------------------------------------------------------------------------------------------

STEPS = "    Given a cart\n    When it is used\n"


@given('a tree old/ with "Apply a code" and "Empty cart" in old/cart.feature')
def old_tree_alike(repo):
    write(repo, "old/cart.feature", feature_text(
        scenario_text("Apply a code", "@slice-1", "    Applying a code.\n" + STEPS),
        scenario_text("Empty cart", body="    Given an empty cart\n"), tags="@cart",
        background="  Background:\n    Given a shop\n\n"))


@given('a tree features/ with "Apply a code" in features/codes.feature and "Empty cart" in features/cart.feature, '
       "each alike in effective tags, description, Background and own steps")
def new_tree_alike(repo):
    write(repo, "features/codes.feature", feature_text(
        scenario_text("Apply a code", "@slice-1 @cart", "    Applying a code.\n    Given a shop\n" + STEPS)))
    write(repo, "features/cart.feature", feature_text(
        scenario_text("Empty cart", "@cart", "    Given a shop\n    Given an empty cart\n")))


BEFORE = scenario_text("Apply a code", "@slice-1", "    Applying a code.\n    Given a cart\n")


@given('trees old/ and features/ that both have "Apply a code"')
def trees_both_hold(repo, context):
    write(repo, "old/cart.feature", feature_text(BEFORE))
    write(repo, "features/cart.feature", feature_text(BEFORE))


@given(parsers.re(r'the two copies of "Apply a code" differ in their (?P<part>effective tags|description|steps)'))
def copies_differ(repo, part):
    after = {"effective tags": BEFORE.replace("@slice-1", "@slice-2"),
             "description": BEFORE.replace("Applying a code.", "Applying it."),
             "steps": BEFORE.replace("Given a cart", "Given a basket")}[part]
    write(repo, "features/cart.feature", feature_text(after))


@given(parsers.re(r'(?P<tree>old|features)/ has a second scenario titled "Apply a code"'))
def tree_holds_second(repo, context, tree):
    write(repo, "%s/again.feature" % tree, feature_text(scenario_text("Apply a code")))
    context["tree"] = tree


@given("trees old/ and features/")
def trees(repo):
    write(repo, "old/cart.feature", feature_text(scenario_text("Empty cart")))
    write(repo, "features/cart.feature", feature_text(scenario_text("Empty cart")))


@given(parsers.re(r'the title "Apply a code" is only in (?P<tree>old|features)/'))
def title_only_in(repo, tree):
    write(repo, "%s/codes.feature" % tree, feature_text(scenario_text("Apply a code")))


# --- Given: test modules --------------------------------------------------------------------------------------

@given('a test module tests/test_cart.py whose line 12 binds the title "Apply a code" in the feature cart.feature')
def module_line_12(repo):
    write(repo, "tests/test_cart.py", binding("Apply a code"))


@given('no feature file has the title "Apply a code"')
def no_file_has_title(repo):
    write(repo, "features/cart.feature", feature_text(scenario_text("Empty cart")))


@given('only features/codes.feature has the title "Apply a code"')
def only_codes_has_title(repo):
    write(repo, "features/cart.feature", feature_text(scenario_text("Empty cart")))
    write(repo, "features/codes.feature", feature_text(scenario_text("Apply a code")))


@given('a test module tests/test_cart.py binding "Apply a code" in cart.feature')
def module_binding_in_cart(repo):
    write(repo, "tests/test_cart.py", binding("Apply a code"))


@given('features/cart.feature has the scenario "Apply a code"')
def cart_has_apply(repo):
    write(repo, "features/cart.feature", feature_text(scenario_text("Apply a code")))


@given("a test module tests/test_broken.py that does not parse")
def module_broken(repo):
    write(repo, "tests/test_broken.py", "def broken(:\n")


@given(parsers.re(r'test modules with (?P<count>\d+) binding calls naming "Apply a code"'))
def modules_naming(repo, context, count):
    count = int(count)
    store(repo, context, "features/cart.feature", scenario_text("Empty cart"))
    old = "Apply a code" if count else "Something else"
    modules = {"tests/test_a.py": binding(old, line=5) + "\nVALUE = 'Apply a code'\n",
               "tests/test_b.py": binding(old) + binding("Empty cart", line=3)}
    for name, text in modules.items():
        write(repo, name, text)
    context.update(modules=modules, old_title=old, count=count)


@given('a test module binding "Apply a code"')
def module_binding(repo, context):
    write(repo, "tests/test_cart.py", binding("Apply a code"))


@given(parsers.parse('a test module tests/test_cart.py whose binding call at line 20 names "Apply a code" in a string written over several lines'))
def module_multiline(repo):
    lines = ["from pytest_bdd import scenario"] + ["# filler"] * 18
    lines += ['@scenario("cart.feature", "Apply "', '          "a code")', "def test_x():", "    pass", ""]
    write(repo, "tests/test_cart.py", "\n".join(lines))


@given('tests binding "Apply a code" to features/cart.feature and to features/old.feature')
def tests_binding_two(repo, context):
    write(repo, "features/cart.feature", feature_text(scenario_text("Apply a code (deprecated)", "@deprecated")))
    write(repo, "features/old.feature", feature_text(scenario_text("Apply a code")))
    context["modules"] = {"tests/test_cart.py": binding("Apply a code", "cart.feature"),
                          "tests/test_old.py": binding("Apply a code", "old.feature"),
                          "tests/test_path.py": binding("Apply a code", "../features/cart.feature")}
    for name, text in context["modules"].items():
        write(repo, name, text)


@given(parsers.parse('{path} has the scenarios "{one}" and "{two}"'))
def file_has_two(repo, context, path, one, two):
    store(repo, context, path, scenario_text(one), scenario_text(two))


@given(parsers.parse("a test module tests/test_cart.py calling {call}"))
def module_calling(repo, call):
    write(repo, "tests/test_cart.py", "from pytest_bdd import scenarios\n\n%s\n" % call)


@given('test modules tests/test_a.py and tests/test_b.py binding "Apply a code" at lines 12 and 5')
def modules_binding_twice(repo):
    write(repo, "tests/test_a.py", binding("Apply a code", line=12))
    write(repo, "tests/test_b.py", binding("Apply a code", line=5))


@given(parsers.parse('a test module tests/test_c.py binding "{title}" in cart.feature'))
def module_c_binding(repo, title):
    write(repo, "tests/test_c.py", binding(title))


@given(parsers.parse('a test module tests/test_cart.py binding "{title}" in cart.feature'))
def module_binding_title(repo, title):
    write(repo, "tests/test_cart.py", binding(title))


# --- When -------------------------------------------------------------------------------------------------------

def invoke(run, repo, context, argv):
    context["before"] = snapshot(repo)
    context["result"] = run("features", *argv)


@when(parsers.re(r"the agent runs features (?P<args>.+?)(?: without --(?:dir|tests|file))?"))
def agent_runs(run, repo, context, args):
    invoke(run, repo, context, shlex.split(args))


@when("the agent runs that edit")
def agent_runs_edit(run, repo, context):
    invoke(run, repo, context, context["edit"])


# --- Then: what a listing printed -------------------------------------------------------------------------------

@then(parsers.re(r'the output lists (?P<path>\S+) with "(?P<title>[^"]+)"'))
def output_lists(context, path, title):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    line = "%s: %s" % (path, title)
    assert line in result.stdout.splitlines(), result.stdout
    context.setdefault("listed", []).append(line)


@then(parsers.re(r'the output does not list "(?P<one>[^"]+)"(?: or "(?P<two>[^"]+)")?'))
def output_does_not_list(run, repo, context, one, two):
    for text in (one, two):
        if text:
            assert text not in context["result"].stdout
    if one == "Phantom":  # r1: the docstring's scenario is not found by its title either
        done = run("features", "list", "--title", "Phantom")
        assert (done.returncode, done.stdout) == (1, "")


@then("nothing is printed")
def nothing_printed(context):
    assert context["result"].stdout == ""


@then(parsers.parse("it exits {code:d}"))
def exits(context, code):
    result = context["result"]
    assert result.returncode == code, result
    assert "Traceback" not in result.stderr


# --- Then: counting (r4) ----------------------------------------------------------------------------------------

@then("it prints 5 scenarios for cart, 1 for slice-1, 3 for slice-2 and 2 for r3")
def counts_by_tag(context):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[:-1] == ["cart 5", "r3 2", "slice-1 1", "slice-2 3"]


@then("it prints a total of 6")
def counts_total(context):
    assert context["result"].stdout == "cart 5\nr3 2\nslice-1 1\nslice-2 3\ntotal 6\n"


# --- Then: refusals ---------------------------------------------------------------------------------------------

@then("the command is rejected because the feature file has a Rule: block")
def rejected_rule(context):
    assert "Rule: blocks are not supported" in rejected(context)


@then(parsers.re(r"the refusal names (?P<names>.+)"))
def refusal_names(repo, context, names):
    reason = context["result"].stderr
    if names == "no file":
        assert not re.findall(r"features/\w+\.feature", reason)
        return
    if names == "tests/test_cart.py and line 20":
        assert "tests/test_cart.py:20" in reason
        return
    wanted = re.split(r", | and ", names)
    for name in wanted:
        assert name in reason
    if context.get("exact_files"):  # r10: every file with the title, no other
        assert re.findall(r"features/\w+\.feature", reason) == wanted
    if names == "tests/test_broken.py":
        assert "tests/test_broken.py does not parse" in reason


@then("the edit is rejected because features could not read the result, and every file is as it was")
def edit_rejected(repo, context):
    assert "Rule:" in rejected(context)
    assert snapshot(repo) == context["before"]


@then("the edit is made")
def edit_made(run, repo, context):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    assert "Scenario: " + context["title"] in (repo / "features" / "cart.feature").read_text()
    if context["result_wanted"].startswith("two"):
        listed = run("features", "list", "--title", "Apply a code")
        assert listed.stdout == "features/cart.feature: Apply a code\n" * 2


@then("the command is rejected because the title is not in exactly one file")
def rejected_not_one(context):
    rejected(context)


@then("no file is changed")
def no_file_changed(repo, context):
    assert snapshot(repo) == context["before"]


@then("no test module is changed")
def no_module_changed(repo, context):
    assert snapshot(repo) == context["before"]


@then("the command is rejected as bad usage because the tag is not written r<n>")
def rejected_bad_usage(repo, context):
    result = context["result"]
    assert result.returncode == 2
    assert "r<n>" in result.stderr and "slice" not in result.stderr
    assert snapshot(repo) == context["before"]


@then("the command is rejected because the destination does not exist")
def rejected_no_destination(repo, context):
    assert "features/missing.feature does not exist" in rejected(context)


@then("the command is rejected because the destination is the scenario's own file")
def rejected_own_file(context):
    assert "is the scenario's own file" in rejected(context)


@then("the reason for the refusal is written to stderr")
def reason_on_stderr(context):
    result = context["result"]
    assert result.stdout == ""
    assert result.stderr == "features: 'Apply a code' is not tagged @deprecated: only a deprecated scenario is retired here\n"


@then("the command is rejected because the test module does not parse")
def rejected_unparsed(context):
    assert "does not parse" in rejected(context)


@then("the command is rejected because no scenario has the new title")
def rejected_no_new_title(context):
    assert "no scenario titled 'Apply a voucher'" in rejected(context)


@then("the command is rejected because several feature files have the new title")
def rejected_several_new_title(context):
    reason = rejected(context)
    assert "several" in reason
    assert "features/cart.feature, features/codes.feature" in reason


@then("the command is rejected because the binding's title is written over several lines")
def rejected_multiline(context):
    assert "tests/test_cart.py:20: the title is written over several lines" in rejected(context)


@then("the command is rejected because the file does not have the title")
def rejected_file_lacks_title(run, repo, context):
    assert "does not have" in rejected(context)
    for command in (("deprecate", "Voucher", "--for-removal"), ("retire", "Voucher"), ("move", "Voucher", "--to", "features/old.feature")):
        reason = refused(run, repo, *command, "--file", "features/cart.feature")
        assert "features/cart.feature" in reason and "does not have" in reason


@then("the command is rejected because the file has the title twice")
def rejected_file_twice(run, repo, context):
    assert "twice" in rejected(context)
    for command in (("deprecate", "Apply a code", "--for-removal"), ("move", "Apply a code", "--to", "features/old.feature")):
        reason = refused(run, repo, *command, "--file", "features/cart.feature")
        assert "features/cart.feature" in reason and "twice" in reason


@then("the command is rejected because the file is outside --dir")
def rejected_outside(run, repo, context):
    assert "outside" in rejected(context)
    for path in ("elsewhere/other.feature", "features/../elsewhere/other.feature"):
        for command in (("tag", "Apply a code", "r7"), ("deprecate", "Apply a code", "--for-removal"), ("retire", "Apply a code"),
                        ("move", "Apply a code", "--to", "features/codes.feature")):
            assert "outside" in refused(run, repo, *command, "--file", path)


# --- Then: retagging --------------------------------------------------------------------------------------------

@then(parsers.re(r"the scenario's tags are (?P<tags>@\S+(?:, @\S+)* and @\S+)"))
def scenario_tags_are(repo, context, tags):
    assert context["result"].returncode == 0, context["result"].stderr
    wanted = re.findall(r"@[\w.-]+", tags)
    assert tag_line_of((repo / "features/cart.feature").read_text(), "Apply a code") == "  " + " ".join(wanted)


@then(parsers.parse("every other line of {path} is unchanged"))
def other_lines_unchanged(repo, context, path):
    before = context["before"][path].splitlines()
    after = (repo / path).read_text().splitlines()
    assert len(after) == len(before)
    changed = [i for i in range(len(before)) if after[i] != before[i]]
    assert len(changed) <= 1 and all(before[i].strip().startswith("@") for i in changed)


@then('the scenario "Apply a code" in features/cart.feature is tagged @r7')
def tagged_r7(repo, context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert tag_line_of((repo / "features/cart.feature").read_text(), "Apply a code") == "  @slice-1 @r1 @r7"


@then("features/old.feature is unchanged")
def old_unchanged(run, repo, context):
    cart_text, old_text = context["two_files"]
    old, cart = repo / "features/old.feature", repo / "features/cart.feature"
    assert old.read_text() == old_text
    tagged_cart = cart_text.replace("@slice-1 @r1", "@slice-1 @r1 @r7")
    # --file names the other file as well: the same title, tagged there, leaves the first alone
    done = run("features", "tag", "Apply a code", "r7", "--file", "features/old.feature")
    assert done.returncode == 0, done.stderr
    assert cart.read_text() == tagged_cart
    assert old.read_text() == old_text.replace("@slice-2 @r1", "@slice-2 @r1 @r7")
    # deprecate, retire and move take --file the same way
    old.write_text(old_text)
    done = run("features", "deprecate", "Apply a code", "--for-removal", "--file", "features/old.feature")
    assert done.returncode == 0, done.stderr
    assert cart.read_text() == tagged_cart
    deprecated = old.read_text()
    assert "Scenario: Apply a code (deprecated)" in deprecated and "Scenario: Checkout" in deprecated
    done = run("features", "retire", "Apply a code (deprecated)", "--file", "features/old.feature")
    assert done.returncode == 0, done.stderr
    assert old.read_text() == feature_text(scenario_text("Checkout", "@r3"))
    assert cart.read_text() == tagged_cart
    old.write_text(old_text)
    dest = write(repo, "features/codes.feature", feature_text(scenario_text("Voucher")))
    done = run("features", "move", "Apply a code", "--file", "features/old.feature", "--to", "features/codes.feature")
    assert done.returncode == 0, done.stderr
    assert cart.read_text() == tagged_cart
    assert old.read_text() == feature_text(scenario_text("Checkout", "@r3"))
    assert "Scenario: Apply a code" in dest.read_text() and "@slice-2 @r1" in dest.read_text()
    # without --file a title in several files is refused, naming both
    old.write_text(old_text)
    cart.write_text(cart_text)
    for command in (("tag", "Apply a code", "r7"), ("deprecate", "Apply a code", "--for-removal"), ("retire", "Apply a code")):
        reason = refused(run, repo, *command)
        assert "features/cart.feature" in reason and "features/old.feature" in reason


# --- deprecate, deprecated and retire (r19, r21, r23, r24) ---------------------------------------------------

CART = "features/cart.feature"


@given(parsers.re(r'a scenario "(?P<title>[^"]+)" exists'))
def replacement_exists(repo, context, title):
    store(repo, context, CART, scenario_text(title))


@given(parsers.re(r'(?:no scenario "[^"]+" exists|no replacement is planned|no scenario titled "[^"]+"|no replacement)'))
def no_replacement():
    pass


@given(parsers.re(r'a scenario "(?P<title>[^"]+)" tagged @(?P<tag>r\d+) in (?P<path>\S+)'))
def replacement_tagged(repo, context, title, tag, path):
    store(repo, context, path, scenario_text(title, "@" + tag))


def deprecated_scenario(title, what):
    return scenario_text(title, "@deprecated", "    Deprecated for: %s\n    Given a step\n" % what)


@given(parsers.re(r'a feature file (?P<path>\S+) with a deprecated scenario "(?P<title>[^"]+)" deprecated for (?P<what>"[^"]+"|removal)'))
def feature_with_deprecated(repo, context, path, title, what):
    store(repo, context, path, deprecated_scenario(title, what.strip('"')))


@given("feature files in which no scenario is tagged @deprecated")
def no_deprecated(repo, context):
    store(repo, context, CART, scenario_text("Apply a code", "@slice-1"))


@given(parsers.re(r'a feature file (?P<path>\S+) with a scenario "(?P<first>[^"]+)" and a scenario "(?P<second>[^"]+)" tagged @deprecated'))
def feature_with_two(repo, context, path, first, second):
    store(repo, context, path, scenario_text(first), scenario_text(second, "@deprecated"))


@given("the scenario has no Deprecated for: line")
def no_deprecated_for_line():
    pass  # the Given before it wrote the scenario without one


@given('it is deprecated for "Apply a voucher", and "Apply a voucher" has no @r<n> tag')
def deprecated_for_untagged(repo, context):
    context["files"][CART]["scenarios"] = []
    store(repo, context, CART, deprecated_scenario("Apply a code (deprecated)", "Apply a voucher"), scenario_text("Apply a voucher", "@slice-1"))


@then("the scenario has the tag @deprecated")
def carries_deprecated(repo, context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert "@deprecated" in tag_line_of((repo / CART).read_text(), "Apply a code (deprecated)").split()


@then('its title is "Apply a code (deprecated)"')
def title_is_deprecated(repo):
    assert "  Scenario: Apply a code (deprecated)\n" in (repo / CART).read_text()


@then(parsers.re(r"it has a description line naming (?P<what>.+) as what it is deprecated for"))
def has_deprecated_for_line(repo, what):
    lines = (repo / CART).read_text().splitlines()
    assert lines[lines.index("  Scenario: Apply a code (deprecated)") + 1] == "    Deprecated for: " + what


@then("nothing else in the scenario is changed")
def nothing_else_changed(repo, context):
    before = context["before"][CART]
    what = re.search(r"Deprecated for: (.+)", (repo / CART).read_text()).group(1)
    expected = before.replace("  Scenario: Apply a code\n",
                              "  @deprecated\n  Scenario: Apply a code (deprecated)\n    Deprecated for: %s\n" % what)
    assert (repo / CART).read_text() == expected


@then("the command is rejected because the scenario is already deprecated")
def rejected_already_deprecated(context):
    assert "already deprecated" in rejected(context)


SAYS = {'that no scenario has the title "Apply a voucher"': "no scenario has that title",
        "that it is deprecated for removal": "deprecated for removal",
        "that it has no Deprecated for: line": "no Deprecated for: line",
        "that the replacement has no @r<n> tag": "the replacement has no @r<n> tag"}


def last_field(said):
    placed = re.fullmatch(r"(\S+) and (@r\d+)", said)
    return "%s %s" % placed.groups() if placed else SAYS[said]


def line_for(context, title):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    return next(line for line in result.stdout.splitlines() if line.startswith("%s: %s | " % (CART, title)))


@then(parsers.re(r'the list shows "(?P<title>[^"]+)" deprecated for (?P<what>"[^"]+"|removal), with (?P<said>.+)'))
def list_shows(context, title, what, said):
    parts = line_for(context, title).split(" | ")
    assert parts[1:] == ["for: " + what.strip('"'), last_field(said)]


@then(parsers.re(r'the line for "(?P<title>[^"]+)" says (?P<said>.+)'))
def line_says(context, title, said):
    assert line_for(context, title).split(" | ")[-1].endswith(last_field(said))


@then("it says that none is deprecated")
def none_deprecated(context):
    assert context["result"].stdout == "none deprecated\n"


@then(parsers.re(r'(?P<path>\S+) no longer has "(?P<title>[^"]+)"'))
def no_longer_holds(repo, context, path, title):
    assert context["result"].returncode == 0, context["result"].stderr
    assert "Scenario: " + title not in (repo / path).read_text()


@then(parsers.re(r"the rest of (?P<path>features/\S+) is as it was"))
def rest_as_it_was(repo, path):
    assert (repo / path).read_text() == feature_text(scenario_text("Empty cart"))


@then("the command is rejected because the scenario is not deprecated")
def rejected_not_deprecated(context):
    assert "not tagged @deprecated" in rejected(context)


@then(parsers.re(r"(?P<path>features/\S+) is as it was"))
def file_as_it_was(repo, context, path):
    assert (repo / path).read_text() == context["before"][path]


@then(parsers.re(r'it prints (?P<path>\S+) and "(?P<title>[^"]+)"'))
def prints_path_and_title(context, path, title):
    assert context["result"].stdout == "%s: %s\n" % (path, title)


# --- Then: moving -----------------------------------------------------------------------------------------------

@then('features/old.feature has "Empty cart" and not "Apply a code"')
def old_holds_empty_cart(repo, context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert (repo / "features/old.feature").read_text() == feature_text(scenario_text("Empty cart"))


@then('the block of "Apply a code" follows "Checkout" at the end of features/cart.feature, unchanged')
def block_follows(repo, context):
    block = scenario_text("Apply a code", "@slice-1", "    Given a cart\n    When a code is applied\n")
    assert (repo / "features/cart.feature").read_text() == context["destination"] + "\n" + block


@then(parsers.re(r'the moved "(?P<title>[^"]+)" has the steps "(?P<first>[^"]+)" then "(?P<second>[^"]+)"'))
def moved_has_steps(repo, context, title, first, second):
    assert context["result"].returncode == 0, context["result"].stderr
    assert "  Scenario: %s\n    %s\n    %s\n" % (title, first, second) in (repo / "features/cart.feature").read_text()


@then(parsers.re(r'the moved "(?P<title>[^"]+)" has the tag lines (?P<lines>"[^"]+"(?: then "[^"]+")*), the last directly above its Scenario: line'))
def moved_has_tag_lines(repo, context, title, lines):
    assert context["result"].returncode == 0, context["result"].stderr
    wanted = "".join("  %s\n" % t for t in titles_in(lines))
    assert (repo / "features/cart.feature").read_text().endswith(wanted + "  Scenario: %s\n    Given a step\n" % title)


# --- Then: the move check ---------------------------------------------------------------------------------------

@then("it prints that 2 scenarios match")
def two_match(context):
    assert context["result"].stdout == "2 scenarios match\n", context["result"].stderr


@then(parsers.re(r'it names "Apply a code" with its (?P<part>effective tags|description|steps) as changed'))
def names_changed(context, part):
    assert context["result"].stdout == "changed: Apply a code (%s)\n" % part.split()[-1]


@then('it names "Apply a code" as a duplicate')
def names_duplicate(context):
    label = "before" if context["tree"] == "old" else "after"
    assert context["result"].stdout == "duplicate title %s: Apply a code\n" % label


@then(parsers.re(r'it names "Apply a code" as (?P<named>missing|added)'))
def names_missing_or_added(context, named):
    assert context["result"].stdout == "%s: Apply a code\n" % named


# --- Then: bindings ---------------------------------------------------------------------------------------------

@then('it reports tests/test_cart.py, line 12, the title "Apply a code" and the feature cart.feature')
def reports_binding(context):
    assert context["result"].stdout == 'tests/test_cart.py:12: no scenario titled "Apply a code" in cart.feature\n'


@then("it says that every binding names a scenario")
def says_all_bound(context):
    assert context["result"].stdout == "every binding names a scenario\n", context["result"].stderr


@then('each of those binding calls names "Apply a voucher"')
def each_names_voucher(repo, context):
    assert context["result"].returncode == 0, context["result"].stderr
    names = [n for n in context["modules"] if context["count"]]
    for name in names:
        text = (repo / name).read_text()
        assert '"Apply a code")' not in text
        assert '"Apply a voucher")' in text


@then("nothing else in the test modules is changed")
def nothing_else_changed(repo, context):
    for name, text in context["modules"].items():
        expected = text.replace('"%s")' % context["old_title"], '"Apply a voucher")') if context["count"] else text
        assert (repo / name).read_text() == expected


@then(parsers.re(r"it prints that (?P<count>\d+) bindings were rebound"))
def prints_rebound(context, count):
    assert context["result"].stdout == "%s bindings rebound\n" % count


@then('the binding to features/cart.feature names "Apply a code (deprecated)"')
def cart_bindings_follow(repo, context):
    result = context["result"]
    assert (result.returncode, result.stdout) == (0, "2 bindings rebound\n"), result.stderr
    for name in ("tests/test_cart.py", "tests/test_path.py"):  # the second names the file by a path
        assert (repo / name).read_text() == context["modules"][name].replace('"Apply a code")', '"Apply a code (deprecated)")')


@then("the binding to features/old.feature is unchanged")
def old_binding_unchanged(repo, context):
    assert (repo / "tests/test_old.py").read_text() == context["modules"]["tests/test_old.py"]


@then('it reports features/cart.feature, the title "Apply a code" and that no test binds it')
def reports_unbound(context):
    assert "features/cart.feature: Apply a code | bound by no test" in context["result"].stdout.splitlines()


@then('it reports features/cart.feature, the title "Apply a code" and the calls tests/test_a.py:12 and tests/test_b.py:5')
def reports_bound_twice(context):
    line = "features/cart.feature: Apply a code | bound by tests/test_a.py:12, tests/test_b.py:5"
    assert line in context["result"].stdout.splitlines(), context["result"].stdout
