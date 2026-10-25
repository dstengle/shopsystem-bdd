# Research notes, w172 (fix the findings of branch review 1 of i28)

Accepts supervision#r102, r103, r104. Tools: `tools refs` ran; `tools tests-of` and `untested` had no map (`tools: no map`), and `tools map` would write into the checkout, so tests were found by search (`by search`). Checkout clean after my runs (`git status --porcelain` empty).

## 1. Why each scenario is red today

None is red. All four accepted scenarios pass today.

- `python3 -m pytest -q -p no:cacheprovider --tb=short <4 node ids of tests/scenarios/test_supervision.py>` gave `4 passed` (run).
- Node ids: `...test_an_accepted_request_this_context_is_the_upstream_of...work_start`, `...kept_drafts...whatever_that_initiatives_capabilityproposals_status_deprecated`, `...kept_drafts...whatever_that_initiatives_capabilityproposals_status`, `...the_gate_round_of_a_capabilityproposal...adds_changes_or_removes`.
- Only warnings: `PytestUnknownMarkWarning` for `@deprecated` (run).

So the work-item's accepted lines are already implemented. The work the findings ask for is a fix to them, not a new behaviour (part 6 and 7).

## 2. What the system answers today

Probe file: `.shop/scratch/w172-1-research/probe_supervision.py` (scratch only). Run with `python3 -m pytest -q -s -n0 -p no:cacheprovider .shop/scratch/w172-1-research/probe_supervision.py` (run). It calls the functions directly, not `work run`; see part 5 for the entry point not probed.

r102, `supervise_drafts.added_by_others` (run). Fixture: spec holds thing 1, 2, 5; i2 drafts thing 4, 5 (round 1) and 6 (round 2); i3 drafts other 1 (integrate round 2) and other 9 (apply stage); i4 drafts thing 3 (status started); i1 drafts thing 7 (own).
- for i1: `['thing#r4', 'thing#r6', 'other#r1', 'thing#r3']`. Held ids (thing 5) excluded; i1's own draft (7) excluded; apply-stage draft (9) excluded; every round of an integrate stage counted.
- for i2: `['thing#r7', 'other#r1', 'thing#r3']`. i2's own drafts excluded.
- no `spec/` at all: `['thing#r4', 'thing#r5', 'thing#r6', 'other#r1', 'thing#r3']`.

r103, `supervise_all.unfulfilled` (run). Requests q1 accepted, q2 accepted, q3 open, q4 accepted; i1 `fulfils: q2`; i2 `fulfils: request/c/q4` (path form).
- `['q1']`: q2 and q4 excluded, q3 not accepted.
- after i3 `fulfils: q1` with `status: abandoned`: `[]`. Any status of an initiative counts as fulfilling (read: `held` takes every initiative.md). Design as coded; it is not in the scenarios.
- q5 status `Accepted` (capital A): not listed, so not started. Strict match (run).

r104, proposal lists and the gate brief's lines (run). `workqueue.frontmatter` parses `adds: [thing#r4, term/ledger]` into a list, and `removes:` with nothing gives `None`, which the brief writes as `Removes: none`. Brief lines: `Adds: thing#r4, term/ledger`, `Changes: thing#r2`, `Removes: thing#r3`; for p2: `Adds: other#r1`, `Changes: none`, `Removes: none`.

