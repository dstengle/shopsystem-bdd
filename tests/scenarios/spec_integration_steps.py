"""spec-integration's steps about a round of the kind integrate and an upstream: `spec/index.md` names billing as an
upstream, billing's published spec is kept beside the repository, and the stand-in round drafts a line and gives the lines
of a request into billing. The Thens read the round's brief (what `work run` told it) and the result `work run` kept."""
import json
import os
import sys

from pytest_bdd import given, then, when

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
