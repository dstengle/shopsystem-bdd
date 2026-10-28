# w222 research: supervision r171, r172

Method: pytest run once (`run`). Code and tests located by Grep and Read (`read`, `by search`). `tools refs` used for `withheld`, `entries`, `write_proposals`. `tools tests-of` and `untested`: no map (`tools map` runs the whole suite, not run), so every test list is `by search`.

## 1. Why each scenario is red today

Command (`run`): `python3 -m pytest -q --work-item w222`. Result: 2 failed, 180 passed, 1 skipped. Both accepted scenarios fail at their first Given with pytest-bdd `StepDefinitionNotFoundError`; no later step ran.

- **r171** (features/supervision.feature:1516; test_supervision.py `test_an_integrate_round_that_ends_with_a_change_list_naming_the_glossary_...`). Undefined first Given: `spec/index.md's Glossary holds the terms "shelf", "loan" and "reader"` (line 1518). Later steps are also undefined (`read`, by search): the change-list Given is defined only for lines ending "on thing" (tests/scenarios/supervision_integrate_steps.py:41, supervision_formulate_steps.py:43); no step matches "the commit that wrote i1's glossary-proposal wrote one, drafted ..." or "names the term ... in none of its adds, changes and removes". Code: no code writes a glossary-proposal. `Changes.write_proposals` (scripts/supervise_change.py:102) skips every glossary entry; `supervise_rounds.py` `run_round` (l.196) has no glossary writer. Grep of `glossary-proposal` in scripts/ finds only supervise_glossary.py (read side). With the steps defined, the Then would fail: no glossary-proposal file in the round's commit.
- **r172** (features/supervision.feature:1800; test_supervision.py `test_a_glossaryproposal_awaitinganswer_...`). Undefined first Given: `i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with ... given by its gate round, and its Answers section with "One file." only` (line 1802). The answered-proposal Givens match only `capability-proposal p1` (tests/scenarios/supervision_rounds_steps.py:21-33, supervision_given.py:247). Undefined Then: `no round of the kind apply was started for g1` (line 1805); defined Thens cover integrate (supervision_rounds_steps.py:179) and formulate (supervision_reintegrate_steps.py:83) only. Code (`read`): `Rounds.due` and `proposals()` (supervise_rounds.py:33, 49-52) route only kind `capability-proposal`, so no apply round is started for any glossary-proposal today. The Then holds by absence; the Answers-versus-Questions check (l.50-51) exists for capability-proposals only.

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_change.py:Changes.write_proposals (l.102) | skips glossary entries; writes one drafted capability-proposal per capability | r171: also writes one drafted glossary-proposal from the glossary entry, returned so the round commits it | by search: supervision_integrate_steps.py:140-155 (capability entries only); glossary skip not checked | refs (l.93, 0 refs); read |
| scripts/supervise_change.py:entries (l.16) | reads glossary entries as `capability: None, glossary: True` | none: already yields the entry the writer needs | by search: spec_integration_steps.py:85 | refs (17 refs); read |
| scripts/supervise_change.py:Changes.unknown (l.43) | glossary entries never counted as unknown capabilities | none | by search: not checked | read |
| scripts/supervise_rounds.py:run_round, integrate (l.137-148, 194-201) | glossary-only list counts as a change list (r96); written proposals joined into the round's commit | the glossary file must join `also` in the same commit | by search: supervision_integrate_steps.py (capability cases) | read |
| scripts/supervise_rounds.py:Rounds.due (l.42-43) | r93: started, no proposal, no work-item, so integrate again | `proposals()` ignores glossary-proposals: a started initiative whose only output is one gets integrate every run (reading R1a); under R1b it does not | none (by search: no step puts a glossary-proposal under a started initiative) | read (l.33) |
| scripts/supervise_rounds.py:Rounds.proposals, due (l.33, 49-52), AFTER (l.22) | routes only capability-proposal kind; Answers-versus-Questions check on those | r172's guard must hold for glossary-proposals once r165 routes them; today the apply Then holds vacuously | none (by search) | read |
| scripts/supervise_glossary.py:withheld (l.9-18) | terms of non-approved glossary-proposals withheld from apply briefs | none for r171/r172 | by search: spec_integration_apply_steps.py:68-111 | refs (supervise_brief.py:86 via import); read |
| scripts/supervise_brief.py:CHANGE_LIST (l.12-16) | tells the integrate round: terms in the glossary entry only, in no capability's entry | sets the form the writer receives; see reading R2 | by search: none asserts its text except spec_integration_steps.py:111 | read |
| tests/scenarios/supervision_integrate_steps.py:entry (l.32-38), proposals_written (l.140-155) | puts `term/ledger` into capability thing's `adds` | conflicts with the brief's CHANGE_LIST under R2 reading B | by search: this test | read |

