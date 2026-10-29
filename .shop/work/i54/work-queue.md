---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i54-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i54
status: formulated
argues: [work-queue]
date: 2026-10-28
adds: [work-queue#r59, work-queue#r60, work-queue#r61]
changes: []
removes: [work-queue#r34, work-queue#r35]
---

# work-queue

The drafts of this proposal are in .shop/work/i54/runs/work-queue/4-integrate/drafts/round-1/.

## Questions
- Decision on work-queue r49 (added): **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status. It replaces r34 (removed, retired; it was: **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.). Added r48 is: **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution. The existing r35 (**Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object.) then contradicts r49, because it still lists requests. Readings: (a) retire r35 and add r50 '**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.', so the text and JSON outputs agree; (b) keep r35 as it is, so the text and JSON outputs differ. Recommended: (a).
- Are the lines of work-queue approved as drafted? Readings: approve work-queue as drafted (recommended), or change its lines.

## Answers
- 2026-10-29: Reading (a): retire r35 and add r50 '**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.', so the text and JSON outputs agree. This follows the person's 2026-10-27 delegation: answer every question with its recommended reading.
  by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1 and 2 are i39's gate-round-7 answers that apply round 8 dropped (work-queue r48, and r34 retired for a list without requests, which requests r46 lists); line 2 replaces work-queue r34, retired, not edited. Line 3 states the merge w206 implemented (reading B). Answer every question with its recommended reading; where none is recommended, choose the one a test can check."
- 2026-10-29: Approve work-queue as drafted (the recommended reading), under the person's 2026-10-27 delegation: "Please get the new version delivered without involving me."
  by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1 and 2 are i39's gate-round-7 answers that apply round 8 dropped (work-queue r48, and r34 retired for a list without requests, which requests r46 lists); line 2 replaces work-queue r34, retired, not edited. Line 3 states the merge w206 implemented (reading B). Answer every question with its recommended reading; where none is recommended, choose the one a test can check."
