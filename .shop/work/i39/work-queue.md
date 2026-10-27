---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i39-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i39
status: drafted
argues: [work-queue]
date: 2026-10-27
adds: [work-queue#r34, work-queue#r35, work-queue#r36, work-queue#r37, work-queue#r38, work-queue#r39]
changes: []
removes: [work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18]
---

# work-queue

The drafts of this proposal are in .shop/work/i39/runs/work-queue/5-integrate/drafts/round-1/.

## Questions
- Approve the added work-queue line [r33] (new, under spec/capabilities/work-queue.md): "**While** a request that an initiative raised into an upstream is not `delivered`, `work status` shall print the initiative as waiting on that request." It pairs with supervision r136, which holds back work-items for the capability-proposal while the request is not delivered. Readings: (A) approve the line as drafted [recommended]; (B) drop it, so `work status` says nothing about such a wait; (C) reword it, in which case give the wording.

## Answers
- 2026-10-27: r33: Reading (C), reworded to name the consolidated list action that replaces work status. Also folded in: work show and work status are consolidated into one action listing all work with its status and one showing the detail of an individual item.
- 2026-10-27: Names: the consolidated actions are named: work list lists all work with its status (initiatives, requests and work-items); work show <id> shows the detail of one initiative, request or work-item; work status is retired, its lines retired and replaced by lines naming work list or work show. r33 is retired and replaced by: '**While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request.'

## Faults
- the gate round left no result `work run` can read: its round wrote no result file; its session ended as a success (success, 8 turns, exit code 0)
