"""The old grammar's literal slots (b240 phase 13): a backticked token is a code and a double-quoted one a quoted
text, so a tree that reads one as the other is never among the trees a parse keeps, and a line of many codes is
not refused when GF enumerates the misread trees first (migration-tools r1, eleven codes: 2^11 trees past LIMIT)."""
import pathlib
import sys

import spec_grammar
import spec_parse_cache

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]


def test_a_code_is_never_read_as_a_quoted_text(tmp_path, monkeypatch):
    toolchain.require()
    monkeypatch.setattr(spec_parse_cache, "_base", lambda: tmp_path / "parse")
    monkeypatch.setattr(spec_grammar, "LIMIT", 1)
    parsed = spec_grammar.parse(REPO, "When the person runs `migrate run`, `migrate` shall relocate `a/`.")
    assert parsed.refusal is None and parsed.tree is not None, parsed.refusal
    assert "QuotedLit" not in str(parsed.tree)
