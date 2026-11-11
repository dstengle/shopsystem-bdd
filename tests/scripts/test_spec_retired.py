"""The capabilities retired in plugin 0.31.0 (workflow simplification plan 9, D3; design-decision/the-old-workflow-retired):
each keeps its file with no group, lists in `retired:` every id it had before the retirement, carries the notice in
its Purpose, and leaves no 0.29 id of its own missing or pending in `model restates`."""
import pathlib
import re
import subprocess

import model_restates
import pytest
import spec_read

REPO = pathlib.Path(__file__).resolve().parents[2]
BEFORE = "19e9fee5"
NOTICE = "**Retired in plugin 0.31.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired)"
RETIRED = ("code-research", "delivery", "formulation", "planning", "red-green", "review", "role-boundaries",
           "spec-consistency", "spec-integration", "spec-migration")


def path(cap):
    return REPO / "spec" / "capabilities" / f"{cap}.md"


def ids_before(cap):
    text = subprocess.run(["git", "show", f"{BEFORE}:spec/capabilities/{cap}.md"], cwd=REPO, capture_output=True,
                          text=True, check=True).stdout
    return sorted({int(n) for n in re.findall(r"(?m)^- \[r(\d+)\]", text)})


@pytest.mark.parametrize("cap", RETIRED)
def test_a_retired_capability_has_no_group_and_lists_every_id(cap):
    doc = spec_read.capability(path(cap))
    assert doc.problems == []
    assert doc.groups == []
    assert sorted(int(i[1:]) for i in doc.retired) == ids_before(cap)
    purpose = path(cap).read_text().split("## Purpose\n", 1)[1]
    assert purpose.startswith(NOTICE)


@pytest.mark.parametrize("cap", RETIRED)
def test_no_id_of_a_retired_capability_is_missing(cap):
    rows = model_restates.coverage(REPO, cap)
    assert [r["id"] for r in rows if r["state"] in ("missing", "pending")] == []


def test_formulation_keeps_no_line_of_its_own():
    """No formulator: each formulation line is dropped or moved to supervision (design §16.2)."""
    doc = spec_read.capability(path("formulation"))
    reasons = [why for cap, _, why in doc.dropped if cap == "formulation"]
    assert len(reasons) == 14
    assert doc.groups == []
    moved = sorted(n for cap, n, why in doc.dropped if why.startswith("moved to supervision"))
    assert moved == [1, 2, 6, 7, 11, 22]


def test_spec_integration_moves_its_script_lines():
    """A spec-integration line about a script goes to the capability owning the script (design §16.2)."""
    moved = {n: why for cap, n, why in spec_read.capability(path("spec-integration")).dropped
             if cap == "spec-integration" and why.startswith("moved to ")}
    assert {n for n, why in moved.items() if why.startswith("moved to supervision")} == {44, 45, 46, 54, 55}
    assert {n for n, why in moved.items() if why.startswith("moved to design-model-check")} == {16, 22}


def test_the_spec_integration_steps_are_gone():
    scenarios = REPO / "tests" / "scenarios"
    assert not list(scenarios.glob("spec_integration_*.py"))
    assert not (scenarios / "test_spec_integration.py").exists()


def test_the_universal_conditions_of_work_run_are_retired():
    """U1, U2, U6, U9 and U10 stated guarantees of `work run` and initiatives (plan-9 review S2, the-old-workflow-retired);
    U11, U4, U5, U7 and U8 are reworded in grammar 4 as U12-U16 (b155, b240), U7's worker now a dispatch with a
    worktree."""
    doc = spec_read.read_universal(REPO)
    assert doc.problems == []
    assert doc.frontmatter["retired"] == ["U1", "U2", "U3", "U6", "U9", "U10", "U11", "U4", "U5", "U7", "U8"]
    assert [u.id for u in doc.conditions] == ["U12", "U13", "U14", "U15", "U16"]
