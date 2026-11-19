"""driver_cli, the protocol driver of the CLI adapter (the domain contract design, §6.2): argv built from a request
by the fixture's spec/adapters/cli.toml, and the envelope read back for done, returned and refused."""
import pathlib
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import adapter_cli
import driver_cli

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"


@pytest.fixture
def contract():
    return adapter_cli.read(FIXTURE)


def test_argv_of_an_option_and_a_flag(contract):
    assert adapter_cli.argv(contract, "notes.add", {"text": "Milk", "priority": "high", "reminder": True}) == [
        "notes", "add", "--text", "Milk", "--priority", "high", "--reminder"]


def test_argv_fills_in_the_examples(contract):
    assert adapter_cli.argv(contract, "notes.add") == ["notes", "add", "--text", "A note", "--priority", "low"]
    assert adapter_cli.argv(contract, "notes.add", without=["text"]) == ["notes", "add", "--priority", "low"]


def test_argv_of_a_positional_and_a_repeat(contract):
    assert adapter_cli.argv(contract, "notes.label", {"note": "n2", "tag": ["home", "shop"]}) == [
        "notes", "label", "n2", "--tag", "home", "--tag", "shop"]
    assert adapter_cli.argv(contract, "notes.file") == ["notes", "file", "n1"]


def test_a_parameter_the_operation_lacks_is_refused(contract):
    from shop_refused import Refused
    with pytest.raises(Refused, match="no parameter colour"):
        adapter_cli.argv(contract, "notes.add", {"colour": "red"})


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    return tmp_path


def test_done_returned_and_refused(repo):
    added = driver_cli.request(repo, "notes.add", {"text": "Milk"}, contract_root=FIXTURE)
    assert added.response.outcome == "done" and added.done.returncode == 0
    assert added.response.content["text"] == "Milk"
    listed = driver_cli.request(repo, "notes.list", contract_root=FIXTURE)
    assert [n["text"] for n in driver_cli.returned(listed)] == ["Milk"]
    driver_cli.request(repo, "notes.file", {"note": "n1"}, contract_root=FIXTURE)
    again = driver_cli.request(repo, "notes.file", {"note": "n1"}, contract_root=FIXTURE)
    assert driver_cli.refused(again, "note:n1") and again.done.returncode == 1
    assert again.response.errors == [{"reason": "not a draft note", "names": ["note:n1"]}]


def test_a_refusal_names_the_parameter(repo):
    refused = driver_cli.request(repo, "notes.add", without=["text"], contract_root=FIXTURE)
    assert driver_cli.refused(refused, "parameter:text")
    assert "--text" in refused.done.stderr
    assert not driver_cli.kept(refused, repo, ["notes.json"])
