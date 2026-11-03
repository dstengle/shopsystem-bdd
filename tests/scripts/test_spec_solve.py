"""spec_solve: `model logic`'s checks L1–L4 on spec_engine (design-r2 §6.4), on the cluster fixture for fixed ids and
on the live spec for the seeded conflict, which names no id of it."""
import json
import pathlib
import re
import shutil
import sys

import pytest
import spec_grammar
import spec_read
import spec_solve
import spec_tree

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
CLUSTER = REPO / "tests" / "scripts" / "fixtures" / "logic" / "cluster"
SUPERVISION = "spec/capabilities/supervision.md"


@pytest.fixture(scope="module")
def findings():
    toolchain.require()
    return spec_solve.run(CLUSTER)


def of(findings, code):
    return [f for f in findings if f.code == code]


def copy(tmp_path, root=CLUSTER, path=SUPERVISION, add=""):
    """The spec at `root` copied, with `add` appended to the end of one capability's Behaviour."""
    out = tmp_path / "copy"
    shutil.copytree(root / "spec", out / "spec")
    target = out / path
    text = target.read_text()
    start = text.index("\n## Behaviour")
    end = text.find("\n## ", start + 1)
    end = len(text) if end < 0 else end
    target.write_text(text[:end].rstrip() + "\n\n" + add + text[end:])
    return out


def test_the_restatements_of_r66_and_r95_are_an_l2_duplicate(findings):
    [dup] = of(findings, "L2")
    assert dup.ids == ["supervision#r3", "supervision#r4"]


def test_two_statements_saying_opposite_things_of_one_trigger_are_an_l1_naming_both(findings):
    l1 = {f.ids[0]: f for f in of(findings, "L1")}
    assert set(l1) == {"supervision#g11", "supervision#g12"}
    assert l1["supervision#g11"].ids == ["supervision#g11", "supervision#r11", "supervision#r12"]
    assert l1["supervision#g11"].text == "supervision#g11 (r11) cannot happen: conflicts with supervision#r12"


def test_the_resource_formulation_has_no_l1(findings):
    named = {i for f in of(findings, "L1") for i in f.ids}
    assert not named & {"supervision#r2", "supervision#r5", "supervision#r6", "supervision#r7", "supervision#r8",
                        "U1", "U2"}


def test_a_set_off_the_transition_table_is_l3_through_its_guard(findings):
    [l3] = of(findings, "L3")
    assert l3.ids == ["supervision#g9", "supervision#r9", "T:status@initiative"]
    assert l3.text == ("supervision#r9 sets the status of an initiative from `proposed` to `abandoned`, which no "
                       "transition allows")


def test_a_pre_state_value_no_transition_path_reaches_is_l4_asked_of_the_solver(findings, monkeypatch):
    [l4] = of(findings, "L4")
    assert l4.ids == ["supervision#g10"]
    assert "`awaiting-asker`" in l4.text
    asked = []
    real = spec_solve.reachable
    monkeypatch.setattr(spec_solve, "reachable", lambda *a: asked.append(a[1:]) or real(*a))
    spec_solve.run(CLUSTER, "supervision", groups=["supervision#g10"])
    assert [a[1] for a in asked] == ["v_awaiting_asker"]


def test_a_group_that_contradicts_itself_is_l1_with_no_other_id(tmp_path):
    root = copy(tmp_path, add=(
        "### [g13] a proposed initiative started and done at once\n"
        "- [r13] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status "
        "to `started` and set its status to `done`.\n"))
    [l1] = of(spec_solve.run(root, "supervision", groups=["supervision#g13"]), "L1")
    assert l1.ids == ["supervision#g13", "supervision#r13"]
    assert l1.text.endswith("it contradicts itself")


def test_an_unsat_core_is_confirmed_at_its_own_horizon_bound(tmp_path, monkeypatch):
    """r20 lengthens g11's cone (g11 -> r20 -> r6: imax 4), but its core r11, r12 is one step from the witness
    (imax 3): the core's confirmation, whose pools grow with imax, is solved at the core's bound."""
    root = copy(tmp_path, add=(
        "### [g20] `work start` starts an integrate round\n"
        "- [r20] When the person runs `work start` on an initiative that is `proposed`, `work run` shall start an "
        "integrate round.\n"))
    calls, real = [], spec_solve.spec_engine.solve
    monkeypatch.setattr(spec_solve.spec_engine, "solve", lambda t, on, imax, *a, **k: calls.append(
        (sorted(i for i in on if not i.startswith("T:")), imax)) or real(t, on, imax, *a, **k))
    [l1] = of(spec_solve.run(root, "supervision", groups=["supervision#g11"]), "L1")
    assert l1.ids == ["supervision#g11", "supervision#r11", "supervision#r12"]
    assert calls[0][1] == 4 and "supervision#r20" in calls[0][0]
    assert calls[1] == (["supervision#r11", "supervision#r12"], 3)


