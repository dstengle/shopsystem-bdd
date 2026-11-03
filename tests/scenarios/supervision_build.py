"""The repository a supervision scenario's `work run` runs in, built from what its Givens recorded (not a handler
module; loaded by path): the nodes rewritten in the form `work run` reads, the request an initiative fulfils, the
conditions of the remote, the branches, the files and the change list, and the git repository with its remote."""
import json
import re
import shutil
from pathlib import Path

W = None     # supervision_world, set by the handler module that loads this one
FLAKY_FEATURE = "Feature: Thing\n\n  @r1\n  Scenario: it closes\n    Given a thing\n    Then it closes\n"
FLAKY_STEPS = """from pytest_bdd import given, scenarios, then

scenarios("../features/thing.feature")


@given("a thing")
def a_thing():
    pass


@then("it closes")
def closes(request):
    alone = any("::" in str(a) for a in request.config.invocation_params.args)
    with open(%r, "a") as runs:
        runs.write(("alone" if alone else "with") + "\\n")
    assert alone, "it does not close with the others"
"""
ASKED_FROM = {"research": "drafted", "plan": "researched", "implement": "claimed", "review": "done"}
UNCODIFIED = "The drafted requirements are refused by the grammar or the logic check"
ANSWER_LOG = {"time": "2026-10-15T00:00:00+00:00", "before": "drafted", "after": "awaiting-answer", "by": "work run"}


def request_text(name, status, asker="internal", turn="upstream", delegation=None, questions="", outcomes="1. accepted\n"):
    extra = 'delegation: "%s"\n' % delegation if delegation else ""
    return ("---\nid: %s\nkind: request\nasker: %s\nstatus: %s\nturn: %s\n%s---\n\n# %s\n\n## Lines\n1. Line 1 text.\n\n"
            "## Questions\n%s\n## Answers\n\n## Outcomes\n%s\n## Resolution\n"
            % (W.full("request", name), asker, status, turn, extra, name, questions, outcomes))


def questions_of(sv, node):
    return [(q, answered) for q, (on, answered) in sv["questions"].items() if on == node]


def sections(sv, node):
    asked = questions_of(sv, node)
    if not asked:
        return ""
    lead = UNCODIFIED + ": " if node in sv.get("uncodified", ()) else ""
    return ("\n## Questions\n\n%s\n## Answers\n\n%s" % (
        "".join("- %sIs %s right?\n" % (lead, q) for q, _ in asked),
        "".join("- Yes, %s is right.\n" % q for q, answered in asked if answered)))


def named_stage(sv, node):
    """The kind of the stage the scenario's When ends for `node`, if any."""
    return next((sv["stages"][s] for s, n in sv["for"].items() if n == node and s in sv["stages"]), None)


def proposal_text(name, kind, status, initiative, codified, sv):
    lists = ("argues: [%s]\nadds: [%s]\nchanges: []\nremoves: []\n" % (("work-queue", "work-queue#r1") if codified
                                                                      else ("thing", "thing#r1"))
             if kind == "capability-proposal" else "adds: [term/ledger]\nchanges: []\nremoves: []\n")
    return ("---\nid: %s\nkind: %s\npart_of: %s\nstatus: %s\n%sdate: 2026-10-15\n---\n%s"
            % (W.full(kind, name), kind, W.full("initiative", initiative), status, lists, sections(sv, name)))


def initiative_of(rel):
    return rel.split("/")[2]


def steps(context):
    """The texts of the scenario's steps (a Then may need what the Givens do not build, e.g. a transition)."""
    return context.get("steps", [])


def fulfilling(context, sv, name, status):
    """An initiative that fulfils a request: one under a delegation, a `proposed` or bare one, or one an `integrate`
    stage is for (v16a: every initiative fulfils one)."""
    integrate = any(sv["stages"].get(s) == "integrate" and n == name for s, n in sv["for"].items())
    return context.get("delegation") or status == "proposed" or integrate or \
        any(t == "the initiative %s is bare" % name for t in steps(context))


