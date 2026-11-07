"""spec_facts: one translation per fun into ground facts (design-r3 §3); spec_logic_vocab.domain; spec_context, the
context read once. The ids are the fixtures' (`tests/scripts/fixtures/logic/cluster`, `fixtures/glossary`), never
the live spec's."""
import os
import pathlib
import shutil
import sys

import pytest
import spec_context
import spec_facts
import spec_grammar
import spec_lexicon
import spec_logic_vocab

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
CLUSTER = REPO / "tests" / "scripts" / "fixtures" / "logic" / "cluster"
GLOSSARY = REPO / "tests" / "scripts" / "fixtures" / "glossary"
START = ("When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to "
         "`started`.")
STOP = ("When the person runs `work start` on an initiative that is `proposed`, `work` shall not set its status to "
        "`started`.")
G13 = ("While a result is outputless, when a session ends a plan stage for a work-item with the result, `work run` "
       "shall set the status of the work-item to `awaiting-answer` and ask a question on the work-item.")


def _vocab(root):
    toolchain.require()
    v = spec_logic_vocab.Vocab(spec_lexicon.read(root))
    spec_context._define(root, spec_lexicon.read(root), v)
    return v


@pytest.fixture(scope="module")
def vocab():
    return _vocab(CLUSTER)


@pytest.fixture(scope="module")
def gvocab():
    return _vocab(GLOSSARY)


def tree(line, root=CLUSTER, grammar="Req"):
    parsed = spec_grammar.parse(root, line, grammar)
    assert parsed.tree, parsed.refusal
    return parsed.tree


def facts(vocab, ident, line, root=CLUSTER):
    return spec_facts.translate(vocab, ident, tree(line, root))


def test_every_fun_of_the_grammar_has_a_translation():
    for root in (CLUSTER, GLOSSARY):
        gram = spec_grammar.load(root)
        voc = spec_logic_vocab.Vocab(spec_lexicon.read(root))
        assert [f for f in gram.functions if not voc.covers(f)] == []


def test_the_vocabulary_names_each_typed_fun_by_its_lexicon_entry(vocab):
    assert vocab.decode("t_status_Is") == ("attribute", "t_status", "Is")
    assert vocab.decode("k_stage_Every") == ("kind", "k_stage", "Every")
    assert vocab.decode("rel_stage_for_initiative") == ("relation", "r_stage_for_initiative", None)
    assert vocab.decode("rel_result_gives_question_Atom") == ("relation", "r_result_gives_question", "Atom")
    assert vocab.decode("c_open_Pre") == ("condition", "c_open", "Pre")
    assert vocab.attrs["t_status_3"][0] == "k_stage"


def test_a_when_statement_gives_roles_condition_trigger_response_and_set(vocab):
    out = facts(vocab, "s#r11", START)
    assert out == ['form("s#r11",when).', 'role("s#r11",v1,k_initiative).',
                   'cond("s#r11",v1,t_status,v_proposed,pos).',
                   'trig("s#r11",ran,"`work start`",a_the_person,v1).', 'set("s#r11",1,v1,t_status,v_started).',
                   'resp("s#r11",1,pos,set(t_status,v_started),a_work,v1).']
    assert out == facts(vocab, "s#r11", START)          # deterministic


def test_shall_not_set_is_a_negative_response_only(vocab):
    out = facts(vocab, "s#r12", STOP)
    assert 'resp("s#r12",1,neg,set(t_status,v_started),a_work,v1).' in out
    assert not any(f.startswith("set(") for f in out)


def test_a_response_object_gives_its_restrictions(vocab):
    out = facts(vocab, "s#r1", "When the person runs `work start` on an initiative, `work run` shall start a "
                               "research stage for the initiative.")
    assert out[-4:] == ['role("s#r1",v2,k_stage).', 'oattr("s#r1",v2,t_stage_kind,v_research).',
                        'orel("s#r1",r_stage_for_initiative,v2,v1).', 'resp("s#r1",1,pos,e_start,a_work_run,v2).']
    out = facts(vocab, "U2", "`work run` shall not start a stage that needs a resource that is not free.")
    assert out == ['form("U2",ubiq).', 'role("U2",v1,k_stage).', 'role("U2",v2,k_resource).',
                   'ocond("U2",v2,c_free,neg).', 'orel("U2",r_stage_needs_resource,v1,v2).',
                   'resp("U2",1,neg,e_start,a_work_run,v1).']


