---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/role-boundaries-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-role-boundaries
status: drafted
wkind: guarantee
under: role-boundaries
check: "python3 -m pytest -q tests/scripts/test_agents.py passes: each line of role-boundaries#r1-r6 checked against agents/*.md"
blocked_by: [work-item/planning-1, work-item/review-2, work-item/red-green-1, work-item/code-research-1]
risk: none
---

# role-boundaries-1

## Observable
A test reads every agent definition and fails when a tool list or model breaks role-boundaries.

## Unknown
none

## What the check covers
r1 (only initiative-round has Agent), r2 (no Edit for reviewers, the scout and the planner), r3, r4 (the
implementer's `skills:` holds bdd-red-green and its tools no Skill), r5 (models by role, bdd-planner opus), r6 (no
Bash for the planner).

## Files, roughly
New `tests/scripts/test_agents.py`.
