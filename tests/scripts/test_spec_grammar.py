"""spec_grammar: tokenising (design §9.4), parsing with the guards (§9.3), linearising, the corpus, and the
compile cache with its atomic rename (§11.3)."""
import contextlib
import os
import pathlib
import re
import subprocess
import sys

import pytest
import spec_grammar
import spec_lexicon
import spec_relations
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

- **`work`** (proper noun): the queue's command.
- **initiative** (noun): a delivery.
- **status** (attribute of initiative): Values: `proposed`, `started`.
"""


@pytest.fixture(scope="module")
def root():
    toolchain.require()
    return FIXTURE


def lines(path):
    return [x.strip() for x in path.read_text().splitlines() if x.strip() and not x.startswith("#")]


@contextlib.contextmanager
def stubbed(root, rows=(), terms=()):
    """spec_lexicon.read of `root` gives its lexicon with `terms` and the relation rows (k1, word, k2) added, as
    rows of a `## Relations` table would be."""
    real = spec_lexicon.read
    lex = real(root)
    stub = spec_lexicon.Lexicon(list(lex.terms) + list(terms),
                                list(lex.rows) + [spec_relations.Row(a, w, b, "", "stub") for a, w, b in rows])
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(spec_lexicon, "read", lambda r: stub if pathlib.Path(r) == pathlib.Path(root) else real(r))
        yield stub


def core():
    """grammar/corpus/core.txt as (rows, [(grammar, line, expected tree, guard row or None)])."""
    rows, out, guard = [], [], None
    for raw in (CORPUS / "core.txt").read_text().splitlines():
        if raw.startswith(("# row: ", "# guard: ")):
            row = tuple(x.strip() for x in raw.split(": ", 1)[1].split("|"))
            rows, guard = (rows + [row], guard) if raw.startswith("# row") else (rows, row)
        elif raw.startswith("= "):
            out[-1] = out[-1][:2] + (raw[2:].strip(), out[-1][3])
        elif raw.strip() and not raw.startswith("#"):
            grammar, line = ("Def", raw[6:]) if raw.startswith("[Def] ") else ("Req", raw)
            out.append((grammar, line.strip(), None, guard))
            guard = None
    return rows, out


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
    assert spec_grammar.tokenise("A worker shall exit successfully.")[0] == "a"       # a one-letter first word


def test_require_fails_naming_tools_install_when_a_tool_is_missing(monkeypatch):
    import tools_grammar
    monkeypatch.setattr(tools_grammar, "gf_binary", lambda environ=None: None)
    with pytest.raises(pytest.fail.Exception) as failed:
        toolchain.require()
    assert "gf" in str(failed.value) and "python3 scripts/tools install" in str(failed.value)


def test_gf_binary_prefers_the_environment(monkeypatch, tmp_path):
    gf = tmp_path / "gf"
    gf.write_text("#!/bin/sh\n")
    monkeypatch.setenv("SHOPSYSTEM_GF", str(gf))
    assert spec_grammar.gf_binary() == str(gf)


def test_gf_binary_is_the_one_lookup_of_tools_grammar(monkeypatch):
    import tools_grammar
    monkeypatch.setattr(tools_grammar, "gf_binary", lambda environ=None: "/the/one/lookup/gf")
    assert spec_grammar.gf_binary() == "/the/one/lookup/gf"


def test_the_rgl_is_found_by_the_one_lookup_of_tools_grammar(monkeypatch):
    import tools_grammar
    monkeypatch.setattr(tools_grammar, "rgl_path", lambda environ=None: "/the/one/lookup/gf-rgl")
    assert spec_grammar.rgl_path() == "/the/one/lookup/gf-rgl"


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
    assert p.tree is not None and p.before == 1     # a literal slot does not read a lexicon word
    assert "CodeLit" not in {n[0] for n in spec_tree.nodes(p.tree)}


def test_a_literal_slot_does_not_read_a_lexicon_word_so_long_coordinations_are_read_whole(root):
    line = ", ".join("`%s` shall print `v%d`" % ("work run" if i % 2 else "work", i) for i in range(7))
    p = spec_grammar.parse(root, line + ", and `features` shall print `v7`.")
    assert p.tree is not None and p.before < spec_grammar.LIMIT


def test_hint_gives_the_parsed_prefix_and_the_nearest_words(root):
    h = spec_grammar.hint(root, "When the person runs `work start` on an initiatve, `work` shall exit successfully.")
    assert h["prefix"] == "When the person runs `work start` on an" and h["token"] == "initiatve"
    assert "initiative" in h["near"]


def test_linearise_writes_a_tree_back_as_a_sentence(root):
    tree = ("Ubiq", ("OneResp", ("Shall", ("ActorSubj", ("a_work_run",)), ("OneVP", ("Hold", ("s_spec_lock",))))))
    assert spec_grammar.linearise(root, tree) == "`work run` shall hold the spec lock."


def unnumbered(tree):
    """A tree as core.txt writes it: the generated ids' numbers left out (t_status_6 -> t_status)."""
    return re.sub(r"_\d+(?=[_ )]|$)", "", spec_tree.show(tree))


