"""A new request through the new requirements system, end to end (the GF conversion's plan P15, the brief's "done
means"): in a clone of a small codified context (tests/scripts/fixtures/e2e/repo: two capabilities and universal.md),
with the stand-in claude (tests/scripts/stub_claude.py) in place of every session and the real GF, a request is
refused while a line does not parse, accepted when every line does, taken in by an intake round, started, integrated
(the first drafts refused by the logic check and sent back), passed through the gate on the person's answer, applied,
formulated by `features generate`, drafted into a work-item, delivered through research, plan, implement and review,
reviewed as a branch, done, and resolved."""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import toolchain

PLUGIN = Path(__file__).resolve().parents[2]
SCRIPTS = PLUGIN / "scripts"
STUB = PLUGIN / "tests" / "scripts" / "stub_claude.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "e2e"
ORIGIN = "observation/example.org/fixture/e2e/obs-1"
BAD = "When asked, frobnicate the widgets wholesale."
GOOD = ("When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to "
        "`abandoned` and exit successfully.")


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


def clone(tmp_path):
    """The fixture context as a git repository on main with a bare remote: its `.in` files written without the suffix,
    the plugin's path in the conftest."""
    root = tmp_path / "repo"
    shutil.copytree(FIXTURE / "repo", root)
    for path in list(root.rglob("*.in")):
        path.with_suffix("").write_text(path.read_text().replace("@PLUGIN@", str(PLUGIN)))
        path.unlink()
    git(root, "init", "-q", "-b", "main")
    for key, value in (("user.name", "Someone"), ("user.email", "someone@example.com"), ("commit.gpgsign", "false")):
        git(root, "config", key, value)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "the fixture context")
    subprocess.run(["git", "init", "-q", "--bare", str(tmp_path / "remote.git")], check=True, capture_output=True)
    git(root, "remote", "add", "origin", str(tmp_path / "remote.git"))
    git(root, "push", "-q", "-u", "origin", "main")
    return root


