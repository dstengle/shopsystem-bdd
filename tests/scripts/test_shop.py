"""`shop`, the plugin's one command (decision 0132): `shop <command> <args>` runs the plugin's command of that name with
the same arguments, its output and exit unchanged, and `shop --help` lists the commands."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
COMMANDS = ("work", "spec", "measure", "migrate", "tools", "features")


def run(*args, cwd=None):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, timeout=600, cwd=cwd)


@pytest.mark.parametrize("command", COMMANDS)
def test_shop_answers_a_command_as_the_command_does(command):
    shop, direct = run(str(SCRIPTS / "shop"), command, "--help"), run(str(SCRIPTS / command), "--help")
    assert (shop.stdout, shop.stderr, shop.returncode) == (direct.stdout, direct.stderr, direct.returncode)
    assert shop.returncode == 0 and shop.stdout.startswith(f"usage: shop {command}"), shop.stdout


def test_shop_keeps_a_refusal_and_its_exit():
    shop, direct = run(str(SCRIPTS / "shop"), "spec", "nosuch"), run(str(SCRIPTS / "spec"), "nosuch")
    assert direct.returncode != 0
    assert (shop.stdout, shop.stderr, shop.returncode) == (direct.stdout, direct.stderr, direct.returncode)


def test_shop_runs_from_another_directory(tmp_path):
    done = run(str(SCRIPTS / "shop"), "tools", "--help", cwd=tmp_path)
    assert done.returncode == 0 and done.stdout.startswith("usage: shop tools"), done.stderr


def test_shop_help_lists_every_command():
    done = run(str(SCRIPTS / "shop"), "--help")
    assert done.returncode == 0 and done.stdout.startswith("usage: shop"), done.stdout
    for command in COMMANDS:
        assert command in done.stdout
    assert "model" not in done.stdout


def test_shop_refuses_a_command_it_does_not_run():
    for args in ([], ["model"], ["nosuch"]):
        done = run(str(SCRIPTS / "shop"), *args)
        assert done.returncode == 2 and "usage: shop" in done.stderr, (args, done.stderr)
