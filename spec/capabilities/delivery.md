---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/delivery
title: Delivery
narrator: the person delivering an initiative
group: service
rests_on: [design-decision/a-script-supervises-delivery, design-decision/gate-on-behaviour-lines, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/review-of-work-items]
formulated_as: features/delivery.feature
retired: []
---

# Delivery

## Purpose
Turns an initiative's formulated capability-proposals into drafted work-items and has `work run` deliver them. It
is `delivering-an-initiative`, run by the session the person talks to; it drafts from the spec and the feature
files, never the code, and reads what `work run` ends with, never what its workers write. A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what running it shows.

## Behaviour
- [r1] **When** the person asks to deliver an initiative, `delivering-an-initiative` shall draft with `work add` work-items that between them accept each requirement the initiative's `formulated` capability-proposals add or change.
- [r2] `delivering-an-initiative` shall draft from `spec/`, `features/` and `.shop/work/` alone, reading no code.
- [r3] **When** the work-items are drafted, `delivering-an-initiative` shall commit them alone.
- [r4] **When** the drafted work-items are committed, `delivering-an-initiative` shall start `work run` on the initiative.
- [r5] **While** `work run` runs, `delivering-an-initiative` shall read nothing its workers write.
- [r6] **When** `work run` exits, `delivering-an-initiative` shall show the person each work-item's status and each open question, as `work run` printed them.
- [r7] **If** `delivering-an-initiative` cannot do what it was asked, then `delivering-an-initiative` shall stop, saying why, and change nothing.

## Implementation, may change
- `skills/delivering-an-initiative/SKILL.md`. It shows the drafted work-items as one table (name, accepts, risk);
  it runs `work run` as a background command and is woken when it exits.

## Not yet
- Rules for cutting work-items (one unknown, one capability, risk, `blocked_by`, Retires, checks for guarantees),
  questions on a requirement with two readings, recording rulings and running again, budgets, formulation
  questions (see skeleton-notes.md).
