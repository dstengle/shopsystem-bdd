---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-role-boundaries
kind: capability-proposal
part_of: initiative/i10
status: merged
date: 2026-10-19
argues: [role-boundaries]
adds: [role-boundaries#r6]
changes: [role-boundaries#r2, role-boundaries#r5]
removes: []
---

# Role boundaries: the planner

What the gate approves: added `role-boundaries#r6`, changed `#r2` and `#r5`.

`bdd-planner` joins the agents: no Edit (r2), Opus (r5), no shell (r6), so a planner cannot build what it plans.
The Purpose no longer says no script checks the lines: `tests/scripts/test_agents.py` does.
