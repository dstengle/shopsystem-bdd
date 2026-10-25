# w193 research notes

Method: no coverage map (`tools tests-of` answers "no map"), so every count below is `refs` or `by search`. Probes ran
through `scripts/work run i1` with the stand-in claude, in `.shop/scratch/w193-1-research/` (gitignored). Tests ran
by node id. Nothing under the checkout changed (`git status --porcelain` is empty at the end).

## 1. Why each accepted scenario is red today

None is red. Command: `python3 -m pytest -q "tests/scenarios/test_supervision.py::<node>"`, one run per node, all
`run`, all `1 passed`:

- r111 `test_an_initiative_that_a_workitems_transition_leaves_able_to_be_done_is_set_done_before_work_run_ends`
- r70 `test_a_capabilityproposal_whose_every_question_has_an_answer_is_given_to_an_apply_round_with_its_answers`
- r116 `test_a_capabilityproposal_whose_every_question_from_its_formulate_round_has_an_answer_is_given_to_a_formulate_round_with_the_answers`
- r114 `test_when_the_apply_round_..._the_proposals_adds_changes_and_removes_are_written_from_the_change_list_the_round_applied`
- r83 `test_when_the_formulate_round_..._ends_without_giving_a_question_the_proposal_is_formulated`
- r112 `test_when_the_formulate_round_..._gives_questions_each_is_written_under_the_proposals__questions`
- r113 `test_when_the_formulate_round_..._gives_a_question_the_proposal_is_awaitinganswer`
- r115, all four Examples: `test_when_the_gate_round_of_a_capabilityproposal_ending_..._[gives BLOCKED ...]`, `[ends in an error]`, `[ends at its turn limit]`, `[ends with no error ... no result file]`

The code behind them already exists: `scripts/supervise_rounds.py` (`AFTER`, `due`, `route`, `run_round`), `supervise_change.py`
(`rewrite_lists`), `supervise.py` (`pull_through` defers a refused round), `supervise_done.py`. Commits `ce5c1bfb`
(r83, r112 to r115) and `968344f4` (r107 on apply, rounds go on past a refused one) carry them.

## 2. What the system answers today

Probes: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w193-1-research/probe_rounds.py` (three tests) and
`probe_reask.py` (one). Each `run`. Stand-in plans: `round:apply` / `round:formulate` as DONE, the given fields below.

- P1, the nearest case of r114: apply round DONE with no `changes`, p1 `awaiting-answer` with adds `thing#r4`, `thing#r5`,
  question "Is thing#r5 kept?" answered "No.". Result: `RC 0`. p1 goes approved, then formulated, keeping
  `adds: [thing#r4, thing#r5]`. The formulated proposal then draws work-item w1, which accepts thing#r5 that the answer
  "No." refused. The lists are not written; the round is taken as a no-op.
- P2, nearest case of r114: apply round DONE with `changes` naming only `other` (`other#r1`), p1 argues `thing`. Result:
  `RC 0`, silent. p1's `adds`, `changes`, `removes` all become `[]`; `other#r1` is written nowhere; no w1 drafted.
- P3, nearest case of r70: p1 `awaiting-answer` with no `## Questions` and no `## Answers`. Result: `RC 0`. An apply
  round starts (every question answered holds vacuously), then approved, formulated, w1 drafted.
- P4, nearest case of r112/r113: p1 `approved` went to `awaiting-answer` by a formulate question, the answer "One place."
  given, the formulate round asks "Are returns counted?". Result: `RC 0`, stdout empty. p1 stays `awaiting-answer`; the
  question is appended under `## Questions`; the commit is `work: p1 awaiting-answer -> awaiting-answer`; log.jsonl gets
  no line for it.
- Read, `scripts/supervise.py:231-244` (`show`): the exit code counts work-items only, so a run whose only waiting node
  is a proposal exits 0 (P4 shows it).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_rounds.py:19 `AFTER` | approved always goes to formulate, then formulated | r71 keeps it; r116 and r83 need `route` to choose | r116, r83, r113 nodes (by search) | refs: 2 uses, lines 47, 61 |
