"""spec_typed_def: the generated Def/DefEng modules, and definitions parsed with grammar="Def" (design-r2 §4.3)."""
import pathlib
import sys

import spec_grammar
import spec_lexicon
import spec_tree
import spec_typed_def

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import toolchain
from test_spec_grammar import REPO, stubbed, unnumbered

ROWS = [("result", "gives", "question"), ("result", "gives", "output")]
LEX = spec_lexicon.Lexicon([
    spec_lexicon.Term("result", "kind"), spec_lexicon.Term("initiative", "kind"),
    spec_lexicon.Term("outputless", "condition", ("result",)),
    spec_lexicon.Term("open", "condition", ("initiative", "work-item")),
])


def test_modules_give_one_def_fun_for_each_condition_and_kind():
    mods = spec_typed_def.modules(LEX)
    assert sorted(mods) == ["Def.gf", "DefEng.gf"]
    assert "abstract Def = Req **" in mods["Def.gf"] and "startcat = Def" in mods["Def.gf"]
    assert "c_outputless_k_result_Def : Cond -> Def ;" in mods["Def.gf"]
    assert "c_open_k_initiative_Def : Cond -> Def ;" in mods["Def.gf"]
    assert "work_item" not in mods["Def.gf"]       # work-item is no kind of this lexicon
    assert 'c_outputless_k_result_Def c = art ++ "result" ++ "is" ++ "outputless" ++ "when" ++ c' in mods["DefEng.gf"]


def test_a_lexicon_with_no_condition_gives_an_empty_def_module_that_compiles(tmp_path):
    mods = spec_typed_def.modules(spec_lexicon.Lexicon([spec_lexicon.Term("result", "kind")]))
    assert "\n  fun\n" not in mods["Def.gf"] and "\n  lin\n" not in mods["DefEng.gf"]
    toolchain.require()
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text("## Glossary\n\n- **`work`** (proper noun): the queue.\n")
    assert "DefEng" in spec_grammar.load(tmp_path, "Def").languages


def test_the_three_definitions_of_the_design_give_their_trees_or_the_refusal():
    toolchain.require()
    with stubbed(REPO, ROWS):
        outputless = spec_grammar.parse(REPO, "A result is outputless when the result gives no question and the "
                                              "result gives no output.", grammar="Def")
        is_open = spec_grammar.parse(REPO, "An initiative is open when the initiative is not `done` and the "
                                           "initiative is not `abandoned`.", grammar="Def")
        it = spec_grammar.parse(REPO, "A result is outputless when it gives no question.", grammar="Def")
    assert spec_tree.show(outputless.tree) == (
        "c_outputless_k_result_Def (CondAnd (rel_result_gives_question_Atom (k_result_The k_result) (k_question_No "
        "k_question)) (CondOne (rel_result_gives_output_Atom (k_result_The k_result) (k_output_No k_output))))")
    assert unnumbered(is_open.tree) == (
        "c_open_k_initiative_Def (CondAnd (t_status_IsNot (k_initiative_The k_initiative) v_done) (CondOne "
        "(t_status_IsNot (k_initiative_The k_initiative) v_abandoned)))")
    assert it.tree is None and it.trees == []
    assert "a definition names its subject as the result" in it.refusal


def test_a_definition_is_no_requirement_and_a_requirement_no_definition():
    toolchain.require()
    with stubbed(REPO, ROWS):
        assert spec_grammar.parse(REPO, "A result is outputless when the result gives no question.").tree is None
        assert spec_grammar.parse(REPO, "`work run` shall exit successfully.", grammar="Def").tree is None
        assert "DefEng" in spec_grammar.load(REPO, "Def").languages
