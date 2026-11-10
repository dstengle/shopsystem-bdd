"""grammar/check.lp (design-r3 §6): the fixed meta-encoding over a context's facts. Conflicts are witnesses found by
one brave solve over the candidate pairs; lifecycle (L3) and reachability (L4) are graph rules; L5 lints an
untriggered positive event obligation. The facts are inline, in the schema of design-r3 §3, so this file runs clingo
directly and reads no tree. The requirements are the research example's (`solver-research.md`), rewritten."""
import pathlib
import time

import clingo

CHECK = pathlib.Path(__file__).resolve().parents[2] / "grammar" / "check.lp"

DOM = """kind(k_work_item). kind(k_initiative). kind(k_stage). kind(k_research_stage). kind(k_delegation).
sub(k_research_stage,k_stage). actor(a_person). actor(a_work_run).
val(k_work_item,t_status,v_drafted). val(k_work_item,t_status,v_researched). val(k_work_item,t_status,v_ready).
val(k_work_item,t_status,v_awaiting_answer). val(k_work_item,t_status,v_done). val(k_work_item,t_status,v_orphan).
trans(k_work_item,t_status,v_drafted,v_researched). trans(k_work_item,t_status,v_researched,v_ready).
trans(k_work_item,t_status,v_ready,v_awaiting_answer). trans(k_work_item,t_status,v_awaiting_answer,v_ready).
trans(k_work_item,t_status,v_ready,v_done). initial(k_work_item,t_status,v_drafted).
"""
RUN = 'trig("{r}",ran,"`work run`",a_person,v2). role("{r}",v2,k_initiative). role("{r}",v1,k_work_item). '


def req(r, body, form="while_when"):
    return RUN.format(r=r) + 'form("%s",%s). ' % (r, form) + body.replace("R,", '"%s",' % r) + "\n"


# supervision r2: While a work-item is drafted, when the person runs `work run` on an initiative, `work run` shall
# start a research stage for the work-item.
R2 = req("r2", "role(R,v3,k_stage). cond(R,v1,t_status,v_drafted,pos). resp(R,1,pos,e_start,a_work_run,v3). "
               "oattr(R,v3,t_kind,v_research). orel(R,r_for,v3,v1).")
R3 = req("r3", "role(R,v3,k_stage). cond(R,v1,t_status,v_researched,pos). resp(R,1,pos,e_start,a_work_run,v3). "
               "oattr(R,v3,t_kind,v_plan). orel(R,r_for,v3,v1).")
# r53: ... drafted ... shall not start a stage for the work-item.
R53 = req("r53", "role(R,v3,k_stage). cond(R,v1,t_status,v_drafted,pos). resp(R,1,neg,e_start,a_work_run,v3). "
                 "orel(R,r_for,v3,v1).")
R52 = req("r52", "role(R,v3,k_stage). cond(R,v1,t_status,v_awaiting_answer,pos). "
                 "resp(R,1,neg,e_start,a_work_run,v3). orel(R,r_for,v3,v1).")
# r72: While a delegation is written and a work-item is awaiting-answer, when ..., `work run` shall start an
# implement stage for the work-item.
R72 = req("r72", "role(R,v3,k_stage). role(R,v4,k_delegation). cond(R,v4,t_wording,v_written,pos). "
                 "cond(R,v1,t_status,v_awaiting_answer,pos). resp(R,1,pos,e_start,a_work_run,v3). "
                 "oattr(R,v3,t_kind,v_implement). orel(R,r_for,v3,v1).")
# r27: While a work-item is awaiting-answer and no delegation is written, ... shall not start a stage for it.
R27 = req("r27", "role(R,v3,k_stage). cond(R,v1,t_status,v_awaiting_answer,pos). "
                 "none(R,k_delegation,t_wording,v_written). resp(R,1,neg,e_start,a_work_run,v3). "
                 "orel(R,r_for,v3,v1).")
