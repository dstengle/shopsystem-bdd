"""feature-file-tools' Givens for trees (verify-moved) and test modules (bindings, rebind)."""
from pytest_bdd import given, parsers

from .feature_file_tools_files import binding, feature_text, scenario_text, store, write

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
    write(repo, "features/codes.feature", feature_text(scenario_text("Checkout")))  # a destination a move may name


@given('features/cart.feature and features/old.feature both have the title "Apply a code"')
def both_have_title(repo, context):
    write(repo, "features/codes.feature", feature_text(scenario_text("Empty cart")))
    for path in ("features/cart.feature", "features/old.feature"):
        write(repo, path, feature_text(scenario_text("Apply a code")))
    context["exact_files"] = True


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


@given(parsers.re(r'(?P<path>\S+) has the scenarios "(?P<one>[^"]+)" and "(?P<two>[^"]+)"'))
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
