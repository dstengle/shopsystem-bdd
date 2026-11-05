---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/delivery
title: Delivery
narrator: the person delivering an initiative
group: guarantees
rests_on: [design-decision/a-script-supervises-delivery, design-decision/gate-on-behaviour-lines, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/review-of-work-items, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator]
language: codified-1
retired: []
---

# Delivery

## Purpose
Has `work run` deliver an initiative and shows the person what it ends with. It is `delivering-an-initiative`; it
drafts no work-item but a trial's fix (`work run` drafts the rest, supervision), starts no `claude -p` session and
merges no branch itself, and reads what `work run` ends with, never what its workers write
(design-decision/the-context-runs-without-a-coordinator). A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Terms

- **`delivering-an-initiative`** (actor): the skill that has `work run` deliver an initiative and shows the person what it ends with.
- **disallowed tool** (kind): a tool a worker needs that `work run` does not allow it.
- **note** (event): a line naming an event is appended to an initiative's ledger with `work note`. Forms: notes, noted.

## Behaviour

### [g1] Asked to deliver an initiative, the skill starts a delivery
Restates: r4@0.29.
- [r1] When the person runs `delivering-an-initiative` on an initiative, `delivering-an-initiative` shall start a
  delivery.

### [g2] The skill reads nothing a worker writes
Restates: r5@0.29.
- [r2] `delivering-an-initiative` shall not read a result or read a report.

### [g3] When the delivery ends, the person sees each status and each question
Restates: r6@0.29.
- [r3] When a delivery ends, `delivering-an-initiative` shall show the status of every work-item and show every
  question.

### [g4] A refused delivery says why and changes nothing
Restates: r7@0.29.
- [r4] If a delivery is refused, then `delivering-an-initiative` shall show the reason and change nothing.

### [g5] A defect a trial finds becomes a drafted work-item
Restates: r10@0.29.
- [r5] When a trial finds a defect, `delivering-an-initiative` shall write a work-item that is `drafted`.

### [g6] The skill changes no code, starts no session and merges no branch
Restates: r11@0.29, r12@0.29, r19@0.29, r20@0.29.
- [r6] `delivering-an-initiative` shall not change a module, start a session, merge a work-item branch or write a
  scenario.

### [g7] A tool a worker needs is put to the person
Restates: r21@0.29.
- [r7] When a worker finds a disallowed tool, `delivering-an-initiative` shall ask a question and name a stage.

### [g8] A change `work run` cannot deliver is put to the person
Restates: r22@0.29.
- [r8] If `work run` refuses a work-item, then `delivering-an-initiative` shall ask a question and change nothing.

### [g9] A dispatch is given a brief
Restates: r13@0.29.
- [r9] When `delivering-an-initiative` starts a dispatch, `delivering-an-initiative` shall give the dispatch a brief.

### [g10] A dispatch's files are read only to decide what to do next
Restates: r14@0.29.
- [r10] When a dispatch ends, `delivering-an-initiative` shall read only a file.

### [g11] An answer is noted in the ledger
Restates: r15@0.29.
- [r11] When the person gives an answer, `delivering-an-initiative` shall note the answer.

## Implementation, may change
- `skills/delivering-an-initiative/SKILL.md`. It runs `work run` as a background command and is woken when it
  exits, and shows each work-item's status and each open question as `work run` printed them.
- A dispatch is asked to reply in a few lines and leave the rest in files. A fix that needs a new scenario goes
  through a capability-proposal, never to the implementer.

## Not yet
- Writing answers and starting `work run` again, budgets (see skeleton-notes.md).

## Dropped