def test_the_k_after_a_response_object_a_k_is_that_object(vocab):
    out = facts(vocab, "s#r2", "When the person runs `work start` on an initiative, `work run` shall start a "
                               "research stage for the initiative and end the stage.")
    assert 'resp("s#r2",1,pos,e_start,a_work_run,v2).' in out
    assert 'resp("s#r2",2,pos,e_end,a_work_run,v2).' in out
    assert not any(f.startswith('role("s#r2",v3') for f in out)


def test_every_gives_every_and_its_restriction_as_cond(vocab):
    out = facts(vocab, "s#r5", "While research stages for an initiative are `waiting`, when the person runs "
                               "`work run`, `work run` shall start every research stage for the initiative.")
    assert out == ['form("s#r5",while_when).', 'role("s#r5",v1,k_stage).', 'cond("s#r5",v1,t_stage_kind,v_research,pos).',
                   'role("s#r5",v2,k_initiative).', 'crel("s#r5",r_stage_for_initiative,v1,v2,pos).',
                   'cond("s#r5",v1,t_status_3,v_waiting,pos).', 'trig("s#r5",ran,a_work_run,a_the_person,none).',
                   'role("s#r5",v3,k_stage).', 'every("s#r5",v3).', 'cond("s#r5",v3,t_stage_kind,v_research,pos).',
                   'crel("s#r5",r_stage_for_initiative,v3,v2,pos).', 'resp("s#r5",1,pos,e_start,a_work_run,v3).']


def test_no_k_in_a_condition_is_none(vocab):
    out = facts(vocab, "s#r1", "While no work-item is `drafted`, `work` shall write a question.")
    assert 'none("s#r1",k_work_item,t_status_4,v_drafted).' in out
    assert not any(f.startswith('role("s#r1",v1,k_work_item)') for f in out)
    out = facts(vocab, "s#r14", "When a session ends a stage with a result that gives no question, `work run` "
                                "shall take the result.")
    assert 'rnone("s#r14",r_result_gives_question,v3,kind(k_question)).' in out
    assert not any("k_question" in f and f.startswith("role(") for f in out)


def test_hold_at_most_is_count(vocab):
    assert facts(vocab, "U1", "`work run` shall hold at most `workers` worker slots at a time.") == [
        'form("U1",ubiq).', 'count("U1",s_worker_slot,"`workers`").']


def test_holds_and_is_free_are_pre_state(vocab):
    out = facts(vocab, "s#r2", "While a session holds the spec lock and the initiative lock is free, `work run` "
                               "shall hold a worker slot.")
    assert out == ['form("s#r2",while).', 'role("s#r2",v1,k_session).', 'holds("s#r2",v1,s_spec_lock).',
                   'free("s#r2",s_initiative_lock).', 'resp("s#r2",1,pos,hold(s_worker_slot),a_work_run,none).']


def test_shall_use_is_static(gvocab):
    out = facts(gvocab, "s#r4", "The implementer shall use `Skill`.", GLOSSARY)
    assert out == ['form("s#r4",ubiq).', 'uses("s#r4",a_the_implementer,"`Skill`").']
    out = facts(gvocab, "s#r6", "The planner shall not use `Bash`.", GLOSSARY)
    assert out == ['form("s#r6",ubiq).', 'nouse("s#r6",a_the_planner,"`Bash`").']


def test_a_where_feature_is_feat(vocab):
    out = facts(vocab, "s#r3", "Where `--json` is given, `work` shall write a question.")
    assert out == ['form("s#r3",where).', 'feat("s#r3","`--json`").', 'role("s#r3",v1,k_question).',
                   'resp("s#r3",1,pos,e_write,a_work,v1).']


def test_the_other_triggers_and_verb_phrases(gvocab):
    def of(line):
        return facts(gvocab, "s#r1", line, GLOSSARY)
    out = of("When `tools size` is run, `tools` shall print the status of the initiative and exit successfully.")
    assert 'trig("s#r1",ran,"`tools size`",any,none).' in out
    assert 'resp("s#r1",1,pos,print,a_tools,value(t_status_4,v1)).' in out
    assert 'resp("s#r1",2,pos,exit_ok,a_tools,none).' in out
    out = of("When `work` refuses a work-item, `work` shall exit with an error naming the work-item.")
    assert out[-2:] == ['trig("s#r1",does,e_refuse,a_work,v1).', 'resp("s#r1",1,pos,exit_error,a_work,v1).']
    out = of("When an initiative becomes `started`, `work` shall change nothing.")
    assert out[-2:] == ['trig("s#r1",becomes,set(t_status_4,v_started),any,v1).',
                        'resp("s#r1",1,pos,change_nothing,a_work,none).']
    out = of("When the person runs `work run`, `work run` shall give only a brief to the stage.")
    assert out[-1] == 'only("s#r1",1,k_brief).' and not any(f.startswith("resp(") for f in out)
    out = of("When the person runs `work start` on the initiative `i1`, `work` shall print the number of work-items "
             "that are `done`.")
    assert out[1:3] == ['role("s#r1",v1,k_initiative).', 'named("s#r1",v1,"`i1`").']
    assert out[-1] == 'resp("s#r1",1,pos,print,a_work,number(k_work_item)).'
    out = of("While no work-item is `done` and no initiative is open, `work` shall print `x`.")
    assert 'cnone("s#r1",k_initiative,c_open).' in out