@pytest.fixture(scope="module")
def live():
    toolchain.require()
    return REPO


def test_every_core_line_has_its_expected_tree_and_linearises_back(live):
    rows, items = core()
    failures = []
    with stubbed(live, rows):
        for grammar, line, want, _ in items:
            p = spec_grammar.parse(live, line, grammar)
            got = unnumbered(p.tree) if p.tree else p.refusal
            if want.startswith("refused: ") and p.tree is None and want[9:] in p.refusal:
                continue
            if got != want:
                failures.append("%s\n    got  %s\n    want %s" % (line, got, want))
            elif spec_grammar.linearise(live, p.tree, grammar) != spec_grammar.normalise(line):
                failures.append("%s\n    linearises as %s" % (line, spec_grammar.linearise(live, p.tree, grammar)))
    assert not failures, "\n".join(failures)


def test_core_has_a_line_for_each_new_fun_and_the_three_definitions():
    _, items = core()
    text = " ".join(want for _, _, want, _ in items)
    for fun in ("AndVP", "OrVP", "OneVPor", "AndResp", "CondOr", "_Atom", "rel_stage_for_node ",
                "rel_stage_for_work_item ", "_Def ", "QuotedFor "):
        assert fun in text, fun
    assert len([g for g, _, _, _ in items if g == "Def"]) == 3 and "the line count and exit" in str(items)


def test_a_guarded_core_line_is_refused_as_ambiguous_once_its_row_is_added(live):
    rows, items = core()
    guarded = [(g, line, row) for g, line, _, row in items if row]
    assert {row for _, _, row in guarded} == {("work-item", "with", "result"), ("initiative", "with", "result")}
    for grammar, line, row in guarded:
        with stubbed(live, rows + [row]):
            p = spec_grammar.parse(live, line, grammar)
        assert p.tree is None and p.refusal == "ambiguous: 2 trees", (line, p.refusal)


def test_the_and_coordinations_replace_refuse_err_and_commit_push(live):
    p = spec_grammar.parse(live, "If `work` refuses a command, then `work` shall exit with an error naming the "
                                 "reason and change nothing.")
    assert p.tree and {n[0] for n in spec_tree.nodes(p.tree)} >= {"AndVP", "ExitErr", "ChangeNothing"}
    gf = (spec_grammar.GRAMMARS / "Req.gf").read_text() + (spec_grammar.GRAMMARS / "ReqEng.gf").read_text()
    assert "RefuseErr" not in gf and "CommitPush" not in gf


PP = """## Glossary

- **`work run`** (proper noun): the supervisor.
- **session** (noun): one conversation.
- **stage** (noun): one session's part.
- **work-item** (noun): a unit of delivery.
- **result** (noun): what a stage writes.
- **stage kind** (attribute of stage): Values: `plan`, `research`.
- **end** (verb): a stage stops. Frame: session ends stage.
- **discard** (verb): a stage's work is dropped. Frame: `work run` discards stage.
"""
PP_LINE = ("When a session ends a `plan` stage for a work-item with the result, `work run` shall discard the "
           "stage.")


def test_a_preposition_resolves_by_the_relation_rows_the_lexicon_gives(tmp_path):
    toolchain.require()
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text(PP)
    rows = [("stage", "for", "work-item"), ("stage", "with", "result")]
    with stubbed(tmp_path, rows):
        p = spec_grammar.parse(tmp_path, PP_LINE)
    assert p.tree and "rel_stage_with_result (rel_stage_for_work_item" in spec_tree.show(p.tree)
    with stubbed(tmp_path, rows + [("work-item", "with", "result")]):
        p = spec_grammar.parse(tmp_path, PP_LINE)
    assert p.tree is None and p.refusal == "ambiguous: 2 trees"
    with stubbed(tmp_path, rows[:1]):
        assert spec_grammar.parse(tmp_path, PP_LINE).tree is None


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
    import spec_gf
    monkeypatch.setattr(spec_gf, "_run_gf", no_gf)
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
