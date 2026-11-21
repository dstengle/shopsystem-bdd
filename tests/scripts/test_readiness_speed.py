"""b430: the readiness bar answers in seconds, with the same reasons. Deterministic proxies of its time, not wall
time: the copy's grammar inputs statted once per state (spec_held), each line parsed at most once per state, no
`spec annotate` and no entailment (decision 0112), the before-lay result kept on disk (readiness_before), the
grammar's key free of the copy's path, and a lay's parse misses parsed by a pool (spec_prefetch)."""
import builtins
import os
import pathlib
import shutil
from collections import Counter

import backlog_items
import pytest
import readiness_bar
import readiness_before
import spec_grammar4
import spec_held
import spec_prefetch
from backlog_testing import git, work, write_item

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"
MODEL = "service notes\n  operation pin(note)  outcomes: done"
TERM = "- **pin** (verb, action) → operation notes.pin. Forms: pins, pinned. Frame: <actor> pins <note>."
LINE = "When the person pins a note, the notes service shall complete the request."
ADDS = "When the person adds a note, the notes service shall file the note."
BROKEN = "When the person frobnicates a note, the notes service shall complete the request."


@pytest.fixture
def modelled(backlog_repo, tmp_path_factory, monkeypatch):
    """The domain-model fixture's spec, committed, an item b1 with a model line, a term and a line, and the before-lay
    results kept in a folder of the test's own."""
    import toolchain
    toolchain.require()
    shutil.rmtree(backlog_repo / "spec")
    shutil.copytree(FIXTURE / "spec", backlog_repo / "spec")
    shutil.copytree(FIXTURE / "features", backlog_repo / "features")
    git(backlog_repo, "add", "-A")
    git(backlog_repo, "commit", "-q", "-m", "the domain-model fixture")
    write_item(backlog_repo, "b1", status="shaped")
    for args in (("--model", MODEL), ("--term", TERM), (LINE,)):
        done = work(backlog_repo, "line", "b1", "--into", "notebook", *args)
        assert done.returncode == 0, done.stderr
    before = tmp_path_factory.mktemp("before")
    monkeypatch.setattr(readiness_before, "_base", lambda: before)
    return backlog_repo


def item(repo):
    return backlog_items.find(repo, "b1")


def _stats(repo, monkeypatch):
    """{path under the copy: os.stat calls} of one run of the bar, which passes."""
    stats, real = Counter(), os.stat

    def stat(path, *args, **kwargs):
        text = os.fspath(path)
        if "readiness-" in text and "/spec" in text:
            stats[text.split("readiness-", 1)[1].split("/", 1)[1]] += 1
        return real(path, *args, **kwargs)
    with monkeypatch.context() as patched:
        patched.setattr(os, "stat", stat)
        assert readiness_bar.check(repo, item(repo)) == ([], [])
    return stats


def test_the_copys_spec_is_statted_once_a_state_whatever_its_number_of_lines(modelled, monkeypatch):
    few = _stats(modelled, monkeypatch)
    path = modelled / "spec" / "capabilities" / "notebook.md"
    more = "".join("\n### [g%d] A note of text t%d is kept\n- [r%d] When the person adds a note with the text "
                   "`t%d`, the notes service shall keep the note.\n" % (100 + k, k, 100 + k, k) for k in range(12))
    path.write_text(path.read_text().replace("\n## ", more + "\n## ", 1) if "\n## Not" in path.read_text()
                    else path.read_text() + more)
    git(modelled, "commit", "-qam", "twelve lines more")
    many = _stats(modelled, monkeypatch)
    assert max(few.values()) <= 40, few.most_common(5)        # 1.08 million on this repository before b430
    assert max(many.values()) <= max(few.values()), (few.most_common(3), many.most_common(3))


def test_each_line_is_parsed_at_most_once_per_state(modelled, monkeypatch):
    calls, real = Counter(), spec_grammar4._parse
    monkeypatch.setattr(spec_grammar4, "_parse", lambda root, line: calls.update([line]) or real(root, line))
    assert readiness_bar.check(modelled, item(modelled)) == ([], [])
    assert calls[LINE] == 1, calls
    assert max(calls.values()) <= 2, calls.most_common(3)       # the state before the lay and the state after


def test_the_bar_runs_no_annotate_and_no_entailment(modelled, monkeypatch):
    def boom(*_args, **_kwargs):
        raise AssertionError("called")
    import adapter_annotate
    import spec_entail
    import spec_solve
    for module, name in ((adapter_annotate, "annotate"), (adapter_annotate, "governing"),
                         (spec_entail, "findings"), (spec_solve, "l2")):
        monkeypatch.setattr(module, name, boom)
    assert readiness_bar.check(modelled, item(modelled)) == ([], [])