## 3. Tests the requirements make impossible to keep

By search (no map). None fails as it stands.
- tests/scenarios/supervision_integrate_steps.py:140-155 (`proposals_written`): asserts `term/ledger` in capability thing's adds. Passes under reading R2-A (writer keeps ids as today). Fails under R2-B (term ids dropped from capability entries): line 150 would change. Undecided here.
- tests/scenarios/spec_integration_apply_steps.py:68-111 (withheld line in apply brief): sound, `withheld` is unchanged.
- tests/scenarios/spec_integration_steps.py:85-126 (glossary entry given to an integrate round): sound; checks the kept changes' glossary entry, which the new writer does not alter (`by search`).
- No test asserts that glossary entries are dropped, nor that a started initiative with only a glossary-proposal is re-integrated: none by search.

Readings the planner must choose between (not decided here):
- R1 (r93, supervise_rounds.py:42-43): a started initiative whose only output is a glossary-proposal. (a) Literal: it has neither a capability-proposal nor a work-item, so integrate runs again each `work run`. (b) The glossary-proposal counts as its output, so no integrate round. The r161 scenario (features/supervision.feature:1850) has the same shape; not verified.
- R2 (brief CHANGE_LIST, writer): (A) term ids stay in a capability's entry as today, test line 150 holds. (B) they are dropped there, test line 150 changes.
- R3 (r172): the glossary apply route is not built by this item (r165 is not accepted here). When r165 lands, `due()` must count the glossary-proposal's Answers against its Questions, which `due()` does for capability-proposals only.

## 4. The file set

Production:
- scripts/supervise_change.py: `write_proposals` writes one drafted glossary-proposal per glossary entry (adds, changes, removes as `term/` ids), returned for the commit. Read l.93-128; `refs write_proposals`.
- scripts/supervise_rounds.py: `run_round` integrate passes the glossary entries to the writer (l.196-201). Read l.137-148, 194-201. `due()` unchanged for r171/r172 as the code stands.

Tests:
- tests/scenarios/supervision_integrate_steps.py: Given for the glossary change list and spec/index.md's glossary; Then on the glossary-proposal's commit. Read l.32-60, 140-155.
- tests/scenarios/supervision_proposal_steps.py: Given for an awaiting-answer glossary-proposal with questions and answers; Then no apply round for it. Read whole file's Given/Then pattern (l.1-152, `by search`).
- tests/scenarios/test_supervision.py: no change; both scenario bindings already exist (the run named them).

Conditional on R1 or R2 (not in the file set unless chosen):
- tests/scenarios/supervision_integrate_steps.py:150 (R2-B only).
- scripts/supervise_rounds.py:42-43 `due()` (R1-b only).

Optional, not required: scripts/supervise_glossary.py (27 lines) could hold the writer, since it already reads the glossary-proposals.

Modules on the change's path (line counts `wc -l`; room under the 300 limit of CLAUDE.md, which gives it for every tracked Python file; `tools size --limit 300` printed no file over it):
- scripts/supervise_change.py: 128 lines, room 172. Edited.
- scripts/supervise_rounds.py: 265 lines, room 35. Edited.
- scripts/supervise.py: 293 lines, room 7. Read only (`Run` mixes in `Changes` and `Rounds`); any edit there needs a split first.
- scripts/supervise_brief.py: 216 lines, room 84. Read only (CHANGE_LIST, l.12-16).
- scripts/supervise_raise.py: 84 lines, room 216. Read only (`raise_requests` returns empty for a result with no `requests`).
- scripts/supervise_glossary.py: 27 lines, room 273. Read only.
- tests/scenarios/supervision_integrate_steps.py: 201 lines, room 99. Edited.
- tests/scenarios/supervision_proposal_steps.py: 152 lines, room 148. Edited.
