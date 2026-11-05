---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-suite-cost
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: final
---

# What the suite spends its time on, after the solver

The solver-driven files were excluded and not run. The figures come from the non-solver files: 649 tests, run with
`-n auto` on 32 CPUs. Scratch plugins and outputs are in the session scratchpad under `suite-cost/`. No tracked file
was changed.

## Baseline

347.4 test-seconds and 26.6 s wall.

## Contributors

1. **The step vocabulary is reloaded on every scenario step.** This takes about 188 test-seconds, 54% of the total.
   - `features_vocab.load(root)` (`scripts/features_vocab.py:85-97`) caches only the compiled grammar. Each call
     re-reads the lexicon twice, rebuilds every GF source and hashes them, about 24 ms a call.
   - It is called once per step from `tests/scenarios/vocab.py:141,175,195` and `work_queue_world.py:198`: 580 calls
     in `test_design_model_check.py` alone.
   - Memoising the load once per process gave 347 → 159 test-seconds and 26.6 → 19.7 s wall, with every test still
     passing.
2. **`migrate upgrade` stages files one at a time.** This takes about 22 test-seconds, 6%.
   - `scripts/migrate_upgrade.py:104-107` runs one `git add -f` per file: 1,739 calls at 6.5 ms each.
   - The setup of `test_migrate_upgrade_codified.py` takes 13.2 s, and xdist runs it on two workers.
   - One batched `git add` brought the setup to 3.0 s and the file from 36.4 to 8.5 test-seconds.
3. **The rest has no shared cause.** That covers nested pytest runs in `tools map` and `work_items`, and
   `model check` subprocesses.

## Ruled out

| candidate | measured |
|---|---|
| interpreter startup | 40–75 ms |
| `import pgf` | 9 ms |
| GF compile | always a cache hit |
| collection | 0.54 s |
| xdist startup | about 1.3 s |
| building git repositories | 0.5 s per file |

## Wall-clock floor

With both fixes applied and no solver tests, the suite took 18.1 s. It is bounded by
`test_e2e_codified.py::test_a_request_goes_through_the_requirements_system_into_delivery` at 11.2 s, which calls
`model logic` and `features generate`, so design-r3 shrinks it. Without that test, the floor is about 6–8 s.
