"""spec-integration's steps about a round of the kind apply: an answered capability-proposal p1 whose kept drafts hold one of
its two answers; the stand-in round applies them and gives, as the contract asks, the answer they do not hold. The Thens
read the round's brief (what `work run` told it) and the result `work run` kept in the apply stage directory."""
import json

from pytest_bdd import given, then, when

from .conftest import INDEX
from .spec_integration_steps import run_integrate
from .supervision_given import repository
from .supervision_rounds_steps import formulate_did_its_work, rounds
from .supervision_world import commit_all, full, starts, write

STATUS = "The customer sees the status of an order."
SHIPS = "The customer is told when an order ships."
KEPT = ".shop/scratch/1-integrate/drafts/round-1"


@given("a capability-proposal whose answers are that the customer sees the status of an order and that the customer is told "
       "when an order ships", target_fixture="plan")
def answered_proposal(repo):
    plan = repository(repo)
    answered_proposal_in(repo)
    return plan


def answered_proposal_in(repo):
    write(repo, ".shop/work/i1/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\n"
          "argues: [thing]\nadds: [thing#r1]\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n\n"
          "The drafts of this proposal are in %s.\n\n## Questions\n\n- Anything shown?\n- Anything told?\n\n"
          "## Answers\n\n- %s\n- %s\n" % (full("capability-proposal", "p1"), full("initiative", "i1"), KEPT, STATUS, SHIPS))
    commit_all(repo, "an answered capability-proposal")


@given("drafts that hold a line that the customer sees the status of an order")
def drafts_hold_status(repo, plan):
    write(repo, KEPT + "/spec/capabilities/thing.md",
          "**When** asked, `thing` shall show the customer the status of an order.\n")
    plan["round:apply"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", "adds": ["thing#r1"]}],
                                                       "unheld_answers": [SHIPS]}}
    plan["initiative-round"] = {"status": "DONE"}
    formulate_did_its_work(plan)


@given("no line of those drafts holds that the customer is told when an order ships")
def drafts_hold_no_shipping(repo):
    assert "ships" not in (repo / KEPT / "spec/capabilities/thing.md").read_text()


@when("work run starts a round of the kind apply on that capability-proposal with those drafts")
def run_apply(repo, plan, context):
    run_integrate(repo, plan, context)


def index_text(repo):
    return (repo / "spec/index.md").read_text()


@given("spec/index.md's glossary has the term order and no term refund", target_fixture="plan")
def glossary_order_only(repo):
    plan = repository(repo)
    write(repo, "spec/index.md", INDEX + "\n## Glossary\n\n- **order**: a thing a customer buys.\n")
    commit_all(repo, "spec/index.md's glossary")
    plan["before"] = index_text(repo)
    return plan


@given("an initiative with a glossary-proposal that adds the term refund and changes the term order")
def initiative_glossary_proposal(repo):
    write(repo, ".shop/work/i1/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: drafted\n"
          "adds: [term/refund]\nchanges: [term/order]\nremoves: []\ndate: 2026-10-28\n---\n\n# glossary\n" % (
              full("glossary-proposal", "g1"), full("initiative", "i1")))
    commit_all(repo, "a glossary-proposal")


@given("the person has not approved the terms of that glossary-proposal")
def terms_not_approved(repo):
    assert "status: approved" not in (repo / ".shop/work/i1/g1.md").read_text()


@given("a capability-proposal of that initiative the person has approved")
def approved_proposal(repo, plan):
    answered_proposal_in(repo)
    write(repo, KEPT + "/spec/capabilities/thing.md", "**When** asked, `thing` shall show the customer the refund of an order.\n")
    commit_all(repo, "an answered capability-proposal")
    plan["round:apply"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", "adds": ["thing#r1"]}]}}
    plan["initiative-round"] = {"status": "DONE"}
    formulate_did_its_work(plan)


@when("work run starts a round of the kind apply on that capability-proposal")
def run_apply_on(repo, plan, context):
    run_integrate(repo, plan, context)


@then("the round applies the capability-proposal's drafts")
def round_applies_proposals_drafts(repo, context):
    round_applies(repo, context)


@then("spec/index.md's glossary has no term refund")
def glossary_no_refund(repo, context):
    assert "refund" not in index_text(repo), index_text(repo)
    brief = apply_round(repo, context)["brief"]
    assert "term/refund" in brief and "Apply none of them to spec/index.md" in brief, brief


@then("spec/index.md's glossary has the term order as it was before the round")
def glossary_order_unchanged(repo, plan, context):
    assert index_text(repo) == plan["before"], index_text(repo)
    assert "term/order" in apply_round(repo, context)["brief"]


def apply_round(repo, context):
    found = rounds(repo, "apply")
    assert len(found) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    return found[0]


def kept_result(repo, context):
    results = sorted((repo / ".shop/work/i1/runs/p1").glob("*-apply/result.json"))
    assert len(results) == 1, (results, context["done"].stdout, context["done"].stderr)
    return json.loads(results[0].read_text())


@then("the round applies those drafts")
def round_applies(repo, context):
    apply_round(repo, context)
    text = (repo / ".shop/work/i1/p1.md").read_text()
    assert "status: awaiting-answer" not in text, (text, context["done"].stderr)


@then("the round's result gives the answer that the customer is told when an order ships")
def result_gives_shipping(repo, context):
    brief = apply_round(repo, context)["brief"]
    assert "`unheld_answers`" in brief and "Answer: %s" % SHIPS in brief, brief
    assert SHIPS in kept_result(repo, context).get("unheld_answers", []), kept_result(repo, context)


@then("the round's result does not give the answer that the customer sees the status of an order")
def result_omits_status(repo, context):
    assert STATUS not in kept_result(repo, context).get("unheld_answers", []), kept_result(repo, context)
