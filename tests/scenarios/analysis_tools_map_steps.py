"""analysis-tools' steps for the coverage map: map, tests-of and untested (r8-r13, r23-r25)."""
import sys

from pytest_bdd import given, parsers, then

from .analysis_tools_probe_steps import a_python_project
from .analysis_tools_project import (
    CART,
    CART_ALL,
    MAP,
    OTHER,
    TEST_CHECKOUT,
    TEST_DISCOUNT,
    TEST_ONLY_TOTAL,
    TEST_TOTAL,
    calls,
    commit,
    interpreter,
    invoke,
    lines,
    mapped,
    put,
    real,
    started,
)


@given("a Python project with the tests test_total and test_discount")
def with_two_tests(repo, context):
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL + TEST_DISCOUNT})
    interpreter(context)


@given(parsers.parse("a map of {count:d} tests made at commit {label}"))
def map_of(context, count, label):
    context["commits"] = {}
    context["planned"] = (count, label)


# what each form of target makes executable: the call both tests make, and the other tests that would show the form ignored
OTHERS = [("test_other_%d" % n, "from other import other", "other()") for n in range(3)]
REFUND = ("test_refund", "from cart import refund", "refund(1)")
PLAIN = ("test_plain", "from cart import total", "total([1])")
FORMS = (("the file", "Cart().total([1])", OTHERS), ("the function", "total([1])", [REFUND] + OTHERS[:2]),
         ("the method", "Cart().total([1])", [PLAIN, REFUND] + OTHERS[:1]), ("lines", "total([1])", [REFUND] + OTHERS[:2]))


@given(parsers.parse("test_total and test_checkout executed {target} and no other test did"))
def executed_target(run, repo, context, target):
    real()
    count, label = context["planned"]
    call, extras = next((call, extras) for form, call, extras in FORMS if target.startswith(form) or form == "the file" and "/" in target)
    assert 2 + len(extras) == count
    files = {"tests/test_cart.py": "from cart import Cart, total\n\n\ndef test_total():\n    assert %s\n" % call,
             "tests/test_checkout.py": "from cart import Cart, total\n\n\ndef test_checkout():\n    assert %s\n" % call,
             "tests/test_extra.py": "".join("%s\n\n\ndef %s():\n    assert %s\n\n\n" % (imp, name, body)
                                            for name, imp, body in extras),
             "src/other.py": OTHER}
    started(repo, files)
    mapped(run, repo, context)
    context["commits"][label] = context["map_commit"]


@given("a map in which two tests in tests/test_cart.py and one test in tests/test_checkout.py executed src/cart.py")
def by_file_map(run, repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL + TEST_DISCOUNT, "tests/test_checkout.py": TEST_CHECKOUT})
    mapped(run, repo, context)


@given("a map has been made")
def a_map_has_been_made(run, repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL})
    mapped(run, repo, context)


@given(parsers.parse("no test in the map executed the function {name} in {path}"))
def nothing_executed(run, repo, context, name, path):
    real()
    count, label = context["planned"]
    tests = "".join("def test_%d():\n    assert total([1]) == 1\n\n\n" % n for n in range(count))
    started(repo, {path: CART + "\n\ndef %s():\n    return 0\n" % name,
                   "tests/test_cart.py": "from cart import total\n\n\n" + tests})
    mapped(run, repo, context)
    context["commits"][label] = context["map_commit"]


@given(parsers.parse("src/cart.py has no function named {name}"))
def no_function_named(repo, context, name):
    assert "def %s" % name not in (repo / "src" / "cart.py").read_text()
    context["absent"] = name


@given("a Python project for which no map has been made")
def no_map(repo, context):
    real()
    a_python_project(repo, context)


@given("a map in which no test executed the function refund in src/cart.py or the function export in src/report.py")
def refund_export_map(repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"src/cart.py": "def total(items):\n    return sum(items)\n\n\ndef refund(order):\n    return -order\n",
               "src/report.py": "def build():\n    return 1\n\n\ndef export():\n    return 2\n"})


@given("every other function in those files was executed by a test")
def the_others_executed(run, repo, context):
    put(repo, {"tests/test_cart.py": "from cart import total\nfrom report import build\n\n\n"
                                     "def test_total():\n    assert total([1]) == 1\n    assert build() == 1\n"})
    mapped(run, repo, context)


@given("a Python project with a map made at an earlier commit")
def earlier_map(run, repo, context):
    real()
    a_python_project(repo, context)
    put(repo, {"tests/test_cart.py": TEST_TOTAL,
               "tests/test_old.py": "from cart import total\n\n\ndef test_old():\n    assert total([1])\n"})
    mapped(run, repo, context)
    earlier = invoke(run, repo, context, ["tests-of", "src/cart.py"]).stdout
    assert "test_old" in earlier


@given(parsers.parse("the project is at commit {label} and its suite {outcome}"))
def new_commit(repo, context, label, outcome):
    (repo / "tests" / "test_old.py").unlink()
    context["last_line"] = "1 passed"
    if outcome != "passes":
        (repo / "tests" / "test_broken.py").write_text("def test_broken():\n    assert False\n")
        context["last_line"] = "1 failed, 1 passed"
    context["commits"][label] = commit(repo)


