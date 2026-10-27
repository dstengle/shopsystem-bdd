"""The agent-time analysis of 2026-10-27: a task reviewer's brief gives the commits the work-item's last merge brought and
work run's whole-suite record on them, read from the initiative's log."""
import json
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import supervise


class Stand:
    def __init__(self, root):
        self.root, self.dir = root, root / ".shop/work/i1"


def test_the_last_merge_of_the_work_item_gives_the_reviewers_lines(tmp_path):
    stand = Stand(tmp_path)
    stand.dir.mkdir(parents=True)
    lines = [{"work-item": "w1", "event": "merged", "commits": ["a1"], "record": "Suite: 1 passed, 0 failed at a1 in 1 s"},
             {"work-item": "w2", "event": "merged", "commits": ["b1"], "record": "Suite: 2 passed"},
             {"work-item": "w1", "event": "merged", "commits": ["c1", "c2"], "record": "Suite: 3 passed, 0 failed at c2 in 2 s"}]
    (stand.dir / "log.jsonl").write_text("".join(json.dumps(line) + "\n" for line in lines))
    assert supervise.Run.merged(stand, "w1") == (("Commits", "c1 c2"), ("Suite record", "Suite: 3 passed, 0 failed at c2 in 2 s"))


def test_a_work_item_never_merged_gives_no_lines(tmp_path):
    stand = Stand(tmp_path)
    stand.dir.mkdir(parents=True)
    assert supervise.Run.merged(stand, "w1") == ()
