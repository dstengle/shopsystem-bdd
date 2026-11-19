"""The 0.38.0 upgrade step "the domain contract" (the domain contract design, §9.6): on the frozen 0.37 copies of the
notes-cli example and the docs-shop fixture, `migrate upgrade` scaffolds the domain model, the vocabulary and the CLI
contract, imports the request pack and names by file and id each line a session rewords; a second run changes
nothing; and the copy reworded by hand passes `spec check`, `features generate --check` and `spec logic`."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

import domain_model
import migrate_upgrade_domain as step
import toolchain

FROZEN = ROOT / "tests/scripts/fixtures/upgrade-0.37"
SCRIPTS = ROOT / "scripts"


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


def repository(tmp_path, name):
    root = tmp_path / name
    shutil.copytree(FROZEN / name, root)
    (root / ".shop").mkdir()
    (root / ".shop/plugin-version").write_text("0.37.0\n")
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.name", "t")
    git(root, "config", "user.email", "t@example.org")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "0.37")
    return root


def migrate(root, command="upgrade"):
    return subprocess.run([sys.executable, str(SCRIPTS / "migrate"), command], cwd=root, capture_output=True,
                          text=True)


def test_notes_cli_is_scaffolded_and_its_lines_named(tmp_path):
    root = repository(tmp_path, "notes-cli")
    done = migrate(root)
    assert done.returncode == 0, done.stderr
    model = domain_model.load(root)
    assert set(model.objects) >= {"note", "tag", "file"}
    notes = model.services["notes"]
    assert [o.name for o in notes.operations] == ["add", "list", "remove"]
    assert [p.name for p in notes.operation("add").parameters] == ["title", "tag"]
    assert "the person" in model.actors
    vocabulary = (root / "spec/vocabulary/notes-cli.md").read_text()
    assert "- **note** (noun) → object note." in vocabulary
    assert "- **add** (verb, action) → operation notes.add." in vocabulary
    assert "- **the notes service** (proper noun) → service notes." in vocabulary
    assert "- **the person** (proper noun) → actor the person." in (root / "spec/vocabulary/shared.md").read_text()
    contract = (root / "spec/adapters/cli.toml").read_text()
    assert '[operations."notes.add"]\ncommand = "notes add"' in contract
    assert 'title = { option = "--title" }' in contract
    index = (root / "spec/index.md").read_text()
    assert "imports: [request]" in index and "## Glossary" not in index and "## Relations" not in index
    capability = (root / "spec/capabilities/notes.md").read_text()
    assert "area: notes-cli\n" in capability
    assert "- [r1] When the person runs `notes add`" in capability       # no line reworded
    assert (root / "spec/moves.json").read_text() == "{}\n"
    assert git(root, "status", "--porcelain") == ""                       # one commit
    assert (root / ".shop/plugin-version").read_text() == "0.38.0\n"
    out = done.stdout
    assert "spec/capabilities/notes.md r1 requests notes.add(title, tag)" in out
    assert "spec/capabilities/notes.md r2 requests notes.add(title)" in out
    assert "spec/capabilities/notes.md r3 says print" in out
    assert "`notes`, spec/index.md: Kind of: tool" in out
    assert "delete, spec/index.md: a tool's act" in out


def test_a_second_run_changes_nothing(tmp_path):
    root = repository(tmp_path, "notes-cli")
    assert migrate(root).returncode == 0
    head = git(root, "rev-parse", "HEAD")
    again = migrate(root)
    assert again.returncode == 0 and "no upgrade step is pending" in again.stdout
    assert git(root, "rev-parse", "HEAD") == head
    assert step.plan(root).texts == {}


def test_docs_shop_is_scaffolded_with_its_state_verbs_as_relations(tmp_path):
    root = repository(tmp_path, "docs-shop")
    done = migrate(root)
    assert done.returncode == 0, done.stderr
    model = domain_model.load(root)
    assert model.objects["shopper"].relation("owns").targets == ("cart",)
    assert model.objects["cart"].attribute("load").values == ("empty", "full")
    assert model.objects["shopper"].relation("has").targets == ("cart",)       # cart | of | shopper
    assert model.objects["till"].relation("for").targets == ("shopper",)       # till | for | shopper
    vocabulary = (root / "spec/vocabulary/shop.md").read_text()
    assert "- **own** (verb, state) → relation shopper.owns." in vocabulary
    assert "pick, spec/index.md: a verb that names no operation" in done.stdout


def test_the_reworded_notes_cli_passes_the_checks():
    toolchain.require()
    reworded = FROZEN / "notes-cli-reworded"
    check = subprocess.run([sys.executable, str(SCRIPTS / "spec"), "--root", str(reworded), "check"],
                           capture_output=True, text=True)
    assert check.returncode == 0 and "0 violations, 0 warnings" in check.stdout, check.stdout + check.stderr
    generated = subprocess.run([sys.executable, str(SCRIPTS / "features"), "generate", "--root", str(reworded),
                                "--check"], capture_output=True, text=True)
    assert generated.returncode == 0, generated.stdout + generated.stderr
    logic = subprocess.run([sys.executable, str(SCRIPTS / "spec"), "--root", str(reworded), "logic"],
                           capture_output=True, text=True)
    assert logic.returncode == 0 and "no findings" in logic.stdout, logic.stdout + logic.stderr
