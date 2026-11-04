"""grammar/check.lp's readings that keep it from reporting clashes the requirements do not have (report-checker-gaps):
a functional relation, a definite noun phrase with no antecedent, `every` and `no` over a defined condition, `no`
over a relation, and a clash that depends on a prose condition (L6, `maybe`). Each reading has its real clash of the
same shape beside it, still found. Inline facts in the schema of design-r3 §3, as test_check_lp."""
from test_check_lp import DOM, clashes, req, solve

ENDS = ('role(R,v1,k_session). role(R,v2,k_stage). role(R,v3,k_result). crel(R,r_with,v2,v3,pos). '
        'trig(R,does,e_end,v1,v2). form(R,{form}). ')
DRAFT = "role(R,v9,k_work_item). resp(R,1,{pol},e_draft,a_work_run,v9). "


def ends(r, body, pol="pos", form="while_when"):
    return (ENDS.format(form=form) + DRAFT.format(pol=pol) + body).replace("R,", '"%s",' % r) + "\n"


def maybes(atoms):
    return {a for a in atoms if a.startswith("maybe(")}


# ---- a functional relation: a stage is with one result --------------------------------------------------------
FIXING = ends("f1", "ccond(R,v3,c_fixing,pos).")
DONE = ends("f2", "cond(R,v3,t_outcome,v_done,pos).", pol="neg")
OUTCOME = "val(k_result,t_outcome,v_done). val(k_result,t_outcome,v_partial). "


def test_a_functional_relation_merges_what_it_relates_one_thing_to():
    # f2 forbids a draft on a DONE result, f3 obliges one on a PARTIAL one: one stage is with one result, so they
    # never fire together; with `with` not functional the two results stay apart and it is a clash
    partial = ends("f3", "cond(R,v3,t_outcome,v_partial,pos).")
    assert not clashes(solve(DONE + partial + OUTCOME + DOM + "fun(r_with)."))
    assert 'clash("f2","f3",neg_pos)' in solve(DONE + partial + OUTCOME + DOM)


def test_one_result_of_a_functional_relation_still_clashes():
    same = ends("f4", "cond(R,v3,t_outcome,v_done,pos).")
    assert 'clash("f2","f4",neg_pos)' in solve(DONE + same + OUTCOME + DOM + "fun(r_with).")


def test_a_clash_that_depends_on_a_prose_condition_is_a_maybe():
    atoms = solve(FIXING + DONE + OUTCOME + DOM + "fun(r_with). prose(c_fixing).")
    assert not clashes(atoms)
    assert maybes(atoms) == {'maybe("f1","f2",pos_neg,c_fixing)'}


def test_a_clash_that_does_not_depend_on_its_prose_condition_stays_a_clash():
    plain = DONE.replace('cond("f2",v3,t_outcome,v_done,pos).', 'ccond("f2",v3,c_fixing,pos).')
    atoms = solve(FIXING + plain + OUTCOME + DOM + "fun(r_with). prose(c_fixing).")
    assert 'clash("f1","f2",pos_neg)' in atoms and not maybes(atoms)       # both say fixing: nothing to decide


def test_a_prose_condition_on_an_instance_kept_apart_is_no_dependency():
    # without the functional relation the two results may be two: that witness is firm
    atoms = solve(FIXING + DONE + OUTCOME + DOM + "prose(c_fixing).")
    assert 'clash("f1","f2",pos_neg)' in atoms


# ---- a definite noun phrase with no antecedent is the one thing of its kind --------------------------------------
QUESTION = ('role(R,v5,k_question). the(R,v5). cond(R,v5,t_asking,{v},pos). ')


def asking(r, v, value):
    body = QUESTION.format(v=v) + "set(R,1,v1,t_status,%s). resp(R,1,pos,set(t_status,%s),a_work_run,v1)." % (
        value, value)
    return req(r, body)


def test_two_definites_of_one_kind_are_one_thing():
    research, plan = asking("q1", "v_research", "v_drafted"), asking("q2", "v_plan", "v_researched")
    assert not clashes(solve(research + plan + DOM))
    indefinite = plan.replace('the("q2",v5). ', "")
    assert not clashes(solve(research + indefinite + DOM))      # one definite binds the other's: still one
    loose = research.replace('the("q1",v5). ', "") + indefinite
    assert 'clash("q1","q2",set)' in solve(loose + DOM)         # two indefinites may be two questions


def test_two_definites_that_agree_still_clash():
    research, other = asking("q1", "v_research", "v_drafted"), asking("q2", "v_research", "v_researched")
    assert 'clash("q1","q2",set)' in solve(research + other + DOM)


# ---- every and no over a defined condition ------------------------------------------------------------------------
# closed: a work-item is closed when it is done or withdrawn (two ways through, each one literal)
CLOSED = ("dalt(c_closed,1). dlit(c_closed,1,t_status,v_done,pos). dalt(c_closed,2). "
          "dlit(c_closed,2,t_status,v_withdrawn,pos). ")
