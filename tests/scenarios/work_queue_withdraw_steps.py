"""features/work-queue.feature's steps of `work withdraw` (r10), `work show --json` (r11) and the log lines the commit
scenarios (r9) read."""
import json

from pytest_bdd import given, parsers, then

from .conftest import full
from .work_queue_git_steps import git


@given(parsers.re(r"an initiative (?P<ident>i\d+) under \.shop/work/ whose work-item (?P<name>\w+) is (?P<status>\w+), "
                  r"its last log\.jsonl line for (?P=name) its transition to (?P=status)$"))
def at_status_logged(repo, ident, name, status):
    from .test_work_queue import initiative, log_line, write
    initiative(repo, ident)
    write(repo, ".shop/work/%s/%s.md" % (ident, name), "---\nid: %s\nkind: work-item\npart_of: initiative/%s\nstatus: %s\n"
          "---\n\n# %s\n" % (full("work-item", name), ident, status, name))
    write(repo, ".shop/work/%s/log.jsonl" % ident, log_line(name, "planned", status))


@then(parsers.parse(".shop/work/i1/log.jsonl's last line is {name}'s transition from {before} to {after}"))
def last_is(repo, name, before, after):
    last = json.loads((repo / ".shop/work/i1/log.jsonl").read_text().splitlines()[-1])
    assert (last["work-item"], last["before"], last["after"]) == (name, before, after), last


@then(parsers.re(r"main has a new last commit, which holds (?P<rel>\S+) as work left it and (?P<log>\S+) with "
                 r"(?P<name>\w+)'s transition from (?P<before>[\w-]+)(?: to (?P<after>[\w-]+))? as its last line$"))
def new_commit_holds_both(repo, context, rel, log, name, before, after):
    assert context["done"].returncode == 0, context["done"]
    assert git(repo, "rev-parse", "main").strip() != context["head"], git(repo, "log", "--oneline")
    for path in (rel, log):
        assert git(repo, "show", "main:" + path) == (repo / path).read_text()
    last = json.loads(git(repo, "show", "main:" + log).splitlines()[-1])
    assert (last["work-item"], last["before"]) == (name, before), last
    assert after is None or last["after"] == after, last


@then("work prints one JSON object and nothing else")
def one_json_object(context):
    assert context["done"].returncode == 0, context["done"]
    context["json"] = json.loads(context["done"].stdout)
    assert isinstance(context["json"], dict), context["done"].stdout


def entries(shown):
    """Every (name, initiative, status) the object holds, wherever it nests them."""
    if isinstance(shown, dict):
        if {"initiative", "status"} <= set(shown):
            yield shown.get("work-item", shown.get("name")), shown["initiative"], shown["status"]
        for value in shown.values():
            yield from entries(value)
    elif isinstance(shown, list):
        for value in shown:
            yield from entries(value)


@then(parsers.re(r"it gives (?P<triples>\S+ in \S+ with .+)$"))
def gives(context, triples):
    found = set(entries(context["json"]))
    for triple in triples.replace(" and ", ", ").split(", "):
        name, rest = triple.split(" in ")
        initiative, status = rest.split(" with ")
        assert (name, initiative, status) in found, (triple, context["json"])
