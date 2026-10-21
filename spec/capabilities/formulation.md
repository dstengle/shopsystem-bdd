---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/formulation
title: Formulation
narrator: the person who approved the lines
group: service
rests_on: [design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/held-scenarios, design-decision/controller-per-spec-round]
retired: [r8, r12]
---

# Formulation

## Purpose
Writes the acceptance-scenarios for approved Behaviour lines, one feature file per capability, from the
narrator's side and without sight of the code. It is `formulating-features`, used in a round, a dispatch of `initiative-round`, which
dispatches `feature-formulator`s. It decides nothing: a line with two readings comes back as a question.

## Behaviour
- [r1] **When** lines are approved, `formulating-features` shall write the scenarios of each added or changed line that has one reading in its capability's feature file `features/<name>.feature`, one scenario or one outline for the line, or one scenario per reason for a line every call must keep (r9).
- [r2] `formulating-features` shall commit formulated scenarios without showing them to the person for approval.
- [r3] **If** a line admits two readings, then `formulating-features` shall show the person the question with its two readings in place of that line's scenarios, formulating the rest of the capability.
- [r4] **When** a line whose old scenario passes today is changed or removed, `formulating-features` shall keep the old scenario in its feature file, deprecated and with the `@r<n>` tags it had, until the work-item whose work makes its replacement pass retires it.
- [r5] **When** a line whose old scenario does not pass today is changed or removed, `formulating-features` shall replace or remove the old scenario.
- [r6] **When** `formulating-features` commits feature files, `formulating-features` shall commit only the feature files and the test files `features rebind` changed, with `features bindings` printing that every binding names a scenario.
- [r7] **When** an existing feature file is changed, `formulating-features` shall keep every scenario not added, changed or removed byte for byte as it was, tags included.
- [r9] `formulating-features` shall formulate a line every call must keep as one scenario per reason the line gives, each with one representative call.
- [r10] **When** the person rules a scenario that a work-item's implementer handed back with evidence a formulation question, `formulating-features` shall rewrite the scenario to fit its line and the evidence, or show the person a question with two readings.
- [r11] `formulating-features` shall tag each scenario, on its tag line, `@r<n>` for each line it formulates, the lines all of one capability, whatever the scenario's title.
- [r13] **Where** `model check` is available, **when** feature files are committed, `model check` shall print no scenario that is not deprecated and names no line or lines of two capabilities, and no added or changed line without a scenario.
- [r14] **When** a scenario uses a word its context's glossary avoids, `formulating-features` shall reword the scenario to its line through the small-change path, without a further gate.
- [r22] **If** `formulating-features` cannot do what it was asked, then `formulating-features` shall stop, saying why, and commit nothing.

## Implementation, may change
- The workflow scenarios of this capability run as fixture sessions (design-decision/fixture-scenarios-under-pytest-bdd).
- The session dispatches `initiative-round` with the job `formulate`; the round dispatches one `feature-formulator`
  a capability with the template in the skill as its input, verifies coverage one to one, runs each old scenario alone before
  replacing it, uses `features deprecate`, `features rebind` and `features bindings`, splices and commits.
- A scenario's title usually restates its lines' condition, though the `@r<n>` tags are what name the lines; Then lines name a refusal's reason, never message text.
- A feature file begins `# formulated from spec/capabilities/<name>.md`, then `Feature: <title>`, then
  `Narrator: <narrator>`. A deprecated scenario is tagged `@deprecated`, has " (deprecated)" at the end of its
  title and a `Deprecated for:` line naming what replaces it.
- Where `model check` is not available, the round says so and verifies coverage by hand.

## Not yet
None.
