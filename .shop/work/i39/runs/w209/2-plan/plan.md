# Plan of w209: design-model-check r120 (v17) and r121 (v18)

From the research notes `.shop/work/i39/runs/w209/1-research/notes.md` (cited as "notes §n").

## 1. What goes green

- **design-model-check#r120**, scenario "a request that is part of no job-thread, cites no origin and is raised for no request is v17" (`features/design-model-check.feature`, line 864). It is red because its first Given is undefined. The Givens for q3 ("part of a job-thread") and q4 ("raised for the request …/other/q7") are also undefined, and the Then "v17 does not name q2, q3 or q4" matches no pattern. In code, the v17 rule in `scripts/model.lp` (lines 256-259) has no raised-for term, and `in_thread` never holds because no job-thread node is ever made in this context. `model_requests.py` reads only `part_of` and `source`, and `request_form` treats a request that is raised for another and has neither of those as a file problem (notes §1, §3, D1, D3).
- **design-model-check#r121**, the outline "an id of a kind kept in .shop/work/ with another context's path is v18 unless a request is raised for it" (7 rows, line 904). It is red because Given "no request is raised for it" (6 rows) and Given "a request q9 of this context is raised for it" (1 row) are undefined. In code, `v18(X) :- foreign(X)` has no exemption (notes §1).
- **Retired by the work-item:** the deprecated scenario "a request that is part of no job-thread and cites no origin is v17 (deprecated)". The feature tags it `@r115 @deprecated` (lines 853-861). Its body says "Deprecated for:" the r120 scenario, which is why the Retires lists it under `@r120`. It is removed (decision 6).

## 2. Where the change lands

- `scripts/model.lp`: changes to v17 and v18:
  - v17 also lets a request off when it names a job-thread in `part_of` or a request it is raised for (decisions 1 and 3).
  - v18 does not fire on a request id that some request is raised for (decision 4).
  - The `#defined` line for the new relations goes beside the existing ones.
  - The labels of v17 and v18 are reworded to the text of r120 and r121 (decision 5), and the `#show` comment cites r120 and r121.
- `scripts/model_requests.py`: changes to how requests are read:
  - `request_links` reads the `raised_for` field (decision 2) and gives a fact for a request's job-thread when its `part_of` id has the kind `job-thread`, judged from the id (decision 1).
  - `request_form` accepts `raised_for` as the request's link when the asker is not internal (decision 3).
- `tests/scenarios/design_model_check_requests.py`: Givens and cleanup:
  - New Givens for r120's q1, q3 and q4, and for r121's two `<raised>` phrases (decision 7).
  - The Given used only by the removed r115 scenario ("…part of no job-thread and cites no origin" with no "raised for" clause) is removed, since no scenario uses it after decision 6.
  - The section comment cites r120 and r121.
- `tests/scenarios/design_model_check_then.py`: the Then pattern at line 129 and the id split under it also accept a list separated by commas with a final "or" or "and" ("q2, q3 or q4").
- `features/design-model-check.feature`: the `@r115 @deprecated` scenario (lines 853-861) is removed, as the Retires says. Nothing else in the feature changes.

This is the researcher's file set, with no file added or removed. `model_facts.py` (room 13 lines) needs no change: `qualify` already emits `foreign` for a raised-for target, and the exemption happens in the solve (notes §3).

## 3. Decisions

