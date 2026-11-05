---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p11
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P11, the core service capabilities

Branch `gfc/P11`, commits 323801e1 (work-queue), 31b10972 (requests), 39c0064e (design-model-check). Written by the layer 3 merge from the package's returned notes: the harness refused the package's own write of this file. done=false
only for `model parse --file`, settled at the merge.

## What was converted

- work-queue: 26 groups; 31 restated, 2 dropped (r12 to Implementation, r39 under Not yet); r59 moved to requests.
- requests: 27 groups; 36 restated, 12 dropped (r25, r72, and 10 lines not implemented today, under Not yet).
- design-model-check: rewritten against v5, 55 groups; 58 restated, 8 dropped. Each table row is a statement
  `If the person runs model check on a <kind> that is <condition>, then model shall exit with an error naming ...`,
  each condition a Terms entry. Uses v_d5 for v_d2, v18d for v18, v_p1 for v_e1/v_e2 (closes the L1 carry), and
  restates spec-integration#r16 and #r22.
- Fixed in passing: attribute `stage` made U10 ambiguous, now `asking stage`. `work` does not push, so a local event
  `commit` is used. Old step modules deleted (9 work_queue_*, 6 requests_*, 11 design_model_check_*).

## Checks on the branch

logic, restates and `features generate --check` exit 0 for each; 108 passed; vocab check exit 0; suite at baseline;
`model check` has no v_p*, v15g-k, v_t4-6, v_s* rows.

## Asks carried

- vocab.py catch-all misses a step naming its kind with no instance; worked around with
  `work_queue_world.bind_all(globals(), ROOT)`.
- features_generate: StopIteration in `precondition()` (as P10); `resolve()` picks a relation id by term alone.
- Shared handler keys P11 claims (ThenDoes write/commit/change, GivenK_C/GivenK_A/GivenK/GivenR for many kinds); P12
  must merge with them or move them to `world_*.py`.
- world_nodes' GivenK_A for a request writes the value as `status` whatever the attribute.

## Module-map rows

- `tests/scenarios/work_queue_handlers.py`: handlers of work-queue's generated feature.
- `tests/scenarios/work_queue_world.py`: the scenario repository as git, noun phrases matched against files written
  or committed, and `bind_all`.
- `tests/scenarios/requests_handlers.py`: handlers of requests' generated feature.
- `tests/scenarios/design_model_check_handlers*.py`: handlers of design-model-check's generated feature.
