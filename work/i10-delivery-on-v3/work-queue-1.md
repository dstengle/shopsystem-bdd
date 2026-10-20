---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/work-queue-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-work-queue
status: drafted
wkind: capability
under: work-queue
accepts: [work-queue#r1-r7]
blocked_by: [work-item/pytest-bdd-suite, work-item/final-layout-read]
risk: data
---

# work-queue-1

## Observable
`work add` and `work show` work over `.shop/work/`, and every move writes the status and a line in `log.jsonl`.

## Unknown
Whether `scripts/model`'s frontmatter reader can be shared with `work` without either changing behaviour.

## What goes green
The scenarios of work-queue#r1-r7, the walking skeleton: `add` with `--part-of`, `--under` and `--accepts`, leaving
an existing file as it was, `show` with each item's status, the move writing the status and its log line, the
refusal on a status the log disagrees with, and the general line. Moves are made by an internal function `work run`
uses; no `move` command is exposed.

## Files, roughly
New `scripts/work` (stdlib); step definitions for `features/work-queue.feature` in i11's pytest-bdd form.

## Notes
Needs this repository's scenarios bound as pytest-bdd step definitions and the `.shop/` layout, both from initiative
i11. Rewritten 2026-10-19 to the skeleton (initiative/i13); the rest of the drafted queue is in the initiative's
"Ideas to test once the skeleton runs".
