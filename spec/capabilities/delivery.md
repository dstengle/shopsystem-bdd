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
Turns an initiative's formulated capability-proposals into drafted work-items and has `work run` deliver them,
with the person asked only what nobody else may decide. It is `delivering-an-initiative`, run by the session the
person talks to. The session drafts from the spec and the feature files, never the code; it starts `work run`
and reads what it ends with, never what its workers write. It does not change a Behaviour line or a scenario: a
question about one goes to integration or formulation.

## Behaviour
- [r1] **When** the person asks to deliver an initiative, the session drafts work-items for each of its capability-proposals that is `formulated`, and names each one it leaves out with its status.
- [r2] **When** work-items are drafted, each requirement a formulated proposal adds or changes, and that has a scenario, is accepted by exactly one of them.
- [r3] **When** a proposal changes or removes a requirement whose old scenario is deprecated, one drafted work-item lists that scenario under Retires: the one that accepts its replacement, or the one that removes what it tests.
- [r4] Each drafted work-item accepts requirements of one capability or has a check, and has one observable sentence and one unknown or none.
- [r5] Each drafted work-item's risk is `contract`, `concurrency`, `data` or `none`, and only the first three are reviewed alone.
- [r6] A drafted work-item is `blocked_by` another only when its scenarios cannot pass without the other's work.
- [r7] **Where** a capability is guarantees, its work-items have a check against the requirement's bound in place of scenarios.
- [r8] The session drafts from `spec/`, `features/` and `.shop/work/` alone and reads no code.
- [r9] **If** drafting finds a requirement that admits two readings, the session drafts no work-item for it and shows the person the question with its readings, to be answered through integrating-a-proposal.
- [r10] **When** the work-items are drafted, the session commits them alone, shows the person one table of them (name, accepts, blocked by, risk) and starts `work run` without waiting for approval.
- [r11] **If** the working tree has changes, or the branch is the repository's default branch, the session stops before drafting and says which.
- [r12] **While** `work run` runs, the session reads nothing its workers write and waits for it to exit.
- [r13] **When** `work run` exits with questions, the session shows the person each question with its readings, as `work run` printed them, and asks nothing else.
- [r14] **When** the person answers, the session records each answer with `work rule` in the person's words and starts `work run` again.
- [r15] **When** `work run` exits with every work-item green or withdrawn, the session tells the person, names the initiative's capability-proposals, and says that closing the initiative is the owner's.
- [r16] **When** `work run` exits on a budget, the session tells the person what was spent and asks whether to raise the budget, and changes nothing before the answer.
- [r17] **Where** a question says a scenario the implementer was given is wrong, the session shows it as a formulation question, and the answer goes through formulating-features or integrating-a-proposal before it is recorded with `work rule`.

## Implementation, may change
- `skills/delivering-an-initiative/SKILL.md`. Drafting uses `work add`; the session runs `work run` as a
  background command and is woken when it exits; it reads `work run`'s last lines and `work questions`.
- Thin, by one unknown: a work-item with an unknown is usually one scenario; scenarios with none that share step
  definitions go together. A refactor a review asks for is an enabling work-item `for:` the one it unblocks.

## Not yet
- Drafting work-items for a cross-context-request's upstream proposal — trigger: a request between two bounded contexts on design model v3 is accepted.
