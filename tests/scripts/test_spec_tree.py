"""spec_tree: the post-parse guards (design §9.3, §9.4), normalised trees and logic_only (§14.2), on trees as
nested tuples (fun, *args) with literals as plain values."""
import spec_tree

WORDS = {"`drafted`", "`work run`", "initiative"}
WORK = ("ActorSubj", ("a_work",))
RUN = ("ActorSubj", ("a_work_run",))


def shall(subject, *vps):
    """`subject shall vp1, vp2 and vpn` as one response of a Resps."""
    tree = ("OneVP", vps[-1])
    for vp in reversed(vps[:-1]):
        tree = ("AndVP", vp, tree)
    return ("OneResp", ("Shall", subject, tree))


def ubiq(*vps):
    return ("Ubiq", shall(("ActorSubj", ("a_work_run",)), *vps))


def values(*vs):
    tree = ("t_status_One", (vs[-1],))
    for v in reversed(vs[:-1]):
        tree = ("t_status_More", (v,), tree)
    return tree


def test_a_value_list_with_a_repeat_is_refused():
    cn = ("t_status_WhoseNot", ("k_initiative",), values("v_done", "v_abandoned", "v_done"))
    tree = ubiq(("Do", ("e_start",), ("k_initiative_toNP", ("k_initiative_Every", cn))))
    assert "v_done" in spec_tree.guard(tree, WORDS)
    ok = ubiq(("Do", ("e_start",), ("k_initiative_toNP", ("k_initiative_Every", ("t_status_WhoseNot", (
        "k_initiative",), values("v_done", "v_abandoned"))))))
    assert spec_tree.guard(ok, WORDS) is None


def test_a_repeated_member_of_a_printed_list_is_refused():
    item = ("CodeNP", ("CodeLit", "`a`"))
    tree = ubiq(("Print", ("MoreNP", item, ("OneNP", item))))
    assert "repeat" in spec_tree.guard(tree, WORDS)


def test_it_needs_an_earlier_noun_phrase_of_its_kind():
    it = ("k_initiative_toNP", ("k_initiative_It",))
    dangling = ubiq(("Do", ("e_start",), it))
    assert "it" in spec_tree.guard(dangling, WORDS)
    other = ("When", ("Happens", ("NPSubj", ("k_session_toNP", ("k_session_An", ("k_session",)))), ("e_end",),
                      ("k_stage_toNP", ("k_stage_An", ("k_stage",)))), shall(WORK, ("Do", ("e_start",), it)))
    assert spec_tree.guard(other, WORDS)
    kept = ("When", ("Runs", ("ActorSubj", ("a_the_person",)), ("CmdCode", ("CodeLit", "`work start`"))), shall(
        WORK, ("Do", ("e_start",), ("k_initiative_toNP", ("k_initiative_An", ("k_initiative",))))))
    assert spec_tree.guard(kept, WORDS) is None
    anaphor = ("When", ("Happens", ("ActorSubj", ("a_the_person",)), ("e_start",),
                        ("k_initiative_toNP", ("k_initiative_An", ("k_initiative",)))), shall(WORK, (
                            "Do", ("e_end",), it)))
    assert spec_tree.guard(anaphor, WORDS) is None


def test_a_code_literal_must_be_backticked_and_not_a_lexicon_word():
    def code(token):
        return ubiq(("Print", ("OneNP", ("CodeNP", ("CodeLit", token)))))
    assert spec_tree.guard(code("`spec/index.md`"), WORDS) is None
    assert "lexicon" in spec_tree.guard(code("`drafted`"), WORDS)
    assert "backtick" in spec_tree.guard(code("plain"), WORDS)
    quoted = ubiq(("Print", ("OneNP", ("QuotedNP", ("QuotedLit", "plain")))))
    assert "quote" in spec_tree.guard(quoted, WORDS)
    assert spec_tree.guard(ubiq(("Print", ("OneNP", ("QuotedNP", ("QuotedLit", '"no initiative"'))))), WORDS) is None


def test_a_recipient_after_its_object_passes_the_guards():
    interpreter = ("k_interpreter_toNP", ("k_interpreter_The", ("k_interpreter",)))
    brief = ("k_brief_toNP", ("k_brief_An", ("k_brief",)))
    assert spec_tree.guard(ubiq(("DoTo", ("e_give",), ("Only", brief), interpreter)), WORDS) is None


