"""feature-file-tools' Givens for feature files: the scenarios, tags, Backgrounds and titles a scenario's files hold."""
import re

from pytest_bdd import given, parsers

from .feature_file_tools_files import feature_text, NOTE_WITH, outline_text, RULE, scenario_text, store, titles_in, write


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
