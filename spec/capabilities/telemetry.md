---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/telemetry
title: Telemetry
narrator: a session measuring a batch
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r3, r4]
---

# Telemetry

## Purpose
`measure` records, for each batch, its wall time, session time, tokens and cost by role (planning, implementing,
review, fixing), and the defects: those the pull request's review found and those found after the merge, each traced
to its item (design goal 8). The system's goals pull against each other (wall time, token cost, defect rate), and the
knobs (batch size, review depth, the readiness bar) are tuned against these figures.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| defect | of | item | one |
| defect | for | batch | one |
| measurement | of | batch | one |

## Behaviour

### [g1] `measure batch` writes a merged batch's measurement
- [r1] When the person runs `measure batch` on a batch that is `merged`, `measure` shall write a measurement of the
  batch, include "wall time", include "session time", include "tokens" and include "cost by role".

### [g2] The review's findings are counted by grade
- [r2] While a review finding is on the pull request of a batch, when the person runs `measure batch` on the batch,
  `measure` shall include the grade of the review finding.

### [g3] A defect after the merge is traced to its item and batch
- [r3] While an item is `delivered` and the item is in a batch, when the person runs `measure defect` on the item,
  `measure` shall write a defect of the item for the batch.

### [g4] `measure compare` sets two batches side by side
- [r4] When the person runs `measure compare batch-2 batch-3`, `measure` shall print "batch-2" and print "batch-3".

## Implementation, may change

- `measure batch` reads the transcripts of Claude Code's project directory for the root (`CLAUDE_CONFIG_DIR`, else
  `~/.claude`, `projects/<the resolved root with every character not a letter or digit written ->`), or the directory
  `--sessions` names; a missing or empty directory measures the batch without sessions, saying so.
- The batch's window is read from the git history of `.shop/batches/<n>/plan.md`: started at its first commit, first
  reviewed at the first `-> in-review`, built at the last `-> awaiting-merge`, closed at `-> merged` or
  `-> abandoned`.
- A main session's requests count inside the window from started to built (else closed, else now), a subagent's
  whole when its first request is inside it; each request once, and session time is the sum of gaps of at most 300 s.
- Cost is computed from a dated price table per model, which `.shop/delivery.toml` `[prices."<model>"]` overrides; a
  request of a model with no price is counted in tokens and named under `unpriced`, never guessed.
- A role is planning for a main session, review for a `pr-reviewer` or a subagent described `batch-<n> review`,
  fixing for `batch-<n> fix`, implementing for `batch-<n> t<k>`, else implementing before the first review and fixing
  after it.
- The measurement is the record `.shop/records/measurements/<date>-batch-<n>.md`, its summary tables before its JSON
  block, not written over without `--replace`.
