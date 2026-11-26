"""The old command names (b631, decision 0132): `work`, `spec`, `measure`, `migrate`, `tools` and `features` run by
their old names print one notice on stderr that `shop` replaces them, then run as before, their output and exit
unchanged; run by `shop`, none."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
COMMANDS = ("work", "spec", "measure", "migrate", "tools", "features")
ENV = "SHOPSYSTEM_BY_SHOP"     # adapter_cli_respond.BY_SHOP


def run(*args, env=None, cwd=None):
    plain = {k: v for k, v in os.environ.items() if k != ENV}
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, timeout=600, cwd=cwd,
                          env={**plain, **(env or {})})


def notice(name):
    return f"{name}: now `shop {name}`; `{name}` goes in the next release\n"


@pytest.mark.parametrize("command", COMMANDS)
def test_an_old_name_prints_the_notice_then_runs_as_before(command):
    old, shop = run(str(SCRIPTS / command), "--help"), run(str(SCRIPTS / "shop"), command, "--help")
    assert old.stderr == notice(command) + shop.stderr, old.stderr
    assert (old.stdout, old.returncode) == (shop.stdout, shop.returncode)
    assert old.returncode == 0 and old.stdout.startswith(f"usage: shop {command}")


@pytest.mark.parametrize("command", COMMANDS)
def test_shop_prints_no_notice(command):
    assert "goes in the next release" not in run(str(SCRIPTS / "shop"), command, "--help").stderr


def test_a_refusal_keeps_its_exit_and_its_own_stderr():
    old, shop = run(str(SCRIPTS / "spec"), "nosuch"), run(str(SCRIPTS / "shop"), "spec", "nosuch")
    assert old.returncode == shop.returncode != 0
    assert old.stderr == notice("spec") + shop.stderr


def test_the_mark_of_shop_is_taken_out_so_a_command_the_run_starts_prints_the_notice(monkeypatch, capsys):
    import adapter_cli_respond
    monkeypatch.setenv(ENV, "1")
    adapter_cli_respond.notice("tools")
    assert capsys.readouterr().err == "" and ENV not in os.environ
    adapter_cli_respond.notice("tools")
    assert capsys.readouterr().err == notice("tools")


def test_model_prints_its_own_notice_and_not_specs():
    done = run(str(SCRIPTS / "model"), "--help")
    assert done.returncode == 0 and done.stdout.startswith("usage: shop spec")
    assert done.stderr == "model: renamed `spec`; `model` goes in the next release\n", done.stderr


@pytest.mark.parametrize("words,count", [(("tools",), 1), (("shop", "tools"), 0)])
def test_tools_run_again_under_the_project_interpreter_prints_the_notice_once(tmp_path, words, count):
    (tmp_path / "a.py").write_text("def found():\n    pass\n\n\nfound()\n")
    (tmp_path / "py").mkdir()
    (tmp_path / "py" / "python").symlink_to(sys.executable)   # another path than sys.executable: `under` runs again
    done = run(str(SCRIPTS / words[0]), *words[1:], "refs", "found", "--python", "py/python", cwd=tmp_path)
    assert done.returncode == 0 and "a.py:5" in done.stdout, done.stderr
    assert done.stderr.count(notice("tools")) == count, done.stderr
