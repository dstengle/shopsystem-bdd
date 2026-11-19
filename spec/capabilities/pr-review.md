---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/pr-review
title: Pull request review
narrator: the person who merges a batch's pull request
group: guarantees
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g2, r2, g3, r3, g5, r5, g6, r6, g7, r7, r8, g8, r9, g4, r4, g12, r13, g13, r14, g14, r15, g1, r1, g17, r17, g9, r10, g10, r11, g11, r12, g18, r18, g19, r19, g20, r20, g15, r16]
unbuilt: []
---

# Pull request review

## Purpose
One adversarial review a batch, at its pull request, and none after each stage or task (design goal 6). It checks
correctness against the items' requirements and engineering quality: the repository's rules, the `judgement`
decisions and the size of the change. It reads only the batch's own commits. A fix-now finding is fixed on the same
branch and the review re-reads what the fix changed; a clean pull request waits for the person's merge.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

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
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g1 | review-guarantees#g1 |
| r1 | review-guarantees#r1 |
| g17 | review-guarantees#g2 |
| r17 | review-guarantees#r2 |
| g9 | review-guarantees#g3 |
| r10 | review-guarantees#r3 |
| g10 | review-guarantees#g4 |
| r11 | review-guarantees#r4 |
| g11 | review-guarantees#g5 |
| r12 | review-guarantees#r5 |
| g18 | review-guarantees#g6 |
| r18 | review-guarantees#r6 |
| g19 | review-guarantees#g7 |
| r19 | review-guarantees#r7 |
| g20 | review-guarantees#g8 |
| r20 | review-guarantees#r8 |
| g15 | review-guarantees#g9 |
| r16 | review-guarantees#r9 |
