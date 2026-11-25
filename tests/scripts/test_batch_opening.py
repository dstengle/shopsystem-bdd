"""b588: opening a batch takes under a minute again. Deterministic proxies of its time, not wall time: the pick checks a
lone item by the readiness bar once (alone and laid over no item are the same check), and `work batch merged` starts
the warming of the base's state (batch_warm), so that the next `work batch start` finds grammar 4 compiled, its lines
parsed and the bar's before state kept."""
import time

import batch_pick
import batch_warm
import pytest
import readiness_bar
import readiness_before
import spec_gf
import spec_grammar4
import spec_parse_cache
import spec_prefetch
import spec_rgl
import toolchain
from backlog_testing import work
from batch_testing import ready_item
from test_batch_close import merge, reviewed  # noqa: F401  (the fixture)
from test_batch_pick import SECOND, THIRD, size
from test_batch_review import both_done  # noqa: F401  (the fixture)
from test_batch_tasks import started  # noqa: F401  (the fixture)


@pytest.fixture(autouse=True)
def warming(monkeypatch):
    """The warming switched on again, which the conftest switches off for every other test (b592)."""
    monkeypatch.delenv("SHOPSYSTEM_NO_WARM", raising=False)


def _counted(monkeypatch):
    calls, real = [], readiness_bar.check
    monkeypatch.setattr(readiness_bar, "check", lambda *a, **k: calls.append(a[1].name) or real(*a, **k))
    return calls


def test_pick_checks_a_lone_item_once(ready_repo, monkeypatch):
    toolchain.require()
    ready_item(ready_repo, "b1", "Item b1", SECOND, size="small")
    calls = _counted(monkeypatch)
    found = batch_pick.pick(ready_repo)
    assert [i.name for i in found.picked] == ["b1"], (found.returned, found.left_out)
    assert calls == ["b1"]


def test_pick_checks_a_later_item_alone_and_laid_over_the_picked(ready_repo, monkeypatch):
    toolchain.require()
    ready_item(ready_repo, "b1", "Item b1", SECOND, value="high-value", size="small")
    ready_item(ready_repo, "b2", "Item b2", THIRD, value="low-value", size="small")
    size(ready_repo, 2)
    calls = _counted(monkeypatch)
    found = batch_pick.pick(ready_repo)
    assert [i.name for i in found.picked] == ["b1", "b2"], (found.returned, found.left_out)
    assert calls == ["b1", "b2", "b2"]
    note = found.picked[1].sections["Notes"]
    assert "renumbered by work batch start: " in note, note


def _warm(root, cache, seconds=300):
    """Wait for the detached warming of `root` into `cache`: its last write is the before state."""
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if list((cache / "shopsystem-bdd" / "readiness").glob("*.json")):
            return
        time.sleep(0.5)
    pytest.fail("the warming kept no before state in %d s" % seconds)


def test_merged_warms_the_base_state(reviewed, batch_outside, monkeypatch, tmp_path):  # noqa: F811
    toolchain.require()
    cache = tmp_path / "cache"
    monkeypatch.setenv("XDG_CACHE_HOME", str(cache))
    merge(reviewed, batch_outside)
    done = work(reviewed, "batch", "merged", "batch-1")
    assert done.returncode == 0, done.stderr
    _warm(reviewed, cache)
    vocab, _, name = spec_grammar4._context(reviewed)        # the sources' sha, nothing compiled here
    assert (spec_gf.cache() / name / ("%s.pgf" % spec_grammar4.GRAMMAR)).is_file()
    texts = spec_prefetch.texts(reviewed)
    words = {w.replace(" ", spec_rgl.TOKEN) for w in vocab.words}
    unparsed = [line for line in texts if spec_parse_cache.get(name, spec_grammar4.GRAMMAR, spec_parse_cache.key(
        name, spec_grammar4.GRAMMAR, spec_gf.gf_text(spec_gf.tokenise(line)), words, spec_grammar4.LIMIT)) is None]
    assert texts and unparsed == []
    with batch_warm.copied(reviewed) as copy:
        assert readiness_before.get(copy, readiness_before.key(copy)) is not None


def test_a_warming_that_fails_ends_quietly(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    process = batch_warm.start(tmp_path / "nowhere")
    assert process is not None and process.wait(timeout=120) == 0
    assert not (tmp_path / "cache" / "shopsystem-bdd" / "readiness").exists()


def test_the_bar_reads_the_before_state_the_warming_kept(ready_repo, monkeypatch, tmp_path):
    toolchain.require()
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    ready_item(ready_repo, "b1", "Item b1", SECOND, size="small")
    batch_warm.warm(ready_repo)
    computed = []
    monkeypatch.setattr(readiness_before, "put", lambda *a: computed.append(a))
    found = batch_pick.pick(ready_repo)
    assert [i.name for i in found.picked] == ["b1"], (found.returned, found.left_out)
    assert computed == []
