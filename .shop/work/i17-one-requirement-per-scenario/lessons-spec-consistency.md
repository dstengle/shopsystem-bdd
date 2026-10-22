---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/lessons-spec-consistency
kind: capability-proposal
part_of: initiative/i17
status: merged
date: 2026-10-22
argues: [spec-consistency]
adds: [spec-consistency#r22, spec-consistency#r23, spec-consistency#r24, spec-consistency#r25, spec-consistency#r26, spec-consistency#r27]
changes: []
removes: []
---

# Spec consistency: the five lessons of 0.22.0's formulation as findings

The person approved (2026-10-22) adding the five lessons of 0.22.0's blind formulation round to the capability
format and the spec-checker. Each lesson is a kind of finding a `spec-checker` reports, rows of one table led by
"When a `spec-checker` finds one of the following in what it reads, the `spec-checker` shall write it as a
finding, naming its ids":

- r22 (lesson 1): a scenario showing observable behaviour no Behaviour line of its capability asks for.
- r23 (lesson 2): two lines acting on one thing without saying which wins.
- r24 (lesson 2): a line leaving to inference which runs, workers or commands it applies to.
- r25 (lesson 3, decisions 0054 and 0055): a scenario showing another line's response, the general failure
  line's exit or refusal included, or giving an exit code.
- r26 (lesson 4): a status or mode with a way into or out of it that no line gives.
- r27 (lesson 5): a word a line depends on that is neither a glossary term nor spelled out in the line.

Purpose gains "that the lines leave nothing to infer"; Implementation says which reader finds which row and how
the findings file groups them. Highest id ever used before: r21. No feature file names these ids yet.
