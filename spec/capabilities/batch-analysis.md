---
id: shopsystem-bdd/batch-analysis
title: Batch analysis
narrator: the person deciding a change to the workflow
group: operations
rests_on: [decision/an-experiment-is-a-release, decision/measure-refuses-unknown-shapes]
formulated_as: features/batch-analysis.feature
retired: []
---

# Batch analysis

## Purpose
Turns a closed batch's facts into a report the person reads to choose one change to the workflow. It is
`analyzing-a-batch`, run in the repository that ran the batch. Counting is the script's; the report judges
only what counting cannot, and words no rule.

## Behaviour
- [r1] **When** a batch is analysed, the report is at `docs/superpowers/reports/<date>-<batch>-analysis.md`, committed with its facts file.
- [r2] Every number in the report is in the facts file, or is arithmetic on two that are, shown.
- [r3] The report has every section of its shape; one with nothing in it says "none", and every table row cites a facts row or a path and line.
- [r4] **When** an earlier measurement exists, the report compares this batch with it per slice and per dispatch; when none does, it says so.
- [r5] Each hand-back and each reply not done is given one cause: a listing omission, a missing decision, a wrong scenario, or other in a few words.
- [r6] Each Critical or Important finding is given the stage that found it and the earliest stage that could have.
- [r7] The report names at most three candidates, each with the observation it rests on and the number that would show it worked.
- [r8] What the facts could not count is listed under "Not counted", the facts' own notes included.

## Implementation, may change
- `measure batch`, `measure show`, `measure compare`; findings files under `.superpowers/sdd/<plan>/`.
- No transcript and no source is read.

## Not yet
- Cost is attributed by work-item and capability from each worker's own usage record — trigger: initiative i5 is approved.
