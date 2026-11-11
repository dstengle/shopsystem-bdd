"""The trace of `pr-review` (workflow simplification plan 5, D19): a guarantees capability has no feature file, so no
strict xfail holds its ids. Instead each id out of `unbuilt:` must have a test marked
`@pytest.mark.requirement("pr-review#r<n>")` in one of the files of `PR_REVIEW_TESTS`, a test in a class included,
and each id still in `unbuilt:` must have none. A marked test that is also marked `skip`, `skipif` or `xfail` does
not count, and is refused (plan 5 review, M7). The marks are read from the files' syntax trees."""
import ast
import re
from pathlib import Path

import pytest
import spec_unbuilt

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PR_REVIEW_TESTS = ("test_batch_findings.py", "test_batch_brief.py", "test_batch_reviewed.py", "test_batch_fix_loop.py",
                   "test_agent_pr_reviewer.py", "test_skill_building_a_batch.py")
CAP = REPO / "spec" / "capabilities" / "pr-review.md"
SKIPS = {"skip", "skipif", "xfail"}


def _mark(decorator):
    """(name, its first argument when a string) of a `pytest.mark.<name>(...)` decorator, else None."""
    call = decorator.func if isinstance(decorator, ast.Call) else decorator
    if not (isinstance(call, ast.Attribute) and isinstance(call.value, ast.Attribute) and call.value.attr == "mark"):
        return None
    args = decorator.args if isinstance(decorator, ast.Call) else []
    first = args[0].value if args and isinstance(args[0], ast.Constant) and isinstance(args[0].value, str) else None
    return call.attr, first


def marked(source, capability, where="<source>"):
    """{r<n>} of the tests in `source` marked as requirements of `capability`; a marked test also skipped or
    xfailed is refused, naming it."""
    found = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
            continue
        marks = [m for m in map(_mark, node.decorator_list) if m]
        ids = {m[1].split("#", 1)[1] for m in marks if m[0] == "requirement" and m[1]
               and m[1].startswith(capability + "#")}
        if ids and SKIPS & {m[0] for m in marks}:
            raise AssertionError("%s: %s is a requirement's test and is skipped or xfailed" % (where, node.name))
        found |= ids
    return found


def marked_tests():
    found = set()
    for name in PR_REVIEW_TESTS:
        path = HERE / name
        if path.is_file():
            found |= marked(path.read_text(), "pr-review", name)
    return found


def ids():
    return set(re.findall(r"(?m)^- \[(r[1-9]\d*)\] ", CAP.read_text()))


def test_every_built_pr_review_line_has_its_test():
    built = ids() - spec_unbuilt.unbuilt(REPO).get("pr-review", set())
    missing = sorted(built - marked_tests(), key=lambda r: int(r[1:]))
    assert not missing, "pr-review ids out of unbuilt: with no test marked requirement: %s" % ", ".join(missing)


def test_no_unbuilt_pr_review_line_has_a_test_yet():
    early = sorted(spec_unbuilt.unbuilt(REPO).get("pr-review", set()) & marked_tests(), key=lambda r: int(r[1:]))
    assert not early, "pr-review ids still in unbuilt: with a test marked requirement: %s" % ", ".join(early)


MARKED = '''
import pytest

@pytest.mark.requirement("pr-review#r1")
def test_one():
    pass

@pytest.mark.requirement("other#r2")
def test_r2_of_another_capability():
    pass

def test_r3_named_but_not_marked():
    pass

class TestIn:
    @pytest.mark.requirement("pr-review#r17")
    def test_in_a_class(self):
        pass
'''


def test_the_marks_are_read_by_capability_and_in_a_class():
    assert marked(MARKED, "pr-review") == {"r1", "r17"}


@pytest.mark.parametrize("skip", ["skip", "xfail", 'skipif(True, reason="x")'])
def test_a_skipped_requirement_test_is_refused(skip):
    source = MARKED.replace('@pytest.mark.requirement("pr-review#r1")',
                            '@pytest.mark.requirement("pr-review#r1")\n@pytest.mark.%s' % skip)
    with pytest.raises(AssertionError, match="test_one"):
        marked(source, "pr-review")