DELEGATION = R72.replace('"r72"', '"r80"')
END = ('role(R,v1,k_session). role(R,v2,k_stage). role(R,v3,k_work_item). cond(R,v2,t_kind,v_plan,pos). '
       'crel(R,r_for,v2,v3,pos). trig(R,does,e_end,v1,v2). ')
# r16: While a result is outputless, when a session ends a plan stage for a work-item, ... set its status to
# awaiting-answer. r99 (seeded): ... set its status to ready.
R16 = req("r16", END + "role(R,v4,k_result). cond(R,v4,t_output,v_outputless,pos). "
                       "set(R,1,v3,t_status,v_awaiting_answer). "
                       "resp(R,1,pos,set(t_status,v_awaiting_answer),a_work_run,v3).").replace(RUN.format(r="r16"), "")
R99 = req("r99", END + "set(R,1,v3,t_status,v_ready). resp(R,1,pos,set(t_status,v_ready),a_work_run,v3).",
          "when").replace(RUN.format(r="r99"), "")
# r98 (seeded): While a work-item is drafted, when ..., `work run` shall set its status to done.
R98 = req("r98", "cond(R,v1,t_status,v_drafted,pos). set(R,1,v1,t_status,v_done). "
                 "resp(R,1,pos,set(t_status,v_done),a_work_run,v1).")
EXAMPLE = R2 + R3 + R53 + R52 + R72 + R16 + R99 + R98


def solve(facts, extra="", warn=False, brave=True, witness=""):
    """The shown atoms of the last model of check.lp over the facts; with `witness`, its part `witness` ground on them
    with those facts (focus(A,B), focusm(A,B)) too."""
    args = (["--enum-mode=brave"] if brave else []) + ([] if warn else ["--warn=none"])
    ctl = clingo.Control(args)
    ctl.load(str(CHECK))
    ctl.add("base", [], facts + extra)
    ctl.ground([("base", [])])
    if witness:
        ctl.add("witness", [], witness)
        ctl.ground([("witness", [])])
    last = []
    ctl.solve(on_model=lambda m: last.__setitem__(slice(None), [str(s) for s in m.symbols(shown=True)]))
    return set(last)


def clashes(atoms):
    return {a for a in atoms if a.startswith("clash(")}


def test_r2_and_r53_clash_on_one_trigger():
    assert 'clash("r2","r53",pos_neg)' in solve(R2 + R53 + DOM)


def test_r52_and_r72_clash():
    assert 'clash("r52","r72",neg_pos)' in solve(R52 + R72 + DOM)


def test_a_different_status_does_not_clash():
    assert not clashes(solve(R2 + R3 + DOM))
    assert not clashes(solve(R3 + R53 + DOM))       # r53 forbids at drafted, r3 starts at researched


def test_a_restricted_prohibition_does_not_cover_a_wider_obligation():
    narrow = R53.replace('orel("r53"', 'oattr("r53",v3,t_kind,v_plan). orel("r53"')
    assert not clashes(solve(R2 + narrow + DOM))    # r2 starts a research stage, the prohibition is of a plan stage
    any_stage = R2.replace('oattr("r2",v3,t_kind,v_research). ', "")
    assert not clashes(solve(any_stage + narrow + DOM))     # a stage of any kind can meet r2 without a plan stage
    assert clashes(solve(any_stage + R53 + DOM))


def test_the_triggers_must_unify():
    on = 'cond("{r}",v2,t_status,{v},pos). '
    proposed = R2.replace("orel(", on.format(r="r2", v="v_proposed") + "orel(")
    started = R53.replace("orel(", on.format(r="r53", v="v_started") + "orel(")
    assert not clashes(solve(proposed + started + DOM))     # one initiative cannot be proposed and started
    assert clashes(solve(proposed + started.replace("v_started", "v_proposed") + DOM))


def test_two_sets_of_one_attribute_clash():
    assert 'clash("r16","r99",set)' in solve(R16 + R99 + DOM)


