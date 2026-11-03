---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/review
title: Review
narrator: the script `work run`, closing a work-item or an initiative
group: guarantees
rests_on: [design-decision/review-of-work-items, design-decision/the-v3-agents, design-decision/worker-results-are-files, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: []
---

# Review

## Purpose
Finds defects in one work-item's commits or in an initiative branch as a whole, against the work-item's plan, the
spec and the repository's rules, and triages them. The reviewers are `bdd-task-reviewer` and `bdd-branch-reviewer`,
started by `work run`, and, when the person asks, `architecture-reviewer`. A reviewer changes nothing: what is to be
fixed now becomes a fix work-item, and the rest an observation.

## Terms

- **the branch reviewer** (actor): the session of a `branch review` stage, started as the agent `bdd-branch-reviewer`.
- **the architecture reviewer** (actor): the agent `architecture-reviewer`, started when the person asks.
- **find** (event): a review finds a thing in what it reads. Forms: finds, found.
- **unrequested behaviour** (kind): observable behaviour of code, such as an output, a file written, a status or a refusal, that no requirement asks for.
- **fix work-item** (kind): a work-item drafted from a branch review's findings to fix now.
- **refactor** (kind): a change of code's shape that keeps its behaviour.
- **wall time** (kind): how long one run of the suite took.
- **code shape** (kind): the code's fit to the rules `CLAUDE.md` gives.
- **coupling** (kind): what the code relies on in the projects it depends on.
- **agreement test** (kind): a randomized test that the dry-run mode and the real mode of one operation agree.
- **triage** (attribute of review finding): Values: `fix now`, `observation`, `drop`.
- **reproduction** (attribute of review finding): Values: `reproduced`, `not run`.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| commit | changes | feature |  |
| commit | weakens | test |  |
| commit | contradicts | requirement |  |
| commit | deletes | scenario |  |
| work-item | of | initiative | one |
| commit | of | work-item |  |

## Behaviour

### [g1] A work-item review leaves its findings and its result and changes nothing else
Restates: r1@0.29.
- [r1] When the reviewer ends a `review` stage, the reviewer shall write a result.
- [r2] When the reviewer ends a `review` stage, the reviewer shall write every review finding.
- [r3] When the reviewer ends a `review` stage, the reviewer shall not change a file in a worktree.
- [r4] When the reviewer ends a `review` stage, the reviewer shall not merge a work-item branch.

### [g2] A work-item review reads the work-item's commits and its plan
Restates: r13@0.29.
- [r5] When `work run` starts a `review` stage, the reviewer shall read every commit of the work-item.
- [r6] When `work run` starts a `review` stage, the reviewer shall read the plan.

### [g3] A branch review reads the initiative branch and every work-item of the initiative
Restates: r13@0.29.
- [r7] When `work run` starts a `branch review` stage, the branch reviewer shall read the initiative branch.
- [r8] When `work run` starts a `branch review` stage, the branch reviewer shall read every work-item of the initiative.

### [g4] The branch reviewer runs nothing
Restates: r32@0.29.
- [r9] The branch reviewer shall not start a command.

### [g5] Every finding is graded and triaged
Restates: r2@0.29, r12@0.29.
- [r10] The reviewer shall give every review finding a grade.
- [r11] The branch reviewer shall give every review finding a grade.
- [r12] The reviewer shall give every review finding a triage.
- [r13] The branch reviewer shall give every review finding a triage.

### [g6] A finding names its work-item
Restates: r12@0.29.
- [r14] When the reviewer writes a review finding, the reviewer shall name a work-item.

### [g7] A change to a feature is Critical
Restates: r10@0.29.
- [r15] If the reviewer finds a commit that changes a feature, then the reviewer shall write a review finding that is `Critical`.

### [g8] A weakened test is listed
Restates: r3@0.29.
- [r16] If the reviewer finds a commit that weakens a test, then the reviewer shall list the test.
- [r17] If the reviewer finds a commit that weakens a test, then the reviewer shall write a review finding that is `Important`.

### [g9] The tests the implementer named are verified against the commits
Restates: r4@0.29.
- [r18] When the reviewer reads a report, the reviewer shall read every commit that weakens a test.

### [g10] A contradiction of a requirement is Important
Restates: r5@0.29.
- [r19] If the reviewer finds a commit that contradicts a requirement, then the reviewer shall write a review finding that is `Important`.

### [g11] A check the branch reviewer cannot verify fails the review
Restates: r6@0.29.
- [r20] If the branch reviewer refuses a check, then the branch reviewer shall write a result that is `BLOCKED`.

### [g12] A check a work-item reviewer cannot verify is listed
Restates: r6@0.29.
- [r21] If the reviewer refuses a check, then the reviewer shall list the check.

### [g13] A branch review writes what a deprecated or deleted scenario leaves
Restates: r11@0.29.
- [r22] If the branch reviewer finds a deprecated scenario, then the branch reviewer shall write a review finding.

### [g14] A deleted scenario is a finding
Restates: r11@0.29.
- [r23] If the branch reviewer finds a commit that deletes a scenario, then the branch reviewer shall write a review finding.

### [g15] Unrequested behaviour is Important and fixed now
Restates: r29@0.29, r30@0.29.
- [r24] If the reviewer finds an unrequested behaviour, then the reviewer shall write a review finding that is `Important`.
- [r25] If the reviewer finds an unrequested behaviour, then the reviewer shall write a review finding that is `fix now`.

### [g16] The branch reviewer fixes unrequested behaviour now
Restates: r30@0.29.
- [r26] If the branch reviewer finds an unrequested behaviour, then the branch reviewer shall write a review finding that is `fix now`.

### [g17] A behaviour only a run would show names the test that would show it
Restates: r33@0.29.
- [r27] When the branch reviewer writes a review finding that is `not run`, the branch reviewer shall name a test.

### [g18] The re-review of a fix work-item finds observations
Restates: r8@0.29.
- [r28] If the reviewer finds a fix work-item, then the reviewer shall write a review finding that is `observation`.

### [g19] A branch review ends with the suite's wall time, the code's shape and its coupling
Restates: r7@0.29, r34@0.29.
- [r29] When the branch reviewer ends a `branch review` stage, the branch reviewer shall write a wall time.
- [r30] When the branch reviewer ends a `branch review` stage, the branch reviewer shall write a code shape.
- [r31] When the branch reviewer ends a `branch review` stage, the branch reviewer shall write a coupling.
- [r32] When the branch reviewer ends a `branch review` stage, the branch reviewer shall name every agreement test.

### [g20] A branch review asks only about what is fixed now
Restates: r31@0.29.
- [r33] When the branch reviewer ends a `branch review` stage, the branch reviewer shall give the result only a review finding that is `fix now`.

### [g21] A refactor is an observation with a check
Restates: r14@0.29.
- [r34] If the architecture reviewer finds a refactor, then the architecture reviewer shall write a review finding that is `observation`.
- [r35] If the architecture reviewer finds a refactor, then the architecture reviewer shall name a check.

### [g22] A reviewer that cannot do what it is asked changes nothing
Restates: r28@0.29.
- [r36] If the reviewer refuses a brief, then the reviewer shall write a reason.
- [r37] If the reviewer refuses a brief, then the reviewer shall change nothing.

## Implementation, may change
- Opus; `work run` starts one `bdd-task-reviewer` for a work-item, however many files its commits touch.
- Probes go in the scratch directory the brief names; another revision is read with `git show`, not checked out.
- `tools check` runs the lint, dead-code and import-contract tools.
- A finding gives its file and line, what is wrong, why it matters and the fix. The findings file is `findings.md` in
  the stage directory; a finding of a branch review that a run would show is marked `not run` in place of a
  reproduction.
- A work-item review's triage is fix now for a wrong answer, a crash where a refusal belongs or lost data; an
  observation, with its reproduction, for hardening; drop for polish that is not cheap.

## Not yet
- None.

## Dropped
