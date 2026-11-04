---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s12
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Report S12: verification and speed acceptance (plan-r3, layer 6)

Written by the layer-6 gate from S12's notes; the harness refused the file in S12's worktree, as it did for
S10/S11. Branch gfr3/S12, head 3a8559f3, reset to gf-conversion eec8ea1d before any work.

## Speed (design-r3 §2 goal 6)

Wall time and max RSS through a getrusage wrapper (no /usr/bin/time on this machine).

| Command | Before | After | Max RSS | Exit |
|---|---|---|---|---|
| `model logic` on the live spec | 4.22 s | 1.15-1.26 s | ~68 MB | 1 (the 32 expected L1s) |
| `features generate --check` | | 1.09-1.11 s | 62 MB | 0 |

## Suite

- Full suite, no ignores (`timeout 900 pytest -q --durations=0`): 920 passed, 1 skipped, 129 subtests, 15.2 s
  wall (baseline 26.6 s, floor 18.1 s). Earlier runs 919/920; before CPU timing, the wall-time speed test failed
  once under load.
- Solver-driven files' test-seconds (target under 15): 38.4 at first; 13.8 alone with -n auto (211 passed in 4.1
  s); 21.5 inside the full suite at 1917% CPU.
- Ceiling: 1 of 4 runs printed `test_a_flaky_scenario_is_run_again_before_the_merge` at 10.01 s (not a solver
  test: 4.6-5.6 s alone, 7.7-9.1 s in the other runs).

## Repository checks

- `tools size --limit 300`: exit 0.
- `tools check scripts tests`: exit 0 after fixing 16 ruff findings that were already there.
- `model check --limit 100000`: exit 1 as at baseline; nothing new against `baseline-model-check.txt` on the
  file:/unresolved: rows after the records fix. v17 is 25 against 24, the extra row from .shop/work (q47).
- `features vocab --check`: exit 0.

## What changed

1. One grounding for the whole check (the 4.2 s → 1.2 s fix). `grammar/check.lp` declares
   `#external focus(A,B) : pair(A,B).`; `spec_solve` grounds once (`_ground`), runs the brave solve, then each L1
   witness on the same control (`_solve`), setting that pair's external true with `assign_external` and false
   after. Assumptions do not work: a default-false external is fixed, so assuming it true is UNSAT.
   `solve(program, limit, brave)` keeps its signature. Pinned by `test_the_whole_context_is_one_grounding`.
2. Witness texts changed (another first model, another valid pre-state), so `tests/scripts/conftest.EXPECTED` is
   keyed by "<code> <id> <id>", as S11 recommended: the same 32 entries and 7 questions, read through
   `expected(f)` (fixture `live_expected`).
3. Suite cost: every `live_logic` test is xdist group "live_logic" (a tryfirst hook in the root conftest.py, and
   `--dist loadgroup` in pytest.ini), so the live spec is solved once a run; pinned by
   `test_the_live_logic_tests_share_one_worker`. The two model-check fixture tests share group "model_check". Both
   speed tests repeat once only when over the limit. `test_model_logic_on_the_live_spec_is_fast` measures the
   child's CPU time (wall failed at 2.6-5.3 s under 32-way load; CPU equals wall at ~1.15 s idle).
4. Ruff findings fixed: I001 (measure_build, workqueue, supervise_analysis), FURB167 (measure_read, stub_claude),
   F401 and PIE810 (test_spec_grammar), RUF100 (test_supervise_answers, test_supervise_change), B023 in
   supervise_change (each lambda binds a default argument; behaviour unchanged).
5. Record frontmatter: `kind: report`/`plan`/measurement gave 13 new model-check file rows; changed to
   analysis/design as revision 2's records use; report-S1's id lowercased.
6. The CLAUDE.md spec_solve row says how witnesses are solved.

## Goals (design-r3 §2)

Goals 1-5, the anti-goals and the §7 module table are met (spec_solve.py 171 lines). Goal 6 is met for both
commands; its test-seconds target is met alone (13.8) but not inside the full suite (21.5 under contention).

## Open

- Two non-solver tests near the 10 s ceiling under load: the flaky-scenario test (12 nested pytest runs) and e2e
  (8.5-9.4 s).
- An L5 text prints a raw term: "give pair(v1,n_grade)".
- logic-r3-after.json still has the old witness texts.
- S11's 7 questions, the If-exception rule, §3.2's false hits and the unread rnone are open for the person.
