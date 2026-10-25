"""supervision's steps about a `work run` started with no initiative (r66, r81, r82): the initiatives it finds, the nodes
that cannot move or wait for the person, and what it prints of each initiative it took."""
import re

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_world import calls, commit_all, fields, item_text, write


def initiative_file(repo, name, status):
    write(repo, ".shop/work/%s/initiative.md" % name, "---\nid: %s\nkind: initiative\nstatus: %s\n---\n" % (
        full("initiative", name), status))


def proposal_file(repo, initiative, name, status, questions=()):
    asked = "\n## Questions\n\n%s" % "".join("- %s\n" % q for q in questions) if questions else ""
    write(repo, ".shop/work/%s/%s.md" % (initiative, name),
          "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: %s\nargues: [thing]\nadds: [thing#r1]\n"
          "changes: []\nremoves: []\ndate: 2026-10-15\n---\n%s" % (
              full("capability-proposal", name), full("initiative", initiative), status, asked))


def stuck_item(repo, initiative, name):
    """A work-item that can make no transition, and waits for no one: it is blocked_by one that is never green."""
    write(repo, ".shop/work/%s/%s.md" % (initiative, name), item_text(name, "drafted", blocked_by=["nothing"]))


@given(parsers.re(r"i1 is started, and i1's (?P<kind>work-item|capability-proposal) (?P<name>\w+) is (?P<status>[\w-]+)$"))
def i1_node(repo, kind, name, status):
    asked = ["Which module owns the log?"] if status == "awaiting-answer" else []
    if kind == "capability-proposal":
        proposal_file(repo, "i1", name, status, asked)
    else:
        text = item_text(name, status) + ("\n## Questions\n\n- Which module owns the log?\n" if asked else "")
        write(repo, ".shop/work/i1/%s.md" % name, text)
    commit_all(repo, "i1's %s %s is %s" % (kind, name, status))


@given("i1 is started, none of its nodes can make a transition and none of them is awaiting-answer or failed")
def idle_i1(repo):
    stuck_item(repo, "i1", "w1")
    commit_all(repo, "i1 has nothing to do")


@given("an initiative i2 under .shop/work/, started, none of whose nodes can make a transition and none of which is "
       "awaiting-answer or failed")
def idle_i2(repo):
    initiative_file(repo, "i2", "started")
    stuck_item(repo, "i2", "w2")
    commit_all(repo, "i2 has nothing to do")


@given("an initiative i3 under .shop/work/ that is done")
def done_i3(repo):
    initiative_file(repo, "i3", "done")
    stuck_item(repo, "i3", "w3")
    commit_all(repo, "i3 is done")


@given("i1's capability-proposal p1 is drafted and i1's work-item w1 is drafted")
def drafted_proposal_and_item(repo):
    proposal_file(repo, "i1", "p1", "drafted")
    write(repo, ".shop/work/i1/w1.md", item_text("w1", "drafted"))
    commit_all(repo, "i1's p1 and w1 are drafted")


@given("an initiative i2 under .shop/work/ whose capability-proposal p2 is drafted")
def i2_with_proposal(repo):
    initiative_file(repo, "i2", "started")
    proposal_file(repo, "i2", "p2", "drafted")
    commit_all(repo, "i2's p2 is drafted")


@given("an initiative i3 under .shop/work/ that is done and an initiative i4 under .shop/work/ that is abandoned, each "
       "with a work-item that is drafted")
def ended_initiatives(repo):
    for name, status in (("i3", "done"), ("i4", "abandoned")):
        initiative_file(repo, name, status)
        write(repo, ".shop/work/%s/w%s.md" % (name, name[1]), item_text("w" + name[1], "drafted"))
    commit_all(repo, "i3 is done and i4 abandoned")


@given("every round ends and every worker gives DONE, the gate rounds of p1 and p2 each ending once both have started")
def gates_meet(plan):
    plan["default"] = {"status": "DONE"}
    plan["initiative-round"] = {"status": "DONE", "meet": 2, "questions": ["Which module owns the log?"]}


@given(parsers.re(r'an initiative (?P<name>i\d) under \.shop/work/ whose capability-proposal (?P<prop>p\d) is awaiting-answer, '
                  r'its ## Questions section with "(?P<asked>[^"]+)", and its Answers section with "(?P<answer>[^"]+)"$'))
