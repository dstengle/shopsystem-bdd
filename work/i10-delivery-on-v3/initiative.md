---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i10
title: Delivery on design model v3
summary: Work-items pulled through their stages by a script supervisor, with a claude -p worker for each stage and only the supervisor writing status.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 1
source: [review-finding/2026-10-13-kb-and-bdd-assessment, measurement/kb-batches-32-35]
date: 2026-10-19
---

The final state of delivery, in place of i4, i5, i6 and i7 (abandoned 2026-10-19). No intermediate stage:
the person's direction of 2026-10-19 (observation/2026-10-19-final-state-only).

## Why

The assessment of 13 October and kb batches 32-35: the controller session read 23-55% of a batch's cache and its
own turns were the span the agents did not use; rules asked of it (models, review by risk, fresh agents, one
batch a session) did not hold; Lands was exceeded in 15 of 23 slices for 790k tokens of sizing scouts; nothing in
the build layer named a capability, and reports, findings and notes were git-ignored and lost. The design model's
answer is the work-item, the work-queue and a supervising script. This initiative builds that, and removes what it
replaces.

## The final state

An initiative's capability-proposals are approved, merged and formulated as before. Then:

1. **The person asks to deliver it.** `delivering-an-initiative` (capability/delivery) drafts work-items from the
   formulated proposals with `work add`, reading only `spec/`, `features/` and `.shop/work/`: each added or changed
   requirement accepted by one work-item, one unknown each, a risk (`contract`, `concurrency`, `data`, `none`),
   `blocked_by` only where scenarios need another's work, deprecated scenarios under Retires. It commits them, shows
   one table, and starts `work run` in the background. It reads nothing workers write.
2. **`work run <initiative>` supervises** (capability/supervision, design-decision/a-script-supervises-delivery).
   Stage by stage it starts a fresh `claude -p --agent shopsystem-bdd:<agent>` worker with one brief file:

   | status | worker | result → status |
   |---|---|---|
   | drafted | `code-scout` (researcher) | DONE with a file set → researched |
   | researched | `bdd-planner` (new) | DONE → planned; QUESTION → awaiting-ruling |
   | planned | none: the guard | blockers green, no claimed file set overlapping → ready |
   | ready | `bdd-implementer`, in `.shop/worktrees/<item>/` | claimed; DONE → rebased, tested, merged → done; PARTIAL → continuation; BLOCKED, HAND-BACK, NEEDS_CONTEXT → awaiting-ruling; a refused `work claim` → ready |
   | done, risk named | `bdd-task-reviewer` | nothing to fix now → green |
   | all done | `bdd-branch-reviewer` from the initiative's base | nothing to fix now → each done item green |

   A worker's outcome is only its `result.json` (design-decision/worker-results-are-files); a missing or malformed
   one is a failed stage, retried once, then a question. Findings to fix now become fix work-items (`fixes:`,
   `findings:`), followed by a scoped re-review; other findings become observations; every review is a
   review-finding record. Each worker has a time and dollar limit by role, and the run has a budget
   (`.shop/delivery.toml`). Only `work run` writes status: a worker that touches `.shop/work/` has its change put
   back and its stage failed.
3. **The person is asked only at the end.** When nothing can move, `work run` exits (0 all green, 3 a question, 4
   a budget) printing each question with its readings and the `work rule` command. The session shows them, records
   the person's answers in their words with `work rule`, and starts `work run` again. A question about a scenario
   goes to formulation or integration first.

`scripts/work` (capability/work-queue) is the queue the supervisor runs on: `add`, `show`, `next`, `claim`,
`questions`, `rule`, `withdraw`, `log`, `step`, `run` and `plugin`, which writes `work_expectations.py`: a
scenario of a work-item not yet claimed is a strict expected failure, so the suite is green between work-items.

