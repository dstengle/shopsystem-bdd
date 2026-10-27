"""Probe of r45 today: an integrate round for i1 whose request q1 has accepted lines and an answer naming notifications.
Uses the scenario steps' own helpers (repository, run_integrate, rounds) in a repository under this scratch directory."""
import shutil
from pathlib import Path

from tests.scenarios.conftest import cap, full
from tests.scenarios.spec_integration_steps import run_integrate
from tests.scenarios.supervision_given import repository
from tests.scenarios.supervision_rounds_steps import rounds
from tests.scenarios.supervision_world import commit_all, write

HERE = Path(__file__).resolve().parent
DRAFTS = ".shop/scratch/1-integrate/drafts/spec/capabilities/notifications.md"
LINE = "**When** an order ships, `notifications` shall tell the customer that the order shipped."


class Ctx(dict):
    pass


def case(name, answer_in_request=None, answer_in_initiative=None):
    base = HERE / name
    shutil.rmtree(base, ignore_errors=True)
    repo = base / "repo"
    repo.mkdir(parents=True)
    plan = repository(repo)
    write(repo, ".shop/work/i1/initiative.md",
          "---\nid: %s\nkind: initiative\nstatus: proposed\nfulfils: q1\n---\n" % full("initiative", "i1")
          + ("\n## Questions\n- line 1: does the customer hear when the order ships?\n\n## Answers\n- %s\n" % answer_in_initiative
             if answer_in_initiative else ""))
    answers = ("\n## Questions\n1. line 1: does the customer hear when the order ships?\n\n## Answers\n1. %s\n"
               % answer_in_request) if answer_in_request else "\n## Questions\n\n## Answers\n"
    write(repo, ".shop/work/requests/q1.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n---\n\n## Lines\n"
          "1. The customer sees the status of an order.\n\n## Outcomes\n1. accepted\n%s" % (full("request", "q1"), answers))
    commit_all(repo, "i1 fulfils q1 with an answer")
    plan["round:integrate"] = {"status": "DONE", "write": {DRAFTS: cap("notifications", ["- [r1] " + LINE])}, "fields": {
        "changes": [{"capability": "notifications", "adds": ["notifications#r1"], "changes": [], "removes": []}]}}
    plan["initiative-round"] = {"status": "DONE"}
    ctx = Ctx()
    run_integrate(repo, plan, ctx)
    found = rounds(repo, "integrate", "i1")
    print("\nCASE", name, "returncode", ctx["done"].returncode)
    print("stderr tail:", ctx["done"].stderr[-600:])
    print("integrate rounds started:", len(found))
    for c in found[:1]:
        print("BRIEF lines:")
        for l in c["brief"].splitlines():
            if l.startswith(("Request", "Accepted", "- 1.", "Answers", "- Question", "  Answer", "Ids drafted")):
                print("   ", l)
    drafts = sorted((repo / ".shop/work/i1/runs/i1").glob("*-integrate/drafts/spec/capabilities/*.md"))
    print("kept drafts:", [str(p.relative_to(repo)) for p in drafts])


def test_answer_in_request():
    case("case_request_answer", answer_in_request="The customer is told when an order ships, under notifications.")


def test_answer_in_initiative():
    case("case_initiative_answer", answer_in_initiative="The customer is told when an order ships, under notifications.")