def environment(tmp_path, phase):
    """The environment of a command: the stand-in first on PATH and as $SHOPSYSTEM_WORK_CLAUDE, its plan and record
    those of `phase`."""
    there = tmp_path / "stub"
    (there / "bin").mkdir(parents=True, exist_ok=True)
    claude = there / "bin" / "claude"
    claude.write_text("#!/bin/sh\nexec %s %s \"$@\"\n" % (sys.executable, STUB))
    claude.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_WORK_RUN_WORKER", "PYTEST_XDIST_WORKER")}
    env.update(PATH="%s%s%s" % (there / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(claude), STUB_CLAUDE_PLAN=str(there / ("%s.json" % phase)),
               STUB_CLAUDE_CALLS=str(there / ("%s.jsonl" % phase)), CLAUDE_CONFIG_DIR=str(there / "claude"))
    env["PYTHONPATH"] = os.pathsep.join(p for p in env.get("PYTHONPATH", "").split(os.pathsep)
                                        if p and not (Path(p) / "work_items.py").exists())
    return env


def tool(root, tmp_path, name, *args, phase="none", plan=None):
    """`<name> <args>` (a script of the plugin) in the clone; with `plan`, the stand-in told what to do in `phase`."""
    env = environment(tmp_path, phase)
    if plan is not None:
        Path(env["STUB_CLAUDE_PLAN"]).write_text(json.dumps(plan))
    done = subprocess.run([sys.executable, str(SCRIPTS / name), *args], cwd=root, env=env, capture_output=True,
                          text=True, timeout=600)
    (tmp_path / ("%s-%s.txt" % (phase, name))).write_text("exit %d\n%s\n%s" % (done.returncode, done.stdout, done.stderr))
    return done


def briefs(tmp_path, phase):
    """The briefs of the sessions the stand-in started in `phase`, in the order they started."""
    path = tmp_path / "stub" / ("%s.jsonl" % phase)
    return [c["brief"] for c in map(json.loads, path.read_text().splitlines()) if c["event"] == "start"]


def feature(root):
    return (root / "features" / "work-queue.feature").read_text()


def lines_file(tmp_path, *lines):
    path = tmp_path / "lines.txt"
    path.write_text("".join(line + "\n" for line in lines))
    return str(path)


def status(root, rel):
    found = re.search(r"^status: (\S+)$", (root / rel).read_text(), re.MULTILINE)
    return found.group(1) if found else None


@pytest.fixture
def repo(tmp_path):
    toolchain.require()
    return clone(tmp_path)


def intake_plan():
    work = ["python3", str(SCRIPTS / "work")]
    return {"default": {"status": "DONE"},
            "initiative-round": {"run": [work + ["outcome", "q1", "1", "accepted"], work + ["turn", "q1"]]}}


def drafted(group):
    """The work-queue capability with `group` added to its Behaviour."""
    text = (FIXTURE / "repo" / "spec" / "capabilities" / "work-queue.md").read_text()
    return text.replace("\n## Not yet", "\n" + group + "\n## Not yet")


REFUSED = drafted("### [g2] `work abandon` abandons a proposed initiative\n- [r2] When the person runs `work abandon` on "
                  "an initiative that is `proposed`, `work` shall set its status to `abandoned`.\n")
CLEAN = drafted("### [g2] `work abandon` abandons a started initiative\n- [r2] %s\n" % GOOD)
CHANGES = [{"capability": "work-queue", "adds": ["work-queue#r2"], "changes": [], "removes": []}]


def integrate_plan():
    """Two integrate sessions: the first drafts a group the logic check refuses, the second the clean group."""
    def session(k, text):
        return {"status": "DONE", "fields": {"changes": CHANGES},
                "write": {".shop/scratch/%d-integrate/drafts/round-1/spec/capabilities/work-queue.md" % k: text}}
    return {"default": {"status": "DONE"}, "initiative-round": [session(1, REFUSED), session(2, CLEAN)]}


HANDLER = """

@handler("WhenRuns", "`work abandon`")
def work_abandon(step):
    status = step.context["status"]
    status[step.names[0]], step.context["exit"] = queue_cmd.abandon(status[step.names[0]])
"""
CODE = """

def abandon(status):
    return ("abandoned", 0) if status == "started" else (status, 1)
"""


def deliver_plan():
    """The apply round writes the approved drafts into spec/; the implementer adds the handler and the code."""
    handlers = (FIXTURE / "repo" / "tests" / "scenarios" / "work_queue_handlers.py.in").read_text() + HANDLER
    code = (FIXTURE / "repo" / "queue_cmd.py.in").read_text() + CODE
    fileset = ["queue_cmd.py", "tests/scenarios/work_queue_handlers.py"]
    return {"default": {"status": "DONE"},
            "round:apply": {"commit": {"spec/capabilities/work-queue.md": CLEAN}, "fields": {"changes": CHANGES}},
            "code-scout": {"fields": {"fileset": fileset}},
            "bdd-planner": {"fields": {"fileset": fileset}, "notes": {"plan.md": "# plan\nAdd abandon.\n"}},
            "bdd-implementer": {"commit": {"tests/scenarios/work_queue_handlers.py": handlers, "queue_cmd.py": code}},
            "bdd-task-reviewer": {"notes": {"findings.md": "# findings\nNothing.\n"}},
            "bdd-branch-reviewer": {"questions": [], "notes": {"findings.md": "# findings\nNothing.\n"}},
            "batch-analyst": {"notes": {"analysis.md": "# analysis of i1\nThe stand-in's analysis.\n"}}}


def test_a_request_goes_through_the_requirements_system_into_delivery(repo, tmp_path):
    # 0. the fixture context is in the new format: one statement a group, no given block that is not example data
    checked = tool(repo, tmp_path, "model", "check")
    assert checked.returncode == 0 and "\n0 violations, " in "\n" + checked.stdout, checked.stdout
    assert tool(repo, tmp_path, "model", "lexicon", "--check").stdout.rstrip().endswith("0 problems")
    # 1. a line that does not parse refuses the request, with the hint
    done = tool(repo, tmp_path, "work", "request", "--from", "internal", "--source", ORIGIN, "--lines",
                lines_file(tmp_path, GOOD, BAD), "Abandon a started initiative")
    assert done.returncode != 0
    assert "line 2 does not parse" in done.stderr and "parsed up to: When asked" in done.stderr
    assert not (repo / ".shop" / "work" / "requests").exists()
    # 2. codified lines are accepted
    done = tool(repo, tmp_path, "work", "request", "--from", "internal", "--source", ORIGIN, "--lines",
                lines_file(tmp_path, GOOD), "Abandon a started initiative")
    assert done.returncode == 0, done.stderr
    request = ".shop/work/requests/q1.md"
    assert status(repo, request) == "open"
    # 3. the intake round writes the line's outcome and passes the turn; then the initiative is started
    done = tool(repo, tmp_path, "work", "run", phase="intake", plan=intake_plan())
    assert status(repo, request) == "accepted", done.stdout + done.stderr
    done = tool(repo, tmp_path, "work", "start", "q1")
    assert done.returncode == 0, done.stderr
    assert status(repo, ".shop/work/i1/initiative.md") == "proposed"
    # 4. the integrate round: its first drafts are refused by the logic check and sent back, its second are clean
    done = tool(repo, tmp_path, "work", "run", "i1", phase="integrate", plan=integrate_plan())
    assert done.returncode == 3, done.stdout + done.stderr
    resent = (repo / ".shop/work/i1/runs/i1/2-integrate/brief.md").read_text()
    assert ("Refused drafts (send-back 1 of 2): L3 work-queue#r2 sets the status of an initiative from `proposed` to "
            "`abandoned`, which no transition allows") in resent
    assert "[r2] %s" % GOOD in (repo / ".shop/work/i1/runs/i1/2-integrate/drafts/round-1/spec/capabilities/work-queue.md"
                                ).read_text()
    # 5. the gate, shown the scenario the drafts would generate, asked the person, who approves through `work answer`
    gate = briefs(tmp_path, "integrate")
    assert [b.split("\n", 1)[0] for b in gate] == ["# integrate of i1", "# integrate of i1", "# gate of work-queue"]
    assert "Generated scenarios (preview):" in gate[-1]
    proposal = ".shop/work/i1/work-queue.md"
    assert status(repo, proposal) == "awaiting-answer"
    done = tool(repo, tmp_path, "work", "answer", "work-queue", "Approve work-queue as drafted.")
    assert done.returncode == 0, done.stderr
    # 6.-9. the apply round, the scripted formulate (the real GF parses, `features generate` writes the scenario), the
    # work-item drafted from the change list, its delivery and merge with `--work-item`, the branch review and done
    done = tool(repo, tmp_path, "work", "run", "i1", phase="deliver", plan=deliver_plan())
    assert done.returncode == 0, done.stdout + done.stderr
    assert [line.split()[-1] for line in done.stdout.splitlines()] == ["green", "formulated"]
    log = git(repo, "log", "--format=%s")
    assert "features: work-queue generated from work-queue" in log and "work: work-queue approved -> formulated" in log
    assert "@g2 @r2\n  Scenario: `work abandon` abandons a started initiative" in feature(repo)
    assert "accepts: [work-queue#r2]" in (repo / ".shop/work/i1/w1.md").read_text()
    logged = [json.loads(line) for line in (repo / ".shop/work/i1/log.jsonl").read_text().splitlines()]
    before = next(e["record"] for e in logged if e.get("event") == "suite")
    assert "failing: tests/scenarios/test_work_queue.py::test_work_abandon_abandons_a_started_initiative" in before
    assert next(e["record"] for e in logged if e.get("event") == "merged").startswith("Suite: 2 passed, 0 failed")
    assert [b.split("\n", 1)[0] for b in briefs(tmp_path, "deliver")] == [
        "# apply of work-queue", *("# %s of w1" % s for s in ("research", "plan", "implement", "review")),
        "# branch review of i1", "# analysis of i1"]
    # 10. the request resolved by the requirement that holds its line
    head = git(repo, "rev-parse", "--short", "HEAD").strip()
    done = tool(repo, tmp_path, "work", "resolve", "q1", "--line", "1", "work-queue#r2", head)
    assert done.returncode == 0, done.stderr
    assert status(repo, request) == "delivered" and status(repo, ".shop/work/i1/initiative.md") == "done"
    assert "1. work-queue#r2 %s" % head in (repo / request).read_text()
    assert tool(repo, tmp_path, "features", "generate", "--check").returncode == 0
    checked = tool(repo, tmp_path, "model", "check")
    assert checked.returncode == 0 and checked.stdout.startswith("0 violations, 0 warnings"), checked.stdout
    logic = tool(repo, tmp_path, "model", "logic")
    assert logic.returncode == 0 and logic.stdout.strip() == "no findings", logic.stdout
    assert git(repo, "status", "--porcelain") == ""
