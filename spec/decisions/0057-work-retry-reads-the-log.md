---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-retry-reads-the-log
summary: "`work retry` returns a `failed` work-item to the status before that `log.jsonl` gives in its transition into `failed`, so a work-item whose push failed after a transition's commit returns to the status that transition made."
date: 2026-10-22
status: proposed
source: [review-finding/2026-10-22-0-22-0-final-review, observation/2026-10-22-deferred-from-0-22-0, design-decision/a-failed-work-item]
by: "the coordinator's recommendation, the person having delegated the drafting decisions to it on 2026-10-22; the design note 2026-10-22-deferred-findings-design (0.23.0, part 1)"
---

# 0057. work retry reads the status before `failed` from the log

## Context

Work-queue r8 returned a `failed` work-item to "the status it had before the failed stage". When the fault is the push
after a transition's commit, the transition is already made and logged, and that phrase reads two ways.

## Alternatives

- The status the work-item had before that transition, as if the transition had not been made.
- The status that transition made, which `log.jsonl` gives as the status before in the transition into `failed`.

## Decision

`work retry` returns a `failed` work-item to the status that `log.jsonl` gives it, in the transition into `failed`,
as its status before: when the fault was the push after a transition's commit, the work-item returns to the status
that transition made, not the one before it.
