"""The CLI spelling of a positional parameter (b807): no positional of the plugin's tools shows a metavar or dest with
an underscore or in upper case in its usage, and a refusal naming a positional parameter spells it by its metavar, the
`--json` errors' names unchanged (adapter_cli_respond's `spelling`)."""
import argparse
import json
import subprocess
import sys

import adapter_cli_respond
import docs_testing
import product_store

SHOP = docs_testing.REPO / "scripts" / "shop"


def _positionals(p, words):
    for action in p._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, child in action.choices.items():
                yield from _positionals(child, words + [name])
        elif not action.option_strings:
            yield " ".join(words), str(action.metavar or action.dest)


# `features` left out until b817 ("features generate and features vocab show their positionals readably") gives
# its positionals readable metavars and takes this exclusion out
CHECKED = tuple(tool for tool in docs_testing.TOOLS if tool != "features")


def test_no_positional_is_shown_with_an_underscore_or_in_upper_case():
    bad = [(words, shown) for tool in CHECKED for words, shown in _positionals(docs_testing.parser(tool), [tool])
           if "_" in shown or shown != shown.lower()]
    assert bad == []


def test_spelling_gives_a_positional_its_metavar_and_an_option_its_option():
    p = argparse.ArgumentParser()
    p.add_argument("product_actor", metavar="product actor")
    p.add_argument("job")
    p.add_argument("--in", dest="bounded_context")
    spell = adapter_cli_respond.spelling(p)
    assert spell("parameter:product actor") == "product actor"
    assert spell("parameter:job") == "job"
    assert spell("parameter:bounded context") == "--in"


def _repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (["init", "-q", "-b", "main"], ["config", "user.name", "t"], ["config", "user.email", "t@example.org"]):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
    product = {**product_store.empty(), "id": "example.org", "purpose": "a product", "actors": ["the developer"]}
    product_store.kept(repo, product, "fixture")
    return repo


def _plays(repo, *extra):
    return subprocess.run([sys.executable, str(SHOP), "spec", "--root", str(repo), "plays", "nobody", "--in",
                           "bounded-context/example.org/x", "--as", "the person", *extra],
                          capture_output=True, text=True)


def test_a_refusal_of_a_positional_spells_it_by_its_metavar(tmp_path):
    run = _plays(_repo(tmp_path))
    assert run.returncode == 1
    assert "product actor 'nobody'" in run.stderr
    assert "product_actor" not in run.stderr


def test_the_json_errors_name_the_parameter_unchanged(tmp_path):
    run = _plays(_repo(tmp_path), "--json")
    assert run.returncode == 1
    errors = json.loads(run.stdout)["errors"]
    assert any("parameter:product actor" in e["names"] for e in errors)
