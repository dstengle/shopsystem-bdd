"""spec_logic: one translation per fun into telingo's `&tel` formulas (design-r2 §5), the labels and signatures
beside it (§5.7), a group's witness, a condition's definition, and the context's facts. The ids here are the
fixture's (`tests/scripts/fixtures/logic/cluster`), never the live spec's."""
import pathlib
import re
import sys
from re import MULTILINE as M

import pytest
import spec_engine
import spec_grammar
import spec_lexicon
import spec_logic

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
CLUSTER = REPO / "tests" / "scripts" / "fixtures" / "logic" / "cluster"
GLOSSARY = REPO / "tests" / "scripts" / "fixtures" / "glossary"
G13 = ("While a result is outputless, when a session ends a plan stage for a work-item with the result, `work run` "
       "shall set the status of the work-item to `awaiting-answer` and ask a question on the work-item.")
START = ("When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to "
         "`started`.")


@pytest.fixture(scope="module")
def vocab():
    toolchain.require()
    return spec_logic.Vocab(spec_lexicon.read(CLUSTER))


def tree(line, root=CLUSTER, grammar="Req"):
    parsed = spec_grammar.parse(root, line, grammar)
    assert parsed.tree, parsed.refusal
    return parsed.tree


def constraints(rules):
    return [r for r in rules.always + rules.dynamic + rules.initial if r.startswith(":- on(")]


def tid(vocab, kind, term="status"):
    return next(t for t, (k, e) in vocab.attrs.items() if vocab.kinds[k] == kind and e.term == term)


def test_every_fun_of_the_grammar_has_a_translation():
    for root in (CLUSTER, GLOSSARY):
        gram = spec_grammar.load(root)
        voc = spec_logic.Vocab(spec_lexicon.read(root))
        assert [f for f in gram.functions if not voc.covers(f)] == []


def test_the_vocabulary_names_each_typed_fun_by_its_lexicon_entry(vocab):
    assert vocab.decode("t_status_Is") == ("attribute", "t_status", "Is")
    assert vocab.decode("k_stage_Every") == ("kind", "k_stage", "Every")
    assert vocab.decode("rel_stage_for_initiative") == ("relation", "r_stage_for_initiative", None)
    assert vocab.decode("rel_result_gives_question_Atom") == ("relation", "r_result_gives_question", "Atom")
    assert vocab.decode("c_open_Pre") == ("condition", "c_open", "Pre")
    assert vocab.attrs[tid(vocab, "stage")][0] == "k_stage"


def test_statement_is_a_tel_constraint(vocab):
    """When T, S shall R: `:- on(id), B, &tel{ T & ~ > (R) }`, the response read at the next state."""
    [rule] = constraints(spec_logic.translate(vocab, "s#r11", tree(START)))
    assert rule == (':- on("s#r11"), kind(X1,k_initiative), &tel{ attr(X1,t_status,v_proposed) & '
                    'ran(a_the_person,"`work start`",X1) & ~ > (does(a_work,set(t_status,v_started),X1)) }.')


def test_each_response_and_trigger_pattern_is_a_choice(vocab):
    out = spec_logic.translate(vocab, "s#r11", tree(START))
    assert '{ ran(a_the_person,"`work start`",V1) : kind(V1,k_initiative) }.' in out.always
    assert "{ does(a_work,set(t_status,v_started),V1) : kind(V1,k_initiative) }." in out.always


def test_a_ubiquitous_statement_holds_in_every_state_over_used_things(vocab):
    [rule] = constraints(spec_logic.translate(vocab, "s#r2", tree(
        "Every stage for an initiative shall hold the initiative lock.")))
    assert rule == (':- on("s#r2"), kind(X1,k_stage), kind(X2,k_initiative), used(X1), '
                    '&tel{ rel(r_stage_for_initiative,X1,X2) & ~ holds(X1,s_initiative_lock) }.')


def test_while_holds_in_the_same_state_and_an_existential_object_is_an_auxiliary_atom(vocab):
    out = spec_logic.translate(vocab, "s#r10", tree("While a request is `awaiting-asker`, `work` shall write a "
                                                    "question."))
    t = tid(vocab, "request")
    [rule] = constraints(out)
    assert rule == (':- on("s#r10"), kind(X1,k_request), &tel{ attr(X1,%s,v_awaiting_asker) & '
                    '~ resp("s#r10",1,t) }.' % t)
    assert 'obj("s#r10",1,t,t(X2)) :- kind(X2,k_question), does(a_work,e_write,X2).' in out.always