def rewrite_nodes(repo, context, sv, codified):
    """Each node the Givens wrote, in the form `work run` reads; the initiative i1 when none was given."""
    if any(t.startswith("`work run` commits the transition") for t in steps(context)) and len(W.nodes(context)) <= 1:
        W.write(repo, W.WORK + "/i1/w1.md", W.item_text("w1", "drafted", "i1"))     # a transition to commit
        context.setdefault("nodes", {})["w1"] = ("work-item", W.WORK + "/i1/w1.md")
    if not W.nodes(context, "initiative"):
        W.write(repo, W.WORK + "/i1/initiative.md", "---\nid: %s\nkind: initiative\nstatus: started\n---\n"
                % W.full("initiative", "i1"))
        context.setdefault("nodes", {})["i1"] = ("initiative", W.WORK + "/i1/initiative.md")
    fulfilled = {}
    for name, rel in W.nodes(context, "initiative").items():
        text = (repo / rel).read_text()
        target = W.field(text, "fulfils")
        if not target and fulfilling(context, sv, name, W.field(text, "status")):
            target = "q9"
            text = W.set_field(text, "fulfils", W.full("request", "q9"))
            W.write(repo, W.WORK + "/requests/q9.md", request_text("q9", "accepted", delegation=DELEGATION))
        if target:
            fulfilled[target.rsplit("/", 1)[-1]] = name
        (repo / rel).write_text(text)
    for name, rel in W.nodes(context, "request").items():
        status = W.field((repo / rel).read_text(), "status")
        if name in fulfilled:
            text = request_text(name, status, delegation=DELEGATION if context.get("delegation") else None)
        elif status in ("asker", "upstream"):
            text = request_text(name, "awaiting-%s" % status, turn=status, outcomes="",
                                questions="1. line 1: Which unit is the limit in?\n" if status == "asker" else "")
        else:
            text = request_text(name, status, outcomes="" if status == "open" else "1. accepted\n")
        (repo / rel).write_text(text)
    for name, rel in W.nodes(context, "work-item").items():
        status = W.field((repo / rel).read_text(), "status")
        sv.setdefault("given_status", {})[name] = status
        if status == "awaiting-answer" and not questions_of(sv, name):     # a node awaiting an answer has a question
            sv["questions"]["q-%s" % name] = (name, False)
        asked = sections(sv, name)
        if asked and status in ("drafted", "awaiting-answer"):     # the stage that asked: the question's asking stage
            status = "awaiting-answer"
            stage = next((a.get("asking stage") for q, _ in questions_of(sv, name)
                          for k, a in [context.get("things", {}).get(q, (None, {}))] if k == "question"), None)
            with open(repo / W.WORK / initiative_of(rel) / "log.jsonl", "a") as out:
                out.write(json.dumps(dict(ANSWER_LOG, before=ASKED_FROM.get(stage, "drafted"), **{"work-item": name}))
                          + "\n")
        blocked = [sv["blocked"][name]] if name in sv["blocked"] else None
        (repo / rel).write_text(W.item_text(name, status, initiative_of(rel), blocked_by=blocked) + asked)
    for kind in ("capability-proposal", "glossary-proposal"):
        for name, rel in W.nodes(context, kind).items():
            status = W.field((repo / rel).read_text(), "status")
            stage = named_stage(sv, name)
            if stage in ("integrate", "apply") and not questions_of(sv, name):     # a proposal those rounds are due for
                status = "awaiting-answer"
                sv["questions"]["q-%s" % name] = (name, True)
                if stage == "integrate":     # sent back to integration: by the check of its drafts, or by its apply round
                    sv.setdefault("uncodified", set()).add(name)
                    W.write(repo, W.WORK + "/%s/runs/%s/1-apply/result.json" % (initiative_of(rel), name),
                            json.dumps({"status": "DONE", "unheld_answers": ["One line an event."]}))
            (repo / rel).write_text(proposal_text(name, kind, status, initiative_of(rel), codified, sv))
            if status == "awaiting-answer":
                log = dict(ANSWER_LOG, **{"work-item": name})
                with open(repo / W.WORK / initiative_of(rel) / "log.jsonl", "a") as out:
                    out.write(json.dumps(log) + "\n")
            if kind == "glossary-proposal" and status == "approved":
                index = repo / "spec" / "index.md"
                index.write_text(index.read_text() + "- **ledger**: a thing.\n")
                W.write(repo, W.WORK + "/%s/ledger.md" % initiative_of(rel), "  - 2026-10-15: gate round 1\n")


DELEGATION = "Please get everything delivered. Do not stop to ask me questions or permission."


def kept_review(repo):
    head = W.git(repo, "rev-parse", "HEAD").strip()
    W.write(repo, W.WORK + "/i1/runs/branch-review/1/brief.md", "# branch review of i1\n\nInitiative branch: main\n"
            "Head: %s\n" % head)
    W.write(repo, W.WORK + "/i1/runs/branch-review/1/findings.md", "# findings\nNothing found.\n")
    W.commit_all(repo, "work: branch review 1")


