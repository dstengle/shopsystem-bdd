---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-5
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r21-r26, supervision#r33]
blocked_by: [work-item/supervision-3]
risk: data
---

# supervision-5

## Observable
Done items with a named risk get a task review; once all are done a branch review runs; findings become fix
work-items, observations and review-finding records; items go green as the lines say.

## Unknown
none

## What goes green
supervision#r21-r26, r33: the task review, fix work-items (planned, `fixes:`, `findings:`, the findings' files),
the review-finding record (frontmatter id, kind, about; `scripts/model check` reads it), observations appended
under `.shop/records/observations.md` in its `## <id>` form, the branch review from the base, the scoped
re-review, and the closing message.

## Files, roughly
`scripts/supervise.py` (review stages, fix items, records), `scripts/workqueue.py`, step definitions.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.