def test_a_capability_and_groups_name_what_is_checked(findings):
    assert spec_solve.run(CLUSTER, "supervision") == findings
    assert spec_solve.run(CLUSTER, "no-such-capability") == []
    assert of(spec_solve.run(CLUSTER, "supervision", groups=["supervision#g11"]), "L1")[0].ids[0] == \
        "supervision#g11"


def test_extra_drafted_files_are_checked_with_the_spec(tmp_path):
    draft = tmp_path / "drafts" / "pacing.md"
    draft.parent.mkdir()
    draft.write_text("---\nid: capability/x/pacing\nlanguage: codified-1\n---\n\n# Pacing\n\n## Behaviour\n\n"
                     "### [g1] proposed initiatives stay proposed\n"
                     "- [r1] When the person runs `work start` on an initiative that is `proposed`, `work` shall not "
                     "set its status to `started`.\n")
    found = spec_solve.run(CLUSTER, extra=[draft])
    assert "pacing#g1" in {f.ids[0] for f in of(found, "L1")}
    assert {f.ids[0] for f in of(spec_solve.run(CLUSTER, "pacing", extra=[draft]), "L1")} == {"pacing#g1"}


def test_the_text_report_lists_each_finding_and_exits_1_on_l1_or_l3(findings):
    text, code = spec_solve.report(findings, False)
    assert code == 1
    lines = text.splitlines()
    assert any(line.startswith("L1 supervision#g11 ") for line in lines)
    assert lines[-1] == "5 findings: 2 L1, 1 L2, 1 L3, 1 L4"


def test_warnings_alone_exit_0():
    text, code = spec_solve.report([spec_solve.Finding("L2", ["a#r1", "a#r2"], "a#r1 and a#r2 say the same")], False)
    assert code == 0 and text.splitlines()[-1] == "1 finding: 1 L2"
    assert spec_solve.report([], False) == ("no findings", 0)


def test_the_json_report_is_one_object(findings):
    text, code = spec_solve.report(findings, True)
    data = json.loads(text)
    assert code == 1 and data["exit"] == 1
    assert {"code": "L4", "ids": ["supervision#g10"], "text": of(findings, "L4")[0].text} in data["findings"]


def test_no_copied_loop_fixed_horizon_or_tree_walk():
    text = (REPO / "scripts" / "spec_solve.py").read_text()
    assert not re.search(r"HORIZON = |def _ground|_reachable|def _edges", text)


def _seed():
    """The first service group of the live spec whose program is SAT, whose statement is `When T, S shall V…` and
    whose trigger no other statement of its capability has (so the core can name only it and the seed):
    (capability, its requirement id, the contradicting line)."""
    for path in sorted((REPO / "spec" / "capabilities").glob("*.md")):
        cap = spec_read.capability(path) if spec_read.codified(path) else None
        if not cap or cap.frontmatter.get("group") != "service":
            continue
        trees = {r.id: spec_grammar.parse(REPO, r.text).tree for g in cap.groups for r in g.requirements}
        triggers = [spec_tree.parts(x)["trig"] for x in trees.values() if x]
        for g in cap.groups:
            parsed = [trees[r.id] for r in g.requirements]
            if len(parsed) != 1 or not parsed[0] or parsed[0][0] != "When" or triggers.count(parsed[0][1]) > 1:
                continue
            tree = parsed[0]
            resps = tree[2]
            if resps[0] != "OneResp" or resps[1][0] != "Shall":
                continue
            vp = resps[1][2][1]
            if of(spec_solve.run(REPO, cap.name, groups=["%s#%s" % (cap.name, g.id)]), "L1"):
                continue
            seeded = ("When", tree[1], ("OneResp", ("ShallNot", resps[1][1], ("OneVPor", vp))))
            return cap, g.requirements[0].id, spec_grammar.linearise(REPO, seeded)
    raise AssertionError("no service group to seed a conflict on")


def test_seeded_conflict(tmp_path):
    """A requirement contradicting a live one, built from the live spec, gives an L1 whose core names both ids."""
    toolchain.require()
    cap, rid, line = _seed()
    assert spec_tree.parts(spec_grammar.parse(REPO, line).tree)["resp"][0][0] == "ShallNot"
    numbers = [int(r.id[1:]) for g in cap.groups for r in g.requirements] + [int(i[1:]) for i in cap.retired]
    gnum = max(int(g.id[1:]) for g in cap.groups) + 1
    new = "r%d" % (max(numbers) + 1)
    root = copy(tmp_path, REPO, "spec/capabilities/%s.md" % cap.name,
                "### [g%d] the seeded conflict\n- [%s] %s\n" % (gnum, new, line))
    found = of(spec_solve.run(root, cap.name, groups=["%s#g%d" % (cap.name, gnum)]), "L1")
    assert len(found) == 1
    assert {"%s#%s" % (cap.name, rid), "%s#%s" % (cap.name, new)} <= set(found[0].ids)
