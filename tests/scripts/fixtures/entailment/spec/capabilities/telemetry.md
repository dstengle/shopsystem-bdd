---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/telemetry
title: Telemetry
narrator: a session measuring a batch
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified, design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-a-batch]
retired: [g1, g2, g3, g4, r1, r2, r3, r4]
unbuilt: []
---

# Telemetry

## Purpose
`measure` records, for each batch, its wall time, session time, tokens and cost by role (planning, implementing,
review, fixing), and the defects: those the pull request's review found and those found after the merge, each traced
to its item (design goal 8). The system's goals pull against each other (wall time, token cost, defect rate), and the
knobs (batch size, review depth, the readiness bar) are tuned against these figures.

## Terms

- **include** (verb, state): a measurement holds a figure or a name. Forms: includes, included. Frame: measurement includes thing.
- **wall time** (noun): the time from the start of a batch to its close. Kind of: thing.
- **session time** (noun): the time the sessions of a batch spent on it. Kind of: thing.
- **token** (noun): a unit of the text a model of a session reads or writes. Kind of: thing.
- **role** (noun): what a session did in a batch: planning, implementing, review or fixing. Kind of: text.
- **cost** (noun): what the tokens of a role cost. Kind of: thing.
- **ratio** (noun): a figure of the second of two measurements divided by the same figure of the first. Kind of: text.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| defect | of | item | one |
| defect | for | batch | one |
| measurement | of | batch | one |
| wall time | of | batch | one |
| session time | of | batch | one |
| token | of | batch |  |
| role | of | batch |  |
| cost | of | role | one |

## Behaviour

### [g5] `measure batch` writes a merged batch's measurement with its wall time, session time, tokens and cost by role
- [r5] While a batch is `merged`, when the person runs `measure batch` on the batch, `measure` shall write a measurement of the batch that includes the wall time of the batch, the session time of the batch, the tokens of the batch and the cost of every role of the batch.

### [g6] The measurement of a batch counts the review findings on its pull request by grade
- [r6] When the person runs `measure batch` on a batch that has a pull request, `measure` shall write a measurement of the batch that includes the number of review findings on the pull request whose grade is `Critical`, the number of review findings on the pull request whose grade is `Important` and the number of review findings on the pull request whose grade is `Minor`.

### [g7] A defect after the merge is traced to its item and batch
- [r7] While an item in a batch is `delivered`, when the person runs `measure defect` on the item, `measure` shall write a defect for the batch that the item has.

### [g8] `measure compare` sets the measurements of two batches side by side with their ratio
- [r8] When the person runs `measure compare` on two batches, `measure` shall print two measurements and a ratio.

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
