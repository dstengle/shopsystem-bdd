---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-18-session-handoff-after-release-0-37-0
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-18
---

# Session handoff after release 0.37.0

Where the session of 2026-11-17/18 left things, for the next session. Standing direction: directive-1 (merge, release, decide when the person is away); directive-2 to -4 are shown at SessionStart.

## State

- Batch-46 merged (PR #69: b346, b289, b324, b333) and measured. Release 0.37.0 merged (PR #70) and tagged `v0.37.0`: batches 43-46. The plugin installed on this machine was updated to 0.37.0 before a restart.
- No batch open. Ready: b318, b309, b334.
- The REST contract design, `.shop/records/2026-11-17-rest-contract/design.md` (b348, b42, b241): the HTTP pack ("a client calls `GET /feed`", return, respond with a status, a body, a caller), one OpenAPI document whose schemas are read into the model and whose prose is generated from the lines, a check of lines against the document both ways, scenarios run against the server through a test-only seeding endpoint. Written with the person and checked by a fresh builder; NOT yet approved by the person. Nothing is planned or shaped from it until they approve it. Later designs, in order: terms and schema fragments proposed in a request (b42), a contract published and pulled (b348, approach A: pinned copy under `.shop/contracts/<ctx>/`), the domain map and asking the product.
- b42 re-rated high urgency and b348 added (quote-49): the person's first product (web and feed contexts) already needs a term its upstream lacks.

## Proposed next, awaiting the person's go

1. Batch-47 with b318, b309, b334.
2. In parallel, a shaping round (one agent per item, `skills/shaping-items/parallel-brief.md`) for b340 (`work batch start` slow when items add terms), b341 (two items making one new capability overwrite each other), b256 (pytest-bdd 9 drops the unbuilt xfails), b347 and b349 (from batch-46's review); what becomes ready goes into batch-48.

## Traps seen this session

- A batch driver stops while a fix subagent is still out ("waiting for ..."); check `work batch status` and resume it, telling it to run commands in the foreground.
- `.github/copilot-instructions.md` is untracked and not this session's; left alone.