def answered_initiative(repo, name, prop, asked, answer):
    initiative_file(repo, name, "started")
    proposal_file(repo, name, prop, "awaiting-answer", [asked])
    path = repo / (".shop/work/%s/%s.md" % (name, prop))
    path.write_text(path.read_text() + "\n## Answers\n\n- %s\n" % answer)
    commit_all(repo, "%s's %s is answered" % (name, prop))


@given("every round ends, each round of the kind integrate, apply or formulate ending only after long enough for another "
       "round to start beside it")
def rounds_linger(plan):
    plan["default"] = {"status": "DONE"}
    plan["initiative-round"] = {"status": "DONE", "linger": 1}


def serial_rounds(repo):
    """(kind, name, start, end) of each round of the kind integrate, apply or formulate, by where it started."""
    found = []
    for _, brief, start, end in sessions(repo):
        kind = re.search(r"^# (integrate|apply|formulate) of (\w+)", brief, re.M)
        if kind:
            found.append((kind.group(1), kind.group(2), start, end))
    return sorted(found, key=lambda r: r[2])


@then("a round of the kind integrate was started for i1, and a round of the kind apply for each of p2 and p3")
def serial_rounds_started(repo, context):
    got = [(kind, name) for kind, name, _, _ in serial_rounds(repo)]
    assert ("integrate", "i1") in got and ("apply", "p2") in got and ("apply", "p3") in got, (got, context["done"].stderr)


@then("no round of the kind integrate, apply or formulate was started before every other round of those kinds had ended")
def serial_rounds_apart(repo, context):
    found = serial_rounds(repo)
    assert len(found) >= 3, (found, context["done"].stderr)
    for (_, _, _, ended), (_, _, started, _) in zip(found, found[1:]):
        assert ended < started, found


def sessions(repo):
    """(initiative, brief, start, end): each session of the stand-in's record, with where in it it started and ended."""
    events = calls(repo)
    found = []
    for i, call in enumerate(events):
        if call["event"] == "start":
            end = next((j for j, e in enumerate(events) if e["event"] == "end" and e["session"] == call["session"]), len(events))
            owner = re.search(r"\.shop/work/(i\d)/", call["brief"])
            found.append((owner.group(1) if owner else None, call["brief"], i, end))
    return found


@then("the gate rounds of p1 and p2 ran at the same time")
def gates_together(repo, context):
    gates = {name: (s, e) for _, brief, s, e in sessions(repo) for name in ("p1", "p2") if "# gate of %s" % name in brief}
    assert sorted(gates) == ["p1", "p2"], (gates, context["done"].stderr)
    (s1, e1), (s2, e2) = gates["p1"], gates["p2"]
    assert s1 < e2 and s2 < e1, gates


@then("no two sessions of i1 ran at the same time")
def i1_one_at_a_time(repo, context):
    mine = [(s, e) for owner, _, s, e in sessions(repo) if owner == "i1"]
    assert len(mine) >= 2, (sessions(repo), context["done"].stderr)
    assert not [1 for n, (s1, e1) in enumerate(mine) for s2, e2 in mine[n + 1:] if s1 < e2 and s2 < e1], mine


@then("no session was started for i3 or i4")
def none_for_ended(repo):
    assert not [o for o, _, _, _ in sessions(repo) if o in ("i3", "i4")], sessions(repo)


@then("w1 is green, and p1 and p2 are awaiting-answer")
def green_and_awaiting(repo, context):
    where = (context["done"].stdout, context["done"].stderr)
    assert fields(repo / ".shop/work/i1/w1.md")["status"] == "green", where
    assert fields(repo / ".shop/work/i1/p1.md")["status"] == "awaiting-answer", where
    assert fields(repo / ".shop/work/i2/p2.md")["status"] == "awaiting-answer", where


@then(parsers.re(r"`work run` prints (?P<first>\w+) with (?P<status>[\w-]+) and (?P<second>\w+) with (?P<status2>[\w-]+)"
                 r"(?:, and does not print (?P<absent>\w+))?$"))
def prints_initiatives(context, first, status, second, status2, absent):
    out = context["done"].stdout.splitlines()
    for name, state in ((first, status), (second, status2)):
        assert [l for l in out if l.split() == [name, state]], (name, state, out)
    assert absent is None or not [l for l in out if absent in re.findall(r"\w+", l)], out
