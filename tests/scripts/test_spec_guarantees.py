"""The 11 guarantees capabilities, converted (the GF conversion's design §16, plan P9): each file is codified, every
statement parses to exactly one tree in the live `Req` grammar, `model logic` finds no error in it (the one live run,
`live_logic`, less its known findings), `model
restates` finds every 0.29 id restated, dropped or moved, and none of them has a feature file."""
import pathlib
import sys

import model_restates
import pytest
import spec_grammar
import spec_lexicon
import spec_read
import spec_solve
import spec_tree

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
RECORDS = REPO / ".shop" / "records" / "2026-11-03-gf-conversion"
GUARANTEES = ("code-research", "delivery", "formulation", "planning", "red-green", "review", "role-boundaries",
              "spec-consistency", "spec-integration", "spec-migration", "trials")


def path(cap):
    return REPO / "spec" / "capabilities" / f"{cap}.md"


@pytest.fixture(scope="module")
def grammar():
    toolchain.require()
    return spec_grammar.load(REPO)


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


@pytest.mark.live_logic
@pytest.mark.parametrize("cap", GUARANTEES)
def test_the_logic_check_finds_no_error(live_logic, live_expected, cap):
    errors = [f.text for f in live_logic if f.code in spec_solve.ERRORS and any(i.startswith(f"{cap}#") for i in f.ids)
              and not live_expected(f)]
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


@pytest.mark.parametrize("cap", GUARANTEES)
def test_each_group_is_one_statement_numbered_as_its_group(cap):
    """Revision 2 (design-r2 §9.1): one statement for each group, and g<n> and r<n> share n."""
    odd = [(g.id, [r.id for r in g.requirements]) for g in spec_read.capability(path(cap)).groups
           if [r.id for r in g.requirements] != ["r" + g.id[1:]]]
    assert odd == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_no_two_groups_share_features_condition_and_trigger(grammar, cap):
    """v15n: statements that share features, condition and trigger are one statement (design-r2 §9.1)."""
    seen, shared = {}, []
    for g in spec_read.capability(path(cap)).groups:
        for r in g.requirements:
            clauses = spec_tree.parts(spec_tree.normal(spec_grammar.parse(REPO, r.text).tree))
            if all(clauses[k] is None for k in ("feat", "cond", "trig")):
                continue
            key = tuple("-" if clauses[k] is None else spec_tree.show(clauses[k]) for k in ("feat", "cond", "trig"))
            if seen.setdefault(key, g.id) != g.id:
                shared.append((seen[key], g.id))
    assert shared == []


@pytest.mark.parametrize("cap", [c for c in GUARANTEES if c != "formulation"])
def test_the_id_map_gives_every_id_the_capability_has(cap):
    """ids-<cap>.tsv (design-r2 §9.1): old codified id, tab, new id; its new ids are exactly the file's."""
    rows = [line.split("\t") for line in (RECORDS / f"ids-{cap}.tsv").read_text().splitlines()]
    olds = [old for old, _ in rows]
    assert len(olds) == len(set(olds))
    groups = spec_read.capability(path(cap)).groups
    assert {new for _, new in rows} == {f"{cap}#{x}" for g in groups for x in [g.id] + [r.id for r in g.requirements]}


@pytest.mark.parametrize("u, conjuncts", [("U3", ["ExitErr", "ChangeNothing"]), ("U4", ["Do", "Do"])])
def test_u3_and_u4_are_one_statement_of_joined_verb_phrases(grammar, u, conjuncts):
    """U3 and U4 by VP coordination (design-r2 §5.6): one `shall`, its verb phrases joined by `and`."""
    text = {c.id: c.text for c in spec_read.universal(REPO)}[u]
    resp = spec_tree.parts(spec_grammar.parse(REPO, text).tree)["resp"]
    assert [vp[0] for _, _, vp in resp] == conjuncts
    assert len({str(subject) for _, subject, _ in resp}) == 1
