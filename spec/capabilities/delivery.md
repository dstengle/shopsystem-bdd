---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/delivery
title: Delivery
narrator: the person delivering an initiative
group: guarantees
rests_on: [design-decision/a-script-supervises-delivery, design-decision/gate-on-behaviour-lines, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/review-of-work-items, design-decision/the-session-keeps-the-gate, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked]
retired: [r16]
---

# Delivery

## Purpose
Turns an initiative's formulated capability-proposals into drafted work-items and has `work run` deliver them. It
is `delivering-an-initiative`, used by the session the person talks to; it drafts from the spec and the feature
files, never the code, and reads what `work run` ends with, never what its workers write. A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Behaviour
- [r1] **When** the person asks to deliver an initiative, `delivering-an-initiative` shall draft with `work add` work-items that between them accept each requirement the initiative's `formulated` capability-proposals add or change.
- [r17] **When** `delivering-an-initiative` drafts a work-item, `delivering-an-initiative` shall list under the work-item's `## Retires` each scenario tagged `@deprecated` whose `@r<n>` tag names a requirement the work-item accepts.
- [r18] **If** a scenario the initiative's formulation added or reworded names a requirement no drafted work-item accepts, then `delivering-an-initiative` shall stop, naming the scenario, and commit no work-item.
- [r2] `delivering-an-initiative` shall draft from `spec/`, `features/` and `.shop/work/` alone, reading no code.
- [r3] **When** the work-items are drafted, `delivering-an-initiative` shall commit them alone.
- [r4] **When** the drafted work-items are committed, `delivering-an-initiative` shall start `work run` on the initiative.
- [r5] **While** a delivery by `work run` lasts, `delivering-an-initiative` shall read nothing its workers write.
- [r6] **When** `work run` exits, `delivering-an-initiative` shall show the person each work-item's status and each open question, as `work run` printed them.
- [r7] **If** `delivering-an-initiative` cannot do what it was asked, then `delivering-an-initiative` shall stop, saying why, and change nothing.
- [r8] **When** `delivering-an-initiative` finds every requirement of the initiative accepted by a work-item, `delivering-an-initiative` shall start `work run` without drafting a work-item.
- [r9] **When** `delivering-an-initiative` drafts work-items, `delivering-an-initiative` shall give each work-item at most five requirements to accept.
- [r10] **When** a review or a trial finds a fix to code, `delivering-an-initiative` shall draft the fix as a work-item for `work run` to deliver.
- [r11] `delivering-an-initiative` shall change no code itself.
- [r12] **When** a fix needs a new scenario or a new row of a scenario's examples, `delivering-an-initiative` shall send it to the `feature-formulator` through a `formulate` round of `initiative-round`, never to the implementer.
- [r13] **When** `delivering-an-initiative` dispatches an agent, `delivering-an-initiative` shall ask it to reply in a few lines and leave the rest in files.
- [r14] **When** a dispatch `delivering-an-initiative` started has replied, `delivering-an-initiative` shall read a file the dispatch wrote only to decide what to do next.
- [r15] **When** the person gives an answer, `delivering-an-initiative` shall append one line naming it to the initiative's ledger with `work note`.

## Implementation, may change
- `skills/delivering-an-initiative/SKILL.md`. It shows the drafted work-items as one table (name, accepts, risk);
  it runs `work run` as a background command and is woken when it exits.

## Not yet
- Rules for cutting work-items (one unknown, one capability, risk, `blocked_by`, checks for guarantees),
  questions on a requirement with two readings, writing answers and starting `work run` again, budgets, formulation
  questions (see skeleton-notes.md).
- `delivering-an-initiative` accepting `merged` capability-proposals as well as `formulated` ones (i8, delivery 1).
