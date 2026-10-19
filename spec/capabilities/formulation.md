---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/formulation
title: Formulation
narrator: the person who approved the lines
group: service
rests_on: [design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/held-scenarios, design-decision/controller-per-spec-round]
formulated_as: features/formulation.feature
retired: []
---

# Formulation

## Purpose
Writes the acceptance-scenarios for approved Behaviour lines, one feature file per capability, from the
narrator's side and without sight of the code. It is `formulating-features`, run in a `initiative-round` that
dispatches `feature-formulator`s. It decides nothing: a line with two readings comes back as a question.

## Behaviour
- [r1] **When** lines are approved, each added or changed line with one reading has its scenarios in its capability's feature file `features/<name>.feature`: one scenario or one outline, or one scenario per reason for a line every call must keep (r9); every scenario that is not held formulates a line.
- [r2] Formulated scenarios are committed without being shown to the person for approval.
- [r3] **If** a line admits two readings, it gets no scenario and the person is shown the question with its two readings; the rest of the capability is formulated.
- [r4] **When** a line is changed or removed and its old scenario passes today, the old scenario stays in the suite tagged `@holding`, with " (held)" on its title and what it is held for, until a slice retires it.
- [r5] **When** a line is changed or removed and its old scenario does not pass today, the old scenario is replaced or removed.
- [r6] **When** feature files are committed, `features bindings` reports that every binding names a scenario, and the commit holds only the feature files and the test files `features rebind` changed.
- [r7] **When** an existing feature file is changed, every scenario not added, changed or removed is byte for byte as it was, tags included.
- [r8] A feature file begins `# formulated from spec/capabilities/<name>.md`, then `Feature: <title>`, then `Narrator: <narrator>`.
- [r9] A line every call must keep is formulated as one scenario per reason the line gives, each with one representative call.
- [r10] **When** slicing hands back a scenario with evidence, the scenario is rewritten to fit its line and the evidence, or a question with two readings goes to the person.
- [r11] Each scenario carries the tag `@r<n>` of the one line it formulates, on the scenario's tag line, and its title is free.
- [r12] A scenario tagged `@holding` keeps the `@r<n>` tag it had and formulates no line.
- [r13] **Where** `model check` can run, **when** feature files are committed, it reports no scenario that names no line or two, and no added or changed line without a scenario; **where** it cannot, the round says so and checks coverage by hand.
- [r14] **When** a scenario uses a word its context's glossary avoids, the scenario is reworded to its line through the small-change path, without a further gate.

## Implementation, may change
- The session dispatches `initiative-round` with the job `formulate`; the round dispatches one `feature-formulator`
  a capability with the brief in the skill, checks coverage one to one, runs each old scenario alone before
  replacing it, uses `features hold`, `features rebind` and `features bindings`, splices and commits.
- A scenario's title usually restates its line's condition, though the `@r<n>` tag is what names the line; Then lines name a refusal's reason, never message text.

## Not yet
None.
