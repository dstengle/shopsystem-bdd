---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/uncommitted-work
kind: capability-proposal
part_of: initiative/i17
status: merged
date: 2026-10-22
argues: [work-queue]
adds: [work-queue#r9]
---

# work-queue: `work` commits what it changes

From the 0.22.0 final review's Critical finding (C1): `work retry` and `work add` wrote without committing, and the
next `work run`'s put-back undid them. The person, 2026-10-22: "I want a release" — the Critical is fixed, the rest
deferred.
