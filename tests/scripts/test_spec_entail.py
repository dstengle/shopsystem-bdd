"""spec_entail: the entailment check (L8, the CNL 4 design's I13a), on a frozen copy of this repository's spec as it
was on 2026-11-10 (tests/scripts/fixtures/entailment/, section 13 point 10), never the live spec: 20 Thens entailed
without the CLI pack's definition of refuse and 55 with it, each with the premises the design's study recorded
(entailment/k1_entailed.txt, as fixtures/entailment/entailed.txt)."""
import pathlib
import sys

import pytest
import spec_context
import spec_entail
from spec_entail_rules import Premises, parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"
FROZEN = FIXTURES / "entailment"


@pytest.fixture(scope="module")
def facts():
    toolchain.require()
    ctx = spec_context.load(FROZEN)
    return list(ctx.domain) + [f for s in ctx.statements for f in ctx.facts[s.id]]


def recorded():
    """{(L, I): ({M}, whether it needs the bridge)} of the study's record."""
    out = {}
    for line in (FROZEN / "entailed.txt").read_text().splitlines():
        L, I, ms, bridge = line.split()
        out[(L, I)] = (set(ms.split(",")), bridge == "bridge")
    return out


def thens(found):
    """The requirements' entailed Thens, the universal conditions' left out."""
    return {k: v for k, v in found.items() if v and not k[0].startswith("U")}


def test_without_the_definition_of_refuse_twenty_thens_are_entailed(facts):
    want = {k: ms for k, (ms, bridge) in recorded().items() if not bridge}
    assert len(want) == 20
    found = thens(spec_entail.entailed(facts, bridge=False))
    assert set(found) == set(want)
    # the premises recorded are the bridge's run: without it a refusal's (U11) is no premise
    assert all(found[k] == want[k] - {"U11"} or found[k] == want[k] for k in want)


def test_with_the_definition_of_refuse_fifty_five_thens_are_entailed(facts):
    want = {k: ms for k, (ms, _) in recorded().items()}
    assert len(want) == 55
    assert thens(spec_entail.entailed(facts, bridge=True)) == want


def test_a_requirement_is_restating_when_every_then_is_entailed(facts):
    found = spec_entail.restating(facts, bridge=True)
    # both Thens of requests#r8 (exit with an error naming an origin, change nothing) are requests#r6's
    assert found["requests#r8"] == [("1", ["requests#r6"]), ("2", ["requests#r6", "U11"])]
    # readiness#r2's exit with an error is its own, said by no other line: one Then entailed is not enough
    assert "readiness#r2" not in found


def test_the_bridge_is_the_definition_of_refuse_an_imported_pack_gives():
    assert spec_entail.refuse_defined(FIXTURES / "codified-2")
    assert not spec_entail.refuse_defined(FROZEN)


def test_an_object_a_negated_restriction_narrows_is_asked_of_no_premise():
    facts = ['trig("c#r1",ran,"`x`",a_p,none).', 'role("c#r1",x1,k_file).', 'resp("c#r1",1,pos,print,a_t,x1).',
             'trig("c#r2",ran,"`x`",a_p,none).', 'role("c#r2",x1,k_file).', 'resp("c#r2",1,pos,print,a_t,x1).',
             'nattr("c#r2",x1,a_status,value(a_status,done)).', 'kind(k_file).']
    idx = spec_entail.index(Premises(*parse(facts)))
    assert idx.get(("c#r1", "1")) == ["c#r2"]
    assert ("c#r2", "1") not in idx


def test_a_premise_whose_object_is_kept_negated_over_a_kind_forces_nothing():
    facts = ['trig("c#r1",ran,"`x`",a_p,none).', 'role("c#r1",x1,k_file).', 'role("c#r1",x2,k_stage).',
             'resp("c#r1",1,pos,print,a_t,x1).', 'nrel("c#r1",r_in,x1,kind(k_stage)).']
    assert Premises(*parse(facts)).rule("c#r1") == []
