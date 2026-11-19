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
    assert json.loads(done.stdout)["content"] == {"forms": [f._asdict() for f in model_forms.FORMS]}


def test_check_passes_this_repository_and_refuses_a_form_by_hand(tmp_path, monkeypatch, capsys):
    """No form of this plugin is written by hand: a new form by hand fails here (b317)."""
    done = run(SCRIPTS / "spec", "--root", REPO, "forms", "--check")
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")
    monkeypatch.setattr(model_forms, "FORMS", model_forms.FORMS + [model_forms.Form("x", "x.md", "by hand")])
    assert model_forms.cmd_forms(type("A", (), {"check": True, "json": False})()) == 1
    assert "x (x.md) is written by hand" in capsys.readouterr().err
