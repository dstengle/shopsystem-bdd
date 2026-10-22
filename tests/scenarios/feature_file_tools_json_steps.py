"""feature-file-tools' --json scenarios (r60, r61, r62): the Givens they add and the Thens that read the one JSON object."""
import json
import re

from pytest_bdd import given, parsers, then

from .feature_file_tools_edit_steps import deprecated_scenario
from .feature_file_tools_files import binding, scenario_text, store, titles_in, write


# --- Given ----------------------------------------------------------------------------------------------------

@given(parsers.re(r'a feature file (?P<path>\S+) with scenarios (?P<titles>"[^"]+" and "[^"]+") tagged @(?P<tag>\S+)'))
def feature_with_tagged_scenarios(repo, context, path, titles, tag):
    store(repo, context, path, *[scenario_text(t, "@" + tag) for t in titles_in(titles)])


@given(parsers.re(r'a feature file (?P<path>\S+) with a scenario "(?P<title>[^"]+)" with no tags'))
def feature_with_untagged_scenario(repo, context, path, title):
    store(repo, context, path, scenario_text(title))


@given(parsers.re(r'a deprecated scenario "(?P<title>[^"]+)" in (?P<path>\S+) deprecated for removal'))
def deprecated_for_removal(repo, context, title, path):
    store(repo, context, path, deprecated_scenario(title, "removal"))


@given(parsers.re(r'(?P<path>\S+) has the scenarios (?P<titles>"[^"]+", "[^"]+" and "[^"]+")'))
def file_has_three(repo, context, path, titles):
    store(repo, context, path, *[scenario_text(t) for t in titles_in(titles)])


@given(parsers.parse('a test module tests/test_cart.py whose line 12 binds the title "{title}" in the feature cart.feature'))
def module_line_12_titled(repo, title):
    write(repo, "tests/test_cart.py", binding(title))


@given('test modules tests/test_a.py and tests/test_b.py binding "Empty cart" in cart.feature at lines 12 and 5, and tests/test_c.py binding "Checkout" in cart.feature')
def modules_binding_empty_cart(repo):
    write(repo, "tests/test_a.py", binding("Empty cart", line=12))
    write(repo, "tests/test_b.py", binding("Empty cart", line=5))
    write(repo, "tests/test_c.py", binding("Checkout"))


# --- Then -----------------------------------------------------------------------------------------------------

@then("the output is one JSON object")
def output_is_one_object(context):
    result = context["result"]
    context["json"] = json.loads(result.stdout)
    assert isinstance(context["json"], dict), result.stdout


@then(parsers.re(r'it gives (?P<pairs>\S+ with "[^"]+"(?:, \S+ with "[^"]+")* and \S+ with "[^"]+")'))
def gives_scenarios(context, pairs):
    wanted = re.findall(r'(\S+) with "([^"]+)"', pairs)
    context["given"] = sorted(wanted)
    assert sorted((s["file"], s["title"]) for s in context["json"]["scenarios"]) == context["given"]


@then("it gives no other scenario")
def gives_no_other(context):
    assert len(context["json"]["scenarios"]) == len(context["given"])


@then(parsers.parse('it gives the binding at {path} line {line:d} of "{title}" in {feature}'))
def gives_wrong_binding(context, path, line, title, feature):
    assert context["json"]["wrong"] == [{"file": path, "line": line, "title": title, "feature": feature}]


@then(parsers.parse('it gives "{one}" in {path} as bound by no test, and "{two}" as bound by {first} and {second}'))
def gives_unbound(context, one, path, two, first, second):
    unbound = {(u["file"], u["title"]): u["bound_by"] for u in context["json"]["unbound"]}
    assert unbound[(path, one)] == []
    assert unbound[(path, two)] == [first, second]
    assert len(unbound) == 2


@then(parsers.re(r'it gives "(?P<title>[^"]+)" deprecated for "(?P<what>[^"]+)", with its replacement in (?P<path>\S+) tagged @(?P<tag>\S+)'))
def gives_deprecated_for_title(context, title, what, path, tag):
    entry = next(d for d in context["json"]["deprecated"] if d["title"] == title)
    assert entry["deprecated_for"] == what
    assert entry["replacement"] == {"file": path, "tags": [tag]}


@then(parsers.re(r'it gives "(?P<title>[^"]+)" deprecated for removal'))
def gives_deprecated_for_removal(context, title):
    entry = next(d for d in context["json"]["deprecated"] if d["title"] == title)
    assert entry["deprecated_for"] == "removal"
    assert entry["replacement"] is None
