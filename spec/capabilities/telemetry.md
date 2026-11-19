---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/telemetry
title: Telemetry
narrator: a session measuring a batch
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified, design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-a-batch]
retired: [g1, g2, g3, g4, r1, r2, r3, r4, g5, r5, g6, r6, g7, r7, g8, r8]
unbuilt: []
---

# Telemetry

## Purpose
`measure` records, for each batch, its wall time, session time, tokens and cost by role (planning, implementing,
review, fixing), and the defects: those the pull request's review found and those found after the merge, each traced
to its item (design goal 8). The system's goals pull against each other (wall time, token cost, defect rate), and the
knobs (batch size, review depth, the readiness bar) are tuned against these figures.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

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
  request of a model with no price (an Opus 4 before 4.6, a Sonnet 4 before 4.6 and a Haiku 4 before 4.5 among
  them) is counted in tokens and named under `unpriced`, never guessed. Claude Haiku 5.5 is priced at its long rate when a request's prompt is over 100K tokens.
- A role is planning for a main session and for the subagent that drove the batch (one begun before the window that
  dispatched a subagent counted in it, by its meta file's `parentAgentId`), its requests inside the window counted;
  review for a `pr-reviewer` or a subagent described `batch-<n> review`, fixing for `batch-<n> fix`, implementing for
  `batch-<n> t<k>`, `<n>` being the measured batch's; planning for a subagent described otherwise; else, with no
  description, implementing before the first review and fixing after it. A session none of whose requests has a
  price has no cost (`-`), not 0.
- The summary says when no main session or driver was counted in the window (a batch driven from a subagent or from
  another directory needs `--sessions <the main session's directory>`), and when transcripts were found but no
  session was in the window.
- The changed lines, a knob, are the batch's from its fork to the last review's head, `.shop/` left out; each review
  gives its own range's lines beside it.
- The measurement is the record `.shop/records/measurements/<date>-batch-<n>.md`, its summary tables before its JSON
  block, not written over without `--replace`.
- `measure defect <item> --says "<the fault and how to reproduce it>"` writes `.shop/batches/<n>/defect-<k>.md`
  (`kind: defect`, its `batch` and `item`) against a `delivered` item of a `merged` batch and commits it alone; it
  refuses anything else, changing nothing, and `measure batch` counts it under the defects after the merge.
- `measure compare` takes a record or `batch-<n>`, the batch's newest measurement by its record's name; two batches
  are set side by side (wall time, session time, tokens, cost, defects per item, each role's cost, the findings by
  grade, and the sizes: items, changed lines and reviews) with the ratio of the second to the first, a batch never measured is refused naming `measure batch`, and a
  batch's measurement is not compared with an initiative's, nor a batch's record that lacks a figure compare reads. `measure show` prints a batch's summary and sessions.

## Not yet

- Recurring findings across batches (plan-5 D21): counted by reading `measure compare`'s rows; a count over many
  batches waits for there being many.
- The third-review park (plan-5 D23) is revisited with the figures of real batches.
- A price table read from a source: the table is dated (`prices_as_of`) and `.shop/delivery.toml` overrides it.
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g5 | measurement#g1 |
| r5 | measurement#r1 |
| g6 | measurement#g2 |
| r6 | measurement#r2 |
| g7 | measurement#g3 |
| r7 | measurement#r3 |
| g8 | measurement#g4 |
| r8 | measurement#r4 |
