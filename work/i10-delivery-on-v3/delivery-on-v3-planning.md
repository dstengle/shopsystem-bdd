---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-planning
kind: capability-proposal
part_of: initiative/i10
status: merged
date: 2026-10-19
argues: [planning]
adds: [planning#r1-r8]
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

Re-synced 2026-10-19 to the EARS lines (initiative/i13, approved by the person): `capabilities/planning.md` is now a walking skeleton (design-decision/behaviour-lines-are-ears), numbered from r1, which replaces the drafted lines wholesale; the drafted ids in the text above were never published. What the drafted lines said beyond the skeleton is in the initiative's "Ideas to test once the skeleton runs".
