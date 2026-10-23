"""supervision's steps about workers running side by side (r20, r59 to r63): the work-items and the stand-in's
orders they need, and the Thens that read when each worker ran, its worktree, the order of the merges and the
transcript a stage's session.json records."""
import json
from pathlib import Path

from pytest_bdd import given, parsers, then

from .supervision_world import (
    AGENTS,
    ROLES,
    calls,
    commit_all,
    git,
    item_text,
    option,
    starts,
    work_item_of,
    write,
)


@given(parsers.re(r"i1's work-items (?P<first>\w+) is (?P<status>[\w-]+), its blocked_by naming (?P<by>\w+), and "
                  r"(?P<other>\w+) is (?P<other_status>[\w-]+)$"))
def blocked_item(repo, first, status, by, other, other_status):
    write(repo, ".shop/work/i1/%s.md" % first, item_text(first, status, blocked_by=[by]))
    write(repo, ".shop/work/i1/%s.md" % other, item_text(other, other_status))
    commit_all(repo, "a blocked work-item")


@given(parsers.re(r"i1's work-items (?P<names>\w+(?:, \w+)+ and \w+) are (?P<status>[\w-]+)$"))
def many_items(repo, names, status):
    for name in names.replace(" and ", ", ").split(", "):
        write(repo, ".shop/work/i1/%s.md" % name, item_text(name, status))
    commit_all(repo, "work-items")


@given(".shop/delivery.toml gives 2 as its number of workers")
def two_workers(repo):
    path = repo / ".shop/delivery.toml"
    path.write_text("workers = 2\n" + path.read_text())     # a top-level key, above the file's first table
    commit_all(repo, "the number of workers")


@given(".shop/delivery.toml gives no number of workers")
def no_workers(repo):
    assert "workers" not in (repo / ".shop/delivery.toml").read_text()


@given(parsers.re(r"every worker gives DONE, each researcher ending once (?P<n>\d+) workers have started$"))
def researchers_meet(plan, n):
    plan["default"] = {"status": "DONE"}
    plan["code-scout"] = {"meet_all": int(n)}


@given("every worker gives DONE, the researcher of w1 and the planner of w2 each ending once both have started")
def research_meets_plan(plan):
    plan["default"] = {"status": "DONE"}
    plan["code-scout"] = plan["bdd-planner"] = {"meet_agents": ["code-scout", "bdd-planner"]}


def spans(repo, only=None):
    """(agent, work-item, start, end): where in the stand-in's record each worker started and ended."""
    events = calls(repo)
    found = []
    for i, c in enumerate(events):
        if c["event"] == "start" and (only is None or c["agent"] == "shopsystem-bdd:" + only):
            end = next((j for j, e in enumerate(events) if e["event"] == "end" and e["session"] == c["session"]), len(events))
            found.append((c["agent"], work_item_of(c), i, end))
    return found


@then(parsers.re(r"the (?P<first>researcher|planner|implementer) of (?P<one>\w+) and the (?P<second>researcher|planner|"
                 r"implementer) of (?P<two>\w+) worked at the same time$"))
def worked_together(repo, context, first, one, second, two):
    def span(role, name):
        found = [(s, e) for a, n, s, e in spans(repo, ROLES[role]) if n == name]
        assert len(found) == 1, (role, name, found, context["done"].stderr)
        return found[0]
    (s1, e1), (s2, e2) = span(first, one), span(second, two)
    assert s1 < e2 and s2 < e1, ((s1, e1), (s2, e2))


@then(parsers.re(r"(?P<limit>\d+) workers worked at the same time, and never more$"))
def at_most_workers(repo, context, limit):
    found = spans(repo)
    most = max((len([1 for _, _, s, e in found if s <= i < e]) for _, _, i, _ in found), default=0)
    assert most == int(limit), (most, found, context["done"].stderr)


@then("each of them worked in a worktree of its own")
def own_worktrees(repo):
    started = [c for c in starts(repo) if c["agent"] == "shopsystem-bdd:bdd-implementer"]
    places = [Path(c["cwd"]).resolve() for c in started]
    assert len(places) >= 2 and len(set(places)) == len(places) and repo.resolve() not in places, places
    assert sorted(p.name for p in places) == sorted(work_item_of(c) for c in started), places


@then("the initiative branch has w2's implementer's commit and then w1's, with no merge commit")
def merged_in_end_order(repo, context):
    subjects = git(repo, "log", "--reverse", "--no-merges", "main", "--format=%s").splitlines()
    mine = [s for s in subjects if s.startswith("bdd-implementer:")]
    assert mine == ["bdd-implementer: w2.txt", "bdd-implementer: w1.txt"], (mine, context["done"].stderr)
    assert git(repo, "log", "--merges", "main", "--format=%H").strip() == ""


@then("the session.json in each of w1's four stage directories records the path of the transcript of that stage's session")
def records_transcript(repo, context):
    dirs = sorted((repo / ".shop/work/i1/runs/w1").iterdir())
    assert len(dirs) == len(AGENTS), (dirs, context["done"].stderr)
    for path in dirs:
        data = json.loads((path / "session.json").read_text())
        found = Path(data.get("transcript_path", "/none"))
        assert found.is_file() and found.name == data["session_id"] + ".jsonl", (path, data)
        assert option(starts_of(repo, data["session_id"])["argv"], "--session-id") == data["session_id"]


def starts_of(repo, session):
    return next(c for c in starts(repo) if c["session"] == session)


@then(parsers.re(r"no worker was started for (?P<name>\w+)$"))
def none_started_for(repo, context, name):
    assert starts(repo) == [] or all(work_item_of(c) != name for c in starts(repo)), (
        [c["agent"] for c in starts(repo) if work_item_of(c) == name], context["done"].stderr)
