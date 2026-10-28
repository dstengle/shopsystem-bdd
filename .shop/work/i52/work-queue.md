---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i52-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i52
status: awaiting-answer
argues: [work-queue]
adds: [work-queue#r40, work-queue#r41]
changes: [work-queue#r23]
removes: []
date: 2026-10-28
---

# work-queue

The drafts of this proposal are in .shop/work/i52/runs/i52/1-integrate/drafts/round-1/.

## Questions
- work-queue r23 and r40: which `work` commands leave a finished initiative's `done` to `work run`? Lines: r23 CHANGED. Now: "**When** a `work` command other than `work withdraw` makes it true by its change that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." Was: "**When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." r40 ADDED: "**When** `work withdraw` leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now." Readings: (a) only `work withdraw`, as drafted (the request names only it); (b) every `work` command: r23 removed (id retired) and r40 reads "**When** a `work` command's change leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now." Recommended: (b), the writer's recommendation; (a) is the narrower reading, as the request names only `work withdraw`.
- work-queue r41: should the logged line also hold the time and who set the status, as r5's does? Line: r41 ADDED: "**When** `work` sets an initiative's status, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status before and after the transition." Readings: (a) yes: "...with the time, the initiative, its status before and after, and who set it."; (b) only the initiative and the status before and after, as drafted. Recommended: (b), what the request asks; (a) if the log is to be an audit trail like r5's.
- work-queue r41: does `work start` writing a `proposed` initiative count as setting its status? Line r41 as in the question above. Readings: (a) yes, a further line: "**When** `work start` writes an initiative, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status `proposed`."; (b) no, as drafted (r41 covers only transitions). Recommended: (b).
- work-queue r41: should the `log.jsonl` line r41 writes be committed with the initiative's file (work-queue r9)? Readings: (a) yes, r9 changed or a new line: "**When** `work` sets an initiative's status, `work` shall commit on the current branch the initiative's file and the `log.jsonl` line it wrote."; (b) no line, as drafted. Recommended: (b), unless the log is to be kept in git, in which case (a).

## Answers
- 2026-10-28: Q1, r23 and r40: reading (b), every work command leaves a finished initiative's done to work run (r23 retired) (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q2, r41's logged line: reading (a), with the time, the initiative, its status before and after, and who set it, as r5's lines do (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q3, work start and r41: reading (b), r41 covers only transitions (answered by the coordinator under the person's delegation, 2026-10-28)
