"""spec_solve: `model logic`'s checks L1–L4 on the spike's cluster codified (design §12.3), and its report."""
import json
import pathlib
import shutil
import sys
import time

import pytest
import spec_solve

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


def copy(tmp_path, drop=(), add=""):
    """The cluster copied, with the named groups' headings and statements left out and `add` appended."""
    root = tmp_path / "cluster"
    shutil.copytree(CLUSTER, root)
    path = root / SUPERVISION
    out, skip = [], False
    for line in path.read_text().splitlines():
        if line.startswith(("### ", "## ")):
            skip = any(line.startswith("### [%s] " % g) for g in drop)
        if not skip:
            out.append(line)
    text = "\n".join(out) + "\n"
    path.write_text(text.replace("## Dropped", add + "\n## Dropped"))
    return root


def test_the_restatements_of_r66_and_r95_are_an_l2_duplicate(findings):
    [dup] = of(findings, "L2")
    assert dup.ids == ["supervision#r3", "supervision#r4"]
    assert "supervision#r3" in dup.text and "supervision#r4" in dup.text


def test_one_stage_at_a_time_against_research_stages_together_is_an_l1_naming_both(findings):
    [l1] = of(findings, "L1")
    assert l1.ids[0] == "supervision#g5"
    assert "supervision#r5" in l1.ids and "supervision#r2" in l1.ids
    assert "U2" in l1.ids
    assert l1.text.startswith("supervision#g5 (r5) cannot happen: conflicts with ")
    assert "supervision#r2" in l1.text


def test_the_resource_formulation_has_no_l1(findings, tmp_path):
    named = {i for f in of(findings, "L1") for i in f.ids}
    assert not named & {"supervision#g6", "supervision#g7", "supervision#g8", "supervision#r6", "supervision#r7",
                        "supervision#r8"}
    assert of(spec_solve.run(copy(tmp_path, drop=("g2",))), "L1") == []


def test_a_set_off_the_transition_table_is_l3(findings):
    [l3] = of(findings, "L3")
    assert l3.ids == ["supervision#r9"]
    assert "`proposed`" in l3.text and "`abandoned`" in l3.text


def test_a_pre_state_value_no_transition_path_reaches_is_l4(findings):
    [l4] = of(findings, "L4")
    assert l4.ids == ["supervision#g10"]
    assert "`awaiting-asker`" in l4.text


def test_a_group_that_contradicts_itself_is_l1_with_no_other_id(tmp_path):
    root = copy(tmp_path, drop=("g2",), add=(
        "### [g12] a proposed initiative started twice over\n"
        "- [r12] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status "
        "to `started`.\n"
        "- [r13] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status "
        "to `done`.\n"))
    [l1] = [f for f in of(spec_solve.run(root), "L1") if f.ids[0] == "supervision#g12"]
    assert l1.ids == ["supervision#g12", "supervision#r12", "supervision#r13"]
    assert "contradicts itself" in l1.text


def test_a_capability_names_the_groups_checked(findings):
    assert spec_solve.run(CLUSTER, "supervision") == findings
    assert spec_solve.run(CLUSTER, "no-such-capability") == []


def test_extra_drafted_files_are_checked_with_the_spec(tmp_path):
    draft = tmp_path / "drafts" / "pacing.md"
    draft.parent.mkdir()
    draft.write_text("---\nid: capability/x/pacing\nlanguage: codified-1\n---\n\n# Pacing\n\n## Behaviour\n\n"
                     "### [g1] plan stages start together\n"
                     "- [r1] While plan stages for an initiative are `waiting`, when the person runs `work run`, "
                     "`work run` shall start every plan stage for the initiative.\n")
    found = spec_solve.run(CLUSTER, extra=[draft])
    assert {f.ids[0] for f in of(found, "L1")} == {"supervision#g5", "pacing#g1"}
    assert {f.ids[0] for f in of(spec_solve.run(CLUSTER, "pacing", extra=[draft]), "L1")} == {"pacing#g1"}


def test_the_text_report_lists_each_finding_and_exits_1_on_l1_or_l3(findings):
    text, code = spec_solve.report(findings, False)
    assert code == 1
    lines = text.splitlines()
    assert any(line.startswith("L1 supervision#g5 ") for line in lines)
    assert lines[-1] == "4 findings: 1 L1, 1 L2, 1 L3, 1 L4"


def test_warnings_alone_exit_0():
    text, code = spec_solve.report([spec_solve.Finding("L2", ["a#r1", "a#r2"], "a#r1 and a#r2 say the same")], False)
    assert code == 0 and text.splitlines()[-1] == "1 finding: 1 L2"
    assert spec_solve.report([], False) == ("no findings", 0)


def test_the_json_report_is_one_object(findings):
    text, code = spec_solve.report(findings, True)
    data = json.loads(text)
    assert code == 1 and data["exit"] == 1
    assert {"code": "L4", "ids": ["supervision#g10"], "text": of(findings, "L4")[0].text} in data["findings"]


def test_forty_groups_finish_in_under_ten_seconds(tmp_path):
    toolchain.require()
    groups = []
    for n in range(1, 41):
        line = [
            ("When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to "
             "`started`."),
            "When `work run` starts an integrate round, the round shall hold the spec lock.",
            "While a request is `accepted`, `work` shall write a question.",
            "Every research stage shall hold a worker slot.",
            "When the person runs `work run`, `work run` shall take every open initiative.",
        ][n % 5]
        groups.append("### [g%d] group %d\n- [r%d] %s\n" % (n + 20, n, n + 20, line))
    root = copy(tmp_path, drop=("g2",), add="\n".join(groups))
    start = time.monotonic()
    found = spec_solve.run(root)
    assert time.monotonic() - start < 10
    assert of(found, "L1") == []
