---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/answers-not-rulings
summary: "The person's answer to a work-item's question is an answer, not a ruling: the status `awaiting-ruling` is `awaiting-answer`, the command is `work answer <work-item> <answer>` and it writes under the work-item's `## Answers`."
date: 2026-10-22
status: proposed
source: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-ruling-returns-to-the-asking-stage, design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-item-lifecycle-as-run]
by: "the person, 2026-10-22 (\"Rename to 'answer' throughout\"), under the delegation of the drafting decisions to the coordinator"
---

# 0064. Answers, not rulings

## Context

"Rule" is already `model check`'s word (`model rules`, its rules' codes), and the person found it a dangerous term
for the person's answer to a work-item's question.

## Alternatives

Offered `work give-ruling`, `work answer`, or a rename throughout, the person chose the rename throughout.

## Decision

A ruling is an answer throughout. The status `awaiting-ruling` is `awaiting-answer`, the command `work rule
<work-item> <ruling>` is `work answer <work-item> <answer>`, and a work-item's section `## Rulings` is `## Answers`.
This renames, without changing what they say, the rows and words of decision 0039 (work-item-lifecycle-as-run) and
decision 0063 (a-ruling-returns-to-the-asking-stage) that name a ruling, `awaiting-ruling`, `work rule` or
`## Rulings`; those decision files stay as written, since an accepted decision file is not edited. An upgrade step,
for the plugin version after 0.24.0, renames the status and the section in a repository's work-items and its
`log.jsonl` lines.
