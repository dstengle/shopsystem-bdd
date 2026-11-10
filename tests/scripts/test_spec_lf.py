"""The logical form (the CNL 4 design, call 8, section 7; I11a): spec_lf's form of a grammar 4 tree over the smallest
codified-2 context, one translation per template, the indexicals and parameters, and `model parse --form`."""
import pathlib
import subprocess
import sys

import pytest
import spec_grammar4
import spec_lf
import spec_meaning

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
CORPUS = REPO / "grammar" / "corpus" / "core-4.txt"


@pytest.fixture(scope="module")
def vocab():
    toolchain.require()
    return spec_grammar4.load(FIXTURE)[0]


def form(vocab, line):
    p = spec_grammar4.parse(FIXTURE, line)
    assert p.tree, p.refusal
    return spec_lf.form(vocab, p.tree)


def test_every_line_the_twin_parses_has_a_logical_form(vocab):
    lines = [raw for raw in CORPUS.read_text().splitlines() if raw.strip() and raw[0] not in "#="]
    for line in lines:
        p = spec_grammar4.parse(FIXTURE, line)
        for tree in p.trees:
            assert spec_lf.show(spec_lf.form(vocab, tree)).startswith("shall ["), line


def test_a_trigger_and_a_response_bind_one_referent_by_the(vocab):
    text = spec_lf.show(form(vocab, "When a session ends a stage, `work` shall print the stage."))
    assert text.splitlines() == ["shall [x3: tool `work` (constant)]",
                                 "  when [x1: session, x2: stage]",
                                 "    end(e1, subject: x1, object: x2)",
                                 "  response",
                                 "    print(e2, subject: x3, object: x2)"]


def test_a_compound_means_what_its_of_phrase_means(vocab):
    said = "When a session ends a stage, `work` shall print the %s."
    assert form(vocab, said % "stage status") == form(vocab, said % "status of the stage")


def test_this_before_a_kind_with_this_is_one_indexical_referent(vocab):
    f = form(vocab, "If `work` refuses this command, then `work` shall exit with an error naming this command.")
    assert [(r.kind, r.origin) for r in f.fixed] == [("tool", "constant"), ("command", "indexical")]
    assert f.fixed[1].value == "the command the run runs"


def test_a_code_that_names_no_word_is_a_parameter_and_an_actor_a_constant(vocab):
    f = form(vocab, "When the person runs `work start`, `work` shall exit successfully.")
    assert [(r.value, r.origin) for r in f.fixed] == [("the person", "constant"), ("`work start`", "parameter"),
                                                      ("`work`", "constant")]


def test_no_every_and_a_negated_clause_are_boxes(vocab):
    f = form(vocab, "While no session follows a stage, when the person runs `work start`, `work` shall print "
                    "every file.")
    assert f.parts[0].body[0].op == "not" and [r.kind for r in f.parts[0].body[0].refs] == ["session", "stage"]
    assert f.parts[-1].body[0].op == "every" and f.parts[-1].body[0].scope.body[0].pred == "event"


def test_the_two_meanings_of_a_line_are_two_forms(vocab):
    p = spec_grammar4.parse(FIXTURE, "When the person runs `work start`, `work` shall print every session that "
                                     "follows a stage and the stage.")
    assert p.refusal.startswith("refused: more than one meaning")
    assert len({spec_meaning.meaning(t, vocab) for t in p.trees}) == 2


def test_a_fun_with_no_translation_is_named(vocab):
    with pytest.raises(ValueError, match="k_stage_Nowhere"):
        spec_lf.form(vocab, "Ubiq NoPre (OneResp (k_stage_Nowhere x))")


def test_model_parse_form_prints_the_form_and_needs_grammar_4(vocab, tmp_path):
    model = [sys.executable, str(REPO / "scripts" / "model")]
    line = "When a session ends a stage, `work` shall print the stage."
    done = subprocess.run(model + ["--root", str(FIXTURE), "parse", "--form", line], capture_output=True, text=True)
    assert done.returncode == 0 and "end(e1, subject: x1, object: x2)" in done.stdout, done.stdout + done.stderr
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text("---\nlanguage: codified-1\n---\n# x\n")
    done = subprocess.run(model + ["--root", str(tmp_path), "parse", "--form", line], capture_output=True, text=True)
    assert done.returncode == 2 and "grammar 4" in done.stdout
