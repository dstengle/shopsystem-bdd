"""spec_parse_cache: GF's parse of a line kept on disk, shared by processes, keyed by the grammar's sources, the
grammar, the lexicon's words and the text; a hit loads no grammar and runs no parse."""
import os
import pathlib
import subprocess
import sys

import pytest
import spec_grammar
import spec_parse_cache

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
TINY = """---
language: codified-1
---
## Glossary

- **`work`** (proper noun): the queue's command.
- **initiative** (noun): a delivery.
- **status** (attribute of initiative): Values: `proposed`, `started`.
"""
LINE = "`work` shall set the status of every initiative to `started`."
BAD = "`work` shall frobnicate the initiative."


@pytest.fixture
def ctx(tmp_path, monkeypatch):
    toolchain.require()
    (tmp_path / "ctx" / "spec").mkdir(parents=True)
    (tmp_path / "ctx" / "spec" / "index.md").write_text(TINY)
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setattr(spec_grammar, "_loaded", {})  # a PGF loaded from another cache is not this test's
    return tmp_path / "ctx"


def no_grammar(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("a cache hit loaded the grammar")
    monkeypatch.setattr(spec_grammar, "load", refuse)


def test_a_second_parse_of_a_line_is_read_from_the_cache(ctx, monkeypatch):
    first = spec_grammar.parse(ctx, LINE)
    refused = spec_grammar.parse(ctx, BAD)
    assert first.tree and refused.refusal
    no_grammar(monkeypatch)
    assert spec_grammar.parse(ctx, LINE) == first
    assert spec_grammar.parse(ctx, BAD) == refused


def test_a_parse_in_one_process_is_a_hit_in_another(ctx, tmp_path, monkeypatch):
    env = dict(os.environ, PYTHONPATH=str(REPO / "scripts"))
    code = "import spec_grammar, sys; print(spec_grammar.parse(sys.argv[1], sys.argv[2]).tree is not None)"
    done = subprocess.run([sys.executable, "-c", code, str(ctx), LINE], env=env, capture_output=True, text=True,
                          timeout=600)
    assert done.stdout.strip() == "True", done.stderr
    no_grammar(monkeypatch)
    assert spec_grammar.parse(ctx, LINE).tree


def test_a_lexicon_edit_misses(ctx, monkeypatch):
    assert spec_grammar.parse(ctx, LINE).tree
    index = ctx / "spec" / "index.md"
    index.write_text(index.read_text().replace("`proposed`, `started`", "`proposed`, `begun`"))
    assert spec_grammar.parse(ctx, LINE).tree is None
    assert spec_grammar.parse(ctx, LINE.replace("started", "begun")).tree


def test_the_key_names_everything_the_parse_reads():
    key = spec_parse_cache.key
    base = key("sha", "Req", "a b", {"x"})
    assert len({base, key("sha2", "Req", "a b", {"x"}), key("sha", "Steps", "a b", {"x"}),
                key("sha", "Req", "a c", {"x"}), key("sha", "Req", "a b", {"y"})}) == 5
    assert key("sha", "Req", "a b", {"x", "y"}) == key("sha", "Req", "a b", ["y", "x"])


def test_an_unwritable_cache_still_parses(ctx, tmp_path, monkeypatch):
    blocked = tmp_path / "blocked"
    blocked.write_text("a file where the cache directory would be")
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setattr(spec_parse_cache, "_base", lambda: blocked / "parse")
    assert spec_grammar.parse(ctx, LINE).tree
    assert spec_grammar.parse(ctx, LINE).tree


def test_a_second_parse_reads_the_lexicon_no_more(ctx, monkeypatch):
    """spec_grammar's context memo: the lexicon is read once per state of the files, not three times a line."""
    import spec_lexicon
    real, calls = spec_lexicon.read, []

    def counted(root):
        calls.append(root)
        return real(root)
    monkeypatch.setattr(spec_lexicon, "read", counted)
    assert spec_grammar.parse(ctx, LINE).tree
    assert spec_grammar.parse(ctx, BAD).refusal
    assert len(calls) == 1


def test_an_edit_of_equal_size_reads_the_lexicon_again(ctx):
    assert spec_grammar.parse(ctx, LINE).tree
    index = ctx / "spec" / "index.md"
    text = index.read_text()
    index.write_text(text.replace("`started`", "`stopped`"))
    assert index.stat().st_size == len(text.encode())
    assert spec_grammar.parse(ctx, LINE).tree is None
