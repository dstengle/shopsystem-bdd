---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p12
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P12, supervision converted

Branch `gfc/P12`, off `gf-conversion` at 76e79f3e.

## What was converted

- `spec/capabilities/supervision.md` is codified (`language: codified-1`): 86 groups, 139 statements (r1–r140; r71
  unused after a rewrite inside this package), 46 terms of its own in `## Terms`, `## Dropped`, and prose under
  "Implementation, may change".
- Of the 164 0.29 ids, 147 are restated and 17 dropped, each with its reason. The 11 lines moved here
  (formulation r1, r2, r6, r7, r11, r22; spec-integration r44, r45, r46, r54, r55) are restated as
  `formulation#r<n>@0.29` and `spec-integration#r<n>@0.29`. `model restates` over the whole spec gives 581 ids:
  516 restated, 65 dropped, 0 pending, 0 missing.
- The resource formulation of r20/r59/r60/r66/r95 is four logic-only groups (g82–g85): the `integrate`, `apply` and
  `formulate` rounds hold the spec lock; every stage that is no worker's holds the initiative lock; every worker's
  stage holds a worker slot; an implement stage holds a claim, and a merge holds the merge lock. U1 and U2 do the rest.
- The new flow (P8): g78 (the formulate round runs `features generate` on a codified change list and commits the
  feature), g79 (an uncodified capability is the formulate round's fault) and g64 (drafts that do not parse are sent
  back twice, then asked about). The removed formulate-question lines (r116, r152, r153, r186) are dropped.
- `features/supervision.feature` is generated (82 scenarios). The 26 old step modules are deleted. The handlers are
  `supervision_handlers.py` (Givens and Whens), `supervision_handlers_then.py` and `supervision_handlers_what.py`
  (Thens), over three helpers loaded by path: `supervision_world.py` (the repository, the stand-in, the run and the
  readings), `supervision_build.py` (the repository built from the Givens) and `supervision_plans.py` (what each
  stand-in session does). `test_supervision.py` is `bind_all` plus `scenarios()`.

## Calls made

- `features generate` drops a condition whose `Means:` is not an attribute constraint when it is written before the
  noun ("a faulty session"). So every such condition is a `While` atom on an instance that its `given` block names
  ("While a session is faulty, when the session ends ..."). The conditions sit on kinds that no other capability's
  handlers claim (session, result, remote, initiative branch, work-item branch, file, change list, question),
  because `GivenK_C` handlers are global and design-model-check's handlers claim the node kinds.
- A stage is named by its kind attribute (`` a `research` stage for the work-item ``). The relations
  `for (stage → work-item|initiative|capability-proposal|glossary-proposal|request|question)` and
  `on (question → …)` are in supervision's Terms.
- What a brief and a worker's tools must hold is carried by the kinds `worker brief`, `round brief`, `review brief`
  and `tool list`. Their definitions list r11–r14, r17, r19, r24, r25, r30, r44, r57, r98, r102, r141, r154–r157,
  r164, r168 and r170. Each group says that the stage is given one, and its handler checks for markers of it.
- In the scenarios, a round that no step names ends with no result, so its node keeps the status that the named stage
  left (U6). A worker that no step names gives DONE. Delegation scenarios start with the question already asked,
  because `work run` answers under a delegation only at the start of a delivery.
- Dropped to "Implementation, may change" (still tested by `tests/scripts`): the `--work-item` plugin option (r22,
  r55, r56, r64, r65), `[tests]` (r29), and the expected-failure counting with the question that gives both runs
  (r43, r122, r220). r42 restated U6. r73, r123 and r124 were dropped because deprecated scenarios are gone.
- Lost as scenarios (now logic-only or carried by a definition): parallel starts (r20, r59, r60), merge order (r61),
  the analysis session that ends at its turn limit (r76's second scenario), r187's merge of ids across proposals, and
  r110's second review in the same run (restated under g41).

## Checks on the branch

- `model parse --file spec/capabilities/supervision.md`, `model logic supervision` (about 75 s, no findings),
  `model restates supervision` and `features generate --check supervision` all exit 0.
- `python3 -m pytest -q tests/scenarios/test_supervision.py`: 82 passed (about 9 s with xdist).
- `features vocab --check --tests tests/scenarios features/supervision.feature`: every step has one handler.
- `tools size --limit 300` exits 0, and ruff is clean on the new modules.
- `model check`: no v_p*, v15g–k, v_t4–6 or v_s* row. Unresolved references rise from about 398 to 457. They are old
  `.shop/work` references to 0.29 supervision ids, now read against the codified file; P13/P14 rewrite them to `@0.29`.

## Asks carried

- The suite has one failure outside the baseline, and P12 does not own its file:
  `tests/scripts/test_model_restates.py::LiveRestatesTest::test_supervision_is_not_restated_yet` asserts the state
  before P12 (`model restates supervision` exits 1). It should now assert exit 0 for the whole spec. All 23 baseline
  failures are gone.

- `features_generate` drops a condition whose `Means:` is not "its <attribute> is …" from the position before the
  noun. Its `resolve()` picks the relation `for (stage → node)` by term alone ("the stage s2 is for the node w1").
- vocab: a step that names its kind with no instance needs `work_queue_world.bind_all`, as P11 found.
- `work run`: when an integrate round's raise into an upstream is refused, the commit of the initiative's transition
  fails on a missing stage directory (`pathspec .shop/work/i1/runs/i1`), instead of a fault that names the refusal.
- P13/P14: the old `.shop/work` references to supervision's 0.29 ids (59 work-items' `accepts`, and the i24 and i41
  proposals).

## Module-map rows

- `tests/scenarios/supervision_handlers*.py`: the handlers of supervision's generated feature (the Givens and the
  Whens; the Thens on stages; the Thens on commits, exits and output).
- `tests/scenarios/supervision_world.py`, `supervision_build.py` and `supervision_plans.py`: the repository that
  `work run` runs in, built from the Givens, and what the stand-in claude does in it.
