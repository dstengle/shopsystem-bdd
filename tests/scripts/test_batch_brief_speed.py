"""`work batch brief`'s checks run side by side (b457): the runs at the head, and the runs at `forked_from` a batch
has not run yet, each started at once, their sections kept in the order of `[review] checks`."""
import threading
import time
from types import SimpleNamespace

import batch_brief

PAUSE = 0.4


class Recorder:
    """A stand-in `_run` that takes PAUSE seconds and counts how many runs overlap."""

    def __init__(self):
        self.lock, self.now, self.most = threading.Lock(), 0, 0

    def __call__(self, command, where):
        with self.lock:
            self.now += 1
            self.most = max(self.most, self.now)
        time.sleep(PAUSE)
        with self.lock:
            self.now -= 1
        return SimpleNamespace(returncode=int(command[-1]), stdout="out of %s\n" % command, stderr="")


COMMANDS = ["check 0", "check 1", "check 2", "check 3", "check 4"]


def test_the_runs_at_the_head_overlap_and_keep_their_order(monkeypatch):
    fake = Recorder()
    monkeypatch.setattr(batch_brief, "_run", fake)
    monkeypatch.setattr(batch_brief, "delivery", lambda root: {"review": {"checks": COMMANDS}})
    monkeypatch.setattr(batch_brief, "base_runs", lambda root, batch, commands: {c: 0 for c in commands})
    start = time.monotonic()
    text = batch_brief._runs("root", "tree", SimpleNamespace(forked_from="abc"))
    took = time.monotonic() - start
    assert fake.most == len(COMMANDS), fake.most
    assert took < PAUSE * 2, took
    assert [text.index("### `%s`" % c) for c in COMMANDS] == sorted(text.index("### `%s`" % c) for c in COMMANDS)
    assert "### `check 3`\n\nExit code: 3 (base: 0)\n\n    out of check 3" in text


def test_the_runs_at_forked_from_overlap(monkeypatch, tmp_path):
    fake = Recorder()
    monkeypatch.setattr(batch_brief, "_run", fake)
    monkeypatch.setattr(batch_brief.batch_findings, "scratch", lambda root, name, k: tmp_path / "scratch")
    monkeypatch.setattr(batch_brief, "trees_dir", lambda root: tmp_path)
    monkeypatch.setattr(batch_brief, "remove_tree", lambda root, tree: None)
    monkeypatch.setattr(batch_brief, "git", lambda *args: None)
    start = time.monotonic()
    found = batch_brief.base_runs("root", SimpleNamespace(name="batch-1", forked_from="abc"), COMMANDS)
    took = time.monotonic() - start
    assert found == {c: int(c[-1]) for c in COMMANDS}
    assert fake.most == len(COMMANDS) and took < PAUSE * 2, (fake.most, took)
