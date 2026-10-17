---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/red-green
title: Red-green
narrator: the controller that dispatched the implementer
group: service
rests_on: [design-decision/feature-files-read-only-in-red-green, design-decision/tests-the-decisions-break, design-decision/suite-record-holds, design-decision/fresh-agents-short-replies]
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
- [r7] **When** the implementer hands back, a HAND-BACK entry with the stop condition, the evidence verbatim and which scenarios are green and red is in the plan's log, or in a lane in its report, and the work so far is committed.
- [r8] **When** a slice goes green, the plan's log has a checkpoint saying what someone can now do, what was surprising, and the open questions, followed by its suite record.
- [r9] **If** the task needs more than 15 files touched, the implementer names in its report, before any edit, the files this dispatch will touch, touches only those, stops at a green commit and replies `PARTIAL`, and a fresh implementer can continue from the report.
- [r10] **When** the scenarios are silent about a case, the code does not choose its behaviour and the checkpoint names it as an open question.
- [r11] **When** the task carries code, the implementer does not paste it and says so in the checkpoint.
- [r12] **If** going green needs work that no scenario of the slice describes and the task's "where the change lands" does not name, beyond a trivial helper, the implementer hands back.
- [r13] **If** a previously green scenario breaks and fixing it would change what a step means, the implementer replies `BLOCKED`.
- [r14] **If** the task needs a decision the brief and the capability's Behaviour leave open, or a file would cross the repository's size limit with no rule in `CLAUDE.md` saying where the code goes, the implementer replies `BLOCKED` with the specifics.
- [r15] **If** the brief has no `Scripts:`, `bdd-red-green` is not in its context, or the brief has Steps and the dispatch names no step, findings file or continuation, the implementer replies `NEEDS_CONTEXT`.
- [r16] Every reply begins with one of `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `NEEDS_CONTEXT` and is under fifteen lines.

## Implementation, may change
- The cycle: run one scenario red, write the step definitions it needs, the least code, run the slice's
  marker and module, refactor, commit; the whole suite once before the slice's last commit.
- `--slice <n>` where the slice expectations plugin is registered. Suites run in parallel and drive the
  entry point in-process.
- The implementer has no Skill tool; `bdd-red-green` is loaded through its `skills` field. Sonnet by default.

## Not yet
- The implementer pulls a ready work-item whose file set is its claim, instead of being dispatched a task — trigger: initiative i5 is approved.
