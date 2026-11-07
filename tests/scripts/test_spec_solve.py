"""spec_solve: `model logic` as one brave solve of the context's facts and `grammar/check.lp` (design-r3 §6), on the
cluster fixture for fixed ids and on seeded pairs, one per kind of clash. The live spec is never solved here."""
import json
import pathlib
import re
import shutil
import sys
import time

import clingo
import pytest
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
CLUSTER = REPO / "tests" / "scripts" / "fixtures" / "logic" / "cluster"
SUPERVISION = "spec/capabilities/supervision.md"
USE = "- **use** (event): Forms: uses, used. Frame: `work run` uses question.\n"


@pytest.fixture(scope="module")
def findings():
    toolchain.require()
    return spec_solve.run(CLUSTER)


def of(findings, code):
    return [f for f in findings if f.code == code]


def copy(tmp_path, root=CLUSTER, path=SUPERVISION, add="", glossary=""):
    """The spec at `root` copied, with `add` appended to the end of one capability's Behaviour and `glossary` to the
    end of the index's glossary entries."""
    out = tmp_path / "copy"
    shutil.copytree(root / "spec", out / "spec")
    target = out / path
    text = target.read_text()
    start = text.index("\n## Behaviour")
    end = text.find("\n## ", start + 1)
    end = len(text) if end < 0 else end
    target.write_text(text[:end].rstrip() + "\n\n" + add + text[end:])
    if glossary:
        index = out / "spec" / "index.md"
        index.write_text(index.read_text().replace("- **start** (event)", glossary + "- **start** (event)"))
    return out


def seeded(*lines):
    return "".join("### [g%d] seeded\n- [r%d] %s\n\n" % (20 + i, 20 + i, line) for i, line in enumerate(lines))


def test_the_restatements_of_r66_and_r95_are_an_l2_duplicate(findings):
    [dup] = of(findings, "L2")
    assert dup.ids == ["supervision#r3", "supervision#r4"]


def test_two_statements_saying_opposite_things_of_one_trigger_are_an_l1_naming_both(findings):
    [l1] = of(findings, "L1")
    assert l1.ids == ["supervision#r11", "supervision#r12"]
    assert l1.text.startswith('supervision#r11 and #r12 clash: on "the person runs `work start` on an initiative ')
    assert "with an initiative that is `proposed`" in l1.text
    assert l1.text.endswith("r11 obliges and r12 forbids `work` to set the status of an initiative to `started`")


def test_the_resource_formulation_has_no_l1(findings):
    named = {i for f in of(findings, "L1") for i in f.ids}
    assert not named & {"supervision#r2", "supervision#r5", "supervision#r6", "supervision#r7", "supervision#r8",
                        "U1", "U2"}


def test_a_set_off_the_transition_table_is_l3(findings):
    [l3] = of(findings, "L3")
    assert l3.ids == ["supervision#r9"]
    assert l3.text == ("supervision#r9 sets the status of an initiative from `proposed` to `abandoned`, which no "
                       "transition allows")


def test_a_pre_state_value_no_path_reaches_is_l4(findings):
    [l4] = of(findings, "L4")
    assert l4.ids == ["supervision#r10"]
    assert l4.text == ("supervision#r10 needs a request whose status is `awaiting-asker`, which no transition path "
                       "reaches")


def test_an_untriggered_event_obligation_is_l5(findings):
    """Holding a resource is a state, not an event: the cluster's `shall hold` lines are not linted."""
    [l5] = of(findings, "L5")
    assert l5.ids == ["supervision#r10"]
    assert l5.text == "supervision#r10 obliges `work` to write a question in every state"


def test_l5_names_the_requirement_that_reacts_to_the_event(tmp_path):
    root = copy(tmp_path, add=seeded("When `work` writes a question, `work run` shall start every research stage."))
    [l5] = of(spec_solve.run(root), "L5")
    assert l5.ids == ["supervision#r10", "supervision#r20"]
    assert l5.text.endswith("in every state; supervision#r20 reacts to it")


def test_a_requirement_that_contradicts_itself_is_l1_with_its_id_only(tmp_path):
    root = copy(tmp_path, add=seeded(
        "When the person runs `work finish` on an initiative that is `started`, `work` shall set its status to "
        "`done` and set its status to `abandoned`."))
    [l1] = [f for f in of(spec_solve.run(root), "L1") if "supervision#r20" in f.ids]
    assert l1.ids == ["supervision#r20"] and l1.text == "supervision#r20 contradicts itself"


