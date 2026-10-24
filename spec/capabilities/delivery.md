---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/delivery
title: Delivery
narrator: the person delivering an initiative
group: guarantees
rests_on: [design-decision/a-script-supervises-delivery, design-decision/gate-on-behaviour-lines, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/review-of-work-items, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator]
retired: [r16, r1, r2, r3, r8, r9, r17, r18]
---

# Delivery

## Purpose
Has `work run` deliver an initiative and shows the person what it ends with. It is `delivering-an-initiative`; it
drafts no work-item but a trial's fix (`work run` drafts the rest, supervision), starts no `claude -p` session and
merges no branch itself, and reads what `work run` ends with, never what its workers write
(design-decision/the-context-runs-without-a-coordinator). A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Behaviour
- [r4] **When** the person asks to deliver an initiative, `delivering-an-initiative` shall start `work run` on the initiative.
- [r5] **While** a delivery by `work run` lasts, `delivering-an-initiative` shall read nothing its workers write.
- [r6] **When** `work run` exits, `delivering-an-initiative` shall show the person each work-item's status and each open question, as `work run` printed them.
- [r7] **If** `delivering-an-initiative` cannot do what it was asked, then `delivering-an-initiative` shall stop, saying why, and change nothing.
- [r10] **When** a trial finds a fix to code, `delivering-an-initiative` shall draft the fix as a work-item for `work run` to deliver.
- [r11] `delivering-an-initiative` shall change no code itself.
- [r19] `delivering-an-initiative` shall start no `claude -p` session itself.
- [r20] `delivering-an-initiative` shall merge no branch itself.
- [r21] **When** a worker needs a tool that `work run` does not allow it, `delivering-an-initiative` shall put the tool to the person as a question, naming the stage.
- [r22] **If** `work run` cannot deliver a change, then `delivering-an-initiative` shall put the change to the person as a question, changing nothing itself.
- [r12] **When** a fix needs a new scenario or a new row of a scenario's examples, `delivering-an-initiative` shall send it to the `feature-formulator` through a `formulate` round of `initiative-round`, never to the implementer.
- [r13] **When** `delivering-an-initiative` dispatches an agent, `delivering-an-initiative` shall ask it to reply in a few lines and leave the rest in files.
- [r14] **When** a dispatch `delivering-an-initiative` started has replied, `delivering-an-initiative` shall read a file the dispatch wrote only to decide what to do next.
- [r15] **When** the person gives an answer, `delivering-an-initiative` shall append one line naming it to the initiative's ledger with `work note`.

## Implementation, may change
- `skills/delivering-an-initiative/SKILL.md`. It runs `work run` as a background command and is woken when it
  exits.

## Not yet
- Writing answers and starting `work run` again, budgets (see skeleton-notes.md).
