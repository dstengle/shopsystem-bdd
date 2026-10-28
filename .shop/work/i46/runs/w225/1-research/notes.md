# Research of w225: glossary-proposal gate, apply, done

Tools: `tools` ran `refs` only; `tests-of` has no map (`tools map` not run), so test lists are `by search`. Search is `by search`.

Requirements: supervision r161 r164 r165 r166 r167 r169 r170 r172 (accepted scenarios, 8 of them; r172 passes).

## 1. Why each scenario is red today

Command (run once): `python3 -m pytest -q --work-item w225`. Result: 8 failed, 180 passed, 1 skipped (run).

- r164 gate asks only on terms (`...a drafted glossary-proposal is given to a gate round...`): red, `StepDefinitionNotFoundError` on Given "i1's glossary-proposal g1 is drafted, its adds naming ... changes ... removes ..." (run). Missing step in `tests/scenarios/supervision_proposal_steps.py`. Code: `supervise_rounds.py` `Rounds.due` and `proposals` (lines 28-35, 53-56) only route `capability-proposal`, so no gate round ever starts for g1 (read).
- r170 gate row (`the gate round ... kept drafts`): red, missing Given "i1's glossary-proposal g1 is drafted" (run). Code path for the drafts line exists: `supervise_brief.py` lines 89-93 (read). Not routed (see r164).
- r170 apply row: red, missing Given "i1's glossary-proposal g1 is awaiting-answer, ... and its Answers section with ..." (run). Step at `supervision_proposal_steps.py:133` has regex `[^,]+` and the Examples row's comma phrasing does not match (read). Apply never routed (see r165).
- r169 (`gate round ends, the proposal is awaiting-answer`): red, missing Given "i1's glossary-proposal g1 is drafted" (run). Also no step for "the gate round gives the question "..." on g1" (`supervision_rounds_steps.py:61` matches p1 only, read). Code: `move` in `supervise.py` would write it, but it is never reached.
- r165 (`every question has an answer -> apply round given the answers`): red, missing Then "a round of the kind apply was started for g1, given the answers ..." (run). `supervision_rounds_steps.py:238` matches p1 only (read). Code: not routed (`due`).
- r166 (`apply ends -> approved`): red, missing Given "the apply round for g1 applies g1's drafts and gives DONE with a change list that adds the term "ledger" in the glossary" (run). Code: `workqueue.py:155` `own` set is `STATUSES` for a non-capability-proposal, and `approved` is not in it, so `workqueue.move` refuses approved (read). Also `supervise_change.py:59` `rewrite_lists` would empty g1's lists (see part 2).
- r167 (`apply ends -> no formulate`): red, same missing Given as r166 (run). Code: not routed; `AFTER` (`supervise_rounds.py:22`) would send approved to formulate for capability only.
- r161 (`glossary-only initiative set done`): red, missing Given "i1 is started, has neither a capability-proposal nor a work-item, and its glossary-proposal g1 is approved, its adds naming the term "ledger"" (run). Also missing Given "spec/index.md's Glossary holds the term "ledger", committed on the initiative branch" (read: `supervision_integrate_steps.py:49` takes three terms only). Code: `workqueue_done.py:36` needs a green work-item; `supervise_done.py:31` needs measurement and analysis (read).
- r172 (`awaiting-answer with an unanswered question -> no apply`): passes (run), but only because no glossary round is routed at all, so it cannot fail today (read).

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:Rounds.proposals, Rounds.due (l.28-57) | routes only `kind: capability-proposal`; a glossary-proposal gets no gate, apply or formulate round | r164, r165, r169, r170, r172 need the glossary-proposal routed through gate, awaiting-answer, apply | none (no map; by search: only r172 reaches it, passing) | read, refs (`glossary_proposals` at l.47, 37-39) |
| scripts/supervise_rounds.py:Rounds.run_round apply branch (l.157-169) and scripts/supervise_change.py:Changes.rewrite_lists (l.59-72) | apply calls rewrite_lists(name, applied); it keeps lists of entries whose capability equals `argues`; a glossary-proposal has none, so its lists become `[]` | r166, r167: g1 must keep its adds/changes/removes after apply | none | read |
| scripts/supervise_glossary.py:withheld (l.9-19), used by scripts/supervise_brief.py:86 | withholds terms of every glossary-proposal not `approved`, including g1 while g1 is applied | CONFLICT: r165/r166 apply g1's drafts while g1 is awaiting-answer; r55 withholds unapproved terms. Reading A: exempt the proposal being applied. Reading B: keep withholding and no apply can add the term, so r166 cannot hold | by search: `tests/scenarios/spec_integration_apply_steps.py:76` (r55 scenario, not read) | read, grep |
| scripts/workqueue.py:move l.155 (`own`) | glossary-proposal may move only to STATUSES; `approved`/`formulated` refused | r166 needs `approved` for glossary-proposal | none | read |
| scripts/workqueue_done.py:_holds (l.25-43) | needs a green work-item; ignores glossary-proposals; docstring says "has a work-item" | r161: initiative with no work-item is done once g1 approved and terms committed | by search: done scenarios in supervision_done_steps.py (r105) with work-items, none glossary-only | read |
| scripts/supervise_done.py:Dones.records_committed, set_done (l.17-36) | requires measurement and analysis record committed | r161: done "without a measurement" | by search: r105, r106, r109 (supervision_done_steps.py) | read |
| scripts/workqueue_answer.py:run l.45-55 | a non-capability-proposal is treated as a work-item: status from the log (asked_from) | r165 says the person's answers reach apply; a `work answer g1` would route g1 as a work-item | none (not in accepted scenarios: they write `## Answers` directly) | read |

