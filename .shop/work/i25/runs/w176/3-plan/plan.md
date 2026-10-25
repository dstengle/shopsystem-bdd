# Plan of w176: a reviewer's question answered with --change or --accept (work-queue r14, r26-r28)

From the research notes `.shop/work/i25/runs/w176/2-research/notes.md` (stage 1's read too), the capability
`spec/capabilities/work-queue.md`, `features/work-queue.feature` (lines 285-336) and the withdrawn w174 this redrafts.

## 1. What goes green

- **work-queue#r14**: "answer to a researcher's, a planner's or an implementer's question transitions the work-item
  to the status that stage started from" (outline, 3 rows). Green today (run); it must stay green. The reviewer
  branch below must not reach these three askers.
- **work-queue#r26**: "answer that asks for a change, to a reviewer's question, transitions the work-item to ready".
  Red: StepDefinitionNotFoundError for the When "…, saying that the answer asks for a change"; `scripts/work`'s
  `answer` has no `--change` (P2: argparse rc 2); `workqueue_answer.answer` would send it to `done` via `asked_from`.
- **work-queue#r27**: "answer that accepts the work-item as it is, to a reviewer's question, transitions the work-item
  to done". Red: no When step "…, saying that the answer accepts the work-item as it is"; no `--accept` (P3).
- **work-queue#r28**: "answer to a reviewer's question that says neither whether it asks for a change nor whether it
  accepts the work-item is refused, and nothing changes". Red: no When step "…, saying neither …", no Then step
  "work exits with an error, saying that the answer must say whether it asks for a change or accepts the work-item
  as it is"; and today the answer lands `done`, rc 0 (P1, defect D1). The Then "… and … are as they were" exists.
- **Retired**: the deprecated outline "answer on an awaiting-answer work-item transitions it to the status the asking
  stage started from (deprecated)" (work-queue @r14, feature 285-298). Its `a reviewer | done` row answers a
  reviewer with no verdict and expects `done`, which r28 refuses; see decision D3. w176.md has no `## Retires`
  section (w174, which this redrafts, had this very entry); the retirement is taken here as a decision.

## 2. Where the change lands

- `scripts/work`: the `answer` subparser takes `--change` and `--accept`; `cmd_answer` passes the verdict on to
  `workqueue_answer.answer`. Usage text names both flags.
- `scripts/workqueue_answer.py`: `answer` takes the verdict; for a work-item whose question a reviewer asked (the
  log's last move into `awaiting-answer` has `before` = `done`, the only stage that starts from `done`), it refuses
  without a verdict (r28, message per D4), moves to `ready` on `--change` (r26), to `done` on `--accept` (r27).
  The line-break check (r15) stays first. `asked_from` keeps its behaviour (D2).
- `tests/scenarios/work_queue_answer_steps.py`: the three When steps (change, accept, neither) and the r28 Then.
- `features/work-queue.feature`: the deprecated outline at 285-298 removed with `features retire` (D3).

Removed from the researcher's set: `scripts/supervise_answers.py` (D2: not edited) and
`tests/scenarios/test_work_queue.py` (it binds the feature with `scenarios()`, so retiring the outline drops its
test with no edit there; the new steps go to the steps module, as test_work_queue.py has 12 lines of room).
No file goes over 300 lines (work 169, workqueue_answer.py 59, steps 41).

## 3. Decisions

- **D1 (Q1) both `--change` and `--accept` given: refused, nothing changed.** r26 and r27 would ask for two
  transitions at once, `ready` and `done`; that is a change `work` cannot make, so r7 (exit with an error, say why,
  change nothing) settles it. The flags are one mutually exclusive choice; the refusal says the two flags cannot be
  given together. Rests on work-queue#r7, #r26, #r27 and the Implementation note naming the two flags.
- **D2 (Q2) the delegated answer path is left as it is.** r26-r28 name `work answer` only; the delegated path
  (`supervise_answers.py:79`, moving by `asked_from`) is supervision's behaviour (r77, r78) and w176 accepts no
  supervision requirement. So the reviewer branch is put in `answer`, not in `asked_from`, and `asked_from` keeps
  returning the asked-from status, `done` for a reviewer: the delegated path observes no change. Rests on
  work-queue#r26-#r28 (their scope) and supervision#r77/#r78 (not accepted here). The gap is in part 5.
- **D3 (Q3) the deprecated outline is retired, not rewritten.** Its "Deprecated for:" line names the r14 outline
  (feature 300) that w176 accepts; r14 as changed names only researcher, planner and implementer, and r28 refuses
  what its reviewer row expects, so its reviewer row cannot pass and its three stage rows are the r14 outline's.
  Rewriting a deprecated scenario's expectation would make it a fifth scenario for r28. Rests on work-queue#r14
  (changed), #r28; the same retirement w174 listed. Done with `features retire` on its exact title.
- **D4 r28's message** says that an answer to a reviewer's question must say whether it asks for a change (`--change`)
  or accepts the work-item as it is (`--accept`): the scenario's Then checks the stderr for that sense, the flags
  named so the person can act. Rests on work-queue#r28 and its Implementation note.
- **D5 (Q4) r27 as written: `--accept` gives `done`.** That `work run` then starts a review of a `done` item again
  is supervision's (STAGES in `supervise.py`), outside the accepted lines. Rests on work-queue#r27.
- **D6 the reviewer test is the log's `before` = `done`**, read the way `asked_from` already reads it (notes part 2:
  no other stage starts from `done`). A non-reviewer asker given `--change` or `--accept`: see part 5.

## 4. Tests the decisions break

- `tests/scenarios/test_work_queue.py::test_answer_on_an_awaitinganswer_workitem_transitions_it_to_the_status_the_asking_stage_started_from_deprecated`
  (4 rows): removed with the outline (D3). Its reviewer row expects what r28 refuses; its three stage rows are
  asserted by the r14 outline at 300, which stays.
- None other. Verified from the notes: the r13, r15, r24 answer tests use the default asker "an implementer"
  (test_work_queue.py:70-80), which the reviewer branch does not reach; the `started` map (`"a reviewer": "done"`,
  test_work_queue.py:79) is still the true before-status; supervision.feature:1044's Givens write the `ready` state
  directly and never run `work answer`; no test runs a delegated reviewer answer, and D2 leaves that path unchanged.

## 5. Open cases (for the implementer to name, not to choose)

- `--change` or `--accept` given on a researcher's, planner's or implementer's question, or on a capability-proposal
  (r24): the scenarios are silent; r14 and r24 say nothing of the flags.
- A delegated answer to a reviewer's question (`supervise_answers.py:79`) still lands `done` with no verdict (D2);
  the r28 refusal does not reach it. A supervision matter.
- An item accepted with `--accept` is `done`, and the next `work run` reviews it again (D5). A supervision matter.
- A reviewer's item whose log has a later non-reviewer shape (P9: `green -> awaiting-answer`) is no reviewer case.
- w176.md has no `## Retires` entry for the outline D3 retires; work run's drafting (`supervise_draft.retires`)
  did not carry w174's over.