def test_exit_ok_and_exit_error_clash():
    ok = req("x1", 'resp(R,1,pos,exit_ok,"`work run`",none).', "when")
    err = req("x2", 'cond(R,v1,t_status,v_ready,pos). resp(R,1,pos,exit_error,"`work run`",none).')
    assert 'clash("x1","x2",exit)' in solve(ok + err + DOM)
    assert 'clash("x1","x2",exit)' in solve(ok.replace("exit_ok", "exit_error") + err.replace("exit_error", "exit_ok"))


def test_change_nothing_and_a_set_clash():
    none = req("x3", 'resp(R,1,pos,change_nothing,"`work run`",none).', "when")
    sets = req("x4", "set(R,1,v1,t_status,v_ready). resp(R,1,pos,set(t_status,v_ready),\"`work run`\",v1).")
    assert 'clash("x3","x4",change)' in solve(none + sets + DOM)
    prints = req("x4", 'resp(R,1,pos,print,"`work run`",none).')
    assert not clashes(solve(none + prints + DOM))


def test_use_and_shall_not_use_clash():
    use = 'uses("u1",a_worker,"`git`"). form("u1",ubiq). '
    assert 'clash("u1","u2",use)' in solve(use + 'nouse("u2",a_worker,"`git`"). form("u2",ubiq).')
    assert not clashes(solve(use + 'nouse("u2",a_worker,"`gh`"). form("u2",ubiq).'))
    event = 'resp("u3",1,neg,e_use,a_worker,"`git`"). form("u3",ubiq). '
    assert not clashes(solve(use + event + req("u4", 'resp(R,1,neg,e_use,a_worker,"`git`").')))


def test_an_inconsistent_own_pre_state_is_self():
    bad = req("r1", "cond(R,v1,t_status,v_ready,pos). cond(R,v1,t_status,v_ready,neg).")
    assert clashes(solve(bad + DOM)) == {'clash("r1","r1",self)'}
    two = req("r1", "cond(R,v1,t_status,v_ready,pos). cond(R,v1,t_status,v_done,pos).")
    assert clashes(solve(two + DOM)) == {'clash("r1","r1",self)'}


def test_two_sets_in_one_requirement_is_self():
    bad = req("r1", "set(R,1,v1,t_status,v_ready). set(R,2,v1,t_status,v_done).")
    assert clashes(solve(bad + DOM)) == {'clash("r1","r1",self)'}


def test_no_k_is_v_blocks_the_unification():
    assert not clashes(solve(R27 + DELEGATION + DOM))
    plain = R27.replace('none("r27",k_delegation,t_wording,v_written). ', "")
    assert 'clash("r27","r80",neg_pos)' in solve(plain + DELEGATION + DOM)    # without the exception they clash


def test_no_k_is_v_reads_a_sub_kind():
    no_stage = R2.replace("orel(", 'none("r2",k_stage,t_kind,v_old). orel(')
    old = req("r9", 'role(R,v4,k_research_stage). cond(R,v4,t_kind,v_old,pos). '
                    'resp(R,1,neg,e_start,a_work_run,v3). role(R,v3,k_stage). orel(R,r_for,v3,v1).')
    assert not clashes(solve(no_stage + old + DOM))
    assert clashes(solve(no_stage.replace("v_old)", "v_new)") + old + DOM))


WAITING = ('role("r60",v1,k_work_item). role("r60",v3,k_stage). cond("r60",v1,t_status,v_awaiting_answer,pos). '
           'resp("r60",1,neg,e_start,a_work_run,v3). orel("r60",r_for,v3,v1). form("r60",while).\n')


def test_an_untriggered_prohibition_clashes_with_a_triggered_obligation():
    start = req("r61", "role(R,v3,k_stage). cond(R,v1,t_status,v_awaiting_answer,pos). "
                       "resp(R,1,pos,e_start,a_work_run,v3). orel(R,r_for,v3,v1).")
    assert 'clash("r60","r61",neg_pos)' in solve(WAITING + start + DOM)


