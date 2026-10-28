"""spec-integration's steps about a round of the kind integrate and an upstream: `spec/index.md` names billing as an
upstream, billing's published spec is kept beside the repository, and the stand-in round drafts a line and gives the lines
of a request into billing. The Thens read the round's brief (what `work run` told it) and the result `work run` kept."""
import json
import os
import subprocess
import sys

from pytest_bdd import given, parsers, then, when

from .conftest import INDEX, SCRIPTS, cap, full
from .supervision_given import repository
from .supervision_integrate_steps import entry
from .supervision_rounds_steps import rounds
from .supervision_world import commit_all, git, starts, write

BILLING = "bounded-context/ex.com/prod/billing"
BILLING_SPEC = "../billing-ctx/spec"     # from the repository's root, as spec/index.md names it
DRAFTS = ".shop/scratch/1-integrate/drafts/spec/capabilities/thing.md"
LINE = "**When** a returned order is refunded, `thing` shall show the customer the refund of the order."
ASK = "**When** an order is returned, `billing` shall give a credit note for the order."


def billing_spec(repo):
    return (repo / BILLING_SPEC).resolve()


@given("spec/index.md names the bounded-context billing as an upstream", target_fixture="plan")
def names_upstream(repo):
    plan = repository(repo)
    write(repo, "spec/index.md", INDEX + "\n## Upstreams\n\n- %s: %s\n" % (BILLING, BILLING_SPEC))
    commit_all(repo, "spec/index.md names billing as an upstream")
    return plan


@given("billing does not yet give a refund of an order")
def billing_gives_no_refund(repo):
    write(repo, BILLING_SPEC + "/capabilities/orders.md", cap("orders", ["- [r1] **When** asked, `orders` shall list the orders."]))
    assert "refund" not in (billing_spec(repo) / "capabilities" / "orders.md").read_text()
    there = billing_spec(repo).parent     # the lines are raised into billing's repository (r135): it is one
    for args in (("init", "-q", "-b", "main"), ("config", "user.name", "Someone"), ("config", "user.email", "someone@example.com"),
                 ("config", "commit.gpgsign", "false"), ("add", "-A"), ("commit", "-q", "-m", "billing")):
        subprocess.run(["git", *args], cwd=there, check=True, capture_output=True)


@given("billing's glossary names a refund of an order a credit note")
def billing_glossary(repo):
    write(repo, BILLING_SPEC + "/index.md", "---\nid: %s\n---\n# billing\n\n## Glossary\n\n"
          "- **credit note**: the refund of an order. Not: refund.\n" % BILLING)


@given("an approved note asks that the customer sees the refund of a returned order")
def approved_note(repo, plan):
    """The note stands as the request i1 fulfils, its one line accepted: the round's input (r44's note is the lines)."""
    write(repo, ".shop/work/i1/initiative.md",
          "---\nid: %s\nkind: initiative\nstatus: proposed\nfulfils: q1\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/requests/q1.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n---\n\n## Lines\n"
          "1. The customer sees the refund of a returned order.\n\n## Outcomes\n1. accepted\n" % full("request", "q1"))
    commit_all(repo, "i1 fulfils q1, the approved note")
    plan["round:integrate"] = {"status": "DONE", "write": {DRAFTS: cap("thing", ["- [r2] " + LINE])}, "fields": {
        "changes": [entry("thing", "adds thing#r2")], "requests": [{"upstream": BILLING, "lines": [ASK]}]}}
    plan["initiative-round"] = {"status": "DONE"}


REFUNDS_DRAFTS = ".shop/scratch/1-integrate/drafts/round-1/spec/capabilities/refunds.md"
REFUND_LINE = "**When** an order is cancelled, `refunds` shall show the customer the refund of the order."


@given(parsers.re(r"spec/index.md's glossary has the terms (?P<first>\w+) and (?P<second>\w+)$"), target_fixture="plan")
def glossary_with_terms(repo, first, second):
    plan = repository(repo)
    write(repo, "spec/index.md", INDEX + "\n## Glossary\n\n- **%s**: a thing.\n- **%s**: a thing.\n" % (first, second))
    commit_all(repo, "spec/index.md's glossary")
    return plan


