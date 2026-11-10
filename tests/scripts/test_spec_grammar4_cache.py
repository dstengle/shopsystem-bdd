"""Grammar 4's caches (b239): its sources and loaded grammar computed once per process for one lexicon and its packs,
computed again when either changes; its parses kept in spec_parse_cache; its compiled PGF reused by every process
while its sources are unchanged."""
import os
import pathlib
import shutil
import subprocess
import sys

import pytest
import spec_grammar4
import spec_parse_cache
import spec_rgl_vocab

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
LINE = "When the person writes a file, `work` shall end every stage."
BAD = "When the person frobnicates a file, `work` shall end every stage."


@pytest.fixture
def ctx(tmp_path, monkeypatch):
    toolchain.require()
    shutil.copytree(FIXTURE, tmp_path / "ctx")
    monkeypatch.setattr(spec_parse_cache, "_base", lambda: tmp_path / "parse")
    return tmp_path / "ctx"


@pytest.fixture
def reads(monkeypatch):
    """The calls of spec_rgl_vocab.read, which every computation of the sources makes once."""
    calls, real = [], spec_rgl_vocab.read
    monkeypatch.setattr(spec_rgl_vocab, "read", lambda root: calls.append(root) or real(root))
    return calls


def test_the_sources_and_the_grammar_of_one_lexicon_are_computed_once_a_process(ctx, reads):
    first = spec_grammar4.sources(ctx)
    assert spec_grammar4.sources(ctx) == first
    assert spec_grammar4.load(ctx)[0] is spec_grammar4.load(ctx)[0]
    spec_grammar4.parse(ctx, LINE)
    assert len(reads) == 1


def test_a_caller_that_changes_the_sources_it_was_given_changes_no_later_call(ctx):
    _, srcs = spec_grammar4.sources(ctx)
    srcs["Extra.gf"] = "-- a caller's own"
    assert "Extra.gf" not in spec_grammar4.sources(ctx)[1]


def test_a_changed_term_of_the_lexicon_computes_the_sources_again(ctx, reads):
    spec_grammar4.sources(ctx)
    index = ctx / "spec" / "index.md"
    index.write_text(index.read_text() + "- **ledger** (noun): a record of the work kept in a file.\n")
    _, srcs = spec_grammar4.sources(ctx)
    assert len(reads) == 2 and "ledger" in srcs["ContextEng.gf"]


def test_a_changed_pack_computes_the_sources_again(ctx, reads):
    spec_grammar4.sources(ctx)
    packs = ctx / "spec" / "packs"
    packs.mkdir()
    cli = (REPO / "grammar" / "packs" / "cli.md").read_text()
    ledger = "## Glossary\n\n- **ledger** (noun): a record of the work kept in a file.\n"
    (packs / "cli.md").write_text(cli.replace("## Glossary\n", ledger, 1))
    _, srcs = spec_grammar4.sources(ctx)
    assert len(reads) == 2 and "ledger" in srcs["ContextEng.gf"]


def no_gf(monkeypatch):
    def refuse(*_):
        raise AssertionError("a cached parse ran GF")
    monkeypatch.setattr(spec_grammar4, "_gf_trees", refuse)


def test_a_line_parsed_twice_is_read_the_second_time_from_the_parse_cache(ctx, tmp_path, monkeypatch):
    first, refused = spec_grammar4.parse(ctx, LINE), spec_grammar4.parse(ctx, BAD)
    assert first.tree and refused.refusal
    assert list((tmp_path / "parse").glob("*/Context/*.json"))
    no_gf(monkeypatch)
    assert spec_grammar4.parse(ctx, LINE) == first
    assert spec_grammar4.parse(ctx, BAD) == refused


def test_a_changed_lexicon_misses_the_parse_cache(ctx, monkeypatch):
    spec_grammar4.parse(ctx, LINE)
    index = ctx / "spec" / "index.md"
    index.write_text(index.read_text() + "- **ledger** (noun): a record of the work kept in a file.\n")
    calls, real = [], spec_grammar4._gf_trees
    monkeypatch.setattr(spec_grammar4, "_gf_trees", lambda *a: calls.append(a) or real(*a))
    assert spec_grammar4.parse(ctx, LINE).tree and calls


def run(code, root, seed):
    env = dict(os.environ, PYTHONPATH=str(REPO / "scripts"), PYTHONHASHSEED=str(seed))
    done = subprocess.run([sys.executable, "-c", code, str(root)], env=env, capture_output=True, text=True,
                          timeout=600)
    assert done.returncode == 0, done.stderr
    return done.stdout.strip()


def test_the_sources_are_the_same_in_every_process():
    code = "import spec_grammar4, sys; print(spec_grammar4.sha(spec_grammar4.sources(sys.argv[1])[1]))"
    assert len({run(code, REPO, seed) for seed in (1, 2, 3)}) == 1


def test_a_second_process_reuses_the_compiled_grammar_of_unchanged_sources(ctx):
    toolchain.require()
    code = ("import spec_grammar, spec_grammar4, sys; spec_grammar4.load(sys.argv[1]); "
            "print(spec_grammar._cache() / spec_grammar4.sha(spec_grammar4.sources(sys.argv[1])[1]) / 'Context.pgf')")
    target = pathlib.Path(run(code, ctx, 1))
    before = target.stat().st_mtime_ns
    assert pathlib.Path(run(code, ctx, 2)) == target
    assert target.stat().st_mtime_ns == before