## 3. Tests the requirements make impossible to keep

No test is shown to fail by these requirements in the run (8 red are missing steps). By search, no map:

- `tests/scenarios/spec_integration_apply_steps.py` (r55 scenario, line 68-76): keeps passing only under reading A above (withhold exempts the proposal being applied and not others). Not read in full; check before the plan.
- r172 (`supervision.feature`, passes now): stays green once routed, if due() holds it; no change needed.
- Done tests r105 (work-items withdrawn, not done): consistent with r161 (glossary-only is a different case). Sound by search.
- No other test found by search that asserts a glossary-proposal is not routed or not moved to approved (grep "glossary-proposal" in tests: only steps and the r55 scenario).

## 4. The file set

Production (must change):
- scripts/supervise_rounds.py (269 lines, room 31): route glossary-proposals in due/proposals; no rewrite_lists for glossary apply.
- scripts/supervise_change.py (140, room 160): rewrite_lists skips glossary-proposal (or keep lists when no `argues`).
- scripts/supervise_glossary.py (27, room 273) and scripts/supervise_brief.py (216, room 84): exempt the applied proposal (reading A, pending the person's choice).
- scripts/workqueue.py (294, room 6): glossary-proposal may move to approved/formulated; at 294 the room is six lines.
- scripts/workqueue_done.py (78, room 222): glossary-only initiative holds with no work-item when g1 approved.
- scripts/supervise_done.py (36, room 264): set_done without measurement for glossary-only initiative.
- scripts/supervise.py (293, room 7): on the move/commit path; change only if move needs a glossary branch.
- scripts/workqueue_answer.py (77, room 223): optional for `work answer` on g1 (not in accepted scenarios).

Tests (must change):
- tests/scenarios/supervision_proposal_steps.py (168, room 132): step "i1's glossary-proposal g1 is drafted, its adds ..."; widen regex at line 133-134 for "and its Answers section".
- tests/scenarios/supervision_rounds_steps.py (273, room 27): "the gate round gives the question ... on g1"; Then "a round of the kind apply was started for g1, given the answers".
- tests/scenarios/supervision_formulate_steps.py (90, room 210): "the apply round for g1 applies g1's drafts ... adds the term ledger in the glossary" (current step is for p1).
- tests/scenarios/supervision_done_steps.py (68, room 232): glossary-only initiative given; spec/index.md glossary holds "ledger" committed on the initiative branch.
- tests/scenarios/supervision_integrate_steps.py (246, room 54): one-term glossary Given (existing step takes three terms).

Modules on the change path, not edited: scripts/supervise_worker.py (259, room 41), scripts/supervise_outputs.py (103, room 197), scripts/supervise_faults.py (190, room 110).

Size check: `tools size --limit 300` printed no file over the limit (run).