1. **What counts as "part of a job-thread" (v17).** A request is part of a job-thread when its `part_of` names an id of kind `job-thread`, judged from the id alone. No job-thread file needs to exist in this context.
   - Rests on design-model-check#r120, r19 and r43, and on design-decision/references-are-ids.
   - r43 reads `<kind>/<context path>/<name>` as a node of that kind. r19 reads no file where a job-thread could be kept, and job-threads are product-level ("Not yet"). If the job-thread had to exist, r120's own scenario (q3 not named) could never pass.
   - Fixes defect D1: a request written with `work request --thread` is no longer v17.
   - A `part_of` naming any other kind (such as the initiative in r120's q1) is still no job-thread.
2. **The field name is `raised_for`.** It holds one request id, written in the frontmatter of the upstream's request.
   - Rests on requests#r29 and requests#r44, which say a request is raised for one request.
   - The name comes from the grammar `scripts/model.lp` implements: `docs/design-model/design-model.md:95` and `grammar.md:77` (notes Q4).
   - No narrator observation depends on the name beyond the request's form.
3. **A request raised for another, with no `source` or `part_of`, is well formed when its asker is not internal.** A request like that counts as raised for a request (v17) when its `raised_for` id has the kind `request`, judged from the id.
   - Rests on design-model-check#r112 ("the form `work request` writes") together with requests#r44 and requests#r31: `work request` writes a request from another context's asker with `--raised-for` alone.
   - The same r112, with requests#r45, keeps today's file problem for an internal request that names neither `--source` nor `--thread`.
   - This settles notes Q2 as reading A, and fixes D3 for an asker that is not internal.
   - r120's q4 is written with another context's asker, so it is neither v17 nor a file problem.
4. **The v18 exemption covers only a request id that some request of this context is raised for.** The id must have the kind `request` and be named in a request's `raised_for`. Any other foreign id is still v18 wherever it is named.
   - Rests on design-model-check#r121: "other than the request a request is raised for". This settles notes Q5.
   - Every r121 row comes out the same either way.
5. **The v17 and v18 labels follow r120 and r121.**
   - v17: "a request neither is part of a job-thread, cites an origin nor is raised for a request".
   - v18: the r121 row's text, without "judged from the id alone" if the implementer keeps labels short. The "other than the request a request is raised for" part is kept.
   - Rests on design-model-check#r2 (each violation printed by its code and plain label) and the rows of r120 and r121.
   - Only `scripts/model.lp` writes the label (Implementation section). No test asserts either label (searched in `scripts`, `tests` and `docs`).
6. **The Retires removes the `@r115 @deprecated` scenario.** That is the scenario whose title the Retires quotes word for word. The `@r120` in the Retires is the scenario it is deprecated for.
   - Rests on the work-item's `## Retires` and on r115 being in the capability's `retired` list. This settles notes Q3 as reading A.
   - The `@r117 @deprecated` outline is not in the Retires, so it stays.
7. **The Givens of the scenarios:**
   - r120's q1 has another kind of `part_of` (the initiative, as today's Given) and no `source` or `raised_for`.
   - q3 is a request whose `part_of` is a job-thread id of this context.
   - q4 is a request from another context's asker whose only link is `raised_for` with the request id from the step.
   - r121's "no request is raised for it" writes nothing.
   - r121's "a request q9 of this context is raised for it" writes q9 under `.shop/work/requests/`. It has the scenario's context path, another context's asker, and `raised_for` naming the row's id.
   - Rests on r120, r121 and decision 3. This covers notes Q6: q9's form is valid under decision 3.

## 4. Tests the decisions break

None. What was checked:
- The notes (§4) collected `-k "v17 or v18 or foreign"` and found only the r120 test and the seven r121 rows. The deprecated r115 and r117 scenarios are not collected. The tests in `tests/scripts/test_model*.py` pass (42) and none asserts on v17, v18, `foreign`, "neither part_of nor source", raised-for or job-thread.
- The plan's own search found no test or doc that asserts the v17 or v18 label (decision 5).
- The `requests_*` writer refusal (`requests_write_steps.py:94`) checks `work request`, not `model`, and is not touched.
- Decision 3 changes `request_form` only for a request from an asker that is not internal and has `raised_for`. No existing Given writes such a request. The r112 scenario's "no asker" and "`work request` wrote" Givens are unchanged.
- Removing the old Given in `design_model_check_requests.py` breaks nothing: only the removed r115 scenario used it (searched in `features/`).

## 5. Open cases (for the implementer to name, not to choose)

- A `raised_for` naming an id whose kind is not `request`: is it a file problem, unresolved, or ignored? No scenario says.
- A `raised_for` naming a request of this context that does not exist: is it unresolved (r24 does not list `raised_for`)? No scenario says.
- A `part_of` job-thread id or `raised_for` id that names nothing is not printed unresolved. This is like D4 for `source`, which this work does not touch.
- D2 (`work request --raised-for` refused) belongs to requests#r29 and r44, not this work-item. Until it is delivered, only a hand-written request has `raised_for`.
- A request that has both `raised_for` and `part_of`/`source`, or several `raised_for` values.
