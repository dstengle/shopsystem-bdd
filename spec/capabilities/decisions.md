---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/decisions
title: Decisions
narrator: the person
group: service
area: specification
specifies: service decisions, object design-decision
language: codified-2
retired: []
unbuilt: []
---

# Decisions

## Purpose
The design-decisions of this bounded context: entered with a tier, superseded by a later one, indexed, and held by the
check to their tier's enforcement.

## Behaviour

### [g1] A decision in force with no tier is a warning
- [r1] While a design-decision is not `superseded` or `rejected` and the design-decision has no tier, when the person
  validates this specification, the specification service shall return `w_untiered`.

### [g2] A `check` decision names its test
- [r2] While the tier of a design-decision is `check` and no test enforces the design-decision, if the person validates
  this specification, then the specification service shall fail the check and name `v_d6`.

### [g3] A `requirement` decision names its requirement
- [r3] While the tier of a design-decision is `requirement` and no requirement enforces the design-decision, if the
  person validates this specification, then the specification service shall fail the check and name `v_d7`.

### [g4] `model decisions --check` runs the tests of the `check` decisions
- [r4] While the tier of a design-decision is `check` and a test enforces the design-decision, when the person rebuilds
  the decisions index with the audit, the decisions service shall return the verdict of the test.

### [g5] `model decisions --check` names each failing decision
- [r5] While the tier of a design-decision is `check` and a test whose verdict is `failed` enforces the design-decision,
  if the person rebuilds the decisions index with the audit, then the decisions service shall fail the check and name
  the design-decision.

### [g6] An accepted decision supersedes no accepted decision
- [r6] While a design-decision whose status is `accepted` supersedes a design-decision whose status is `accepted`, if
  the person validates this specification, then the specification service shall fail the check and name `v_d8`.

### [g7] `work decision` writes and commits a decision and the decisions index
- [r7] When the person enters a design-decision, the decisions service shall keep the design-decision and the decisions
  index.

### [g8] `work decision` refuses a decision with no tier
- [r8] If the person enters a design-decision without a tier, then the decisions service shall refuse the request and
  name the tier.

### [g9] `work decision` refuses a decision with no summary
- [r9] If the person enters a design-decision without a summary, then the decisions service shall refuse the request and
  name the summary.

### [g10] `work decision` refuses a decision with no text
- [r10] If the person enters a design-decision without a wording, then the decisions service shall refuse the request
  and name the wording.

### [g11] `work decision` with `--verified-by` writes a route
- [r11] When the person enters a design-decision with a route, the decisions service shall keep a design-decision that
  has a route.

### [g12] the check names a universal condition no decision verifies
- [r12] When the person validates this specification, the specification service shall return every universal condition
  that no design-decision verifies.

### [g13] the check refuses a route outside the four
- [r13] While the kind of a route of a design-decision is not `scenario`, `check`, `judgement` or `monitor`, if the
  person validates this specification, then the specification service shall fail the check and name the design-decision.

### [g14] `work decision --supersedes` marks the decision it replaces superseded
- [r14] When the person enters a design-decision over a design-decision whose status is `accepted`, the decisions
  service shall set the status of the design-decision to `superseded` and keep the design-decision.

### [g15] `work decision --supersedes` refuses a decision not in force
- [r15] If the person enters a design-decision over a design-decision whose status is not `accepted`, then the decisions
  service shall refuse the request and name the design-decision.

### [g16] `model decisions` writes the decisions index
Restates: design-model-check#r14@0.29, spec-integration#r22@0.29.
- [r16] When the person rebuilds the decisions index, the decisions service shall keep the decisions index.

### [g17] A decision with no id
Restates: design-model-check#r29@0.29.
- [r17] While a design-decision has no id, if the person validates this specification, then the specification service
  shall fail the check and name the design-decision.

### [g18] `model decisions --check` refuses an index that lacks an index entry
Restates: design-model-check#r15@0.29.
- [r18] While a design-decision has an index entry that a decisions index does not hold, if the person rebuilds the
  decisions index with the audit, then the decisions service shall fail the check, name the decisions index and change
  no file.

### [g19] `model decisions --check` passes a current index
Restates: design-model-check#r37@0.29.
- [r19] While no decisions index lacks an index entry, when the person rebuilds the decisions index with the audit, the
  decisions service shall complete the request.

### [g20] A decision with no Decision section
- [r20] While a design-decision has no section whose heading is `Decision`, if the person validates this specification,
  then the specification service shall fail the check and name the design-decision.

### [g21] `work decision --amend` adds an enforcer to an accepted decision
- [r21] When the person amends a design-decision whose status is `accepted` with an enforcer, the decisions service shall keep a design-decision that has an enforcer and keep the decisions index.

### [g22] `work decision --amend` adds a foundation to an accepted decision
- [r22] When the person amends a design-decision whose status is `accepted` with a foundation, the decisions service shall keep a design-decision that has a foundation and keep the decisions index.

### [g23] `work decision --amend` refuses a decision not in force
- [r23] If the person amends a design-decision whose status is not `accepted`, then the decisions service shall refuse the request and name the design-decision.

### [g24] `work decision --amend` with ids the decision names already changes nothing
- [r24] While a design-decision whose status is `accepted` has an enforcer, when the person amends the design-decision with the enforcer, the decisions service shall complete the request and change no file.

### [g25] `work decision --amend` with a foundation the decision names already changes nothing
- [r25] While a design-decision whose status is `accepted` has a foundation, when the person amends the design-decision with the foundation, the decisions service shall complete the request and change no file.

### [g26] A superseded decision may name a requirement a later line retired
- [r26] While a requirement retires the requirement id of a requirement that enforces a design-decision whose status is `superseded`, when the person validates this specification, the specification service shall complete the request.

