# Research of w220: spec-integration r54, r55

No `tools map` exists: `tools tests-of` and `untested` answer "no map". I did not make one. Every test list below is `by search`. `refs` ran for `entries`, `withheld` and `write_proposals`; it misses `self.`-method calls and imports, so the callers are `by search` too.

## 1. Why each scenario is red today

Command run once: `python3 -m pytest -q --work-item w220` (183 collected).
Result: 182 passed, 1 skipped, 56 subtests passed. Both accepted scenarios passed; nothing was red. The brief expected red; that does not hold.

- `@r54` "a round of the kind integrate ... gives the terms ... in the change list's entry for the glossary": green. `tests/scenarios/spec_integration_steps.py:84-86` gives the writer's reply the glossary entry already in it. The then-steps (`:108-124`) read the round's `result.json`. Nothing in production turns that entry into a file (see section 2).
- `@r55` "while the person has not approved the terms ... no round applies any of them": green. `tests/scenarios/spec_integration_apply_steps.py:68-73` writes `g1.md` by hand. The then-steps (`:101-111`) check that `spec/index.md` has no `refund` (true, because the stubbed writer writes nothing) and that the brief holds the withheld-terms sentence.

So the two scenarios pass without the mechanisms their requirements name.

## 2. Old assumptions

Places that handle the change list and the glossary, all found by `refs`/grep from `supervise_change.py`. Column "tests that execute it": no map, so `by search` lists the tests that name the place.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_change.py:entries (l.25-26) | accepts a `{"glossary": true}` entry with no `capability`; accepts `term/...` ids inside any capability entry | r54: terms belong only in the glossary entry; nothing checks a capability entry for `term/` ids | by search: tests/scenarios/spec_integration_steps.py:111-126 (fake reply only) | read, grep |
| scripts/supervise_change.py:write_proposals (l.102) | skips every glossary entry; writes capability-proposals only | r54 gives the glossary change; no glossary-proposal file is written, so r55 has nothing real to withhold | none (by search: no test asserts a glossary-proposal written from an integrate round) | read, grep `glossary-proposal` (only supervise_glossary.py) |
| scripts/supervise_change.py:rewrite_lists, merge_lists (l.58-91), write_proposals (l.93-128) | writes `adds`/`changes`/`removes` of a proposal from entries; capability ids `<cap>#r<n>` assumed | a term id inside a capability entry would be written into its proposal (old form) | by search: tests/scenarios/supervision_integrate_steps.py:32-38, :140-154; tests/scenarios/supervision_proposal_steps.py:99-106, :140-146 | read, grep |
| scripts/supervise_rounds.py:136-148 (integrate) | `found = entries(data)`; a round whose only entry is the glossary's counts as found, then writes no proposal | a glossary-only change list is silently dropped, not refused | none (by search) | read |
| scripts/supervise_rounds.py:153-165 (apply) | `applied = entries(data)`; `rewrite_lists` for the proposal; glossary entries ignored | r46/r114 unaffected; glossary terms of an apply list are dropped silently | none (by search) | read, grep |
| scripts/supervise_brief.py:12-16 CHANGE_LIST | the one sentence telling the writer glossary terms go in one entry and "in no capability's entry" | r54 is enforced by this prompt sentence alone; no code checks it | by search: tests/scenarios/spec_integration_steps.py:111 (checks the sentence is in the brief) | read |
| scripts/supervise_brief.py:83-86 (apply brief) | adds `supervise_glossary.text` only when `withheld` is non-empty | r55 is enforced by prompt text alone; nothing after an apply round checks that `spec/index.md` is unchanged (grep for `index.md` in supervise*.py: none) | by search: tests/scenarios/spec_integration_apply_steps.py:101-105 | read, grep |
| scripts/supervise_glossary.py:9-18 withheld | reads `kind: glossary-proposal` files in the initiative dir, status not `approved`, returns their `term/` ids | r55 reads these files; they are written by hand in the test only | by search: spec_integration_apply_steps.py:68-73 | read, refs (1 reference, supervise_brief.py) |
| scripts/supervise_glossary.py:17 | `if i not in terms` tests the outer list, so an id in both `adds` and `changes` repeats | minor: a term listed twice in one proposal is shown twice | none (by search) | read |

Reading of r54 for the plan: (a) keep accepting `term/` ids in capability entries and rely on the prompt; or (b) reject them in `entries`, which makes the test fixtures in section 3 the old form. Both are readings; the plan chooses.

## 3. Tests the requirements make impossible to keep

`tools tests-of` has no map, so this list is `by search`.

- tests/scenarios/supervision_integrate_steps.py:32-38 `entry()`: parses `and the term "ledger"` into the capability's entry. Under reading (b) of r54 it builds an input that is refused. Under (a) it passes unchanged.
- tests/scenarios/supervision_integrate_steps.py:140-154 `proposals_written`: expects `thing`'s proposal to hold `term/ledger` in `adds`. Same status: passes under (a); fails under (b).
- tests/scenarios/supervision_proposal_steps.py:99-106 `drafted_with`, :140-146 `gate_names_its_ids`: write and expect `term/ledger` in a capability proposal's lists. Same status.
- tests/scenarios/spec_integration_apply_steps.py:101-105 (r55): passes today, but only because the stubbed writer writes nothing. It would stay green if the guard were removed. Not impossible to keep; weak.
- tests/scenarios/spec_integration_steps.py:111-126 (r54): passes; the check reads the fake reply, so it would stay green if the entry were dropped in production.

Checked and sound: the r54/r55 scenarios themselves are unchanged by either reading; `supervise_outputs.py:88` already skips `term/` ids for formulate rounds, so it needs no change.

## 4. The file set

Production (none is named by the brief's file set; these are from the read above):
- scripts/supervise_change.py: write a glossary entry as a `drafted` glossary-proposal (kind, part_of, adds/changes/removes as `term/` ids) instead of skipping it at l.102; under reading (b), refuse `term/` ids in capability entries. Found by read of l.16-37, l.93-128.
- scripts/supervise_glossary.py: fix the duplicate test at l.17. Found by read.
- scripts/supervise_rounds.py: integrate and apply rounds given only a glossary entry should not be silent (l.136-148, l.153-165). Found by read.
- scripts/supervise_brief.py: CHANGE_LIST sentence and r55 line stay; change only if the plan adds a check. Found by read.

Tests:
- tests/scenarios/spec_integration_steps.py: r54 then-steps check the glossary-proposal file, not only `result.json`. Found by read.
- tests/scenarios/spec_integration_apply_steps.py: r55 test has the writer try to change `spec/index.md`, so the guard is exercised. Found by read.
- tests/scenarios/supervision_integrate_steps.py, tests/scenarios/supervision_proposal_steps.py: change only under reading (b). Found by search.

Modules on the path, with lines and room under the 300-line limit (CLAUDE.md gives it):
- scripts/supervise_change.py 128 lines, room 172
- scripts/supervise_glossary.py 27 lines, room 273
- scripts/supervise_brief.py 216 lines, room 84
- scripts/supervise_rounds.py 265 lines, room 35
- scripts/supervise_outputs.py 103 lines, room 197 (not edited)
- tests/scenarios/spec_integration_steps.py 224 lines, room 76
- tests/scenarios/spec_integration_apply_steps.py 142 lines, room 158
- tests/scenarios/supervision_integrate_steps.py 201 lines, room 99
- tests/scenarios/supervision_proposal_steps.py 152 lines, room 148
- features/spec-integration.feature 60 lines (not a Python file; no limit)

Line counts from `wc -l`. `git status --porcelain` was empty at the start and after the run; I wrote only this file and `result.json`.
