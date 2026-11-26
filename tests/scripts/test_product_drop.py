"""product_drop: a drop of a job, a product actor, a subdomain or a bounded context the product does not hold
completes with the product file unchanged and nothing committed (b795, product r46, r48, r52, r56; review f1)."""
import argparse
import subprocess

import product_drop_cli
import product_store
import pytest


def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


def _repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(tmp_path, "init", "-q", "-b", "main", str(repo))
    _git(repo, "config", "user.name", "t")
    _git(repo, "config", "user.email", "t@example.org")
    product = {**product_store.empty(), "id": "example.org", "purpose": "a product", "actors": ["the developer"]}
    product_store.kept(repo, product, "fixture")
    return repo


@pytest.mark.parametrize("what,dest", [("job", "job"), ("actor", "product_actor"), ("subdomain", "subdomain"),
                                       ("context", "bounded_context")])
def test_a_drop_of_what_the_product_does_not_hold_completes_unchanged(tmp_path, capsys, what, dest):
    repo = _repo(tmp_path)
    before, head = (repo / product_store.REL).read_text(), _git(repo, "rev-parse", "HEAD")
    args = argparse.Namespace(root=repo, what=what, **{dest: "unheld"})
    assert product_drop_cli.cmd_drop(args) == 0
    assert (repo / product_store.REL).read_text() == before
    assert _git(repo, "rev-parse", "HEAD") == head


def test_a_drop_with_no_product_file_writes_none(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(tmp_path, "init", "-q", "-b", "main", str(repo))
    assert product_drop_cli.cmd_drop(argparse.Namespace(root=repo, what="job", job="unheld")) == 0
    assert not (repo / product_store.REL).exists()
