---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-r3
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# R3: the solver engine (revision 2, layer 1)

Commit 410a22f8 on `gfr/R3`, off 864f61e9: three new files, `scripts/spec_engine.py` (178 lines), `grammar/cone.lp`
(29) and `tests/scripts/test_spec_engine.py` (201). No other file touched. The package could not write this file (the
harness refuses report files from a subagent); the layer 1 gate wrote it from the package's returned notes.

## Checks

- `tests/scripts/test_spec_engine.py`: 18 passed, every test the plan names among them (stops_at_horizon_1,
  chained_stops_at_horizon_2, core_names_both_ids, least_model_is_hash_seed_free, reachable_value, unreachable_value,
  cycle_bound, pool_retry, cone_rules, engine_uses_imain).
- `grep 'release_external\|def _ground' scripts/spec_engine.py` finds nothing.
- `tools size --limit 300` exits 0; full suite on gfr/R3: 789 passed, 1 skipped; `tools check` clean.

## Interface for R4/R6

- `solve(text, on_ids, imax, pools, optimise=False) -> Result(sat, horizon, core, models)`. `imax` goes to
  `telingo.imain` unchanged, so the horizons tried are 0..imax-1.
- pools render as `pool_size(K,n).` under `#program always`. The background must define
  `pool(K,1..N) :- pool_size(K,N).`
- On UNSAT with pools, the engine solves once more with each pool at n*imax+1; the core then comes from that solve.
- `core` is None when SAT; on UNSAT the minimal core as sorted ids, or [] when no id is on.
- `models` are the sorted shown atom strings. With `optimise` they are the optimal models (all models when the
  program has no `#minimize`). Collection stops at CAP+1; `least(models)` raises `Undetermined` past CAP (10000).
- `cone(facts, gid) -> (ids, edges)` reads trig/eff/uses/untriggered, plus two added facts: `sub(Kind,Super)`
  (transitive, matched both ways) and an optional `own(G,Id)`. The witness's facts carry gid as their id, and
  `edge(gid,T)` holds for each statement the witness's trigger fires.
- `horizon_bound(edges, gid)` is the longest path from gid, counting the witness's edge, plus 2; with a reachable
  cycle, the number of nodes reached plus 2.

## Calls made

- cone rule 2 is a least fixpoint: the closure condition is stated both ways and `#minimize` keeps the least set, so
  a While over an unused kind cannot support itself (r5 in test_cone_rules).
- on/1 ids not in `on_ids` are left free, which leaves those statements off.

## Module map row

| `scripts/spec_engine.py` with `grammar/cone.lp` | the solver of the codified spec: telingo.imain through a proxy, cores over the on/1 assumptions, optimal models and the least of them, the pool retry, a group's cone and its horizon bound (design-r2 §6.3) |