CLOSE = "When the person runs `work close` on an initiative that is `started`, `work` shall set its status to "
SEEDED = [
    ("pos_neg", ["When the person runs `work stop` on a stage, `work run` shall end the stage.",
                 "When the person runs `work stop` on a stage, `work run` shall not end the stage."],
     "r20 obliges and r21 forbids `work run` to end a stage"),
    ("set", [CLOSE + "`done`.", CLOSE + "`abandoned`."],
     "r20 sets the status of an initiative to `done` and r21 to `abandoned`"),
    ("exit", ["When the person runs `work check`, `work` shall exit successfully.",
              "When the person runs `work check`, `work` shall exit with an error naming `work check`."],
     "r20 exits successfully and r21 with an error"),
    ("change", ["When the person runs `work peek`, `work` shall change nothing.",
                "When the person runs `work peek`, `work` shall write a question."],
     "r20 changes nothing and r21 obliges `work` to write a question"),
    ("use", ["`work run` shall use a question.", "`work run` shall not use a question."],
     "r20 obliges and r21 forbids `work run` to use a question"),
]


@pytest.mark.parametrize("why, lines, phrase", SEEDED, ids=[s[0] for s in SEEDED])
def test_a_seeded_pair_is_an_l1_naming_both(tmp_path, why, lines, phrase):
    root = copy(tmp_path, add=seeded(*lines), glossary=USE if why == "use" else "")
    found = [f for f in of(spec_solve.run(root), "L1") if "supervision#r20" in f.ids]
    assert [f.ids for f in found] == [["supervision#r20", "supervision#r21"]]
    assert found[0].text.startswith("supervision#r20 and #r21 clash: ")
    assert found[0].text.endswith(phrase)


def test_no_k_is_v_in_a_condition_does_not_clash(tmp_path):
    root = copy(tmp_path, add=seeded(
        "While an initiative is `proposed` and no request is `open`, when the person runs `work ask` on a request, "
        "`work` shall write a question.",
        "While a request is `open`, when the person runs `work ask` on the request, `work` shall not write a "
        "question."))
    assert not [f for f in of(spec_solve.run(root), "L1") if "supervision#r20" in f.ids]


def test_a_capability_names_what_is_reported(findings):
    assert spec_solve.run(CLUSTER, "supervision") == findings
    assert spec_solve.run(CLUSTER, "no-such") == []


def _draft(tmp_path, name, body):
    draft = tmp_path / "drafts" / ("%s.md" % name)
    draft.parent.mkdir(exist_ok=True)
    draft.write_text(body)
    return draft


PACING = ("---\nid: capability/x/pacing\nlanguage: codified-1\n---\n\n# Pacing\n\n## Behaviour\n\n"
          "### [g1] proposed initiatives stay proposed\n"
          "- [r1] When the person runs `work start` on an initiative that is `proposed`, `work` shall not "
          "set its status to `started`.\n")


def test_extra_drafted_files_are_checked_with_the_spec(tmp_path):
    draft = _draft(tmp_path, "pacing", PACING)
    found = [f for f in of(spec_solve.run(CLUSTER, extra=[draft]), "L1") if "pacing#r1" in f.ids]
    assert [f.ids for f in found] == [["pacing#r1", "supervision#r11"]]
    assert found[0].text.startswith("pacing#r1 and supervision#r11 clash: ")
    assert [f.ids for f in of(spec_solve.run(CLUSTER, "pacing", extra=[draft]), "L1")] == [["pacing#r1",
                                                                                          "supervision#r11"]]


def test_a_draft_of_a_live_capability_replaces_it(tmp_path, findings):
    draft = _draft(tmp_path, "supervision", (CLUSTER / SUPERVISION).read_text())
    assert spec_solve.run(CLUSTER, extra=[draft]) == findings


def test_a_context_with_nothing_codified_has_no_findings(tmp_path):
    empty = tmp_path / "empty"
    (empty / "spec" / "capabilities").mkdir(parents=True)
    shutil.copy(CLUSTER / "spec" / "index.md", empty / "spec" / "index.md")
    assert spec_solve.report(spec_solve.run(empty), False) == ("no findings", 0)


