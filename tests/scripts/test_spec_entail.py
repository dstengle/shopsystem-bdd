"""spec_entail: the entailment check (L8, the CNL 4 design's I13a), on a frozen copy of this repository's spec as it
was on 2026-11-10 after grammar 4's rewording (tests/scripts/fixtures/entailment/, every file codified-2), never the
live spec: 13 Thens entailed without the CLI pack's definition of refuse and 20 with it, each with the premises
recorded in fixtures/entailment/entailed.txt (`bridge` where only the definition entails it). The rewording left no
line restating: a restating pair is the logic check's cluster's (fixtures/logic/cluster, r3 and r4)."""
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


def test_without_the_definition_of_refuse_thirteen_thens_are_entailed(facts):
    want = {k: ms for k, (ms, bridge) in recorded().items() if not bridge}
    assert len(want) == 13
    assert thens(spec_entail.entailed(facts, bridge=False)) == want


def test_with_the_definition_of_refuse_twenty_thens_are_entailed(facts):
    want = {k: ms for k, (ms, _) in recorded().items()}
    assert len(want) == 20
    assert thens(spec_entail.entailed(facts, bridge=True)) == want
    # a refusal's Then, entailed only through the definition of refuse, by the universal condition of a refusal
    assert want[("design-model-check#r202", "2")] == {"U12"}


def test_a_requirement_is_restating_when_every_then_is_entailed(facts):
    # every requirement of the reworded spec adds a Then of its own
    assert spec_entail.restating(facts, bridge=True) == {}
    found = spec_entail.restating(_facts(CLUSTER), bridge=True)
    assert found == {"supervision#r3": [("1", ["supervision#r4"])], "supervision#r4": [("1", ["supervision#r3"])]}


def test_the_bridge_is_the_definition_of_refuse_an_imported_pack_gives():
    assert spec_entail.refuse_defined(FIXTURES / "codified-2")
    assert spec_entail.refuse_defined(FROZEN)
    assert not spec_entail.refuse_defined(FIXTURES / "facts")      # it imports no pack
