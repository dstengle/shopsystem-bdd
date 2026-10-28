---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i43-review
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i43
status: awaiting-answer
argues: [review]
adds: [review#r32, review#r33, review#r34]
changes: []
removes: [review#r9]
date: 2026-10-28
---

# review

The drafts of this proposal are in .shop/work/i43/runs/i43/1-integrate/drafts/round-1/.

## Questions
- supervision#r155 (exit code). Line: [r155] When `work run` starts a branch review, `work run` shall give the branch reviewer each run r154 names with its command, how it exited and its output, naming the commit they ran at. Reading A (recommended, drafted): 'how it exited', with the exit code in Implementation. Reading B: 'each run r154 names with its command, exit code and output, naming the commit they ran at.'
- review#r33 (the request's Where). Line: [r33] When a branch review finds a behaviour that only a run would show, the branch reviewer shall give it as a finding with the test that would show it, marked not run, in place of a reproduction. Reading A (recommended, drafted): When ... Reading B: keep 'Where the branch reviewer finds ...'.
- review#r12 ('an observation, with its reproduction') against r32/r33. Reading A (recommended): r12 stands; a reproduction is written, not run. Reading B: retire r12, add [r35] '...as an observation, with its reproduction or, in a branch review, the test r33 names, for hardening, ...'.
- review#r7 (the suite's wall time) against r32. Reading A (recommended): r7 stands; the reviewer reads the wall time from the suite run output r155 gives. Reading B: add supervision [r158] 'When `work run` starts a branch review, `work run` shall give the branch reviewer the wall time of the whole suite's run r154 names.'
- review#r6 (a check the reviewer cannot verify fails a branch review) against r32. Reading A (recommended): r6 stands; the reviewer verifies each check from the run r154/r155 give. Reading B: retire r6, change its branch-review cell to 'fail the review where the run of it that `work run` gave shows it did not exit successfully, or `work run` gave no run of it'.
- review Implementation ('Probes go in the scratch directory the brief names'). Reading A (recommended): keep, it covers only the work-item reviewer now. Reading B: reword to 'A work-item reviewer's probes go in the scratch directory the brief names; the branch reviewer makes none (r32).'
- Agent tools: design-decision/the-v3-agents gives bdd-branch-reviewer Bash, against review#r32 (runs nothing). Reading A (recommended): no change; r32 is held by the brief. Reading B: a new decision superseding the-v3-agents' row and a role-boundaries line giving the branch reviewer no Bash tool, raised as its own request.

## Answers
- 2026-10-28: supervision#r155 exit code: Reading A, 'how it exited', with the exit code in Implementation (answered by the coordinator under the person's delegation of 2026-10-28).
- 2026-10-28: review#r33: Reading A, 'When a branch review finds ...' as drafted (answered by the coordinator under the person's delegation of 2026-10-28).
- 2026-10-28: review#r12 against r32/r33: Reading A, r12 stands; a reproduction is written, not run (answered by the coordinator under the person's delegation of 2026-10-28).
- 2026-10-28: review#r7 against r32: Reading A, r7 stands; the reviewer reads the wall time from the suite run output r155 gives (answered by the coordinator under the person's delegation of 2026-10-28).
- 2026-10-28: review#r6 against r32: Reading A, r6 stands; the reviewer verifies each check from the runs r154/r155 give (answered by the coordinator under the person's delegation of 2026-10-28).
- 2026-10-28: review Implementation probes: Reading A, keep; it covers only the work-item reviewer now (answered by the coordinator under the person's delegation of 2026-10-28).
