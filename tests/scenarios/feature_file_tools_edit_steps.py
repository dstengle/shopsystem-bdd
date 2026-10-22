"""feature-file-tools' steps for the edits: tag, deprecate, deprecated, retire and move (r19, r21, r23, r24)."""
import re

from pytest_bdd import given, parsers, then

from .feature_file_tools_files import feature_text, refused, rejected, scenario_text, store, tag_line_of, titles_in, write


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
    assert tag_line_of((repo / "features/cart.feature").read_text(), "Apply a code") == "  @slice-1 @r7"  # r51: @r7 in place of @r1


@then("features/old.feature is unchanged")
def old_unchanged(run, repo, context):
    cart_text, old_text = context["two_files"]
    old, cart = repo / "features/old.feature", repo / "features/cart.feature"
    assert old.read_text() == old_text
    tagged_cart = cart_text.replace("@slice-1 @r1", "@slice-1 @r7")  # r51
    # --file names the other file as well: the same title, tagged there, leaves the first alone
    done = run("features", "tag", "Apply a code", "r7", "--file", "features/old.feature")
    assert done.returncode == 0, done.stderr
    assert cart.read_text() == tagged_cart
    assert old.read_text() == old_text.replace("@slice-2 @r1", "@slice-2 @r7")
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


# --- Then: moving -----------------------------------------------------------------------------------------------

@then('features/old.feature has "Empty cart" and not "Apply a code"')
def old_holds_empty_cart(repo, context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert (repo / "features/old.feature").read_text() == feature_text(scenario_text("Empty cart"))


@then('the block of "Apply a code" follows "Checkout" at the end of features/cart.feature, unchanged')
def block_follows(repo, context):
    block = scenario_text("Apply a code", "@slice-1", "    Given a cart\n    When a code is applied\n")
    assert (repo / "features/cart.feature").read_text() == context["destination"] + "\n" + block


@then(parsers.re(r'the relocated "(?P<title>[^"]+)" has the steps "(?P<first>[^"]+)" then "(?P<second>[^"]+)"'))
def moved_has_steps(repo, context, title, first, second):
    assert context["result"].returncode == 0, context["result"].stderr
    assert "  Scenario: %s\n    %s\n    %s\n" % (title, first, second) in (repo / "features/cart.feature").read_text()


@then(parsers.re(r'the relocated "(?P<title>[^"]+)" has the tag lines (?P<lines>"[^"]+"(?: then "[^"]+")*), the last directly above its Scenario: line'))
def moved_has_tag_lines(repo, context, title, lines):
    assert context["result"].returncode == 0, context["result"].stderr
    wanted = "".join("  %s\n" % t for t in titles_in(lines))
    assert (repo / "features/cart.feature").read_text().endswith(wanted + "  Scenario: %s\n    Given a step\n" % title)
