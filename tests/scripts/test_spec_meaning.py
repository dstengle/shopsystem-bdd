"""One meaning, or refused (the CNL 4 design, call 2; I9): spec_meaning's normalised trees, the tree kept and the
words that read two ways."""
import spec_meaning

# two trees of one line that differ only in the funs that carry a noun phrase to its slot
CARRIED = "e_print (k_thing_One (k_session_Up_k_thing (k_session_Det DetA k_session_n)))"
DIRECT = "e_print (k_session_Det DetA k_session_n)"
# a list under follow, or under print
UNDER_FOLLOW = 'Shall a (e_print (k_thing_One (Rel (e_follow (k_stage_And (Two s t))))))'
UNDER_PRINT = 'Shall a (e_print (k_thing_And (Two (Rel (e_follow (k_stage_One s))) t)))'


def test_a_tree_is_read_and_written_back_word_for_word():
    text = 'When NoPre (k_command_Code (CodeLit "`work start`")) (OneResp x)'
    assert spec_meaning.write(spec_meaning.read(text)) == text


def test_trees_that_differ_only_in_carrying_funs_have_one_meaning_and_the_shorter_is_kept():
    assert spec_meaning.meaning(CARRIED) == spec_meaning.meaning(DIRECT)
    assert spec_meaning.one([CARRIED, DIRECT]) == (DIRECT, None)


def test_only_and_a_code_are_no_carrying_funs():
    assert spec_meaning.meaning("k_stage_Only (k_stage_Simple x)") != spec_meaning.meaning("x")


def test_trees_of_two_meanings_are_refused_naming_the_subtree_that_reads_two_ways():
    kept, two = spec_meaning.one([UNDER_FOLLOW, UNDER_PRINT])
    assert kept is None and two[1] == 2
    assert two[0] in ("k_thing_One (Rel (e_follow (k_stage_And (Two s t))))",
                      "k_thing_And (Two (Rel (e_follow (k_stage_One s))) t)")


def test_a_tree_with_no_translation_is_no_meaning_and_none_raises(monkeypatch):
    import pytest
    import spec_lf

    def form(_vocab, tree):
        if tree == UNDER_PRINT:
            raise ValueError("no translation of it")
        return tree
    monkeypatch.setattr(spec_lf, "form", form)
    assert spec_meaning.one([UNDER_FOLLOW, UNDER_PRINT], vocab=object()) == (UNDER_FOLLOW, None)
    with pytest.raises(ValueError, match="no translation of it"):
        spec_meaning.one([UNDER_PRINT], vocab=object())
