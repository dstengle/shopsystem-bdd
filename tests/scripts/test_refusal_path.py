"""One refusal path (b145, design-decision one-refusal-path): every command's refusal is a shop_refused.Refused, and
each tool catches that base once, prints `<tool>: <reason>`, exits 1 and changes nothing."""
import importlib.machinery
import importlib.util
import pathlib
import subprocess
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import batch_git
import features_gherkin
import shop_files
import shop_refused
import tools_env
import tools_grammar
import transcripts

IMPORTERS = ("shop_files", "tools_env", "tools_grammar", "features_gherkin", "transcripts", "shop_refused")


def test_every_refusal_class_reaches_the_one_base():
    for cls in (shop_files.Refused, tools_env.Refused, tools_grammar.Refused, features_gherkin.Refused,
                transcripts.Refused, batch_git.GitFailed):
        assert issubclass(cls, shop_refused.Refused), cls
    assert shop_files.Refused is shop_refused.Refused


@pytest.mark.parametrize("name", IMPORTERS)
def test_each_importer_imports_alone(name):
    done = subprocess.run([sys.executable, "-I", "-c", "import sys; sys.path.insert(0, %r); import %s"
                           % (str(SCRIPTS), name)], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr


def _git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


def _state(repo):
    return _git(repo, "rev-parse", "HEAD"), _git(repo, "status", "--porcelain", "--untracked-files=all")


CASES = {
    "work": (["work", "show", "b9"], ["work: there is no item b9"], {}),
    "tools": (["tools", "--python", "/nonexistent/python", "probe"], ["tools: no analysis tools are known"], {}),
    "features": (["features", "count", "--by-tag"], ["features: ", "Rule: blocks are not supported"],
                 {"features/a.feature": "Feature: a\n  Rule: r\n"}),
    "measure": (["measure", "show", "nothing"], ["measure show: no measurement at nothing"], {}),
}


@pytest.mark.parametrize("tool", sorted(CASES))
def test_a_refused_command_exits_1_naming_the_reason_and_changes_nothing(tmp_path, tool):
    argv, said, files = CASES[tool]
    _git(tmp_path, "init", "-q")
    for rel, text in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
        _git(tmp_path, "add", rel)
    _git(tmp_path, "commit", "-q", "--allow-empty", "-m", "start")
    before = _state(tmp_path)
    done = subprocess.run([sys.executable, str(SCRIPTS / argv[0]), *argv[1:]], cwd=tmp_path,
                          capture_output=True, text=True)
    assert done.returncode == 1, done.stdout + done.stderr
    for text in said:
        assert text in done.stderr, done.stderr
    assert "Traceback" not in done.stderr
    assert _state(tmp_path) == before


def _script(name):
    loader = importlib.machinery.SourceFileLoader("refusal_" + name, str(SCRIPTS / name))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    return module


OTHERS = (tools_grammar.Refused, shop_files.Refused, transcripts.Refused)


@pytest.mark.parametrize("cls", OTHERS, ids=["tools_grammar", "shop_files", "transcripts"])
@pytest.mark.parametrize("tool", ["tools", "features", "measure"])
def test_a_refusal_of_another_modules_class_is_caught_by_each_tool(tool, cls, monkeypatch, capsys, tmp_path):
    def refuse(*_args, **_kwargs):
        raise cls("x")

    monkeypatch.chdir(tmp_path)
    module = _script(tool)
    if tool == "tools":
        monkeypatch.setattr(module.tools_size, "cmd_size", refuse)
        monkeypatch.setattr(sys, "argv", ["tools", "size"])
        code = module.main()
    elif tool == "features":
        monkeypatch.setattr(module, "cmd_count", refuse)
        monkeypatch.setattr(sys, "argv", ["features", "count", "--by-tag"])
        code = module.main()
    else:
        monkeypatch.setitem(module.COMMANDS, "show", refuse)
        code = module.main(["show", "nothing"])
    assert code == 1
    assert capsys.readouterr().err.endswith(": x\n")