def test_the_before_lay_result_is_kept_on_disk_and_read_again(modelled, monkeypatch):
    first = readiness_bar.check(modelled, item(modelled))
    reads, real = [], readiness_bar._violations
    monkeypatch.setattr(readiness_bar, "_violations", lambda copy: reads.append(copy) or real(copy))
    assert readiness_bar.check(modelled, item(modelled)) == first
    assert len(reads) == 1                                    # the state after the lay only
    path = modelled / "spec" / "capabilities" / "notebook.md"
    path.write_text(path.read_text() + "\n")                  # another spec: another key
    assert readiness_bar.check(modelled, item(modelled)) == first
    assert len(reads) == 3


def test_the_reasons_are_the_same_on_a_cold_and_a_warm_run(modelled):
    assert work(modelled, "line", "b1", "--into", "notebook", BROKEN).returncode == 0
    cold = readiness_bar.check(modelled, item(modelled))
    assert any("frobnicates" in r or "notebook#r" in r for r in cold[0]), cold
    assert readiness_bar.check(modelled, item(modelled)) == cold


def test_the_key_of_the_before_lay_result_reads_the_spec_and_the_tools(modelled, tmp_path):
    copy = tmp_path / "copy"
    shutil.copytree(modelled / "spec", copy / "spec")
    key = readiness_before.key(copy)
    assert key == readiness_before.key(copy)
    (copy / "spec" / "index.md").write_text((copy / "spec" / "index.md").read_text() + "\n")
    assert readiness_before.key(copy) != key


def test_the_grammars_key_is_free_of_the_copys_path(modelled, tmp_path):
    copy = tmp_path / "elsewhere"
    shutil.copytree(modelled / "spec", copy / "spec")
    assert spec_grammar4.sha(spec_grammar4.sources(modelled)[1]) == spec_grammar4.sha(spec_grammar4.sources(copy)[1])


def test_the_inputs_are_every_spec_file_the_vocabulary_reads(modelled, monkeypatch):
    import io

    import spec_rgl_vocab
    opened, real = set(), io.open

    def spy(file, *args, **kwargs):
        opened.add(os.path.realpath(os.fspath(file)))
        return real(file, *args, **kwargs)
    pathlib.Path(modelled / "spec" / "decisions").mkdir()
    (modelled / "spec" / "decisions" / "0001-x.md").write_text("# x\n")
    monkeypatch.setattr(builtins, "open", spy)
    monkeypatch.setattr(io, "open", spy)
    spec_rgl_vocab.read(modelled)
    spec = os.path.realpath(modelled / "spec")
    read = {p for p in opened if p.startswith(spec + os.sep)}
    inputs = {os.path.realpath(p) for p in spec_held.inputs(modelled)}
    assert read and read <= inputs, read - inputs
    assert not any("/decisions/" in p for p in inputs)


def test_a_held_state_is_statted_once_until_it_is_invalidated(modelled, monkeypatch):
    calls, real = [], spec_held._stat
    monkeypatch.setattr(spec_held, "_stat", lambda root: calls.append(root) or real(root))
    with spec_held.held(modelled):
        first = spec_held.state(modelled)
        assert spec_held.state(modelled) == first and len(calls) == 1
        index = modelled / "spec" / "index.md"
        index.write_text(index.read_text() + "\n")
        spec_held.invalidate(modelled)
        assert spec_held.state(modelled) != first and len(calls) == 2
    spec_held.state(modelled)
    spec_held.state(modelled)
    assert len(calls) == 4                                    # outside a held scope, every call stats


def test_the_pool_is_at_most_eight_and_a_quarter_of_the_cpus():
    assert [spec_prefetch.workers(n) for n in (1, 4, 8, 16, 32, 64)] == [1, 1, 2, 4, 8, 8]


def test_the_misses_of_a_lay_are_parsed_by_the_pool_into_the_cache(modelled, monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    texts = [ADDS, BROKEN]
    assert spec_prefetch.misses(modelled, texts) == texts
    spec_prefetch.prefetch(modelled, texts, processes=2)
    assert spec_prefetch.misses(modelled, texts) == []
    gf, real = [], spec_grammar4._gf_trees
    monkeypatch.setattr(spec_grammar4, "_gf_trees", lambda *a: gf.append(a) or real(*a))
    assert spec_grammar4.parse(modelled, ADDS).tree
    assert gf == []
