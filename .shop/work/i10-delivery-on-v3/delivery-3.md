---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-3
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: withdrawn
wkind: enabling
under: delivery
check: "test ! -e scripts/plan && test ! -e skills/slicing-into-increments && ! grep -rniE 'slic(e|es|ed|ing)|writing-plans|subagent-driven|executing-plans|scripts/plan|plan (log|show|status|archive|add-slice)|\blanes?\b|batch plan' skills agents --exclude-dir=analyzing-a-batch, and python3 -m pytest -q passes"
for: work-item/delivery-1
blocked_by: [work-item/delivery-2, work-item/red-green-2, work-item/review-2, work-item/planning-1, work-item/code-research-1, work-item/feature-file-tools-1]
risk: none
---

# delivery-3

## Observable
Nothing of slicing is left in the plugin: no skill, script, agent text or test.

## Unknown
none

## What the check covers
Deleted: `skills/slicing-into-increments/`, `scripts/plan`, `tests/scripts/test_plan.py`. Reworded in work-item
terms: `skills/formulating-features` (slicing hands back, hands to slicing), `skills/integrating-a-proposal` (the
hand-off to writing-plans, QUESTION FOR THE SPEC from slicing), `skills/migrating-to-capabilities` (a slice in
progress, slice-tag counts), `skills/checking-spec-consistency` (the backlog), `agents/initiative-round.md` (reads the
plan), `agents/capability-writer.md`, `agents/spec-checker.md`, `agents/feature-formulator.md` where they speak of
slices. `skills/analyzing-a-batch/` and `scripts/measure` are i12's and are left as they are.

## Files, roughly
The files above (about 12).

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
