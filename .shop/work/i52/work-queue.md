---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i52-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i52
status: awaiting-answer
argues: [work-queue]
date: 2026-10-28
adds: [work-queue#r50, work-queue#r51]
changes: []
removes: [work-queue#r23]
---

# work-queue

The drafts of this proposal are in .shop/work/i52/runs/work-queue/3-integrate/drafts/round-1/.

## Questions
- work-queue r23 and r40: which `work` commands leave a finished initiative's `done` to `work run`? Lines: r23 CHANGED. Now: "**When** a `work` command other than `work withdraw` makes it true by its change that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." Was: "**When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." r40 ADDED: "**When** `work withdraw` leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now." Readings: (a) only `work withdraw`, as drafted (the request names only it); (b) every `work` command: r23 removed (id retired) and r40 reads "**When** a `work` command's change leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now." Recommended: (b), the writer's recommendation; (a) is the narrower reading, as the request names only `work withdraw`.
- work-queue r41: should the logged line also hold the time and who set the status, as r5's does? Line: r41 ADDED: "**When** `work` sets an initiative's status, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status before and after the transition." Readings: (a) yes: "...with the time, the initiative, its status before and after, and who set it."; (b) only the initiative and the status before and after, as drafted. Recommended: (b), what the request asks; (a) if the log is to be an audit trail like r5's.
- work-queue r41: does `work start` writing a `proposed` initiative count as setting its status? Line r41 as in the question above. Readings: (a) yes, a further line: "**When** `work start` writes an initiative, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status `proposed`."; (b) no, as drafted (r41 covers only transitions). Recommended: (b).
- work-queue r41: should the `log.jsonl` line r41 writes be committed with the initiative's file (work-queue r9)? Readings: (a) yes, r9 changed or a new line: "**When** `work` sets an initiative's status, `work` shall commit on the current branch the initiative's file and the `log.jsonl` line it wrote."; (b) no line, as drafted. Recommended: (b), unless the log is to be kept in git, in which case (a).
- work-queue r23 (REMOVED, id retired; was: "**When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`."), with r50 ADDED ("**When** a `work` command's change leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now."): the Purpose of work-queue says `work` "makes it `done` when its work and the requests it raised are", which r23's removal contradicts. Readings: (a) Purpose stays as it is; (b) Purpose reads "...it starts an initiative from an `accepted` request and leaves its `done` to `work run`; ...". Recommended: (b).
- work-queue r23 (REMOVED): the Implementation, may-change note "r23: a request names the initiative in its `part_of` or its `source`." points at a retired id. Readings: (a) it stays; (b) it is removed, or moved to the supervision line that sets `done` if that line uses the same condition. Recommended: (b).
- work-queue r51 (ADDED: "**When** `work` sets an initiative's status, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the time, the initiative, its status before and after, and who set it."): with r23 gone, no work-queue line has `work` set an initiative's status (r22 writes `proposed`, which is not a transition), so r51 has no trigger here unless another initiative's draft adds one. Readings: (a) r51 stays as a standing rule; (b) r51 is held until a line that sets an initiative's status exists. Recommended: (a).

## Answers
- 2026-10-28: Q1, r23 and r40: reading (b), every work command leaves a finished initiative's done to work run (r23 retired) (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q2, r41's logged line: reading (a), with the time, the initiative, its status before and after, and who set it, as r5's lines do (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q3, work start and r41: reading (b), r41 covers only transitions (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q4, committing r41's line: reading (b), no line (answered by the coordinator under the person's delegation, 2026-10-28)

## Faults
- the session answering work-queue's question faulted: while its answerer worked, .shop/work/i61/spec-integration.md, .shop/work/i61/runs/spec-integration/3-answer/brief.md, .shop/work/i61/runs/spec-integration/3-answer/result.json, .shop/work/i61/runs/spec-integration/3-answer/session.json changed in the repository's own checkout and not committed; work run put them back
