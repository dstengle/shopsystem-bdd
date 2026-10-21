---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/red-green
title: Red-green
narrator: the script `work run`, which started the implementer
group: service
rests_on: [design-decision/feature-files-read-only-in-red-green, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/work-item-lifecycle-as-run]
retired: [r4, r8, r12, r13, r14, r19, r37]
---

# Red-green

## Purpose
Implements one ready work-item, one scenario at a time, under `bdd-red-green`, by the `bdd-implementer` that
`work run` starts in the work-item's worktree; or continues one, or does one fix work-item. The scenarios are
the contract; the implementer satisfies them and stops when one cannot be satisfied honestly. It never decides what
a scenario should have said, and it never moves a work-item: `work run` reads its result.

## Behaviour
- [r1] **When** the implementer reports a work-item done, the implementer shall have every scenario the work-item accepts passing, leaving the whole suite to `work run`'s check before it merges.
- [r2] The implementer shall not commit a change to a `.feature` file or to a file under `.shop/work/`, except removing, with `features retire`, a deprecated scenario the work-item lists under Retires.
- [r3] **If** a scenario the work-item accepts passes before any code is written for it or can only fail on setup, the work-item's check passes before any work is done, a scenario of a work-item not yet claimed passes, a Then line can only pass through code that contradicts it, or going green needs work that no scenario of the work-item describes and its plan does not name, beyond a trivial helper, then the implementer shall hand back.
- [r5] **If** an existing test could stay green only by being removed, loosened, skipped or rewritten to assert something else and the work-item's plan does not list it, a previously green scenario breaks and fixing it would change what a step means, the work needs a decision the plan, its rulings and the capability's Behaviour leave open, or a file would cross the repository's size limit with no rule in `CLAUDE.md` saying where the code goes, then the implementer shall stop `BLOCKED`, naming the test, step, decision or file.
- [r6] **When** the implementer changes a test's setup without touching what it asserts, or rewrites a test first committed after the initiative's base, the implementer shall name the test in its report.
- [r7] **When** the implementer hands back, the implementer shall return the result `HAND-BACK` with the stop condition and its evidence verbatim, the work so far committed on the work-item's branch.
- [r9] **If** the work needs more than 15 files touched, then the implementer shall stop with the result `PARTIAL` at a green commit, having touched only the files it named in its report before its first edit.
- [r10] **When** the scenarios are silent about a case, the implementer shall name the case in its report as an open question, leaving its behaviour unchosen by the code.
- [r11] **When** the plan contains code, the implementer shall not paste it.
- [r15] **If** the implementer cannot do what its brief asks, then the implementer shall stop with the result `NEEDS_CONTEXT`, saying why.
- [r16] The implementer shall end every run with a result whose status is one of `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `NEEDS_CONTEXT`.
- [r17] **When** the work needs a file outside the work-item's file set, the implementer shall name the file in its report under `## Outside the file set` before editing it.
- [r18] The implementer shall work only in the worktree and on the branch its brief names, pushing, merging, rebasing and resetting nothing.

## Implementation, may change
- The cycle: run one scenario red, write the step definitions it needs, the least code, run the work-item's
  scenarios (`--work-item <name>` where `work_expectations.py` is registered) and the scenario's module, refactor,
  commit, with `--work-item`; the whole suite is `work run`'s, run once before it merges (supervision r4).
- The implementer loads `bdd-red-green`, listed in its `skills` field, with the Skill tool (role-boundaries r4). Sonnet by default.
- A continuation reads the report first and takes the next part it names; a fix work-item reads its findings and
  fixes those and nothing else.
- A `HAND-BACK` result says which scenarios are green and which are red. When a work-item's scenarios are green,
  the report says what someone can now do, what was surprising and the open questions, and the result gives the
  commits. The report says when the plan's code was not pasted. A result's summary is under fifteen lines.
- `NEEDS_CONTEXT` cases seen so far: the brief names no scripts directory or no result file, or `bdd-red-green` is
  not in the implementer's context.

## Not yet
- Claiming a file outside the work-item's file set with `work claim`, and stopping `BLOCKED` at a green commit, naming the file and the work-item whose claim has it, when the claim is refused (was r37; a refused claim cannot happen while there is no `work claim`).