def test_an_untriggered_requirement_is_read_in_the_state_after_the_sets():
    moved = req("r62", "role(R,v3,k_stage). cond(R,v1,t_status,v_awaiting_answer,pos). "
                       "set(R,1,v1,t_status,v_ready). resp(R,1,pos,set(t_status,v_ready),a_work_run,v1). "
                       "resp(R,2,pos,e_start,a_work_run,v3). orel(R,r_for,v3,v1).")
    assert not clashes(solve(WAITING + moved + DOM))  # r60 applies to an awaiting work-item; r62 made it ready


def test_a_sub_kind_object_unifies():
    research = req("r70", "role(R,v3,k_research_stage). resp(R,1,pos,e_start,a_work_run,v3). "
                          "orel(R,r_for,v3,v1).", "when")
    assert 'clash("r53","r70",neg_pos)' in solve(R53 + research + DOM)


def test_disjoint_kinds_are_never_paired():
    other = R53.replace('"`work run`",a_person,v2', '"`work run`",a_person,v9').replace(
        'role("r53",v2,k_initiative)', 'role("r53",v9,k_delegation)')
    atoms = solve(R2 + other + DOM, "#show pair/2.")
    assert not any(a.startswith("pair(") for a in atoms) and not clashes(atoms)
    assert 'pair("r2","r53")' in solve(R2 + R53 + DOM, "#show pair/2.")


def test_a_pair_that_cannot_fire_hides_no_other_finding():
    atoms = solve(R27 + DELEGATION + R2 + R53 + R98 + DOM)   # r27 and r80 can never fire together
    assert 'clash("r2","r53",pos_neg)' in atoms and 'bad_set("r98",t_status,v_drafted,v_done)' in atoms


def test_a_set_with_no_transition_is_bad_set():
    assert 'bad_set("r98",t_status,v_drafted,v_done)' in solve(R98 + DOM)
    assert not any(a.startswith("bad_set") for a in solve(R16 + DOM))     # no pre-value; a transition enters it
    ok = R98.replace("v_done", "v_researched")
    assert not any(a.startswith("bad_set") for a in solve(ok + DOM))


def test_a_set_to_a_value_nothing_enters_is_bad_set():
    born = req("r97", "set(R,1,v1,t_status,v_orphan). resp(R,1,pos,set(t_status,v_orphan),a_work_run,v1).")
    assert 'bad_set("r97",t_status,none,v_orphan)' in solve(born + DOM)


def test_an_attribute_with_no_transitions_gives_no_l3_or_l4():
    free = req("r96", "cond(R,v1,t_colour,v_red,pos). set(R,1,v1,t_colour,v_blue).")
    atoms = solve(free + DOM)
    assert not any(a.startswith(("bad_set", "unreachable")) for a in atoms)


def test_an_unreached_value_is_unreachable():
    needs = req("r95", "cond(R,v1,t_status,v_orphan,pos). resp(R,1,pos,print,a_work_run,none).")
    atoms = solve(needs + DOM)
    assert 'unreachable("r95",t_status,v_orphan)' in atoms
    assert not any(a.startswith("unreachable") for a in solve(R52 + DOM))


def test_an_untriggered_event_obligation_is_linted():
    write = ('role("r10",v1,k_work_item). cond("r10",v1,t_status,v_ready,pos). '
             'resp("r10",1,pos,e_write,a_work_run,v1). form("r10",while).\n')
    assert 'lint("r10",e_write,none)' in solve(write + DOM)
    react = 'role("r6",v1,k_session). trig("r6",does,e_write,a_work_run,none). form("r6",when).\n'
    atoms = solve(write + react + DOM)
    assert 'lint("r10",e_write,"r6")' in atoms and 'lint("r10",e_write,none)' not in atoms
    assert not any(a.startswith("lint") for a in solve(R2 + R98 + DOM))    # triggered, or a set: not linted
    assert not any(a.startswith("lint") for a in solve(WAITING + DOM))      # a prohibition: not linted


