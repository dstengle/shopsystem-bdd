"""spec_engine (design-r2 §6.3, §5.7): telingo's own incremental loop through a proxy, cores over the `on/1`
assumptions, optimal models and the least of them, the pool retry, the cone and the horizon bound. The programs are
hand-written `&tel` programs in the spike's shape; no tree is read."""
import os
import pathlib
import subprocess
import sys

import pytest
import spec_engine

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"

# r1: when trig happens, shall resp1 at the next state.
R1 = """
#program initial.
trig.
#program always.
#external on("r1").
{ resp1 }.
:- on("r1"), &tel{ trig & ~ > resp1 }.
"""
# r2: when resp1 happens, shall resp2 at the next state (chained on r1).
R2 = """
#program always.
#external on("r2").
{ resp2 }.
:- on("r2"), &tel{ resp1 & ~ > resp2 }.
"""
# r9: when trig happens, shall not resp1 at the next state (the seeded conflict with r1).
R9 = """
#program always.
#external on("r9").
:- on("r9"), &tel{ trig & > resp1 }.
"""
# r5: unrelated: when other happens, shall resp5.
R5 = """
#program always.
#external on("r5").
{ other; resp5 }.
:- on("r5"), &tel{ other & ~ > resp5 }.
"""


@pytest.fixture(autouse=True)
def tools():
    toolchain.require()


def test_stops_at_horizon_1():
    res = spec_engine.solve(R1, ["r1"], 5, {})
    assert res.sat and res.horizon == 1 and res.core is None


def test_chained_stops_at_horizon_2():
    res = spec_engine.solve(R1 + R2, ["r1", "r2"], 5, {})
    assert res.sat and res.horizon == 2


def test_off_statement_does_not_bind():
    """An id not passed in on_ids leaves its constraint free: r9 off, r1 is SAT."""
    assert spec_engine.solve(R1 + R9, ["r1"], 5, {}).sat


def test_core_names_both_ids():
    res = spec_engine.solve(R1 + R9 + R5, ["r1", "r9", "r5"], 4, {})
    assert not res.sat
    assert res.core == ["r1", "r9"]
    assert res.horizon == 3


def test_minimal_core_drops_an_id_the_conflict_does_not_need():
    """r2 depends on r1's response; the core of r1 against r9 stays exactly r1 and r9."""
    res = spec_engine.solve(R1 + R2 + R9, ["r1", "r2", "r9"], 4, {})
    assert res.core == ["r1", "r9"]


CHOICE = """
#program initial.
{ pick(1..3) } = 1.
#program always.
#minimize { 1@1 : pick(2) }.
#show pick/1.
"""


def test_optimal_models_and_least():
    res = spec_engine.solve(CHOICE, [], 2, {}, optimise=True)
    assert res.sat and len(res.models) == 2
    assert spec_engine.least(res.models) == ["pick(1,0)"]


def test_least_refuses_past_the_cap():
    with pytest.raises(spec_engine.Undetermined, match="not determined"):
        spec_engine.least([["a"]] * (spec_engine.CAP + 1))


def test_least_model_is_hash_seed_free():
    code = ("import spec_engine; r = spec_engine.solve(%r, [], 2, {}, optimise=True); "
            "print(len(r.models), spec_engine.least(r.models))" % CHOICE)
    outs = set()
    for seed in ("1", "4242"):
        env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONPATH=str(SCRIPTS))
        outs.add(subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True,
                                check=True).stdout)
    assert len(outs) == 1 and "pick(1,0)" in outs.pop()


STEPS = """
#program initial.
v(a).
#program dynamic.
v(b) :- 'v(a).
v(c) :- 'v(b).
v(d) :- 'v(d).
"""


def test_reachable_value():
    res = spec_engine.solve(STEPS + "#program initial.\n:- not &tel{ >? v(c) }.\n", [], 4, {})
    assert res.sat and res.horizon == 2


def test_unreachable_value():
    res = spec_engine.solve(STEPS + "#program initial.\n:- not &tel{ >? v(d) }.\n", [], 4, {})
    assert not res.sat and res.horizon == 3 and res.core == []


# four distinct instances of k_x used at state 0; a pool of 2 is too small for it
FOUR = """
#program always.
pool(K,1..N) :- pool_size(K,N).
#program initial.
{ used(o(K,N)) : pool(K,N) }.
:- #count { X : used(X) } < 4.
"""


def test_pool_retry():
    res = spec_engine.solve(FOUR, [], 2, {"k_x": 2})
    assert res.sat


def test_pool_retry_does_not_hide_a_conflict():
    res = spec_engine.solve(FOUR + "#program initial.\n:- used(_).\n", [], 2, {"k_x": 2})
    assert not res.sat


def test_engine_uses_imain(monkeypatch):
    import telingo
    calls = []
    real = telingo.imain

    def record(*args, **kwargs):
        calls.append(kwargs.get("imax"))
        return real(*args, **kwargs)
    monkeypatch.setattr(telingo, "imain", record)
    spec_engine.solve(R1, ["r1"], 5, {})
    assert calls == [5]


def test_horizon_bound_is_longest_path_plus_2():
    edges = [("g", "r1"), ("r1", "r2"), ("r1", "r3"), ("r3", "r4"), ("x", "y")]
    assert spec_engine.horizon_bound(edges, "g") == 5
    assert spec_engine.horizon_bound([], "g") == 2


def test_cycle_bound():
    edges = [("g", "a"), ("a", "b"), ("b", "a"), ("x", "y")]
    assert spec_engine.horizon_bound(edges, "g") == 3 + 2


SIGS = """
trig("g",does,e_start,k_initiative). uses("g",k_initiative). uses("g",k_work_item).
trig("r1",does,e_start,k_initiative). eff("r1",does,e_begin,k_stage). uses("r1",k_initiative). uses("r1",k_stage).
trig("r2",does,e_begin,k_node). eff("r2",does,e_log,k_stage). uses("r2",k_stage).
sub(k_stage,k_node).
trig("r3",does,e_end,k_stage). uses("r3",k_stage).
untriggered("r4"). uses("r4",k_work_item).
untriggered("r5"). uses("r5",k_result).
untriggered("r6"). uses("r6",k_stage). uses("r6",k_work_item).
"""


def test_cone_rules():
    ids, edges = spec_engine.cone(SIGS, "g")
    assert ids == ["r1", "r2", "r4", "r6"]
    assert edges == [("g", "r1"), ("r1", "r2")]


def test_cone_own_statement_enters():
    ids, _ = spec_engine.cone('own("g","r5"). uses("g",k_result). untriggered("r5"). uses("r5",k_result).', "g")
    assert ids == ["r5"]


def test_no_copied_loop():
    text = (SCRIPTS / "spec_engine.py").read_text()
    assert "release_external" not in text and "def _ground" not in text
