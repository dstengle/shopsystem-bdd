---
name: analyzing-a-batch
description: Use when a batch has closed and the person asks what it cost, why it took so long, why it grew, how it compares with an earlier batch, or what to change in the shopsystem-bdd workflow. Also use when about to sum agents' token reports by hand, read a session transcript to count something, or propose a workflow change with no measurement behind it.
---

# Analyzing a Batch

## Overview

A delivery's cost is counted by a script and judged by you. The script counts everything countable; you judge only what counting cannot, and every judgement cites a line. The result is a report the shopsystem-bdd session receives as a request: it says what happened and what to try, never how a rule should be worded.

Scripts: this plugin's `scripts/`, at `<this skill's base directory>/../../scripts/`, run with `python3`. `measure --help` is its contract.

## Process

1. **Read the batch's measurement.** Read the measurement building-a-batch wrote, after `work batch merged` or `abandon`: `measure show <record>`. Run `measure batch <batch>` yourself only when there is none, since a second run of the day is refused without `--replace`. `measure batch <batch>` writes `.shop/records/measurements/<date>-batch-<n>.md`, reading the git history of the batch's plan and the transcripts of the sessions in its window from Claude Code's store for this repository (`--sessions <dir>` names another directory of transcripts). It gives the wall time, the session time, the tokens and the cost by role (planning, implementing, review, fixing), the pull request's findings by grade, the defects traced to their items and the knobs the batch ran with. Carry into the report anything it says it could not count (unpriced requests, no transcripts, no main session in the window).
2. **Compare with the batch before.** `measure compare <earlier batch> <batch>` (by name, `batch-<n>`: each batch's newest measurement) prints the figures side by side with the ratio of this to the earlier, each role's cost and the findings by grade among them. Compare with the batch before, unless the person names another. With none to compare with, say so.
3. **Judge three things**, from the measurement, the batch's files under `.shop/batches/<n>/` and its items. Read no transcript and no source.
   - **Each `fix now` finding** of the pull request's review (its record `review-<k>.md`): the earliest point that could have caught it (the item's lines, its task, the review), with why.
   - **Each defect after the merge** (its `defect-<k>.md`, recorded with `measure defect`): what let it through the review.
   - **Each parked item**: its question, and whether the readiness bar could have caught it before the batch.
4. **Write the report** in the shape below to a scratch file, then keep it as a record: `python3 <scripts>/work record "<repository>, <batch>: analysis" --kind analysis --summary "<one line for the records index>" --body <file>` writes `.shop/records/<date>-<slug>.md`, adds its row to `.shop/records/README.md` and commits both. Commit the measurement with `git` if it is not committed yet.

An initiative of plugin 0.30's frozen queue keeps the measurement it was given: `measure show` and `measure compare` still read it, with its work-items for the batch's items.

## The Report

```
# <repository>, <batch>: analysis

Plugin <version>. <window>. Measurement: <path>. Compared with: <path | nothing>.

## The delivery
<the tables measure show printed, as they are>

## Against <the earlier measurement>
<the table measure compare printed, as it is>

## Findings and defects
| finding or defect | grade | item | earliest it could have been caught | cited |

## Items parked
| item | question | could the readiness bar have caught it | cited |

## Observations
- <one sentence>. (<a row of the measurement, or path:line>)

## Candidates
- Try: <what to change in the workflow, in a sentence>. Rests on: <the observation>. It worked if: <the figure of the measurement it should move, and which way>.

## Not counted
<what the measurement could not count, and anything you could not judge, with why>
```

Every section is present; one with nothing in it says "none". A table row with no citation is removed.

- **Numbers are the script's.** A number in the report is in the measurement, or is arithmetic on two that are, shown. Tokens are given as the measurement gives them (output, new input, cache read), never added into one figure.
- **An observation is something the measurement shows**, not what should be done about it: "the implementers' cache reads were 31M, more than the researchers' 29M".
- **A candidate that changes a knob** (`batch_size`, `[review] size` or `[review] checks`, the readiness bar) is made as a design-decision giving the figures of `measure compare` before and after and the goal it trades (design-decision/a-knob-is-changed-by-a-decision), written with `work decision "<title>" --summary "<one sentence>" --tier judgement --decision "<text>"`; the candidate says so.
- **A candidate names what to try and the figure that would show it worked**, the figure of the measurement the change should move. Three at most, the ones the observations bear out most. Wording the rule, naming the skill or agent to edit, and deciding whether to release are the shopsystem-bdd session's.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Summing the agents' usage from their replies | `measure batch`. The agents cannot see their cache reads or their starting context |
| Adding the roles' costs by hand | `cost by role` in the measurement |
| Opening a transcript to count something the measurement lacks | Say it is not counted, under Not counted. A count the script does not make is a request for the script |
| "About 3M tokens" | The three figures as the measurement gives them |
| A cause given from the hand-back's title alone | Read the item's notes and its task's commits; cite both |
| "The plan should require…", "add a rule to the batch's subagent brief that…" | A candidate: what to try, what it rests on, the figure that moves |
| Seven candidates | Three. The report is read to choose one change for one release |
| A comparison across batches of different size, by totals alone | Say the sizes (items, changed lines: the knobs) beside the ratio `measure compare` prints, and compare defects per item |
| Running `measure batch` again where a measurement exists | Read it with `measure show`. The script refuses to write over it without `--replace`: the transcripts it was made from may be gone |