@given("an approved note asks that the customer sees the refund of a cancelled order")
def cancelled_note(repo, plan):
    approved_note(repo, plan)


@given("that note adds the term refund, changes the term order and removes the term basket")
def note_terms(plan):
    plan["round:integrate"] = {"status": "DONE", "write": {REFUNDS_DRAFTS: cap("refunds", ["- [r1] " + REFUND_LINE])}, "fields": {
        "changes": [entry("refunds", "adds refunds#r1"), {"glossary": True, "adds": ["term/refund"],
                                                          "changes": ["term/order"], "removes": ["term/basket"]}]}}


def kept_changes(repo, context):
    results = sorted((repo / ".shop/work/i1/runs/i1").glob("*-integrate/result.json"))
    assert len(results) == 1, (git(repo, "ls-files"), context["done"].stdout, context["done"].stderr)
    return json.loads(results[0].read_text()).get("changes") or []


def entry_of(repo, context, whose):
    found = [e for e in kept_changes(repo, context) if (e.get("glossary") if whose == "glossary" else e.get("capability") == whose)]
    assert len(found) == 1, (kept_changes(repo, context), context["done"].stdout, context["done"].stderr)
    return found[0]


@then("the round drafts a line under the capability refunds that the customer sees the refund of a cancelled order")
def drafts_refunds_line(repo, context):
    drafts = sorted((repo / ".shop/work/i1/runs/i1").glob("*-integrate/drafts/round-*/spec/capabilities/refunds.md"))
    assert any("refund of the order" in p.read_text() for p in drafts), (drafts, context["done"].stdout, context["done"].stderr)
    assert (repo / ".shop/work/i1/refunds.md").is_file(), (git(repo, "ls-files", ".shop/work"), context["done"].stderr)


@then("the round drafts a change to the glossary")
def drafts_glossary_change(repo, context):
    brief = integrate_brief(repo, context)
    assert "glossary" in brief and "no capability's entry" in brief, brief
    assert entry_of(repo, context, "glossary")


@then(parsers.re(r"the change list's entry for the glossary gives (?P<a>\w+) as added, (?P<c>\w+) as changed and (?P<r>\w+) as removed$"))
def glossary_entry_gives(repo, context, a, c, r):
    one = entry_of(repo, context, "glossary")
    assert (one["adds"], one["changes"], one["removes"]) == (["term/" + a], ["term/" + c], ["term/" + r]), one


@then("the change list's entry for refunds gives none of the terms refund, order and basket")
def refunds_entry_no_terms(repo, context):
    one = entry_of(repo, context, "refunds")
    ids = one["adds"] + one["changes"] + one["removes"]
    assert ids and not [i for i in ids if i.startswith("term/")], one


SHIP = "The customer is told when an order ships."
SHIP_DRAFTS = ".shop/scratch/1-integrate/drafts/round-1/spec/capabilities/notifications.md"


@given("a request whose accepted lines ask that the customer sees the status of an order", target_fixture="plan")
def status_request(repo):
    plan = repository(repo)
    write(repo, ".shop/work/i1/initiative.md",
          "---\nid: %s\nkind: initiative\nstatus: proposed\nfulfils: q1\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/work/requests/q1.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n---\n\n## Lines\n"
          "1. The customer sees the status of an order.\n\n## Outcomes\n1. accepted\n" % full("request", "q1"))
    commit_all(repo, "i1 fulfils q1")
    return plan


@given("none of those lines asks that the customer is told when an order ships")
def lines_ask_no_shipping(repo):
    assert "ships" not in (repo / ".shop/work/requests/q1.md").read_text()


@given("an answer that asks that the customer is told when an order ships")
def answer_asks_shipping(repo):
    path = repo / ".shop/work/i1/initiative.md"
    write(repo, ".shop/work/i1/initiative.md", path.read_text() + "\n## Questions\n\n- Anything the customer is told?\n\n"
          "## Answers\n\n- %s Put it under notifications.\n" % SHIP)
    commit_all(repo, "i1 has an answer")


