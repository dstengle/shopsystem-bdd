"""shop_contexts: an id the shop's product id covers kept whatever its last part (b576, shop r1; review f1), the
context id form refused by no line of shop's yet."""
import subprocess
import tomllib

import shop_contexts

INDEX = "---\nid: bounded-context/example.org/home/home\nkind: bounded-context\nlanguage: codified-2\n---\n\n# home\n"


def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


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
    kept = tomllib.loads((repo / shop_contexts.REL).read_text())["contexts"]
    assert kept == [ident]
    assert _git(repo, "status", "--porcelain") == ""
