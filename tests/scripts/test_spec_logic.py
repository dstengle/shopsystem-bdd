"""spec_logic: one translation per core and typed fun (design §12.1), the witness of a group, and the context's
facts for the background theory (§12.2)."""
import pathlib
import sys

import pytest
import spec_grammar
import spec_lexicon
import spec_logic

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
CLUSTER = REPO / "tests" / "scripts" / "fixtures" / "logic" / "cluster"
GLOSSARY = REPO / "tests" / "scripts" / "fixtures" / "glossary"


@pytest.fixture(scope="module")
def vocab():
    toolchain.require()
    return spec_logic.Vocab(spec_lexicon.read(CLUSTER))


def tree(line, root=CLUSTER):
    parsed = spec_grammar.parse(root, line)
    assert parsed.tree, parsed.refusal
    return parsed.tree


def rules(part):
    return "\n".join(part)


def constraints(part):
    return [r for r in part if r.startswith(":-")]


def test_every_fun_of_the_grammar_has_a_translation(vocab):
    for root in (CLUSTER, GLOSSARY):
        gram = spec_grammar.load(root)
        voc = spec_logic.Vocab(spec_lexicon.read(root))
        missing = [f for f in gram.functions if not voc.covers(f)]
        assert missing == []


def test_the_vocabulary_names_each_typed_fun_by_its_lexicon_entry(vocab):
    assert vocab.decode("t_status_3_Is") == ("attribute", "t_status_3", "Is")
    assert vocab.decode("k_stage_Every") == ("kind", "k_stage", "Every")
    assert vocab.decode("r_for_2") == ("relation", "r_for_2", None)
    assert vocab.decode("c_open_Pre") == ("condition", "c_open", "Pre")
    assert vocab.decode("v_waiting") == ("value", "v_waiting", None)
    assert vocab.attrs["t_status_3"][0] == "k_stage"
    assert vocab.rels["r_for_2"] == "r_for"


def test_an_event_driven_statement_is_a_dynamic_constraint_with_the_response_at_the_next_step(vocab):
    out = spec_logic.translate(vocab, "s#r11", tree(
        "When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to "
        "`started`."))
    assert constraints(out["always"]) == []
    [rule] = constraints(out["dynamic"])
    assert "{ attr(X1,t_status,v_started) } :- 'kind(X1,k_initiative), " in rules(out["dynamic"])
    assert rule.startswith(':- on("s#r11"), ')
    assert "'ran(a_the_person,\"`work start`\",X1)" in rule
    assert "'attr(X1,t_status,v_proposed)" in rule
    assert rule.endswith("not attr(X1,t_status,v_started).")


def test_a_ubiquitous_statement_holds_in_every_state(vocab):
    out = spec_logic.translate(vocab, "s#r2", tree("Every stage for an initiative shall hold the initiative lock."))
    [rule] = constraints(out["always"])
    assert rule == ':- on("s#r2"), kind(X1,k_stage), rel(r_for,X1,X2), kind(X2,k_initiative), ' \
                   "not holds(X1,s_initiative_lock)."
    assert out["dynamic"] == []


def test_shall_not_puts_the_response_in_the_body_and_reads_its_object_universally(vocab):
    out = spec_logic.translate(vocab, "U2", tree(
        "`work run` shall not start a stage that needs a resource that is not free."))
    assert not any(r.startswith("{") for r in out["always"])
    [rule] = constraints(out["always"])
    assert rule == ':- on("U2"), does(a_work_run,e_start,X1), kind(X1,k_stage), rel(r_needs,X1,X2), ' \
                   "kind(X2,k_resource), not cond(c_free,X2)."


def test_an_existential_object_of_a_response_is_a_new_thing(vocab):
    out = spec_logic.translate(vocab, "s#r10", tree("While a request is `awaiting-asker`, `work` shall write a "
                                                    "question."))
    assert 'thing(n("s#r10",1)).' in out["always"]
    assert 'kind(n("s#r10",1),k_question).' in out["always"]
    assert out["always"][-1].endswith('not does(a_work,e_write,n("s#r10",1)).')


