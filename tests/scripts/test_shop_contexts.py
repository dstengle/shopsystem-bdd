"""shop_contexts: an id the shop's product id covers kept whatever its last part (b576, shop r1; review f1), the
context id form refused by no line of shop's yet; with no product file kept, an id under another product kept (shop r1,
r6 applying only while the product of the shop has an id: b666, review f1)."""
import subprocess
import tomllib

import product_store
import pytest
import shop_contexts
from shop_refused import Refused

INDEX = "---\nid: bounded-context/example.org/home/home\nkind: bounded-context\nlanguage: codified-2\n---\n\n# home\n"


def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


def _repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "spec").mkdir(parents=True)
    (repo / "spec" / "index.md").write_text(INDEX)
    _git(tmp_path, "init", "-q", "-b", "main", str(repo))
    _git(repo, "config", "user.name", "t")
    _git(repo, "config", "user.email", "t@example.org")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")
    return repo


def test_with_no_product_file_an_id_under_another_product_is_kept(tmp_path, capsys):
    repo = _repo(tmp_path)
    ident = "bounded-context/elsewhere.org/away/notes"
    assert shop_contexts.keep(repo, ident) == 0
    assert capsys.readouterr().out == "kept %s\n" % ident
    assert tomllib.loads((repo / shop_contexts.REL).read_text())["contexts"] == [ident]


def test_an_id_the_product_id_covers_out_of_the_context_id_form_is_kept(tmp_path, capsys):
    repo = tmp_path / "repo"
    (repo / "spec").mkdir(parents=True)
    (repo / "spec" / "index.md").write_text(INDEX)
    _git(tmp_path, "init", "-q", "-b", "main", str(repo))
    _git(repo, "config", "user.name", "t")
    _git(repo, "config", "user.email", "t@example.org")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")
    ident = "bounded-context/example.org/home/A B"
    assert shop_contexts.keep(repo, ident) == 0
    assert capsys.readouterr().out == "kept %s\n" % ident
    kept = tomllib.loads((repo / shop_contexts.REL).read_text())["contexts"]
    assert kept == [ident]
    assert _git(repo, "status", "--porcelain") == ""


def test_an_id_the_product_does_not_cover_is_refused_with_the_declared_reason(tmp_path):
    repo = _repo(tmp_path)
    (repo / ".shop" / "product").mkdir(parents=True)
    product = {"id": "example.org/notes", "purpose": "notes", "actors": [], "jobs": {}}
    (repo / product_store.REL).write_text(product_store.render(product))
    ident = "bounded-context/example.org/home/away"
    with pytest.raises(Refused) as refused:
        shop_contexts.keep(repo, ident)
    assert refused.value.reason == "id outside the product"
    assert "example.org/notes" in str(refused.value) and "product id" not in str(refused.value)
