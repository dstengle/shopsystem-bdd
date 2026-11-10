---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/pr-review
title: Pull request review
narrator: the person who merges a batch's pull request
group: guarantees
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [r8]
unbuilt: []
---

# Pull request review

## Purpose
One adversarial review a batch, at its pull request, and none after each stage or task (design goal 6). It checks
correctness against the items' requirements and engineering quality: the repository's rules, the `judgement`
decisions and the size of the change. It reads only the batch's own commits. A fix-now finding is fixed on the same
branch and the review re-reads what the fix changed; a clean pull request waits for the person's merge.

## Terms
- **`pr-reviewer`** (proper noun): the agent that reviews a batch's pull request. Kind of: dispatch.
- **unreviewed** (adjective of pull request): a pull request that no review has been written of yet, so that its next review is its first.

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
- [r9] When `pr-reviewer` writes a review finding, `pr-reviewer` shall give a grade to the review finding and write a
  file.

## Implementation, may change

- The review's findings are written under `.shop/batches/<n>/`, each with its grade. Findings that keep recurring are
  a signal for a new decision, a new check or a higher readiness bar.
- The size of the change and the repository's rules (`CLAUDE.md`) are read with the `judgement` decisions.
- `work batch reviewed <batch>` records the findings file, `pr-reviewer`'s reply saved by the batch session, as `.shop/batches/<n>/review-<k>.md`,
  committed on the base with the batch file, and posts it on the pull request (`gh pr comment`). A finding still
  `fix now` sets the batch `building`; a clean review sets it `awaiting-merge` and marks the pull request ready
  (`gh pr ready`).
- `pr-reviewer` (`agents/pr-reviewer.md`: Read, Glob and Grep, no shell and no Write) reads the brief `work batch brief`
  writes in the ignored worktrees directory: the range's commits, each with its own patch, and `change.diff`, the
  items' lines (first review) or the open findings with the commits for each (re-review), the `tier: judgement`
  decisions, `CLAUDE.md`, the size and the runs of `[review] checks`, each with its exit code at the head and, run
  once a batch, at `forked_from`. Its reply is one findings file's content, each finding graded and triaged: the harness refuses a subagent's Write of a
  findings file, so the batch session saves the reply byte for byte at the brief's `Findings file:` path.
- The loop is the batch session's (skill `building-a-batch`): after `work batch review`, `work batch brief`, one
  fresh `pr-reviewer` on the brief, its reply saved, then `work batch reviewed`. On `building`, each open finding is fixed on its
  item's branch by commits ending `Item: b<j>` and `Finding: f<m>`; `work batch review` checks and pushes them, and
  the next brief is a re-review of only the commits after the last review. No review is written when a task becomes
  `done`.

## Not yet
- A cap on review rounds in code: `building-a-batch` parks each item an open finding names after the third review
  that leaves one open.
- Findings posted as inline comments on the pull request's lines: each review is one comment.
- Recurring findings counted, as a signal for a new decision, check or readiness bar (plan 7's telemetry).
- A transition `awaiting-merge` -> `abandoned`: `work batch abandon` still refuses an `awaiting-merge` batch.
