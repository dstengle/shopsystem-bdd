# Plan of w150: Retires covers a requirement named through a range (supervision#r73)

## 1. What goes green

**supervision#r73**: when `work run` drafts a work-item for a formulated capability-proposal, its `## Retires` lists each `@deprecated` scenario whose `@r<n>` names a requirement the work-item accepts.

- "a work-item drafted for a formulated capability-proposal lists under its Retires each deprecated scenario of a requirement it accepts" (features/supervision.feature:898). **Passes today** (notes §1). It must stay green.
- "a work-item drafted for a formulated capability-proposal whose changes name a range lists under its Retires each deprecated scenario of a requirement in the range" (features/supervision.feature:907). **Red today.** It fails at the Then in tests/scenarios/supervision_proposal_steps.py:72 because "it used to wait" is missing from Retires. There are two causes (notes §1, D1 and D3):
  1. `Drafts.retires` in scripts/supervise_draft.py (line 30) keeps the accepted text `r3-r6` and compares it to the `@r4` tag by equality, so nothing matches.
  2. The step helper `named` in the step module (line 17) reads `thing#r3-r6` as `thing#r3`. The fixture proposal therefore never carries the range. Even a `retires` that reads ranges would find no `r4`.

Retired scenarios: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/supervise_draft.py`: `Drafts.retires` reads each accepted entry as the set of requirement ids it names. A single id gives itself. A range `r<a>-r<b>` gives each id from a to b. It then matches the `@deprecated` scenarios' `@r` tags against that set. Nothing else in the file changes. `draft_proposals` still copies `accepts` as written, range text included (notes §3).
- `tests/scenarios/supervision_proposal_steps.py`: the helper `named` keeps a trailing `-r<m>`. "changes naming thing#r3-r6" then writes `changes: [thing#r3-r6]`. Single ids and lists of ids ("thing#r1 and thing#r2") read as they do today.

This is the researcher's set, unchanged. The modules on the path (supervise.py, workqueue.py, model_parse.py, features_gherkin.py, supervise_brief.py, test_supervision.py) are not edited. Both edited files have more than 200 lines of room under the 300-line limit.

## 3. Decisions

- **D-a. A range in accepts means every requirement from its first id to its last, both included.** `retires` reads it the same way the other readers already do (`model_parse.expand`, `supervise_brief.accepted_scenarios`, `work_items.requirements`; notes §3 and §5). Reuse the existing expansion, `model_parse.expand`, instead of writing a third copy. It is imported, not edited. This rests on supervision#r73 ("a requirement the work-item accepts", where accepts holds ranges), and the range scenario pins the reading.
- **D-b. Only the requirement-id part of each accepted entry is matched against tags.** The entry is the part after `#`, expanded. This is the same scoping `retires` already uses: it reads only `features/<capability>.feature` of the work-item's own capability. Rests on supervision#r73.
- **D-c. The fixture's Given keeps the range text exactly as the scenario states it.** It is a fixture fix (D3), not product behaviour. The r72 Givens that share `named` keep their single-id output. Rests on the range scenario's own Given.
- **Duplicate listing (notes D2) stays as it is.** A scenario tagged for two accepted ids is still listed once per matching tag. No scenario covers this case, and the work-item does not ask for it. Changing it would change the Retires lines the narrator sees, so it is left as an open case, not decided here.

## 4. Tests the decisions break

None. The notes searched tests/ for range texts (`#r\d+-r\d+`). They appear only in tests/scripts/test_model_reading.py (proposal parsing) and tests/scripts/test_work_items.py (the plugin option), and neither reaches `retires`. The equality scenario keeps passing: `r4` is listed and `r8` is still excluded. The r72 scenarios go through `retires` with single ids only, and `named` gives them the same ids as before (D-c). Nothing asserts the duplicate listing.

## 5. Open cases (for the implementer to name, not to choose)

- A scenario tagged `@deprecated` with two `@r` tags that both fall inside an accepted range (or under two accepted ids). Today it is listed once per tag (D2). The scenarios do not say whether it should be listed once.
- A reversed or malformed range in accepts (`r6-r3`, `r3-`). `retires` follows whatever `model_parse.expand` gives for it. The scenarios do not cover it.
- An accepted entry whose capability differs from the work-item's `under`. `draft_proposals` groups by capability, so this should not arise. The scenarios do not cover it.
- The stderr line seen on the failing run, "…4-review/session.json is not a session.json of a shape measure knows" (notes §6). It is unrelated to r73. Name it if it still appears once the scenario is green.