@given("a Python project in which running the suite under coverage leaves no map")
def leaves_no_map(repo, context):
    a_python_project(repo, context)
    interpreter(context).update(pytest="noop", pytest_out="collected nothing at all")


@given(parsers.parse("a Python project with a map made at commit {label}"))
def map_files_at(repo, context, label):
    a_python_project(repo, context)
    put(repo, {MAP: "the map's data", MAP + ".at": label + "\n"})
    context["map_files"] = {MAP: "the map's data", MAP + ".at": label + "\n"}


@given("running the suite under coverage now leaves no map")
def now_leaves_no_map(context):
    interpreter(context).update(pytest="noop", pytest_out="collected nothing at all")


@then(parsers.parse("the map made at commit {label} is as it was"))
def map_kept(repo, context, label):
    assert {path: (repo / path).read_text() for path in context["map_files"]} == context["map_files"]
    assert sorted(p.name for p in (repo / MAP).parent.iterdir()) == ["coverage", "coverage.at"]


@given(parsers.parse("a map made at commit {label} in which no test executed {count:d} functions in src/cart.py"))
def map_with_lost(run, repo, context, label, count):
    real()
    a_python_project(repo, context)
    text = CART_ALL + "".join("\n\ndef lost_%d():\n    return %d\n" % (n, n) for n in range(count))
    put(repo, {"src/cart.py": text, "tests/test_cart.py": TEST_ONLY_TOTAL})
    mapped(run, repo, context)
    context["commits"][label] = context["map_commit"]
    context["source"] = text


@given("the project has no file src/gone.py")
def no_gone(repo):
    assert not (repo / "src" / "gone.py").exists()


# r8
@then("the suite is run once under coverage with a context for each test")
def suite_once(context):
    runs = [call for call in calls(context["python"]) if call[:2] == ["python", "pytest"]]
    assert len(runs) == 1
    assert "--cov-context=test" in runs[0]
    context["pytest_run"] = runs[0]


@then("only test_total is run")
def only_test_total(repo, run, context):
    assert context["pytest_run"][-2:] == ["-k", "test_total"]
    assert "1 passed" in context["result"].stdout
    listed = run("tools", "--python", sys.executable, "tests-of", "src/cart.py", cwd=repo).stdout
    assert listed.splitlines()[0] == "tests/test_cart.py::test_total"
    assert "test_discount" not in listed


@then(parsers.parse("the map is kept in `{path}`"))
def map_kept_in(repo, path):
    assert path == MAP
    assert (repo / path).is_file()


# r9
@then("tools prints test_total and test_checkout, one a line")
def prints_two(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert lines(context)[:-1] == ["tests/test_cart.py::test_total", "tests/test_checkout.py::test_checkout"]


@then(parsers.parse("it says that is {n:d} of the map's {total:d} tests"))
def says_share(context, n, total):
    assert lines(context)[-1].startswith("%d of the %d tests in the map executed %s (" % (n, total, context["args"][-1]))


@then(parsers.parse("it gives commit {label}"))
def gives_commit(context, label):
    assert lines(context)[-1].endswith("(map made at %s)" % context["commits"][label])


# r10
@then("tools prints tests/test_cart.py with 2 and tests/test_checkout.py with 1")
def by_file(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert lines(context)[:2] == ["tests/test_cart.py 2", "tests/test_checkout.py 1"]


@then("it prints no test names")
def no_test_names(context):
    assert "::" not in context["result"].stdout
    assert "test_total" not in context["result"].stdout


# r11
@then("tools prints that no test of the map executed it")
def prints_none_executed(context):
    assert context["result"].returncode == 0, context["result"].stderr
    assert lines(context) == ["no test of the map executed %s (map made at %s)" % (
        context["args"][-1], context["map_commit"])]


# r12, r26
@then("the command is refused because no map has been made")
def refused_no_map(context):
    assert context["result"].returncode == 1
    assert "no map" in context["result"].stderr




# r13
@then("tools prints refund and export")
def prints_refund_export(context):
    assert lines(context)[:-1] == ["src/cart.py:5 refund", "src/report.py:5 export"]


@then("it prints no other function")
def no_other_function(context):
    assert len(lines(context)) == 3
    assert lines(context)[-1].startswith("2 functions no test executed")


# r23
@then(parsers.parse("the earlier map is replaced by one made at commit {label}"))
def map_replaced(run, repo, context, outside, label):
    later = invoke(run, repo, context, ["tests-of", "src/cart.py"], outside).stdout
    assert "test_old" not in later
    assert "(map made at %s)" % context["commits"][label] in later




# r24
@then("the command is refused because no map was made")
def refused_no_map_made(repo, context):
    assert context["result"].returncode == 1
    assert not (repo / MAP.replace("coverage", "coverage.at")).exists()




# r25
@then("tools prints each of those functions")
def lost_functions(context):
    source = context["source"].splitlines()
    count = len(lines(context)) - 1
    want = ["src/cart.py:%d lost_%d" % (source.index("def lost_%d():" % n) + 1, n) for n in range(count)]
    assert lines(context)[:-1] == want


@then(parsers.parse("it says {count:d} functions no test executed and gives commit {label}"))
def says_count(context, count, label):
    assert lines(context)[-1] == "%d functions no test executed, in the map made at %s" % (
        count, context["commits"][label])
    assert len(lines(context)) - 1 == count
