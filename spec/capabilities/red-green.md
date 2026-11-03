---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/red-green
title: Red-green
narrator: the script `work run`, which started the implementer
group: guarantees
rests_on: [design-decision/feature-files-read-only-in-red-green, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/work-item-lifecycle-as-run, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: []
---

# Red-green

## Purpose
Implements one ready work-item, one scenario at a time, under `bdd-red-green`, by the `bdd-implementer` that
`work run` starts in the work-item's worktree; or continues one, or does one fix work-item. The scenarios are
the contract; the implementer satisfies them and stops when one cannot be satisfied honestly. It never decides what
a scenario should have said, and it never writes a work-item's transition: `work run` reads its result.

## Terms

- **passing** (condition of scenario): a scenario that passes when it is run alone with `python3 -m pytest`.
- **large** (condition of work-item): a work-item whose work needs more than 15 files touched.
- **silent case** (kind): a case the scenarios of a work-item say nothing of, named in the report as an open question and left unchosen by the code.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| file | outside | file set |  |

## Behaviour

### [g1] `DONE` only with every accepted scenario passing
Restates: r1@0.29.
- [r1] While a scenario of the work-item is not passing, the implementer shall not write a result that is `DONE`.

### [g2] The whole suite is `work run`'s
Restates: r1@0.29.
- [r2] The implementer shall not use `--whole-suite`.

### [g3] The implementer changes no feature and writes no status
Restates: r2@0.29.
- [r3] The implementer shall not change a feature or write a status.

### [g4] A scenario that passes before its work is a hand-back
Restates: r3@0.29.
- [r4] If the implementer finds a scenario of the work-item that is passing, then the implementer shall write a result
  that is `HAND-BACK`.

### [g5] An open decision blocks the work
Restates: r5@0.29.
- [r5] If the implementer finds a plan decision settled by no requirement, then the implementer shall write a result
  that is `BLOCKED` and name the plan decision.

### [g6] A test the work would break blocks the work
Restates: r5@0.29.
- [r6] If the implementer finds a test broken by the work-item, then the implementer shall write a result that is
  `BLOCKED` and name the test.

### [g7] A changed test is named in the report
Restates: r6@0.29.
- [r7] When the implementer changes a test, the implementer shall name the test.

### [g8] A hand-back gives its condition and evidence, with the work so far committed
Restates: r7@0.29.
- [r8] When the implementer writes a result that is `HAND-BACK`, the implementer shall write a hand-back and commit
  every file changed by the work-item.

### [g9] A large work-item stops at a green commit
Restates: r9@0.29.
- [r9] If the implementer finds a work-item that is large, then the implementer shall write a result that is `PARTIAL`
  and name every file changed by the work-item.

### [g10] A case the scenarios are silent about is named
Restates: r10@0.29.
- [r10] When the implementer finds a silent case, the implementer shall name the silent case.

### [g11] The plan's code is not pasted
Restates: r11@0.29.
- [r11] When the implementer reads a code block, the implementer shall not write the code block.

### [g12] An implementer that cannot do what its brief asks says why
Restates: r15@0.29.
- [r12] If the implementer refuses a brief, then the implementer shall write a result that is `NEEDS_CONTEXT` and
  write a reason.

### [g13] Every session ends with a result
Restates: r16@0.29.
- [r13] When the implementer ends an `implement` stage, the implementer shall write a result.

### [g14] A file outside the file set is named before it is edited
Restates: r17@0.29.
- [r14] When the implementer finds a file outside the file set, the implementer shall name the file.

### [g15] The implementer pushes and merges nothing
Restates: r18@0.29.
- [r15] The implementer shall not push a commit or merge a work-item branch.

## Implementation, may change
- The cycle: run one scenario red, write the step definitions it needs, the least code, run the work-item's
  scenarios (`--work-item <name>` where `work_expectations.py` is registered) and the scenario's module, refactor,
  commit, with `--work-item`; the whole suite is `work run`'s, run once before it merges.
- The implementer loads `bdd-red-green`, listed in its `skills` field, with the Skill tool (role-boundaries). Sonnet by default.
- A continuation reads the report first and takes the next part it names; a fix work-item reads its findings and
  fixes those and nothing else.
- A hand-back is also given when a scenario can only fail on setup, the work-item's check passes before its work, a
  scenario of a work-item not yet claimed passes, a Then line can only pass through code that contradicts it, or the
  scenarios need work no scenario describes and the plan does not name. `BLOCKED` is also given when a scenario that
  passed now fails and fixing it would change what a step means, or a file would cross the size limit with no rule in
  `CLAUDE.md` saying where the code goes; a test the plan lists as broken is not a block.
- A result's outcome is one of `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `NEEDS_CONTEXT`. A
  file outside the file set is named under `## Outside the file set` in the report before it is edited. The
  implementer works only in the worktree and on the branch its brief names, and rebases and resets nothing.
- A result with the outcome `HAND-BACK` says which scenarios pass and which fail. When a work-item's scenarios pass,
  the report says what someone can now do, what was surprising and the open questions, and the result gives the
  commits. The report says when the plan's code was not pasted. A result's summary is under fifteen lines.
- `NEEDS_CONTEXT` cases seen so far: the brief names no scripts directory or no result, or `bdd-red-green` is
  not in the implementer's context.

## Not yet
- Claiming a file outside the work-item's file set with `work claim`, and stopping with the outcome `BLOCKED` at a
  green commit, naming the file and the work-item whose claim has it, when the claim is refused.

## Dropped