def test_normal_sorts_value_lists_and_conjunctions():
    a = ("k_initiative_toNP", ("k_initiative_Every", ("t_status_WhoseNot", ("k_initiative",),
                                                    values("v_done", "v_abandoned"))))
    b = ("k_initiative_toNP", ("k_initiative_Every", ("t_status_WhoseNot", ("k_initiative",),
                                                    values("v_abandoned", "v_done"))))
    assert a != b and spec_tree.normal(a) == spec_tree.normal(b)
    free = ("IsFree", ("s_spec_lock",))
    holds = ("Holds", ("k_session_toNP", ("k_session_An", ("k_session",))), ("s_merge_lock",))
    c1 = ("CondAnd", free, ("CondOne", holds))
    c2 = ("CondAnd", holds, ("CondOne", free))
    assert spec_tree.normal(c1) == spec_tree.normal(c2)
    assert spec_tree.normal(("CondOr", free, ("CondOne", holds))) == spec_tree.normal(("CondOr", holds, (
        "CondOne", free)))


def test_normal_keeps_the_order_of_a_list_mixing_and_with_or():
    a, b, c = (("IsFree", ("s_%s" % x,)) for x in "cba")
    mixed = ("CondAnd", a, ("CondOr", b, ("CondOne", c)))
    assert spec_tree.normal(mixed) == ("CondAnd", a, ("CondOr", c, ("CondOne", b)))


def test_a_step_saying_a_relation_between_two_instances_is_kept_as_its_rows_clause():
    """A relation step is the SAtom of its row's clause (design-r2 §4.4): no guard drops it."""
    inst = ("k_stage_Inst", ("NameLit", "s1")), ("k_work_item_Inst", ("NameLit", "w1"))
    assert spec_tree.guard(("SAtom", ("rel_stage_for_work_item_Atom",) + inst), WORDS) is None


def test_parts_split_a_requirement_into_its_clauses():
    trig = ("IsRun", ("CmdCode", ("CodeLit", "`tools size`")))
    resp = shall(WORK, ("ExitOk",))
    assert spec_tree.parts(("When", trig, resp)) == {"feat": None, "cond": None, "trig": trig,
                                                     "resp": [("Shall", WORK, ("ExitOk",))]}
    cond = ("CondOne", ("IsFree", ("s_spec_lock",)))
    assert spec_tree.parts(("WhileIf", cond, trig, resp))["cond"] == cond
    assert spec_tree.parts(("Ubiq", resp))["trig"] is None


def test_parts_give_two_conjuncts_for_shall_a_and_b():
    commit = ("Do", ("e_commit",), ("k_transition_toNP", ("k_transition_Every", ("k_transition",))))
    push = ("Do", ("e_push",), ("k_commit_toNP", ("k_commit_The", ("k_commit",))))
    assert spec_tree.parts(ubiq(commit, push))["resp"] == [("Shall", RUN, commit), ("Shall", RUN, push)]


def test_parts_give_each_response_and_each_forbidden_verb_phrase_in_spoken_order():
    merge, push = ("Do", ("e_merge",), ("CodeNP", ("CodeLit", "`a`"))), ("Do", ("e_push",), ("CodeNP", (
        "CodeLit", "`b`")))
    forbid = ("ShallNot", RUN, ("OrVP", merge, ("OneVPor", push)))
    resps = ("AndResp", forbid, shall(WORK, ("ExitOk",)))
    assert spec_tree.parts(("Ubiq", resps))["resp"] == [
        ("ShallNot", RUN, merge), ("ShallNot", RUN, push), ("Shall", WORK, ("ExitOk",))]


def test_logic_only_is_a_group_of_ubiquitous_resource_statements():
    hold = ubiq(("Hold", ("s_spec_lock",)))
    most = ubiq(("HoldAtMost", ("CountCode", ("CodeLit", "`workers`")), ("s_worker_slot",)))
    other = ("When", ("IsRun", ("CmdCode", ("CodeLit", "`work run`"))), shall(WORK, ("Hold", ("s_spec_lock",))))
    assert spec_tree.logic_only([hold, most])
    assert spec_tree.logic_only([ubiq(("Hold", ("s_spec_lock",)), ("HoldA", ("s_worker_slot",)))])
    assert not spec_tree.logic_only([ubiq(("Hold", ("s_spec_lock",)), ("ExitOk",))])
    assert not spec_tree.logic_only([hold, other])
    assert not spec_tree.logic_only([ubiq(("ExitOk",))])
    assert not spec_tree.logic_only([])


def test_show_writes_a_tree_as_gf_does():
    tree = ubiq(("Print", ("OneNP", ("CodeNP", ("CodeLit", '`a "b"`')))))
    assert spec_tree.show(tree) == ('Ubiq (OneResp (Shall (ActorSubj a_work_run) (OneVP (Print (OneNP (CodeNP '
                                    '(CodeLit "`a \\"b\\"`")))))))')
