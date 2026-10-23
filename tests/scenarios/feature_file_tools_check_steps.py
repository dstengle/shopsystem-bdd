"""feature-file-tools' Thens for verify-moved and bindings, rebind and --unbound."""
from pytest_bdd import parsers, then

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

@then('it prints tests/test_cart.py, line 12, the title "Apply a code" and the feature cart.feature')
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


@then('the binding to features/cart.feature names "Apply a code (deprecated)"')
def cart_bindings_follow(repo, context):
    result = context["result"]
    assert (result.returncode, result.stdout) == (0, "2 bindings rebound\n"), result.stderr
    for name in ("tests/test_cart.py", "tests/test_path.py"):  # the second names the file by a path
        assert (repo / name).read_text() == context["modules"][name].replace('"Apply a code")', '"Apply a code (deprecated)")')


@then("the binding to features/old.feature is unchanged")
def old_binding_unchanged(repo, context):
    assert (repo / "tests/test_old.py").read_text() == context["modules"]["tests/test_old.py"]


@then('it prints features/cart.feature and the title "Apply a code"')
def reports_unbound(context):
    assert any(line.startswith("features/cart.feature: Apply a code |") for line in context["result"].stdout.splitlines())


@then(parsers.re(r'it prints neither "(?P<one>[^"]+)" nor "(?P<two>[^"]+)"(?P<unbound> as bound by no test)?'))
def prints_neither(context, one, two, unbound):
    out = context["result"].stdout
    for title in (one, two):
        if unbound:
            assert not any(line.endswith(": %s | bound by no test" % title) for line in out.splitlines()), out
        else:
            assert title not in out, out


@then('it prints features/cart.feature, the title "Apply a code" and the calls tests/test_a.py:12 and tests/test_b.py:5')
def reports_bound_twice(context):
    line = "features/cart.feature: Apply a code | bound by tests/test_a.py:12, tests/test_b.py:5"
    assert line in context["result"].stdout.splitlines(), context["result"].stdout
