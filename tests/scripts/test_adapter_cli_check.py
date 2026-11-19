"""adapter_cli and adapter_cli_check: the CLI contract read, and checked both ways against the domain model and the
program's argparse, v_a1-v_a4 (the domain contract design, §6.1)."""
import pathlib
import shutil

import adapter_annotate
import adapter_cli
import adapter_cli_check
import pytest
from shop_refused import Refused

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"
SCRIPTS = str(FIXTURE.parents[3] / "scripts")


@pytest.fixture
def context(tmp_path):
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURE, root)
    program = root / "notes_cli.py"
    program.write_text(program.read_text().replace('Path(__file__).resolve().parents[4] / "scripts"', repr(SCRIPTS)))
    _contract(root).write_text(adapter_annotate.annotated(_contract(root).read_text(), {}))    # no requirements held
    return root


def _contract(root):
    return root / "spec" / "adapters" / "cli.toml"


def _edit(root, old, new):
    path = _contract(root)
    text = path.read_text()
    assert old in text
    path.write_text(text.replace(old, new))


def _codes(root):
    return [(code, subject) for code, subject, _ in adapter_cli_check.problems(root)]


def test_the_fixture_is_clean():
    assert adapter_cli_check.problems(FIXTURE) == []


def test_no_contract_no_problems(context):
    _contract(context).unlink()
    assert adapter_cli.read(context) is None and adapter_cli_check.problems(context) == []


def test_v_a1_an_operation_with_no_table(context):
    _edit(context, '[operations."notes.list"]\ncommand = "notes list"\n', "")
    assert ("v_a1", "notes.list") in _codes(context)


def test_v_a1_not_for_an_unexposed_operation(context):
    _edit(context, '[operations."notes.list"]\ncommand = "notes list"\n', '[unexposed]\noperations = ["notes.list"]\n')
    _edit(context, 'options = ["--root", "--json"]', 'options = ["--root", "--json"]\ncommands = ["notes list"]')
    assert _codes(context) == []


def test_v_a2_a_table_naming_no_operation_or_parameter(context):
    _edit(context, '[operations."notes.list"]', '[operations."notes.lists"]')
    _edit(context, 'tag = { option = "--tag", repeat = true }', 'tag = { option = "--tag", repeat = true }\n'
                   'colour = { option = "--colour" }')
    found = _codes(context)
    assert ("v_a2", "notes.lists") in found and ("v_a2", "notes.label.colour") in found


def test_v_a3_a_command_or_an_option_argparse_lacks(context):
    _edit(context, 'command = "notes archive"', 'command = "notes shelve"')
    _edit(context, 'priority = { option = "--priority"', 'priority = { option = "--urgency"')
    found = _codes(context)
    assert ("v_a3", "notes.archive") in found and ("v_a3", "notes add --urgency") in found


def test_v_a3_a_program_the_contract_does_not_name(context):
    _edit(context, 'notes = "notes_cli.py"', 'notes = "missing.py"')
    assert ("v_a3", "notes.add") in _codes(context)


def test_v_a4_an_option_or_a_command_no_table_names(context):
    program = context / "notes_cli.py"
    text = program.read_text()
    text = text.replace('    sub.add_parser("list")\n', '    sub.add_parser("list").add_argument("--since")\n'
                                                           '    sub.add_parser("export")\n')
    program.write_text(text)
    found = _codes(context)
    assert ("v_a4", "notes list --since") in found and ("v_a4", "notes export") in found


def test_reading_the_argparse_runs_nothing_of_the_program_here(context, tmp_path, monkeypatch):
    """The program is read in a process of its own, in a scratch folder, with no input: a main that reads stdin and
    writes a file before it parses neither hangs the check nor writes beside it, and a module of the program's folder
    named as one of the plugin's (loaded here) is the program's own."""
    (context / "domain_model.py").write_text("OWN = True\n")
    (context / "notes_cli.py").write_text(
        "import argparse, sys\nfrom pathlib import Path\nimport domain_model\n\n\n"
        "def main(argv=None):\n    sys.stdin.read()\n    Path('written.txt').write_text('x')\n"
        "    assert domain_model.OWN\n    ap = argparse.ArgumentParser(prog='notes')\n"
        "    ap.add_subparsers().add_parser('add')\n    return ap.parse_args(argv)\n")
    monkeypatch.chdir(tmp_path)
    found = adapter_cli_check.problems(context)
    assert not [f for f in found if "does not parse" in f[2]] and ("v_a3", "notes add --text") in _codes(context)
    assert not (tmp_path / "written.txt").exists() and not (context / "written.txt").exists()


def test_a_program_that_never_parses_is_v_a3(context):
    (context / "notes_cli.py").write_text("def main(argv=None):\n    return 0\n")
    assert ("v_a3", "notes.add") in _codes(context)


def test_a_business_reference_rendered_as_its_option():
    contract = adapter_cli.read(FIXTURE)
    assert contract.spell("parameter:text", "notes.add") == "--text"
    assert contract.spell("parameter:note", "notes.file") == "note"
    assert contract.spell("note:n3") == "n3"
    assert contract.by_command("notes add").id == "notes.add"


def test_a_contract_that_does_not_read_is_refused(context):
    _contract(context).write_text("[operations\n")
    with pytest.raises(Refused, match="cli.toml does not read"):
        adapter_cli.read(context)


def test_model_check_reports_them(context):
    import json
    import subprocess
    import sys
    _edit(context, '[operations."notes.list"]\ncommand = "notes list"\n', "")
    done = subprocess.run([sys.executable, str(FIXTURE.parents[3] / "scripts" / "spec"), "--root", str(context),
                           "check", "--json"], capture_output=True, text=True)
    found = json.loads(done.stdout)
    assert found["outcome"] == "failed" and done.returncode == 1
    why = "the operation notes.list has no table in spec/adapters/cli.toml and is not unexposed"
    assert ["v_a1", ["notes.list", why]] in found["content"]["violations"]
