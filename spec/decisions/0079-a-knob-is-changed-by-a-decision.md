---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-knob-is-changed-by-a-decision
summary: "A change to a knob of the batch workflow (batch size, review size or checks, the readiness bar) is made with a design-decision that gives the figures of `measure compare` before and after."
date: 2026-11-05
status: accepted
tier: judgement
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design]
by: "workflow simplification plan 7, decided by the planner; revisit"
---

# 0079. A knob is changed by a decision

## Decision

A change to `batch_size`, to `[review] size` or `[review] checks` of `.shop/delivery.toml`, or to the readiness bar
is made with a design-decision that gives the figures of `measure compare` for the batches before and after, and
names the goal it trades (wall time, cost, defects per item).
