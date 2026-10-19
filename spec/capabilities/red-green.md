---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/red-green
title: Red-green
narrator: the supervisor that started the implementer
group: service
rests_on: [design-decision/feature-files-read-only-in-red-green, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/work-item-lifecycle-as-run]
formulated_as: features/red-green.feature
retired: []
---

# Red-green

## Purpose
Implements one ready work-item, one scenario at a time, under `bdd-red-green`, by the `bdd-implementer` that
`work run` starts in the work-item's worktree; or continues one, or does one fix work-item. The scenarios are
the contract; the implementer satisfies them and stops when one cannot be satisfied honestly. It never decides what
a scenario should have said, and it never moves a work-item: `work run` reads its result.

## Behaviour
- [r1] **When** a work-item is done, every scenario it accepts passes, and so does everything that passed in the suite record its brief gives.
- [r2] No commit of an implementer changes a `.feature` file, except removing, with `features retire`, a deprecated scenario the work-item lists under Retires.
- [r3] **If** a scenario the work-item accepts passes before any code is written for it, its check passes before any work, or a scenario of a work-item not yet claimed passes early, the implementer hands back.
- [r4] **If** a Then line can only pass through code that contradicts it, or a scenario can only fail on setup, the implementer hands back.
- [r5] **If** an existing test could stay green only by being removed, loosened, skipped or rewritten to assert something else, and the work-item's plan does not list it, the implementer stops `BLOCKED` naming the test.
- [r6] **When** the implementer changes a test's setup without touching what it asserts, or rewrites a test first committed after the initiative's base, its report names each such test.
- [r7] **When** the implementer hands back, its result is `HAND-BACK` with the stop condition, the evidence verbatim and which scenarios are green and red, and the work so far is committed on the work-item's branch.
- [r8] **When** a work-item's scenarios are green, the report says what someone can now do, what was surprising and the open questions, and the result gives the commits.
- [r9] **If** the work needs more than 15 files touched, the implementer names in its report, before any edit, the files this worker will touch, touches only those, stops at a green commit with the result `PARTIAL`, and a new implementer can continue from the report.
- [r10] **When** the scenarios are silent about a case, the code does not choose its behaviour and the report names it as an open question.
- [r11] **When** the plan contains code, the implementer does not paste it and says so in the report.
- [r12] **If** going green needs work that no scenario of the work-item describes and its plan does not name, beyond a trivial helper, the implementer hands back.
- [r13] **If** a previously green scenario breaks and fixing it would change what a step means, the implementer stops `BLOCKED`.
- [r14] **If** the work needs a decision the plan, its rulings and the capability's Behaviour leave open, or a file would cross the repository's size limit with no rule in `CLAUDE.md` saying where the code goes, the implementer stops `BLOCKED` with the specifics.
- [r15] **If** the brief names no scripts directory or no result file, or `bdd-red-green` is not in the implementer's context, the implementer stops `NEEDS_CONTEXT`.
- [r16] Every result's status is one of `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `NEEDS_CONTEXT`, and its summary is under fifteen lines.
- [r17] **If** the work needs a file outside the work-item's file set, the implementer claims it with `work claim` before editing it. **If** the claim is refused, it commits what is green and stops `BLOCKED`, naming the file and the work-item whose claim has it.
- [r18] The implementer works only in the worktree and on the branch its brief names, and never pushes, merges, rebases or resets.
- [r19] No commit of an implementer changes a file under `.shop/work/`.

## Implementation, may change
- The cycle: run one scenario red, write the step definitions it needs, the least code, run the work-item's
  scenarios (`--work-item <name>` where `work_expectations.py` is registered) and the scenario's module, refactor,
  commit; the whole suite once before the last commit, its record in the report.
- The implementer has no Skill tool; `bdd-red-green` is loaded through its `skills` field. Sonnet by default.
- A continuation reads the report first and takes the next part it names; a fix work-item reads its findings and
  fixes those and nothing else.

## Not yet
- None.
