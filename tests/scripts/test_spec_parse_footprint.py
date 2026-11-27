"""A line's parse kept by its footprint (b877, spec_footprint): a term the line does not use keeps its parse with no
compile of grammar 4 and no new entry; a term it uses parses it again; and over a history of changes to a context's
lexicon and model every parse read by its footprint is the parse a fresh grammar gives (the same trees, the same
refusals)."""
import pathlib
import shutil
import sys

import pytest
import spec_gf
import spec_grammar4
import spec_parse_cache

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURES = REPO / "tests" / "scripts" / "fixtures"
LINE = "When the person writes a file, `work` shall end every stage."
UNUSED = "- **ledger** (noun): a record of the work kept in a file.\n"


@pytest.fixture
def cache(tmp_path, monkeypatch):
    toolchain.require()
    monkeypatch.setattr(spec_parse_cache, "_base", lambda: tmp_path / "parse")
    return tmp_path / "parse"


def kept(cache):
    return sorted(cache.with_name("parse-footprint").glob("*/*.json"))


def no_grammar(monkeypatch):
    def refuse(*_):
        raise AssertionError("grammar 4 compiled or GF run for a kept parse")
    monkeypatch.setattr(spec_gf, "compile", refuse)
    monkeypatch.setattr(spec_grammar4, "_gf_trees", refuse)


def test_a_term_the_line_does_not_use_keeps_its_parse(tmp_path, cache, monkeypatch):
    ctx = tmp_path / "ctx"
    shutil.copytree(FIXTURES / "codified-2", ctx)
    first = spec_grammar4.parse(ctx, LINE)
    assert first.tree
    entries = kept(cache)
    index = ctx / "spec" / "index.md"
    index.write_text(index.read_text() + UNUSED)
    no_grammar(monkeypatch)
    assert spec_grammar4.parse(ctx, LINE) == first
    assert kept(cache) == entries


def test_a_term_the_line_uses_parses_it_again(tmp_path, cache, monkeypatch):
    ctx = tmp_path / "ctx"
    shutil.copytree(FIXTURES / "codified-2", ctx)
    spec_grammar4.parse(ctx, LINE)
    index = ctx / "spec" / "index.md"
    index.write_text(index.read_text().replace("Frame: agent writes file.", "Frame: agent writes file. "
                                               "Frame: agent writes stage."))
    calls, real = [], spec_grammar4._gf_trees
    monkeypatch.setattr(spec_grammar4, "_gf_trees", lambda *a: calls.append(a) or real(*a))
    assert spec_grammar4.parse(ctx, LINE).tree and calls


def corpus():
    lines = []
    for name in ("core-4.txt", "refused.txt"):
        for line in (REPO / "grammar" / "corpus" / name).read_text().splitlines():
            if line.strip() and not line.startswith(("#", "=")):
                lines.append(line)
    return list(dict.fromkeys(lines))


def model(text, after, added):
    return text.replace(after, after + added, 1)


# the history replayed over request-4: each step a change of its model and vocabulary, kept after the ones before
WORK, TERMS = ("spec", "model", "work.md"), ("spec", "vocabulary", "work.md")
LEDGER = "- **ledger** (noun) → object ledger. A record of the work.\n"
WEIGHT = ("- **weight** (attribute) → attribute line.weight.\n- **light** (adjective) → value line.weight light.\n"
          "- **heavy** (adjective) → value line.weight heavy.\n")
BOARD = "- **the board** (proper noun) → actor the board. A screen of the work.\n"
BLOCKED = "- **blocked** (adjective) → value stage.status blocked.\n"
DRAFT = "- **draft** (noun) → object draft. A file not yet kept.\n"
SHELF = "- **shelf** (noun) → object shelf. Where files wait.\n"
INDEX = "- **`spec/index.md`** (proper noun) → object index. The context's index.\n"
HISTORY = [
    ("an unused noun", [(WORK, "object push\n", "\nobject ledger\n"), (TERMS, "## Terms\n\n", LEDGER)]),
    ("an attribute of a used kind", [(WORK, "  attributes: verdict: proposed | accepted | refused | withdrawn\n",
                                      "  attributes: weight: light | heavy\n"), (TERMS, "## Terms\n\n", WEIGHT)]),
    ("a relation row", [(WORK, "object push\n", "  relations: has → ledger (one)\n")]),
    ("a frame of a used verb", [(TERMS, "Frame: <actor> writes <file>.", " Frame: <actor> writes <line>.")]),
    ("an actor that opens a used phrase", [(WORK, "actor the person kind of agent\n",
                                            "actor the board kind of agent\n"), (TERMS, "## Terms\n\n", BOARD)]),
    ("a value of a used attribute", [(WORK, "status: open | done", " | blocked"), (TERMS, "## Terms\n\n", BLOCKED)]),
    ("a kind under a used kind", [(WORK, "object push\n", "\nobject draft kind of file\n"),
                                  (TERMS, "## Terms\n\n", DRAFT)]),
    ("a row that holds a used kind", [(WORK, "  relations: has → ledger (one)\n",
                                       "\nobject shelf\n  relations: holds → file (many)\n"),
                                      (TERMS, "## Terms\n\n", SHELF)]),
    ("a noun spelled as a code a line holds", [(WORK, "object push\n", "\nobject index\n"),
                                               (TERMS, "## Terms\n\n", INDEX)]),
]


def fresh(root, lines, cache, monkeypatch, tmp_path, k):
    """Each line's Parse in a cache of its own, empty."""
    monkeypatch.setattr(spec_parse_cache, "_base", lambda: tmp_path / ("fresh-%d" % k))
    try:
        return [spec_grammar4.parse(root, line) for line in lines]
    finally:
        monkeypatch.setattr(spec_parse_cache, "_base", lambda: cache)


def test_every_parse_read_by_its_footprint_over_a_history_is_a_fresh_parse(tmp_path, cache, monkeypatch):
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURES / "request-4", root)
    lines = corpus()
    for line in lines:
        spec_grammar4.parse(root, line)
    hits = misses = 0
    for k, (_, edits) in enumerate(HISTORY):
        for path, after, added in edits:
            target = root.joinpath(*path)
            assert after in target.read_text()
            target.write_text(model(target.read_text(), after, added))
        vocab, srcs, name = spec_grammar4._context(root)
        words = spec_grammar4._words_of(vocab)
        gram = spec_grammar4.load(root)[1]
        for line in lines:
            tokens = spec_gf.tokenise(line)
            hit = spec_parse_cache.lookup(name, srcs, spec_grammar4.GRAMMAR, spec_gf.gf_text(tokens), words,
                                          spec_grammar4.LIMIT)[1]
            if hit is None:
                misses += 1
                continue
            hits += 1
            assert hit == spec_grammar4._gf_trees(gram, words, tokens)[:2], (HISTORY[k][0], line)
        warm = [spec_grammar4.parse(root, line) for line in lines]
        assert warm == fresh(root, lines, cache, monkeypatch, tmp_path, k), HISTORY[k][0]
    assert hits > misses > 0
