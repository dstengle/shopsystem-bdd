---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i54-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i54
status: awaiting-answer
argues: [work-queue]
adds: [work-queue#r48, work-queue#r49]
changes: []
removes: [work-queue#r34]
date: 2026-10-28
---

# work-queue

The drafts of this proposal are in .shop/work/i54/runs/i54/1-integrate/drafts/round-1/.

## Questions
- Decision on work-queue r49 (added): **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status. It replaces r34 (removed, retired; it was: **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.). Added r48 is: **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution. The existing r35 (**Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object.) then contradicts r49, because it still lists requests. Readings: (a) retire r35 and add r50 '**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.', so the text and JSON outputs agree; (b) keep r35 as it is, so the text and JSON outputs differ. Recommended: (a).