def test_the_anaphora_binds_the_noun_phrase_before_it(vocab):
    out = spec_logic.translate(vocab, "s#r5", tree(
        "While research stages for an initiative are `waiting`, when the person runs `work run`, `work run` shall "
        "start every research stage for the initiative."))
    [rule] = constraints(out["dynamic"])
    assert "'rel(r_for,X1,X2)" in rule and "'rel(r_for,X3,X2)" in rule
    assert rule.endswith("not does(a_work_run,e_start,X3).")


def test_a_count_is_an_aggregate_of_the_running_holders(vocab):
    out = spec_logic.translate(vocab, "U1", tree("`work run` shall hold at most `workers` worker slots at a time."))
    assert constraints(out["always"]) == [':- on("U1"), #count{ Y : holds(Y,s_worker_slot), active(Y) } > 3.']


def test_a_group_witness_makes_plurals_two_things_and_puts_the_trigger_at_step_one(vocab):
    out = spec_logic.witness(vocab, "g5", [tree(
        "While research stages for an initiative are `waiting`, when the person runs `work run`, `work run` shall "
        "start every research stage for the initiative.")])
    facts = rules(out["always"])
    for name in ('w("g5",1)', 'w("g5",2)'):
        assert "kind(%s,k_stage)." % name in facts
        assert "rel(r_for,%s,w(\"g5\",3))." % name in facts
    assert facts.count("kind(w(\"g5\",3),k_initiative).") == 1
    assert ':- not wit(0).' in out["initial"]
    assert ":- '__w0, not wit(1)." in out["dynamic"]
    assert "attr(w(\"g5\",1),t_status_3,v_waiting)" in facts
    assert "ran(a_the_person,a_work_run,none)" in facts


def test_the_lexicon_gives_values_transitions_and_resources(vocab):
    out = rules(spec_logic.facts(vocab)["always"])
    assert "value(k_stage,t_status_3,v_waiting)." in out
    assert "capacity(s_spec_lock,1)." in out and "capacity(s_worker_slot,3)." in out
    assert "start_event(e_start)." in out and "end_event(e_end)." in out
    assert "free_condition(c_free)." in out and "resource_kind(k_resource)." in out
    assert "resource_relation(r_needs)." in out


def test_a_condition_means_what_its_means_says(vocab):
    out = rules(spec_logic.facts(vocab)["always"])
    assert "cond(c_open,X) :- kind(X,k_initiative), not attr(X,t_status,v_done), not attr(X,t_status,v_abandoned)." \
        in out


def test_a_condition_whose_means_does_not_read_is_left_free(vocab):
    lex = spec_lexicon.read(GLOSSARY)
    out = rules(spec_logic.facts(spec_logic.Vocab(lex))["always"])
    assert "{ cond(c_passing,X) } :- kind(X,k_scenario)." in out
    assert "cond(c_closed,X) :- kind(X,k_capability_proposal), attr(X,t_status,V), vals(" in out


def test_the_values_a_means_reads(vocab):
    assert spec_logic.means_values(vocab, "c_open") == ([], ["v_done", "v_abandoned"])


def test_the_program_puts_the_background_first():
    text = spec_logic.program([{"always": ["p."], "dynamic": [], "initial": []}])
    assert text.index("#program always.") < text.index("p.")
    assert "active(X) :- does(_,E,X), start_event(E)." in text


def test_every_corpus_line_translates_into_one_program_that_has_a_model(vocab):
    import spec_solve
    voc = spec_logic.Vocab(spec_lexicon.read(GLOSSARY))
    trees = []
    for path in sorted((REPO / "grammar" / "corpus").glob("*.txt")):
        for line in path.read_text().splitlines():
            if line.strip() and not line.startswith("#") and path.name != "refused.txt":
                trees.append(tree(line.split("] ", 1)[-1] if line.startswith("[U") else line, GLOSSARY))
    parts = [spec_logic.facts(voc)] + [spec_logic.translate(voc, "c#r%d" % n, t) for n, t in enumerate(trees)]
    ctl = spec_solve._ground(spec_logic.program(parts + [spec_logic.witness(voc, "c#g1", trees[:1])]))
    assert len(trees) > 150 and spec_solve._core(ctl) is None
