---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified
summary: "The workflow is simplified to one kind of item in a backlog, built in batches closed by one reviewed pull request, with the questions moved to a mechanical readiness bar before building."
date: 2026-11-04
status: accepted
tier: judgement
supersedes: [design-decision/gate-on-behaviour-lines, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/plans-carry-intent-not-code, design-decision/held-scenarios, design-decision/controller-per-spec-round, design-decision/scout-on-haiku-at-low-effort, design-decision/work-file-forms, design-decision/one-capability-per-proposal, design-decision/held-scenario-formulates-no-requirement, design-decision/consistency-check-on-demand, design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/plans-list-the-tests-they-break, design-decision/living-plan-to-work-items, design-decision/a-failed-work-item, design-decision/work-retry-reads-the-log, design-decision/work-items-named-by-ids, design-decision/answers-not-rulings, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/work-list-and-work-show-replace-work-status, design-decision/the-glossary-is-a-target-of-spec-work]
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design]
by: "the person, 2026-11-04, in the brainstorming of the workflow simplification"
---

# 0074. The workflow simplified

## Decision

Request, initiative and capability-proposal become one kind, the item, whose states are idea, shaped, ready, in batch and delivered (with needs input, refused and withdrawn off the main line) and whose provenance (this context, a peer or the product) is a property; the items are kept in the repository as a backlog any session can read and change, ranked by WSJF over their value, urgency and size, with dependencies that keep an item out of a batch until what it depends on is delivered; an item becomes ready only by passing a mechanical bar (its lines parse, `model logic` finds no L0 or L1 with them laid over `spec/`, `features generate` writes their scenarios), so no question gate stands in the build and a question while building parks the item; work comes in by a brainstorming with the person or by a negotiation with a peer that accepts, refuses or counter-proposes each line with no person in the loop; ready items are built together in batches, like a sprint, each one branch with its own plan on disk so any session can resume it, and one pull request; each batch's pull request gets one adversarial review of correctness and engineering quality over the batch's own commits, fixed on the branch, and the person merges; decisions return in three tiers (checkable, a requirement, judgement), each naming what enforces it; `measure` records each batch's time, tokens, cost and defects so the knobs (batch size, review depth, the readiness bar) are tuned against figures; a quote of the person keeps the conversation turns around it, committed; and the person reads names, not opaque ids.

## Context

The request, initiative and work-item process held initiatives open 18-119 h on question gates for 15-104 min of session time, and its per-task review was the largest single cost while finding little to fix; the GF conversion built with superpowers' process cost about a tenth of the estimate for `work run` (`.shop/records/2026-11-04-workflow-simplification/recon.md`).

## Alternatives

Keeping the stage pipeline and trimming its gates: rejected, the gates and per-stage reviews are the overhead. Translating the old queue into items: rejected, the queue is frozen as history and its open work entered again by hand.
