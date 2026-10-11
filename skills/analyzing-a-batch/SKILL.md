---
name: analyzing-a-batch
description: Use when a batch has closed and the person asks what it cost, why it took so long, why it grew, how it compares with an earlier batch, or what to change in the shopsystem-bdd workflow. Also use when about to sum agents' token reports by hand, read a session transcript to count something, or propose a workflow change with no measurement behind it.
---

# Analyzing a Batch

## Overview

A batch's cost is counted by a script and judged by you. The script counts everything countable; you judge only what counting cannot, and every judgement cites a line. The result is a report the shopsystem-bdd session receives as a request: it says what happened and what to try, never how a rule should be worded.

Scripts: this plugin's `scripts/`, at `<this skill's base directory>/../../scripts/`, run with `python3`. `measure --help` is its contract.

## Process

1. **Get the facts.** The facts file is `docs/superpowers/measurements/<archive file's name>.json`. If it is missing, write it: `measure batch <the archive file>` (for a batch not yet archived, `measure batch --name <batch>`). Read it with `measure show <file>`. A note at the end of its output says what it could not count; carry every note into the report.
2. **Compare.** `measure compare <earlier> <this>` against one earlier measurement: the batch before, unless the person names another. With none to compare with, say so.
3. **Judge three things**, from the facts, the archive's log, the batch plan and the findings files under `.superpowers/sdd/<batch plan's name>/`. Read no transcript and no source.
   - **Each hand-back and each reply that was not done** (a status of `BLOCKED`, `PARTIAL` or `NEEDS_CONTEXT`; a dispatch the facts could not attribute is not one, and goes under Not counted). Its cause is one of: *listing omission* (an existing test the task's "Tests the decisions break" did not name); *decision missing* (the plan left something undecided); *scenario wrong* (a Given, When or Then had to change); *other*, said in a few words.
   - **Each Critical or Important finding.** The stage that found it (task review, branch review, after the batch closed) and the earliest stage that could have (planning, the task, the task's review), with why. Open the findings file for the finding's own words; the counts in the facts are as the reviewer replied and may be off by one.
   - **Each task added after the batch plan was written** (tasks run less tasks planned). What caused it: a review finding, a hand-back, a spec question, a re-count.
4. **Write the report** to `docs/superpowers/reports/<date>-<batch>-analysis.md`, in the shape below, and commit it with the facts file.

## The Report

```
# <repository>, batch <name>: analysis

Plugin <version>. <window>. Facts: <path of the facts file>. Compared with: <path | nothing>.

## The batch
<the tables measure show printed, as they are>

## Against <the earlier batch>
<the table measure compare printed, as it is>

## Hand-backs and replies not done
| slice | what stopped | cause | cited |

## Findings
| finding | grade | found by | earliest it could have been found | cited |

## Tasks added
| task | caused by | cited |

## Observations
- <one sentence>. (<a row of the facts, or path:line>)

## Candidates
- Try: <what to change in the workflow, in a sentence>. Rests on: <the observation>. It worked if: <a number in the facts, and which way it moves>.

## Not counted
<the facts' notes, and anything you could not judge, with why>
```

Every section is present; one with nothing in it says "none". A table row with no citation is removed.

- **Numbers are the script's.** A number in the report is in the facts file, or is arithmetic on two that are, shown. Tokens are given as the facts give them (output, new input, cache read), never added into one figure.
- **An observation is something the facts show**, not what should be done about it: "the controller's cache reads were 31M, more than the implementers' 29M (roles)".
- **A candidate names what to try and the number that would show it worked.** Three at most, the ones the observations bear out most. Wording the rule, naming the skill or agent to edit, and deciding whether to release are the shopsystem-bdd session's.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Summing the agents' usage from their replies or from the ledger | `measure batch`. The agents cannot see their cache reads or their starting context |
| Opening a transcript to count something the facts lack | Say it is not counted, under Not counted. A count the script does not make is a request for the script |
| "About 3M tokens" | The three figures as the facts give them |
| A cause given from the hand-back's title alone | Read the entry and the task's "Tests the decisions break"; cite both |
| "The plan should require…", "add a rule to bdd-implementer that…" | A candidate: what to try, what it rests on, the number that moves |
| Seven candidates | Three. The report is read to choose one change for one release |
| A comparison across batches of different size, by totals | The per-slice and per-dispatch rows `measure compare` prints |
| Running `measure batch` again where a facts file exists | Read it with `measure show`. The script refuses to write over it: the transcripts it was made from may be gone |
| Leaving out the facts' notes because they look like warnings | They say what the numbers do not cover. They go under Not counted |