def test_shall_not_is_the_constraint_on_the_forbidden_response(vocab):
    out = spec_logic.translate(vocab, "U2", tree("`work run` shall not start a stage that needs a resource that is "
                                                 "not free."))
    assert constraints(out) == [':- on("U2"), &tel{ resp("U2",1,t) }.']
    assert ('obj("U2",1,t,t(X1,X2)) :- kind(X1,k_stage), kind(X2,k_resource), does(a_work_run,e_start,X1), '
            'not cond(c_free,X2), rel(r_stage_needs_resource,X1,X2).') in out.always


def test_shall_not_under_a_trigger_is_strong_next_of_the_response(vocab):
    [rule] = constraints(spec_logic.translate(vocab, "s#r12", tree(
        "When the person runs `work start` on an initiative that is `proposed`, `work` shall not set its status to "
        "`started`.")))
    assert rule.endswith("& > (does(a_work,set(t_status,v_started),X1)) }.")


def test_and_gives_one_constraint_for_each_conjunct_under_one_guard(vocab):
    out = spec_logic.translate(vocab, "s#r13", tree(G13))
    rules = constraints(out)
    assert len(rules) == 2 and all(r.startswith(':- on("s#r13"), ') for r in rules)
    assert all("cond(c_outputless,X1) & " in r and "does(X2,e_end,X3) & ~ > (" in r for r in rules)
    assert "~ > (does(a_work_run,set(%s,v_awaiting_answer),X4)) }." % tid(vocab, "work-item") in rules[0]
    assert rules[1].endswith('~ > (resp("s#r13",2,t(X4))) }.')


def test_the_anaphora_binds_the_noun_phrase_before_it(vocab):
    [rule] = constraints(spec_logic.translate(vocab, "s#r5", tree(
        "While research stages for an initiative are `waiting`, when the person runs `work run`, `work run` shall "
        "start every research stage for the initiative.")))
    assert "rel(r_stage_for_initiative,X1,X2)" in rule and "rel(r_stage_for_initiative,X3,X2)" in rule
    assert rule.endswith("~ > (does(a_work_run,e_start,X3)) }.")


def test_no_in_a_clause_is_the_negation_of_an_auxiliary_atom(vocab):
    out = spec_logic.translate(vocab, "s#r14", tree(
        "When a session ends a stage with a result that gives no question, `work run` shall take the result."))
    [rule] = constraints(out)
    assert '~ some("s#r14",1,t(X3))' in rule
    assert ('some("s#r14",1,t(X3)) :- kind(X3,k_result), kind(X4,k_question), rel(r_result_gives_question,X3,X4).'
            in out.always)


def test_a_count_is_an_aggregate_of_the_running_holders(vocab):
    out = spec_logic.translate(vocab, "U1", tree("`work run` shall hold at most `workers` worker slots at a time."))
    assert constraints(out) == [':- on("U1"), #count{ Y : holds(Y,s_worker_slot), active(Y) } > 3.']


def test_labels(vocab):
    """g13 merged: the witness labels its condition and trigger at state 0, the statement its two responses."""
    t = tree(G13)
    text = "\n".join(spec_logic.witness(vocab, "s#g13", t, "s#r13").initial
                     + spec_logic.translate(vocab, "s#r13", t).always)
    assert re.search(r'^lab\("s#g13",cond\(1\),cond\(c_outputless,X1\)\) :- .*bind\("s#g13","X1",X1\)', text, M)
    assert re.search(r'^lab\("s#g13",trig,does\(X2,e_end,X3\)\) :- ', text, M)
    assert re.search(r'^lab\("s#g13",mod\(0,1\),attr\(X3,t_stage_kind,v_plan\)\) :- ', text, M)
    assert re.search(r'^lab\("s#r13",resp\(1\),does\(a_work_run,set\(t_status_\d,v_awaiting_answer\),X4\)\) :- .*'
                     r'not &tel\{ ~ < \(', text, M)
    assert re.search(r'^lab\("s#r13",resp\(2\),does\(a_work_run,e_ask,X5\)\) :- obj\("s#r13",2,t\(X4\),t\(X5\)\)',
                     text, M)
    assert re.search(r'^lab\("s#r13",mod\(2,1\),rel\(r_question_on_work_item,X5,X4\)\) :- obj\(', text, M)