# a1: While every work-item of the initiative is closed, when ..., `work run` shall set the initiative to done.
ALL = req("a1", "uall(R,u1,k_work_item). urel(R,r_of,u1,v2). uccond(R,u1,c_closed,pos). "
                "set(R,1,v2,t_status,v_done). resp(R,1,pos,set(t_status,v_done),a_work_run,v2).")
OPEN = req("a2", "role(R,v3,k_work_item). crel(R,r_of,v3,v2,pos). {lit} "
                 "resp(R,1,neg,set(t_status,v_done),a_work_run,v2).")


def test_every_reads_its_restriction_universally():
    assert not clashes(solve(ALL + OPEN.format(lit='ccond("a2",v3,c_closed,neg).') + CLOSED + DOM))
    assert not clashes(solve(ALL + OPEN.format(lit='cond("a2",v3,t_status,v_ready,pos).') + CLOSED + DOM))
    outside = OPEN.format(lit='ccond("a2",v3,c_closed,neg).').replace('crel("a2",r_of,v3,v2,pos). ', "")
    assert 'clash("a1","a2",pos_neg)' in solve(ALL + outside + CLOSED + DOM)     # not of the initiative: real


def test_every_with_a_value_it_allows_still_clashes():
    done = OPEN.format(lit='cond("a2",v3,t_status,v_withdrawn,pos).')
    assert 'clash("a1","a2",pos_neg)' in solve(ALL + done + CLOSED + DOM)


NONE = req("n1", "cnone(R,k_work_item,c_open). resp(R,1,pos,exit_ok,a_work_run,none).")
OPEN_DEF = "dalt(c_open,1). dlit(c_open,1,t_status,v_done,neg). dlit(c_open,1,t_status,v_withdrawn,neg). "
WAITS = req("n2", "cond(R,v1,t_status,v_ready,pos). resp(R,1,pos,exit_error,a_work_run,none).")


def test_no_reads_a_defined_condition_through_its_definition():
    assert not clashes(solve(NONE + WAITS + OPEN_DEF + DOM))         # a ready work-item is open
    done = WAITS.replace("v_ready", "v_done")
    assert 'clash("n1","n2",exit)' in solve(NONE + done + OPEN_DEF + DOM)    # a done one is not: real


def on_item(r, body):
    """A requirement triggered by `work answer` on its work-item v1."""
    return ('trig(R,ran,"`work answer`",a_person,v1). role(R,v1,k_work_item). form(R,while_when). ' + body).replace(
        "R,", '"%s",' % r) + "\n"


def test_a_negated_defined_condition_is_read_through_its_definition():
    neg = on_item("d1", "ccond(R,v1,c_open,neg). resp(R,1,pos,exit_ok,a_work_run,none).")
    ready = on_item("d2", "cond(R,v1,t_status,v_ready,pos). resp(R,1,pos,exit_error,a_work_run,none).")
    assert not clashes(solve(neg + ready + OPEN_DEF + DOM))          # one work-item: ready, and not open
    assert 'clash("d1","d2",exit)' in solve(neg + ready.replace("v_ready", "v_done") + OPEN_DEF + DOM)


def test_a_value_every_gives_reads_a_negated_defined_condition():
    # u1: every work-item of the initiative is `done`; u2: a work-item of it is not closed. A done one is closed.
    every = req("u1", "uall(R,u1,k_work_item). urel(R,r_of,u1,v2). ucond(R,u1,t_status,v_done,pos). "
                      "set(R,1,v2,t_status,v_done). resp(R,1,pos,set(t_status,v_done),a_work_run,v2).")
    assert not clashes(solve(every + OPEN.format(lit='ccond("a2",v3,c_closed,neg).') + CLOSED + DOM))
    ready = every.replace("v_done,pos). set", "v_ready,pos). set")         # a ready one is not: real
    assert 'clash("a2","u1",neg_pos)' in solve(ready + OPEN.format(lit='ccond("a2",v3,c_closed,neg).') + CLOSED
                                               + DOM)


# ---- no over a relation (rnone) -----------------------------------------------------------------------------------
def test_no_over_a_relation_blocks_the_unification():
    alone = req("m1", 'rnone(R,r_of,kind(k_work_item),v2). resp(R,1,pos,exit_ok,a_work_run,none).')
    kept = req("m2", 'role(R,v3,k_work_item). crel(R,r_of,v1,v2,pos). resp(R,1,pos,exit_error,a_work_run,none).')
    assert not clashes(solve(alone + kept + DOM))
    loose = kept.replace('crel("m2",r_of,v1,v2,pos). ', "")
    assert 'clash("m1","m2",exit)' in solve(alone + loose + DOM)
