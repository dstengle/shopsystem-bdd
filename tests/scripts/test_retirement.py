"""What the retirement of plugin 1.x's workflow must not break (workflow simplification plan 9, Review Focus 1 and 5):
every `work` command still answers, and no kept skill, agent or doc names a deleted agent, skill or command."""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# D12's deleted agents and skills, and the deleted commands and names.
DELETED_AGENTS = ("code-scout", "bdd-planner", "bdd-implementer", "bdd-task-reviewer", "bdd-branch-reviewer",
                  "initiative-round", "capability-writer", "delegation-answerer", "spec-checker", "batch-analyst")
DELETED_SKILLS = ("delivering-an-initiative", "formulating-features", "integrating-a-proposal",
                  "checking-spec-consistency", "migrating-to-capabilities", "bdd-red-green")
DELETED_NAMES = ("work run", "--work-item", "supervise_")
HISTORY = re.compile(r"^## \d+\.\d+\.\d+:")


def work(*args):
    return subprocess.run([sys.executable, str(REPO / "scripts" / "work"), *args], capture_output=True, text=True)


def test_every_work_command_answers_help():
    usage = work("--help")
    assert usage.returncode == 0, usage.stderr
    commands = re.search(r"\{([a-z,-]+)\}", usage.stdout).group(1).split(",")
    failed = [(name, done.returncode) for name in commands if (done := work(name, "--help")).returncode != 0]
    assert failed == []


def readme_less_history():
    kept, history = [], False
    for line in (REPO / "README.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            history = bool(HISTORY.match(line))
        if not history:
            kept.append(line)
    return "\n".join(kept)


def texts():
    for path in sorted((REPO / "skills").rglob("*")) + sorted((REPO / "agents").rglob("*")):
        if path.is_file():
            yield path.relative_to(REPO).as_posix(), path.read_text(encoding="utf-8")
    yield "README.md", readme_less_history()
    yield "CLAUDE.md", (REPO / "CLAUDE.md").read_text(encoding="utf-8")


def test_no_kept_skill_or_agent_names_a_deleted_one():
    names = DELETED_AGENTS + DELETED_SKILLS + DELETED_NAMES
    hits = ["%s:%d names %s" % (rel, n, name) for rel, text in texts()
            for n, line in enumerate(text.splitlines(), 1) for name in names
            if re.search(r"(?<![\w-])%s%s" % (re.escape(name), r"(?![\w-])" if name[-1].isalnum() else ""), line)]
    assert hits == [], "\n".join(hits)
