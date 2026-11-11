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
DELETED_NAMES = ("work run", "--work-item", "supervise_", "work add", "work status", "work note", "work start",
                 "work delegate", "work retry", "migrate prompting", "migrate compacting")
HISTORY = re.compile(r"^## \d+\.\d+\.\d+:")
OLD_EXAMPLE = "plugin 1.x's vocabulary"     # the note above a fenced example of docs/capability-format.md it allows


def work(*args):
    return subprocess.run([sys.executable, str(REPO / "scripts" / "work"), *args], capture_output=True, text=True)


def test_every_work_command_answers_help():
    usage = work("--help")
    assert usage.returncode == 0, usage.stderr
    commands = re.search(r"\{([a-z,-]+)\}", usage.stdout).group(1).split(",")
    failed = [(name, done.returncode) for name in commands if (done := work(name, "--help")).returncode != 0]
    assert failed == []


def readme_less_history(name="README.md"):
    """A page's lines less its history sections, `## x.y.z: ...` (CHANGELOG.md's rule: each release's note is kept as
    it was written, in the words of its day)."""
    kept, history = [], False
    for line in (REPO / name).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            history = bool(HISTORY.match(line))
        if not history:
            kept.append(line)
    return "\n".join(kept)


def doc_less_old_examples(path):
    """A doc's lines, each fenced block that a line naming plugin 1.x's vocabulary introduces blanked (kept as an
    illustration, plan-9 review M3); the line numbers stay."""
    kept, fenced, allowed, noted = [], False, False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            if not fenced:
                allowed = noted
            fenced = not fenced
            kept.append(line)
            continue
        kept.append("" if fenced and allowed else line)
        if line.strip():
            noted = OLD_EXAMPLE in line
    return "\n".join(kept)


def texts():
    paths = sorted((REPO / "skills").rglob("*")) + sorted((REPO / "agents").rglob("*"))
    for path in paths + sorted((REPO / ".claude-plugin").glob("*")):
        if path.is_file():
            yield path.relative_to(REPO).as_posix(), path.read_text(encoding="utf-8")
    yield "README.md", readme_less_history()
    yield "CHANGELOG.md", readme_less_history("CHANGELOG.md")
    yield "CLAUDE.md", (REPO / "CLAUDE.md").read_text(encoding="utf-8")
    yield "docs/capability-format.md", doc_less_old_examples(REPO / "docs" / "capability-format.md")


def test_no_kept_skill_or_agent_names_a_deleted_one():
    names = DELETED_AGENTS + DELETED_SKILLS + DELETED_NAMES
    hits = ["%s:%d names %s" % (rel, n, name) for rel, text in texts()
            for n, line in enumerate(text.splitlines(), 1) for name in names
            if re.search(r"(?<![\w-])%s%s" % (re.escape(name), r"(?![\w-])" if name[-1].isalnum() else ""), line)]
    assert hits == [], "\n".join(hits)


def test_the_marketplace_describes_the_plugin_as_plugin_json_does():
    """The marketplace listing shows marketplace.json's description (plan-9 review S1): it is plugin.json's."""
    import json
    plugin = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    listed = [p["description"] for p in market["plugins"] if p["name"] == plugin["name"]]
    assert listed == [plugin["description"]]


def test_the_module_map_is_whole():
    """CLAUDE.md's module map (plan 9, Task 8): each backticked scripts/ or tests/ path or glob of its table names a
    tracked file (a `<placeholder>` read as `*`), and each tracked scripts/*.py and extensionless script in scripts/ is named by some row."""
    import fnmatch
    tracked = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True).stdout.split()
    rows = [line for line in (REPO / "CLAUDE.md").read_text(encoding="utf-8").splitlines() if line.startswith("| `")]
    named = [re.sub(r"<[^>]+>", "*", p.rstrip("/")) for row in rows
             for p in re.findall(r"`((?:scripts|tests)/[^`\s]*)`", row.split(" | ")[0])]
    missing = [p for p in named if not any(fnmatch.fnmatch(t, p) or t.startswith(p + "/") for t in tracked)]
    assert missing == [], missing
    modules = [t for t in tracked if re.fullmatch(r"scripts/[^/]+", t) and (t.endswith(".py") or "." not in t[8:])]
    unnamed = [m for m in modules if not any(fnmatch.fnmatch(m, p) for p in named)]
    assert unnamed == [], unnamed
