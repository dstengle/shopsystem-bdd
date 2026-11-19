"""spec_entail: the entailment check (L8, the CNL 4 design's I13a), on a frozen copy of this repository's spec as the
domain contract left it (2026-11-19: the request pack, a domain model and its vocabulary; tests/scripts/fixtures/
entailment/), never the live spec: 26 Thens entailed, each with the premises recorded in fixtures/entailment/
entailed.txt, the same with the CLI pack's definition of refuse or without it, since the request pack's refuse is
primitive; the 15 requirements every Then of which is entailed are the L8 findings of baseline-logic.txt, their ids
moved. A restating pair is also the logic check's cluster's (fixtures/logic/cluster, r3 and r4)."""
import pathlib
import sys

import pytest
import spec_context
import spec_entail

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"
FROZEN = FIXTURES / "entailment"
CLUSTER = FIXTURES / "logic" / "cluster"


def _facts(root):
    toolchain.require()
    ctx = spec_context.load(root)
    assert ctx.refused == {}
    return list(ctx.domain) + [f for s in ctx.statements for f in ctx.facts[s.id]]


@pytest.fixture(scope="module")
def facts():
    return _facts(FROZEN)


def recorded():
    """{(L, I): ({M}, whether it needs the bridge)} of the record."""
    out = {}
    for line in (FROZEN / "entailed.txt").read_text().splitlines():
        L, I, ms, bridge = line.split()
        out[(L, I)] = (set(ms.split(",")), bridge == "bridge")
    return out


def thens(found):
    """The requirements' entailed Thens, the universal conditions' left out."""
    return {k: v for k, v in found.items() if v and not k[0].startswith("U")}


def test_twenty_six_thens_are_entailed_with_the_definition_of_refuse_or_without(facts):
    want = {k: ms for k, (ms, _) in recorded().items()}
    assert len(want) == 26 and not any(bridge for _, bridge in recorded().values())
    assert thens(spec_entail.entailed(facts, bridge=False)) == want
    assert thens(spec_entail.entailed(facts, bridge=True)) == want


def test_a_requirement_is_restating_when_every_then_is_entailed(facts):
    found = spec_entail.restating(facts, bridge=True)
    assert len(found) == 15 and found["reading#r57"] == [("1", ["reading#r13", "reading#r46"])]
    found = spec_entail.restating(_facts(CLUSTER), bridge=True)
    assert found == {"supervision#r3": [("1", ["supervision#r4"])], "supervision#r4": [("1", ["supervision#r3"])]}


def test_the_bridge_is_the_definition_of_refuse_an_imported_pack_gives():
    assert spec_entail.refuse_defined(FIXTURES / "codified-2")
    assert not spec_entail.refuse_defined(FROZEN)      # it imports the request pack
    assert not spec_entail.refuse_defined(FIXTURES / "glossary")      # it imports no pack
