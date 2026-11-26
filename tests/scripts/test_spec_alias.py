"""`model`, renamed `spec` by the domain contract (its design §10 step 6), kept one release as an alias: it says so on
stderr and answers as `spec` does, the same output and exit."""
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "domain-model"


def run(program, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / program), "--root", str(FIXTURE), *args],
                          capture_output=True, text=True, timeout=600)


def test_model_check_says_it_is_spec_now_and_answers_as_spec_check():
    alias, spec = run("model", "check"), run("spec", "check")
    assert "renamed `spec`" in alias.stderr
    assert (alias.stdout, alias.returncode) == (spec.stdout, spec.returncode)
    assert "renamed" not in spec.stderr


def test_spec_is_the_program_name():
    done = run("spec", "--help")
    assert done.returncode == 0 and done.stdout.startswith("usage: shop spec"), done.stdout
