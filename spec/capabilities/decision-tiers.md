---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/decision-tiers
title: Decision tiers
narrator: a person or session keeping the decisions
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r1, r2, r3, r4, r5, r6]
---

# Decision tiers

## Purpose
Decisions return, in three tiers (design goal 7). A `check` decision names the test that enforces it, and the test
runs with the suite and at the pull request; a `requirement` decision names the requirement it is written as; a
`judgement` decision is read by the batch's plan and by the pull request's review. `model check` keeps each decision
to its tier, and keeps a superseded decision marked so.

## Terms
- **untiered** (condition of design-decision): a design-decision whose frontmatter gives no `tier`.
- **untested** (condition of design-decision): A design-decision is untested when the design-decision is enforced by no test.
- **unrequired** (condition of design-decision): A design-decision is unrequired when the design-decision is enforced by no requirement.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| design-decision | enforced by | requirement | |

## Behaviour

### [g1] A decision with no tier is a warning
- [r1] When the person runs `model check` on a design-decision that is untiered, `model` shall print `w_untiered`.

### [g2] A `check` decision names its test
- [r2] While a design-decision is `check` and the design-decision is untested, if the person runs `model check`, then
  `model` shall exit with an error naming `v_d6`.

### [g3] A `requirement` decision names its requirement
- [r3] While a design-decision is `requirement` and the design-decision is unrequired, if the person runs `model
  check`, then `model` shall exit with an error naming `v_d7`.

### [g4] `model decisions --check` runs the tests of the `check` decisions
- [r4] While a design-decision is `check` and the design-decision is enforced by a test, when the person runs `model
  decisions --check`, `model` shall use the test.

### [g5] `model decisions --check` names each failing decision
- [r5] While a design-decision is `check` and the design-decision is enforced by a test that is failing, if the person
  runs `model decisions --check`, then `model` shall exit with an error naming the design-decision.

### [g6] A superseded decision is `superseded`
- [r6] While a design-decision that is `accepted` supersedes a design-decision that is `accepted`, if the person runs `model check`, then
  `model` shall exit with an error naming `v_d8`.

## Implementation, may change

- `w_untiered` is a warning while plan 6 sorts the 74 decisions into their tiers; a decision gives its tier as `tier:`
  in its frontmatter.

## Not yet
- The tier-1 decision checks in the readiness bar: the design's bar includes "the tier-1 decision checks hold for any
  constraint the item states", but `passing` leaves them out until plan 6 builds `model decisions --check`; plan 6 adds
  them to the bar.
