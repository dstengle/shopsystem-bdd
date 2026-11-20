"""`migrate init` with no git identity: refused before it writes, naming git config (b415), so a session asks the
person for their name and email rather than making one up."""
import os
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


def test_no_identity_is_refused_before_anything_is_written(tmp_path):
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "EMAIL"}
    env.update(HOME=str(tmp_path / ".git" / "home"), XDG_CONFIG_HOME=str(tmp_path / ".git" / "home"),
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="user.useConfigOnly",
               GIT_CONFIG_VALUE_0="true")
    done = subprocess.run([sys.executable, str(SCRIPTS / "migrate"), "init", "--id",
                           "bounded-context/example.org/checklists/checklists-cli"], cwd=tmp_path,
                          capture_output=True, text=True, env=env)
    assert done.returncode == 1, done.stdout
    assert 'git config user.name "…" and git config user.email "…"; nothing written' in done.stderr, done.stderr
    assert sorted(p.name for p in tmp_path.iterdir()) == [".git"]
