---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i58-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i58
status: awaiting-answer
argues: [work-queue]
adds: [work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45]
changes: []
removes: []
date: 2026-10-28
---

# work-queue

The drafts of this proposal are in .shop/work/i58/runs/i58/1-integrate/drafts/round-1/.

## Questions
- r42, r43: how does `work` learn that the person approved? The trigger is the person's approval, which `work` cannot see, and the lines name no command a session runs to hand the drafts over.
  Lines:
  - [r42] **When** the person approves drafted lines at a gate that a session keeps, `work` shall write a capability-proposal for each capability the drafts change, with the requirement ids it adds, changes and removes.
  - [r43] **When** the drafts that the person approves at a gate a session keeps change the glossary, `work` shall write a glossary-proposal with the terms the drafts add, change and remove.
  Readings:
  A (recommended): the trigger is a command run with the drafts path and the approval. r42 would read "**When** `work <cmd>` is run with drafts the person approved at a gate a session keeps, `work` shall write a capability-proposal for each capability the drafts change, with the requirement ids it adds, changes and removes."; r43 alike. The command's name goes in an Implementation line.
  B: keep both as drafted.
- r44: where is the log of the proposal's transitions written?
  Line: [r44] **When** `work` writes a proposal from a gate that a session kept, `work` shall write the proposal as `approved` and log each of its transitions, naming the gate and the commit that applied its drafts.
  Readings:
  A (recommended): the initiative's `log.jsonl`, as r5: "...and append a line to `.shop/work/<initiative>/log.jsonl` for each of its transitions, naming the gate and the commit that applied its drafts."
  B: the ledger, `.shop/work/<initiative>/ledger.md`.
- r44: which transitions are logged?
  Line: [r44] **When** `work` writes a proposal from a gate that a session kept, `work` shall write the proposal as `approved` and log each of its transitions, naming the gate and the commit that applied its drafts.
  Readings:
  A (recommended): one transition, into `approved`; the line stands as drafted.
  B: each status the gate went through: "...log the transitions `drafted`, `awaiting-answer` and `approved`, each naming the gate and the commit that applied its drafts."
