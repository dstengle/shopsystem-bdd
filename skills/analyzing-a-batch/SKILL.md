---
name: analyzing-a-batch
description: Use when a batch has closed and the person asks what it cost, why it took so long, why it grew, how it compares with an earlier batch, or what to change in the shopsystem-bdd workflow. Also use when about to sum agents' token reports by hand, read a session transcript to count something, or propose a workflow change with no measurement behind it.
---

# Analyzing a Batch

## Overview

A delivery's cost is counted by a script and judged by you. The script counts everything countable; you judge only what counting cannot, and every judgement cites a line. The result is a report the shopsystem-bdd session receives as a request: it says what happened and what to try, never how a rule should be worded.

Scripts: this plugin's `scripts/`, at `<this skill's base directory>/../../scripts/`, run with `python3`. `measure --help` is its contract.

## Process

1. **Measure the initiative.** `measure initiative <initiative>` writes `.shop/records/measurements/<date>-<initiative>.md` from the initiative's `log.jsonl`, the `session.json` of each stage and git. To count the sessions around it too (the person's own, and those they dispatched), add `--sessions <dir of Claude Code transcripts>`. A measurement of that day that exists is not written over without `--replace`. Read it with `measure show <record>`; carry into the report anything it says it could not count.
2. **Compare.** `measure compare <earlier record> <this record>` prints the totals side by side with the ratio of this to the earlier. Compare with the measurement before, unless the person names another. With none to compare with, say so.
3. **Judge three things**, from the measurement, the initiative's `log.jsonl`, its work-items and their stage reports. Read no transcript and no source.
   - **Each work-item that went to awaiting-ruling or failed** (the measurement gives the counts). Its cause is one of: *listing omission* (an existing test the plan's "Tests the decisions break" did not name); *decision missing* (the plan left something undecided); *scenario wrong* (a Given, When or Then had to change); *other*, said in a few words.
   - **Each Critical or Important finding** of the branch review. The stage that found it and the earliest stage that could have, with why.
   - **Each work-item added after the initiative's first were drafted.** What caused it: a review finding, a hand-back, a spec question, a re-count.
4. **Write the report** to `.shop/records/` as a record, in the shape below, and commit it with the measurement.

## The Report

```
# <repository>, <initiative>: analysis

Plugin <version>. <window>. Measurement: <path>. Compared with: <path | nothing>.

## The delivery
<the tables measure show printed, as they are>

## Against <the earlier measurement>
<the table measure compare printed, as it is>

## Work-items that stopped
| work-item | what stopped | cause | cited |

## Findings
| finding | grade | found by | earliest it could have been found | cited |

## Work-items added
| work-item | caused by | cited |

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
- **A candidate names what to try and the figure that would show it worked**, the figure of the measurement the change should move. Three at most, the ones the observations bear out most. Wording the rule, naming the skill or agent to edit, and deciding whether to release are the shopsystem-bdd session's.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Summing the agents' usage from their replies | `measure initiative`. The agents cannot see their cache reads or their starting context |
| Opening a transcript to count something the measurement lacks | Say it is not counted, under Not counted. A count the script does not make is a request for the script |
| "About 3M tokens" | The three figures as the measurement gives them |
| A cause given from the hand-back's title alone | Read the work-item's stage report and its plan; cite both |
| "The plan should require…", "add a rule to bdd-implementer that…" | A candidate: what to try, what it rests on, the figure that moves |
| Seven candidates | Three. The report is read to choose one change for one release |
| A comparison across initiatives of different size, by totals alone | Say the sizes (stages, work-items) beside the ratio `measure compare` prints |
| Running `measure initiative` again where a measurement exists | Read it with `measure show`. The script refuses to write over it without `--replace`: the transcripts it was made from may be gone |
