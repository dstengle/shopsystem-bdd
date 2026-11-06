"""The commands of hooks/hooks.json (plan 8's review, S2): each runs under a `python3` with no site packages, so a bare
interpreter first on the person's PATH never fails a prompt or a session's start; the conversation's hooks still do
their work there."""
import json
import shlex
import subprocess
import sys
from pathlib import Path

import pytest
import transcript_testing as T
from conversation_prompt import kept

ROOT = Path(__file__).resolve().parents[2]
HOOKS = json.loads((ROOT / "hooks" / "hooks.json").read_text())["hooks"]
COMMANDS = [(event, h["command"]) for event, groups in sorted(HOOKS.items()) for g in groups for h in g["hooks"]]


def bare(command):
    """The argv of a hooks.json command, its `python3` this interpreter with `-S` (no site packages)."""
    argv = shlex.split(command.replace("${CLAUDE_PLUGIN_ROOT}", str(ROOT)))
    assert argv[0] == "python3", command
    return [sys.executable, "-S", *argv[1:]]


def run(command, cwd, event):
    stdin = json.dumps({"session_id": "s-1", "transcript_path": str(cwd / "s-1.jsonl"), "cwd": str(cwd),
                        "hook_event_name": event, "prompt": "x", "source": "startup"})
    return subprocess.run(bare(command), cwd=cwd, input=stdin, capture_output=True, text=True, timeout=60)


@pytest.mark.parametrize("where", ["shopped", "outside"])
@pytest.mark.parametrize(("event", "command"), COMMANDS)
def test_every_hook_runs_with_no_site_packages(backlog_repo, tmp_path_factory, where, event, command):
    if where == "shopped":
        T.crowded(backlog_repo, items=1, batches=0)
    cwd = backlog_repo if where == "shopped" else tmp_path_factory.mktemp("outside")
    done = run(command, cwd, event)
    assert (done.returncode, done.stderr) == (0, ""), (command, done.stderr)


def test_the_conversation_hooks_work_with_no_site_packages(backlog_repo):
    T.crowded(backlog_repo, items=1, batches=0)
    done = run(_one("UserPromptSubmit", "quote"), backlog_repo, "UserPromptSubmit")
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")
    assert kept(backlog_repo) == ("s-1", str(backlog_repo / "s-1.jsonl"))
    done = run(_one("SessionStart", "names"), backlog_repo, "SessionStart")
    assert done.returncode == 0 and '| b1 | Item number 1 | shaped |' in done.stdout, (done.stdout, done.stderr)


def _one(event, sub):
    found = [c for e, c in COMMANDS if e == event and sub in c]
    assert len(found) == 1, found
    return found[0]


@pytest.mark.parametrize("sub", ["quote", "names"])
def test_the_conversation_hook_exits_0_when_its_modules_are_missing(tmp_path, sub):
    """Whatever goes wrong, an import included, the hook is silent and exits 0."""
    alone = tmp_path / "alone"
    alone.mkdir()
    (alone / "conversation_hook").write_text((ROOT / "scripts" / "conversation_hook").read_text())
    done = subprocess.run([sys.executable, "-S", str(alone / "conversation_hook"), sub], cwd=tmp_path, input="{}",
                          capture_output=True, text=True, timeout=60)
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")


def test_no_hook_names_the_old_queue(tmp_path):
    """Plan 9, D15: no hook runs `migrate prompting` or `migrate compacting`, and the SessionStart hook prints no
    initiative of the frozen queue."""
    assert [c for _, c in COMMANDS if "prompting" in c or "compacting" in c] == []
    for rel, text in {"spec/index.md": "---\nid: bounded-context/o/p/c\nkind: bounded-context\n---\n",
                      ".shop/work/i1/initiative.md": "---\nkind: initiative\nstatus: started\ntitle: Cart\n---\n",
                      ".shop/work/i1/ledger.md": "# i1\n"}.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    done = subprocess.run([sys.executable, str(ROOT / "scripts" / "migrate"), "status", "--hook"], cwd=tmp_path,
                          capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr
    assert "i1" not in done.stdout, done.stdout


REQUEST = ("---\nid: request/q1\nkind: request\nupstream: bounded-context/ex.com/prod/up\n"
           "asker: bounded-context/ex.com/prod/ctx\nstatus: %s\nturn: upstream\n---\n\n# Old items\n")


@pytest.mark.parametrize(("status", "named"), [("awaiting-upstream", True), ("delivered", False)])
def test_the_requests_hook_names_a_waiting_request_with_no_site_packages(tmp_path, status, named):
    """r54, r56 under a bare `python3`: `work` itself imports clingo, so hooks.json runs request_hook."""
    for rel, text in {"spec/index.md": "---\nid: bounded-context/ex.com/prod/ctx\nkind: bounded-context\n---\n",
                      ".shop/requests/q1.md": REQUEST % status}.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    done = run(_one("SessionStart", "request_hook"), tmp_path, "SessionStart")
    assert (done.returncode, done.stderr) == (0, ""), done.stderr
    assert ("q1 awaiting-upstream: Old items" in done.stdout) == named, done.stdout
    assert ("work watch --forward" in done.stdout) == named, done.stdout


def test_the_requests_hook_exits_0_when_its_modules_are_missing(tmp_path):
    alone = tmp_path / "alone"
    alone.mkdir()
    (alone / "request_hook").write_text((ROOT / "scripts" / "request_hook").read_text())
    done = subprocess.run([sys.executable, "-S", str(alone / "request_hook"), "watch"], cwd=tmp_path, input="{}",
                          capture_output=True, text=True, timeout=60)
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")
