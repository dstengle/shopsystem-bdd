"""contract_form: the contract `spec prepare` prints, in the contract form (b547, checking r64-r66)."""
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import contract_form

FIXTURE = Path(__file__).parent / "fixtures" / "domain-model"
SPEC = Path(__file__).resolve().parents[2] / "scripts" / "spec"


def _context(tmp_path):
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")
    path = tmp_path / "spec" / "model" / "notes.md"
    path.write_text(path.read_text().replace("  operation file(note)\n", "  operation file(note)  idempotent by note\n")
                    .replace("raised by notes.add\n", "raised by notes.add; delivery: at least once\n"))
    return tmp_path


def test_the_contract_conforms_and_holds_requirements_and_properties(tmp_path):
    text = contract_form.render(_context(tmp_path), "1.0.0")
    assert contract_form.problems(text) == []
    data = tomllib.loads(text)
    assert (data["context"], data["version"]) == ("bounded-context/example.org/fixture/domain-model", "1.0.0")
    filed = data["operations"]["notes.file"]
    assert filed["properties"] == ["idempotent by note"] and filed["reasons"] == ["not a draft note"]
    assert any(r.startswith("notebook#r7: ") for r in filed["requirements"])
    assert data["events"]["a note is added"] == {"raised_by": "notes.add", "properties": ["delivery: at least once"]}
    assert data["objects"]["note"]["relations"] == ["carries → tag (many)"]


def test_a_text_out_of_the_form_is_named():
    assert contract_form.problems('version = "1"\nextra = 1\n[operations."a.b"]\noutcomes = "done"\n') == [
        "the contract has no context", "the contract: extra is no key of the contract form",
        "operations.a.b: outcomes is not a list of strings"]
    assert contract_form.problems("not toml =")[0].startswith("the contract does not read as TOML")


def test_spec_prepare_prints_it_and_writes_nothing(tmp_path):
    root = _context(tmp_path)
    before = sorted((p, p.read_bytes()) for p in root.rglob("*") if p.is_file())
    done = subprocess.run([sys.executable, str(SPEC), "--root", str(root), "prepare", "--contract", "2.1.0"],
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    assert tomllib.loads(done.stdout)["version"] == "2.1.0"
    assert sorted((p, p.read_bytes()) for p in root.rglob("*") if p.is_file()) == before