def test_signatures(vocab):
    t = tree(G13)
    sigs = spec_logic.translate(vocab, "s#r13", t).sigs
    assert 'trig("s#r13",does(k_session),e_end,k_stage).' in sigs
    assert 'eff("s#r13",does(a_work_run),set(%s,v_awaiting_answer),k_work_item).' % tid(vocab, "work-item") in sigs
    assert 'eff("s#r13",does(a_work_run),e_ask,k_question).' in sigs
    assert {'uses("s#r13",%s).' % k for k in ("k_result", "k_session", "k_stage", "k_work_item", "k_question")} \
        <= set(sigs)
    assert 'untriggered("U2").' in spec_logic.translate(vocab, "U2", tree(
        "`work run` shall not start a stage that needs a resource that is not free.")).sigs
    assert 'trig("s#g13",does(k_session),e_end,k_stage).' in spec_logic.witness(vocab, "s#g13", t, "s#r13").sigs


def test_contrast_in_witness(vocab):
    """`every … that …`: the witness asks for one stage that fails the restriction, labelled no(1) (design-r2
    §5.7's not(1); `not` is a keyword of clingo)."""
    out = spec_logic.witness(vocab, "s#g20", tree(
        "When the person runs `work run`, `work run` shall start every research stage that is `waiting`."), "s#r20")
    text = "\n".join(out.initial + out.dynamic)
    assert '1 { bind("s#g20","C1",V) : kind(V,k_stage) } 1.' in text
    assert re.search(r'^:- bind\("s#g20","C1",C1\), .*&tel\{ attr\(C1,t_stage_kind,v_research\) & '
                     r'attr\(C1,t_status_\d,v_waiting\) \}\.', text, M)
    assert 'contrast("s#g20",1,C1) :- bind("s#g20","C1",C1).' in text
    assert re.search(r'^lab\("s#r20",no\(1\),does\(a_work_run,e_start,C1\)\) :- \'contrast\("s#g20",1,C1\)', text,
                     M)


def test_a_definition_is_a_rule_from_its_def_sentence(vocab):
    out = spec_logic.definition(vocab, tree("A result is outputless when the result gives no question.", grammar="Def"))
    assert 'cond(c_outputless,X0) :- kind(X0,k_result), not some("def:c_outputless",1,t(X0)).' in out.always
    assert ('some("def:c_outputless",1,t(X0)) :- kind(X0,k_result), kind(X1,k_question), '
            'rel(r_result_gives_question,X0,X1).') in out.always
    out = spec_logic.definition(vocab, tree("An initiative is open when the initiative is not `done` and the "
                                            "initiative is not `abandoned`.", grammar="Def"))
    assert out.always == [("cond(c_open,X0) :- kind(X0,k_initiative), not attr(X0,t_status,v_done), "
                          "not attr(X0,t_status,v_abandoned).")]


def test_the_lexicon_gives_values_transitions_guards_and_resources(vocab):
    out = spec_logic.facts(vocab)
    text = "\n".join(out["always"] + out["dynamic"])
    assert "value(k_stage,%s,v_waiting)." % tid(vocab, "stage") in text
    assert "trans(t_status,v_proposed,v_started)." in text and '#external on("T:status@initiative").' in text
    assert ":- on(\"T:status@initiative\"), does(_,set(t_status,W),X), 'attr(X,t_status,V), V != W, " \
           "not trans(t_status,V,W)." in text
    assert "capacity(s_spec_lock,1)." in text and "capacity(s_worker_slot,3)." in text
    assert "relk(r_stage_for_initiative,k_stage,k_initiative)." in text
    assert "primitive(c_outputless,k_result)." in text and "free_condition(c_free)." in text
    vocab.define("c_outputless")
    assert "primitive(c_outputless,k_result)." not in spec_logic.facts(vocab)["always"]
    vocab.defined.clear()


def test_the_program_puts_the_background_first_and_leaves_out_the_minimisation():
    text = spec_logic.program([{"always": ["p."]}])
    assert text.index("#program always.") < text.index("p.")
    assert "#minimize" not in text and "#minimize" in spec_logic.program([], optimise=True)


def test_a_witness_and_its_statement_solve_at_horizon_1(vocab):
    t = tree(START)
    parts = [spec_logic.facts(vocab), spec_logic.translate(vocab, "s#r11", t), spec_logic.witness(vocab, "s#g11", t,
                                                                                                    "s#r11")]
    pools = spec_logic.pool_sizes(parts)
    res = spec_engine.solve(spec_logic.program(parts), ["s#r11"], 3, pools)
    assert res.sat and res.horizon == 1
    [model] = res.models[:1]
    assert any(re.fullmatch(r'lab\("s#r11",resp\(1\),does\(a_work,set\(t_status,v_started\),o\(k_initiative,\d\)\),1\)', a)
               for a in model)
