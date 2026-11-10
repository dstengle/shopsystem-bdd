---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/review
title: Review
narrator: the script `work run`, closing a work-item or an initiative
group: guarantees
rests_on: [design-decision/review-of-work-items, design-decision/the-v3-agents, design-decision/worker-results-are-files, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21]
---

# Review

## Purpose
**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Finds defects in one work-item's commits or in an initiative branch as a whole, against the work-item's plan, the
spec and the repository's rules, and triages them. The reviewers are `bdd-task-reviewer` and `bdd-branch-reviewer`,
started by `work run`, and, when the person asks, `architecture-reviewer`. A reviewer changes nothing: what is to be
fixed now becomes a fix work-item, and the rest an observation.

## Terms

- **the branch reviewer** (proper noun): the session of a `branch review` stage, started as the agent `bdd-branch-reviewer`. Kind of: worker.
- **the architecture reviewer** (proper noun): the agent `architecture-reviewer`, started when the person asks. Kind of: dispatch.
- **find** (verb): a review finds a thing in what it reads. Forms: finds, found. Frame: review finds review finding.
- **unrequested behaviour** (noun): observable behaviour of code, such as an output, a file written, a status or a refusal, that no requirement asks for.
- **fix work-item** (noun): a work-item drafted from a branch review's findings to fix now.
- **refactor** (noun): a change of code's shape that keeps its behaviour.
- **wall time** (noun): how long one run of the suite took.
- **code shape** (noun): the code's fit to the rules `CLAUDE.md` gives.
- **coupling** (noun): what the code relies on in the projects it depends on.
- **agreement test** (noun): a randomized test that the dry-run mode and the real mode of one operation agree.
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

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r1@0.29: retired with review#r1 in 2.0.0 (the-old-workflow-retired).
- r2@0.29: retired with review#r5 in 2.0.0 (the-old-workflow-retired).
- r3@0.29: retired with review#r8 in 2.0.0 (the-old-workflow-retired).
- r4@0.29: retired with review#r9 in 2.0.0 (the-old-workflow-retired).
- r5@0.29: retired with review#r10 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with review#r11, #r12 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with review#r19 in 2.0.0 (the-old-workflow-retired).
- r8@0.29: retired with review#r18 in 2.0.0 (the-old-workflow-retired).
- r10@0.29: retired with review#r7 in 2.0.0 (the-old-workflow-retired).
- r11@0.29: retired with review#r13, #r14 in 2.0.0 (the-old-workflow-retired).
- r12@0.29: retired with review#r5, #r6 in 2.0.0 (the-old-workflow-retired).
- r13@0.29: retired with review#r2, #r3 in 2.0.0 (the-old-workflow-retired).
- r14@0.29: retired with review#r20 in 2.0.0 (the-old-workflow-retired).
- r28@0.29: retired with review#r21 in 2.0.0 (the-old-workflow-retired).
- r29@0.29: retired with review#r15 in 2.0.0 (the-old-workflow-retired).
- r30@0.29: retired with review#r15, #r16 in 2.0.0 (the-old-workflow-retired).
- r31@0.29: retired with review#r19 in 2.0.0 (the-old-workflow-retired).
- r32@0.29: retired with review#r4 in 2.0.0 (the-old-workflow-retired).
- r33@0.29: retired with review#r17 in 2.0.0 (the-old-workflow-retired).
- r34@0.29: retired with review#r19 in 2.0.0 (the-old-workflow-retired).
