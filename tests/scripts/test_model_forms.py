"""`model forms` (design-model-check r55): each file form with its path and what writes it; each command it names
exists, and each item it names is in the plugin's backlog."""
import json
import re
import subprocess
import sys

import model_forms
import pytest
from backlog_testing import REPO, SCRIPTS


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, timeout=60)


@pytest.mark.parametrize("command", sorted({tuple(f.command) for f in model_forms.FORMS if f.command}))
def test_each_command_it_names_exists(command):
    script, *words = [w for w in command if not w.startswith("--")]
    done = run(SCRIPTS / script, *words, "--help")
    assert done.returncode == 0, (command, done.stderr)
    for flag in (w for w in command if w.startswith("--")):
        assert flag in done.stdout, (command, done.stdout)


def test_each_form_without_a_command_names_an_item_or_the_hand():
    for form in model_forms.FORMS:
        if form.command:
            continue
        found = re.fullmatch(r"plugin item (b\d+) \(no command yet\)", form.writer)
        assert found or form.writer == "by hand (no command yet)", form
        assert not found or (REPO / ".shop" / "backlog" / ("%s.md" % found.group(1))).is_file(), form


def test_each_item_it_names_is_open():
    """A form names an item that will give it a command only while that item is open (b451)."""
    for form in model_forms.FORMS:
        found = re.fullmatch(r"plugin item (b\d+) \(no command yet\)", form.writer)
        if found:
            text = (REPO / ".shop" / "backlog" / ("%s.md" % found.group(1))).read_text()
            assert not re.search(r"^status: (delivered|withdrawn|refused)$", text, re.MULTILINE), form


def test_it_lists_the_catalogues_the_corpus_and_the_packs():
    paths = {f.path for f in model_forms.FORMS}
    for path in ("grammar/constructs.md", "grammar/corpus/spec/<capability>.md", "grammar/catalogue-entries.toml",
                 "spec/packs/<name>.md"):
        assert path in paths, path


def test_it_lists_no_working_rules():
    """CLAUDE.md is the person's and the sessions' working rules, no file form of a bounded context (b473)."""
    assert "CLAUDE.md" not in {f.path for f in model_forms.FORMS}


def test_it_prints_every_form_on_its_line(tmp_path):
    done = run(SCRIPTS / "spec", "--root", tmp_path, "forms")
    assert done.returncode == 0, done.stderr
    lines = done.stdout.splitlines()
    assert len(lines) == len(model_forms.FORMS)
    for line, form in zip(lines, model_forms.FORMS):
        assert re.fullmatch(r"%s +%s +%s" % tuple(map(re.escape, form)), line), line
    for path, writer in (("spec/decisions/<nnnn>-<slug>.md", "work decision"),
                         (".shop/records/<date>-<slug>.md", "work record")):
        assert any(f.path == path and f.writer == writer for f in model_forms.FORMS)


def test_json_is_one_object(tmp_path):
    done = run(SCRIPTS / "spec", "--root", tmp_path, "forms", "--json")
    forms = json.loads(done.stdout)["content"]["forms"]
    assert forms == [dict(f._asdict(), kind=f.kind) for f in model_forms.FORMS]
    assert {f["kind"] for f in forms} == {"command", "item", "hand"}


def test_check_refuses_each_form_by_hand_and_passes_with_none(monkeypatch, capsys):
    """`--check` names each form written by hand and exits 1 (b317, b451); with none it exits 0, printing nothing."""
    hand = [f for f in model_forms.FORMS if f.kind == "hand"]
    done = run(SCRIPTS / "spec", "--root", REPO, "forms", "--check")
    assert (done.returncode, done.stdout) == (1 if hand else 0, "")
    for form in hand:
        assert "%s (%s) is written by hand" % (form.name, form.path) in done.stderr
    args = type("A", (), {"check": True, "json": False})()
    monkeypatch.setattr(model_forms, "FORMS", [f for f in model_forms.FORMS if f.kind != "hand"])
    assert model_forms.cmd_forms(args) == 0
    monkeypatch.setattr(model_forms, "FORMS", model_forms.FORMS + [model_forms.Form("x", "x.md", "by hand")])
    assert model_forms.cmd_forms(args) == 1
    assert "x (x.md) is written by hand" in capsys.readouterr().err
