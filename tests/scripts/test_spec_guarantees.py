"""The 11 guarantees capabilities, converted (the GF conversion's design §16, plan P9): each file is codified, every
statement parses to exactly one tree in the live `Req` grammar, `model logic` finds no L1 or L3 in it, `model
restates` finds every 0.29 id restated, dropped or moved, and none of them has a feature file."""
import pathlib
import sys

import model_restates
import pytest
import spec_grammar
import spec_lexicon
import spec_read
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
GUARANTEES = ("code-research", "delivery", "formulation", "planning", "red-green", "review", "role-boundaries",
              "spec-consistency", "spec-integration", "spec-migration", "trials")


def path(cap):
    return REPO / "spec" / "capabilities" / f"{cap}.md"


@pytest.fixture(scope="module")
def grammar():
    toolchain.require()
    return spec_grammar.load(REPO)


@pytest.fixture(scope="module")
def findings(grammar):
    return spec_solve.run(REPO)


@pytest.mark.parametrize("cap", GUARANTEES)
def test_the_capability_is_codified_and_well_formed(cap):
    assert spec_read.codified(path(cap)), f"{cap} has no `language: codified-1`"
    doc = spec_read.capability(path(cap))
    assert doc.problems == []
    assert doc.groups or cap == "formulation", f"{cap} has no group"
    assert doc.frontmatter.get("group") == "guarantees"


@pytest.mark.parametrize("cap", GUARANTEES)
def test_every_statement_parses_to_one_tree(grammar, cap):
    refused = []
    for g in spec_read.capability(path(cap)).groups:
        for r in g.requirements:
            p = spec_grammar.parse(REPO, r.text)
            if p.tree is None:
                refused.append(f"{cap}#{r.id}: {p.refusal}: {r.text}")
    assert refused == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_the_logic_check_finds_no_error(findings, cap):
    errors = [f.text for f in findings if f.code in ("L1", "L3") and any(i.startswith(f"{cap}#") for i in f.ids)]
    assert errors == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_every_old_id_is_restated_dropped_or_moved(cap):
    rows = model_restates.coverage(REPO, cap)
    assert rows, f"spec/restated.json has no id of {cap}"
    assert [r["id"] for r in rows if r["state"] == "missing"] == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_a_guarantees_capability_has_no_feature(cap):
    assert not (REPO / "features" / f"{cap}.feature").exists()


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


def test_the_lexicon_has_no_problem(grammar):
    assert spec_lexicon.problems(spec_lexicon.read(REPO)) == []
