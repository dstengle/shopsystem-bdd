"""`model rules --write` and `--check` (design-model-check r73, r72): the rule catalogue grammar/rules.md, every rule
with a failing and a passing example that does what it says, and the plugin's own catalogue current."""
import subprocess
import sys

import model_rules
from backlog_testing import REPO, SCRIPTS


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPTS / "model"), *map(str, args)], capture_output=True, text=True,
                          timeout=120)


def test_every_rule_has_examples_that_do_what_they_say():
    entries = model_rules.rules()
    assert len({e[0] for e in entries}) == len(entries)
    assert model_rules.wrong(entries) == []


def test_a_rule_whose_example_does_not_fire_is_named():
    entry = ("v15a", "a requirement has no id", 'node("q","requirement"). req_id("q","c",1).', "x.", "facts")
    assert model_rules.wrong([entry]) == ["v15a does not fire on its failing example"]
    assert model_rules.wrong([entry[:2] + (None, "x.", "facts")]) == ["v15a has no failing example"]


def test_the_lines_citing_a_rule_are_listed(tmp_path):
    (tmp_path / "spec" / "capabilities").mkdir(parents=True)
    (tmp_path / "spec" / "capabilities" / "thing.md").write_text(
        "- [r4] If ..., then `model` shall exit with an error naming `v15a`.\n- [r5] ... print \"v_t11\".\n")
    assert model_rules.citing(tmp_path) == {"v15a": ["thing#r4"], "v_t11": ["thing#r5"]}


def test_write_then_check_then_stale(tmp_path):
    assert run("--root", tmp_path, "rules", "--check").returncode == 1
    done = run("--root", tmp_path, "rules", "--write")
    assert done.returncode == 0, done.stderr
    text = (tmp_path / "grammar" / "rules.md").read_text()
    assert "## v15a" in text and "## v_t7" in text and "- Severity: warning" in text
    assert run("--root", tmp_path, "rules", "--check").returncode == 0
    (tmp_path / "grammar" / "rules.md").write_text(text + "\nedited\n")
    done = run("--root", tmp_path, "rules", "--check")
    assert done.returncode == 1 and "grammar/rules.md" in done.stdout
    assert (tmp_path / "grammar" / "rules.md").read_text() == text + "\nedited\n"


def test_write_and_check_are_not_given_together(tmp_path):
    assert run("--root", tmp_path, "rules", "--write", "--check").returncode == 2


def test_the_plugins_catalogue_is_current():
    done = run("--root", REPO, "rules", "--check")
    assert done.returncode == 0, done.stdout + done.stderr + "\nrun `model rules --write`"