def test_a_quoted_figure_for_a_thing_is_an_event_on_that_thing(gvocab):
    out = facts(gvocab, "s#r1", 'When the person runs `work start` on an initiative, `work` shall not show "turns" '
                                'for the initiative.', GLOSSARY)
    assert out[-1] == 'resp("s#r1",1,neg,for(e_show,"turns"),a_work,v1).'


def test_cond_or_splits_the_requirement(vocab):
    out = facts(vocab, "s#r5", "While an initiative is `proposed` or the initiative is `started`, `work` shall "
                               "write a question.")
    assert out[:4] == ['disj("s#r5#1","s#r5").', 'form("s#r5#1",while).', 'role("s#r5#1",v1,k_initiative).',
                       'cond("s#r5#1",v1,t_status,v_proposed,pos).']
    assert 'disj("s#r5#2","s#r5").' in out and 'cond("s#r5#2",v1,t_status,v_started,pos).' in out
    assert not any(f.startswith("disj(") and '"s#r5#3"' in f for f in out)
    assert spec_facts.split("s#r5#2") == "s#r5" and spec_facts.split("s#r5") == "s#r5"
    assert spec_facts.split("U1#2") == "U1" and spec_facts.split("U1") == "U1"


def test_a_value_list_splits_and_a_negated_one_is_one_neg_each(vocab):
    out = facts(vocab, "s#r7", "When the person runs `work start` on an initiative whose status is `proposed` or "
                               "`started`, `work` shall set its status to `done`.")
    assert 'cond("s#r7#1",v1,t_status,v_proposed,pos).' in out and 'cond("s#r7#2",v1,t_status,v_started,pos).' in out
    out = facts(vocab, "s#r8", "When the person runs `work start` on an initiative whose status is not `proposed` or "
                               "`started`, `work` shall set its status to `done`.")
    assert not any(f.startswith("disj(") for f in out)
    assert out[2:4] == ['cond("s#r8",v1,t_status,v_proposed,neg).', 'cond("s#r8",v1,t_status,v_started,neg).']


def test_a_defined_condition_expands_when_positive(vocab):
    out = facts(vocab, "s#r13", G13)
    assert out[:4] == ['form("s#r13",while_when).', 'role("s#r13",v1,k_result).',
                       'ccond("s#r13",v1,c_outputless,pos).',
                       'rnone("s#r13",r_result_gives_question,v1,kind(k_question)).']
    assert 'set("s#r13",1,v4,t_status_4,v_awaiting_answer).' in out
    assert out[-3:] == ['role("s#r13",v5,k_question).', 'orel("s#r13",r_question_on_work_item,v5,v4).',
                        'resp("s#r13",2,pos,e_ask,a_work_run,v5).']
    out = facts(vocab, "s#r1", "When the person runs `work run`, `work run` shall take every open initiative.")
    assert out[3:7] == ['every("s#r1",v1).', 'ccond("s#r1",v1,c_open,pos).', 'cond("s#r1",v1,t_status,v_done,neg).',
                        'cond("s#r1",v1,t_status,v_abandoned,neg).']
    out = facts(vocab, "s#r2", "While a result is not outputless, `work` shall write a question.")
    assert out[2] == 'ccond("s#r2",v1,c_outputless,neg).' and not any(f.startswith("rnone") for f in out)


def test_a_prose_condition_is_opaque(vocab):
    out = facts(vocab, "s#r1", "While a resource is free, `work` shall write a question.")
    assert out[1:3] == ['role("s#r1",v1,k_resource).', 'ccond("s#r1",v1,c_free,pos).']
    assert out[3] == 'role("s#r1",v2,k_question).'


def test_an_unknown_fun_is_refused_naming_it(vocab):
    with pytest.raises(ValueError, match="k_nothing_An"):
        spec_facts.translate(vocab, "s#r1", ("Ubiq", ("OneResp", ("Shall", ("NPSubj", ("k_nothing_An", ("k_x",))),
                                                                   ("OneVP", ("ExitOk",))))))
    with pytest.raises(ValueError, match="NoSuchVP"):
        spec_facts.translate(vocab, "s#r1", ("Ubiq", ("OneResp", ("Shall", ("ActorSubj", ("a_work",)),
                                                                   ("OneVP", ("NoSuchVP",))))))


