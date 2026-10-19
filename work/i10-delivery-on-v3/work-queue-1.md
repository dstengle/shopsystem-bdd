---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/work-queue-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-work-queue
status: drafted
wkind: capability
under: work-queue
accepts: [work-queue#r1-r8, work-queue#r17, work-queue#r18]
blocked_by: [work-item/pytest-bdd-suite, work-item/final-layout-read]
risk: data
---

# work-queue-1

## Observable
`work add`, `work show`, `work next` and `work log` work over `.shop/work/`, and every move is in `log.jsonl`.

## Unknown
Whether `scripts/model`'s frontmatter reader and feature reader can be shared with `work` without either changing behaviour.

## What goes green
The scenarios of work-queue#r1-r8, r17, r18: reading the queue, `add` and its refusals, `show` (with `--status`),
`next` (read-only), the move with its log line, the refusal on a status the log disagrees with, `log`, and exit
statuses. Moves are made by an internal function the later items and `work run` use; no `move` command is exposed.

## Files, roughly
New `scripts/work` and `scripts/workqueue.py` (stdlib); `tests/` step definitions for `features/work-queue.feature`
in i11's pytest-bdd form; possibly a shared reader factored out of `scripts/model` (then `tests/scripts/test_model.py`
must stay green as it is).

## Notes
Needs this repository's scenarios bound as pytest-bdd step definitions and the `.shop/` layout, both from initiative i11; the coordinator links i11's work-item into `blocked_by`.
