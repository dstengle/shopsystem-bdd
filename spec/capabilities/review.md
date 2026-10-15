---
id: shopsystem-bdd/review
title: Review
narrator: the controller closing a task or a batch
group: service
rests_on: [decision/review-by-risk, decision/rules-held-by-agent-tools, decision/fresh-agents-short-replies]
formulated_as: features/review.feature
retired: []
---

# Review

## Purpose
Finds defects in a task's diff or a whole batch's branch, against the brief, the spec and the repository's
rules, and triages them. The reviewers are `bdd-task-reviewer`, `bdd-branch-reviewer` and, on request,
`architecture-reviewer`. A reviewer changes nothing; its findings go to a fresh implementer.

## Behaviour
- [r1] **When** a review ends, its findings are in the findings file the dispatch named, and the working tree, index, HEAD and branches are as they were.
- [r2] Every finding is graded Critical, Important or Minor, and every Critical or Important finding says how it was observed.
- [r3] **When** a test was removed or weakened in the diff, the review lists it, and one the task did not list is Important.
- [r4] **When** the implementer reported a setup-only change or a rewrite of a test this batch wrote, the review checks each against the diff.
- [r5] Behaviour that contradicts a Behaviour line or a capability's Purpose is Important, whether or not a scenario covers it.
- [r6] **If** the reviewer cannot verify something the brief requires, the review fails rather than passes.
- [r7] **When** a branch review ends, it reports the suite's wall time and checks the code's shape against `CLAUDE.md` and its coupling to the projects it depends on.
- [r8] **When** a fix round's re-review finds something other than data left invalid, the system's own fault on input, or a write that lands where a refusal belongs, it is logged to the backlog and the batch closes.
- [r9] **Where** the system has a dry run and a real run of one operation, the branch review runs the randomized test that they agree.

## Implementation, may change
- Opus by default; a diff over 8 production or 4 test files is reviewed by area, in parallel.
- Probes go in the scratch directory the dispatch names; another revision is checked out as a worktree there.
- `tools check` runs the lint, dead-code and import-contract tools.

## Not yet
- Review runs per work-item only on named risks, and otherwise once per initiative when its last work-item is done — trigger: initiative i5 is approved.