@given("that answer names the capability notifications")
def answer_names_notifications(repo, plan):
    assert "notifications" in (repo / ".shop/work/i1/initiative.md").read_text()
    line = "**When** an order ships, `notifications` shall tell the customer that the order has shipped."
    plan["round:integrate"] = {"status": "DONE", "write": {SHIP_DRAFTS: cap("notifications", ["- [r1] " + line])}, "fields": {
        "changes": [entry("notifications", "adds notifications#r1")]}}
    plan["initiative-round"] = {"status": "DONE"}


@when("work run starts a round of the kind integrate given that request and that answer")
@when("work run starts a round of the kind integrate on that note")
def run_integrate(repo, plan, context):
    stub = repo.parent / "stub"
    (stub / "plan.json").write_text(json.dumps(plan))
    env = dict({k: v for k, v in os.environ.items() if k != "SHOPSYSTEM_WORK_RUN_WORKER"},
               PATH="%s%s%s" % (stub / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(stub / "bin" / "claude"), STUB_CLAUDE_PLAN=str(stub / "plan.json"),
               STUB_CLAUDE_CALLS=str(stub / "calls.jsonl"), PYTEST_XDIST_AUTO_NUM_WORKERS="2",
               CLAUDE_CONFIG_DIR=str(stub / "claude"))
    kept = [p for p in env.get("PYTHONPATH", "").split(os.pathsep) if p and not (os.path.exists(os.path.join(p, "work_items.py")))]
    env["PYTHONPATH"] = os.pathsep.join(kept)
    context["done"] = __import__("subprocess").run([sys.executable, str(SCRIPTS / "work"), "run", "i1"], cwd=repo, env=env,
                                                   capture_output=True, text=True, timeout=300)


def integrate_brief(repo, context):
    found = rounds(repo, "integrate", "i1")
    assert len(found) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    return found[0]["brief"]


def kept_requests(repo, context):
    """The `requests` of the result `work run` kept with the integrate round's stage directory."""
    results = sorted((repo / ".shop/work/i1/runs/i1").glob("*-integrate/result.json"))
    assert len(results) == 1, (git(repo, "ls-files"), context["done"].stdout, context["done"].stderr)
    return json.loads(results[0].read_text()).get("requests")


@then("the round drafts a line that needs a refund of an order")
def drafts_refund_line(repo, context):
    drafts = sorted((repo / ".shop/work/i1/runs/i1").glob("*-integrate/drafts/spec/capabilities/*.md"))
    assert any("refund" in p.read_text() for p in drafts), (drafts, context["done"].stdout, context["done"].stderr)


@then("the round's result gives the lines of a request into billing")
def result_gives_request(repo, context):
    brief = integrate_brief(repo, context)
    assert BILLING in brief and "`requests`" in brief, brief
    given = kept_requests(repo, context)
    assert given and any(r.get("upstream") == BILLING and r.get("lines") for r in given), given


@then("those lines ask for a credit note, in billing's terms")
def lines_in_billing_terms(repo, context):
    brief = integrate_brief(repo, context)
    assert str(billing_spec(repo)) in brief and "glossary" in brief, brief
    lines = " ".join(l for r in kept_requests(repo, context) for l in r["lines"])
    assert "credit note" in lines and "refund" not in lines, lines


@then("the round drafts, under notifications, a line that the customer is told when an order ships")
def drafts_shipping_line(repo, context):
    brief = integrate_brief(repo, context)
    assert SHIP in brief and "notifications" in brief and "asks for lines the request's accepted lines do not" in brief, brief
    drafts = sorted((repo / ".shop/work/i1/runs/i1").glob("*-integrate/drafts/round-*/spec/capabilities/notifications.md"))
    assert any("ships" in p.read_text() for p in drafts), (drafts, context["done"].stdout, context["done"].stderr)
    proposals = git(repo, "ls-files", ".shop/work")
    assert "notifications" in proposals, proposals