PIGEONHOLE_12 = "p(1..13). h(1..12). 1 { at(P,H) : h(H) } 1 :- p(P). :- at(P,H), at(Q,H), P < Q."


def test_a_solve_past_its_limit_is_partial():
    atoms, done = spec_solve.solve(PIGEONHOLE_12, 0.2)
    assert done is False
    atoms, done = spec_solve.solve("a. #show a/0.", 1.0)
    assert done is True and atoms == ["a"]


def test_l0_is_an_error_and_its_report_exits_1(monkeypatch):
    monkeypatch.setattr(spec_solve, "_solve", lambda ctl, limit, brave=True, focus=None: ([], False))
    found = spec_solve.run(CLUSTER)
    [l0] = of(found, "L0")
    assert l0.ids == [] and l0.text == "the check did not finish in 20 s; the findings so far are listed"
    assert "L0" in spec_solve.ERRORS and spec_solve.report([l0], False)[1] == 1


def test_the_whole_context_is_one_grounding(monkeypatch, findings):
    """One brave solve finds every finding; each L1's witness is a focused solve of that same grounding, its pair's
    external `focus` set true (S12: a grounding a witness made the live check 4 s)."""
    built, real = [], clingo.Control
    monkeypatch.setattr(spec_solve.clingo, "Control", lambda *a, **k: built.append(a) or real(*a, **k))
    assert spec_solve.run(CLUSTER) == findings
    assert of(findings, "L1") and len(built) == 1


def test_the_cluster_is_checked_in_under_a_second(findings):
    start = time.perf_counter()
    spec_solve.run(CLUSTER)
    assert time.perf_counter() - start < 1.0


def test_the_text_report_lists_each_finding_and_exits_1_on_l1_or_l3(findings):
    text, code = spec_solve.report(findings, False)
    assert code == 1
    lines = text.splitlines()
    assert any(line.startswith("L1 supervision#r11 ") for line in lines)
    assert lines[-1] == "5 findings: 1 L1, 1 L2, 1 L3, 1 L4, 1 L5"


def test_warnings_alone_exit_0():
    text, code = spec_solve.report([spec_solve.Finding("L2", ["a#r1", "a#r2"], "a#r1 and a#r2 say the same")], False)
    assert code == 0 and text.splitlines()[-1] == "1 finding: 1 L2"
    assert spec_solve.report([], False) == ("no findings", 0)


def test_the_json_report_is_one_object(findings):
    text, code = spec_solve.report(findings, True)
    data = json.loads(text)
    assert code == 1 and data["exit"] == 1
    assert {"code": "L4", "ids": ["supervision#r10"], "text": of(findings, "L4")[0].text} in data["findings"]


def test_the_findings_are_sorted_by_code_then_requirement(findings):
    assert [f.code for f in findings] == ["L1", "L2", "L3", "L4", "L5"]


def test_no_telingo_cone_pool_or_horizon():
    text = (REPO / "scripts" / "spec_solve.py").read_text()
    assert not re.search(r"telingo|spec_engine|spec_logic|spec_trace|cone|pool|horizon|HORIZON", text)
    assert len(text.splitlines()) <= 200


ODD = "- **odd** (condition of result): a result nobody reads.\n"
ENDS = "When a session ends a stage with a result that is {}, `work run` shall not write a question."


def test_a_clash_that_depends_on_a_prose_condition_is_an_l6_naming_it(tmp_path):
    first = "While a result is odd, when a session ends a stage with the result, `work run` shall write a question."
    root = copy(tmp_path, add=seeded(first, ENDS.format("not outputless")), glossary=ODD)
    found = [f for f in spec_solve.run(root) if "supervision#r20" in f.ids]
    assert [(f.code, f.ids) for f in found] == [("L6", ["supervision#r20", "supervision#r21"])]
    assert found[0].text.startswith("supervision#r20 and #r21: possible clash, depends on the prose condition odd; "
                                    "define it in the controlled language to decide: ")
    assert "a result that is odd and not outputless" in found[0].text and spec_solve.report(found, False)[1] == 0
    root = copy(tmp_path / "real", add=seeded(first, ENDS.format("odd")), glossary=ODD)
    assert [f.code for f in spec_solve.run(root) if "supervision#r20" in f.ids] == ["L1"]   # both say odd: firm
