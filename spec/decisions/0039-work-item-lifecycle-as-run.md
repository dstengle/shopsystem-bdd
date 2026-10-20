---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-item-lifecycle-as-run
summary: "work run moves work-items drafted → researched → planned → ready → claimed → done → green, with awaiting-ruling for every question to the person, and runs the suite itself before an item is done; a stopped or refused implementer releases its claim."
date: 2026-10-19
status: proposed
supersedes: design-decision/suite-record-holds
source: [initiative/i10]
by: "docs/design-model/grammar.md v3 section 5"
---

# 0039. The work-item lifecycle as work run runs it

## Decision

Transitions and their guards:

| from → to | made by | guard |
|---|---|---|
| drafted → researched | researcher's result | DONE, a non-empty file set, the notes file present |
| researched → planned | planner's result | DONE, the plan file present, a final file set |
| planned → awaiting-ruling | planner's result | QUESTION, each question with its readings |
| planned → ready | work | every `blocked_by` green; no claimed item's file set shares a path |
| ready → claimed | work, as it starts an implementer | the same, at that moment |
| claimed → done | implementer's result | DONE; rebased on the initiative branch; commits inside the file set; accepted scenarios (or check) pass; the suite fails nothing the last record passed |
| claimed → ready | work, on a refused `work claim` | the holder is claimed (EXTENSION: release) |
| claimed → awaiting-ruling | implementer's result | BLOCKED, HAND-BACK, NEEDS_CONTEXT, a fourth PARTIAL, a second failed stage, a conflict (EXTENSION) |
| awaiting-ruling → planned | the person, `work rule` | every open question answered |
| done → green | review | no finding to fix now, every fix work-item for it green, its scenarios pass at the head |
| any but claimed, green → withdrawn | the person, `work withdraw` | — |

A ruling is written into the work-item under `## Rulings` in the person's words; the next implementer reads it, and
no planner runs again. The suite record is `work run`'s own run after each rebase, logged in `log.jsonl` and given
in each implementer's brief; implementers do not log suite records.

## Consequences

Two transitions are extensions against grammar.md v3, which has awaiting-ruling only from planned: a claimed item
goes back to ready or to awaiting-ruling, so that a claim is never kept by a stopped worker.
