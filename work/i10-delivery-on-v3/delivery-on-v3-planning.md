---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-planning
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [planning]
adds: [planning#r1-r14]
changes: []
removes: []
---

# Planning: a new capability

What the gate approves: `planning#r1-r14`, a new capability, as written in `capabilities/planning.md`.

The planner stage, researched to planned, was the planning session under `superpowers:writing-plans` with the
constraints slicing handed it. It becomes an agent, `bdd-planner`, that plans one work-item from its researcher's
notes and writes a plan file, and asks a question where a client-visible decision is open. The rules that held
(no code in a plan; tests the decisions break; a stage left out; a dry run that agrees) are its lines.

Decisions: design-decision/plans-carry-intent-not-code (stands), design-decision/plans-list-the-tests-they-break
(supersedes design-decision/tests-the-decisions-break).
