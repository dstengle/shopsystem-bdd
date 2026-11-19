"""This repository's specification after the domain contract's move (plan 5): every live line parses to one meaning
(v_p*), uses only what the domain model declares (v_m1-v_m3), every declared refusal is stated (v_m4) and every
operation requested (v_m7), the model and the vocabulary are clean (v_m8, v_t18-v_t21), and spec/moves.json maps
every id a moved capability retired, once."""
import json
import pathlib
import re
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "tests"))

import spec_moves  # noqa: E402
import spec_read  # noqa: E402
import toolchain  # noqa: E402

MOVED = ("analysis-tools", "backlog", "batch-measurement", "batches-0-37", "brainstorming", "conversation",
         "decision-tiers", "design-model-check", "feature-file-tools", "intake", "migration-tools", "pr-review",
         "readiness", "requests", "telemetry", "trials-0-37")
CODES = re.compile(r"^(v_p\d*|v_m[1-8]|v_t1[89]|v_t2[01])$")


@pytest.fixture(scope="module")
def found():
    toolchain.require()
    from model_check import Model, solve
    model = Model(str(REPO)).read()
    violations, _ = solve(model)
    return [f for f in violations if f[0].startswith("v")]


def test_every_live_line_reads_and_uses_only_the_model(found):
    assert [f for f in found if CODES.match(f[0])] == []


def test_moves_json_maps_every_retired_id_of_a_moved_capability_once():
    moves = json.loads((REPO / "spec" / "moves.json").read_text())
    for name in MOVED:
        cap = spec_read.capability(REPO / "spec" / "capabilities" / ("%s.md" % name))
        assert cap.groups == []
        old = name.replace("-0-37", "")
        text = (REPO / "spec" / "capabilities" / ("%s.md" % name)).read_text()
        for ident in re.findall(r"^\| ([rg]\d+) \|", text, re.M):
            assert "%s#%s" % (old, ident) in moves
    assert spec_moves.problems(REPO) == []
