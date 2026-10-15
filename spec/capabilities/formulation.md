---
id: shopsystem-bdd/formulation
title: Formulation
narrator: the person who approved the lines
group: service
rests_on: [decision/formulation-needs-no-second-approval, decision/spec-writers-blind-to-code, decision/held-scenarios, decision/controller-per-spec-round]
formulated_as: features/formulation.feature
retired: []
---

# Formulation

## Purpose
Writes the acceptance-scenarios for approved Behaviour lines, one feature file per capability, from the
narrator's side and without sight of the code. It is `formulating-features`, run in a `spec-round` that
dispatches `feature-formulator`s. It decides nothing: a line with two readings comes back as a question.

## Behaviour
- [r1] **When** lines are approved, each capability that changed has its feature file `features/<name>.feature` with exactly one scenario, or one outline, for each added or changed line, and no scenario without a line.
- [r2] Formulated scenarios are committed without being shown to the person for approval.
- [r3] **If** a line admits two readings, it gets no scenario and the person is shown the question with its two readings; the rest of the capability is formulated.
- [r4] **When** a line is changed or removed and its old scenario passes today, the old scenario stays in the suite tagged `@holding`, with " (held)" on its title and what it is held for, until a slice retires it.
- [r5] **When** a line is changed or removed and its old scenario does not pass today, the old scenario is replaced or removed.
- [r6] **When** feature files are committed, every scenario a test module binds by title exists, and no module stops collecting.
- [r7] **When** an existing feature file is changed, every scenario not added, changed or removed is byte for byte as it was, tags included.
- [r8] A feature file begins `# formulated from spec/capabilities/<name>.md`, then `Feature: <title>`, then `Narrator: <narrator>`.
- [r9] A line every call must keep is formulated as one scenario per reason the line gives, each with one representative call.
- [r10] **When** slicing hands back a scenario with evidence, the scenario is rewritten to fit its line and the evidence, or a question with two readings goes to the person.

## Implementation, may change
- The session dispatches `spec-round` with the job `formulate`; the round dispatches one `feature-formulator`
  a capability with the brief in the skill, checks coverage one to one, runs each old scenario alone before
  replacing it, uses `features hold`, `features rebind` and `features bindings`, splices and commits.
- Scenario titles restate the line's condition; Then lines name a refusal's reason, never message text.

## Not yet
- A scenario names its requirement by `@r<n>` and its title is free, so `rebind` is no longer needed for a re-worded line — trigger: initiative i3 is approved.
