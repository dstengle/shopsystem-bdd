---
id: shopsystem-bdd/red-green
title: Red-green
narrator: the controller that dispatched the implementer
group: service
rests_on: [decision/feature-files-read-only-in-red-green, decision/tests-the-decisions-break, decision/suite-record-holds, decision/fresh-agents-short-replies]
formulated_as: features/red-green.feature
retired: []
---

# Red-green

## Purpose
Implements one task, one step of it, or one fix round, one scenario at a time, under `bdd-red-green`, by the
`bdd-implementer`. The scenarios are the contract; the implementer satisfies them and stops when one cannot
be satisfied honestly. It never decides what a scenario should have said.

## Behaviour
- [r1] **When** a task is done, every scenario it lists passes, and so does everything that passed in the record it started from.
- [r2] No commit of an implementer changes a `.feature` file, except removing a held scenario the task lists under `Retires:`.
- [r3] **If** a scenario passes before any code is written for it, a slice's check passes before any work, or a scenario of an unbuilt slice passes early, the implementer hands back.
- [r4] **If** a Then line can only pass through code that contradicts it, or a scenario can only fail on setup, the implementer hands back.
- [r5] **If** an existing test could stay green only by being removed, loosened, skipped or rewritten to assert something else, and the task does not list it, the implementer replies `BLOCKED` naming the test.
- [r6] **When** the implementer changes a test's setup without touching what it asserts, or rewrites a test first committed after the task's batch base, its report names each such test.
- [r7] **When** the implementer hands back, the plan's log has a HAND-BACK entry with the stop condition, the evidence verbatim and which scenarios are green and red, and the work so far is committed.
- [r8] **When** a slice goes green, the plan's log has a checkpoint saying what someone can now do, what was surprising, and the open questions, followed by its suite record.
- [r9] **If** a dispatch would touch more files than its written budget, the implementer stops at a green commit and replies `PARTIAL`, and a fresh implementer can continue from the report.
- [r10] **When** the scenarios are silent about a case, the code does not choose its behaviour and the checkpoint names it as an open question.
- [r11] **When** the task carries code, the implementer does not paste it and says so in the checkpoint.

## Implementation, may change
- The cycle: run one scenario red, write the step definitions it needs, the least code, run the slice's
  marker and module, refactor, commit; the whole suite once before the slice's last commit.
- `--slice <n>` where the slice expectations plugin is registered. Suites run in parallel and drive the
  entry point in-process.
- The implementer has no Skill tool; `bdd-red-green` is loaded through its `skills` field. Sonnet by default.

## Not yet
- The implementer pulls a ready work-item whose file set is its claim, instead of being dispatched a task — trigger: initiative i5 is approved.