def test_focus_shows_one_merged_pre_state():
    atoms = solve(R52 + R72 + DOM, brave=False, witness='focus("r52","r72").')
    pre = {a for a in atoms if a.startswith("pre(")}
    assert 'pre("r52","r72",v1,t_status,v_awaiting_answer,pos)' in pre
    assert 'pre("r52","r72",b(v4),t_wording,v_written,pos)' in pre
    assert 'clash("r52","r72",neg_pos)' in atoms
    assert not any(a.startswith("pre(") for a in solve(R52 + R72 + DOM))


def test_no_facts_no_atoms_no_warnings(capfd):
    assert solve("", warn=True) == set()
    assert capfd.readouterr().err == ""


def test_the_example_grounds_small_and_fast():
    t = time.time()
    ctl = clingo.Control(["--enum-mode=brave", "--warn=none", "--stats"])
    ctl.load(str(CHECK))
    ctl.add("base", [], EXAMPLE + DOM)
    ctl.ground([("base", [])])
    last = []
    ctl.solve(on_model=lambda m: last.__setitem__(slice(None), [str(s) for s in m.symbols(shown=True)]))
    took = time.time() - t
    assert ctl.statistics["problem"]["lp"]["rules"] < 2000 and took < 0.5
    assert clashes(set(last)) == {'clash("r2","r53",pos_neg)', 'clash("r16","r99",set)',
                                 'clash("r52","r72",neg_pos)'}
    assert 'bad_set("r98",t_status,v_drafted,v_done)' in last


def test_one_named_code_is_one_thing():
    # analysis-tools r3 and r6: r3 needs `.venv` absent, r6 present (and names it twice), so they never fire together
    probe = 'trig("{r}",ran,"`tools probe`",a_person,none). form("{r}",while_when). '
    cs = 'role("{{r}}",{v},k_python_interpreter). named("{{r}}",{v},"{c}"). '
    r3 = (probe + cs.format(v="v1", c="venv") + cs.format(v="v2", c=".venv") + 'ccond("{r}",v1,c_present,pos). '
          'ccond("{r}",v2,c_present,neg). resp("{r}",1,pos,print,a_tools,v1). ').format(r="r3")
    r6 = (probe + "".join(cs.format(v=v, c=c) for v, c in (("v1", ".venv"), ("v2", "venv"), ("v3", ".venv"))) +
          'ccond("{r}",v1,c_present,pos). ccond("{r}",v2,c_present,pos). resp("{r}",1,pos,print,a_tools,v3). '
          'resp("{r}",2,neg,print,a_tools,v2). ').format(r="r6")
    assert not clashes(solve(r3 + r6 + DOM))
    assert clashes(solve(r3.replace("c_present,neg", "c_present,pos") + r6 + DOM))


def test_an_if_requirement_is_the_exception_on_its_trigger():
    refuse = R53.replace("while_when", "while_if")
    assert not clashes(solve(R2 + refuse + DOM))                    # the unwanted-behaviour form wins over r2
    assert clashes(solve(R2.replace("while_when", "while_if") + refuse + DOM))     # two of one form still clash


def test_a_requirement_changes_nothing_but_its_own_events():
    show = 'resp(R,1,pos,change_nothing,a_skill,none). resp(R,2,pos,e_show,a_skill,"the reason"). '
    one, two = req("x5", show), req("x6", "cond(R,v1,t_status,v_ready,pos). " + show)
    assert not clashes(solve(one + two + DOM))                      # "show the reason and change nothing" twice
    writes = req("x6", 'cond(R,v1,t_status,v_ready,pos). resp(R,1,pos,e_write,a_skill,"a reason").')
    assert 'clash("x5","x6",change)' in solve(one + writes + DOM)