def build(repo, context):
    """The scenario's repository, committed, with its remote; what is left for the plan is in the return value."""
    sv = W.sv(context)
    conds = sv["conds"]
    codified = "codified" in conds.get("change list", set()) or "unparsing" in conds.get("result", set())
    W.base(repo, codified)
    one_initiative(repo, context, sv)
    rewrite_nodes(repo, context, sv, codified)
    branch = conds.get("work-item branch", set())
    if "flaky" in branch:
        W.write(repo, "features/thing.feature", FLAKY_FEATURE)
        W.write(repo, "tests/test_thing.py", FLAKY_STEPS % str(repo.parent / "closes.runs"))
        (repo / ".shop/delivery.toml").unlink()
    if "lost" in branch:
        with open(repo / ".shop/delivery.toml", "a") as out:
            out.write('\n[allowed_tools]\nimplement = ["Read", "Write", "Bash(git checkout *)", "Bash(git branch *)"]\n')
    W.init(repo)
    W.git(repo, "add", "--", ".", ":(exclude).shop/work")
    W.git(repo, "add", "--", *[str(p.relative_to(repo)) for p in (repo / W.WORK).glob("*/initiative.md")])
    W.git(repo, "commit", "-q", "--allow-empty", "-m", "the repository and its initiatives")
    W.commit_all(repo, "the work of the initiatives")
    W.remote(repo)
    if "kept" in branch:
        name = next(iter(W.nodes(context, "work-item")), "w1")
        W.git(repo, "checkout", "-q", "-b", "work/" + name)
        W.write(repo, "kept.txt", "kept\n")
        W.commit_all(repo, "kept work on " + name)
        W.git(repo, "checkout", "-q", "main")
    ib = conds.get("initiative branch", set())
    if "reviewed" in ib:
        kept_review(repo)
        W.git(repo, "push", "-q", "origin", "main")
    if "ahead" in ib:
        W.write(repo, "notes.txt", "notes\n")
        W.commit_all(repo, "notes.txt")
    if "unpushable" in conds.get("remote", set()):     # the remote's branch has a commit the repository does not
        other = repo.parent / "elsewhere"
        W.git(repo.parent, "clone", "-q", "-b", "main", str(W.remote_dir(repo)), str(other))
        W.init_identity(other)
        W.write(other, "elsewhere.txt", "elsewhere\n")
        W.commit_all(other, "a commit the repository does not have")
        W.git(other, "push", "-q", "origin", "main")
    for name in sv["dirty"]:
        W.write(repo, name, "a change not committed\n")
    if "gitless" in ib:
        shutil.rmtree(repo / ".git")


def one_initiative(repo, context, sv):
    """A trace may name the scenario's one initiative i2 (an initiative branch took i1): it is kept as i1, where
    its parts are, and `work run` is given i1 for it."""
    found = W.nodes(context, "initiative")
    if len(found) != 1 or "i1" in found:
        return
    name, rel = next(iter(found.items()))
    text = (repo / rel).read_text().replace(W.full("initiative", name), W.full("initiative", "i1"))
    (repo / rel).unlink()
    W.write(repo, W.WORK + "/i1/initiative.md", text)
    context["nodes"][name] = ("initiative", W.WORK + "/i1/initiative.md")
    sv.setdefault("alias", {})[name] = "i1"


def committed_names(repo, context):
    """Each instance a `commits` Then names, with the file it stands for (work-queue's commit handler reads them from
    the nodes): a transition is a line of log.jsonl, a stage its stage directory's result, a measurement its record,
    a draft a file under its round's drafts path, a feature the generated file."""
    nodes, sv = context.setdefault("nodes", {}), W.sv(context)
    globs = {"transition": W.WORK + "/i1/log.jsonl", "measurement": ".shop/records/measurements/*i1*.md",
             "draft": W.WORK + "/i1/runs/i1/*-integrate/drafts/**/*.md", "feature": "features/*.feature"}
    for text in steps(context):
        found = re.match(r"`work run` commits the (transition|stage|measurement|draft|feature) ([a-z]\d+)$", text)
        if not found or found.group(2) in nodes:
            continue
        what, name = found.groups()
        if what == "stage":
            said = [re.match(r"the stage %s is `(.+)`$" % name, s) for s in steps(context)]
            kind = (sv["stages"].get(name) or next((m.group(1) for m in said if m), "")).replace(" ", "-")
            globs["stage"] = W.WORK + ("/i1/runs/branch-review/*/result.json" if kind == "branch-review" else
                                       "/i1/runs/*/*-%s/result.json" % kind)
        paths = sorted(Path(repo).glob(globs[what]))
        if paths:
            nodes[name] = (what, str(paths[-1].relative_to(repo)))


def flaky_runs(repo):
    path = Path(repo).parent / "closes.runs"
    return path.read_text().split() if path.exists() else []
