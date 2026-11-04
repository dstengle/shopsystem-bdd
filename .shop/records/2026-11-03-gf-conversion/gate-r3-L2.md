---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-gate-r3-l2
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Revision 3, layer 2 gate

The gate passed on `gf-conversion`. Its base was f626b7f4. Both task branches were reset by their tasks to that
commit, and both merged without conflicts. CLAUDE.md auto-merged, because the rows the two branches changed are
adjacent but do not overlap.

## Merged

| task | branch head | merge |
|---|---|---|
| S5 `model logic` on facts | ea5afb63 | merge gfr3/S5 (revision 3, layer 2) |
| S6 Gherkin from facts | 18b7b1c6 | merge gfr3/S6 (revision 3, layer 2) |

## Review

- **S5** matches the plan:
  - `run(root, capability=None, extra=None)`, `report`, `ERRORS` with L0, `LIMIT`, `solve(program, limit)` with
    `async_`/`wait`, and `l2`, `_key` and `_order` kept.
  - One brave solve, plus one focused normal solve per reported pair.
  - `spec_solve.py` is 157 lines, under the 200 limit. The finding texts are in the new `spec_findings.py`, which
    has its map row.
  - The tests the plan lists are all there, including `test_a_draft_of_a_live_capability_replaces_it` (Review
    Focus 2) and `test_a_context_with_nothing_codified_has_no_findings` (Review Focus 3).
  - Departure: `hold(Res)` is now stative in check.lp, so L5 does not lint "shall hold". This follows design §3.1
    ("an event, not a state"), and the cluster's L5 test pins it.
- **S6** matches the plan:
  - `spec_trace_steps.py` was renamed to `spec_steps.py` with `git mv`. `read(facts, logic, steps)` is built on
    the unchanged `Reader`.
  - The fact-to-atom work is in the new `spec_steps_facts.py`, which has its map row.
  - `features_generate` has no solver and no multiprocessing. `scenario_text(v, ctx, cap, group)` raises
    `GenerateError` on a refused requirement.
  - The tests the plan lists are there, including `test_no_failing_value_gives_no_contrast` (Review Focus 5), the
    hash-seed byte stability test and the no-solver import test.
  - Its five reasoned departures are in report-S6: the defined-condition expansion is dropped, the restrictions of
    a negative response are not Thens, a condition contrast is the opposite condition, `only` gives no Then, and the
    toy world's default status is `none`. The gate accepts them.

## Fixed by the gate

- The harness refused S5's write of `report-S5.md`. The gate wrote it from S5's result and committed it with this
  record.
- No code was changed.

## Results

- `python3 scripts/tools size --limit 300`: exit 0.
- `scripts/spec_solve.py`: 157 lines.
- Module-map condition, checked inline because `test_revision_done` is still ignored: every `scripts/*.py` has a
  row. The only leftover mention of `spec_trace_steps` is in the docstring of the dead `spec_trace.py`, which S7
  deletes.
- `timeout 600 python3 -m pytest -n 8 -q --durations=8 $SLOW'`: 718 passed, 1 skipped and 125 subtests, in 17.4 s.
  - `$SLOW'` ignores `test_spec_guarantees`, `test_spec_trace`, `test_revision_done`, `test_spec_engine`,
    `test_spec_logic` and `tests/scenarios/test_supervision`.
  - `test_spec_solve` and `test_features_generate` are rewritten, so they now run.
  - The run includes `test_e2e_codified`, `test_supervise_outputs` and `test_supervise_formulate`, which the plan
    defers to this gate. All three pass.
- Slowest tests:
  - `test_e2e_codified.py::test_a_request_goes_through_the_requirements_system_into_delivery` took 11.9 s. This is
    over the 10 s ceiling. It was already over before this layer, and S8 owns it.
  - `test_features_generate.py::test_check_on_the_live_repo_runs_to_its_end` took 6.9 s. Almost all of it is pgf
    parsing in `spec_context.load`.

## Left

- S6 found that a later "the K" after "a K" in a response's object becomes a new role, because `Walk.objects`
  restores the bindings. Examples: supervision r39 reads as stages s1 to s4, and requests r1 as "commits the request
  q2". This affects both the scenarios and the facts check.lp reads. It is left for S10, or for S11 before the live
  clashes are counted.
- The parse cost of `spec_context.load` (about 6 s on the live spec) and the thread-unsafe `_once` are left for
  S8 and S12. They need a parse cache shared across processes.
- The live spec has not been solved (S11). Each focused L1 solve grounds the program again; if that is slow, the
  fix is an `#external focus/2` on one Control.
- The e2e test is over the 10 s ceiling (S8).
- `spec_trace.py` and `spec_engine.py` are dead until S7 deletes them.
