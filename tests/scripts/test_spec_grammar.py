"""spec_grammar: tokenising (design §9.4), parsing with the guards (§9.3), linearising, the corpus, and the
compile cache with its atomic rename (§11.3)."""
import os
import pathlib
import subprocess
import sys

import pytest
import spec_grammar
import spec_tree

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "glossary"
CORPUS = REPO / "grammar" / "corpus"
CAPABILITIES = sorted(p.stem for p in (REPO / "spec" / "capabilities").glob("*.md"))
TINY = """---
language: codified-1
---
## Glossary

- **`work`** (actor): the queue's command.
- **initiative** (kind): a delivery.
- **status** (attribute of initiative): Values: `proposed`, `started`.
"""


@pytest.fixture(scope="module")
def root():
    toolchain.require()
    return FIXTURE


def lines(path):
    return [x.strip() for x in path.read_text().splitlines() if x.strip() and not x.startswith("#")]


def corpus():
    out = []
    for name in CAPABILITIES + ["universal"]:
        out += [(name, line.split("] ", 1)[1] if line.startswith("[U") else line) for line in lines(
            CORPUS / ("%s.txt" % name))]
    return out


def test_tokenise_keeps_backticked_and_quoted_spans_and_splits_punctuation():
    assert spec_grammar.tokenise('When the person runs `work start`, `work` shall print "no such initiative".') == [
        "when", "the", "person", "runs", "`work start`", ",", "`work`", "shall", "print",
        '"no such initiative"', "."]
    assert spec_grammar.tokenise("`work run` shall hold at most 4 worker slots.")[5] == "4"
    assert spec_grammar.normalise("When  the person runs `x` ,`work` shall exit successfully .") == (
        "When the person runs `x`, `work` shall exit successfully.")


def test_require_fails_naming_tools_install_when_a_tool_is_missing(monkeypatch):
    monkeypatch.setattr(spec_grammar, "gf_binary", lambda: None)
    with pytest.raises(pytest.fail.Exception) as failed:
        toolchain.require()
    assert "gf" in str(failed.value) and "python3 scripts/tools install" in str(failed.value)


def test_a_sentence_may_start_with_a_one_letter_word():
    assert spec_grammar.tokenise("A worker shall exit successfully.")[0] == "a"


def test_gf_binary_prefers_the_environment(monkeypatch, tmp_path):
    gf = tmp_path / "gf"
    gf.write_text("#!/bin/sh\n")
    monkeypatch.setenv("SHOPSYSTEM_GF", str(gf))
    assert spec_grammar.gf_binary() == str(gf)


def test_every_capability_has_a_corpus_of_at_least_eight_sentences():
    for name in CAPABILITIES:
        assert len(lines(CORPUS / ("%s.txt" % name))) >= 8, name
    assert [x.split("]")[0] for x in lines(CORPUS / "universal.txt")] == ["[U%d" % n for n in range(1, 11)]


def test_every_corpus_sentence_has_one_tree_and_linearises_back(root):
    failures = []
    for name, line in corpus():
        p = spec_grammar.parse(root, line)
        if p.tree is None:
            failures.append("%s: %s\n    %s" % (name, line, p.refusal))
        elif spec_grammar.linearise(root, p.tree) != spec_grammar.normalise(line):
            failures.append("%s: %s\n    linearises as %s" % (name, line, spec_grammar.linearise(root, p.tree)))
    assert not failures, "\n".join(failures)


def test_the_corpus_has_all_six_forms_lexicon_words_and_code_literals(root):
    funs = set()
    for _, line in corpus():
        funs |= {node[0] for node in spec_tree.nodes(spec_grammar.parse(root, line).tree)}
    assert {"Ubiq", "When", "While", "Where", "IfThen"} <= funs
    assert funs & {"WhileWhen", "WhereWhen", "WhereWhile", "WhileIf", "WhereIf"}
    assert "CodeLit" in funs and "QuotedLit" in funs and "CmdActor" in funs
    assert any(f.startswith("v_") for f in funs) and any(f.endswith("_It") for f in funs)


def test_every_refused_sentence_is_refused(root):
    accepted = [x for x in lines(CORPUS / "refused.txt") if spec_grammar.parse(root, x).trees]
    assert not accepted, accepted


def test_a_value_in_another_kinds_slot_is_refused_with_its_token(root):
    p = spec_grammar.parse(root, "When the person runs `work start` on an initiative that is `drafted`, "
                                 "`work` shall exit successfully.")
    assert p.tree is None and "`drafted`" in p.refusal and "token 11" in p.refusal


def test_a_guard_refusal_names_its_reason(root):
    p = spec_grammar.parse(root, "`work run` shall start it.")
    assert p.tree is None and p.trees == [] and '"it"' in p.refusal


def test_a_backticked_lexicon_word_parses_only_as_the_word(root):
    p = spec_grammar.parse(root, "When the person runs `work run`, `work run` shall exit successfully.")
    assert p.tree is not None and p.before > 1
    assert "CodeLit" not in {n[0] for n in spec_tree.nodes(p.tree)}


def test_hint_gives_the_parsed_prefix_and_the_nearest_words(root):
    h = spec_grammar.hint(root, "When the person runs `work start` on an initiatve, `work` shall exit successfully.")
    assert h["prefix"] == "When the person runs `work start` on an" and h["token"] == "initiatve"
    assert "initiative" in h["near"]


def test_linearise_writes_a_tree_back_as_a_sentence(root):
    tree = ("Ubiq", ("Shall", ("ActorSubj", ("a_work_run",)), ("Hold", ("s_spec_lock",))))
    assert spec_grammar.linearise(root, tree) == "`work run` shall hold the spec lock."


def _tiny(tmp_path):
    (tmp_path / "ctx" / "spec").mkdir(parents=True)
    (tmp_path / "ctx" / "spec" / "index.md").write_text(TINY)
    return tmp_path / "ctx"


def test_a_second_load_of_one_glossary_runs_no_gf(monkeypatch, tmp_path):
    toolchain.require()
    ctx = _tiny(tmp_path)
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    assert "ReqEng" in spec_grammar.load(ctx).languages
    spec_grammar._loaded.clear()

    def no_gf(*args, **kwargs):
        raise AssertionError("gf ran on a cache hit")
    monkeypatch.setattr(spec_grammar, "_run_gf", no_gf)
    assert "ReqEng" in spec_grammar.load(ctx).languages
    assert spec_grammar.parse(ctx, "`work` shall set the status of every initiative to `started`.").tree


def test_two_processes_loading_one_new_glossary_both_get_a_pgf(tmp_path):
    toolchain.require()
    ctx = _tiny(tmp_path)
    env = dict(os.environ, XDG_CACHE_HOME=str(tmp_path / "cache"), PYTHONPATH=str(REPO / "scripts"))
    code = "import spec_grammar, sys; print(sorted(spec_grammar.load(sys.argv[1]).languages))"
    procs = [subprocess.Popen([sys.executable, "-c", code, str(ctx)], env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True) for _ in range(2)]
    outs = [p.communicate(timeout=600) for p in procs]
    assert [p.returncode for p in procs] == [0, 0], outs
    assert all("ReqEng" in out for out, _ in outs)
    left = sorted(p.name for p in (tmp_path / "cache" / "shopsystem-bdd" / "pgf").iterdir())
    assert len(left) == 1 and not left[0].startswith(".tmp"), left
