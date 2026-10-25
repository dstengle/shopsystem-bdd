"""features/work-queue.feature's steps of `work add` numbering its work-items (r1, r12): the id it prints, the file it writes."""
from pytest_bdd import given, parsers, then

from .conftest import full


@given(parsers.re(r"an initiative (?P<ident>i\d+) under \.shop/work/$"))
def bare_initiative(repo, ident):
    from .test_work_queue import initiative
    initiative(repo, ident)


@then(parsers.parse("work prints one id w<n>, and nothing else"))
def prints_one_id(context):
    done = context["done"]
    assert done.returncode == 0, done
    lines = done.stdout.splitlines()
    assert len(lines) == 1 and lines[0].startswith("w") and lines[0][1:].isdigit(), done.stdout
    context["printed"] = lines[0]


@then(parsers.re(r"work prints (?P<ident>w\d+)$"))
def prints_id(context, ident):
    done = context["done"]
    assert done.returncode == 0 and done.stdout.split() == [ident], done
    context["printed"] = ident


@then(parsers.re(r"the add is refused because (?P<ident>i\d+) is (?P<status>\w+), naming (?P=status)$"))
def add_refused_for_status(context, ident, status):
    done = context["done"]
    assert done.returncode == 1, done
    assert done.stdout == "" and status in done.stderr, done


def _fields(path):
    from .test_work_queue import fields
    return fields(path)


@then(parsers.parse(".shop/work/{initiative}/w<n>.md is a drafted work-item whose id is that w<n>"))
def drafted_that(repo, context, initiative):
    ident = context["printed"]
    data = _fields(repo / f".shop/work/{initiative}/{ident}.md")
    assert (data.get("id"), data.get("kind"), data.get("status")) == (full("work-item", ident), "work-item", "drafted"), data


@then(parsers.re(r"\.shop/work/(?P<initiative>\w+)/(?P<name>w\d+)\.md is a drafted work-item whose id is (?P=name)$"))
def drafted_named(repo, context, initiative, name):
    data = _fields(repo / f".shop/work/{initiative}/{name}.md")
    assert (data.get("id"), data.get("kind"), data.get("status")) == (full("work-item", name), "work-item", "drafted"), data


@then(parsers.parse("its `# ` heading is {title}"))
def heading_is(repo, context, title):
    text = (repo / ".shop/work/i1/{}.md".format(context["printed"])).read_text()
    assert "\n# %s\n" % title in text, text


@then("no other work-item's file has changed")
def no_other_changed(repo, context):
    from .test_work_queue import snapshot
    now = snapshot(repo)
    new = ".shop/work/i1/%s.md" % context["printed"]
    assert new not in context["before"], new
    work = {k: v for k, v in now.items() if k.startswith(".shop/work/") and k != new}   # add commits, so .git moves
    assert work == {k: v for k, v in context["before"].items() if k.startswith(".shop/work/")}