| supervise_rounds.py:52 `route` | awaiting-answer answered goes to apply, unless the last log move into it came from approved | r116: from approved, to formulate | r116 and r83 nodes execute it; no test pins it (review F5) | refs: 1 use, line 49 |
| supervise_rounds.py:34 `due` | answered means as many answers as questions, zero included | unchanged; P3 shows zero questions counts as answered | r70, r116 nodes (by search) | refs: 4 uses (intake's `due` is its own function) |
| supervise_rounds.py:135-147 apply branch | a DONE apply with no `changes` leaves the lists as drafted (`if applied:`) | r114: lists written from the change list the round applied | r114 node (by search); it uses the stand-in's `fields`, not the real brief | read |
| supervise_change.py:53 `rewrite_lists` | writes only entries naming `argues`; the others are dropped, lists emptied | r114 names what was applied | r114 node (by search) | refs: 0 uses in tests |
| supervise_rounds.py:148-156 formulate branch | a formulate question with before `awaiting-answer` is committed with no move and no log line | r112 needs questions written; P4 | r112 node (by search) | read |
| supervise.py:201-229 `pull_through` | a refused round is raised after draft and pull | r111, r115 defer it; the branch review and `set_done` wait for the next run (review F6) | r115 nodes (by search); supervise_all.py:65 also calls it | refs |
| supervise.py:231-244 `show` | exit 0 when every work-item is green or withdrawn, proposals not counted | a proposal `awaiting-answer` ends the run with no error (P4) | none found by search | read |
| supervise_brief.py:47-51, :78-91 | the apply brief has no change-list line; only `integrate_lines` gives the `changes` form | r114 needs the real apply round to give `changes` | none found by search | read |
| agents/initiative-round.md:32-33 | apply reply is "under eight lines"; no `changes` field | r114 needs it | none (agent text) | read |

## 4. Tests the requirements make impossible to keep

Searched by search, since there is no map. Read each of the 11 accepted nodes (above): all pass, so none is broken.
Searched `tests/scenarios/` for assertions on the old behaviour (apply with no list left alone, approved to formulated
without a log, `show` exit 0 on proposals): none found. Deprecated scenarios: old r83 removed in `ce5c1bfb`; `@r75`,
`@r102`, `@r105` deprecated before this work-item (not w193's). Result: **none** can no longer pass. But the r114
node passes only because its stand-in gives `fields.changes` (`supervision_formulate_steps.py:35-37`): it does not test
the real apply brief. A fix to Finding 1 would keep it green without proving it.

## 5. A step the work-item skips

The formulate-question path (`supervise_rounds.py:150-154`) writes the questions and commits with `self.commit`, not
`self.move`. Effects only that step produces, from P4 (`run`): the question is written; the commit message is
`awaiting-answer -> awaiting-answer`; no log.jsonl line; the status is unchanged; the commit is pushed (`commit()`
pushes by default). The existing way (`move`) logs the transition and does not commit to the same status.

## 6. Defects

Each reproduced by `run`; the probe is in `probe_rounds.py` / `probe_reask.py`.

### D1. An apply round's `changes` is never given by the real round (Finding 1 of the branch review)
- Reproduction: P1 above. `RC 0`, the proposal keeps `adds: [thing#r4, thing#r5]` after "No." on thing#r5.
- Read: `supervise_brief.py:47-51` and `:78-91`; `agents/initiative-round.md:32-33`.
- The branch review names this; the stand-in's `fields` hides it.

### D2. An apply list naming only other capabilities erases the proposal's lists silently
- Reproduction: P2 above. `RC 0`, stdout empty; `other#r1` written nowhere.
- Both readings: "the lists become what the list gives for `argues`" (the code) or "a list that names no `argues` is
  refused or left alone" (the review, F2).

### D3. `work run` exits 0 while a proposal waits on an answer
- Reproduction: P4 above. `RC 0`, stdout empty; the question sits in `p1.md` only.
- Reading A: a defect, since r32 and r81 make waiting work-items an error. Reading B: a gap, since r9 counts work-items
  only and r101 covers requests only. The spec is silent.

### D4 (minor). A proposal awaiting-answer with no question goes to apply
- Reproduction: P3. Reachable only by hand-editing: gate and formulate always write a question.
- Read: `supervise_rounds.py:47-48`.

## 7. The file set

Scenarios: no file has to change for the 11 to pass (all pass today). Everything passing today keeps passing if the
files below change as their findings say. The findings are branch review 1's (`.shop/work/i31/runs/branch-review/1/findings.md`),
which the work-item cites.

Files to change for the findings:
- `agents/initiative-round.md` (61 lines, markdown, no room rule): the apply reply gives `changes` in the integrate form. Read, lines 32-33.
- `scripts/supervise_brief.py` (167 lines, room 133): the apply brief names the `changes` form, as `integrate_lines` does. Read, lines 47-51, 78-91.
- `scripts/supervise_rounds.py` (192 lines, room 108): decides whether a DONE apply with no list is a no-op (D1) or an error as r96 is. Read, lines 135-147.
- `scripts/supervise_change.py` (88 lines, room 212): `rewrite_lists` leaves the lists or refuses when no entry names `argues` (D2, F3). Read, lines 53-66.
- `features/supervision.feature` (1513 lines, no limit): a scenario for a real apply round's change list (D1) and for D3 if the spec wants it. Search: r114 scenario, `:975`.
- `tests/scenarios/supervision_formulate_steps.py` (82 lines, room 218): the r114 Given's stand-in fields pin only the stand-in. Search, `:35-37`.

Modules on the change's path, edited or not:
- `scripts/supervise.py` (271 lines, room 29): `pull_through`, `show` (D3, F6). Read.
- `scripts/supervise_all.py` (83 lines, room 217): calls `pull_through` per run. Refs.
- `scripts/supervise_worker.py` (251 lines, room 49): reads the apply result (`outcome`). Read.
- `scripts/supervise_draft.py` (81 lines, room 219): drafts from a formulated proposal's lists (P1's w1). Read.
- `scripts/supervise_done.py` (36 lines, room 264): `set_done` from r111. Read.
- `tests/scenarios/test_supervision.py` (261 lines, room 39): the node ids run. Run.
- `tests/scenarios/supervision_rounds_steps.py` (288 lines, room 12): the apply-round steps; no room for growth. Search.

Size: `tools size --limit 300` printed nothing, so no tracked Python file is over the limit now. CLAUDE.md gives the
300-line limit. Also stale and not on the critical path: `supervise_rounds.py:1-6` docstring (review finding 8);
CLAUDE.md's `scripts/supervise_change.py` row (review: it names no apply list).
