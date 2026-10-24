"""Probe: a work-item of another initiative, read today by `work show` (file status only) and by `work run i2` (which
checks it with agrees, log.jsonl included). Repositories are built by probe_blocked.build under this scratch directory."""
import json
import os
import subprocess
import sys

from probe_blocked import BASE, build
from tests.scenarios.conftest import SCRIPTS
from tests.scenarios.supervision_world import commit_all, write

LOG_TO_DONE = json.dumps({"time": "2026-10-19T10:00:00+00:00", "work-item": "w2", "before": "researched",
                          "after": "done", "by": "someone"}) + "\n"


def work(repo, *args):
    done = subprocess.run([sys.executable, str(SCRIPTS / "work"), *args], cwd=repo, capture_output=True, text=True,
                          timeout=300, env=dict(os.environ, SHOPSYSTEM_WORK_RUN_WORKER=""))
    return done


def test_other_initiative_file_says_green_log_says_done():
    repo, _ = build("file_green_log_done", [("i1", "w1", "drafted", ["w2"]), ("i2", "w2", "green", None)])
    write(repo, ".shop/work/i2/log.jsonl", LOG_TO_DONE)
    commit_all(repo, "w2's log says done")
    show = work(repo, "show")
    print("\nwork show: rc %d, %s" % (show.returncode, show.stdout.strip().replace("\n", " | ")))
    run_i2 = work(repo, "run", "i2")
    print("work run i2: rc %d, stdout %r, stderr %r" % (run_i2.returncode, run_i2.stdout.strip(),
                                                        run_i2.stderr.strip().splitlines()[-1:]))
    run_i1 = work(repo, "run", "i1")
    print("work run i1 (w2 in i2 not read today): rc %d, stdout %r" % (run_i1.returncode, run_i1.stdout.strip()))


def test_other_initiative_item_without_status():
    repo, _ = build("other_no_status", [("i1", "w1", "drafted", ["w2"]), ("i2", "w2", "green", None)])
    text = (repo / ".shop/work/i2/w2.md").read_text().replace("status: green\n", "")
    write(repo, ".shop/work/i2/w2.md", text)
    commit_all(repo, "w2 without a status")
    show = work(repo, "show")
    print("\nwork show: rc %d, %s" % (show.returncode, show.stdout.strip().replace("\n", " | ")))
    print("work show stderr: %r" % show.stderr.strip().splitlines()[-1:])
    run_i1 = work(repo, "run", "i1")
    print("work run i1 today: rc %d, stdout %r" % (run_i1.returncode, run_i1.stdout.strip()))
