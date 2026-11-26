"""migrate_upgrade_commands (b632, upgrades#r44): each old command line of an instructions file run as `shop <name>`,
a mention left alone, no other file read."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from upgrades import migrate_upgrade_commands as C


def test_shell_commands_in_command_position():
    assert C.shell("work backlog") == "shop work backlog"
    assert C.shell("spec check && features generate --check") == "shop spec check && shop features generate --check"
    assert C.shell("model check; tools size --limit 300") == "shop spec check; shop tools size --limit 300"
    assert C.shell("x=$(migrate status) | measure batch 3") == "x=$(shop migrate status) | shop measure batch 3"


def test_shell_plugin_script():
    assert C.shell('python3 "${CLAUDE_PLUGIN_ROOT}/scripts/migrate" status --hook') == \
        'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/shop" migrate status --hook'
    assert C.shell('python3 \\"$CLAUDE_PLUGIN_ROOT/scripts/work\\" watch') == \
        'python3 \\"$CLAUDE_PLUGIN_ROOT/scripts/shop\\" work watch'


def test_shell_leaves_mentions_and_shop_alone():
    for text in ("work", "spec/", "python3 scripts/tools size", "shop work backlog", "echo work done",
                 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/shop" work backlog', "network backlog"):
        assert C.shell(text) == text


def test_markdown_spans_and_shell_fences_only():
    text = ("Run `work idea` for an idea; the work of a session and `spec` alone stay.\n"
            "```bash\n$ spec check\n```\n"
            "```markdown\n- the person runs `work ready`\nwork backlog\n```\n"
            "work backlog in prose\n")
    assert C.markdown(text) == (
        "Run `shop work idea` for an idea; the work of a session and `spec` alone stay.\n"
        "```bash\n$ shop spec check\n```\n"
        "```markdown\n- the person runs `work ready`\nwork backlog\n```\n"
        "work backlog in prose\n")
    assert C.markdown(C.markdown(text)) == C.markdown(text)


def test_settings_hook_commands():
    text = json.dumps({"hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "work names --hook"}]}]},
                       "env": {"NOTE": "work stays"}}, indent=2)
    after = json.loads(C.settings(text))
    assert after["hooks"]["SessionStart"][0]["hooks"][0]["command"] == "shop work names --hook"
    assert after["env"]["NOTE"] == "work stays"


def test_delivery_tests_and_checks_only():
    text = ('[batch]\ntests = "python3 -m pytest -q && spec check"\nrules = ["work only in your worktree"]\n'
            '[review]\nchecks = [\n  "tools check --base main",\n  "ruff check",\n]\nsize = 1000\n')
    assert C.delivery(text) == (
        '[batch]\ntests = "python3 -m pytest -q && shop spec check"\nrules = ["work only in your worktree"]\n'
        '[review]\nchecks = [\n  "shop tools check --base main",\n  "ruff check",\n]\nsize = 1000\n')


def git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def test_plan_reads_only_tracked_instructions_files(tmp_path):
    files = {"CLAUDE.md": "Run `work backlog`.\n", "docs/guide.md": "`spec check`\n", "README.md": "`work backlog`\n",
             "docs/notes.txt": "`work backlog`\n", "docs/same.md": "the work of a page\n"}
    for rel, text in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", "-A")
    (tmp_path / "docs/untracked.md").write_text("`work backlog`\n")
    changes = C.plan(tmp_path)
    assert changes.texts == {"CLAUDE.md": "Run `shop work backlog`.\n", "docs/guide.md": "`shop spec check`\n"}
    assert len(changes.notes) == 2 and changes.notes[0].startswith("CLAUDE.md: ")
