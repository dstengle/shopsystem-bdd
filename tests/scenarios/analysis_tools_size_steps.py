"""analysis-tools' steps for `tools size` (r50-r52): the tracked, edited and untracked files a Given writes, and
the lines the Thens read."""
import re

from pytest_bdd import given, parsers, then

from .analysis_tools_probe_steps import a_python_project
from .analysis_tools_project import lines, put

LISTED = re.compile(r"(\S+?) of (\d+) lines?")


def body(count):
    return "".join("x%d = %d\n" % (n, n) for n in range(count))


@given("a Python project in git")
def python_project_in_git(repo, context):
    a_python_project(repo, context)


@given(parsers.re(r"it tracks (?P<what>\S+ of \d+ lines.*)"))
def tracks_listed(repo, what):
    put(repo, {name: body(int(count)) for name, count in LISTED.findall(what)})


@given(parsers.parse("it tracks {path}, with no extension, a python shebang and {count:d} lines"))
def tracks_shebang(repo, path, count):
    put(repo, {path: "#!/usr/bin/env python3\n" + body(count - 1)})


@given(parsers.parse("it tracks {path}, committed at {before:d} lines and edited in the working tree to {after:d} lines"))
def tracks_edited(repo, path, before, after):
    put(repo, {path: body(before)})
    (repo / path).write_text(body(after))


@given(parsers.parse("it has an untracked {path} of {count:d} lines"))
def has_untracked(repo, path, count):
    (repo / path).write_text(body(count))


def printed(context):
    return {line.split()[0]: line for line in lines(context)}


@then(parsers.re(r"tools prints (?P<what>\S+ with \d+ lines(?:, | and ).*)"))
def prints_files(context, what):
    wanted = re.findall(r"(\S+) with (\d+) lines", what)
    assert sorted(printed(context)) == sorted(name for name, _ in wanted), lines(context)
    for name, count in wanted:
        assert printed(context)[name].split() == [name, count], lines(context)
    context["printed"] = {name for name, _ in wanted}


@then(parsers.re(r"tools prints (?P<path>\S+) with (?P<count>\d+) lines"))
def prints_one(context, path, count):
    assert printed(context).get(path, "").split() == [path, count], lines(context)


@then("it prints no other file")
def prints_no_other(context):
    assert set(printed(context)) == context["printed"], lines(context)


@then(parsers.parse("it does not print {path}"))
def does_not_print(context, path):
    assert path not in printed(context), lines(context)
