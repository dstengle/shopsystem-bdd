"""supervise_rounds.undo_round (r135): an integrate round whose raise into an upstream is refused is taken back, and the
initiative's next commit still runs. Its stage directory was the only thing under runs/<name>, so the emptied
runs/<name> is removed too, and a commit naming it does not fail with "pathspec ... did not match any files"."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import supervise


def sh(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


def test_a_refused_raise_taken_back_leaves_the_next_commit_able_to_run(tmp_path):
    root = tmp_path
    sh(root, "init", "-q", "-b", "main")
    sh(root, "config", "user.email", "t@t")
    sh(root, "config", "user.name", "t")
    run = supervise.Run(root, "i1")
    run.dir.mkdir(parents=True)
    (run.dir / "initiative.md").write_text("---\nstatus: started\n---\n")
    (run.dir / "log.jsonl").write_text("")
    sh(root, "add", "-A")
    sh(root, "commit", "-q", "-m", "start")
    sh(root, "branch", "round/i1-r1")
    here = run.dir / "runs" / "i1" / "r1"
    here.mkdir(parents=True)
    (here / "result.json").write_text("{}")
    run.own.add(run.rel(here))
    line = json.dumps({"work-item": "i1", "stage": "integrate"}) + "\n"
    run.unlogged = [line]
    (run.dir / "log.jsonl").write_text(line)
    run.undo_round("i1", "integrate", here, "round/i1-r1")
    assert not (run.dir / "runs" / "i1").exists()
    (run.dir / "initiative.md").write_text("---\nstatus: started\n---\nfault\n")
    run.commit("i1", "started", "started", push=False)
    assert "work: i1 started -> started" in sh(root, "log", "-1", "--format=%s").stdout
