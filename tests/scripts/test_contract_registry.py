"""contract_registry and its shop-folder adapter (b636): a contract deposited kept at its version as the published one
and the one published before superseded, committed, the reply done; one retrieved published (of the highest version)
or at a version, the reply returned, a version never deposited the reply refused naming it; a bounded context of the same shop read from its own folder,
never GitHub (b622); `$SHOPSYSTEM_CONTRACT_REGISTRY` an adapter run in place of the shop folder's."""
import subprocess

import contract_registry
import contract_registry_folder

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
    assert done.outcome == "done" and done.content == {"kept": ".shop/contracts/1.10.0/contract.toml",
                    "superseded": [".shop/contracts/1.9.0/contract.toml"]}
    assert contract_registry_folder.kept(notebook)["1.9.0"][1] == "superseded"
    assert contract_registry.retrieve(notebook).content == ("1.10.0", (CONTRACT % "1.10.0").encode())
    assert ".shop/contracts/1.10.0/contract.toml" in _git(notebook, "show", "--name-only", "HEAD")


def test_a_version_never_deposited_is_refused_naming_it(tmp_path, monkeypatch):
    notebook, _ = _shop(tmp_path, monkeypatch)
    reply = contract_registry.retrieve(notebook, None, "2.0.0")
    assert reply.outcome == "refused" and reply.errors == [{"reason": contract_registry.REASON,
                                                           "names": ["version:2.0.0"]}]


def test_a_context_of_the_same_shop_is_read_from_its_folder(tmp_path, monkeypatch):
    notebook, sharing = _shop(tmp_path, monkeypatch)
    contract_registry.deposit(notebook, CONTRACT % "1.0.0", "1.0.0")
    context = "bounded-context/example.org/shop/notebook"
    assert contract_registry.retrieve(sharing, context, "1.0.0").content == ("1.0.0", (CONTRACT % "1.0.0").encode())
    assert contract_registry.retrieve(sharing, context, "3.0.0").errors[0]["names"] == ["version:3.0.0"]


def test_the_adapter_named_is_run_in_place_of_the_shop_folders(tmp_path, monkeypatch):
    adapter = tmp_path / "adapter.py"
    adapter.write_text("def retrieve(root, context=None, version=None):\n    return 'stood in', b''\n")
    monkeypatch.setenv(contract_registry.ADAPTER, str(adapter))
    assert contract_registry.retrieve(tmp_path) == ("stood in", b"")


def _stand_in(tmp_path, monkeypatch, reply):
    adapter = tmp_path / "adapter.py"
    adapter.write_text("import contract_registry\n\ndef retrieve(root, context=None, version=None):\n    return %s\n"
                       % reply)
    monkeypatch.setenv(contract_registry.ADAPTER, str(adapter))


def test_fetch_prints_the_contract_the_registry_returns(tmp_path, monkeypatch, capsys):
    import contract_publish
    _stand_in(tmp_path, monkeypatch, "contract_registry.returned('1.2.0', b'returned = 1\\n')")
    assert contract_publish.fetch(tmp_path, "1.2.0").content == "returned = 1\n"
    assert capsys.readouterr().out == "returned = 1\n"


def test_fetch_names_the_version_the_registry_refuses(tmp_path, monkeypatch):
    import contract_publish
    import pytest
    from plumbing.shop_refused import Refused
    _stand_in(tmp_path, monkeypatch, "contract_registry.undeposited('1.2.0')")
    with pytest.raises(Refused) as refused:
        contract_publish.fetch(tmp_path)
    assert refused.value.names == ["version:1.2.0"]


def test_publish_with_no_version_passes_every_version_deposited(tmp_path, monkeypatch, capsys):
    """After 1.6 then 1.5 (1.5 published, 1.6 superseded), no version is 1.7, never the 1.6 kept already (f1)."""
    import contract_form
    import contract_publish
    notebook, _ = _shop(tmp_path, monkeypatch)
    monkeypatch.setattr(contract_publish, "nonconforming", lambda root: [])
    monkeypatch.setattr(contract_form, "render", lambda root, version: 'context = "c"\nversion = "%s"\n' % version)
    for version in ("1.6", "1.5", None):
        assert contract_publish.publish(notebook, version) == 0
    assert capsys.readouterr().out.splitlines()[-2] == "published .shop/contracts/1.7/contract.toml"
