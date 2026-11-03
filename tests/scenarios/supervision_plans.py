"""What the stand-in claude is told to do in a supervision scenario (not a handler module; loaded by path): the result
of the stage the scenario's When ends, read from the Givens of its stage, its result and its session, and for every
other session what a session that did its stage's work gives. A round no step names ends with no result, so its node
keeps the status the named stage left it in (U6) and the Thens read that status.

The plan's keys are the stand-in's (tests/scripts/stub_claude.py): an agent, `round:<kind>:<node>`, or `default`."""
import json
import subprocess
from pathlib import Path

W = None     # supervision_world, set by the handler module that loads this one
AGENTS = {"research": "code-scout", "plan": "bdd-planner", "implement": "bdd-implementer", "review": "bdd-task-reviewer",
          "branch review": "bdd-branch-reviewer", "answer": "delegation-answerer", "analysis": "batch-analyst"}
ROUNDS = ("integrate", "gate", "apply", "formulate", "intake")
QUESTION = "Which module owns the log?"
ANSWER = "The delegation covers it."
FIX_NOW = ["Fix now: w1 leaves the log unclosed.", "Fix now: w1 names the wrong file."]
CATALOGUE = "bounded-context/ex.com/prod/catalogue"
FIXTURE = (Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "glossary" / "spec" / "index.md").read_text()
# A line the catalogue's grammar parses: its index is codified, with the typed glossary of the fixture.
RAISED = "When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`."
BAD = ("\n### [g9] A line the grammar refuses\n- [r9] When asked, frobnicate the widgets wholesale.\n")


def defaults(context):
    answer = dict(a for _, (k, attrs) in context.get("things", {}).items() if k == "answer" for a in attrs.items())
    verdict = {"--change": "change", "--accept": "accept"}.get(answer.get("flag"))
    return {"default": {"status": "DONE"}, "initiative-round": {"result": "none"},
            "bdd-branch-reviewer": {"questions": []},
            "batch-analyst": {"notes": {"analysis.md": "# analysis of i1\nThe stand-in's analysis.\n"}},
            "delegation-answerer": {"fields": dict({"answer": ANSWER}, **({"verdict": verdict} if verdict else {}))}}


def catalogue(repo):
    """The upstream catalogue beside the repository, named by its spec/index.md's `## Upstreams`."""
    there = repo.parent / "catalogue-ctx"
    W.write(there, "spec/index.md", "---\nid: %s\nlanguage: codified-1\n---\n# catalogue\n\n%s"
            % (CATALOGUE, FIXTURE[FIXTURE.index("## Glossary"):]))
    for args in (("init", "-q", "-b", "main"), ("config", "user.name", "Someone"),
                 ("config", "user.email", "someone@example.com"), ("config", "commit.gpgsign", "false"),
                 ("add", "-A"), ("commit", "-q", "-m", "catalogue")):
        subprocess.run(["git", *args], cwd=there, check=True, capture_output=True)
    index = repo / "spec" / "index.md"
    index.write_text(index.read_text() + "\n## Upstreams\n\n- %s: ../catalogue-ctx/spec\n" % CATALOGUE)
    W.commit_all(repo, "spec/index.md names catalogue as an upstream")


def awaited(repo):
    """p1 written by an integrate round that raised a request into catalogue, which is not delivered."""
    there = repo.parent / "catalogue-ctx"
    kept = W.WORK + "/i1/runs/i1/1-integrate/drafts/round-1/"
    W.write(there, ".shop/work/requests/q2.md", "---\nid: request/ex.com/prod/catalogue/q2\nkind: request\nasker: "
            "bounded-context/%s\nraised_for: %s\nstatus: awaiting-upstream\nturn: upstream\n---\n\n# q2\n\n## Lines\n"
            "1. A line.\n" % (W.PATH, W.full("request", "q1")))
    subprocess.run(["git", "add", "-A"], cwd=there, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "q2"], cwd=there, check=True)
    path = repo / W.WORK / "i1" / "p1.md"
    path.write_text(path.read_text() + "\n# thing\n\nThe drafts of this proposal are in %s.\n" % kept)
    W.write(repo, W.WORK + "/i1/raised.jsonl", json.dumps({"upstream": CATALOGUE, "request": "q2", "initiative": "i1",
                                                         "status": "open", "round": kept}) + "\n")
    W.commit_all(repo, "i1 raised q2 in catalogue")


def drafts(name, text, k):
    """The drafts an integrate round writes under its drafts path: the round's `k`, as its scratch directory has it."""
    return {".shop/scratch/%d-integrate/drafts/round-1/spec/capabilities/%s" % (k, name): text}