**What it records, for i12.** Per initiative, `.shop/work/<initiative>/log.jsonl`: the base commit; every move
(time, item, before, after, by whom, why); every worker start and end (item, stage, attempt, agent, model, session
id, result status, exit, duration, cost, tokens from `claude`'s JSON); every suite record. Per stage, a run
directory `runs/<item>/<k>-<stage>/` with the brief, the result, `session.json` and the notes, plan, report or
findings. Each move is its own commit (`work: <item> <before> -> <after>`). The session ids name the transcripts
i12's `measure` reads; nothing in it needs a dispatch description to be parsed.

## Removed

- `skills/slicing-into-increments`, `scripts/plan`, `scripts/slice_expectations.py`, `features plugin`, slice tags,
  Lands, Steps, lanes, batch plans, the living plan and its archive, the HAND-BACK log entry and the checkpoint
  entry, the plan's Backlog (now observations).
- `superpowers:writing-plans`, `superpowers:subagent-driven-development` and `superpowers:executing-plans` as the
  delivery pipeline, and `superpowers@claude-plugins-official` as a dependency
  (design-decision/superpowers-not-a-dependency supersedes design-decision/superpowers-dependency).
- Decisions superseded: one-batch-one-session, fresh-agents-short-replies, suite-record-holds, review-by-risk,
  slice-budget-refused-by-plan, tests-the-decisions-break (0037-0041, 0044).
- `model check` reading `#behaviour/r<n>` (design-decision/one-requirement-form).

Kept for i12 as they are: `scripts/measure`, `spec/capabilities/batch-measurement.md`, `skills/analyzing-a-batch`.

## Capabilities

New: work-queue, supervision, delivery, planning. Rewritten in work-item terms: code-research, red-green, review,
role-boundaries. Changed by the removal: design-model-check, feature-file-tools, formulation, spec-migration,
spec-consistency, analysis-tools. One capability-proposal each, `capability-proposal/delivery-on-v3-<capability>`.

## The workflow scenarios as fixture sessions

design-decision/fixture-scenarios-under-pytest-bdd: the feature files of the workflow capabilities carry `@fixture`,
deselected from `python3 -m pytest` and run by `python3 -m pytest -m fixture`. The harness moves into
`tests/workflow/` from `/home/vscode/scratch/shopsystem-bdd/ids/` (formulation-1). A Given binds a fixture case of
the shelf repository, a When runs its prompt headless three times (cached by the plugin's tree hash), a Then checks
every run. The stage capabilities run through `work step <item>`; delivery's session runs `work run` with a stub
`claude`. Which case each requirement's scenario binds:

| capability | cases (requirements) |
|---|---|
| spec-integration | integrate (r1, r3), integrate-question (r1, r2), answer (r4), apply-reject (r5, r6), integrate-second-spec (r7), brainstormed-here (r10), apply (r11-r16, r18), small-change (r8), apply-delegated (r9), apply-with-work (r17), glossary-no-work (r19) |
| formulation | formulate (r1, r2, r4-r8, r11-r13), noclingo (r13), formulate-two-readings (r3), formulate-every-call (r9), formulate-hand-back (r10), formulate-avoided-word (r14) |
| spec-migration | migrate-notes (r2-r5, r7, r8), migrate-unclean ×3 (r1), migrate-drift (r6), migrate (r9-r11, r13, r14), migrate-ambiguous (r12) |
| spec-consistency | consistency-report (r1-r4), consistency-fix (r5-r10), formulate and apply transcripts (r11) |
| code-research | research (r1, r4, r5, r7, r9-r12), research-changed-line (r3), research-defect (r8), research-skipped-stage (r6) |
| planning | plan (r1-r6, r9, r13, r14), plan-question (r7, r8), plan-defect (r10), plan-import (r11, r12) |
| red-green | implement (r1, r2, r6, r8, r10, r11, r16, r18, r19), implement-big (r9), implement-no-context (r15), implement-passes-early (r3, r7), implement-contradiction (r4, r7), implement-breaks-test (r5), implement-unnamed-work (r12), implement-meaning (r13), implement-open-decision (r14), implement-claim-refused (r17) |
| review | task-review (r1-r5, r10, r12, r13), re-review (r8), branch-review (r6, r7, r9, r11), architecture-review (r14) |
| delivery | deliver (r1-r8, r10, r12, r15), deliver-unclean ×2 (r11), deliver-two-readings (r9), deliver-question (r13, r14), deliver-budget (r16), deliver-scenario-wrong (r17) |

role-boundaries is guarantees, checked by `tests/scripts/test_agents.py`. One end-to-end case, deliver-real, has
real workers deliver the lending initiative (delivery-5). The script capabilities (work-queue, supervision and the
others) are ordinary pytest-bdd scenarios, `work run`'s with the stub.

## Order

work-queue-1..4 → supervision-1..5 → the agents and skills with their fixture scenarios (code-research-1,
planning-1, red-green-1..2, review-1..2, delivery-1..2) → the removals (feature-file-tools-1, delivery-3, delivery-4)
→ delivery-5. The harness (formulation-1) and the spec side's fixture scenarios run beside them. Every binding item
waits for i11's pytest-bdd conversion of this repository's suite.
