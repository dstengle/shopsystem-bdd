"""adapter_cli and adapter_cli_check: the CLI contract read, and checked both ways against the domain model and the
program's argparse, v_a1-v_a4 (the domain contract design, §6.1)."""
import pathlib
import shutil

import adapter_cli
import adapter_cli_check
import pytest
from shop_refused import Refused

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"


@pytest.fixture
def context(tmp_path):
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURE, root)
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
    program.write_text(text.replace('parents[4] / "scripts"', 'parents[0] / "scripts"'))
    (context / "scripts").symlink_to(FIXTURE.parents[3] / "scripts")
    found = _codes(context)
    assert ("v_a4", "notes list --since") in found and ("v_a4", "notes export") in found


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
