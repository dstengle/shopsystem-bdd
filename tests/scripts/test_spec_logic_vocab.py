"""spec_logic_vocab: a codified-2 context's Vocab read from its layered lexicon with grammar 4's kind tree, and its
domain facts for `grammar/check.lp`, on the logic check's cluster (never the live spec)."""
import pathlib

import spec_logic_vocab
import spec_rgl_vocab

CLUSTER = pathlib.Path(__file__).resolve().parent / "fixtures" / "logic" / "cluster"


def _domain():
    vocab = spec_logic_vocab.Vocab(spec_rgl_vocab.lexicon(CLUSTER), spec_rgl_vocab.read(CLUSTER).kinds)
    return spec_logic_vocab.domain(vocab)


def test_domain_gives_kinds_values_transitions_and_initial_values():
    d = _domain()
    assert {"kind(k_initiative).", "kind(k_thing).", "sub(k_stage,k_session).", "actor(a_work).",
            "akind(a_work,k_tool)."} <= set(d)
    assert "trans(k_initiative,t_status,v_proposed,v_started)." in d
    assert "initial(k_initiative,t_status,v_proposed)." in d
    assert "initial(k_initiative,t_status,v_started)." not in d
    assert [f for f in d if f.startswith("val(k_stage,t_status_3,")] == [
        "val(k_stage,t_status_3,v_waiting).", "val(k_stage,t_status_3,v_running).", "val(k_stage,t_status_3,v_ended)."]


def test_a_relation_of_cardinality_one_or_a_preposition_is_functional():
    funs = {f for f in _domain() if f.startswith("fun(")}
    assert funs == {"fun(r_question_on_result).", "fun(r_result_of_stage).", "fun(r_stage_for_initiative)."}


def test_every_condition_is_prose_to_the_check():
    """Grammar 4 reads no definition of a condition: each is `prose(C)`, and nothing is `dalt` or `dlit`."""
    d = _domain()
    assert {f for f in d if f.startswith("prose(")} == {"prose(c_open).", "prose(c_outputless)."}
    assert not any(f.startswith(("dalt(", "dlit(")) for f in d)