def outcome_entry(kind, outcome, conds, repo, codified, k=1):
    """The result of a stage of `kind` with `outcome` and the conditions of its result."""
    cap = "work-queue" if codified else "thing"
    if kind == "intake":
        work = ["python3", str(W.SCRIPTS / "work")]
        runs = [work + ["outcome", "q1", "1", "accepted"], work + ["turn", "q1"]]
        if outcome == "QUESTION":
            return {"status": "DONE", "questions": ["1. " + QUESTION], "run": [runs[1]]}
        return {"status": "DONE", "run": runs}
    if kind == "branch review" and "fixing" in conds:
        return [{"questions": FIX_NOW, "notes": {"findings.md": "# findings\n" + "\n".join(FIX_NOW) + "\n"}},
                {"questions": []}]
    entry = {"status": "DONE" if kind in ROUNDS and outcome == "QUESTION" else (outcome or "DONE")}
    if outcome == "QUESTION":
        entry["questions"] = [QUESTION]
    if kind == "integrate":
        entry["fields"] = {"changes": [{"capability": cap, "adds": ["%s#r9" % cap], "changes": [], "removes": []}]}
        if "glossarial" in conds:
            entry["fields"] = {"changes": [{"glossary": True, "adds": ["term/ledger"], "changes": [], "removes": []}]}
        if "strange" in conds:
            entry["fields"] = {"changes": [{"capability": "nowhere", "adds": ["nowhere#r1"]}]}
        if "listless" in conds:
            entry.pop("fields")
        if "raising" in conds:
            catalogue(repo)
            entry["fields"]["requests"] = [{"upstream": CATALOGUE, "lines": [RAISED]}]
        if "unparsing" in conds:
            text = (W.GENERATE / "capabilities" / "work-queue.md").read_text().replace("\n## Not yet", BAD + "\n## Not yet")
            return [dict(entry, write=drafts("work-queue.md", text, n), result="file") for n in range(k, k + 3)]
        entry["write"] = drafts("%s.md" % cap, "# %s\nThe capability as the integrate round drafted it.\n" % cap, k)
    if kind == "apply":
        entry["fields"] = {"changes": [{"capability": cap, "adds": ["%s#r1" % cap]}]}
        if "unheld" in conds:
            entry["fields"]["unheld_answers"] = ["One line an event."]
    if "setless" in conds:
        entry["fields"] = {"fileset": []}
    if "outputless" in conds:
        entry["fields"] = {"plan": None, "fileset": None}
    if "naming" in conds:
        entry.update({"write": {"report.md": "the implementer's report\n"}, "names": {"report": "report.md"}})
    return entry


def session_entry(conds, repo):
    entry = {}
    if "faulty" in conds:
        entry["subtype"] = "error_max_turns"
    if "meddling" in conds:
        entry["write"] = {W.WORK + "/i1/initiative.md": "changed by a worker\n"}
    if "littering" in conds:
        entry["elsewhere"] = {"root": str(repo), "write": {W.WORK + "/i1/initiative.md": "changed elsewhere\n"}}
    if "crossing" in conds:
        own = (repo / W.WORK / "i1" / "initiative.md").read_text()
        entry["elsewhere"] = {"root": str(repo), "commit": {
            W.WORK + "/i2/initiative.md": "---\nid: %s\nkind: initiative\nstatus: proposed\n---\n" % W.full("initiative", "i2"),
            W.WORK + "/i1/initiative.md": own + "\nChanged by another session.\n"}}
    return entry


def branch_entry(conds, branch, name="w1"):
    """The implementer's work: a commit of feature.txt where the Givens name a work-item branch."""
    if "lost" in conds:
        return {"run": [["git", "checkout", "-q", "--detach"], ["git", "branch", "-q", "-D", "work/" + name]]}
    commit = {"feature.txt": "the feature\n"}
    if "not green check" in conds:
        commit["scenarios-fail"] = "\n"
    return {"commit": commit} if branch else {}


def plan_for(repo, context, stage=None):
    """The stand-in's plan; `stage` names the stage the scenario's When ends, if any."""
    sv = W.sv(context)
    plan = defaults(context)
    codified = bool({"codified"} & sv["conds"].get("change list", set())) or "unparsing" in sv["conds"].get("result", set())
    if "awaited" in sv["conds"].get("result", set()):
        catalogue(repo)
        awaited(repo)
    implementer = branch_entry(sv["conds"].get("work-item branch", set()), "work-item branch" in sv["things"].values(),
                               next(iter(W.nodes(context, "work-item")), "w1"))
    if implementer:
        plan["bdd-implementer"] = implementer
    if stage is None:
        return plan
    kind, node = sv["stages"][stage], sv["for"].get(stage, "w1")
    result = sv["with"].get(stage)
    k = 1 + len(list((repo / W.WORK).glob("*/runs/%s/*" % node)))     # the number the round's stage directory takes
    entry = outcome_entry(kind, sv["results"].get(result), sv["inst"].get(result, set()), repo, codified, k)
    session = session_entry(set().union(*[sv["inst"].get(s, set()) for s in sv["sessions"]] or [set()]), repo)
    if isinstance(entry, list):
        entry[0].update(session)
    else:
        entry.update(session)
        if kind == "implement":
            entry = dict(implementer, **entry)
    if kind in ROUNDS and isinstance(entry, list):     # a round sent back gives each of its sessions its own result
        plan["initiative-round"] = entry + [plan["initiative-round"]]
    elif kind in ROUNDS:
        plan["round:%s:%s" % (kind, node)] = dict(entry, result="file")
    elif kind == "answer":
        plan["delegation-answerer"] = dict(plan["delegation-answerer"], **entry)
    else:
        plan[AGENTS[kind]] = entry if isinstance(entry, list) else [entry, {}]
    return plan
