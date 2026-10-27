---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i39-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i39
status: awaiting-answer
argues: [work-queue]
adds: [work-queue#r33]
changes: []
removes: []
date: 2026-10-27
---

# work-queue

The drafts of this proposal are in .shop/work/i39/runs/i39/1-integrate/drafts/round-1/.

## Questions
- Approve the added work-queue line [r33] (new, under spec/capabilities/work-queue.md): "**While** a request that an initiative raised into an upstream is not `delivered`, `work status` shall print the initiative as waiting on that request." It pairs with supervision r136, which holds back work-items for the capability-proposal while the request is not delivered. Readings: (A) approve the line as drafted [recommended]; (B) drop it, so `work status` says nothing about such a wait; (C) reword it, in which case give the wording.

## Answers
- 2026-10-27: r33: Reading (C), reworded to name the consolidated list action that replaces work status. Also folded in: work show and work status are consolidated into one action listing all work with its status and one showing the detail of an individual item.
- 2026-10-27: Names: the consolidated actions are named: work list lists all work with its status (initiatives, requests and work-items); work show <id> shows the detail of one initiative, request or work-item; work status is retired, its lines retired and replaced by lines naming work list or work show. r33 is retired and replaced by: '**While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request.'
