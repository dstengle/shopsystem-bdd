---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-5
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: drafted
wkind: enabling
under: delivery
check: "python3 -m pytest -m fixture tests/workflow/test_end_to_end.py passes in every run: the lending initiative delivered by delivering-an-initiative with real workers to every work-item green"
for: work-item/delivery-1
blocked_by: [work-item/delivery-4]
risk: none
---

# delivery-5

## Observable
One initiative goes from formulated proposals to every work-item green with real workers, on the shelf fixture.

## Unknown
The cost and time of one real delivery (it is i12's baseline material; the run's `log.jsonl` is kept with the
measurement record).

## What the check covers
Case deliver-real: as delivery-1's deliver case, with `claude` itself. Checks: every work-item green; the lend-items
and keep-items scenarios pass at the head; `log.jsonl` has a start and an end line for each stage of each item with a
session id and cost; at least one review-finding record (the branch review's); no file under `.shop/work/` changed
by a worker; the session read no worker output (its transcript). `--fixture-record` keeps the figures.

## Files, roughly
New `tests/workflow/test_end_to_end.py`, `tests/workflow/checks/delivery.py`, fixtures.