Nearest cases not probed: a second `work run` of the same queue (the r103 "no second one" half is covered by `unfulfilled` above, read); a request whose upstream is another context (the requests dir holds only requests this context is upstream of, `spec/capabilities/requests.md:43-44`, read).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_brief.py:79` (`Briefs.integrate_lines`) | writes "Requirement ids other initiatives' kept drafts add, which spec/ does not hold yet; take none of them: …" | the integrate instructions (`agents/initiative-round.md:27`, `skills/integrating-a-proposal/SKILL.md:23`) look for a line named "Ids drafted elsewhere" and number added lines above every listed id; r43 says "above every id it is given". The label and the instruction differ | the three r102 scenarios, by search (`integrate_given_ids` only checks presence) | grep for "drafted elsewhere" and "take none" (read) |
| `scripts/supervise_rounds.py:103-105` (`Rounds.run_round`) | passes the gate round's questions to `move` as given, unfiltered | r104 asks the gate round to raise questions only on its proposal's lines and terms; the filter is only the brief's sentence (`supervise_brief.py:45-46`) | the gate scenarios, by search (`supervision_rounds_steps.py`) | read |
| `scripts/supervise_drafts.py:29` (`added_by_others`) | reads spec on the `root` checkout | r102 says "spec/ on the branch the integrate round starts from"; the two are the same only while the round starts from the checkout's branch | the r102 scenarios use the root checkout, by search | read |
| `scripts/supervise_all.py:18-35` (`unfulfilled`, `run_all`) | starts `work start` for every accepted request no initiative fulfils, in no-initiative mode only | r103 lines the same start; `work start` by hand (`scripts/work:84`) is the other way in | r103 scenario; `work start` CLI by search (`tests/scenarios/work_queue_start_steps.py`) | refs of `workqueue_start.start`: `supervise_all.py:35`, `scripts/work:84` |

## 4. Tests the requirements make impossible to keep

tests-of: no map; by search.

- `tests/scenarios/test_supervision.py`, the deprecated r102 test (`..._status_deprecated`): passes today. It is the old r102 scenario, tagged `@deprecated` in `features/supervision.feature:1239-1250`; the step `other_initiative` (`tests/scenarios/supervision_integrate_steps.py:144-155`) exists for it. Its brief check is presence-only. Retiring it (finding 3 of the branch review) would remove the test; it does not fail today. The findings file says w171 changed only the draft path in that step.
- `integrate_given_ids` / `integrate_not_given` (`supervision_integrate_steps.py:175-187`): pass; they check the brief has the ids, not the label the round reads. A label fix needs a new assertion.
- Verified and sound: `tests/scenarios/supervision_intake_steps.py:72-80` (`work start` for q1 and not q2), `supervision_proposal_steps.py:104-110` (gate brief has the ids, not thing#r1 or other#r1). Both pass (run).
- None of the tests assert the old label text (`grep` for "take none" and "drafted elsewhere" in `tests/`: no hit, by search).

## 5. A step the work-item skips

The new path in `run_all` is `workqueue_start.start` called from `supervise_all.py:35`, with no `Run.check()` before it for the new initiative and no `lock`. The existing `work start` (`scripts/work:84`) goes through the same function, so its refusals are the same: "no request", "not accepted" (`workqueue_start.py:28,32`). Effects only the start produces: an `initiative.md` with `status: proposed` under `.shop/work/i<n>/` and a commit "work: start i<n>, fulfilling q<n>". Read; the entry point was not probed (a `work` repo in scratch would need git setup). Its refusal after an earlier start has committed leaves the earlier one (read; see the branch review's observation).

## 6. Defects

### 6.1 The integrate brief's label is not the one the round reads (read)
- Code: `scripts/supervise_brief.py:79`: "Requirement ids other initiatives' kept drafts add, which spec/ does not hold yet; take none of them: <ids or none>".
- Instructions: `agents/initiative-round.md:27` ("its "Ids drafted elsewhere"") and `skills/integrating-a-proposal/SKILL.md:23` ("the brief lists requirement ids that other initiatives' drafts add (its "Ids drafted elsewhere"), the first added row of a capability also goes above every listed id").
- Effect: the round is not told to number above the listed ids; it is told "take none of them", which allows a lower free id (r43 says above every id given).
- Read, not run: no probe drives an integrate session.

### 6.2 Nothing filters a gate round's questions (read)
- `scripts/supervise_rounds.py:103-105` passes the questions through. The only limit is the brief's instruction. Read.

## 7. The file set

Production and test files the fix must change (to make the findings' fixes; the accepted scenarios already pass):
- `scripts/supervise_brief.py` (143 lines, room 157): line 79 label and "take none" wording (6.1); line 3 import order and line 82 ISC004 (ruff, branch review finding 4). Found by grep and the findings file.
- `agents/initiative-round.md` or `skills/integrating-a-proposal/SKILL.md` (not counted, not Python): only if the plan reconciles the label on their side, not the code's.
- `features/supervision.feature` (lines 1239-1250): retire the deprecated r102 scenario (finding 3) through a work-item's `## Retires`. Found by `features deprecated` in the findings.
- `tests/scenarios/test_supervision.py` (258 lines, room 42): removes the deprecated test function when retired. Found by the collect-only listing.
- `tests/scenarios/supervision_integrate_steps.py` (188 lines, room 112): drop `other_initiative` once retired; add a label assertion (6.1); ruff on line 107 and 112. Found by grep.
- `tests/scenarios/supervision_intake_steps.py` (80 lines, room 220): ruff line 65 (FURB167).
- `tests/scenarios/supervision_proposal_steps.py` (116 lines, room 184): ruff line 96 (RUF100).
- `tests/scripts/stub_claude.py` (ruff lines 186, 187, FURB167): the stub's brief label if it reads one; found in the findings file.
- `CLAUDE.md` line 32 (module map row for `scripts/supervise_all.py`, 44 lines; the size rule gives no limit for markdown): add r103 to the row (finding 2).

Modules on the change path, edited or not:
- `scripts/supervise_drafts.py` 32 lines, room 268 (r102 reader; not edited unless 6.1 moves the label).
- `scripts/supervise_all.py` 84 lines, room 216 (r103).
- `scripts/supervise_rounds.py` 134 lines, room 166 (gate and integrate rounds).
- `scripts/supervise_change.py` 52 lines, room 248 (change list written as drafted proposals).
- `scripts/workqueue_start.py` 53 lines, room 247 (`work start`).
- `scripts/workqueue.py` 290 lines, room 10 (`requests`, `frontmatter`, `committed`; no edit needed; little room).
- `scripts/supervise.py` 248 lines, room 52 (the stage path).
- `scripts/supervise_intake.py` 112 lines, room 188.

Limits: the 300-line limit from `CLAUDE.md`, "Size limit"; `tools size` not run (its check is the same count).
