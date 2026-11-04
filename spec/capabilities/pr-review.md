---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/pr-review
title: Pull request review
narrator: the person who merges a batch's pull request
group: guarantees
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r1, r2, r3, r4, r5, r6, r7, r8]
---

# Pull request review

## Purpose
One adversarial review a batch, at its pull request, and none after each stage or task (design goal 6). It checks
correctness against the items' requirements and engineering quality: the repository's rules, the `judgement`
decisions and the size of the change. It reads only the batch's own commits. A fix-now finding is fixed on the same
branch and the review re-reads what the fix changed; a clean pull request waits for the person's merge.

## Terms
- **`pr-reviewer`** (actor): the agent that reviews a batch's pull request.
- **unreviewed** (condition of pull request): a pull request that no review has been written of yet, so that its next review is its first.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| review | of | pull request | |
| requirement | proposed by | item | |
| commit | of | batch | |
| commit | outside | batch | |
| commit | for | review finding | |

## Behaviour

### [g1] One review a batch, at its pull request
- [r1] When `work` publishes a pull request of a batch, `pr-reviewer` shall write a review of the pull request.

### [g2] No review after each task
- [r2] When a task of a batch becomes `done`, `pr-reviewer` shall not write a review.

### [g3] Correctness against the items' requirements, over the batch's own commits
- [r3] While a pull request of a batch is unreviewed, when `pr-reviewer` writes a review of the pull request,
  `pr-reviewer` shall read every requirement proposed by an item in the batch and read every commit of the batch, and
  `pr-reviewer` shall not read a commit outside the batch.

### [g4] Engineering quality against the judgement decisions
- [r4] While a design-decision is `judgement`, when `pr-reviewer` writes a review of a pull request, `pr-reviewer`
  shall read the design-decision.

### [g5] A fix-now finding sends the batch back to building
- [r5] While a review finding on a pull request of a batch is `fix now`, when `pr-reviewer` writes a review of the
  pull request, `work` shall set the status of the batch to `building`.

### [g6] The next review reads what the fix changed
- [r6] While a review finding on a pull request is `fix now`, when `work` publishes the pull request, `pr-reviewer`
  shall read every commit for the review finding.

### [g7] A clean pull request awaits the person's merge
- [r7] While a pull request of a batch is clean, when `pr-reviewer` writes a review of the pull request, `work` shall
  set the status of the batch to `awaiting-merge`.

### [g8] Findings recorded with their grade
- [r8] When `pr-reviewer` writes a review finding, `pr-reviewer` shall give the review finding a grade and write a
  file.

## Implementation, may change

- The review's findings are written under `.shop/batches/<n>/`, each with its grade. Findings that keep recurring are
  a signal for a new decision, a new check or a higher readiness bar.
- The size of the change and the repository's rules (`CLAUDE.md`) are read with the `judgement` decisions.
