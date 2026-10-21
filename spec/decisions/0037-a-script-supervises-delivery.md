---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-script-supervises-delivery
summary: "scripts/work run pulls an initiative's work-items through their stages, starting a fresh claude -p worker for each stage, and is the only writer of a work-item's status; no language-model session controls delivery."
date: 2026-10-19
status: accepted
supersedes: design-decision/one-batch-one-session
source: [initiative/i10, review-finding/2026-10-13-kb-and-bdd-assessment, measurement/kb-batches-32-35]
by: "sections 3 and 4"
---

# 0037. A script supervises delivery

## Decision

Delivery is a loop in a script: `work run <initiative>` reads the work-queue under `.shop/work/`, starts one
`claude -p` session per stage of a work-item (researcher `code-scout`, planner `bdd-planner`, implementer
`bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`), checks each transition's guard itself and
writes the status. The session the person talks to drafts the work-items, starts `work run`, relays the
questions it ends with and records the person's rulings with `work rule`. It reads no worker's output.

## Context

In kb batches 32-35 the controller session read 23-55% of a batch's cache tokens and its own turns were the
gap between span and agent-minutes; "one batch, one session" was asked of it, not enforced. Rules a controller
was given (models, review by risk, fresh agents) were broken in the batches measured.

## Alternatives

A controller agent per batch (the assessment's recommendation 11); a shell loop with the guards in
`model check` (initiative i5). The first keeps a language model in the loop that decides nothing; the second
splits the guards from the loop that needs them.
