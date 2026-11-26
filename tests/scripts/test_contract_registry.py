"""contract_registry and its shop-folder adapter (b636): a contract deposited kept at its version as the published one
and the one published before superseded, committed; one retrieved published (of the highest version) or at a
version, a version never deposited refused naming it; a bounded context of the same shop read from its own folder,
never GitHub (b622); `$SHOPSYSTEM_CONTRACT_REGISTRY` an adapter run in place of the shop folder's."""
import subprocess

import contract_registry
import contract_registry_folder
import pytest
from shop_refused import Refused

INDEX = "---\nid: bounded-context/example.org/shop/%s\nlanguage: codified-2\n---\n"
CONTRACT = 'context = "c"\nversion = "%s"\nstatus = "published"\n'


def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


def _shop(tmp_path, monkeypatch):
    """A shop of two contexts in `contexts/`, one git repository, no adapter swapped in and no gh to call."""
    monkeypatch.delenv(contract_registry.ADAPTER, raising=False)
    monkeypatch.setenv("SHOPSYSTEM_WORK_GH", "false")
    for name in ("notebook", "sharing"):
        (tmp_path / "contexts" / name / "spec").mkdir(parents=True)
        (tmp_path / "contexts" / name / "spec" / "index.md").write_text(INDEX % name)
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "user.email", "t@example.org")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "shop")
    return tmp_path / "contexts" / "notebook", tmp_path / "contexts" / "sharing"


def test_a_deposit_supersedes_the_published_contract(tmp_path, monkeypatch):
    notebook, _ = _shop(tmp_path, monkeypatch)
    contract_registry.deposit(notebook, CONTRACT % "1.9.0", "1.9.0")
    done = contract_registry.deposit(notebook, CONTRACT % "1.10.0", "1.10.0")
    assert done == {"kept": ".shop/contracts/1.10.0/contract.toml",
                    "superseded": [".shop/contracts/1.9.0/contract.toml"]}
    assert contract_registry_folder.kept(notebook)["1.9.0"][1] == "superseded"
    assert contract_registry.retrieve(notebook) == ("1.10.0", (CONTRACT % "1.10.0").encode())
    assert ".shop/contracts/1.10.0/contract.toml" in _git(notebook, "show", "--name-only", "HEAD")


def test_a_version_never_deposited_is_refused_naming_it(tmp_path, monkeypatch):
    notebook, _ = _shop(tmp_path, monkeypatch)
    with pytest.raises(Refused) as refused:
        contract_registry.retrieve(notebook, None, "2.0.0")
    assert refused.value.reason == contract_registry.REASON and refused.value.names == ["version:2.0.0"]


def test_a_context_of_the_same_shop_is_read_from_its_folder(tmp_path, monkeypatch):
    notebook, sharing = _shop(tmp_path, monkeypatch)
    contract_registry.deposit(notebook, CONTRACT % "1.0.0", "1.0.0")
    context = "bounded-context/example.org/shop/notebook"
    assert contract_registry.retrieve(sharing, context, "1.0.0") == ("1.0.0", (CONTRACT % "1.0.0").encode())
    with pytest.raises(Refused) as refused:
        contract_registry.retrieve(sharing, context, "3.0.0")
    assert refused.value.names == ["version:3.0.0"]


def test_the_adapter_named_is_run_in_place_of_the_shop_folders(tmp_path, monkeypatch):
    adapter = tmp_path / "adapter.py"
    adapter.write_text("def retrieve(root, context=None, version=None):\n    return 'stood in', b''\n")
    monkeypatch.setenv(contract_registry.ADAPTER, str(adapter))
    assert contract_registry.retrieve(tmp_path) == ("stood in", b"")
