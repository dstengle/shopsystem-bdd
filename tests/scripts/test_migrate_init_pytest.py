"""A fresh context's tests run with plain pytest (b419): `migrate init`'s tests/scenarios/conftest.py loads the
plugin's pytest plugin, found by `$CLAUDE_PLUGIN_ROOT` or else the plugin cache's folder of the release
`.shop/plugin-version` names, which registers each @g<n> and @r<n> tag as a mark and keeps an unbuilt scenario a
strict xfail; no PYTHONPATH and no `-p work_items`."""
import json
import os
import subprocess
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]

CAPABILITY = """---
id: capability/example.org/notes/notes-cli/notes
title: Notes
narrator: the person
group: service
language: codified-2
retired: []
unbuilt: [r2]
---

# Notes

## Purpose

Notes.

## Behaviour

### [g1] A note is kept
- [r1] When the person adds a note, the notes service shall keep the note.
- [r2] When the person removes a note, the notes service shall forget the note.
"""

FEATURE = """Feature: Notes

  @g1 @r1
  Scenario: A note is kept
    Given a note n1
    Then the note n1 is kept

  @g1 @r2
  Scenario: A note is forgotten
    Given a note n1
    Then the note n1 is forgotten
"""

STEPS = '''from pytest_bdd import given, parsers, scenarios, then

scenarios("../../features/notes.feature")


@given(parsers.parse("a note {n}"), target_fixture="notes")
def a_note(n):
    return [n]


@then(parsers.parse("the note {n} is kept"))
def kept(notes, n):
    assert n in notes


@then(parsers.parse("the note {n} is forgotten"))
def forgotten(notes, n):
    assert n not in notes
'''


def context(tmp_path):
    """A context `migrate init` founded, with one capability, its feature and its test module."""
    root = tmp_path / "ctx"
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    for key, value in (("user.name", "Test"), ("user.email", "test@example.org")):
        subprocess.run(["git", "-C", str(root), "config", key, value], check=True)
    subprocess.run([sys.executable, str(PLUGIN / "scripts" / "migrate"), "init", "--id",
                    "bounded-context/example.org/notes/notes-cli"], cwd=root, check=True, capture_output=True)
    (root / "spec/capabilities/notes.md").write_text(CAPABILITY)
    (root / "features/notes.feature").write_text(FEATURE)
    (root / "tests/scenarios/test_notes.py").write_text(STEPS)
    return root


def plain_pytest(root, **env):
    """`python -m pytest` in the context with no PYTHONPATH, an unknown mark an error."""
    clean = {k: v for k, v in os.environ.items()
             if k not in ("PYTHONPATH", "CLAUDE_PLUGIN_ROOT", "CLAUDE_CONFIG_DIR") and not k.startswith("PYTEST")}
    clean.update(env)
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-rxX", "-p", "no:cacheprovider",
                           "-W", "error::pytest.PytestUnknownMarkWarning"],
                          cwd=root, capture_output=True, text=True, env=clean)


def assert_marked(done):
    out = done.stdout + done.stderr
    assert done.returncode == 0, out
    assert "1 passed, 1 xfailed" in out, out
    assert "unbuilt: notes#r2" in out, out
    assert "PytestUnknownMarkWarning" not in out, out


def test_plain_pytest_finds_the_plugin_by_its_root(tmp_path):
    assert_marked(plain_pytest(context(tmp_path), CLAUDE_PLUGIN_ROOT=str(PLUGIN)))


def test_plain_pytest_finds_the_plugin_in_the_cache(tmp_path):
    root = context(tmp_path)
    version = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())["version"]
    assert (root / ".shop/plugin-version").read_text().strip() == version
    cache = tmp_path / "claude" / "plugins" / "cache" / "market" / "shopsystem-bdd"
    cache.mkdir(parents=True)
    (cache / version).symlink_to(PLUGIN)
    assert_marked(plain_pytest(root, CLAUDE_CONFIG_DIR=str(tmp_path / "claude")))


def test_an_unbuilt_scenario_that_passes_fails_the_run(tmp_path):
    root = context(tmp_path)
    (root / "tests/scenarios/test_notes.py").write_text(STEPS.replace("n not in notes", "n in notes"))
    done = plain_pytest(root, CLAUDE_PLUGIN_ROOT=str(PLUGIN))
    assert done.returncode == 1, done.stdout + done.stderr
    assert "XPASS(strict)" in done.stdout, done.stdout