def test_domain_gives_values_transitions_and_initial_values(vocab):
    d = spec_logic_vocab.domain(vocab)
    assert "kind(k_initiative)." in d and "actor(a_work_run)." in d
    assert "trans(k_initiative,t_status,v_proposed,v_started)." in d
    assert "initial(k_initiative,t_status,v_proposed)." in d
    assert "initial(k_initiative,t_status,v_started)." not in d
    vals = [f for f in d if f.startswith("val(k_stage,t_status_3,")]
    assert vals == ["val(k_stage,t_status_3,v_waiting).", "val(k_stage,t_status_3,v_running).",
                    "val(k_stage,t_status_3,v_ended)."]
    assert "initial(k_stage,t_stage_kind,v_plan)." in d       # no transitions: every value


def test_the_context_is_read_once_per_state_of_its_files(tmp_path):
    toolchain.require()
    shutil.copytree(CLUSTER, tmp_path / "c")
    root = tmp_path / "c"
    ctx = spec_context.load(root)
    assert spec_context.load(root) is ctx
    assert [s.id for s in ctx.statements][:2] == ["supervision#r1", "supervision#r2"]
    assert ctx.statements[-1] == spec_context.Statement("U2", None, None, ctx.statements[-1].tree)
    assert ctx.statements[0].group == "supervision#g1" and ctx.statements[0].capability == "supervision"
    assert ctx.facts["supervision#r11"][0] == 'form("supervision#r11",when).'
    assert ctx.refused == {} and ctx.domain == spec_logic_vocab.domain(ctx.vocab) + spec_facts.def_facts(ctx.vocab)
    assert "c_outputless" in ctx.vocab.def_lits and "c_free" not in ctx.vocab.def_lits
    cap = root / "spec" / "capabilities" / "supervision.md"
    cap.write_text(cap.read_text().replace("- [r12] When", "- [r12] Whenever"))
    os.utime(cap, ns=(cap.stat().st_mtime_ns + 10**9,) * 2)
    again = spec_context.load(root)
    assert again is not ctx and "supervision#r12" in again.refused and "supervision#r12" not in again.facts
    draft = tmp_path / "supervision.md"
    draft.write_text(cap.read_text().replace("- [r12] Whenever", "- [r12] When").replace(
        "shall not set its status to `started`.", "shall set its status to `done`."))
    drafted = spec_context.load(root, [draft])
    assert drafted.refused == {} and drafted.caps["supervision"].path == draft
    assert 'set("supervision#r12",1,v1,t_status,v_done).' in drafted.facts["supervision#r12"]
    assert spec_context.load(root, [draft]) is drafted


def test_a_definite_with_no_antecedent_is_the_one_thing_of_its_kind(vocab):
    out = facts(vocab, "x", "When the person runs `work run` on the initiative, `work run` shall start a stage for "
                            "the initiative.")
    assert 'the("x",v1).' in out and 'orel("x",r_stage_for_initiative,v2,v1).' in out
    assert not any(f.startswith("the(") for f in facts(vocab, "x", START))     # "its" has the initiative before it


def test_every_in_a_condition_is_a_universal_not_a_role(vocab):
    out = facts(vocab, "x", "While every stage for the initiative is `ended`, when the person runs `work run` on an "
                            "initiative that is `started`, `work run` shall start a stage.")
    assert {'uall("x",u1,k_stage).', 'urel("x",r_stage_for_initiative,u1,v1).',
            'ucond("x",u1,t_status_3,v_ended,pos).'} <= set(out)
    assert not any(f.startswith('role("x",u1') for f in out)


def test_a_definition_of_literals_on_its_subject_is_a_domain_fact(vocab):
    out = spec_facts.def_facts(vocab)
    assert {"prose(c_free).", "dalt(c_open,1).", "dlit(c_open,1,t_status,v_done,neg).",
            "dlit(c_open,1,t_status,v_abandoned,neg)."} <= set(out)
    assert not any("c_outputless" in f for f in out)            # defined with a relation: followed, not a literal


def test_a_relation_of_cardinality_one_or_a_preposition_is_functional(vocab):
    funs = {f for f in spec_logic_vocab.domain(vocab) if f.startswith("fun(")}
    assert "fun(r_stage_with_result)." in funs and "fun(r_stage_for_initiative)." in funs
    assert "fun(r_result_gives_question)." not in funs and "fun(r_stage_needs_resource)." not in funs
